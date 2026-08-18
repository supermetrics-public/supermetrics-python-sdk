"""Custom exceptions for the Supermetrics SDK.

This module defines a hierarchy of exceptions that provide clear, actionable
error messages when SDK operations fail. All exceptions include contextual
information such as HTTP status codes, API endpoints, response headers, and
response bodies to aid in debugging.

Exception Hierarchy:
    SupermetricsError (base)
    ├── SupermetricsClientError (client-side configuration/validation; also a ValueError)
    ├── NetworkError (timeout, connection errors — no HTTP response)
    └── SupermetricsAPIError (HTTP 4xx / 5xx responses)          [alias: APIError]
        ├── SupermetricsAuthError (HTTP 401)                     [alias: AuthenticationError]
        ├── SupermetricsForbiddenError (HTTP 403)
        ├── SupermetricsNotFoundError (HTTP 404)
        ├── SupermetricsValidationError (HTTP 400 / 422)         [alias: ValidationError]
        ├── SupermetricsRateLimitError (HTTP 429)
        └── SupermetricsServerError (HTTP 5xx)

Backwards compatibility:
    ``APIError``, ``AuthenticationError`` and ``ValidationError`` remain importable and
    are aliases of the ``Supermetrics*`` names above. Note that ``AuthenticationError``
    and ``ValidationError`` are now subclasses of ``APIError``; catching ``APIError``
    therefore also catches them. ``except SupermetricsError`` is unaffected.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    import httpx


class SupermetricsError(Exception):
    """Base exception for all Supermetrics SDK errors.

    This is the base class for all custom exceptions in the SDK. All SDK
    exceptions inherit from this class, allowing users to catch all SDK-specific
    errors with a single except clause if desired.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code from the API response, if applicable.
        endpoint: API endpoint that was called when the error occurred.
        response_body: Raw response body from the API for detailed debugging.

    Example:
        ```python
        try:
            client.login_links.create(ds_id="GAWA", description="Test")
        except SupermetricsError as e:
            print(f"SDK Error: {e.message}")
            if e.status_code:
                print(f"HTTP Status: {e.status_code}")
            if e.endpoint:
                print(f"Endpoint: {e.endpoint}")
        ```
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        endpoint: str | None = None,
        response_body: str | None = None,
    ) -> None:
        """Initialize a SupermetricsError.

        Args:
            message: Human-readable error description.
            status_code: HTTP status code from the API response, if applicable.
            endpoint: API endpoint that was called when the error occurred.
            response_body: Raw response body from the API for detailed debugging.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        self.response_body = response_body


class SupermetricsClientError(SupermetricsError, ValueError):
    """Raised for client-side configuration and validation errors.

    These errors are detected locally, before any HTTP request is made — for
    example, supplying two competing authentication mechanisms to a client
    constructor, or supplying none at all.

    This class also inherits from :class:`ValueError`, so existing code that
    catches ``ValueError`` around client construction keeps working.

    Example:
        ```python
        try:
            SupermetricsClient()  # no credentials supplied
        except SupermetricsClientError as e:
            print(f"Configuration problem: {e.message}")
        ```
    """

    pass


class NetworkError(SupermetricsError):
    """Raised for network-level failures (timeout, connection errors, DNS errors).

    This exception indicates that a network-level failure occurred before or
    during the HTTP request. This is distinct from HTTP errors and indicates
    issues with network connectivity, DNS resolution, or request timeouts.

    Note that NetworkError instances do not have a status_code since these
    errors occur at the network layer before an HTTP response is received.

    Common causes:
        - Connection timeout
        - Connection refused (API server unreachable)
        - DNS resolution failure
        - Network connectivity issues
        - SSL/TLS errors

    Example:
        ```python
        try:
            client = SupermetricsClient(api_key="key", timeout=1.0)
            client.login_links.list()
        except NetworkError as e:
            print(f"Network error: {e.message}")
            print(f"Endpoint: {e.endpoint}")
            print("Please check your network connection")
        ```
    """

    pass


class SupermetricsAPIError(SupermetricsError):
    """Raised when the Supermetrics API returns an unsuccessful HTTP response.

    This is the base class for every HTTP-level error. In addition to the
    attributes inherited from :class:`SupermetricsError`, it preserves the full
    transport context so callers can implement retries, token refresh, and
    structured logging.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code from the API response.
        endpoint: API endpoint that was called when the error occurred.
        response_body: Raw response body from the API.
        headers: Response headers, when available.
        error_code: Machine-readable upstream error code, e.g.
            ``"ACCESS_TOKEN_INVALID"`` or ``"TRANSFER_NOT_FOUND"``.
        details: Structured error details from the response payload.
        raw_response: The underlying ``httpx.Response``, when available. Note that its
            ``.request.headers`` still contains the ``Authorization`` header, so avoid
            dumping it wholesale into logs.

    Example:
        ```python
        try:
            client.logins.get("missing")
        except SupermetricsAPIError as e:
            print(e.status_code, e.error_code, e.error_message)
            print(e.headers.get("X-Request-Id") if e.headers else None)
        ```
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        endpoint: str | None = None,
        response_body: str | None = None,
        *,
        headers: httpx.Headers | None = None,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
        raw_response: httpx.Response | None = None,
    ) -> None:
        """Initialize a SupermetricsAPIError.

        Args:
            message: Human-readable error description.
            status_code: HTTP status code from the API response.
            endpoint: API endpoint that was called when the error occurred.
            response_body: Raw response body from the API.
            headers: Response headers, when available.
            error_code: Machine-readable upstream error code.
            details: Structured error details from the response payload.
            raw_response: The underlying ``httpx.Response``, when available.
        """
        super().__init__(message, status_code=status_code, endpoint=endpoint, response_body=response_body)
        self.headers = headers
        self.error_code = error_code
        self.details = details
        self.raw_response = raw_response

    @property
    def error_message(self) -> str:
        """Alias of :attr:`message`, matching the Supermetrics error payload naming."""
        return self.message

    @property
    def retry_after(self) -> int | None:
        """Value of the ``Retry-After`` response header in seconds.

        ``None`` when the header is absent or holds an HTTP-date rather than a
        delay in seconds.
        """
        if self.headers is None:
            return None
        value: str | None = self.headers.get("Retry-After")
        if value is None:
            return None
        stripped = value.strip()
        return int(stripped) if stripped.isdecimal() else None

    @property
    def request_id(self) -> str | None:
        """Upstream request identifier from the response headers, if present."""
        if self.headers is None:
            return None
        value: str | None = self.headers.get("X-Request-Id")
        return value

    @property
    def span_id(self) -> str | None:
        """Upstream span identifier from the response headers, if present."""
        if self.headers is None:
            return None
        value: str | None = self.headers.get("X-Span-Id")
        return value


