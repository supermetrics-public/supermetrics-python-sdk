"""Official Python SDK for Supermetrics API."""

from supermetrics.__version__ import __version__
from supermetrics.async_client import SupermetricsAsyncClient
from supermetrics.client import SupermetricsClient
from supermetrics.exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsError,
    ValidationError,
)

__author__ = "Supermetrics"
__email__ = "opensource@supermetrics.com"

__all__ = [
    "SupermetricsClient",
    "SupermetricsAsyncClient",
    "__version__",
    "SupermetricsError",
    "AuthenticationError",
    "ValidationError",
    "APIError",
    "NetworkError",
]
