"""Backfills resource adapter for Supermetrics Data Warehouse API."""

from datetime import date
from typing import cast

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_backfills import (
    create_backfill,
    get_backfill_by_id,
    get_latest_backfill,
    list_incomplete_backfills,
    update_backfill_status,
)
from supermetrics._generated.supermetrics_api_client.models.backfill import Backfill
from supermetrics._generated.supermetrics_api_client.models.backfill_response import BackfillResponse
from supermetrics._generated.supermetrics_api_client.models.create_backfill_request import CreateBackfillRequest
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_200 import (
    ListIncompleteBackfillsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_body import UpdateBackfillStatusBody
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler


class BackfillsAsyncResource:
    """Asynchronous resource adapter for Data Warehouse Backfills operations.

    Async version of BackfillsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> from datetime import date
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> backfill = await client.backfills.create(
        ...     team_id=12345,
        ...     transfer_id=456789,
        ...     range_start=date(2024, 1, 1),
        ...     range_end=date(2024, 1, 31)
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def create(self, team_id: int, transfer_id: int, range_start: date, range_end: date) -> Backfill:
        """Create a new backfill for a transfer.

        Async version of BackfillsResource.create(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills"
        with api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Transfer not found"):
            request = CreateBackfillRequest(range_start=range_start, range_end=range_end)
            response = await create_backfill.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg=f"Invalid request parameters: {response.parsed}",
            )

    async def get(self, team_id: int, backfill_id: int) -> Backfill:
        """Retrieve a backfill by ID.

        Async version of BackfillsResource.get(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the backfill is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/backfills/{backfill_id}"
        with api_error_handler(endpoint, context_404="Backfill not found"):
            response = await get_backfill_by_id.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="Backfill not found or you do not have access to it",
            )

    async def get_latest(self, team_id: int, transfer_id: int) -> Backfill:
        """Get the latest backfill for a transfer.

        Async version of BackfillsResource.get_latest(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If no backfill exists or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills/latest"
        with api_error_handler(endpoint, context_404="Backfill not found"):
            response = await get_latest_backfill.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="No backfill found for this transfer",
            )

    async def list_incomplete(self, team_id: int) -> list[Backfill]:
        """List all incomplete backfills for a team.

        Async version of BackfillsResource.list_incomplete(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/backfills"
        with api_error_handler(endpoint):
            response = await list_incomplete_backfills.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(ListIncompleteBackfillsResponse200, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="No backfills found for this team",
            )

    async def cancel(self, team_id: int, backfill_id: int) -> Backfill:
        """Cancel a backfill.

        Async version of BackfillsResource.cancel(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the backfill is not found or cannot be cancelled (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/backfills/{backfill_id}"
        with api_error_handler(endpoint, context_400="Cannot cancel backfill", context_404="Backfill not found"):
            body = UpdateBackfillStatusBody(status="CANCELLED")
            response = await update_backfill_status.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
                body=body,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="Backfill not found or you do not have access to it",
                bad_request_msg=f"Cannot cancel backfill - it may already be in a final state: {response.parsed}",
            )


class BackfillsResource:
    """Synchronous resource adapter for Data Warehouse Backfills operations.

    Provides a clean, Pythonic interface for scheduling and managing historical
    data backfills for Data Warehouse transfers.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> from datetime import date
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Create a backfill
        >>> backfill = client.backfills.create(
        ...     team_id=12345,
        ...     transfer_id=456789,
        ...     range_start=date(2024, 1, 1),
        ...     range_end=date(2024, 1, 31)
        ... )
        >>> print(f"Backfill created: {backfill.transfer_backfill_id}")
        >>> # Get latest backfill for a transfer
        >>> latest = client.backfills.get_latest(team_id=12345, transfer_id=456789)
        >>> # List incomplete backfills for a team
        >>> backfills = client.backfills.list_incomplete(team_id=12345)
        >>> # Cancel a backfill
        >>> cancelled = client.backfills.cancel(team_id=12345, backfill_id=67890)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the BackfillsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def create(self, team_id: int, transfer_id: int, range_start: date, range_end: date) -> Backfill:
        """Create a new backfill for a transfer.

        Schedules a new backfill to re-process historical data for the specified date range.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer.
            range_start: Start date of the backfill range as a date object.
            range_end: End date of the backfill range as a date object.

        Returns:
            Backfill: The created backfill object with status "CREATED".

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from datetime import date
            >>> backfill = client.backfills.create(
            ...     team_id=12345,
            ...     transfer_id=456789,
            ...     range_start=date(2024, 1, 1),
            ...     range_end=date(2024, 1, 31)
            ... )
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills"
        with api_error_handler(endpoint, context_400="Invalid request parameters", context_404="Transfer not found"):
            request = CreateBackfillRequest(range_start=range_start, range_end=range_end)
            response = create_backfill.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg=f"Invalid request parameters: {response.parsed}",
            )

    def get(self, team_id: int, backfill_id: int) -> Backfill:
        """Retrieve a backfill by ID.

        Fetches detailed information about a specific backfill, including current status,
        progress tracking, and error details.

        Args:
            team_id: The unique identifier of the team.
            backfill_id: The unique identifier of the backfill.

        Returns:
            Backfill: The backfill object with current status and progress.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 422).
            APIError: If the backfill is not found or API error (HTTP 404, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> backfill = client.backfills.get(team_id=12345, backfill_id=67890)
            >>> print(f"Status: {backfill.status}")
            >>> print(f"Progress: {backfill.transfer_runs_completed}/{backfill.transfer_runs_total}")
        """
        endpoint = f"/teams/{team_id}/backfills/{backfill_id}"
        with api_error_handler(endpoint, context_404="Backfill not found"):
            response = get_backfill_by_id.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="Backfill not found or you do not have access to it",
            )

    def get_latest(self, team_id: int, transfer_id: int) -> Backfill:
        """Get the latest backfill for a transfer.

        Retrieves information about the most recent backfill for a specific transfer,
        regardless of its status.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer.

        Returns:
            Backfill: The latest backfill object.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If no backfill exists or API error (HTTP 404, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> latest = client.backfills.get_latest(team_id=12345, transfer_id=456789)
            >>> print(f"Latest backfill status: {latest.status}")
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills/latest"
        with api_error_handler(endpoint, context_404="Backfill not found"):
            response = get_latest_backfill.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="No backfill found for this transfer",
            )

    def list_incomplete(self, team_id: int) -> list[Backfill]:
        """List all incomplete backfills for a team.

        Retrieves all backfills that are not yet finished (statuses: CREATED, SCHEDULED,
        RUNNING, or FAILED). Completed and cancelled backfills are excluded.

        Args:
            team_id: The unique identifier of the team.

        Returns:
            List[Backfill]: List of incomplete backfill objects sorted by creation time.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> backfills = client.backfills.list_incomplete(team_id=12345)
            >>> for backfill in backfills:
            ...     print(f"Backfill {backfill.transfer_backfill_id}: {backfill.status}")
        """
        endpoint = f"/teams/{team_id}/backfills"
        with api_error_handler(endpoint):
            response = list_incomplete_backfills.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(ListIncompleteBackfillsResponse200, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="No backfills found for this team",
            )

    def cancel(self, team_id: int, backfill_id: int) -> Backfill:
        """Cancel a backfill.

        Updates the backfill status to "CANCELLED". All pending/queued transfer runs
        are cancelled, but runs that are already in progress will complete.

        Args:
            team_id: The unique identifier of the team.
            backfill_id: The unique identifier of the backfill to cancel.

        Returns:
            Backfill: The updated backfill object with status "CANCELLED".

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the backfill is not found or cannot be cancelled (HTTP 404, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> cancelled = client.backfills.cancel(team_id=12345, backfill_id=67890)
            >>> print(f"Backfill cancelled: {cancelled.status}")
        """
        endpoint = f"/teams/{team_id}/backfills/{backfill_id}"
        with api_error_handler(endpoint, context_400="Cannot cancel backfill", context_404="Backfill not found"):
            body = UpdateBackfillStatusBody(status="CANCELLED")
            response = update_backfill_status.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
                body=body,
            )
            if response.status_code == 200:
                return cast(BackfillResponse, response.parsed).data
            _raise_for_status(
                response.status_code,
                response.parsed,
                endpoint,
                not_found_msg="Backfill not found or you do not have access to it",
                bad_request_msg=f"Cannot cancel backfill - it may already be in a final state: {response.parsed}",
            )
