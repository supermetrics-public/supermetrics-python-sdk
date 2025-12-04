"""Login Links resource adapter for Supermetrics API."""

import datetime
import logging
from typing import Any

from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_source_login_links import (
    close_login_link,
    create_login_link,
    get_login_link,
    list_login_links,
)
from supermetrics._generated.supermetrics_api_client.models.create_login_link_body import CreateLoginLinkBody
from supermetrics._generated.supermetrics_api_client.models.login_link import LoginLink
from supermetrics._generated.supermetrics_api_client.types import UNSET

logger = logging.getLogger(__name__)


class LoginLinksResource:
    """Synchronous resource adapter for Login Links operations.

    Provides a clean, Pythonic interface for managing data source login links.
    Login links are used to initiate the OAuth authentication flow for connecting
    data sources.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> link = client.login_links.create(
        ...     ds_id="GA4",
        ...     description="Google Analytics connection"
        ... )
        >>> print(f"Visit: {link.login_url}")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the LoginLinksResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def create(
        self,
        ds_id: str,
        description: str | None = None,
        expiry_time: datetime.datetime | None = None,
        **kwargs: Any,
    ) -> LoginLink:
        """Create a new login link for data source authentication.

        Creates a login link that users can visit to authenticate with a data source
        (e.g., Google Analytics, Facebook Ads). The link generates a URL that initiates
        the OAuth flow.

        Args:
            ds_id: Data source ID (e.g., "GA4", "google_ads", "facebook_ads").
            description: Optional internal description for the link. Not shown during
                authentication.
            expiry_time: Optional expiry datetime for the link. Defaults to 24 hours
                from creation if not specified.
            **kwargs: Additional API parameters (require_username, redirect_url).

        Returns:
            LoginLink: The created login link with authentication URL.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.TimeoutException: If the request times out.

        Example:
            >>> link = client.login_links.create(
            ...     ds_id="GA4",
            ...     description="Q4 Analytics Setup"
            ... )
            >>> print(link.login_url)  # URL for user to visit
            >>> print(link.link_id)    # Store this to check auth status later
        """
        logger.debug(f"Creating login link: ds_id={ds_id}, description={description}")

        # Set default expiry to 24 hours from now if not provided
        if expiry_time is None:
            expiry_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)

        # Build request body
        body = CreateLoginLinkBody(
            ds_id=ds_id,
            expiry_time=expiry_time,
            description=description if description is not None else UNSET,
            require_username=kwargs.get("require_username", UNSET),
            redirect_url=kwargs.get("redirect_url", UNSET),
        )

        # Call generated API
        response = create_login_link.sync(client=self._client, body=body)

        # Unwrap response
        if response is None or response is UNSET or response.data is None or response.data is UNSET:
            raise ValueError("API returned empty response")

        link = response.data
        logger.info(f"Created login link: id={link.link_id}, ds_id={link.ds_id}")

        return link

    def get(self, link_id: str) -> LoginLink:
        """Retrieve a login link by ID.

        Fetches the current state of a login link, including authentication status.

        Args:
            link_id: The login link ID to retrieve.

        Returns:
            LoginLink: The login link details.

        Raises:
            httpx.HTTPStatusError: If the API returns an error (e.g., 404 if not found).
            httpx.TimeoutException: If the request times out.

        Example:
            >>> link = client.login_links.get("link_123abc")
            >>> if link.login_id:
            ...     print(f"Authentication completed: {link.login_username}")
            ... else:
            ...     print(f"Status: {link.status_code}")
        """
        logger.debug(f"Retrieving login link: link_id={link_id}")

        response = get_login_link.sync(link_id=link_id, client=self._client)

        if response is None or response is UNSET or response.data is None or response.data is UNSET:
            raise ValueError("API returned empty response")

        link = response.data
        logger.info(f"Retrieved login link: id={link.link_id}, status={link.status_code}")

        return link

    def list(self) -> list[LoginLink]:
        """List all login links for the authenticated user.

        Returns:
            list[LoginLink]: List of all login links.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.TimeoutException: If the request times out.

        Example:
            >>> links = client.login_links.list()
            >>> for link in links:
            ...     print(f"{link.ds_name}: {link.status_code}")
        """
        logger.debug("Listing all login links")

        response = list_login_links.sync(client=self._client)

        if response is None or response is UNSET or response.data is None or response.data is UNSET:
            return []

        links = response.data
        logger.info(f"Retrieved {len(links)} login links")

        return links

    def close(self, link_id: str) -> None:
        """Close/expire a login link.

        Closes an open login link, preventing further authentication attempts.
        Useful for revoking access or cleaning up expired links.

        Args:
            link_id: The login link ID to close.

        Raises:
            httpx.HTTPStatusError: If the API returns an error (e.g., 404 if not found).
            httpx.TimeoutException: If the request times out.

        Example:
            >>> client.login_links.close("link_123abc")
        """
        logger.debug(f"Closing login link: link_id={link_id}")

        close_login_link.sync(link_id=link_id, client=self._client)

        logger.info(f"Closed login link: id={link_id}")


class LoginLinksAsyncResource:
    """Asynchronous resource adapter for Login Links operations.

    Async version of LoginLinksResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> link = await client.login_links.create(
        ...     ds_id="GA4",
        ...     description="Google Analytics connection"
        ... )
        >>> print(f"Visit: {link.login_url}")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the LoginLinksAsyncResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    async def create(
        self,
        ds_id: str,
        description: str | None = None,
        expiry_time: datetime.datetime | None = None,
        **kwargs: Any,
    ) -> LoginLink:
        """Create a new login link for data source authentication.

        Async version of create(). See LoginLinksResource.create() for full documentation.

        Args:
            ds_id: Data source ID (e.g., "GA4", "google_ads").
            description: Optional internal description.
            expiry_time: Optional expiry datetime.
            **kwargs: Additional API parameters.

        Returns:
            LoginLink: The created login link.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
        """
        logger.debug(f"Creating login link (async): ds_id={ds_id}, description={description}")

        if expiry_time is None:
            expiry_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)

        body = CreateLoginLinkBody(
            ds_id=ds_id,
            expiry_time=expiry_time,
            description=description if description is not None else UNSET,
            require_username=kwargs.get("require_username", UNSET),
            redirect_url=kwargs.get("redirect_url", UNSET),
        )

        response = await create_login_link.asyncio(client=self._client, body=body)

        if response is None or response is UNSET or response.data is None or response.data is UNSET:
            raise ValueError("API returned empty response")

        link = response.data
        logger.info(f"Created login link (async): id={link.link_id}, ds_id={link.ds_id}")

        return link

    async def get(self, link_id: str) -> LoginLink:
        """Retrieve a login link by ID.

        Async version of get(). See LoginLinksResource.get() for full documentation.

        Args:
            link_id: The login link ID.

        Returns:
            LoginLink: The login link details.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
        """
        logger.debug(f"Retrieving login link (async): link_id={link_id}")

        response = await get_login_link.asyncio(link_id=link_id, client=self._client)

        if response is None or response is UNSET or response.data is None or response.data is UNSET:
            raise ValueError("API returned empty response")

        link = response.data
        logger.info(f"Retrieved login link (async): id={link.link_id}, status={link.status_code}")

        return link

    async def list(self) -> list[LoginLink]:
        """List all login links.

        Async version of list(). See LoginLinksResource.list() for full documentation.

        Returns:
            list[LoginLink]: List of all login links.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
        """
        logger.debug("Listing all login links (async)")

        response = await list_login_links.asyncio(client=self._client)

        if response is None or response is UNSET or response.data is None or response.data is UNSET:
            return []

        links = response.data
        logger.info(f"Retrieved {len(links)} login links (async)")

        return links

    async def close(self, link_id: str) -> None:
        """Close/expire a login link.

        Async version of close(). See LoginLinksResource.close() for full documentation.

        Args:
            link_id: The login link ID to close.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
        """
        logger.debug(f"Closing login link (async): link_id={link_id}")

        await close_login_link.asyncio(link_id=link_id, client=self._client)

        logger.info(f"Closed login link (async): id={link_id}")
