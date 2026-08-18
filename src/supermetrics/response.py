"""Transport-aware response envelope and ``with_raw_response`` helpers.

High-level resource methods return deserialized models for ergonomics. Callers
that also need HTTP status codes, response headers, correlation identifiers, or
raw payloads — proxies, MCP servers, tracing layers, retry logic — reach for the
``with_raw_response`` accessor on either client, which returns
:class:`ApiResponse` instead:

```python
response = client.with_raw_response.logins.get("login_abc")
print(response.status_code)  # 200
print(response.span_id)      # "a8f3b2c9e10d"
print(response.data.username)
```
"""

from __future__ import annotations

import functools
import json
from collections.abc import Awaitable, Callable
from typing import Any, Generic, ParamSpec, TypeVar

import httpx

from supermetrics._transport import ResponseRecord, capture_last_response
from supermetrics.exceptions import SupermetricsClientError

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


class ApiResponse(Generic[T]):
    """A deserialized result plus the transport metadata of the HTTP response.

    Attributes:
        data: The parsed value the plain resource method would have returned.
        status_code: HTTP status code, e.g. ``200``, ``201``, ``204``.
        headers: Response headers (case-insensitive).
        raw_body: Raw response body bytes.
        request_url: Absolute URL of the request that produced this response.
    """

    __slots__ = ("_json_cache", "_json_parsed", "data", "headers", "raw_body", "request_url", "status_code")

    def __init__(
        self,
        data: T,
        *,
        status_code: int,
        headers: httpx.Headers,
        raw_body: bytes,
        request_url: str | None = None,
    ) -> None:
        """Initialize an ApiResponse.

        Args:
            data: The parsed value returned by the resource method.
            status_code: HTTP status code of the response.
            headers: Response headers.
            raw_body: Raw response body bytes.
            request_url: Absolute URL of the originating request.
        """
        self.data: T = data
        self.status_code: int = status_code
        self.headers: httpx.Headers = headers
        self.raw_body: bytes = raw_body
        self.request_url: str | None = request_url
        self._json_parsed: bool = False
        self._json_cache: dict[str, Any] | list[Any] | None = None

    @property
    def json_body(self) -> dict[str, Any] | list[Any] | None:
        """The response body decoded as JSON, or ``None`` if it is absent or not JSON."""
        if not self._json_parsed:
            self._json_parsed = True
            if self.raw_body:
                try:
                    decoded = json.loads(self.raw_body)
                except (ValueError, UnicodeDecodeError):
                    decoded = None
                self._json_cache = decoded if isinstance(decoded, dict | list) else None
        return self._json_cache

    @property
    def span_id(self) -> str | None:
        """Upstream span identifier (``X-Span-Id``), for trace correlation."""
        value: str | None = self.headers.get("X-Span-Id")
        return value

    @property
    def request_id(self) -> str | None:
        """Upstream request identifier (``X-Request-Id``), for support and auditing."""
        value: str | None = self.headers.get("X-Request-Id")
        return value

    @property
    def retry_after(self) -> int | None:
        """Value of the ``Retry-After`` header in seconds.

        ``None`` when the header is absent or holds an HTTP-date rather than a
        delay in seconds.
        """
        value: str | None = self.headers.get("Retry-After")
        if value is None:
            return None
        stripped = value.strip()
        return int(stripped) if stripped.isdecimal() else None

    def __repr__(self) -> str:
        """Return a concise debug representation."""
        return f"ApiResponse(status_code={self.status_code}, data={self.data!r})"


def _build(data: R, record: ResponseRecord | None) -> ApiResponse[R]:
    """Assemble an :class:`ApiResponse` from a recorded response.

    Args:
        data: The value returned by the wrapped resource method.
        record: Transport metadata captured by the response event hook.

    Returns:
        The response envelope.

    Raises:
        SupermetricsClientError: If the method completed without issuing any HTTP
            request, so there is no transport metadata to report.
    """
    if record is None:
        raise SupermetricsClientError(
            "with_raw_response was used on a call that issued no HTTP request, so no transport metadata is available."
        )
    return ApiResponse(
        data,
        status_code=record.status_code,
        headers=record.headers,
        raw_body=record.content,
        request_url=record.request_url,
    )


def to_raw_response_wrapper(func: Callable[P, R]) -> Callable[P, ApiResponse[R]]:
    """Wrap a synchronous resource method so it returns an :class:`ApiResponse`.

    Args:
        func: The bound resource method to wrap.

    Returns:
        A callable with the same signature whose return value is wrapped in an
        ``ApiResponse``. For methods that issue several HTTP requests, the
        metadata describes the last response.
    """

    @functools.wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> ApiResponse[R]:
        with capture_last_response() as recorded:
            data = func(*args, **kwargs)
        return _build(data, recorded[0])

    return wrapped


def async_to_raw_response_wrapper(
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[ApiResponse[R]]]:
    """Wrap an asynchronous resource method so it returns an :class:`ApiResponse`.

    Args:
        func: The bound async resource method to wrap.

    Returns:
        A coroutine function with the same signature whose awaited value is
        wrapped in an ``ApiResponse``.
    """

    @functools.wraps(func)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> ApiResponse[R]:
        with capture_last_response() as recorded:
            data = await func(*args, **kwargs)
        return _build(data, recorded[0])

    return wrapped


__all__ = ["ApiResponse", "async_to_raw_response_wrapper", "to_raw_response_wrapper"]
