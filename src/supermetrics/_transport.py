"""Per-request transport plumbing for the Supermetrics SDK.

The generated low-level client shares a single ``httpx.Client`` /
``httpx.AsyncClient`` and its endpoint functions accept no extra transport
arguments. To support per-request authorization, header injection, timeout
overrides, and raw-response capture on a *shared, pooled* client, the SDK binds
those overrides to :mod:`contextvars` and applies them from ``httpx`` event
hooks just before the request goes out.

Context variables are isolated per thread and per asyncio task, so a single
client instance can safely serve concurrent callers that each carry their own
token and tracing headers.

The three ``current_*`` variables and ``request_options`` are re-exported from the
``supermetrics`` package: async web frameworks can set them once per inbound
request (for example in middleware) and every SDK call made while handling that
request inherits them, without threading arguments through application code.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable, Coroutine, Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import partial
from typing import Any

import httpx

from supermetrics._auth import AuthConfig, format_authorization
from supermetrics.exceptions import SupermetricsClientError

#: Bearer token to use for the current request, overriding the client credential.
current_auth_token: ContextVar[str | None] = ContextVar("supermetrics_current_auth_token", default=None)

#: Extra headers to merge into the current request, taking precedence over all others.
current_request_headers: ContextVar[Mapping[str, str] | None] = ContextVar(
    "supermetrics_current_request_headers", default=None
)

#: Timeout override for the current request.
current_request_timeout: ContextVar[float | httpx.Timeout | None] = ContextVar(
    "supermetrics_current_request_timeout", default=None
)

#: Transport metadata of the most recent response in this context.
current_last_response: ContextVar[ResponseRecord | None] = ContextVar(
    "supermetrics_current_last_response", default=None
)


@dataclass(frozen=True)
class ResponseRecord:
    """Transport metadata for a single HTTP response.

    A record is written by the response event hook for *every* request, which
    lets two things work: the ``with_raw_response`` accessor, and correct error
    classification when a response body does not match the schema the generated
    models expect (a proxy returning HTML for a 502, for example).

    Attributes:
        status_code: HTTP status code of the response.
        headers: Response headers.
        content: Raw response body bytes.
        request_url: Absolute URL of the request that produced the response.
        response: The underlying ``httpx.Response``, so raised errors can carry it.
            Always set by :meth:`of`, and therefore always present for a record the
            transport produced; the default exists only for records built by hand.
            Its ``.request.headers`` still holds the ``Authorization`` header, so it
            is deliberately not included in any string representation.
    """

    status_code: int
    headers: httpx.Headers
    content: bytes
    request_url: str | None
    response: httpx.Response | None = None

    @classmethod
    def of(cls, response: httpx.Response) -> ResponseRecord:
        """Build a record from a fully-read response.

        Args:
            response: The response to snapshot.

        Returns:
            The immutable record.
        """
        # httpx.Response.request raises RuntimeError when no request is attached; it
        # does not return None, so a truthiness guard would raise instead of degrading.
        try:
            request_url: str | None = str(response.request.url)
        except RuntimeError:
            request_url = None

        return cls(
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
            request_url=request_url,
            response=response,
        )


def reset_last_response() -> None:
    """Forget the most recent response record in the current context.

    Called before an HTTP call so that a stale record from an earlier call can
    never be mistaken for the current one.
    """
    current_last_response.set(None)


def build_default_headers(
    *,
    auth: AuthConfig,
    user_agent: str,
    custom_headers: Mapping[str, str] | None,
) -> dict[str, str]:
    """Build the default header set shared by both clients.

    A static credential is baked in here so the common path costs nothing at
    request time; a dynamic provider is resolved per request by the event hook
    instead.

    The credential always outranks ``custom_headers``: without that rule the
    header set would mean different things depending on which authentication
    mechanism was chosen, because the event hook overrides ``Authorization`` for
    a provider but there is nothing to override for a static token. Per-request
    ``headers`` remain the supported way to send a different credential for one
    call.

    Args:
        auth: The client's resolved authentication configuration.
        user_agent: The ``User-Agent`` value to advertise.
        custom_headers: Client-level headers supplied by the caller.

    Returns:
        The header mapping to hand to the underlying httpx client.

    Warns:
        UserWarning: If ``custom_headers`` tries to set ``Authorization`` while a
            static credential is configured, since the credential wins.
    """
    headers = {"User-Agent": user_agent}

    static_authorization = auth.static_authorization()
    if static_authorization is not None:
        headers["Authorization"] = static_authorization

    if custom_headers:
        conflicting = [name for name in custom_headers if name.lower() == "authorization"]
        headers.update(custom_headers)
        if conflicting:
            # Drop every casing the caller used, then put the real credential back. With a
            # token provider there is nothing to put back and the hook supplies it per
            # request, so no stale Authorization is left sitting in the client defaults.
            for name in conflicting:
                headers.pop(name, None)
            if static_authorization is not None:
                headers["Authorization"] = static_authorization
            warnings.warn(
                "custom_headers set 'Authorization', which the SDK ignores: the credential "
                "comes from api_key, bearer_token, or token_provider. Pass a different "
                "credential for a single call with the per-request headers argument instead.",
                UserWarning,
                stacklevel=3,
            )

    return headers


@contextmanager
def request_options(
    *,
    auth_token: str | None = None,
    headers: Mapping[str, str] | None = None,
    timeout: float | httpx.Timeout | None = None,
) -> Iterator[None]:
    """Bind per-request overrides for the duration of the block.

    Only arguments that are not ``None`` are bound, so any ambient value already
    set by the caller (for example in web-framework middleware) is inherited by
    calls that do not override it.

    Args:
        auth_token: Bearer token to use instead of the client credential.
        headers: Extra headers merged into the request with highest precedence.
        timeout: Timeout override, in seconds or as an ``httpx.Timeout``.

    Yields:
        ``None``. The overrides are unbound on exit, including on exceptions.

    Raises:
        SupermetricsClientError: If ``auth_token`` is empty or only whitespace.

    Example:
        ```python
        from supermetrics import request_options

        with request_options(auth_token="otok_abc", headers={"X-Span-Id": "s1"}):
            client.logins.list()
        ```
    """
    if auth_token is not None:
        _validated_token(auth_token, source="auth_token")

    resets: list[Callable[[], None]] = []
    if auth_token is not None:
        resets.append(partial(current_auth_token.reset, current_auth_token.set(auth_token)))
    if headers is not None:
        resets.append(partial(current_request_headers.reset, current_request_headers.set(headers)))
    if timeout is not None:
        resets.append(partial(current_request_timeout.reset, current_request_timeout.set(timeout)))
    try:
        yield
    finally:
        for reset in reversed(resets):
            reset()


@contextmanager
def capture_last_response() -> Iterator[list[ResponseRecord | None]]:
    """Isolate and collect the response record produced inside the block.

    Yields:
        A one-element list that holds the record of the last response observed
        inside the block, or ``None`` if no request was made.
    """
    holder: list[ResponseRecord | None] = [None]
    token = current_last_response.set(None)
    try:
        yield holder
    finally:
        holder[0] = current_last_response.get()
        current_last_response.reset(token)


def _validated_token(token: str, *, source: str) -> str:
    """Reject a blank credential before it becomes a meaningless header.

    A blank token would be sent as a bare ``Authorization: Bearer``, which the API
    rejects with an opaque error that looks like a server problem rather than the
    caller's mistake.

    Args:
        token: The credential to check.
        source: Where it came from, named in the error message.

    Returns:
        The token unchanged.

    Raises:
        SupermetricsClientError: If the token is empty or only whitespace.
    """
    if not token.strip():
        raise SupermetricsClientError(f"{source} must be a non-empty string.")
    return token


def _apply_header_and_timeout_overrides(request: httpx.Request) -> None:
    """Apply the ambient header and timeout overrides to an outgoing request.

    Per-request headers are applied last so they take precedence over both the
    SDK defaults and the resolved ``Authorization`` header. ``httpx.Headers`` is
    case-insensitive, so ``{"x-span-id": ...}`` correctly replaces ``X-Span-Id``.

    Args:
        request: The outgoing request, mutated in place.
    """
    extra = current_request_headers.get()
    if extra:
        for key, value in extra.items():
            request.headers[key] = value

    timeout = current_request_timeout.get()
    if timeout is not None:
        resolved = timeout if isinstance(timeout, httpx.Timeout) else httpx.Timeout(timeout)
        request.extensions["timeout"] = resolved.as_dict()


def build_sync_event_hooks(auth: AuthConfig) -> dict[str, list[Callable[..., Any]]]:
    """Build the ``httpx.Client`` event hooks for a synchronous SDK client.

    Args:
        auth: The client's resolved authentication configuration.

    Returns:
        An ``event_hooks`` mapping suitable for ``httpx.Client``.
    """

    def on_request(request: httpx.Request) -> None:
        token = current_auth_token.get()
        source = "auth_token"
        if token is None and auth.is_dynamic:
            token = auth.resolve_sync()
            source = "token_provider"
        if token is not None:
            request.headers["Authorization"] = format_authorization(_validated_token(token, source=source), auth.scheme)
        _apply_header_and_timeout_overrides(request)

    def on_response(response: httpx.Response) -> None:
        # The SDK never streams, so the body is buffered by httpx regardless;
        # reading it here simply makes it available to error classification.
        response.read()
        current_last_response.set(ResponseRecord.of(response))

    return {"request": [on_request], "response": [on_response]}


def build_async_event_hooks(auth: AuthConfig) -> dict[str, list[Callable[..., Coroutine[Any, Any, None]]]]:
    """Build the ``httpx.AsyncClient`` event hooks for an asynchronous SDK client.

    Args:
        auth: The client's resolved authentication configuration.

    Returns:
        An ``event_hooks`` mapping suitable for ``httpx.AsyncClient``.
    """

    async def on_request(request: httpx.Request) -> None:
        token = current_auth_token.get()
        source = "auth_token"
        if token is None and auth.is_dynamic:
            token = await auth.resolve_async()
            source = "token_provider"
        if token is not None:
            request.headers["Authorization"] = format_authorization(_validated_token(token, source=source), auth.scheme)
        _apply_header_and_timeout_overrides(request)

    async def on_response(response: httpx.Response) -> None:
        # The SDK never streams, so the body is buffered by httpx regardless;
        # reading it here simply makes it available to error classification.
        await response.aread()
        current_last_response.set(ResponseRecord.of(response))

    return {"request": [on_request], "response": [on_response]}


__all__ = [
    "ResponseRecord",
    "build_default_headers",
    "build_async_event_hooks",
    "build_sync_event_hooks",
    "capture_last_response",
    "current_auth_token",
    "current_last_response",
    "current_request_headers",
    "current_request_timeout",
    "request_options",
    "reset_last_response",
]
