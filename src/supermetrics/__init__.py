"""Official Python SDK for Supermetrics API."""

from supermetrics.__version__ import __version__
from supermetrics._auth import AsyncTokenProvider, TokenProvider
from supermetrics._transport import (
    current_auth_token,
    current_request_headers,
    current_request_timeout,
    request_options,
)
from supermetrics.async_client import SupermetricsAsyncClient
from supermetrics.client import SupermetricsClient
from supermetrics.exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsClientError,
    SupermetricsError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
    ValidationError,
)
from supermetrics.response import ApiResponse

__author__ = "Supermetrics"
__email__ = "opensource@supermetrics.com"

__all__ = [
    # Clients
    "SupermetricsClient",
    "SupermetricsAsyncClient",
    "__version__",
    # Authentication
    "TokenProvider",
    "AsyncTokenProvider",
    # Transport
    "ApiResponse",
    "request_options",
    "current_auth_token",
    "current_request_headers",
    "current_request_timeout",
    # Exceptions
    "SupermetricsError",
    "SupermetricsClientError",
    "NetworkError",
    "SupermetricsAPIError",
    "SupermetricsAuthError",
    "SupermetricsForbiddenError",
    "SupermetricsNotFoundError",
    "SupermetricsValidationError",
    "SupermetricsRateLimitError",
    "SupermetricsServerError",
    # Backwards-compatible exception aliases
    "AuthenticationError",
    "ValidationError",
    "APIError",
]
