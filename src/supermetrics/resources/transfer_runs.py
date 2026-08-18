"""Transfer Runs resource adapter for Supermetrics Data Warehouse API."""

from __future__ import annotations

from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_transfers import (
    get_transfer_run,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_run_detail import TransferRunDetail
from supermetrics._generated.supermetrics_api_client.models.transfer_run_detail_response import (
    TransferRunDetailResponse,
)
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler


class TransferRunsAsyncResource:
    """Asynchronous resource adapter for Data Warehouse Transfer Run operations.

    Async version of TransferRunsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> run = await client.transfer_runs.get(team_id=12345, transfer_run_id=98765)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def get(
        self,
        team_id: int,
        transfer_run_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferRunDetail:
        """Retrieve a transfer run by ID.

        Async version of TransferRunsResource.get(). See sync version for full documentation.

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
            APIError: If the transfer run is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfer_runs/{transfer_run_id}"
        with (
            api_error_handler(endpoint, context_404="Transfer run not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_transfer_run.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_run_id=transfer_run_id,
            )
            if response.status_code == 200:
                return cast(TransferRunDetailResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer run not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )


class TransferRunsResource:
    """Synchronous resource adapter for Data Warehouse Transfer Run operations.

    Provides a clean, Pythonic interface for inspecting a single execution of a
    Data Warehouse transfer, including its status, timing, row counts, and
    per-query execution details.

    A run is looked up by its own identifier and is scoped to the team, so the
    transfer it belongs to does not need to be named. This endpoint is served by
    the Data Warehouse API, which lives on a separate host; the SDK routes the
    request there automatically.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> run = client.transfer_runs.get(team_id=12345, transfer_run_id=98765)
        >>> print(f"Status: {run.status}")
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the TransferRunsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def get(
        self,
        team_id: int,
        transfer_run_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferRunDetail:
        """Retrieve a transfer run by ID.

        Fetches detailed information about a single transfer run, including its current
        status, queued/started/ended timestamps, total duration, row counts, and the
        per-query execution details. The run is addressed by its own identifier within
        the team, so the transfer that produced it does not have to be known.

        Args:
            team_id: The unique identifier of the team.
            transfer_run_id: The unique identifier of the transfer run.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TransferRunDetail: The transfer run with its status, timings and query details.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer run is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> run = client.transfer_runs.get(team_id=12345, transfer_run_id=98765)
            >>> print(f"Status: {run.status}")
            >>> print(f"Rows: {run.total_rows} in {run.total_duration}s")
            >>> for query in run.query_details:
            ...     print(query)
        """
        endpoint = f"/teams/{team_id}/transfer_runs/{transfer_run_id}"
        with (
            api_error_handler(endpoint, context_404="Transfer run not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_transfer_run.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_run_id=transfer_run_id,
            )
            if response.status_code == 200:
                return cast(TransferRunDetailResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer run not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )
