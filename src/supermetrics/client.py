"""Synchronous client for Supermetrics API."""

import logging
import sys
from typing import Any

import httpx

from supermetrics.__version__ import __version__
from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics.resources.accounts import AccountsResource
from supermetrics.resources.login_links import LoginLinksResource
from supermetrics.resources.logins import LoginsResource
from supermetrics.resources.queries import QueriesResource

logger = logging.getLogger(__name__)


class SupermetricsClient:
    """Synchronous client for Supermetrics API.

    This client provides a type-safe, Pythonic interface to the Supermetrics
    API with full IDE autocomplete support. All methods are synchronous and
    suitable for scripts, notebooks, and REPL exploration.

    For asynchronous usage (recommended for production applications), use
    SupermetricsAsyncClient instead.

    Example:
        >>> from supermetrics import SupermetricsClient
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Use client for API operations
        >>> client.close()

        Or using context manager (recommended):
        >>> with SupermetricsClient(api_key="your-key") as client:
        ...     # Use client for API operations
        ...     pass
    """

    def __init__(
        self,
        api_key: str,
        *,
        user_agent: str | None = None,
        custom_headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        base_url: str = "https://api.supermetrics.com",
    ) -> None:
        """Initialize Supermetrics client.

        Args:
            api_key: Supermetrics API key (required). This will be sent as a
                Bearer token in the Authorization header.
            user_agent: Custom User-Agent header. Defaults to
                "supermetrics-sdk/{version} python/{py_version}".
            custom_headers: Additional HTTP headers for all requests. These
                headers will override defaults if there are conflicts.
            timeout: Request timeout in seconds (default: 30.0).
            base_url: API base URL (default: production API at
                https://api.supermetrics.com).

        Example:
            >>> client = SupermetricsClient(api_key="sk_live_abc123")
            >>> client = SupermetricsClient(
            ...     api_key="sk_live_abc123",
            ...     timeout=60.0,
            ...     custom_headers={"X-Custom": "value"}
            ... )
        """
        self._api_key = api_key

        # Build headers with Authorization and User-Agent
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent or default_user_agent,
        }

        # Merge custom headers (user headers take precedence)
        if custom_headers:
            headers.update(custom_headers)

        logger.debug(f"Initializing SupermetricsClient with base_url={base_url}")

        # Create internal generated client
        self._client = GeneratedClient(base_url=base_url, headers=headers, timeout=httpx.Timeout(timeout))

        # Attach resource adapters
        self.login_links = LoginLinksResource(self._client)
        self.logins = LoginsResource(self._client)
        self.accounts = AccountsResource(self._client)
        self.queries = QueriesResource(self._client)

        logger.info("SupermetricsClient initialized successfully")

    def close(self) -> None:
        """Close the client and release resources.

        Call this when you're done using the client to ensure proper cleanup.
        Alternatively, use the client as a context manager.

        Example:
            >>> client = SupermetricsClient(api_key="your-key")
            >>> try:
            ...     # Use client
            ...     pass
            ... finally:
            ...     client.close()
        """
        logger.debug("Closing SupermetricsClient")
        self._client.get_httpx_client().close()

    def __enter__(self) -> "SupermetricsClient":
        """Context manager entry.

        Returns:
            The client instance.
        """
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit.

        Ensures the client is properly closed when exiting the context.
        """
        self.close()
