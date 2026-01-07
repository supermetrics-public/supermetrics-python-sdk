"""Custom exceptions for the Supermetrics SDK.

This module defines a hierarchy of exceptions that provide clear, actionable
error messages when SDK operations fail. All exceptions include contextual
information such as HTTP status codes, API endpoints, and response bodies
to aid in debugging.

Exception Hierarchy:
    SupermetricsError (base)
    ├── AuthenticationError (HTTP 401)
    ├── ValidationError (HTTP 400)
    ├── APIError (HTTP 404, 5xx, other HTTP errors)
    └── NetworkError (timeout, connection errors)
"""


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


class AuthenticationError(SupermetricsError):
    """Raised when API authentication fails (HTTP 401).

    This exception indicates that the provided API key is invalid, expired,
    or missing. Users should verify their API key and ensure it has not been
    revoked or expired.

    Common causes:
        - Invalid API key
        - Expired API key
        - Revoked API key
        - Missing Authorization header

    Example:
        ```python
        try:
            client.login_links.create(ds_id="GAWA", description="Test")
        except AuthenticationError as e:
            print(f"Authentication failed: {e.message}")
            print(f"Status code: {e.status_code}")
            print("Please check your API key")
        ```
    """

    pass


class ValidationError(SupermetricsError):
    """Raised when request validation fails (HTTP 400).

    This exception indicates that the request parameters are invalid or missing.
    The API rejected the request before processing due to validation failures.

    Common causes:
        - Missing required parameters
        - Invalid parameter values
        - Incorrect parameter types
        - Parameters that don't conform to API constraints

    Example:
        ```python
        try:
            client.login_links.create(ds_id="", description="Test")
        except ValidationError as e:
            print(f"Validation failed: {e.message}")
            print(f"Response: {e.response_body}")
        ```
    """

    pass


class APIError(SupermetricsError):
    """Raised for API-level errors (HTTP 404, 5xx, and other HTTP errors).

    This exception indicates that the API encountered an error while processing
    the request. This can include server-side errors, resource not found errors,
    and other HTTP errors that don't fall into the authentication or validation
    categories.

    Common causes:
        - Resource not found (404)
        - Internal server errors (500)
        - Service unavailable (503)
        - Gateway timeout (504)
        - Other HTTP errors

    Example:
        ```python
        try:
            client.login_links.get(link_id="nonexistent-id")
        except APIError as e:
            print(f"API error: {e.message}")
            print(f"Status code: {e.status_code}")
            print(f"Endpoint: {e.endpoint}")
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
