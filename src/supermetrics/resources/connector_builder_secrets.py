"""Connector Builder Secrets resource adapter for Supermetrics API."""

import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.connector_secrets import (
    create_connector_secret,
    delete_connector_secret,
    list_connector_secrets,
    update_connector_secret,
)
from supermetrics._generated.supermetrics_api_client.models.create_connector_secret_response_201 import (
    CreateConnectorSecretResponse201,
)
from supermetrics._generated.supermetrics_api_client.models.create_secret_request import (
    CreateSecretRequest,
)
from supermetrics._generated.supermetrics_api_client.models.list_connector_secrets_response_200 import (
    ListConnectorSecretsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.update_secret_request import (
    UpdateSecretRequest,
)
from supermetrics.exceptions import APIError, AuthenticationError, ValidationError
from supermetrics.resources._error_handlers import _handle_http_error, _handle_request_error, _raise_for_error_response

logger = logging.getLogger(__name__)


class ConnectorBuilderSecretsAsyncResource:
    """Asynchronous resource adapter for Connector Builder Secrets operations.

    Async version of ConnectorBuilderSecretsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> secrets = await client.connector_builder_secrets.list(
        ...     team_id=12345, connector_identifier="my-connector"
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: int,
        connector_identifier: str,
    ) -> ListConnectorSecretsResponse200:
        """List all secrets for a connector.

        Async version of ConnectorBuilderSecretsResource.list(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets"
        try:
            response = await list_connector_secrets.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, ListConnectorSecretsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Connector not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    async def create(
        self,
        team_id: int,
        connector_identifier: str,
        secret_name: str,
        secret_value: str,
    ) -> CreateConnectorSecretResponse201:
        """Create a new secret for a connector.

        Async version of ConnectorBuilderSecretsResource.create(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the connector is not found or API error (HTTP 403, 404, 409, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets"
        try:
            body = CreateSecretRequest(
                secret_name=secret_name,
                secret_value=secret_value,
            )
            response = await create_connector_secret.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                body=body,
            )
            if isinstance(response, CreateConnectorSecretResponse201):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Invalid request parameters", context_404="Connector not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    async def update(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
        secret_value: str,
    ) -> None:
        """Update an existing secret value.

        Async version of ConnectorBuilderSecretsResource.update(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the secret is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}"
        try:
            body = UpdateSecretRequest(secret_value=secret_value)
            response = await update_connector_secret.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
                body=body,
            )
            if response is None:
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Invalid request parameters", context_404="Secret not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    async def delete(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
    ) -> None:
        """Delete a secret from a connector.

        Async version of ConnectorBuilderSecretsResource.delete(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the secret is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}"
        try:
            response = await delete_connector_secret.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
            )
            if response is None:
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Secret not found")
        except httpx.RequestError as e:
            _handle_request_error(e)


class ConnectorBuilderSecretsResource:
    """Synchronous resource adapter for Connector Builder Secrets operations.

    Provides a clean, Pythonic interface for managing secrets associated with
    Connector Builder connectors.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # List secrets
        >>> secrets = client.connector_builder_secrets.list(
        ...     team_id=12345, connector_identifier="my-connector"
        ... )
        >>> # Create a secret
        >>> result = client.connector_builder_secrets.create(
        ...     team_id=12345,
        ...     connector_identifier="my-connector",
        ...     secret_name="API_KEY",
        ...     secret_value="sk-abc123",
        ... )
        >>> # Update a secret
        >>> client.connector_builder_secrets.update(
        ...     team_id=12345,
        ...     connector_identifier="my-connector",
        ...     secret_placeholder="{{API_KEY}}",
        ...     secret_value="sk-new-value",
        ... )
        >>> # Delete a secret
        >>> client.connector_builder_secrets.delete(
        ...     team_id=12345,
        ...     connector_identifier="my-connector",
        ...     secret_placeholder="{{API_KEY}}",
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the ConnectorBuilderSecretsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        connector_identifier: str,
    ) -> ListConnectorSecretsResponse200:
        """List all secrets for a Connector Builder connector.

        Returns placeholder names only, never secret values.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.

        Returns:
            ListConnectorSecretsResponse200: Response containing the list of
                secret placeholders and a count.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> secrets = client.connector_builder_secrets.list(
            ...     team_id=12345, connector_identifier="my-connector"
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets"
        try:
            response = list_connector_secrets.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, ListConnectorSecretsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Connector not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    def create(
        self,
        team_id: int,
        connector_identifier: str,
        secret_name: str,
        secret_value: str,
    ) -> CreateConnectorSecretResponse201:
        """Create a new secret for a Connector Builder connector.

        The secret value is encrypted at rest.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            secret_name: Human-readable name for the secret.
            secret_value: Plaintext secret value (will be encrypted at rest).

        Returns:
            CreateConnectorSecretResponse201: Response containing the updated list
                of secret placeholders and a count.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the connector is not found or conflict (HTTP 403, 404, 409, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> result = client.connector_builder_secrets.create(
            ...     team_id=12345,
            ...     connector_identifier="my-connector",
            ...     secret_name="API_KEY",
            ...     secret_value="sk-abc123",
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets"
        try:
            body = CreateSecretRequest(
                secret_name=secret_name,
                secret_value=secret_value,
            )
            response = create_connector_secret.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                body=body,
            )
            if isinstance(response, CreateConnectorSecretResponse201):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Invalid request parameters", context_404="Connector not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    def update(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
        secret_value: str,
    ) -> None:
        """Update the value of an existing secret.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            secret_placeholder: The placeholder identifier of the secret to update.
            secret_value: New plaintext secret value (will be encrypted at rest).

        Returns:
            None: The API returns 204 No Content on success.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the secret is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.connector_builder_secrets.update(
            ...     team_id=12345,
            ...     connector_identifier="my-connector",
            ...     secret_placeholder="{{API_KEY}}",
            ...     secret_value="sk-new-value",
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}"
        try:
            body = UpdateSecretRequest(secret_value=secret_value)
            response = update_connector_secret.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
                body=body,
            )
            if response is None:
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Invalid request parameters", context_404="Secret not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    def delete(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
    ) -> None:
        """Delete a secret from a Connector Builder connector.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            secret_placeholder: The placeholder identifier of the secret to delete.

        Returns:
            None: The API returns 204 No Content on success.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the secret is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.connector_builder_secrets.delete(
            ...     team_id=12345,
            ...     connector_identifier="my-connector",
            ...     secret_placeholder="{{API_KEY}}",
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}"
        try:
            response = delete_connector_secret.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
            )
            if response is None:
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            raise APIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Secret not found")
        except httpx.RequestError as e:
            _handle_request_error(e)
