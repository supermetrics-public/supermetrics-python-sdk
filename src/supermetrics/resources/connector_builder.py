"""Connector Builder resource adapter for Supermetrics API."""

from __future__ import annotations

import logging
from typing import Any, cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.connector_logo import (
    get_connector_logo,
    upload_connector_logo,
)
from supermetrics._generated.supermetrics_api_client.api.connectors import (
    create_connector,
    delete_connector,
    get_connector,
    list_connectors,
    update_connector,
)
from supermetrics._generated.supermetrics_api_client.models.connector_with_configuration import (
    ConnectorWithConfiguration,
)
from supermetrics._generated.supermetrics_api_client.models.create_connector_body import CreateConnectorBody
from supermetrics._generated.supermetrics_api_client.models.get_connector_logo_response_200 import (
    GetConnectorLogoResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_connectors_response_200 import (
    ListConnectorsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.update_connector_request import UpdateConnectorRequest
from supermetrics._generated.supermetrics_api_client.models.update_connector_request_configuration import (
    UpdateConnectorRequestConfiguration,
)
from supermetrics._generated.supermetrics_api_client.models.update_connector_request_connector import (
    UpdateConnectorRequestConnector,
)
from supermetrics._generated.supermetrics_api_client.models.upload_connector_logo_body import UploadConnectorLogoBody
from supermetrics._generated.supermetrics_api_client.models.upload_connector_logo_response_201 import (
    UploadConnectorLogoResponse201,
)
from supermetrics._generated.supermetrics_api_client.types import UNSET, File
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import (
    _raise_for_error_response,
    _raise_if_failed,
    _raise_unexpected_response,
    api_error_handler,
)

logger = logging.getLogger(__name__)


class ConnectorBuilderAsyncResource:
    """Asynchronous resource adapter for Connector Builder operations.

    Async version of ConnectorBuilderResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> connectors = await client.connector_builder.list(team_id=12345)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: int,
        *,
        include_configs: bool = False,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ListConnectorsResponse200:
        """List all connectors for a team.

        Async version of ConnectorBuilderResource.list(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns an error (HTTP 403, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors"
        with (
            api_error_handler(endpoint),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            kwargs: dict[str, Any] = {
                "client": cast(AuthenticatedClient, self._client),
                "team_id": team_id,
            }
            if include_configs:
                kwargs["include_configs"] = include_configs
            response = await list_connectors.asyncio(**kwargs)
            if isinstance(response, ListConnectorsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def get(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ConnectorWithConfiguration:
        """Get a single connector with its configuration.

        Async version of ConnectorBuilderResource.get(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_connector.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, ConnectorWithConfiguration):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def create(
        self,
        team_id: int,
        title: str,
        *,
        description: str | None = None,
        connector_identifier: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ConnectorWithConfiguration:
        """Create a new connector.

        Async version of ConnectorBuilderResource.create(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns an error (HTTP 403, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = CreateConnectorBody(
                title=title,
                description=description if description is not None else UNSET,
                connector_identifier=connector_identifier if connector_identifier is not None else UNSET,
            )
            response = await create_connector.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=body,
            )
            if isinstance(response, ConnectorWithConfiguration):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def update(
        self,
        team_id: int,
        connector_identifier: str,
        connector: dict[str, Any],
        configuration: dict[str, Any],
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Update a connector and its configuration.

        Async version of ConnectorBuilderResource.update(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = UpdateConnectorRequest(
                connector=UpdateConnectorRequestConnector.from_dict(connector),
                configuration=UpdateConnectorRequestConfiguration.from_dict(configuration),
            )
            response = await update_connector.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                body=body,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Connector not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def delete(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Soft-delete a connector.

        Async version of ConnectorBuilderResource.delete(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_connector.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Connector not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def get_logo(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> GetConnectorLogoResponse200:
        """Get the logo URL for a connector.

        Async version of ConnectorBuilderResource.get_logo(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logo"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_connector_logo.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, GetConnectorLogoResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def upload_logo(
        self,
        team_id: int,
        connector_identifier: str,
        logo: File,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> UploadConnectorLogoResponse201:
        """Upload a logo image for a connector.

        Async version of ConnectorBuilderResource.upload_logo(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the file is invalid (HTTP 400, 413, 415).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logo"
        with (
            api_error_handler(endpoint, context_400="Invalid logo file", context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = UploadConnectorLogoBody(logo=logo)
            response = await upload_connector_logo.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                body=body,
            )
            if isinstance(response, UploadConnectorLogoResponse201):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)


class ConnectorBuilderResource:
    """Synchronous resource adapter for Connector Builder operations.

    Provides a clean, Pythonic interface for managing Connector Builder connectors,
    including CRUD operations and logo management.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # List connectors
        >>> connectors = client.connector_builder.list(team_id=12345)
        >>> # Create a connector
        >>> connector = client.connector_builder.create(
        ...     team_id=12345,
        ...     title="My Connector",
        ...     description="Custom data connector",
        ... )
        >>> # Get a connector
        >>> connector = client.connector_builder.get(
        ...     team_id=12345,
        ...     connector_identifier="my-connector",
        ... )
        >>> # Delete a connector
        >>> client.connector_builder.delete(
        ...     team_id=12345,
        ...     connector_identifier="my-connector",
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the ConnectorBuilderResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        *,
        include_configs: bool = False,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ListConnectorsResponse200:
        """List all Connector Builder connectors for a team.

        Args:
            team_id: The unique identifier of the team.
            include_configs: Whether to include connector configurations in the
                response. Defaults to False.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ListConnectorsResponse200: Response containing the list of connectors
                and a count.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns an error (HTTP 403, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> connectors = client.connector_builder.list(team_id=12345)
            >>> connectors_with_config = client.connector_builder.list(
            ...     team_id=12345, include_configs=True
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors"
        with (
            api_error_handler(endpoint),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            kwargs: dict[str, Any] = {
                "client": cast(AuthenticatedClient, self._client),
                "team_id": team_id,
            }
            if include_configs:
                kwargs["include_configs"] = include_configs
            response = list_connectors.sync(**kwargs)
            if isinstance(response, ListConnectorsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def get(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ConnectorWithConfiguration:
        """Get a single Connector Builder connector with its configuration.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ConnectorWithConfiguration: The connector details with configuration.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> connector = client.connector_builder.get(
            ...     team_id=12345, connector_identifier="my-connector"
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_connector.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, ConnectorWithConfiguration):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def create(
        self,
        team_id: int,
        title: str,
        *,
        description: str | None = None,
        connector_identifier: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ConnectorWithConfiguration:
        """Create a new Connector Builder connector.

        Optionally duplicate from an existing connector by providing its identifier.

        Args:
            team_id: The unique identifier of the team.
            title: Name of the connector.
            description: Description of the connector. Optional.
            connector_identifier: Identifier of an existing connector to duplicate
                from. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ConnectorWithConfiguration: The created connector.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns an error (HTTP 403, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> connector = client.connector_builder.create(
            ...     team_id=12345,
            ...     title="My Connector",
            ...     description="Custom data connector",
            ... )
            >>> # Duplicate from existing connector
            >>> connector = client.connector_builder.create(
            ...     team_id=12345,
            ...     title="My Connector Copy",
            ...     connector_identifier="existing-connector",
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = CreateConnectorBody(
                title=title,
                description=description if description is not None else UNSET,
                connector_identifier=connector_identifier if connector_identifier is not None else UNSET,
            )
            response = create_connector.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=body,
            )
            if isinstance(response, ConnectorWithConfiguration):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def update(
        self,
        team_id: int,
        connector_identifier: str,
        connector: dict[str, Any],
        configuration: dict[str, Any],
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Update a Connector Builder connector and its configuration.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            connector: Connector metadata as a dict with name and description.
            configuration: Connector configuration as a dict with id, version,
                and configuration_json.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            None: The API returns 204 No Content on success.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.connector_builder.update(
            ...     team_id=12345,
            ...     connector_identifier="my-connector",
            ...     connector={"name": "Updated Name", "description": "Updated"},
            ...     configuration={"id": "cfg-1", "version": 2, "configuration_json": "{}"},
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = UpdateConnectorRequest(
                connector=UpdateConnectorRequestConnector.from_dict(connector),
                configuration=UpdateConnectorRequestConfiguration.from_dict(configuration),
            )
            response = update_connector.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                body=body,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Connector not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def delete(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Soft-delete a Connector Builder connector.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            None: The API returns 204 No Content on success.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.connector_builder.delete(
            ...     team_id=12345, connector_identifier="my-connector"
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_connector.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Connector not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def get_logo(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> GetConnectorLogoResponse200:
        """Get the logo URL for a Connector Builder connector.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            GetConnectorLogoResponse200: Response containing the logo URL.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> logo = client.connector_builder.get_logo(
            ...     team_id=12345, connector_identifier="my-connector"
            ... )
            >>> print(logo.logo_url)
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logo"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_connector_logo.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, GetConnectorLogoResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def upload_logo(
        self,
        team_id: int,
        connector_identifier: str,
        logo: File,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> UploadConnectorLogoResponse201:
        """Upload a logo image for a Connector Builder connector.

        Max 5MB, PNG/JPG/JPEG formats accepted.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            logo: A File object containing the logo image data.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            UploadConnectorLogoResponse201: Response containing the uploaded logo URL.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the file is invalid (HTTP 400, 413, 415).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics._generated.supermetrics_api_client.types import File
            >>> with open("logo.png", "rb") as f:
            ...     logo_file = File(payload=f, file_name="logo.png", mime_type="image/png")
            ...     result = client.connector_builder.upload_logo(
            ...         team_id=12345,
            ...         connector_identifier="my-connector",
            ...         logo=logo_file,
            ...     )
            >>> print(result.logo_url)
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logo"
        with (
            api_error_handler(endpoint, context_400="Invalid logo file", context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = UploadConnectorLogoBody(logo=logo)
            response = upload_connector_logo.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                body=body,
            )
            if isinstance(response, UploadConnectorLogoResponse201):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)
