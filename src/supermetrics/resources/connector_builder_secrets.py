"""Connector Builder Secrets resource adapter for Supermetrics API."""

from __future__ import annotations

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
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import (
    _raise_for_error_response,
    _raise_if_failed,
    _raise_unexpected_response,
    api_error_handler,
)

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
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ListConnectorSecretsResponse200:
        """List all secrets for a connector.

        Async version of ConnectorBuilderSecretsResource.list(). See sync version for full documentation.

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
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await list_connector_secrets.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, ListConnectorSecretsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def create(
        self,
        team_id: int,
        connector_identifier: str,
        secret_name: str,
        secret_value: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> CreateConnectorSecretResponse201:
        """Create a new secret for a connector.

        Async version of ConnectorBuilderSecretsResource.create(). See sync version for full documentation.

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
            APIError: If the connector is not found or API error (HTTP 403, 404, 409, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
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
            _raise_unexpected_response(response, endpoint)

    async def update(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
        secret_value: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Update an existing secret value.

        Async version of ConnectorBuilderSecretsResource.update(). See sync version for full documentation.

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
            APIError: If the secret is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}"
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Secret not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = UpdateSecretRequest(secret_value=secret_value)
            response = await update_connector_secret.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
                body=body,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Secret not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def delete(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a secret from a connector.

        Async version of ConnectorBuilderSecretsResource.delete(). See sync version for full documentation.

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
            APIError: If the secret is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}"
        with (
            api_error_handler(endpoint, context_404="Secret not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_connector_secret.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Secret not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)


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
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ListConnectorSecretsResponse200:
        """List all secrets for a Connector Builder connector.

        Returns placeholder names only, never secret values.

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
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = list_connector_secrets.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
            )
            if isinstance(response, ListConnectorSecretsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def create(
        self,
        team_id: int,
        connector_identifier: str,
        secret_name: str,
        secret_value: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> CreateConnectorSecretResponse201:
        """Create a new secret for a Connector Builder connector.

        The secret value is encrypted at rest.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            secret_name: Human-readable name for the secret.
            secret_value: Plaintext secret value (will be encrypted at rest).
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

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
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
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
            _raise_unexpected_response(response, endpoint)

    def update(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
        secret_value: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Update the value of an existing secret.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            secret_placeholder: The placeholder identifier of the secret to update.
            secret_value: New plaintext secret value (will be encrypted at rest).
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
        with (
            api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Secret not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = UpdateSecretRequest(secret_value=secret_value)
            response = update_connector_secret.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
                body=body,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Secret not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def delete(
        self,
        team_id: int,
        connector_identifier: str,
        secret_placeholder: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a secret from a Connector Builder connector.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            secret_placeholder: The placeholder identifier of the secret to delete.
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
        with (
            api_error_handler(endpoint, context_404="Secret not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_connector_secret.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                secret_placeholder=secret_placeholder,
            )
            if response is None:
                # The generated parser also returns None for a status the spec does not
                # describe, so confirm the transport actually saw a success.
                _raise_if_failed(endpoint, not_found_msg="Secret not found")
                return None
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)
