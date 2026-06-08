"""DatasourceDetails resource adapter for Supermetrics API."""

from typing import cast

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.datasource import (
    get_datasource_details,
)
from supermetrics._generated.supermetrics_api_client.models.datasource_details import DatasourceDetails
from supermetrics._generated.supermetrics_api_client.models.datasource_details_response import DatasourceDetailsResponse
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset
from supermetrics.exceptions import APIError
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler


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
        with api_error_handler(endpoint, context_404="Datasource not found"):
            response = await get_datasource_details.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                data_source_id=data_source_id,
                sm_app_id=sm_app_id if sm_app_id is not None else UNSET,
            )
            if response.status_code == 200:
                data = cast(DatasourceDetailsResponse, response.parsed).data
                if isinstance(data, Unset):
                    raise APIError(
                        "Response missing datasource details data",
                        status_code=200,
                        endpoint=endpoint,
                    )
                return data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Datasource not found or you do not have access to it",
            )


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
        with api_error_handler(endpoint, context_404="Datasource not found"):
            response = get_datasource_details.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                data_source_id=data_source_id,
                sm_app_id=sm_app_id if sm_app_id is not None else UNSET,
            )
            if response.status_code == 200:
                data = cast(DatasourceDetailsResponse, response.parsed).data
                if isinstance(data, Unset):
                    raise APIError(
                        "Response missing datasource details data",
                        status_code=200,
                        endpoint=endpoint,
                    )
                return data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Datasource not found or you do not have access to it",
            )
