"""Authentication configuration for the Supermetrics SDK.

The SDK supports three mutually exclusive credential mechanisms:

1. A static API key (``api_key="api_..."``).
2. A static OAuth bearer token (``bearer_token="otok_..."``).
3. A dynamic token provider callable, re-evaluated on every request, which lets
   long-lived clients follow short-lived OAuth access tokens (including RFC 8693
   exchanged/delegated tokens) without discarding their connection pool.

Token values are treated as opaque strings; the SDK never parses or validates
their contents.
"""

from __future__ import annotations

import inspect
import re
from collections.abc import Awaitable, Callable, Coroutine
from dataclasses import dataclass
from typing import TypeAlias

from supermetrics.exceptions import SupermetricsClientError

#: A callable returning a fresh bearer token, evaluated once per request.
TokenProvider: TypeAlias = Callable[[], str]

#: A callable returning a fresh bearer token, awaited when it returns an awaitable.
AsyncTokenProvider: TypeAlias = Callable[[], Awaitable[str]] | Callable[[], str]

DEFAULT_AUTH_SCHEME = "Bearer"

#: Characters that cannot appear in an HTTP header value.
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")


def format_authorization(token: str, scheme: str = DEFAULT_AUTH_SCHEME) -> str:
    """Format a token into an ``Authorization`` header value.

    A token that already carries the scheme prefix is passed through unchanged,
    so callers can supply either ``"otok_123"`` or ``"Bearer otok_123"``.

    Args:
        token: The raw credential.
        scheme: Authorization scheme to prefix with (default ``"Bearer"``).

    Returns:
        The full header value, e.g. ``"Bearer otok_123"``.

    Raises:
        SupermetricsClientError: If the credential contains control characters or
            non-ASCII characters, neither of which can be sent in a header.
    """
    stripped = token.strip()
    # These messages deliberately never echo the credential: the HTTP layer would
    # otherwise quote the whole value in its own error, and callers log those.
    if _CONTROL_CHARACTERS.search(stripped):
        raise SupermetricsClientError(
            "Credential contains control characters (for example a newline) and cannot be "
            "sent in an Authorization header. This usually means it was read from a "
            "line-wrapped file or a YAML block scalar; strip interior whitespace before use."
        )
    if not stripped.isascii():
        raise SupermetricsClientError(
            "Credential contains non-ASCII characters and cannot be sent in an "
            "Authorization header. This usually means the value was corrupted in transit "
            "or copied with a typographic character such as a smart quote or en dash."
        )
    if stripped.lower().startswith(f"{scheme.lower()} "):
        return stripped
    return f"{scheme} {stripped}"


@dataclass(frozen=True)
class AuthConfig:
    """Resolved authentication configuration for a client instance.

    Attributes:
        static_token: The fixed credential, when the client was created with an
            ``api_key`` or ``bearer_token``. ``None`` when a provider is used.
        token_provider: The dynamic provider callable, when one was supplied.
        scheme: Authorization scheme, always ``"Bearer"`` today.
    """

    static_token: str | None = None
    token_provider: TokenProvider | AsyncTokenProvider | None = None
    scheme: str = DEFAULT_AUTH_SCHEME

    @property
    def is_dynamic(self) -> bool:
        """Whether the credential is produced by a provider on every request."""
        return self.token_provider is not None

    def static_authorization(self) -> str | None:
        """The ``Authorization`` header value for the static credential, if any."""
        if self.static_token is None:
            return None
        return format_authorization(self.static_token, self.scheme)

    def resolve_sync(self) -> str | None:
        """Resolve the current token synchronously.

        Returns:
            The token string, or ``None`` when no provider is configured (in which
            case the static header already present on the client is used).

        Raises:
            SupermetricsClientError: If the provider returned a non-string value or
                an awaitable on a synchronous client.
        """
        if self.token_provider is None:
            return None
        value = self.token_provider()
        if inspect.isawaitable(value):
            if isinstance(value, Coroutine):
                # Prevent a "coroutine was never awaited" warning before failing.
                value.close()
            raise SupermetricsClientError(
                "token_provider returned an awaitable on a synchronous client. "
                "Use SupermetricsAsyncClient for async token providers."
            )
        if not isinstance(value, str):
            raise SupermetricsClientError(f"token_provider must return a string, got {type(value).__name__}.")
        return value

    async def resolve_async(self) -> str | None:
        """Resolve the current token, awaiting the provider when it is a coroutine.

        Returns:
            The token string, or ``None`` when no provider is configured.

        Raises:
            SupermetricsClientError: If the provider returned a non-string value.
        """
        if self.token_provider is None:
            return None
        value = self.token_provider()
        if inspect.isawaitable(value):
            value = await value
        if not isinstance(value, str):
            raise SupermetricsClientError(f"token_provider must return a string, got {type(value).__name__}.")
        return value


