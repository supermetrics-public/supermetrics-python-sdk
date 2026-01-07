"""Accounts resource adapter for Supermetrics API."""

import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_source import get_accounts
from supermetrics._generated.supermetrics_api_client.models.get_accounts_json import GetAccountsJson
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200 import GetAccountsResponse200
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200_data_item_accounts_item import (
    GetAccountsResponse200DataItemAccountsItem,
)
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_400 import GetAccountsResponse400
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_401 import GetAccountsResponse401
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_403 import GetAccountsResponse403
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_422 import GetAccountsResponse422
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_429 import GetAccountsResponse429
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_500 import GetAccountsResponse500
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError

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

        try:
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

            # Handle error responses by checking type before casting
            if isinstance(response, GetAccountsResponse400):
                error_msg: str = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=400,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, GetAccountsResponse401):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid or expired API key"
                )
                raise AuthenticationError(
                    error_msg,
                    status_code=401,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, GetAccountsResponse403):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Forbidden - insufficient permissions"
                )
                raise APIError(
                    error_msg,
                    status_code=403,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, GetAccountsResponse422):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=422,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, (GetAccountsResponse429, GetAccountsResponse500)):
                status = 429 if isinstance(response, GetAccountsResponse429) else 500
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Supermetrics API error"
                )
                raise APIError(
                    error_msg,
                    status_code=status,
                    endpoint="/ds/accounts",
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, GetAccountsResponse200):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/ds/accounts",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is GetAccountsResponse200
            if response.data is None or isinstance(response.data, Unset):
                logger.info("No accounts found (empty response)")
                return []

            # Flatten nested structure: response.data[].accounts[] -> single list
            all_accounts: list[GetAccountsResponse200DataItemAccountsItem] = []
            for data_item in response.data:
                if data_item.accounts is not None and not isinstance(data_item.accounts, Unset):
                    all_accounts.extend(data_item.accounts)

            logger.info(f"Retrieved {len(all_accounts)} accounts for ds_id={ds_id}")
            return all_accounts

        except (AuthenticationError, ValidationError, APIError):
            # Re-raise SDK exceptions
            raise
        except httpx.HTTPStatusError as e:
            # Map HTTP status codes to SDK exceptions
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 400:
                raise ValidationError(
                    f"Invalid request parameters: {e.response.text}",
                    status_code=400,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 404:
                raise APIError(
                    f"Account not found: {e.response.text}",
                    status_code=404,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code >= 500:
                raise APIError(
                    f"Supermetrics API error: {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            else:
                raise APIError(
                    f"API error ({e.response.status_code}): {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(
                f"Network error: {str(e)}",
                endpoint=str(e.request.url) if e.request else None,
            ) from e


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

        try:
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

            # Handle error responses by checking type before casting
            if isinstance(response, GetAccountsResponse400):
                error_msg: str = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=400,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, GetAccountsResponse401):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid or expired API key"
                )
                raise AuthenticationError(
                    error_msg,
                    status_code=401,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, GetAccountsResponse403):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Forbidden - insufficient permissions"
                )
                raise APIError(
                    error_msg,
                    status_code=403,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, GetAccountsResponse422):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=422,
                    endpoint="/ds/accounts",
                )
            elif isinstance(response, (GetAccountsResponse429, GetAccountsResponse500)):
                status = 429 if isinstance(response, GetAccountsResponse429) else 500
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Supermetrics API error"
                )
                raise APIError(
                    error_msg,
                    status_code=status,
                    endpoint="/ds/accounts",
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, GetAccountsResponse200):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/ds/accounts",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is GetAccountsResponse200
            if response.data is None or isinstance(response.data, Unset):
                logger.info("No accounts found (async - empty response)")
                return []

            # Flatten nested structure: response.data[].accounts[] -> single list
            all_accounts: list[GetAccountsResponse200DataItemAccountsItem] = []
            for data_item in response.data:
                if data_item.accounts is not None and not isinstance(data_item.accounts, Unset):
                    all_accounts.extend(data_item.accounts)

            logger.info(f"Retrieved {len(all_accounts)} accounts (async) for ds_id={ds_id}")
            return all_accounts

        except (AuthenticationError, ValidationError, APIError):
            # Re-raise SDK exceptions
            raise
        except httpx.HTTPStatusError as e:
            # Map HTTP status codes to SDK exceptions
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 400:
                raise ValidationError(
                    f"Invalid request parameters: {e.response.text}",
                    status_code=400,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 404:
                raise APIError(
                    f"Account not found: {e.response.text}",
                    status_code=404,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code >= 500:
                raise APIError(
                    f"Supermetrics API error: {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            else:
                raise APIError(
                    f"API error ({e.response.status_code}): {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(
                f"Network error: {str(e)}",
                endpoint=str(e.request.url) if e.request else None,
            ) from e
