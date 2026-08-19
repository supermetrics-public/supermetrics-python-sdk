"""Logins resource adapter for Supermetrics API."""

from __future__ import annotations

import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_source_logins import (
    get_data_source_login,
    list_data_source_login_accounts,
    list_data_source_logins,
    revoke_data_source_login,
)
from supermetrics._generated.supermetrics_api_client.models.data_source_account import DataSourceAccount
from supermetrics._generated.supermetrics_api_client.models.data_source_account_list_response import (
    DataSourceAccountListResponse,
)
from supermetrics._generated.supermetrics_api_client.models.data_source_login import DataSourceLogin
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_200 import (
    GetDataSourceLoginResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_200 import (
    ListDataSourceLoginsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.login_revoke_response import LoginRevokeResponse
from supermetrics._generated.supermetrics_api_client.types import Unset
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

logger = logging.getLogger(__name__)

# The resource classes expose a method named ``list``, which binds ``list`` in the class
# namespace and shadows the builtin for every annotation evaluated in the class body after
# that point. Aliasing the collection type out here, at module scope, is what keeps
# ``get_accounts``'s ``list[DataSourceAccount]`` return annotation meaning a list of
# accounts rather than a subscript of ``LoginsResource.list``. Do not inline this back.
DataSourceAccountList = list[DataSourceAccount]


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

    def get(
        self,
        login_id: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceLogin:
        """Retrieve a login by login ID.

        Fetches the details of a specific data source login, including
        authentication status, scopes, and user information.

        Args:
            login_id: The Supermetrics login ID to retrieve.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DataSourceLogin: The login details.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> login = client.logins.get("login_abc123")
            >>> print(f"Username: {login.username}")
            >>> print(f"Data Source: {login.ds_info.ds_name}")
            >>> print(f"Authenticated: {login.auth_time}")
        """
        logger.debug(f"Retrieving login: login_id={login_id}")

        endpoint = f"/ds/login/{login_id}"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Login not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_data_source_login.sync_detailed(
                login_id=login_id, client=cast(AuthenticatedClient, self._client)
            )
            if response.status_code == 200:
                parsed = cast(GetDataSourceLoginResponse200, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    raise ValueError("API returned empty response")
                login = parsed.data
                logger.info(f"Retrieved login: id={login.login_id}")
                logger.debug(f"Retrieved login: id={login.login_id}, username={login.username}")
                return login
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    def list(
        self,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> list[DataSourceLogin]:
        """List all logins for the authenticated user.

        Returns all data source logins associated with the API key's account,
        including their authentication status and credentials.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[DataSourceLogin]: List of all logins.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> logins = client.logins.list()
            >>> for login in logins:
            ...     print(f"{login.ds_info.ds_name}: {login.username}")
        """
        logger.debug("Listing all logins")

        endpoint = "/ds/logins"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = list_data_source_logins.sync_detailed(client=cast(AuthenticatedClient, self._client))
            if response.status_code == 200:
                parsed = cast(ListDataSourceLoginsResponse200, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    return []
                logins = parsed.data
                logger.info(f"Retrieved {len(logins)} logins")
                return logins
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    def get_accounts(
        self,
        login_id: str,
        *,
        offset: int = 0,
        limit: int = 100,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceAccountList:
        """List the data source accounts authorized under a login.

        Returns the customer accounts (ad accounts, properties, profiles, ...) that a
        specific data source login can access. This is the set of accounts you can pass
        to a query or bind to a transfer for that login.

        The endpoint is paginated: ``offset`` and ``limit`` select a window, and the
        total count rides in the response ``meta`` (reachable via
        ``client.with_raw_response.logins.get_accounts(...).json_body["meta"]["paginate"]``).

        Args:
            login_id: The Supermetrics login ID to list accounts for.
            offset: Zero-based index of the first account to return. Defaults to 0.
            limit: Maximum number of accounts to return (1-1000). Defaults to 100.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[DataSourceAccount]: The accounts on this page of results.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the login is not found (HTTP 404) or the API returns a
                server error (HTTP 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> accounts = client.logins.get_accounts("login_abc123")
            >>> for account in accounts:
            ...     print(f"{account.account_id}: {account.name}")
        """
        logger.debug(f"Listing accounts for login: login_id={login_id}, offset={offset}, limit={limit}")

        endpoint = f"/ds/login/{login_id}/accounts"
        with (
            api_error_handler(endpoint, context_404="Login not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = list_data_source_login_accounts.sync_detailed(
                login_id=login_id, client=cast(AuthenticatedClient, self._client), offset=offset, limit=limit
            )
            if response.status_code == 200:
                parsed = cast(DataSourceAccountListResponse, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    return []
                accounts = parsed.data
                logger.info(f"Retrieved {len(accounts)} accounts for login: id={login_id}")
                return accounts
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    def revoke(
        self,
        login_id: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> bool:
        """Revoke a login, disconnecting and invalidating its OAuth credentials.

        Permanently disconnects the data source login: its stored OAuth credentials are
        invalidated and it can no longer be used for queries or transfers. Bind a fresh
        login (via a login link) to restore access.

        Args:
            login_id: The Supermetrics login ID to revoke.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            bool: ``True`` when the login was revoked.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the login is not found (HTTP 404) or the API returns a
                server error (HTTP 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> client.logins.revoke("login_abc123")
            True
        """
        logger.debug(f"Revoking login: login_id={login_id}")

        endpoint = f"/ds/login/{login_id}"
        with (
            api_error_handler(endpoint, context_404="Login not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = revoke_data_source_login.sync_detailed(
                login_id=login_id, client=cast(AuthenticatedClient, self._client)
            )
            if response.status_code == 200:
                parsed = cast(LoginRevokeResponse, response.parsed)
                data = parsed.data
                result = data.result if data is not None and not isinstance(data, Unset) else None
                revoked = result if isinstance(result, bool) else False
                logger.info(f"Revoked login: id={login_id}, result={revoked}")
                return revoked
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    def get_by_username(
        self,
        login_username: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceLogin:
        """Retrieve a login by username.

        Finds a login by searching for a matching username across all logins.
        This is a convenience method that filters the list of all logins.

        Args:
            login_username: The username to search for (case-sensitive).
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DataSourceLogin: The login with matching username.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> login = client.logins.get_by_username("user@example.com")
            >>> print(f"Login ID: {login.login_id}")
            >>> print(f"Data Source: {login.ds_info.ds_name}")
        """
        logger.debug(f"Searching for login by username: {login_username}")

        # Get all logins and filter by username
        logins = self.list(auth_token=auth_token, headers=headers, timeout=timeout)

        for login in logins:
            if login.username == login_username:
                logger.info(f"Found login by username: id={login.login_id}")
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

    async def get(
        self,
        login_id: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceLogin:
        """Retrieve a login by login ID.

        Async version of get(). See LoginsResource.get() for full documentation.

        Args:
            login_id: The Supermetrics login ID to retrieve.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DataSourceLogin: The login details.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(f"Retrieving login (async): login_id={login_id}")

        endpoint = f"/ds/login/{login_id}"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Login not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_data_source_login.asyncio_detailed(
                login_id=login_id, client=cast(AuthenticatedClient, self._client)
            )
            if response.status_code == 200:
                parsed = cast(GetDataSourceLoginResponse200, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    raise ValueError("API returned empty response")
                login = parsed.data
                logger.info(f"Retrieved login (async): id={login.login_id}")
                logger.debug(f"Retrieved login (async): id={login.login_id}, username={login.username}")
                return login
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    async def list(
        self,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> list[DataSourceLogin]:
        """List all logins for the authenticated user.

        Async version of list(). See LoginsResource.list() for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[DataSourceLogin]: List of all logins.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug("Listing all logins (async)")

        endpoint = "/ds/logins"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = await list_data_source_logins.asyncio_detailed(client=cast(AuthenticatedClient, self._client))
            if response.status_code == 200:
                parsed = cast(ListDataSourceLoginsResponse200, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    return []
                logins = parsed.data
                logger.info(f"Retrieved {len(logins)} logins (async)")
                return logins
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    async def get_accounts(
        self,
        login_id: str,
        *,
        offset: int = 0,
        limit: int = 100,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceAccountList:
        """List the data source accounts authorized under a login.

        Async version of get_accounts(). See LoginsResource.get_accounts() for full documentation.

        Args:
            login_id: The Supermetrics login ID to list accounts for.
            offset: Zero-based index of the first account to return. Defaults to 0.
            limit: Maximum number of accounts to return (1-1000). Defaults to 100.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[DataSourceAccount]: The accounts on this page of results.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the login is not found (HTTP 404) or the API returns a
                server error (HTTP 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(f"Listing accounts for login (async): login_id={login_id}, offset={offset}, limit={limit}")

        endpoint = f"/ds/login/{login_id}/accounts"
        with (
            api_error_handler(endpoint, context_404="Login not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await list_data_source_login_accounts.asyncio_detailed(
                login_id=login_id, client=cast(AuthenticatedClient, self._client), offset=offset, limit=limit
            )
            if response.status_code == 200:
                parsed = cast(DataSourceAccountListResponse, response.parsed)
                if parsed.data is None or isinstance(parsed.data, Unset):
                    return []
                accounts = parsed.data
                logger.info(f"Retrieved {len(accounts)} accounts for login (async): id={login_id}")
                return accounts
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    async def revoke(
        self,
        login_id: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> bool:
        """Revoke a login, disconnecting and invalidating its OAuth credentials.

        Async version of revoke(). See LoginsResource.revoke() for full documentation.

        Args:
            login_id: The Supermetrics login ID to revoke.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            bool: ``True`` when the login was revoked.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the login is not found (HTTP 404) or the API returns a
                server error (HTTP 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(f"Revoking login (async): login_id={login_id}")

        endpoint = f"/ds/login/{login_id}"
        with (
            api_error_handler(endpoint, context_404="Login not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await revoke_data_source_login.asyncio_detailed(
                login_id=login_id, client=cast(AuthenticatedClient, self._client)
            )
            if response.status_code == 200:
                parsed = cast(LoginRevokeResponse, response.parsed)
                data = parsed.data
                result = data.result if data is not None and not isinstance(data, Unset) else None
                revoked = result if isinstance(result, bool) else False
                logger.info(f"Revoked login (async): id={login_id}, result={revoked}")
                return revoked
            _raise_for_status(
                response.status_code, response.parsed, endpoint, headers=response.headers, raw_body=response.content
            )

    async def get_by_username(
        self,
        login_username: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceLogin:
        """Retrieve a login by username.

        Async version of get_by_username(). See LoginsResource.get_by_username() for full documentation.

        Args:
            login_username: The username to search for (case-sensitive).
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DataSourceLogin: The login with matching username.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(f"Searching for login by username (async): {login_username}")

        # Get all logins and filter by username
        logins = await self.list(auth_token=auth_token, headers=headers, timeout=timeout)

        for login in logins:
            if login.username == login_username:
                logger.info(f"Found login by username (async): id={login.login_id}")
                return login

        # No matching login found
        raise ValueError(f"No login found with username: {login_username}")