class SupermetricsAuthError(SupermetricsAPIError):
    """Raised when API authentication fails (HTTP 401).

    This exception indicates that the supplied credential is invalid, expired,
    revoked, or missing. When the upstream API reports an OAuth error code it is
    preserved in :attr:`~SupermetricsAPIError.error_code` (for example
    ``"ACCESS_TOKEN_INVALID"``) so that callers can refresh a token and retry
    instead of failing the whole operation.

    Example:
        ```python
        try:
            client.logins.list()
        except SupermetricsAuthError as e:
            if e.error_code == "ACCESS_TOKEN_INVALID":
                refresh_token()
        ```
    """

    pass


class SupermetricsForbiddenError(SupermetricsAPIError):
    """Raised when the caller is authenticated but not permitted (HTTP 403).

    Typically means the token lacks the required scope, or the account has no
    access to the requested team or resource.
    """

    pass


class SupermetricsNotFoundError(SupermetricsAPIError):
    """Raised when the requested resource does not exist (HTTP 404)."""

    pass


class SupermetricsValidationError(SupermetricsAPIError):
    """Raised when request validation fails (HTTP 400 or HTTP 422).

    Common causes:
        - Missing required parameters
        - Invalid parameter values
        - Incorrect parameter types
        - Parameters that don't conform to API constraints
    """

    pass


class SupermetricsRateLimitError(SupermetricsAPIError):
    """Raised when the API rate limit is exceeded (HTTP 429).

    Use :attr:`~SupermetricsAPIError.retry_after` to find out how long to wait
    before retrying.
    """

    pass


class SupermetricsServerError(SupermetricsAPIError):
    """Raised when the API reports a server-side failure (HTTP 5xx)."""

    pass


# --- Backwards-compatible aliases -------------------------------------------------
# These names predate the expanded taxonomy and remain part of the public API.
APIError = SupermetricsAPIError
AuthenticationError = SupermetricsAuthError
ValidationError = SupermetricsValidationError

__all__ = [
    "APIError",
    "AuthenticationError",
    "NetworkError",
    "SupermetricsAPIError",
    "SupermetricsAuthError",
    "SupermetricsClientError",
    "SupermetricsError",
    "SupermetricsForbiddenError",
    "SupermetricsNotFoundError",
    "SupermetricsRateLimitError",
    "SupermetricsServerError",
    "SupermetricsValidationError",
    "ValidationError",
]
