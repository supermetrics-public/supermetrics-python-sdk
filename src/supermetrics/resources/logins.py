"""Logins resource adapter for Supermetrics API."""

import logging
from typing import cast

import httpx

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
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_401 import (
    GetDataSourceLoginResponse401,
)
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_404 import (
    GetDataSourceLoginResponse404,
)
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_422 import (
    GetDataSourceLoginResponse422,
)
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_429 import (
    GetDataSourceLoginResponse429,
)
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_500 import (
    GetDataSourceLoginResponse500,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_200 import (
    ListDataSourceLoginsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_401 import (
    ListDataSourceLoginsResponse401,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_422 import (
    ListDataSourceLoginsResponse422,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_429 import (
    ListDataSourceLoginsResponse429,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_500 import (
    ListDataSourceLoginsResponse500,
)
from supermetrics._generated.supermetrics_api_client.types import Unset
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError

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

        try:
            response = get_data_source_login.sync(login_id=login_id, client=cast(AuthenticatedClient, self._client))

            if response is None or isinstance(response, Unset):
                raise ValueError("API returned empty response")

            # Handle error responses by checking type before casting
            if isinstance(response, GetDataSourceLoginResponse401):
                error_msg: str = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid or expired API key"
                )
                raise AuthenticationError(
                    error_msg,
                    status_code=401,
                    endpoint="/ds/logins/{login_id}",
                )
            elif isinstance(response, GetDataSourceLoginResponse404):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and hasattr(response.error, 'message')
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Login not found"
                )
                raise APIError(
                    error_msg,
                    status_code=404,
                    endpoint="/ds/logins/{login_id}",
                )
            elif isinstance(response, GetDataSourceLoginResponse422):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=422,
                    endpoint="/ds/logins/{login_id}",
                )
            elif isinstance(response, (GetDataSourceLoginResponse429, GetDataSourceLoginResponse500)):
                status = 429 if isinstance(response, GetDataSourceLoginResponse429) else 500
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and hasattr(response.error, 'message')
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Supermetrics API error"
                )
                raise APIError(
                    error_msg,
                    status_code=status,
                    endpoint="/ds/logins/{login_id}",
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, GetDataSourceLoginResponse200):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/ds/logins/{login_id}",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is GetDataSourceLoginResponse200
            if response.data is None or isinstance(response.data, Unset):
                raise ValueError("API returned empty response")

            login = response.data
            logger.info(f"Retrieved login: id={login.login_id}, username={login.username}")

            return login

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
                    f"Login not found: {e.response.text}",
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

    def list(self) -> list[DataSourceLogin]:
        """List all logins for the authenticated user.

        Returns all data source logins associated with the API key's account,
        including their authentication status and credentials.

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

        try:
            response = list_data_source_logins.sync(client=cast(AuthenticatedClient, self._client))

            if response is None or isinstance(response, Unset):
                return []

            # Handle error responses by checking type before casting
            if isinstance(response, ListDataSourceLoginsResponse401):
                error_msg: str = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid or expired API key"
                )
                raise AuthenticationError(
                    error_msg,
                    status_code=401,
                    endpoint="/ds/logins",
                )
            elif isinstance(response, ListDataSourceLoginsResponse422):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=422,
                    endpoint="/ds/logins",
                )
            elif isinstance(response, (ListDataSourceLoginsResponse429, ListDataSourceLoginsResponse500)):
                status = 429 if isinstance(response, ListDataSourceLoginsResponse429) else 500
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and hasattr(response.error, 'message')
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Supermetrics API error"
                )
                raise APIError(
                    error_msg,
                    status_code=status,
                    endpoint="/ds/logins",
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, ListDataSourceLoginsResponse200):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/ds/logins",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is ListDataSourceLoginsResponse200
            if response.data is None or isinstance(response.data, Unset):
                return []

            logins = response.data
            logger.info(f"Retrieved {len(logins)} logins")

            return logins

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
                    f"Login not found: {e.response.text}",
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

    def get_by_username(self, login_username: str) -> DataSourceLogin:
        """Retrieve a login by username.

        Finds a login by searching for a matching username across all logins.
        This is a convenience method that filters the list of all logins.

        Args:
            login_username: The username to search for (case-sensitive).

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
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(f"Retrieving login (async): login_id={login_id}")

        try:
            response = await get_data_source_login.asyncio(
                login_id=login_id, client=cast(AuthenticatedClient, self._client)
            )

            if response is None or isinstance(response, Unset):
                raise ValueError("API returned empty response")

            # Handle error responses by checking type before casting
            if isinstance(response, GetDataSourceLoginResponse401):
                error_msg: str = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid or expired API key"
                )
                raise AuthenticationError(
                    error_msg,
                    status_code=401,
                    endpoint="/ds/logins/{login_id}",
                )
            elif isinstance(response, GetDataSourceLoginResponse404):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and hasattr(response.error, 'message')
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Login not found"
                )
                raise APIError(
                    error_msg,
                    status_code=404,
                    endpoint="/ds/logins/{login_id}",
                )
            elif isinstance(response, GetDataSourceLoginResponse422):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=422,
                    endpoint="/ds/logins/{login_id}",
                )
            elif isinstance(response, (GetDataSourceLoginResponse429, GetDataSourceLoginResponse500)):
                status = 429 if isinstance(response, GetDataSourceLoginResponse429) else 500
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and hasattr(response.error, 'message')
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Supermetrics API error"
                )
                raise APIError(
                    error_msg,
                    status_code=status,
                    endpoint="/ds/logins/{login_id}",
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, GetDataSourceLoginResponse200):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/ds/logins/{login_id}",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is GetDataSourceLoginResponse200
            if response.data is None or isinstance(response.data, Unset):
                raise ValueError("API returned empty response")

            login = response.data
            logger.info(f"Retrieved login (async): id={login.login_id}, username={login.username}")

            return login

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
                    f"Login not found: {e.response.text}",
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

    async def list(self) -> list[DataSourceLogin]:
        """List all logins for the authenticated user.

        Async version of list(). See LoginsResource.list() for full documentation.

        Returns:
            list[DataSourceLogin]: List of all logins.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug("Listing all logins (async)")

        try:
            response = await list_data_source_logins.asyncio(client=cast(AuthenticatedClient, self._client))

            if response is None or isinstance(response, Unset):
                return []

            # Handle error responses by checking type before casting
            if isinstance(response, ListDataSourceLoginsResponse401):
                error_msg: str = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid or expired API key"
                )
                raise AuthenticationError(
                    error_msg,
                    status_code=401,
                    endpoint="/ds/logins",
                )
            elif isinstance(response, ListDataSourceLoginsResponse422):
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Invalid request parameters"
                )
                raise ValidationError(
                    error_msg,
                    status_code=422,
                    endpoint="/ds/logins",
                )
            elif isinstance(response, (ListDataSourceLoginsResponse429, ListDataSourceLoginsResponse500)):
                status = 429 if isinstance(response, ListDataSourceLoginsResponse429) else 500
                error_msg = (
                    response.error.message
                    if (response.error and not isinstance(response.error, Unset)
                        and hasattr(response.error, 'message')
                        and response.error.message and not isinstance(response.error.message, Unset))
                    else "Supermetrics API error"
                )
                raise APIError(
                    error_msg,
                    status_code=status,
                    endpoint="/ds/logins",
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, ListDataSourceLoginsResponse200):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/ds/logins",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is ListDataSourceLoginsResponse200
            if response.data is None or isinstance(response.data, Unset):
                return []

            logins = response.data
            logger.info(f"Retrieved {len(logins)} logins (async)")

            return logins

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
                    f"Login not found: {e.response.text}",
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

    async def get_by_username(self, login_username: str) -> DataSourceLogin:
        """Retrieve a login by username.

        Async version of get_by_username(). See LoginsResource.get_by_username() for full documentation.

        Args:
            login_username: The username to search for (case-sensitive).

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
        logins = await self.list()

        for login in logins:
            if login.username == login_username:
                logger.info(f"Found login by username (async): id={login.login_id}, username={login_username}")
                return login

        # No matching login found
        raise ValueError(f"No login found with username: {login_username}")
