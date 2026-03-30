"""DatasourceDetails resource adapter for Supermetrics API."""

import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.datasource import (
    get_teams_team_id_datasource_data_source_id,
)
from supermetrics._generated.supermetrics_api_client.models.datasource_details import DatasourceDetails
from supermetrics._generated.supermetrics_api_client.models.datasource_details_response import DatasourceDetailsResponse
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources._error_handlers import _handle_http_error, _handle_request_error

logger = logging.getLogger(__name__)


def _raise_for_error_status(status_code: int, endpoint: str, response_body: str) -> None:
    """Translate HTTP error status codes into SDK exceptions."""
    if status_code == 401:
        raise AuthenticationError("Invalid or expired API key", status_code=401, endpoint=endpoint)
    if status_code == 400:
        raise ValidationError(
            "Invalid request parameters",
            status_code=400,
            endpoint=endpoint,
            response_body=response_body,
        )
    if status_code == 403:
        raise APIError(
            "Forbidden - insufficient permissions",
            status_code=403,
            endpoint=endpoint,
            response_body=response_body,
        )
    if status_code == 404:
        raise APIError(
            "Datasource not found or you do not have access to it",
            status_code=404,
            endpoint=endpoint,
            response_body=response_body,
        )
    if status_code == 429:
        raise APIError(
            "Rate limit exceeded",
            status_code=429,
            endpoint=endpoint,
            response_body=response_body,
        )
    raise APIError(
        f"API error ({status_code})",
        status_code=status_code,
        endpoint=endpoint,
        response_body=response_body,
    )


class DatasourceDetailsAsyncResource:
    """Asynchronous resource adapter for Datasource Details operations.

    Async version of DatasourceDetailsResource for use with SupermetricsAsyncClient.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> details = await client.datasource_details.get(team_id=12345, data_source_id="GAWA")
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def get(
        self,
        team_id: int,
        data_source_id: str,
        *,
        sm_app_id: str | None = None,
    ) -> DatasourceDetails:
        """Retrieve configuration details for a data source.

        Async version of DatasourceDetailsResource.get(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the datasource is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/datasource/{data_source_id}"
        try:
            response = await get_teams_team_id_datasource_data_source_id.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                data_source_id=data_source_id,
                sm_app_id=sm_app_id if sm_app_id is not None else UNSET,
            )
            if response.status_code == 200:
                return cast(DatasourceDetailsResponse, response.parsed).data
            _raise_for_error_status(
                status_code=int(response.status_code),
                endpoint=endpoint,
                response_body=str(response.parsed),
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Datasource not found")
        except httpx.RequestError as e:
            _handle_request_error(e)


class DatasourceDetailsResource:
    """Synchronous resource adapter for Datasource Details operations.

    Provides a clean, Pythonic interface for retrieving complete configuration
    details for a Supermetrics data source, including report types, settings,
    and authentication requirements.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> details = client.datasource_details.get(team_id=12345, data_source_id="GAWA")
        >>> print(f"Datasource: {details.name}")
        >>> print(f"Status: {details.status}")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the DatasourceDetailsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def get(
        self,
        team_id: int,
        data_source_id: str,
        *,
        sm_app_id: str | None = None,
    ) -> DatasourceDetails:
        """Retrieve complete configuration details for a data source.

        Fetches all available metadata for a datasource including its report types,
        settings, authentication requirements, and capabilities.

        Args:
            team_id: The unique identifier of the team.
            data_source_id: The unique identifier of the datasource (e.g. "GAWA", "AW").
            sm_app_id: Optional Sm-App-Id header value.

        Returns:
            DatasourceDetails: The datasource configuration details.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the datasource is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> details = client.datasource_details.get(team_id=12345, data_source_id="GAWA")
            >>> print(f"Name: {details.name}")
            >>> print(f"Categories: {details.categories}")
        """
        endpoint = f"/teams/{team_id}/datasource/{data_source_id}"
        try:
            response = get_teams_team_id_datasource_data_source_id.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                data_source_id=data_source_id,
                sm_app_id=sm_app_id if sm_app_id is not None else UNSET,
            )
            if response.status_code == 200:
                return cast(DatasourceDetailsResponse, response.parsed).data
            _raise_for_error_status(
                status_code=int(response.status_code),
                endpoint=endpoint,
                response_body=str(response.parsed),
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Datasource not found")
        except httpx.RequestError as e:
            _handle_request_error(e)