def _is_async_callable(obj: object) -> bool:
    """Report whether calling ``obj`` produces an awaitable.

    ``inspect.iscoroutinefunction`` only recognises ``async def`` functions, so an
    instance of a class whose ``__call__`` is ``async def`` would otherwise slip
    past the synchronous client's up-front check and fail on the first request
    instead of at construction time.

    Args:
        obj: The candidate callable.

    Returns:
        ``True`` when calling it returns a coroutine.
    """
    if inspect.iscoroutinefunction(obj):
        return True
    call = getattr(obj, "__call__", None)  # noqa: B004 - probing the bound method, not truthiness
    return call is not None and inspect.iscoroutinefunction(call)


def resolve_auth_config(
    api_key: str | None,
    bearer_token: str | None,
    token_provider: TokenProvider | AsyncTokenProvider | None,
    *,
    allow_async_provider: bool,
) -> AuthConfig:
    """Validate credential arguments and build an :class:`AuthConfig`.

    Args:
        api_key: Static Supermetrics API key, if supplied.
        bearer_token: Static OAuth access token, if supplied.
        token_provider: Dynamic token provider callable, if supplied.
        allow_async_provider: ``True`` for the async client, which may await a
            coroutine provider. ``False`` for the sync client, which rejects
            ``async def`` providers up front.

    Returns:
        The resolved configuration.

    Raises:
        SupermetricsClientError: If zero or more than one mechanism was supplied,
            if a supplied value is empty, if the provider is not callable, or if a
            coroutine provider was given to the synchronous client. This is also a
            ``ValueError``.
    """
    supplied = [
        name
        for name, value in (
            ("api_key", api_key),
            ("bearer_token", bearer_token),
            ("token_provider", token_provider),
        )
        if value is not None
    ]

    if not supplied:
        raise SupermetricsClientError(
            "No credentials supplied. Provide exactly one of: api_key, bearer_token, or token_provider."
        )
    if len(supplied) > 1:
        raise SupermetricsClientError(
            f"Multiple credentials supplied ({', '.join(supplied)}). "
            "Provide exactly one of: api_key, bearer_token, or token_provider."
        )

    if token_provider is not None:
        if not callable(token_provider):
            raise SupermetricsClientError("token_provider must be callable.")
        if not allow_async_provider and _is_async_callable(token_provider):
            raise SupermetricsClientError(
                "An async token_provider cannot be used with SupermetricsClient. "
                "Use SupermetricsAsyncClient, or supply a synchronous callable."
            )
        return AuthConfig(token_provider=token_provider)

    field, static_token = ("api_key", api_key) if api_key is not None else ("bearer_token", bearer_token)
    if static_token is None or not static_token.strip():
        raise SupermetricsClientError(f"{field} must be a non-empty string.")

    return AuthConfig(static_token=static_token)


__all__ = [
    "DEFAULT_AUTH_SCHEME",
    "AsyncTokenProvider",
    "AuthConfig",
    "TokenProvider",
    "format_authorization",
    "resolve_auth_config",
]
