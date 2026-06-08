"""Unit tests for BackfillsResource and BackfillsAsyncResource."""

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.backfill import Backfill
from supermetrics._generated.supermetrics_api_client.models.backfill_response import BackfillResponse
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_200 import (
    ListIncompleteBackfillsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.types import Response
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.backfills import BackfillsAsyncResource, BackfillsResource


def _make_success_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=parsed)


def _make_error_response(status_code: HTTPStatus, code: str, message: str) -> Response:
    return Response(
        status_code=status_code,
        content=b"",
        headers={},
        parsed=ErrorResponse(
            meta=ResponseMeta(request_id="req-id"),
            error=Error(code=code, message=message),
        ),
    )


class TestBackfillsResource:
    """Test suite for BackfillsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def backfills_resource(self, mock_client: MagicMock) -> BackfillsResource:
        """Create a BackfillsResource instance with mock client."""
        return BackfillsResource(mock_client)

    @pytest.fixture
    def meta(self) -> ResponseMeta:
        """Create a sample ResponseMeta object."""
        return ResponseMeta(request_id="test-request-id")

    @pytest.fixture
    def sample_backfill(self) -> Backfill:
        """Create a sample Backfill for testing."""
        return Backfill(
            transfer_backfill_id=67890,
            transfer_id=456789,
            range_start_date=datetime.date(2024, 1, 1),
            range_end_date=datetime.date(2024, 1, 31),
            created_time=datetime.datetime(2024, 2, 1, 9, 0, 0, tzinfo=datetime.UTC),
            created_user_id=789,
            status="CREATED",
            transfer_runs_total=31,
            transfer_runs_created=31,
            transfer_runs_completed=0,
            transfer_runs_failed=0,
        )

    @pytest.fixture
    def sample_running_backfill(self) -> Backfill:
        """Create a sample running Backfill for testing."""
        return Backfill(
            transfer_backfill_id=11111,
            transfer_id=456789,
            range_start_date=datetime.date(2024, 2, 1),
            range_end_date=datetime.date(2024, 2, 29),
            created_time=datetime.datetime(2024, 3, 1, 9, 0, 0, tzinfo=datetime.UTC),
            created_user_id=789,
            status="RUNNING",
            transfer_runs_total=29,
            transfer_runs_created=29,
            transfer_runs_completed=15,
            transfer_runs_failed=0,
        )

    # --- create() ---

    def test_create_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful backfill creation."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill))
        )

        backfill = backfills_resource.create(
            team_id=12345,
            transfer_id=456789,
            range_start="2024-01-01",
            range_end="2024-01-31",
        )

        assert backfill.transfer_backfill_id == 67890
        assert backfill.transfer_id == 456789
        assert backfill.status == "CREATED"
        assert backfills_module.create_backfill.sync_detailed.called

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_passes_correct_params(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test that create() passes correct parameters to the API."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill)))
        backfills_module.create_backfill.sync_detailed = mock_sync

        backfills_resource.create(
            team_id=12345,
            transfer_id=456789,
            range_start="2024-01-01",
            range_end="2024-01-31",
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 456789
        assert call_kwargs["body"].range_start == "2024-01-01"
        assert call_kwargs["body"].range_end == "2024-01-31"

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_validation_error_on_400(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises ValidationError on 400."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Invalid request parameters")
        )

        with pytest.raises(ValidationError) as exc_info:
            backfills_resource.create(team_id=12345, transfer_id=456789, range_start="bad", range_end="bad")

        assert "Invalid request parameters" in str(exc_info.value)

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_api_error_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.create(
                team_id=12345, transfer_id=999999, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Internal server error"
            )
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert exc_info.value.status_code == 500

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_api_error_on_403(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises APIError on 403."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert exc_info.value.status_code == 403
        assert "Forbidden" in str(exc_info.value)

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_api_error_on_429(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert exc_info.value.status_code == 429

        backfills_module.create_backfill.sync_detailed = original

    def test_create_backfill_network_error(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises NetworkError on network timeout."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync_detailed
        backfills_module.create_backfill.sync_detailed = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.create_backfill.sync_detailed = original

    # --- get() ---

    def test_get_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful backfill retrieval by ID."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill))
        )

        backfill = backfills_resource.get(team_id=12345, backfill_id=67890)

        assert backfill.transfer_backfill_id == 67890
        assert backfill.status == "CREATED"
        assert backfills_module.get_backfill_by_id.sync_detailed.called

        backfills_module.get_backfill_by_id.sync_detailed = original

    def test_get_backfill_not_found_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Backfill not found")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        backfills_module.get_backfill_by_id.sync_detailed = original

    def test_get_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.get_backfill_by_id.sync_detailed = original

    def test_get_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(
            return_value=_make_error_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Internal server error"
            )
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 500

        backfills_module.get_backfill_by_id.sync_detailed = original

    def test_get_backfill_api_error_on_403(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises APIError on 403."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 403
        assert "Forbidden" in str(exc_info.value)

        backfills_module.get_backfill_by_id.sync_detailed = original

    def test_get_backfill_api_error_on_429(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 429

        backfills_module.get_backfill_by_id.sync_detailed = original

    def test_get_backfill_network_error(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync_detailed
        backfills_module.get_backfill_by_id.sync_detailed = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.get_backfill_by_id.sync_detailed = original

    # --- get_latest() ---

    def test_get_latest_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_running_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful retrieval of the latest backfill for a transfer."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_running_backfill))
        )

        backfill = backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert backfill.transfer_backfill_id == 11111
        assert backfill.status == "RUNNING"
        assert backfills_module.get_latest_backfill.sync_detailed.called

        backfills_module.get_latest_backfill.sync_detailed = original

    def test_get_latest_backfill_not_found_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises APIError when no backfill exists (404)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "No backfill found")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 404

        backfills_module.get_latest_backfill.sync_detailed = original

    def test_get_latest_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.get_latest_backfill.sync_detailed = original

    def test_get_latest_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Internal server error"
            )
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 500

        backfills_module.get_latest_backfill.sync_detailed = original

    def test_get_latest_backfill_api_error_on_403(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises APIError on 403."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 403
        assert "Forbidden" in str(exc_info.value)

        backfills_module.get_latest_backfill.sync_detailed = original

    def test_get_latest_backfill_api_error_on_429(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 429

        backfills_module.get_latest_backfill.sync_detailed = original

    def test_get_latest_backfill_network_error(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync_detailed
        backfills_module.get_latest_backfill.sync_detailed = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.get_latest_backfill.sync_detailed = original

    # --- list_incomplete() ---

    def test_list_incomplete_backfills_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        sample_running_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful listing of incomplete backfills."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(
            return_value=_make_success_response(
                ListIncompleteBackfillsResponse200(meta=meta, data=[sample_backfill, sample_running_backfill])
            )
        )

        backfills = backfills_resource.list_incomplete(team_id=12345)

        assert len(backfills) == 2
        assert backfills[0].transfer_backfill_id == 67890
        assert backfills[1].transfer_backfill_id == 11111
        assert backfills_module.list_incomplete_backfills.sync_detailed.called

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_backfills_empty(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        meta: ResponseMeta,
    ) -> None:
        """Test list_incomplete() with empty list returns empty list."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(
            return_value=_make_success_response(ListIncompleteBackfillsResponse200(meta=meta, data=[]))
        )

        backfills = backfills_resource.list_incomplete(team_id=12345)

        assert backfills == []

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_backfills_passes_team_id(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        meta: ResponseMeta,
    ) -> None:
        """Test that list_incomplete() passes the correct team_id."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(ListIncompleteBackfillsResponse200(meta=meta, data=[]))
        )
        backfills_module.list_incomplete_backfills.sync_detailed = mock_sync

        backfills_resource.list_incomplete(team_id=99999)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 99999

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(
            return_value=_make_error_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Internal server error"
            )
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert exc_info.value.status_code == 500

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_api_error_on_403(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises APIError on 403."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert exc_info.value.status_code == 403
        assert "Forbidden" in str(exc_info.value)

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_api_error_on_429(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert exc_info.value.status_code == 429

        backfills_module.list_incomplete_backfills.sync_detailed = original

    def test_list_incomplete_network_error(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync_detailed
        backfills_module.list_incomplete_backfills.sync_detailed = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.list_incomplete_backfills.sync_detailed = original

    # --- cancel() ---

    def test_cancel_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful backfill cancellation."""
        cancelled_backfill = Backfill(
            transfer_backfill_id=sample_backfill.transfer_backfill_id,
            transfer_id=sample_backfill.transfer_id,
            range_start_date=sample_backfill.range_start_date,
            range_end_date=sample_backfill.range_end_date,
            created_time=sample_backfill.created_time,
            created_user_id=sample_backfill.created_user_id,
            status="CANCELLED",
            transfer_runs_total=sample_backfill.transfer_runs_total,
            transfer_runs_created=sample_backfill.transfer_runs_created,
            transfer_runs_completed=sample_backfill.transfer_runs_completed,
            transfer_runs_failed=sample_backfill.transfer_runs_failed,
        )

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=cancelled_backfill))
        )

        result = backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert result.transfer_backfill_id == 67890
        assert result.status == "CANCELLED"
        assert backfills_module.update_backfill_status.sync_detailed.called

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_sends_cancelled_status(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test that cancel() sends CANCELLED status in the request body."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill)))
        backfills_module.update_backfill_status.sync_detailed = mock_sync

        backfills_resource.cancel(team_id=12345, backfill_id=67890)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["backfill_id"] == 67890
        assert call_kwargs["body"].status == "CANCELLED"

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_validation_error_on_400(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises ValidationError on 400 (e.g., already in final state)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Backfill already in final state")
        )

        with pytest.raises(ValidationError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert "Cannot cancel backfill" in str(exc_info.value)

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_not_found_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Backfill not found")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_error_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Internal server error"
            )
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 500

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_api_error_on_403(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises APIError on 403."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 403
        assert "Forbidden" in str(exc_info.value)

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_api_error_on_429(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 429

        backfills_module.update_backfill_status.sync_detailed = original

    def test_cancel_backfill_network_error(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync_detailed
        backfills_module.update_backfill_status.sync_detailed = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.update_backfill_status.sync_detailed = original


class TestBackfillsAsyncResource:
    """Test suite for BackfillsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def backfills_async_resource(self, mock_client: MagicMock) -> BackfillsAsyncResource:
        return BackfillsAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> ResponseMeta:
        return ResponseMeta(request_id="test-request-id")

    @pytest.fixture
    def sample_backfill(self) -> Backfill:
        return Backfill(
            transfer_backfill_id=67890,
            transfer_id=456789,
            range_start_date=datetime.date(2024, 1, 1),
            range_end_date=datetime.date(2024, 1, 31),
            created_time=datetime.datetime(2024, 2, 1, 9, 0, 0, tzinfo=datetime.UTC),
            created_user_id=789,
            status="CREATED",
            transfer_runs_total=31,
            transfer_runs_created=31,
            transfer_runs_completed=0,
            transfer_runs_failed=0,
        )

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        backfills_async_resource: BackfillsAsyncResource,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful async backfill creation."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.asyncio_detailed
        backfills_module.create_backfill.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill))
        )

        backfill = await backfills_async_resource.create(
            team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
        )

        assert backfill.transfer_backfill_id == 67890
        assert backfill.status == "CREATED"
        assert backfills_module.create_backfill.asyncio_detailed.called

        backfills_module.create_backfill.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_auth_error_on_401(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async create() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.asyncio_detailed
        backfills_module.create_backfill.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError):
            await backfills_async_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        backfills_module.create_backfill.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_api_error_on_429(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async create() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.asyncio_detailed
        backfills_module.create_backfill.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            await backfills_async_resource.create(
                team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31"
            )

        assert exc_info.value.status_code == 429

        backfills_module.create_backfill.asyncio_detailed = original

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        backfills_async_resource: BackfillsAsyncResource,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful async backfill retrieval by ID."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.asyncio_detailed
        backfills_module.get_backfill_by_id.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill))
        )

        backfill = await backfills_async_resource.get(team_id=12345, backfill_id=67890)

        assert backfill.transfer_backfill_id == 67890
        assert backfills_module.get_backfill_by_id.asyncio_detailed.called

        backfills_module.get_backfill_by_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_auth_error_on_401(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async get() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.asyncio_detailed
        backfills_module.get_backfill_by_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError):
            await backfills_async_resource.get(team_id=12345, backfill_id=67890)

        backfills_module.get_backfill_by_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_429(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async get() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.asyncio_detailed
        backfills_module.get_backfill_by_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            await backfills_async_resource.get(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 429

        backfills_module.get_backfill_by_id.asyncio_detailed = original

    # --- get_latest() ---

    @pytest.mark.asyncio
    async def test_get_latest_success(
        self,
        backfills_async_resource: BackfillsAsyncResource,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful async retrieval of latest backfill."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.asyncio_detailed
        backfills_module.get_latest_backfill.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=sample_backfill))
        )

        backfill = await backfills_async_resource.get_latest(team_id=12345, transfer_id=456789)

        assert backfill.transfer_backfill_id == 67890
        assert backfills_module.get_latest_backfill.asyncio_detailed.called

        backfills_module.get_latest_backfill.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_latest_auth_error_on_401(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async get_latest() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.asyncio_detailed
        backfills_module.get_latest_backfill.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError):
            await backfills_async_resource.get_latest(team_id=12345, transfer_id=456789)

        backfills_module.get_latest_backfill.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_latest_api_error_on_429(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async get_latest() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.asyncio_detailed
        backfills_module.get_latest_backfill.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            await backfills_async_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 429

        backfills_module.get_latest_backfill.asyncio_detailed = original

    # --- list_incomplete() ---

    @pytest.mark.asyncio
    async def test_list_incomplete_success(
        self,
        backfills_async_resource: BackfillsAsyncResource,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful async listing of incomplete backfills."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.asyncio_detailed
        backfills_module.list_incomplete_backfills.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(ListIncompleteBackfillsResponse200(meta=meta, data=[sample_backfill]))
        )

        backfills = await backfills_async_resource.list_incomplete(team_id=12345)

        assert len(backfills) == 1
        assert backfills[0].transfer_backfill_id == 67890
        assert backfills_module.list_incomplete_backfills.asyncio_detailed.called

        backfills_module.list_incomplete_backfills.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_incomplete_auth_error_on_401(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async list_incomplete() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.asyncio_detailed
        backfills_module.list_incomplete_backfills.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError):
            await backfills_async_resource.list_incomplete(team_id=12345)

        backfills_module.list_incomplete_backfills.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_incomplete_api_error_on_429(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async list_incomplete() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.asyncio_detailed
        backfills_module.list_incomplete_backfills.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            await backfills_async_resource.list_incomplete(team_id=12345)

        assert exc_info.value.status_code == 429

        backfills_module.list_incomplete_backfills.asyncio_detailed = original

    # --- cancel() ---

    @pytest.mark.asyncio
    async def test_cancel_success(
        self,
        backfills_async_resource: BackfillsAsyncResource,
        sample_backfill: Backfill,
        meta: ResponseMeta,
    ) -> None:
        """Test successful async backfill cancellation."""
        cancelled = Backfill(
            transfer_backfill_id=sample_backfill.transfer_backfill_id,
            transfer_id=sample_backfill.transfer_id,
            range_start_date=sample_backfill.range_start_date,
            range_end_date=sample_backfill.range_end_date,
            created_time=sample_backfill.created_time,
            created_user_id=sample_backfill.created_user_id,
            status="CANCELLED",
            transfer_runs_total=sample_backfill.transfer_runs_total,
            transfer_runs_created=sample_backfill.transfer_runs_created,
            transfer_runs_completed=sample_backfill.transfer_runs_completed,
            transfer_runs_failed=sample_backfill.transfer_runs_failed,
        )

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.asyncio_detailed
        backfills_module.update_backfill_status.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(BackfillResponse(meta=meta, data=cancelled))
        )

        result = await backfills_async_resource.cancel(team_id=12345, backfill_id=67890)

        assert result.status == "CANCELLED"
        assert backfills_module.update_backfill_status.asyncio_detailed.called

        backfills_module.update_backfill_status.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_cancel_auth_error_on_401(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async cancel() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.asyncio_detailed
        backfills_module.update_backfill_status.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError):
            await backfills_async_resource.cancel(team_id=12345, backfill_id=67890)

        backfills_module.update_backfill_status.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_cancel_api_error_on_429(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async cancel() raises APIError on 429."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.asyncio_detailed
        backfills_module.update_backfill_status.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMIT", "Rate limit exceeded")
        )

        with pytest.raises(APIError) as exc_info:
            await backfills_async_resource.cancel(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 429

        backfills_module.update_backfill_status.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_cancel_network_error(
        self,
        backfills_async_resource: BackfillsAsyncResource,
    ) -> None:
        """Test that async cancel() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.asyncio_detailed
        backfills_module.update_backfill_status.asyncio_detailed = AsyncMock(side_effect=error)

        with pytest.raises(NetworkError):
            await backfills_async_resource.cancel(team_id=12345, backfill_id=67890)

        backfills_module.update_backfill_status.asyncio_detailed = original
