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
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

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
        >>> accounts = client.accounts.list(ds_id="GAWA")
        >>> for account in accounts:
        ...     print(f"{account.account_name} ({account.account_id})")
        >>> # Filter by login username
        >>> accounts = client.accounts.list(
        ...     ds_id="GAWA",
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
            ds_id: Data source ID (e.g., "GAWA", "google_ads", "facebook_ads").
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
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> # Get all accounts for Google Analytics 4
            >>> accounts = client.accounts.list(ds_id="GAWA")
            >>> print(f"Found {len(accounts)} accounts")
            >>>
            >>> # Filter by specific login
            >>> accounts = client.accounts.list(
            ...     ds_id="GAWA",
            ...     login_usernames="user@example.com"
            ... )
            >>>
            >>> # Filter by multiple logins
            >>> accounts = client.accounts.list(
            ...     ds_id="GAWA",
            ...     login_usernames=["user1@example.com", "user2@example.com"]
            ... )
        """
        logger.debug(
            f"Listing accounts: ds_id={ds_id}, login_usernames={login_usernames}, cache_minutes={cache_minutes}"
        )

        endpoint = "/query/accounts"
        with api_error_handler(endpoint, context_400="Invalid request parameters"):
            request_params = GetAccountsJson(
                ds_id=ds_id,
                ds_users=login_usernames if login_usernames is not None else UNSET,
                cache_minutes=cache_minutes if cache_minutes is not None else UNSET,
            )
            response = get_accounts.sync_detailed(client=cast(AuthenticatedClient, self._client), json=request_params)
            if response.status_code == 200:
                parsed = cast(GetAccountsResponse200, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    logger.info("No accounts found (empty response)")
                    return []
                all_accounts: list[GetAccountsResponse200DataItemAccountsItem] = []
                for data_item in parsed.data:
                    if data_item.accounts is not None and not isinstance(data_item.accounts, Unset):
                        all_accounts.extend(data_item.accounts)
                logger.info(f"Retrieved {len(all_accounts)} accounts for ds_id={ds_id}")
                return all_accounts
            _raise_for_status(response.status_code, response.parsed, endpoint)


class AccountsAsyncResource:
    """Asynchronous resource adapter for Accounts operations.

    Async version of AccountsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> accounts = await client.accounts.list(ds_id="GAWA")
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
            ds_id: Data source ID (e.g., "GAWA", "google_ads").
            login_usernames: Optional login username(s) to filter accounts.
            cache_minutes: Maximum allowed age of cache in minutes.

        Returns:
            list[GetAccountsResponse200DataItemAccountsItem]: Flattened list
                of all accounts.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(
            f"Listing accounts (async): ds_id={ds_id}, login_usernames={login_usernames}, cache_minutes={cache_minutes}"
        )

        endpoint = "/query/accounts"
        with api_error_handler(endpoint, context_400="Invalid request parameters"):
            request_params = GetAccountsJson(
                ds_id=ds_id,
                ds_users=login_usernames if login_usernames is not None else UNSET,
                cache_minutes=cache_minutes if cache_minutes is not None else UNSET,
            )
            response = await get_accounts.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client), json=request_params
            )
            if response.status_code == 200:
                parsed = cast(GetAccountsResponse200, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    logger.info("No accounts found (async - empty response)")
                    return []
                all_accounts: list[GetAccountsResponse200DataItemAccountsItem] = []
                for data_item in parsed.data:
                    if data_item.accounts is not None and not isinstance(data_item.accounts, Unset):
                        all_accounts.extend(data_item.accounts)
                logger.info(f"Retrieved {len(all_accounts)} accounts (async) for ds_id={ds_id}")
                return all_accounts
            _raise_for_status(response.status_code, response.parsed, endpoint)
