"""Official Python SDK for Supermetrics API."""

from supermetrics.__version__ import __version__
from supermetrics.async_client import SupermetricsAsyncClient
from supermetrics.client import SupermetricsClient

__author__ = "Supermetrics"
__email__ = "opensource@supermetrics.com"

__all__ = [
    "SupermetricsClient",
    "SupermetricsAsyncClient",
    "__version__",
]
