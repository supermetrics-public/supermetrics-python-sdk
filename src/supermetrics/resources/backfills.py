"""Backfills resource adapter for Supermetrics Data Warehouse API."""

import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.dwh import (
    create_backfill,
    get_backfill_by_id,
    get_latest_backfill,
    list_incomplete_backfills,
    update_backfill_status,
)
from supermetrics._generated.supermetrics_api_client.models.backfill import Backfill
from supermetrics._generated.supermetrics_api_client.models.create_backfill_request import CreateBackfillRequest
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_body import UpdateBackfillStatusBody
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_body_status import (
    UpdateBackfillStatusBodyStatus,
)
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError

logger = logging.getLogger(__name__)


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
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Create a backfill
        >>> backfill = client.backfills.create(
        ...     team_id=12345,
        ...     transfer_id=456789,
        ...     range_start="2024-01-01",
        ...     range_end="2024-01-31"
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

    def create(self, team_id: int, transfer_id: int, range_start: str, range_end: str) -> Backfill:
        """Create a new backfill for a transfer.

        Schedules a new backfill to re-process historical data for the specified date range.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer.
            range_start: Start date of the backfill range (YYYY-MM-DD).
            range_end: End date of the backfill range (YYYY-MM-DD).

        Returns:
            Backfill: The created backfill object with status "CREATED".

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> backfill = client.backfills.create(
            ...     team_id=12345,
            ...     transfer_id=456789,
            ...     range_start="2024-01-01",
            ...     range_end="2024-01-31"
            ... )
        """
        try:
            request = CreateBackfillRequest(range_start=range_start, range_end=range_end)
            response = create_backfill.sync_detailed(
                client=self._client,
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )

            if response.status_code == 200 and hasattr(response.parsed, "data"):
                return cast(Backfill, response.parsed.data)
            elif response.status_code == 401:
                raise AuthenticationError("Invalid or expired API key")
            elif response.status_code in (400, 422):
                error_msg = "Invalid request parameters"
                if hasattr(response.parsed, "error") and hasattr(response.parsed.error, "description"):
                    error_msg = response.parsed.error.description
                raise ValidationError(error_msg)
            elif response.status_code == 404:
                raise APIError("Transfer not found or you do not have access to it", status_code=404)
            else:
                raise APIError(f"API error: {response.status_code}", status_code=response.status_code)

        except httpx.RequestError as e:
            logger.error(f"Network error creating backfill: {e}")
            raise NetworkError(f"Network error: {e}")

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
        try:
            response = get_backfill_by_id.sync_detailed(
                client=self._client,
                team_id=team_id,
                backfill_id=backfill_id,
            )

            if response.status_code == 200 and hasattr(response.parsed, "data"):
                return cast(Backfill, response.parsed.data)
            elif response.status_code == 401:
                raise AuthenticationError("Invalid or expired API key")
            elif response.status_code == 404:
                raise APIError("Backfill not found or you do not have access to it", status_code=404)
            elif response.status_code == 422:
                raise ValidationError("Invalid request parameters")
            else:
                raise APIError(f"API error: {response.status_code}", status_code=response.status_code)

        except httpx.RequestError as e:
            logger.error(f"Network error retrieving backfill: {e}")
            raise NetworkError(f"Network error: {e}")

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
            ValidationError: If request parameters are invalid (HTTP 422).
            APIError: If no backfill exists or API error (HTTP 404, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> latest = client.backfills.get_latest(team_id=12345, transfer_id=456789)
            >>> print(f"Latest backfill status: {latest.status}")
        """
        try:
            response = get_latest_backfill.sync_detailed(
                client=self._client,
                team_id=team_id,
                transfer_id=transfer_id,
            )

            if response.status_code == 200 and hasattr(response.parsed, "data"):
                return cast(Backfill, response.parsed.data)
            elif response.status_code == 401:
                raise AuthenticationError("Invalid or expired API key")
            elif response.status_code == 404:
                raise APIError("No backfill found for this transfer", status_code=404)
            elif response.status_code == 422:
                raise ValidationError("Invalid request parameters")
            else:
                raise APIError(f"API error: {response.status_code}", status_code=response.status_code)

        except httpx.RequestError as e:
            logger.error(f"Network error retrieving latest backfill: {e}")
            raise NetworkError(f"Network error: {e}")

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
            ValidationError: If request parameters are invalid (HTTP 422).
            APIError: If the API returns a server error (HTTP 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> backfills = client.backfills.list_incomplete(team_id=12345)
            >>> for backfill in backfills:
            ...     print(f"Backfill {backfill.transfer_backfill_id}: {backfill.status}")
        """
        try:
            response = list_incomplete_backfills.sync_detailed(
                client=self._client,
                team_id=team_id,
            )

            if response.status_code == 200 and hasattr(response.parsed, "data"):
                return cast(list[Backfill], response.parsed.data)
            elif response.status_code == 401:
                raise AuthenticationError("Invalid or expired API key")
            elif response.status_code == 422:
                raise ValidationError("Invalid request parameters")
            else:
                raise APIError(f"API error: {response.status_code}", status_code=response.status_code)

        except httpx.RequestError as e:
            logger.error(f"Network error listing incomplete backfills: {e}")
            raise NetworkError(f"Network error: {e}")

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
            ValidationError: If request parameters are invalid (HTTP 400, 422).
            APIError: If the backfill is not found or cannot be cancelled (HTTP 404, 422).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> cancelled = client.backfills.cancel(team_id=12345, backfill_id=67890)
            >>> print(f"Backfill cancelled: {cancelled.status}")
        """
        try:
            body = UpdateBackfillStatusBody(status=UpdateBackfillStatusBodyStatus.CANCELLED)
            response = update_backfill_status.sync_detailed(
                client=self._client,
                team_id=team_id,
                backfill_id=backfill_id,
                body=body,
            )

            if response.status_code == 200 and hasattr(response.parsed, "data"):
                return cast(Backfill, response.parsed.data)
            elif response.status_code == 401:
                raise AuthenticationError("Invalid or expired API key")
            elif response.status_code in (400, 422):
                error_msg = "Cannot cancel backfill - it may already be in a final state"
                if hasattr(response.parsed, "error") and hasattr(response.parsed.error, "description"):
                    error_msg = response.parsed.error.description
                raise ValidationError(error_msg)
            elif response.status_code == 404:
                raise APIError("Backfill not found or you do not have access to it", status_code=404)
            else:
                raise APIError(f"API error: {response.status_code}", status_code=response.status_code)

        except httpx.RequestError as e:
            logger.error(f"Network error cancelling backfill: {e}")
            raise NetworkError(f"Network error: {e}")
