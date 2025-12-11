"""Accounts resource adapter for Supermetrics API."""

import logging
from typing import cast

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_source import get_accounts
from supermetrics._generated.supermetrics_api_client.models.get_accounts_json import GetAccountsJson
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200 import GetAccountsResponse200
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200_data_item_accounts_item import (
    GetAccountsResponse200DataItemAccountsItem,
)
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset

logger = logging.getLogger(__name__)


class AccountsResource:
    """Synchronous resource adapter for Accounts operations.

    Provides a clean, Pythonic interface for retrieving data source accounts
    that are available for querying after authentication.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures with intuitive parameter names
    - Automatic response flattening from nested structure
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # List all accounts for a data source
        >>> accounts = client.accounts.list(ds_id="GA4")
        >>> for account in accounts:
        ...     print(f"{account.account_name} ({account.account_id})")
        >>> # Filter by login username
        >>> accounts = client.accounts.list(
        ...     ds_id="GA4",
        ...     login_usernames="user@example.com"
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the AccountsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        ds_id: str,
        login_usernames: str | list[str] | None = None,
        cache_minutes: int | None = None,
    ) -> list[GetAccountsResponse200DataItemAccountsItem]:
        """List all accounts for a data source.

        Retrieves all available accounts for the specified data source,
        optionally filtered by login usernames. The response is automatically
        flattened from the nested API structure into a simple list.

        Args:
            ds_id: Data source ID (e.g., "GA4", "google_ads", "facebook_ads").
            login_usernames: Optional login username(s) to filter accounts.
                Can be a single string or list of strings. Only accounts
                belonging to these login usernames will be returned.
            cache_minutes: Maximum allowed age of cache in minutes. If the
                cached data is older, fresh data will be fetched.

        Returns:
            list[GetAccountsResponse200DataItemAccountsItem]: Flattened list
                of all accounts across all matching logins. Each account has
                account_id, account_name, and group_name fields.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.TimeoutException: If the request times out.

        Example:
            >>> # Get all accounts for Google Analytics 4
            >>> accounts = client.accounts.list(ds_id="GA4")
            >>> print(f"Found {len(accounts)} accounts")
            >>>
            >>> # Filter by specific login
            >>> accounts = client.accounts.list(
            ...     ds_id="GA4",
            ...     login_usernames="user@example.com"
            ... )
            >>>
            >>> # Filter by multiple logins
            >>> accounts = client.accounts.list(
            ...     ds_id="GA4",
            ...     login_usernames=["user1@example.com", "user2@example.com"]
            ... )
        """
        logger.debug(
            f"Listing accounts: ds_id={ds_id}, login_usernames={login_usernames}, cache_minutes={cache_minutes}"
        )

        # Build request parameters
        request_params = GetAccountsJson(
            ds_id=ds_id,
            ds_users=login_usernames if login_usernames is not None else UNSET,
            cache_minutes=cache_minutes if cache_minutes is not None else UNSET,
        )

        # Call generated API
        response = get_accounts.sync(client=cast(AuthenticatedClient, self._client), json=request_params)

        # Handle empty or error responses
        if response is None or isinstance(response, Unset):
            logger.info("No accounts found (empty response)")
            return []

        # Cast to success response type - error responses are handled by generated client
        success_response = cast(GetAccountsResponse200, response)

        if success_response.data is None or isinstance(success_response.data, Unset):
            logger.info("No accounts found (empty response)")
            return []

        # Flatten nested structure: response.data[].accounts[] -> single list
        all_accounts: list[GetAccountsResponse200DataItemAccountsItem] = []
        for data_item in success_response.data:
            if data_item.accounts is not None and not isinstance(data_item.accounts, Unset):
                all_accounts.extend(data_item.accounts)

        logger.info(f"Retrieved {len(all_accounts)} accounts for ds_id={ds_id}")
        return all_accounts


class AccountsAsyncResource:
    """Asynchronous resource adapter for Accounts operations.

    Async version of AccountsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> accounts = await client.accounts.list(ds_id="GA4")
        >>> print(f"Found {len(accounts)} accounts")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the AccountsAsyncResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    async def list(
        self,
        ds_id: str,
        login_usernames: str | list[str] | None = None,
        cache_minutes: int | None = None,
    ) -> list[GetAccountsResponse200DataItemAccountsItem]:
        """List all accounts for a data source.

        Async version of list(). See AccountsResource.list() for full documentation.

        Args:
            ds_id: Data source ID (e.g., "GA4", "google_ads").
            login_usernames: Optional login username(s) to filter accounts.
            cache_minutes: Maximum allowed age of cache in minutes.

        Returns:
            list[GetAccountsResponse200DataItemAccountsItem]: Flattened list
                of all accounts.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
        """
        logger.debug(
            f"Listing accounts (async): ds_id={ds_id}, login_usernames={login_usernames}, cache_minutes={cache_minutes}"
        )

        # Build request parameters
        request_params = GetAccountsJson(
            ds_id=ds_id,
            ds_users=login_usernames if login_usernames is not None else UNSET,
            cache_minutes=cache_minutes if cache_minutes is not None else UNSET,
        )

        # Call generated API
        response = await get_accounts.asyncio(client=cast(AuthenticatedClient, self._client), json=request_params)

        # Handle empty or error responses
        if response is None or isinstance(response, Unset):
            logger.info("No accounts found (async - empty response)")
            return []

        # Cast to success response type - error responses are handled by generated client
        success_response = cast(GetAccountsResponse200, response)

        if success_response.data is None or isinstance(success_response.data, Unset):
            logger.info("No accounts found (async - empty response)")
            return []

        # Flatten nested structure: response.data[].accounts[] -> single list
        all_accounts: list[GetAccountsResponse200DataItemAccountsItem] = []
        for data_item in success_response.data:
            if data_item.accounts is not None and not isinstance(data_item.accounts, Unset):
                all_accounts.extend(data_item.accounts)

        logger.info(f"Retrieved {len(all_accounts)} accounts (async) for ds_id={ds_id}")
        return all_accounts
