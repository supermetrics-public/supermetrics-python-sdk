"""Asynchronous client for Supermetrics API."""

import logging
import sys
from typing import Any

import httpx

from supermetrics.__version__ import __version__
from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics.resources.accounts import AccountsAsyncResource
from supermetrics.resources.login_links import LoginLinksAsyncResource
from supermetrics.resources.logins import LoginsAsyncResource
from supermetrics.resources.queries import QueriesAsyncResource

logger = logging.getLogger(__name__)


class SupermetricsAsyncClient:
    """Asynchronous client for Supermetrics API.

    This client provides the same interface as SupermetricsClient but all
    methods are async and must be awaited. Recommended for production
    applications that need high concurrency or integration with async
    frameworks (FastAPI, asyncio, etc.).

    Example:
        >>> import asyncio
        >>> from supermetrics import SupermetricsAsyncClient
        >>>
        >>> async def main():
        ...     async with SupermetricsAsyncClient(api_key="your-key") as client:
        ...         # Use client for API operations
        ...         pass
        >>>
        >>> asyncio.run(main())
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
        """Initialize async Supermetrics client.

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
            >>> client = SupermetricsAsyncClient(api_key="sk_live_abc123")
            >>> client = SupermetricsAsyncClient(
            ...     api_key="sk_live_abc123",
            ...     timeout=60.0,
            ...     custom_headers={"X-Custom": "value"}
            ... )
        """
        self._api_key = api_key

        # Build headers (identical to sync client)
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent or default_user_agent,
        }

        # Merge custom headers (user headers take precedence)
        if custom_headers:
            headers.update(custom_headers)

        logger.debug(f"Initializing SupermetricsAsyncClient with base_url={base_url}")

        # Create internal generated client (supports both sync and async)
        self._client = GeneratedClient(base_url=base_url, headers=headers, timeout=httpx.Timeout(timeout))

        # Attach resource adapters
        self.login_links = LoginLinksAsyncResource(self._client)
        self.logins = LoginsAsyncResource(self._client)
        self.accounts = AccountsAsyncResource(self._client)
        self.queries = QueriesAsyncResource(self._client)

        logger.info("SupermetricsAsyncClient initialized successfully")

    async def close(self) -> None:
        """Close the client and release resources.

        Important: Always call this when done, or use async context manager.

        Example:
            >>> client = SupermetricsAsyncClient(api_key="your-key")
            >>> try:
            ...     # Use client
            ...     pass
            ... finally:
            ...     await client.close()
        """
        logger.debug("Closing SupermetricsAsyncClient")
        await self._client.get_async_httpx_client().aclose()

    async def __aenter__(self) -> "SupermetricsAsyncClient":
        """Async context manager entry.

        Returns:
            The client instance.
        """
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit.

        Ensures the client is properly closed when exiting the context.
        """
        await self.close()
