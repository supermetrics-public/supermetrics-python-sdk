"""Unit tests for BackfillsResource."""

import datetime
from unittest.mock import MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.backfill import Backfill
from supermetrics._generated.supermetrics_api_client.models.backfill_status import BackfillStatus
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response import CreateBackfillResponse
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_400 import CreateBackfillResponse400
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_401 import CreateBackfillResponse401
from supermetrics._generated.supermetrics_api_client.models.create_backfill_response_500 import CreateBackfillResponse500
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.error_response_error import ErrorResponseError
from supermetrics._generated.supermetrics_api_client.models.get_backfill_by_id_response_401 import GetBackfillByIdResponse401
from supermetrics._generated.supermetrics_api_client.models.get_backfill_by_id_response_500 import GetBackfillByIdResponse500
from supermetrics._generated.supermetrics_api_client.models.get_backfill_response import GetBackfillResponse
from supermetrics._generated.supermetrics_api_client.models.get_latest_backfill_response_401 import GetLatestBackfillResponse401
from supermetrics._generated.supermetrics_api_client.models.get_latest_backfill_response_500 import GetLatestBackfillResponse500
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_200 import (
    ListIncompleteBackfillsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_401 import (
    ListIncompleteBackfillsResponse401,
)
from supermetrics._generated.supermetrics_api_client.models.list_incomplete_backfills_response_500 import (
    ListIncompleteBackfillsResponse500,
)
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_400 import (
    UpdateBackfillStatusResponse400,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_401 import (
    UpdateBackfillStatusResponse401,
)
from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_response_500 import (
    UpdateBackfillStatusResponse500,
)
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.backfills import BackfillsResource


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
    def meta(self) -> Meta:
        """Create a sample Meta object."""
        return Meta(request_id="test-request-id")

    @pytest.fixture
    def sample_backfill(self) -> Backfill:
        """Create a sample Backfill for testing."""
        return Backfill(
            transfer_backfill_id=67890,
            transfer_id=456789,
            range_start_date=datetime.date(2024, 1, 1),
            range_end_date=datetime.date(2024, 1, 31),
            created_time=datetime.datetime(2024, 2, 1, 9, 0, 0, tzinfo=datetime.timezone.utc),
            created_user_id=789,
            status=BackfillStatus.CREATED,
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
            created_time=datetime.datetime(2024, 3, 1, 9, 0, 0, tzinfo=datetime.timezone.utc),
            created_user_id=789,
            status=BackfillStatus.RUNNING,
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
        meta: Meta,
    ) -> None:
        """Test successful backfill creation."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync
        backfills_module.create_backfill.sync = MagicMock(
            return_value=CreateBackfillResponse(meta=meta, data=sample_backfill)
        )

        backfill = backfills_resource.create(
            team_id=12345,
            transfer_id=456789,
            range_start="2024-01-01",
            range_end="2024-01-31",
        )

        assert backfill.transfer_backfill_id == 67890
        assert backfill.transfer_id == 456789
        assert backfill.status == BackfillStatus.CREATED
        assert backfills_module.create_backfill.sync.called

        backfills_module.create_backfill.sync = original

    def test_create_backfill_passes_correct_params(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: Meta,
    ) -> None:
        """Test that create() passes correct parameters to the API."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync
        mock_sync = MagicMock(return_value=CreateBackfillResponse(meta=meta, data=sample_backfill))
        backfills_module.create_backfill.sync = mock_sync

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

        backfills_module.create_backfill.sync = original

    def test_create_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync
        backfills_module.create_backfill.sync = MagicMock(return_value=CreateBackfillResponse401())

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.create(team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31")

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.create_backfill.sync = original

    def test_create_backfill_validation_error_on_400(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises ValidationError on 400."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync
        backfills_module.create_backfill.sync = MagicMock(
            return_value=CreateBackfillResponse400(type_="about:blank", title="Bad Request", status=400)
        )

        with pytest.raises(ValidationError) as exc_info:
            backfills_resource.create(team_id=12345, transfer_id=456789, range_start="bad", range_end="bad")

        assert "Invalid request parameters" in str(exc_info.value)

        backfills_module.create_backfill.sync = original

    def test_create_backfill_api_error_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync
        error_response = ErrorResponse(
            meta=Meta(request_id="req-id"),
            error=ErrorResponseError(code="NOT_FOUND", message="Transfer not found"),
        )
        backfills_module.create_backfill.sync = MagicMock(return_value=error_response)

        with pytest.raises(APIError) as exc_info:
            backfills_resource.create(team_id=12345, transfer_id=999999, range_start="2024-01-01", range_end="2024-01-31")

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        backfills_module.create_backfill.sync = original

    def test_create_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that create() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.create_backfill.sync
        backfills_module.create_backfill.sync = MagicMock(return_value=CreateBackfillResponse500())

        with pytest.raises(APIError) as exc_info:
            backfills_resource.create(team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31")

        assert exc_info.value.status_code == 500

        backfills_module.create_backfill.sync = original

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

        original = backfills_module.create_backfill.sync
        backfills_module.create_backfill.sync = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.create(team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31")

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.create_backfill.sync = original

    # --- get() ---

    def test_get_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: Meta,
    ) -> None:
        """Test successful backfill retrieval by ID."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync
        backfills_module.get_backfill_by_id.sync = MagicMock(
            return_value=GetBackfillResponse(meta=meta, data=sample_backfill)
        )

        backfill = backfills_resource.get(team_id=12345, backfill_id=67890)

        assert backfill.transfer_backfill_id == 67890
        assert backfill.status == BackfillStatus.CREATED
        assert backfills_module.get_backfill_by_id.sync.called

        backfills_module.get_backfill_by_id.sync = original

    def test_get_backfill_not_found_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync
        error_response = ErrorResponse(
            meta=Meta(request_id="req-id"),
            error=ErrorResponseError(code="NOT_FOUND", message="Backfill not found"),
        )
        backfills_module.get_backfill_by_id.sync = MagicMock(return_value=error_response)

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        backfills_module.get_backfill_by_id.sync = original

    def test_get_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync
        backfills_module.get_backfill_by_id.sync = MagicMock(return_value=GetBackfillByIdResponse401())

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.get_backfill_by_id.sync = original

    def test_get_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_backfill_by_id.sync
        backfills_module.get_backfill_by_id.sync = MagicMock(return_value=GetBackfillByIdResponse500())

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 500

        backfills_module.get_backfill_by_id.sync = original

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

        original = backfills_module.get_backfill_by_id.sync
        backfills_module.get_backfill_by_id.sync = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.get(team_id=12345, backfill_id=67890)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.get_backfill_by_id.sync = original

    # --- get_latest() ---

    def test_get_latest_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_running_backfill: Backfill,
        meta: Meta,
    ) -> None:
        """Test successful retrieval of the latest backfill for a transfer."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync
        backfills_module.get_latest_backfill.sync = MagicMock(
            return_value=GetBackfillResponse(meta=meta, data=sample_running_backfill)
        )

        backfill = backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert backfill.transfer_backfill_id == 11111
        assert backfill.status == BackfillStatus.RUNNING
        assert backfills_module.get_latest_backfill.sync.called

        backfills_module.get_latest_backfill.sync = original

    def test_get_latest_backfill_not_found_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises APIError when no backfill exists (404)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync
        error_response = ErrorResponse(
            meta=Meta(request_id="req-id"),
            error=ErrorResponseError(code="NOT_FOUND", message="No backfill found"),
        )
        backfills_module.get_latest_backfill.sync = MagicMock(return_value=error_response)

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 404

        backfills_module.get_latest_backfill.sync = original

    def test_get_latest_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync
        backfills_module.get_latest_backfill.sync = MagicMock(return_value=GetLatestBackfillResponse401())

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.get_latest_backfill.sync = original

    def test_get_latest_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that get_latest() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.get_latest_backfill.sync
        backfills_module.get_latest_backfill.sync = MagicMock(return_value=GetLatestBackfillResponse500())

        with pytest.raises(APIError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert exc_info.value.status_code == 500

        backfills_module.get_latest_backfill.sync = original

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

        original = backfills_module.get_latest_backfill.sync
        backfills_module.get_latest_backfill.sync = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.get_latest(team_id=12345, transfer_id=456789)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.get_latest_backfill.sync = original

    # --- list_incomplete() ---

    def test_list_incomplete_backfills_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        sample_running_backfill: Backfill,
        meta: Meta,
    ) -> None:
        """Test successful listing of incomplete backfills."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync
        backfills_module.list_incomplete_backfills.sync = MagicMock(
            return_value=ListIncompleteBackfillsResponse200(
                meta=meta, data=[sample_backfill, sample_running_backfill]
            )
        )

        backfills = backfills_resource.list_incomplete(team_id=12345)

        assert len(backfills) == 2
        assert backfills[0].transfer_backfill_id == 67890
        assert backfills[1].transfer_backfill_id == 11111
        assert backfills_module.list_incomplete_backfills.sync.called

        backfills_module.list_incomplete_backfills.sync = original

    def test_list_incomplete_backfills_empty(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        meta: Meta,
    ) -> None:
        """Test list_incomplete() with empty list returns empty list."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync
        backfills_module.list_incomplete_backfills.sync = MagicMock(
            return_value=ListIncompleteBackfillsResponse200(meta=meta, data=[])
        )

        backfills = backfills_resource.list_incomplete(team_id=12345)

        assert backfills == []

        backfills_module.list_incomplete_backfills.sync = original

    def test_list_incomplete_backfills_passes_team_id(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        meta: Meta,
    ) -> None:
        """Test that list_incomplete() passes the correct team_id."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync
        mock_sync = MagicMock(return_value=ListIncompleteBackfillsResponse200(meta=meta, data=[]))
        backfills_module.list_incomplete_backfills.sync = mock_sync

        backfills_resource.list_incomplete(team_id=99999)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 99999

        backfills_module.list_incomplete_backfills.sync = original

    def test_list_incomplete_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync
        backfills_module.list_incomplete_backfills.sync = MagicMock(return_value=ListIncompleteBackfillsResponse401())

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.list_incomplete_backfills.sync = original

    def test_list_incomplete_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that list_incomplete() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.list_incomplete_backfills.sync
        backfills_module.list_incomplete_backfills.sync = MagicMock(return_value=ListIncompleteBackfillsResponse500())

        with pytest.raises(APIError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert exc_info.value.status_code == 500

        backfills_module.list_incomplete_backfills.sync = original

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

        original = backfills_module.list_incomplete_backfills.sync
        backfills_module.list_incomplete_backfills.sync = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.list_incomplete(team_id=12345)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.list_incomplete_backfills.sync = original

    # --- cancel() ---

    def test_cancel_backfill_success(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: Meta,
    ) -> None:
        """Test successful backfill cancellation."""
        cancelled_backfill = Backfill(
            transfer_backfill_id=sample_backfill.transfer_backfill_id,
            transfer_id=sample_backfill.transfer_id,
            range_start_date=sample_backfill.range_start_date,
            range_end_date=sample_backfill.range_end_date,
            created_time=sample_backfill.created_time,
            created_user_id=sample_backfill.created_user_id,
            status=BackfillStatus.CANCELLED,
            transfer_runs_total=sample_backfill.transfer_runs_total,
            transfer_runs_created=sample_backfill.transfer_runs_created,
            transfer_runs_completed=sample_backfill.transfer_runs_completed,
            transfer_runs_failed=sample_backfill.transfer_runs_failed,
        )

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync
        backfills_module.update_backfill_status.sync = MagicMock(
            return_value=GetBackfillResponse(meta=meta, data=cancelled_backfill)
        )

        result = backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert result.transfer_backfill_id == 67890
        assert result.status == BackfillStatus.CANCELLED
        assert backfills_module.update_backfill_status.sync.called

        backfills_module.update_backfill_status.sync = original

    def test_cancel_backfill_sends_cancelled_status(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
        sample_backfill: Backfill,
        meta: Meta,
    ) -> None:
        """Test that cancel() sends CANCELLED status in the request body."""
        from supermetrics._generated.supermetrics_api_client.models.update_backfill_status_body_status import (
            UpdateBackfillStatusBodyStatus,
        )

        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync
        mock_sync = MagicMock(return_value=GetBackfillResponse(meta=meta, data=sample_backfill))
        backfills_module.update_backfill_status.sync = mock_sync

        backfills_resource.cancel(team_id=12345, backfill_id=67890)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["backfill_id"] == 67890
        assert call_kwargs["body"].status == UpdateBackfillStatusBodyStatus.CANCELLED

        backfills_module.update_backfill_status.sync = original

    def test_cancel_backfill_auth_error_on_401(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises AuthenticationError on 401."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync
        backfills_module.update_backfill_status.sync = MagicMock(return_value=UpdateBackfillStatusResponse401())

        with pytest.raises(AuthenticationError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert "Invalid or expired API key" in str(exc_info.value)

        backfills_module.update_backfill_status.sync = original

    def test_cancel_backfill_validation_error_on_400(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises ValidationError on 400 (e.g., already in final state)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync
        backfills_module.update_backfill_status.sync = MagicMock(
            return_value=UpdateBackfillStatusResponse400(type_="about:blank", title="Bad Request", status=400)
        )

        with pytest.raises(ValidationError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert "Cannot cancel backfill" in str(exc_info.value)

        backfills_module.update_backfill_status.sync = original

    def test_cancel_backfill_not_found_on_404(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync
        error_response = ErrorResponse(
            meta=Meta(request_id="req-id"),
            error=ErrorResponseError(code="NOT_FOUND", message="Backfill not found"),
        )
        backfills_module.update_backfill_status.sync = MagicMock(return_value=error_response)

        with pytest.raises(APIError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        backfills_module.update_backfill_status.sync = original

    def test_cancel_backfill_api_error_on_500(
        self,
        backfills_resource: BackfillsResource,
        mock_client: MagicMock,
    ) -> None:
        """Test that cancel() raises APIError on 500."""
        import supermetrics.resources.backfills as backfills_module

        original = backfills_module.update_backfill_status.sync
        backfills_module.update_backfill_status.sync = MagicMock(return_value=UpdateBackfillStatusResponse500())

        with pytest.raises(APIError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert exc_info.value.status_code == 500

        backfills_module.update_backfill_status.sync = original

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

        original = backfills_module.update_backfill_status.sync
        backfills_module.update_backfill_status.sync = MagicMock(side_effect=error)

        with pytest.raises(NetworkError) as exc_info:
            backfills_resource.cancel(team_id=12345, backfill_id=67890)

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

        backfills_module.update_backfill_status.sync = original
