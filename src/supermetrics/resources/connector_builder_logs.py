"""Connector Builder Logs resource adapter for Supermetrics API."""

from __future__ import annotations

import datetime
import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.connector_logs import (
    get_connector_log,
    list_connector_logs,
)
from supermetrics._generated.supermetrics_api_client.models.list_connector_logs_response_200 import (
    ListConnectorLogsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.log_entry import LogEntry
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import (
    _raise_for_error_response,
    _raise_unexpected_response,
    api_error_handler,
)

logger = logging.getLogger(__name__)


class ConnectorBuilderLogsAsyncResource:
    """Asynchronous resource adapter for Connector Builder Logs operations.

    Async version of ConnectorBuilderLogsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> logs = await client.connector_builder_logs.list(
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
        limit: int | None = None,
        before: datetime.datetime | str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ListConnectorLogsResponse200:
        """List execution logs for a connector.

        Async version of ConnectorBuilderLogsResource.list(). See sync version for full documentation.

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
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logs"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await list_connector_logs.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                limit=limit if limit is not None else UNSET,
                before=datetime.datetime.fromisoformat(before)
                if isinstance(before, str)
                else (before if before is not None else UNSET),
            )
            if isinstance(response, ListConnectorLogsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    async def get(
        self,
        team_id: int,
        connector_identifier: str,
        log_id: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> LogEntry:
        """Get detailed information for a specific log entry.

        Async version of ConnectorBuilderLogsResource.get(). See sync version for full documentation.

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
            APIError: If the log is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logs/{log_id}"
        with (
            api_error_handler(endpoint, context_404="Log entry not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_connector_log.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                log_id=log_id,
            )
            if isinstance(response, LogEntry):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)


class ConnectorBuilderLogsResource:
    """Synchronous resource adapter for Connector Builder Logs operations.

    Provides a clean, Pythonic interface for viewing execution logs associated
    with Connector Builder connectors.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # List logs
        >>> logs = client.connector_builder_logs.list(
        ...     team_id=12345, connector_identifier="my-connector"
        ... )
        >>> # Get a specific log entry
        >>> log = client.connector_builder_logs.get(
        ...     team_id=12345,
        ...     connector_identifier="my-connector",
        ...     log_id="log-abc123",
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the ConnectorBuilderLogsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        connector_identifier: str,
        *,
        limit: int | None = None,
        before: datetime.datetime | str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ListConnectorLogsResponse200:
        """List execution logs for a Connector Builder connector.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            limit: Maximum number of log entries to return. Optional.
            before: Cursor for pagination - return logs before this ID. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ListConnectorLogsResponse200: Response containing the list of log entries.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the connector is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> logs = client.connector_builder_logs.list(
            ...     team_id=12345, connector_identifier="my-connector"
            ... )
            >>> # With pagination
            >>> logs = client.connector_builder_logs.list(
            ...     team_id=12345,
            ...     connector_identifier="my-connector",
            ...     limit=10,
            ...     before="log-cursor-id",
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logs"
        with (
            api_error_handler(endpoint, context_404="Connector not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = list_connector_logs.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                limit=limit if limit is not None else UNSET,
                before=datetime.datetime.fromisoformat(before)
                if isinstance(before, str)
                else (before if before is not None else UNSET),
            )
            if isinstance(response, ListConnectorLogsResponse200):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)

    def get(
        self,
        team_id: int,
        connector_identifier: str,
        log_id: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> LogEntry:
        """Get detailed information for a specific execution log entry.

        Args:
            team_id: The unique identifier of the team.
            connector_identifier: The unique identifier of the connector.
            log_id: The unique identifier of the log entry.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            LogEntry: The detailed log entry.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the log is not found or API error (HTTP 403, 404, 500).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> log = client.connector_builder_logs.get(
            ...     team_id=12345,
            ...     connector_identifier="my-connector",
            ...     log_id="log-abc123",
            ... )
        """
        endpoint = f"/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logs/{log_id}"
        with (
            api_error_handler(endpoint, context_404="Log entry not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_connector_log.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                connector_identifier=connector_identifier,
                log_id=log_id,
            )
            if isinstance(response, LogEntry):
                return response
            if hasattr(response, "error"):
                _raise_for_error_response(response, endpoint)
            _raise_unexpected_response(response, endpoint)
