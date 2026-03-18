"""Backfills resource adapter for Supermetrics Data Warehouse API."""

import logging
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
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
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response import CreateBackfillResponse
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_400 import CreateBackfillResponse400
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_401 import CreateBackfillResponse401
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_403 import CreateBackfillResponse403
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_429 import CreateBackfillResponse429
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_500 import CreateBackfillResponse500
from supermetrics._generated.supermetrics_api_client.models.get_backfill_by_id_response_401 import GetBackfillByIdResponse401
from supermetrics._generated.supermetrics_api_client.models.get_backfill_by_id_response_403 import GetBackfillByIdResponse403
from supermetrics._generated.supermetrics_api_client.models.get_backfill_by_id_response_429 import GetBackfillByIdResponse429
from supermetrics._generated.supermetrics_api_client.models.get_backfill_by_id_response_500 import GetBackfillByIdResponse500
from supermetrics._generated.supermetrics_api_client.models.get_backfill_response import GetBackfillResponse
from supermetrics._generated.supermetrics_api_client.models.get_latest_backfill_response_401 import GetLatestBackfillResponse401
from supermetrics._generated.supermetrics_api_client.models.get_latest_backfill_response_403 import GetLatestBackfillResponse403
from supermetrics._generated.supermetrics_api_client.models.get_latest_backfill_response_429 import GetLatestBackfillResponse429
from supermetrics._generated.supermetrics_api_client.models.get_latest_backfill_response_500 import GetLatestBackfillResponse500
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_200 import (
    ListIncompleteBackfillsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_401 import (
    ListIncompleteBackfillsResponse401,
)
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_403 import (
    ListIncompleteBackfillsResponse403,
)
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_429 import (
    ListIncompleteBackfillsResponse429,
)
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_500 import (
    ListIncompleteBackfillsResponse500,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_body import UpdateBackfillStatusBody
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_body_status import (
    UpdateBackfillStatusBodyStatus,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_400 import (
    UpdateBackfillStatusResponse400,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_401 import (
    UpdateBackfillStatusResponse401,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_403 import (
    UpdateBackfillStatusResponse403,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_429 import (
    UpdateBackfillStatusResponse429,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_500 import (
    UpdateBackfillStatusResponse500,
)
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources._error_handlers import _handle_http_error, _handle_request_error, _raise_for_response

logger = logging.getLogger(__name__)


class BackfillsAsyncResource:
    """Asynchronous resource adapter for Data Warehouse Backfills operations.

    Async version of BackfillsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> backfill = await client.backfills.create(
        ...     team_id=12345,
        ...     transfer_id=456789,
        ...     range_start="2024-01-01",
        ...     range_end="2024-01-31"
        ... )
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def create(self, team_id: int, transfer_id: int, range_start: str, range_end: str) -> Backfill:
        """Create a new backfill for a transfer.

        Async version of BackfillsResource.create(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills"
        try:
            request = CreateBackfillRequest(range_start=range_start, range_end=range_end)
            response = await create_backfill.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if isinstance(response, CreateBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=CreateBackfillResponse401,
                type_400=CreateBackfillResponse400,
                type_403=CreateBackfillResponse403,
                type_429=CreateBackfillResponse429,
                type_500=CreateBackfillResponse500,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg=f"Invalid request parameters: {response}",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Invalid request parameters", context_404="Transfer not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    async def get(self, team_id: int, backfill_id: int) -> Backfill:
        """Retrieve a backfill by ID.

        Async version of BackfillsResource.get(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the backfill is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/backfills/{backfill_id}"
        try:
            response = await get_backfill_by_id.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
            )
            if isinstance(response, GetBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=GetBackfillByIdResponse401,
                type_403=GetBackfillByIdResponse403,
                type_429=GetBackfillByIdResponse429,
                type_500=GetBackfillByIdResponse500,
                not_found_msg="Backfill not found or you do not have access to it",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Backfill not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    async def get_latest(self, team_id: int, transfer_id: int) -> Backfill:
        """Get the latest backfill for a transfer.

        Async version of BackfillsResource.get_latest(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If no backfill exists or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills/latest"
        try:
            response = await get_latest_backfill.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if isinstance(response, GetBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=GetLatestBackfillResponse401,
                type_403=GetLatestBackfillResponse403,
                type_429=GetLatestBackfillResponse429,
                type_500=GetLatestBackfillResponse500,
                not_found_msg="No backfill found for this transfer",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Backfill not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

    async def list_incomplete(self, team_id: int) -> list[Backfill]:
        """List all incomplete backfills for a team.

        Async version of BackfillsResource.list_incomplete(). See sync version for full documentation.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/backfills"
        try:
            response = await list_incomplete_backfills.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if isinstance(response, ListIncompleteBackfillsResponse200):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=ListIncompleteBackfillsResponse401,
                type_403=ListIncompleteBackfillsResponse403,
                type_429=ListIncompleteBackfillsResponse429,
                type_500=ListIncompleteBackfillsResponse500,
                not_found_msg="No backfills found for this team",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e)
        except httpx.RequestError as e:
            _handle_request_error(e)

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
        try:
            body = UpdateBackfillStatusBody(status=UpdateBackfillStatusBodyStatus.CANCELLED)
            response = await update_backfill_status.asyncio(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
                body=body,
            )
            if isinstance(response, GetBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=UpdateBackfillStatusResponse401,
                type_400=UpdateBackfillStatusResponse400,
                type_403=UpdateBackfillStatusResponse403,
                type_429=UpdateBackfillStatusResponse429,
                type_500=UpdateBackfillStatusResponse500,
                not_found_msg="Backfill not found or you do not have access to it",
                bad_request_msg=f"Cannot cancel backfill - it may already be in a final state: {response}",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Cannot cancel backfill", context_404="Backfill not found")
        except httpx.RequestError as e:
            _handle_request_error(e)


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
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/backfills"
        try:
            request = CreateBackfillRequest(range_start=range_start, range_end=range_end)
            response = create_backfill.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if isinstance(response, CreateBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=CreateBackfillResponse401,
                type_400=CreateBackfillResponse400,
                type_403=CreateBackfillResponse403,
                type_429=CreateBackfillResponse429,
                type_500=CreateBackfillResponse500,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg=f"Invalid request parameters: {response}",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Invalid request parameters", context_404="Transfer not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

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
        try:
            response = get_backfill_by_id.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
            )
            if isinstance(response, GetBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=GetBackfillByIdResponse401,
                type_403=GetBackfillByIdResponse403,
                type_429=GetBackfillByIdResponse429,
                type_500=GetBackfillByIdResponse500,
                not_found_msg="Backfill not found or you do not have access to it",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Backfill not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

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
        try:
            response = get_latest_backfill.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if isinstance(response, GetBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=GetLatestBackfillResponse401,
                type_403=GetLatestBackfillResponse403,
                type_429=GetLatestBackfillResponse429,
                type_500=GetLatestBackfillResponse500,
                not_found_msg="No backfill found for this transfer",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_404="Backfill not found")
        except httpx.RequestError as e:
            _handle_request_error(e)

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
        try:
            response = list_incomplete_backfills.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if isinstance(response, ListIncompleteBackfillsResponse200):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=ListIncompleteBackfillsResponse401,
                type_403=ListIncompleteBackfillsResponse403,
                type_429=ListIncompleteBackfillsResponse429,
                type_500=ListIncompleteBackfillsResponse500,
                not_found_msg="No backfills found for this team",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e)
        except httpx.RequestError as e:
            _handle_request_error(e)

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
        try:
            body = UpdateBackfillStatusBody(status=UpdateBackfillStatusBodyStatus.CANCELLED)
            response = update_backfill_status.sync(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                backfill_id=backfill_id,
                body=body,
            )
            if isinstance(response, GetBackfillResponse):
                return response.data
            _raise_for_response(
                response, endpoint,
                type_401=UpdateBackfillStatusResponse401,
                type_400=UpdateBackfillStatusResponse400,
                type_403=UpdateBackfillStatusResponse403,
                type_429=UpdateBackfillStatusResponse429,
                type_500=UpdateBackfillStatusResponse500,
                not_found_msg="Backfill not found or you do not have access to it",
                bad_request_msg=f"Cannot cancel backfill - it may already be in a final state: {response}",
            )
        except (AuthenticationError, ValidationError, APIError):
            raise
        except httpx.HTTPStatusError as e:
            _handle_http_error(e, context_400="Cannot cancel backfill", context_404="Backfill not found")
        except httpx.RequestError as e:
            _handle_request_error(e)
