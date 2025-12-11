"""Logins resource adapter for Supermetrics API."""

import logging
from typing import cast

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_source_logins import (
    get_data_source_login,
    list_data_source_logins,
)
from supermetrics._generated.supermetrics_api_client.models.data_source_login import DataSourceLogin
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_200 import (
    GetDataSourceLoginResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_200 import (
    ListDataSourceLoginsResponse200,
)
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset

logger = logging.getLogger(__name__)


class LoginsResource:
    """Synchronous resource adapter for Logins operations.

    Provides a clean, Pythonic interface for retrieving login information
    and credentials after data source authentication is complete.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Get login by link ID
        >>> login = client.logins.get("link_123")
        >>> print(f"Authenticated as: {login.username}")
        >>> # List all logins
        >>> logins = client.logins.list()
        >>> # Get login by username
        >>> login = client.logins.get_by_username("user@example.com")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the LoginsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def get(self, login_id: str) -> DataSourceLogin:
        """Retrieve a login by login ID.

        Fetches the details of a specific data source login, including
        authentication status, scopes, and user information.

        Args:
            login_id: The Supermetrics login ID to retrieve.

        Returns:
            DataSourceLogin: The login details.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.TimeoutException: If the request times out.
            ValueError: If the API returns an empty response.

        Example:
            >>> login = client.logins.get("login_abc123")
            >>> print(f"Username: {login.username}")
            >>> print(f"Data Source: {login.ds_info.ds_name}")
            >>> print(f"Authenticated: {login.auth_time}")
        """
        logger.debug(f"Retrieving login: login_id={login_id}")

        response = get_data_source_login.sync(login_id=login_id, client=cast(AuthenticatedClient, self._client))

        if response is None or isinstance(response, Unset):
            raise ValueError("API returned empty response")

        # Cast to success response type - error responses are handled by generated client
        success_response = cast(GetDataSourceLoginResponse200, response)

        if success_response.data is None or isinstance(success_response.data, Unset):
            raise ValueError("API returned empty response")

        login = success_response.data
        logger.info(f"Retrieved login: id={login.login_id}, username={login.username}")

        return login

    def list(self) -> list[DataSourceLogin]:
        """List all logins for the authenticated user.

        Returns all data source logins associated with the API key's account,
        including their authentication status and credentials.

        Returns:
            list[DataSourceLogin]: List of all logins.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.TimeoutException: If the request times out.

        Example:
            >>> logins = client.logins.list()
            >>> for login in logins:
            ...     print(f"{login.ds_info.ds_name}: {login.username}")
        """
        logger.debug("Listing all logins")

        response = list_data_source_logins.sync(client=cast(AuthenticatedClient, self._client))

        if response is None or isinstance(response, Unset):
            return []

        # Cast to success response type - error responses are handled by generated client
        success_response = cast(ListDataSourceLoginsResponse200, response)

        if success_response.data is None or isinstance(success_response.data, Unset):
            return []

        logins = success_response.data
        logger.info(f"Retrieved {len(logins)} logins")

        return logins

    def get_by_username(self, login_username: str) -> DataSourceLogin:
        """Retrieve a login by username.

        Finds a login by searching for a matching username across all logins.
        This is a convenience method that filters the list of all logins.

        Args:
            login_username: The username to search for (case-sensitive).

        Returns:
            DataSourceLogin: The login with matching username.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.TimeoutException: If the request times out.
            ValueError: If no login with the specified username is found.

        Example:
            >>> login = client.logins.get_by_username("user@example.com")
            >>> print(f"Login ID: {login.login_id}")
            >>> print(f"Data Source: {login.ds_info.ds_name}")
        """
        logger.debug(f"Searching for login by username: {login_username}")

        # Get all logins and filter by username
        logins = self.list()

        for login in logins:
            if login.username == login_username:
                logger.info(f"Found login by username: id={login.login_id}, username={login_username}")
                return login

        # No matching login found
        raise ValueError(f"No login found with username: {login_username}")


class LoginsAsyncResource:
    """Asynchronous resource adapter for Logins operations.

    Async version of LoginsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> login = await client.logins.get("link_123")
        >>> print(f"Authenticated as: {login.username}")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the LoginsAsyncResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    async def get(self, login_id: str) -> DataSourceLogin:
        """Retrieve a login by login ID.

        Async version of get(). See LoginsResource.get() for full documentation.

        Args:
            login_id: The Supermetrics login ID to retrieve.

        Returns:
            DataSourceLogin: The login details.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
            ValueError: If the API returns an empty response.
        """
        logger.debug(f"Retrieving login (async): login_id={login_id}")

        response = await get_data_source_login.asyncio(login_id=login_id, client=cast(AuthenticatedClient, self._client))

        if response is None or isinstance(response, Unset):
            raise ValueError("API returned empty response")

        # Cast to success response type - error responses are handled by generated client
        success_response = cast(GetDataSourceLoginResponse200, response)

        if success_response.data is None or isinstance(success_response.data, Unset):
            raise ValueError("API returned empty response")

        login = success_response.data
        logger.info(f"Retrieved login (async): id={login.login_id}, username={login.username}")

        return login

    async def list(self) -> list[DataSourceLogin]:
        """List all logins for the authenticated user.

        Async version of list(). See LoginsResource.list() for full documentation.

        Returns:
            list[DataSourceLogin]: List of all logins.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
        """
        logger.debug("Listing all logins (async)")

        response = await list_data_source_logins.asyncio(client=cast(AuthenticatedClient, self._client))

        if response is None or isinstance(response, Unset):
            return []

        # Cast to success response type - error responses are handled by generated client
        success_response = cast(ListDataSourceLoginsResponse200, response)

        if success_response.data is None or isinstance(success_response.data, Unset):
            return []

        logins = success_response.data
        logger.info(f"Retrieved {len(logins)} logins (async)")

        return logins

    async def get_by_username(self, login_username: str) -> DataSourceLogin:
        """Retrieve a login by username.

        Async version of get_by_username(). See LoginsResource.get_by_username() for full documentation.

        Args:
            login_username: The username to search for (case-sensitive).

        Returns:
            DataSourceLogin: The login with matching username.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.TimeoutException: If the request times out.
            ValueError: If no login with the specified username is found.
        """
        logger.debug(f"Searching for login by username (async): {login_username}")

        # Get all logins and filter by username
        logins = await self.list()

        for login in logins:
            if login.username == login_username:
                logger.info(f"Found login by username (async): id={login.login_id}, username={login_username}")
                return login

        # No matching login found
        raise ValueError(f"No login found with username: {login_username}")
