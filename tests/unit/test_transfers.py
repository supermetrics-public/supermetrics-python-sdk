"""Unit tests for TransfersResource and TransfersAsyncResource."""

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import UUID

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.available_sources_response import AvailableSourcesResponse
from supermetrics._generated.supermetrics_api_client.models.create_data_source_connection_response import (
    CreateDataSourceConnectionResponse,
)
from supermetrics._generated.supermetrics_api_client.models.data_source_connection import DataSourceConnection
from supermetrics._generated.supermetrics_api_client.models.data_source_info import DataSourceInfo
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.models.transfer_account import TransferAccount
from supermetrics._generated.supermetrics_api_client.models.transfer_configuration_response import (
    TransferConfigurationResponse,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_created_envelope import TransferCreatedEnvelope
from supermetrics._generated.supermetrics_api_client.models.transfer_created_response import TransferCreatedResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_destination import TransferDestination
from supermetrics._generated.supermetrics_api_client.models.transfer_info_response import TransferInfoResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_list_response import TransferListResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_options_response import TransferOptionsResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_run_item import TransferRunItem
from supermetrics._generated.supermetrics_api_client.models.transfer_run_list_response import TransferRunListResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_schedule import TransferSchedule
from supermetrics._generated.supermetrics_api_client.models.transfer_segment import TransferSegment
from supermetrics._generated.supermetrics_api_client.models.transfer_state_update_response import (
    TransferStateUpdateResponse,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_updated_response import TransferUpdatedResponse
from supermetrics._generated.supermetrics_api_client.models.validation_error import (
    ValidationError as FieldValidationError,
)
from supermetrics._generated.supermetrics_api_client.models.validation_errors_response import ValidationErrorsResponse
from supermetrics._generated.supermetrics_api_client.types import UNSET, Response
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.transfers import TransfersAsyncResource, TransfersResource

CONNECTION_ID = UUID("2f1c4a5e-9b3d-4a7f-8c21-6d0e5b7a3f92")


def _make_success_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=parsed)


def _make_created_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.CREATED, content=b"", headers={}, parsed=parsed)


def _make_no_content_response() -> Response:
    return Response(status_code=HTTPStatus.NO_CONTENT, content=b"", headers={}, parsed=None)


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


class TestTransfersResource:
    """Test suite for TransfersResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def transfers_resource(self, mock_client: MagicMock) -> TransfersResource:
        """Create a TransfersResource instance with mock client."""
        return TransfersResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def schedule(self) -> list[TransferSchedule]:
        """Create a sample transfer schedule."""
        return [TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)]

    @pytest.fixture
    def accounts(self) -> list[TransferAccount]:
        """Create a sample list of transfer accounts."""
        return [TransferAccount(login_id=2682599, account_id="8733197711")]

    @pytest.fixture
    def sample_transfer_info(self) -> TransferInfoResponse:
        """Create a sample transfer summary for testing."""
        return TransferInfoResponse(
            dwh_transfer_id=36091,
            display_name="AW enhanced",
            status="OK",
            state="ACTIVE",
            schedule="Daily at 22:00",
        )

    @pytest.fixture
    def sample_configuration(self, schedule: list[TransferSchedule]) -> TransferConfigurationResponse:
        """Create a sample transfer configuration for testing."""
        return TransferConfigurationResponse(
            transfer_id=36091,
            display_name="AW enhanced",
            schema_id=2,
            destination_id=8,
            schedule=schedule,
        )

    @pytest.fixture
    def sample_created(self) -> TransferCreatedResponse:
        """Create a sample transfer-created payload for testing."""
        return TransferCreatedResponse(transfer_id=36091, transfer_name="AW enhanced")

    @pytest.fixture
    def sample_updated(self) -> TransferUpdatedResponse:
        """Create a sample transfer-updated payload for testing."""
        return TransferUpdatedResponse(transfer_id=36091, transfer_name="AW enhanced (hourly)")

    @pytest.fixture
    def sample_state(self) -> TransferStateUpdateResponse:
        """Create a sample state-change payload for testing."""
        return TransferStateUpdateResponse(result=True, state="PAUSED")

    @pytest.fixture
    def sample_available_sources(self) -> AvailableSourcesResponse:
        """Create a sample available-sources payload for testing."""
        return AvailableSourcesResponse(
            data_sources=[DataSourceInfo(data_source_id="AW", service_name="Google Ads")],
            destinations=[TransferDestination(destination_id=8, destination_name="BigQuery")],
        )

    @pytest.fixture
    def sample_options(self) -> TransferOptionsResponse:
        """Create a sample transfer-options payload for testing."""
        return TransferOptionsResponse(schemas=[], logins=[], accounts=[])

    @pytest.fixture
    def sample_run_item(self) -> TransferRunItem:
        """Create a sample transfer run summary for testing."""
        return TransferRunItem(
            id=98765,
            status="SUCCESS",
            type_="Recurring",
            message="",
            data_date=datetime.date(2024, 1, 15),
            total_rows=4200,
        )

    @pytest.fixture
    def sample_connection(self) -> DataSourceConnection:
        """Create a sample data source connection for testing."""
        return DataSourceConnection(connection_id=CONNECTION_ID, login_url="https://example.test/login")

    # --- list() ---

    def test_list_success(
        self,
        transfers_resource: TransfersResource,
        sample_transfer_info: TransferInfoResponse,
        meta: Meta,
    ) -> None:
        """Test successful transfer listing."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.sync_detailed
        module.list_transfers.sync_detailed = MagicMock(
            return_value=_make_success_response(TransferListResponse(meta=meta, data=[sample_transfer_info]))
        )

        transfers = transfers_resource.list(team_id=12345)

        assert len(transfers) == 1
        assert transfers[0].dwh_transfer_id == 36091
        assert transfers[0].state == "ACTIVE"

        module.list_transfers.sync_detailed = original

    def test_list_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_transfer_info: TransferInfoResponse,
        meta: Meta,
    ) -> None:
        """Test that list() passes the correct parameters to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(TransferListResponse(meta=meta, data=[sample_transfer_info]))
        )
        module.list_transfers.sync_detailed = mock_sync

        transfers_resource.list(team_id=12345)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345

        module.list_transfers.sync_detailed = original

    def test_list_auth_error_on_401(self, transfers_resource: TransfersResource) -> None:
        """Test that list() raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.sync_detailed
        module.list_transfers.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            transfers_resource.list(team_id=12345)

        assert exc_info.value.status_code == 401
        assert "Invalid or expired API key" in str(exc_info.value)

        module.list_transfers.sync_detailed = original

    def test_list_api_error_on_500(self, transfers_resource: TransfersResource) -> None:
        """Test that list() raises APIError on 500."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.sync_detailed
        module.list_transfers.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.list(team_id=12345)

        assert exc_info.value.status_code == 500

        module.list_transfers.sync_detailed = original

    def test_list_network_error(self, transfers_resource: TransfersResource) -> None:
        """Test that list() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.sync_detailed
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/teams/12345/transfers"
        module.list_transfers.sync_detailed = MagicMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        with pytest.raises(NetworkError):
            transfers_resource.list(team_id=12345)

        module.list_transfers.sync_detailed = original

    # --- get() ---

    def test_get_success(
        self,
        transfers_resource: TransfersResource,
        sample_configuration: TransferConfigurationResponse,
    ) -> None:
        """Test successful transfer configuration retrieval from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer.sync_detailed
        module.get_transfer.sync_detailed = MagicMock(return_value=_make_success_response(sample_configuration))

        configuration = transfers_resource.get(team_id=12345, transfer_id=36091)

        assert configuration.transfer_id == 36091
        assert configuration.display_name == "AW enhanced"
        assert configuration.schema_id == 2

        module.get_transfer.sync_detailed = original

    def test_get_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_configuration: TransferConfigurationResponse,
    ) -> None:
        """Test that get() passes the correct parameters to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_configuration))
        module.get_transfer.sync_detailed = mock_sync

        transfers_resource.get(team_id=12345, transfer_id=36091)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091

        module.get_transfer.sync_detailed = original

    def test_get_api_error_on_404(self, transfers_resource: TransfersResource) -> None:
        """Test that get() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer.sync_detailed
        module.get_transfer.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.get(team_id=12345, transfer_id=999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        module.get_transfer.sync_detailed = original

    # --- create() ---

    def test_create_success(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful transfer creation, which the API answers with HTTP 201."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.sync_detailed
        module.create_transfer.sync_detailed = MagicMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )

        created = transfers_resource.create(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        assert created.transfer_id == 36091
        assert created.transfer_name == "AW enhanced"

        module.create_transfer.sync_detailed = original

    def test_create_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that create() passes the correct body to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.create_transfer.sync_detailed = mock_sync

        segments = [TransferSegment(login_id=2682599, segment_id="seg-1")]
        transfers_resource.create(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
            segments=segments,
            notification_recipients=["ops@example.test"],
            transfer_type=1,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        body = call_kwargs["body"]
        assert body.data_source_id == "AW"
        assert body.schema_id == 2
        assert body.destination_id == 8
        assert body.display_name == "AW enhanced"
        assert body.schedule == schedule
        assert body.accounts == accounts
        assert body.segments == segments
        assert body.notification_recipients == ["ops@example.test"]
        assert body.transfer_type == 1

        module.create_transfer.sync_detailed = original

    def test_create_omits_optional_fields(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that create() leaves omitted optional fields UNSET rather than null."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.create_transfer.sync_detailed = mock_sync

        transfers_resource.create(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        body = mock_sync.call_args.kwargs["body"]
        assert body.segments is UNSET
        assert body.data_source_settings is UNSET
        assert body.notification_recipients is UNSET
        assert body.transfer_type is UNSET
        assert "segments" not in body.to_dict()

        module.create_transfer.sync_detailed = original

    def test_create_validation_error_on_400(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that create() raises ValidationError on 400."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.sync_detailed
        module.create_transfer.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Invalid configuration")
        )

        with pytest.raises(ValidationError) as exc_info:
            transfers_resource.create(
                team_id=12345,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 400
        assert "Invalid transfer configuration" in str(exc_info.value)

        module.create_transfer.sync_detailed = original

    # --- update() ---

    def test_update_success(
        self,
        transfers_resource: TransfersResource,
        sample_updated: TransferUpdatedResponse,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful transfer update from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.update_transfer.sync_detailed
        module.update_transfer.sync_detailed = MagicMock(return_value=_make_success_response(sample_updated))

        updated = transfers_resource.update(
            team_id=12345,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced (hourly)",
            schedule=schedule,
            accounts=accounts,
        )

        assert updated.transfer_id == 36091
        assert updated.transfer_name == "AW enhanced (hourly)"

        module.update_transfer.sync_detailed = original

    def test_update_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_updated: TransferUpdatedResponse,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that update() passes the transfer id and body to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.update_transfer.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_updated))
        module.update_transfer.sync_detailed = mock_sync

        transfers_resource.update(
            team_id=12345,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced (hourly)",
            schedule=schedule,
            accounts=accounts,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091
        body = call_kwargs["body"]
        assert body.display_name == "AW enhanced (hourly)"
        assert body.accounts == accounts

        module.update_transfer.sync_detailed = original

    def test_update_api_error_on_404(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that update() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.update_transfer.sync_detailed
        module.update_transfer.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.update(
                team_id=12345,
                transfer_id=999,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="AW enhanced",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 404

        module.update_transfer.sync_detailed = original

    # --- delete() ---

    def test_delete_success(self, transfers_resource: TransfersResource) -> None:
        """Test that delete() returns None on the API's 204 No Content."""
        import supermetrics.resources.transfers as module

        original = module.delete_transfer.sync_detailed
        module.delete_transfer.sync_detailed = MagicMock(return_value=_make_no_content_response())

        result = transfers_resource.delete(team_id=12345, transfer_id=36091)

        assert result is None

        module.delete_transfer.sync_detailed = original

    def test_delete_passes_correct_params(self, transfers_resource: TransfersResource) -> None:
        """Test that delete() passes the correct parameters to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.delete_transfer.sync_detailed
        mock_sync = MagicMock(return_value=_make_no_content_response())
        module.delete_transfer.sync_detailed = mock_sync

        transfers_resource.delete(team_id=12345, transfer_id=36091)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091

        module.delete_transfer.sync_detailed = original

    def test_delete_api_error_on_404(self, transfers_resource: TransfersResource) -> None:
        """Test that delete() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.delete_transfer.sync_detailed
        module.delete_transfer.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.delete(team_id=12345, transfer_id=999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        module.delete_transfer.sync_detailed = original

    # --- set_state() ---

    def test_set_state_success(
        self,
        transfers_resource: TransfersResource,
        sample_state: TransferStateUpdateResponse,
    ) -> None:
        """Test successful pause, whose response reports the state in upper case."""
        import supermetrics.resources.transfers as module

        original = module.change_transfer_state.sync_detailed
        module.change_transfer_state.sync_detailed = MagicMock(return_value=_make_success_response(sample_state))

        paused = transfers_resource.set_state(team_id=12345, transfer_id=36091, state="pause")

        assert paused.result is True
        assert paused.state == "PAUSED"

        module.change_transfer_state.sync_detailed = original

    def test_set_state_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_state: TransferStateUpdateResponse,
    ) -> None:
        """Test that set_state() sends the lower-case verb in the request body."""
        import supermetrics.resources.transfers as module

        original = module.change_transfer_state.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_state))
        module.change_transfer_state.sync_detailed = mock_sync

        transfers_resource.set_state(team_id=12345, transfer_id=36091, state="pause")

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["body"].transfer_state == "pause"
        assert call_kwargs["body"].to_dict() == {"transfer_state": "pause"}

        transfers_resource.set_state(team_id=12345, transfer_id=36091, state="unpause")

        assert mock_sync.call_args.kwargs["body"].transfer_state == "unpause"

        module.change_transfer_state.sync_detailed = original

    def test_set_state_validation_error_on_400(self, transfers_resource: TransfersResource) -> None:
        """Test that set_state() raises ValidationError on 400."""
        import supermetrics.resources.transfers as module

        original = module.change_transfer_state.sync_detailed
        module.change_transfer_state.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Already paused")
        )

        with pytest.raises(ValidationError) as exc_info:
            transfers_resource.set_state(team_id=12345, transfer_id=36091, state="pause")

        assert exc_info.value.status_code == 400
        assert "Cannot change transfer state" in str(exc_info.value)

        module.change_transfer_state.sync_detailed = original

    # --- validate() ---

    def test_validate_success(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful validation of a valid configuration."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.sync_detailed
        module.validate_transfer.sync_detailed = MagicMock(
            return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[]))
        )

        result = transfers_resource.validate(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is True
        assert result.errors == []

        module.validate_transfer.sync_detailed = original

    def test_validate_returns_errors_when_invalid(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that validate() returns the field errors instead of raising when invalid."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.sync_detailed
        module.validate_transfer.sync_detailed = MagicMock(
            return_value=_make_success_response(
                ValidationErrorsResponse(
                    is_valid=False,
                    errors=[FieldValidationError(field_id="display_name", error_code="isEmpty")],
                )
            )
        )

        result = transfers_resource.validate(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is False
        assert result.errors[0].field_id == "display_name"
        assert result.errors[0].error_code == "isEmpty"

        module.validate_transfer.sync_detailed = original

    def test_validate_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that validate() passes the same body create() would send."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[])))
        module.validate_transfer.sync_detailed = mock_sync

        transfers_resource.validate(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert "transfer_id" not in call_kwargs
        body = call_kwargs["body"]
        assert body.data_source_id == "AW"
        assert body.display_name == "AW enhanced"
        assert body.segments is UNSET

        module.validate_transfer.sync_detailed = original

    def test_validate_api_error_on_500(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that validate() raises APIError on 500."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.sync_detailed
        module.validate_transfer.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.validate(
                team_id=12345,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="AW enhanced",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 500

        module.validate_transfer.sync_detailed = original

    # --- validate_update() ---

    def test_validate_update_success(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful validation of a change to an existing transfer."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.sync_detailed
        module.validate_transfer_update.sync_detailed = MagicMock(
            return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[]))
        )

        result = transfers_resource.validate_update(
            team_id=12345,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced (hourly)",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is True

        module.validate_transfer_update.sync_detailed = original

    def test_validate_update_returns_errors_when_invalid(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that validate_update() returns the field errors instead of raising when invalid."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.sync_detailed
        module.validate_transfer_update.sync_detailed = MagicMock(
            return_value=_make_success_response(
                ValidationErrorsResponse(
                    is_valid=False,
                    errors=[FieldValidationError(field_id="schema_id", error_code="notFound")],
                )
            )
        )

        result = transfers_resource.validate_update(
            team_id=12345,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=999,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is False
        assert result.errors[0].field_id == "schema_id"

        module.validate_transfer_update.sync_detailed = original

    def test_validate_update_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that validate_update() passes the transfer id alongside the body."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[])))
        module.validate_transfer_update.sync_detailed = mock_sync

        transfers_resource.validate_update(
            team_id=12345,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["body"].data_source_id == "AW"

        module.validate_transfer_update.sync_detailed = original

    def test_validate_update_api_error_on_404(
        self,
        transfers_resource: TransfersResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that validate_update() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.sync_detailed
        module.validate_transfer_update.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.validate_update(
                team_id=12345,
                transfer_id=999,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="AW enhanced",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 404

        module.validate_transfer_update.sync_detailed = original

    # --- list_available_sources() ---

    def test_list_available_sources_success(
        self,
        transfers_resource: TransfersResource,
        sample_available_sources: AvailableSourcesResponse,
    ) -> None:
        """Test successful available-sources retrieval from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.get_available_sources.sync_detailed
        module.get_available_sources.sync_detailed = MagicMock(
            return_value=_make_success_response(sample_available_sources)
        )

        available = transfers_resource.list_available_sources(team_id=12345)

        assert available.data_sources[0].data_source_id == "AW"
        assert available.destinations[0].destination_id == 8

        module.get_available_sources.sync_detailed = original

    def test_list_available_sources_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_available_sources: AvailableSourcesResponse,
    ) -> None:
        """Test that list_available_sources() passes the team id to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.get_available_sources.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_available_sources))
        module.get_available_sources.sync_detailed = mock_sync

        transfers_resource.list_available_sources(team_id=12345)

        assert mock_sync.call_args.kwargs["team_id"] == 12345

        module.get_available_sources.sync_detailed = original

    def test_list_available_sources_auth_error_on_401(self, transfers_resource: TransfersResource) -> None:
        """Test that list_available_sources() raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.get_available_sources.sync_detailed
        module.get_available_sources.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            transfers_resource.list_available_sources(team_id=12345)

        assert exc_info.value.status_code == 401

        module.get_available_sources.sync_detailed = original

    # --- get_available_options() ---

    def test_get_available_options_success(
        self,
        transfers_resource: TransfersResource,
        sample_options: TransferOptionsResponse,
    ) -> None:
        """Test successful transfer-options retrieval from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer_options.sync_detailed
        module.get_transfer_options.sync_detailed = MagicMock(return_value=_make_success_response(sample_options))

        options = transfers_resource.get_available_options(team_id=12345, source_id="AW", destination_id=8)

        assert options.schemas == []
        assert options.accounts == []

        module.get_transfer_options.sync_detailed = original

    def test_get_available_options_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_options: TransferOptionsResponse,
    ) -> None:
        """Test that get_available_options() passes source_id and destination_id as query params."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer_options.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_options))
        module.get_transfer_options.sync_detailed = mock_sync

        transfers_resource.get_available_options(team_id=12345, source_id="AW", destination_id=8)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["source_id"] == "AW"
        assert call_kwargs["destination_id"] == 8

        module.get_transfer_options.sync_detailed = original

    def test_get_available_options_api_error_on_404(self, transfers_resource: TransfersResource) -> None:
        """Test that get_available_options() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer_options.sync_detailed
        module.get_transfer_options.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "No options")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.get_available_options(team_id=12345, source_id="ZZ", destination_id=8)

        assert exc_info.value.status_code == 404
        assert "No options found" in str(exc_info.value)

        module.get_transfer_options.sync_detailed = original

    # --- list_runs() ---

    def test_list_runs_success(
        self,
        transfers_resource: TransfersResource,
        sample_run_item: TransferRunItem,
        meta: Meta,
    ) -> None:
        """Test successful transfer run listing."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.sync_detailed
        module.list_transfer_runs.sync_detailed = MagicMock(
            return_value=_make_success_response(TransferRunListResponse(meta=meta, data=[sample_run_item]))
        )

        runs = transfers_resource.list_runs(
            team_id=12345,
            transfer_id=36091,
            start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
            end_date=datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC),
        )

        assert len(runs) == 1
        assert runs[0].id == 98765
        assert runs[0].status == "SUCCESS"
        assert runs[0].type_ == "Recurring"

        module.list_transfer_runs.sync_detailed = original

    def test_list_runs_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_run_item: TransferRunItem,
        meta: Meta,
    ) -> None:
        """Test that list_runs() passes the date range and every optional query param."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(TransferRunListResponse(meta=meta, data=[sample_run_item]))
        )
        module.list_transfer_runs.sync_detailed = mock_sync

        start_date = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
        end_date = datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC)
        transfers_resource.list_runs(
            team_id=12345,
            transfer_id=36091,
            start_date=start_date,
            end_date=end_date,
            filter_issues_only=True,
            sort_field="data_date",
            sort_direction="DESC",
            limit=50,
            offset=10,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["start_date"] == start_date
        assert call_kwargs["end_date"] == end_date
        assert call_kwargs["filter_issues_only"] is True
        assert call_kwargs["sort_field"] == "data_date"
        assert call_kwargs["sort_direction"] == "DESC"
        assert call_kwargs["limit"] == 50
        assert call_kwargs["offset"] == 10

        module.list_transfer_runs.sync_detailed = original

    def test_list_runs_omits_optional_query_params(
        self,
        transfers_resource: TransfersResource,
        sample_run_item: TransferRunItem,
        meta: Meta,
    ) -> None:
        """Test that list_runs() converts omitted optional query params to UNSET."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(TransferRunListResponse(meta=meta, data=[sample_run_item]))
        )
        module.list_transfer_runs.sync_detailed = mock_sync

        transfers_resource.list_runs(
            team_id=12345,
            transfer_id=36091,
            start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
            end_date=datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC),
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["filter_issues_only"] is UNSET
        assert call_kwargs["sort_field"] is UNSET
        assert call_kwargs["sort_direction"] is UNSET
        assert call_kwargs["limit"] is UNSET
        assert call_kwargs["offset"] is UNSET

        module.list_transfer_runs.sync_detailed = original

    def test_list_runs_api_error_on_404(self, transfers_resource: TransfersResource) -> None:
        """Test that list_runs() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.sync_detailed
        module.list_transfer_runs.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            transfers_resource.list_runs(
                team_id=12345,
                transfer_id=999,
                start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
                end_date=datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC),
            )

        assert exc_info.value.status_code == 404

        module.list_transfer_runs.sync_detailed = original

    # --- create_datasource_connection() ---

    def test_create_datasource_connection_success(
        self,
        transfers_resource: TransfersResource,
        sample_connection: DataSourceConnection,
        meta: Meta,
    ) -> None:
        """Test successful connection creation, which the API answers with HTTP 201."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.sync_detailed
        module.create_data_source_connection.sync_detailed = MagicMock(
            return_value=_make_created_response(CreateDataSourceConnectionResponse(meta=meta, data=sample_connection))
        )

        connection = transfers_resource.create_datasource_connection(
            team_id=12345,
            data_source_id="ADM",
            destination_type="DWH_SNOWFLAKE",
        )

        assert connection.connection_id == CONNECTION_ID
        assert connection.login_url == "https://example.test/login"

        module.create_data_source_connection.sync_detailed = original

    def test_create_datasource_connection_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        sample_connection: DataSourceConnection,
        meta: Meta,
    ) -> None:
        """Test that create_datasource_connection() passes the correct body."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(CreateDataSourceConnectionResponse(meta=meta, data=sample_connection))
        )
        module.create_data_source_connection.sync_detailed = mock_sync

        transfers_resource.create_datasource_connection(
            team_id=12345,
            data_source_id="ADM",
            destination_type="DWH_SNOWFLAKE",
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        body = call_kwargs["body"]
        assert body.data_source_id == "ADM"
        assert body.destination_type == "DWH_SNOWFLAKE"

        module.create_data_source_connection.sync_detailed = original

    def test_create_datasource_connection_never_sends_api_key(
        self,
        transfers_resource: TransfersResource,
        sample_connection: DataSourceConnection,
        meta: Meta,
    ) -> None:
        """Test that create_datasource_connection() never puts an api_key in the body."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(CreateDataSourceConnectionResponse(meta=meta, data=sample_connection))
        )
        module.create_data_source_connection.sync_detailed = mock_sync

        transfers_resource.create_datasource_connection(
            team_id=12345,
            data_source_id="ADM",
            destination_type="DWH_SNOWFLAKE",
        )

        body = mock_sync.call_args.kwargs["body"]
        assert body.api_key is UNSET
        assert "api_key" not in body.to_dict()

        module.create_data_source_connection.sync_detailed = original

    def test_create_datasource_connection_validation_error_on_400(self, transfers_resource: TransfersResource) -> None:
        """Test that create_datasource_connection() raises ValidationError on 400."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.sync_detailed
        module.create_data_source_connection.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Unknown destination type")
        )

        with pytest.raises(ValidationError) as exc_info:
            transfers_resource.create_datasource_connection(
                team_id=12345,
                data_source_id="ADM",
                destination_type="NOPE",
            )

        assert exc_info.value.status_code == 400
        assert "Invalid connection configuration" in str(exc_info.value)

        module.create_data_source_connection.sync_detailed = original

    def test_clone_success_201(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Test successful transfer clone, which the API answers with HTTP 201."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.sync_detailed
        module.clone_transfer.sync_detailed = MagicMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )

        cloned = transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert cloned.transfer_id == 36091
        assert cloned.transfer_name == "AW enhanced"

        module.clone_transfer.sync_detailed = original

    def test_clone_success_200(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Some transfers return 200 instead of 201 on clone — both must work."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.sync_detailed
        module.clone_transfer.sync_detailed = MagicMock(
            return_value=_make_success_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )

        cloned = transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert cloned.transfer_id == 36091
        assert cloned.transfer_name == "AW enhanced"

        module.clone_transfer.sync_detailed = original

    def test_clone_200_parsed_none_fallback(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """When clone returns 200 with parsed=None, the wrapper falls back to manual JSON parsing."""
        import json

        import supermetrics.resources.transfers as module

        envelope = TransferCreatedEnvelope(meta=meta, data=sample_created)
        original = module.clone_transfer.sync_detailed
        module.clone_transfer.sync_detailed = MagicMock(
            return_value=Response(
                status_code=HTTPStatus.OK,
                content=json.dumps(envelope.to_dict()).encode(),
                headers={},
                parsed=None,
            )
        )

        cloned = transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert cloned.transfer_id == 36091
        assert cloned.transfer_name == "AW enhanced"

        module.clone_transfer.sync_detailed = original

    def test_clone_passes_overrides(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Test that clone() passes the overrides body to the generated client."""
        import supermetrics.resources.transfers as module
        from supermetrics._generated.supermetrics_api_client.models.clone_transfer_body import CloneTransferBody

        original = module.clone_transfer.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.clone_transfer.sync_detailed = mock_sync

        overrides = CloneTransferBody(display_name="My Clone")
        transfers_resource.clone(team_id=12345, transfer_id=36091, overrides=overrides)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["body"].display_name == "My Clone"

        module.clone_transfer.sync_detailed = original

    def test_clone_without_overrides_sends_unset(
        self,
        transfers_resource: TransfersResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Test that clone() without overrides sends UNSET as body."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.clone_transfer.sync_detailed = mock_sync

        transfers_resource.clone(team_id=12345, transfer_id=36091)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["body"] is UNSET

        module.clone_transfer.sync_detailed = original

    def test_clone_auth_error_on_401(self, transfers_resource: TransfersResource) -> None:
        """Test that clone() raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.sync_detailed
        module.clone_transfer.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert exc_info.value.status_code == 401

        module.clone_transfer.sync_detailed = original

    def test_batch_create_success(
        self,
        transfers_resource: TransfersResource,
        meta: Meta,
    ) -> None:
        """Test successful batch create, which the API answers with HTTP 200."""
        import supermetrics.resources.transfers as module
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200 import (
            BatchCreateTransfersResponse200,
        )
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200_data import (
            BatchCreateTransfersResponse200Data,
        )

        data = BatchCreateTransfersResponse200Data(has_errors=False, results=[])
        original = module.batch_create_transfers.sync_detailed
        module.batch_create_transfers.sync_detailed = MagicMock(
            return_value=_make_success_response(BatchCreateTransfersResponse200(meta=meta, data=data))
        )

        result = transfers_resource.batch_create(team_id=12345, transfers=[])

        assert result.has_errors is False
        assert result.results == []

        module.batch_create_transfers.sync_detailed = original

    def test_batch_create_passes_correct_params(
        self,
        transfers_resource: TransfersResource,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that batch_create() forwards the transfers array to the generated client."""
        import supermetrics.resources.transfers as module
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200 import (
            BatchCreateTransfersResponse200,
        )
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200_data import (
            BatchCreateTransfersResponse200Data,
        )
        from supermetrics._generated.supermetrics_api_client.models.transfer_configuration_request import (
            TransferConfigurationRequest,
        )

        data = BatchCreateTransfersResponse200Data(has_errors=False, results=[])
        original = module.batch_create_transfers.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(BatchCreateTransfersResponse200(meta=meta, data=data))
        )
        module.batch_create_transfers.sync_detailed = mock_sync

        config = TransferConfigurationRequest(
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="Batch item",
            schedule=schedule,
            accounts=accounts,
        )
        transfers_resource.batch_create(team_id=12345, transfers=[config])

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        body = call_kwargs["body"]
        assert len(body.transfers) == 1
        assert body.transfers[0].data_source_id == "AW"
        assert body.transfers[0].display_name == "Batch item"

        module.batch_create_transfers.sync_detailed = original

    def test_batch_create_auth_error_on_401(self, transfers_resource: TransfersResource) -> None:
        """Test that batch_create() raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.batch_create_transfers.sync_detailed
        module.batch_create_transfers.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            transfers_resource.batch_create(team_id=12345, transfers=[])

        assert exc_info.value.status_code == 401

        module.batch_create_transfers.sync_detailed = original


class TestTransfersAsyncResource:
    """Test suite for TransfersAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def transfers_resource(self, mock_client: MagicMock) -> TransfersAsyncResource:
        """Create a TransfersAsyncResource instance with mock client."""
        return TransfersAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def schedule(self) -> list[TransferSchedule]:
        """Create a sample transfer schedule."""
        return [TransferSchedule(run_interval="hourly", refresh_window=1)]

    @pytest.fixture
    def accounts(self) -> list[TransferAccount]:
        """Create a sample list of transfer accounts."""
        return [TransferAccount(login_id=2682599, account_id="8733197711")]

    @pytest.fixture
    def sample_transfer_info(self) -> TransferInfoResponse:
        """Create a sample transfer summary for testing."""
        return TransferInfoResponse(
            dwh_transfer_id=36091,
            display_name="AW enhanced",
            status="OK",
            state="PAUSED",
            schedule="Hourly",
        )

    @pytest.fixture
    def sample_configuration(self, schedule: list[TransferSchedule]) -> TransferConfigurationResponse:
        """Create a sample transfer configuration for testing."""
        return TransferConfigurationResponse(
            transfer_id=36091,
            display_name="AW enhanced",
            schema_id=2,
            destination_id=8,
            schedule=schedule,
        )

    @pytest.fixture
    def sample_created(self) -> TransferCreatedResponse:
        """Create a sample transfer-created payload for testing."""
        return TransferCreatedResponse(transfer_id=36091, transfer_name="AW enhanced")

    @pytest.fixture
    def sample_updated(self) -> TransferUpdatedResponse:
        """Create a sample transfer-updated payload for testing."""
        return TransferUpdatedResponse(transfer_id=36091, transfer_name="AW enhanced (hourly)")

    @pytest.fixture
    def sample_state(self) -> TransferStateUpdateResponse:
        """Create a sample state-change payload for testing."""
        return TransferStateUpdateResponse(result=True, state="PAUSED")

    @pytest.fixture
    def sample_available_sources(self) -> AvailableSourcesResponse:
        """Create a sample available-sources payload for testing."""
        return AvailableSourcesResponse(
            data_sources=[DataSourceInfo(data_source_id="AW", service_name="Google Ads")],
            destinations=[TransferDestination(destination_id=8, destination_name="BigQuery")],
        )

    @pytest.fixture
    def sample_options(self) -> TransferOptionsResponse:
        """Create a sample transfer-options payload for testing."""
        return TransferOptionsResponse(schemas=[], logins=[], accounts=[])

    @pytest.fixture
    def sample_run_item(self) -> TransferRunItem:
        """Create a sample transfer run summary for testing."""
        return TransferRunItem(
            id=98765,
            status="FAILED",
            type_="Backfill",
            message="Query failed",
            data_date=datetime.date(2024, 1, 15),
        )

    @pytest.fixture
    def sample_connection(self) -> DataSourceConnection:
        """Create a sample data source connection for testing."""
        return DataSourceConnection(connection_id=CONNECTION_ID, login_url="https://example.test/login")

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_transfer_info: TransferInfoResponse,
        meta: Meta,
    ) -> None:
        """Test successful async transfer listing."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.asyncio_detailed
        module.list_transfers.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(TransferListResponse(meta=meta, data=[sample_transfer_info]))
        )

        transfers = await transfers_resource.list(team_id=99999)

        assert len(transfers) == 1
        assert transfers[0].dwh_transfer_id == 36091
        assert transfers[0].state == "PAUSED"

        module.list_transfers.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_transfer_info: TransferInfoResponse,
        meta: Meta,
    ) -> None:
        """Test that async list() passes correct parameters."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(TransferListResponse(meta=meta, data=[sample_transfer_info]))
        )
        module.list_transfers.asyncio_detailed = mock_asyncio

        await transfers_resource.list(team_id=99999)

        assert mock_asyncio.call_args.kwargs["team_id"] == 99999

        module.list_transfers.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_auth_error_on_401(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async list() raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.asyncio_detailed
        module.list_transfers.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await transfers_resource.list(team_id=99999)

        assert exc_info.value.status_code == 401

        module.list_transfers.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_api_error_on_500(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async list() raises APIError on 500."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.asyncio_detailed
        module.list_transfers.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.list(team_id=99999)

        assert exc_info.value.status_code == 500

        module.list_transfers.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_network_error(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async list() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.transfers as module

        original = module.list_transfers.asyncio_detailed
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/teams/99999/transfers"
        module.list_transfers.asyncio_detailed = AsyncMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        with pytest.raises(NetworkError):
            await transfers_resource.list(team_id=99999)

        module.list_transfers.asyncio_detailed = original

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_configuration: TransferConfigurationResponse,
    ) -> None:
        """Test successful async transfer configuration retrieval from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer.asyncio_detailed
        module.get_transfer.asyncio_detailed = AsyncMock(return_value=_make_success_response(sample_configuration))

        configuration = await transfers_resource.get(team_id=99999, transfer_id=36091)

        assert configuration.transfer_id == 36091
        assert configuration.destination_id == 8

        module.get_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_configuration: TransferConfigurationResponse,
    ) -> None:
        """Test that async get() passes correct parameters."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_success_response(sample_configuration))
        module.get_transfer.asyncio_detailed = mock_asyncio

        await transfers_resource.get(team_id=99999, transfer_id=36091)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_id"] == 36091

        module.get_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_404(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async get() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer.asyncio_detailed
        module.get_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.get(team_id=99999, transfer_id=999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        module.get_transfer.asyncio_detailed = original

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful async transfer creation, which the API answers with HTTP 201."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.asyncio_detailed
        module.create_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )

        created = await transfers_resource.create(
            team_id=99999,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        assert created.transfer_id == 36091

        module.create_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async create() passes the correct body to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.create_transfer.asyncio_detailed = mock_asyncio

        segments = [TransferSegment(login_id=2682599, segment_id="seg-1")]
        await transfers_resource.create(
            team_id=99999,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
            segments=segments,
            transfer_type=1,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        body = call_kwargs["body"]
        assert body.data_source_id == "AW"
        assert body.segments == segments
        assert body.transfer_type == 1

        module.create_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_omits_optional_fields(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async create() leaves omitted optional fields UNSET rather than null."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.create_transfer.asyncio_detailed = mock_asyncio

        await transfers_resource.create(
            team_id=99999,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        body = mock_asyncio.call_args.kwargs["body"]
        assert body.segments is UNSET
        assert body.data_source_settings is UNSET
        assert body.notification_recipients is UNSET
        assert body.transfer_type is UNSET

        module.create_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_validation_error_on_400(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async create() raises ValidationError on 400."""
        import supermetrics.resources.transfers as module

        original = module.create_transfer.asyncio_detailed
        module.create_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Invalid configuration")
        )

        with pytest.raises(ValidationError) as exc_info:
            await transfers_resource.create(
                team_id=99999,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 400
        assert "Invalid transfer configuration" in str(exc_info.value)

        module.create_transfer.asyncio_detailed = original

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_updated: TransferUpdatedResponse,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful async transfer update from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.update_transfer.asyncio_detailed
        module.update_transfer.asyncio_detailed = AsyncMock(return_value=_make_success_response(sample_updated))

        updated = await transfers_resource.update(
            team_id=99999,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced (hourly)",
            schedule=schedule,
            accounts=accounts,
        )

        assert updated.transfer_name == "AW enhanced (hourly)"

        module.update_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_updated: TransferUpdatedResponse,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async update() passes the transfer id and body to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.update_transfer.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_success_response(sample_updated))
        module.update_transfer.asyncio_detailed = mock_asyncio

        await transfers_resource.update(
            team_id=99999,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced (hourly)",
            schedule=schedule,
            accounts=accounts,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["body"].schedule == schedule

        module.update_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_api_error_on_404(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async update() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.update_transfer.asyncio_detailed
        module.update_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.update(
                team_id=99999,
                transfer_id=999,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="AW enhanced",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 404

        module.update_transfer.asyncio_detailed = original

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_success(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async delete() returns None on the API's 204 No Content."""
        import supermetrics.resources.transfers as module

        original = module.delete_transfer.asyncio_detailed
        module.delete_transfer.asyncio_detailed = AsyncMock(return_value=_make_no_content_response())

        result = await transfers_resource.delete(team_id=99999, transfer_id=36091)

        assert result is None

        module.delete_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_delete_passes_correct_params(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async delete() passes correct parameters."""
        import supermetrics.resources.transfers as module

        original = module.delete_transfer.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_no_content_response())
        module.delete_transfer.asyncio_detailed = mock_asyncio

        await transfers_resource.delete(team_id=99999, transfer_id=36091)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_id"] == 36091

        module.delete_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_delete_api_error_on_404(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async delete() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.delete_transfer.asyncio_detailed
        module.delete_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.delete(team_id=99999, transfer_id=999)

        assert exc_info.value.status_code == 404

        module.delete_transfer.asyncio_detailed = original

    # --- set_state() ---

    @pytest.mark.asyncio
    async def test_set_state_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_state: TransferStateUpdateResponse,
    ) -> None:
        """Test successful async pause, whose response reports the state in upper case."""
        import supermetrics.resources.transfers as module

        original = module.change_transfer_state.asyncio_detailed
        module.change_transfer_state.asyncio_detailed = AsyncMock(return_value=_make_success_response(sample_state))

        paused = await transfers_resource.set_state(team_id=99999, transfer_id=36091, state="pause")

        assert paused.result is True
        assert paused.state == "PAUSED"

        module.change_transfer_state.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_set_state_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_state: TransferStateUpdateResponse,
    ) -> None:
        """Test that async set_state() sends the lower-case verb in the request body."""
        import supermetrics.resources.transfers as module

        original = module.change_transfer_state.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_success_response(sample_state))
        module.change_transfer_state.asyncio_detailed = mock_asyncio

        await transfers_resource.set_state(team_id=99999, transfer_id=36091, state="unpause")

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["body"].transfer_state == "unpause"
        assert call_kwargs["body"].to_dict() == {"transfer_state": "unpause"}

        module.change_transfer_state.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_set_state_validation_error_on_400(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async set_state() raises ValidationError on 400."""
        import supermetrics.resources.transfers as module

        original = module.change_transfer_state.asyncio_detailed
        module.change_transfer_state.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Already paused")
        )

        with pytest.raises(ValidationError) as exc_info:
            await transfers_resource.set_state(team_id=99999, transfer_id=36091, state="pause")

        assert exc_info.value.status_code == 400
        assert "Cannot change transfer state" in str(exc_info.value)

        module.change_transfer_state.asyncio_detailed = original

    # --- validate() ---

    @pytest.mark.asyncio
    async def test_validate_success(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful async validation of a valid configuration."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.asyncio_detailed
        module.validate_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[]))
        )

        result = await transfers_resource.validate(
            team_id=99999,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is True

        module.validate_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_validate_returns_errors_when_invalid(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async validate() returns the field errors instead of raising when invalid."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.asyncio_detailed
        module.validate_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(
                ValidationErrorsResponse(
                    is_valid=False,
                    errors=[FieldValidationError(field_id="display_name", error_code="isEmpty")],
                )
            )
        )

        result = await transfers_resource.validate(
            team_id=99999,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is False
        assert result.errors[0].error_code == "isEmpty"

        module.validate_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_validate_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async validate() passes the same body create() would send."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[]))
        )
        module.validate_transfer.asyncio_detailed = mock_asyncio

        await transfers_resource.validate(
            team_id=99999,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert "transfer_id" not in call_kwargs
        assert call_kwargs["body"].display_name == "AW enhanced"

        module.validate_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_validate_api_error_on_500(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async validate() raises APIError on 500."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer.asyncio_detailed
        module.validate_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.validate(
                team_id=99999,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="AW enhanced",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 500

        module.validate_transfer.asyncio_detailed = original

    # --- validate_update() ---

    @pytest.mark.asyncio
    async def test_validate_update_success(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test successful async validation of a change to an existing transfer."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.asyncio_detailed
        module.validate_transfer_update.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[]))
        )

        result = await transfers_resource.validate_update(
            team_id=99999,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced (hourly)",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is True

        module.validate_transfer_update.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_validate_update_returns_errors_when_invalid(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async validate_update() returns the field errors instead of raising when invalid."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.asyncio_detailed
        module.validate_transfer_update.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(
                ValidationErrorsResponse(
                    is_valid=False,
                    errors=[FieldValidationError(field_id="schema_id", error_code="notFound")],
                )
            )
        )

        result = await transfers_resource.validate_update(
            team_id=99999,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=999,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        assert result.is_valid is False
        assert result.errors[0].field_id == "schema_id"

        module.validate_transfer_update.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_validate_update_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async validate_update() passes the transfer id alongside the body."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(ValidationErrorsResponse(is_valid=True, errors=[]))
        )
        module.validate_transfer_update.asyncio_detailed = mock_asyncio

        await transfers_resource.validate_update(
            team_id=99999,
            transfer_id=36091,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=schedule,
            accounts=accounts,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_id"] == 36091

        module.validate_transfer_update.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_validate_update_api_error_on_404(
        self,
        transfers_resource: TransfersAsyncResource,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async validate_update() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.validate_transfer_update.asyncio_detailed
        module.validate_transfer_update.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.validate_update(
                team_id=99999,
                transfer_id=999,
                data_source_id="AW",
                schema_id=2,
                destination_id=8,
                display_name="AW enhanced",
                schedule=schedule,
                accounts=accounts,
            )

        assert exc_info.value.status_code == 404

        module.validate_transfer_update.asyncio_detailed = original

    # --- list_available_sources() ---

    @pytest.mark.asyncio
    async def test_list_available_sources_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_available_sources: AvailableSourcesResponse,
    ) -> None:
        """Test successful async available-sources retrieval from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.get_available_sources.asyncio_detailed
        module.get_available_sources.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(sample_available_sources)
        )

        available = await transfers_resource.list_available_sources(team_id=99999)

        assert available.data_sources[0].service_name == "Google Ads"

        module.get_available_sources.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_available_sources_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_available_sources: AvailableSourcesResponse,
    ) -> None:
        """Test that async list_available_sources() passes the team id to the generated client."""
        import supermetrics.resources.transfers as module

        original = module.get_available_sources.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_success_response(sample_available_sources))
        module.get_available_sources.asyncio_detailed = mock_asyncio

        await transfers_resource.list_available_sources(team_id=99999)

        assert mock_asyncio.call_args.kwargs["team_id"] == 99999

        module.get_available_sources.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_available_sources_auth_error_on_401(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async list_available_sources() raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.get_available_sources.asyncio_detailed
        module.get_available_sources.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await transfers_resource.list_available_sources(team_id=99999)

        assert exc_info.value.status_code == 401

        module.get_available_sources.asyncio_detailed = original

    # --- get_available_options() ---

    @pytest.mark.asyncio
    async def test_get_available_options_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_options: TransferOptionsResponse,
    ) -> None:
        """Test successful async transfer-options retrieval from a bare payload."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer_options.asyncio_detailed
        module.get_transfer_options.asyncio_detailed = AsyncMock(return_value=_make_success_response(sample_options))

        options = await transfers_resource.get_available_options(team_id=99999, source_id="AW", destination_id=8)

        assert options.logins == []

        module.get_transfer_options.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_available_options_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_options: TransferOptionsResponse,
    ) -> None:
        """Test that async get_available_options() passes source_id and destination_id as query params."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer_options.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_success_response(sample_options))
        module.get_transfer_options.asyncio_detailed = mock_asyncio

        await transfers_resource.get_available_options(team_id=99999, source_id="AW", destination_id=8)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["source_id"] == "AW"
        assert call_kwargs["destination_id"] == 8

        module.get_transfer_options.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_available_options_api_error_on_404(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async get_available_options() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.get_transfer_options.asyncio_detailed
        module.get_transfer_options.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "No options")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.get_available_options(team_id=99999, source_id="ZZ", destination_id=8)

        assert exc_info.value.status_code == 404

        module.get_transfer_options.asyncio_detailed = original

    # --- list_runs() ---

    @pytest.mark.asyncio
    async def test_list_runs_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_run_item: TransferRunItem,
        meta: Meta,
    ) -> None:
        """Test successful async transfer run listing."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.asyncio_detailed
        module.list_transfer_runs.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(TransferRunListResponse(meta=meta, data=[sample_run_item]))
        )

        runs = await transfers_resource.list_runs(
            team_id=99999,
            transfer_id=36091,
            start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
            end_date=datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC),
        )

        assert len(runs) == 1
        assert runs[0].status == "FAILED"
        assert runs[0].type_ == "Backfill"

        module.list_transfer_runs.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_runs_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_run_item: TransferRunItem,
        meta: Meta,
    ) -> None:
        """Test that async list_runs() passes the date range and every optional query param."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(TransferRunListResponse(meta=meta, data=[sample_run_item]))
        )
        module.list_transfer_runs.asyncio_detailed = mock_asyncio

        start_date = datetime.datetime(2024, 2, 1, tzinfo=datetime.UTC)
        end_date = datetime.datetime(2024, 2, 29, tzinfo=datetime.UTC)
        await transfers_resource.list_runs(
            team_id=99999,
            transfer_id=36091,
            start_date=start_date,
            end_date=end_date,
            filter_issues_only=False,
            sort_field="created_time",
            sort_direction="ASC",
            limit=25,
            offset=0,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["start_date"] == start_date
        assert call_kwargs["end_date"] == end_date
        assert call_kwargs["filter_issues_only"] is False
        assert call_kwargs["sort_field"] == "created_time"
        assert call_kwargs["sort_direction"] == "ASC"
        assert call_kwargs["limit"] == 25
        assert call_kwargs["offset"] == 0

        module.list_transfer_runs.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_runs_omits_optional_query_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_run_item: TransferRunItem,
        meta: Meta,
    ) -> None:
        """Test that async list_runs() converts omitted optional query params to UNSET."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(TransferRunListResponse(meta=meta, data=[sample_run_item]))
        )
        module.list_transfer_runs.asyncio_detailed = mock_asyncio

        await transfers_resource.list_runs(
            team_id=99999,
            transfer_id=36091,
            start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
            end_date=datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC),
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["filter_issues_only"] is UNSET
        assert call_kwargs["sort_field"] is UNSET
        assert call_kwargs["sort_direction"] is UNSET
        assert call_kwargs["limit"] is UNSET
        assert call_kwargs["offset"] is UNSET

        module.list_transfer_runs.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_runs_api_error_on_404(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test that async list_runs() raises APIError on 404."""
        import supermetrics.resources.transfers as module

        original = module.list_transfer_runs.asyncio_detailed
        module.list_transfer_runs.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer not found")
        )

        with pytest.raises(APIError) as exc_info:
            await transfers_resource.list_runs(
                team_id=99999,
                transfer_id=999,
                start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
                end_date=datetime.datetime(2024, 1, 31, tzinfo=datetime.UTC),
            )

        assert exc_info.value.status_code == 404

        module.list_transfer_runs.asyncio_detailed = original

    # --- create_datasource_connection() ---

    @pytest.mark.asyncio
    async def test_create_datasource_connection_success(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_connection: DataSourceConnection,
        meta: Meta,
    ) -> None:
        """Test successful async connection creation, which the API answers with HTTP 201."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.asyncio_detailed
        module.create_data_source_connection.asyncio_detailed = AsyncMock(
            return_value=_make_created_response(CreateDataSourceConnectionResponse(meta=meta, data=sample_connection))
        )

        connection = await transfers_resource.create_datasource_connection(
            team_id=99999,
            data_source_id="ADM",
            destination_type="DWH_SNOWFLAKE",
        )

        assert connection.connection_id == CONNECTION_ID

        module.create_data_source_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_datasource_connection_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_connection: DataSourceConnection,
        meta: Meta,
    ) -> None:
        """Test that async create_datasource_connection() passes the correct body."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(CreateDataSourceConnectionResponse(meta=meta, data=sample_connection))
        )
        module.create_data_source_connection.asyncio_detailed = mock_asyncio

        await transfers_resource.create_datasource_connection(
            team_id=99999,
            data_source_id="GA",
            destination_type="SQL_BQ",
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        body = call_kwargs["body"]
        assert body.data_source_id == "GA"
        assert body.destination_type == "SQL_BQ"

        module.create_data_source_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_datasource_connection_never_sends_api_key(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_connection: DataSourceConnection,
        meta: Meta,
    ) -> None:
        """Test that async create_datasource_connection() never puts an api_key in the body."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(CreateDataSourceConnectionResponse(meta=meta, data=sample_connection))
        )
        module.create_data_source_connection.asyncio_detailed = mock_asyncio

        await transfers_resource.create_datasource_connection(
            team_id=99999,
            data_source_id="GA",
            destination_type="SQL_BQ",
        )

        body = mock_asyncio.call_args.kwargs["body"]
        assert body.api_key is UNSET
        assert "api_key" not in body.to_dict()

        module.create_data_source_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_datasource_connection_validation_error_on_400(
        self,
        transfers_resource: TransfersAsyncResource,
    ) -> None:
        """Test that async create_datasource_connection() raises ValidationError on 400."""
        import supermetrics.resources.transfers as module

        original = module.create_data_source_connection.asyncio_detailed
        module.create_data_source_connection.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Unknown destination type")
        )

        with pytest.raises(ValidationError) as exc_info:
            await transfers_resource.create_datasource_connection(
                team_id=99999,
                data_source_id="GA",
                destination_type="NOPE",
            )

        assert exc_info.value.status_code == 400
        assert "Invalid connection configuration" in str(exc_info.value)

        module.create_data_source_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_clone_success_201(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Test async clone success with 201."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.asyncio_detailed
        module.clone_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )

        cloned = await transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert cloned.transfer_id == 36091
        assert cloned.transfer_name == "AW enhanced"

        module.clone_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_clone_success_200(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Some transfers return 200 instead of 201 — both must work."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.asyncio_detailed
        module.clone_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )

        cloned = await transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert cloned.transfer_id == 36091
        assert cloned.transfer_name == "AW enhanced"

        module.clone_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_clone_200_parsed_none_fallback(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """When async clone returns 200 with parsed=None, the wrapper falls back to manual JSON parsing."""
        import json

        import supermetrics.resources.transfers as module

        envelope = TransferCreatedEnvelope(meta=meta, data=sample_created)
        original = module.clone_transfer.asyncio_detailed
        module.clone_transfer.asyncio_detailed = AsyncMock(
            return_value=Response(
                status_code=HTTPStatus.OK,
                content=json.dumps(envelope.to_dict()).encode(),
                headers={},
                parsed=None,
            )
        )

        cloned = await transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert cloned.transfer_id == 36091
        assert cloned.transfer_name == "AW enhanced"

        module.clone_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_clone_passes_overrides(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Test that async clone() passes the overrides body to the generated client."""
        import supermetrics.resources.transfers as module
        from supermetrics._generated.supermetrics_api_client.models.clone_transfer_body import CloneTransferBody

        original = module.clone_transfer.asyncio_detailed
        mock_async = AsyncMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.clone_transfer.asyncio_detailed = mock_async

        overrides = CloneTransferBody(display_name="My Clone")
        await transfers_resource.clone(team_id=12345, transfer_id=36091, overrides=overrides)

        call_kwargs = mock_async.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_id"] == 36091
        assert call_kwargs["body"].display_name == "My Clone"

        module.clone_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_clone_without_overrides_sends_unset(
        self,
        transfers_resource: TransfersAsyncResource,
        sample_created: TransferCreatedResponse,
        meta: Meta,
    ) -> None:
        """Test that async clone() without overrides sends UNSET as body."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.asyncio_detailed
        mock_async = AsyncMock(
            return_value=_make_created_response(TransferCreatedEnvelope(meta=meta, data=sample_created))
        )
        module.clone_transfer.asyncio_detailed = mock_async

        await transfers_resource.clone(team_id=12345, transfer_id=36091)

        call_kwargs = mock_async.call_args.kwargs
        assert call_kwargs["body"] is UNSET

        module.clone_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_clone_auth_error_on_401(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test async clone raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.clone_transfer.asyncio_detailed
        module.clone_transfer.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await transfers_resource.clone(team_id=12345, transfer_id=36091)

        assert exc_info.value.status_code == 401

        module.clone_transfer.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_create_success(
        self,
        transfers_resource: TransfersAsyncResource,
        meta: Meta,
    ) -> None:
        """Test async batch create success."""
        import supermetrics.resources.transfers as module
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200 import (
            BatchCreateTransfersResponse200,
        )
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200_data import (
            BatchCreateTransfersResponse200Data,
        )

        data = BatchCreateTransfersResponse200Data(has_errors=False, results=[])
        original = module.batch_create_transfers.asyncio_detailed
        module.batch_create_transfers.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(BatchCreateTransfersResponse200(meta=meta, data=data))
        )

        result = await transfers_resource.batch_create(team_id=12345, transfers=[])

        assert result.has_errors is False

        module.batch_create_transfers.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_create_passes_correct_params(
        self,
        transfers_resource: TransfersAsyncResource,
        meta: Meta,
        schedule: list[TransferSchedule],
        accounts: list[TransferAccount],
    ) -> None:
        """Test that async batch_create() forwards the transfers array to the generated client."""
        import supermetrics.resources.transfers as module
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200 import (
            BatchCreateTransfersResponse200,
        )
        from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200_data import (
            BatchCreateTransfersResponse200Data,
        )
        from supermetrics._generated.supermetrics_api_client.models.transfer_configuration_request import (
            TransferConfigurationRequest,
        )

        data = BatchCreateTransfersResponse200Data(has_errors=False, results=[])
        original = module.batch_create_transfers.asyncio_detailed
        mock_async = AsyncMock(
            return_value=_make_success_response(BatchCreateTransfersResponse200(meta=meta, data=data))
        )
        module.batch_create_transfers.asyncio_detailed = mock_async

        config = TransferConfigurationRequest(
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="Batch item",
            schedule=schedule,
            accounts=accounts,
        )
        await transfers_resource.batch_create(team_id=12345, transfers=[config])

        call_kwargs = mock_async.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        body = call_kwargs["body"]
        assert len(body.transfers) == 1
        assert body.transfers[0].data_source_id == "AW"
        assert body.transfers[0].display_name == "Batch item"

        module.batch_create_transfers.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_create_auth_error_on_401(self, transfers_resource: TransfersAsyncResource) -> None:
        """Test async batch create raises AuthenticationError on 401."""
        import supermetrics.resources.transfers as module

        original = module.batch_create_transfers.asyncio_detailed
        module.batch_create_transfers.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await transfers_resource.batch_create(team_id=12345, transfers=[])

        assert exc_info.value.status_code == 401

        module.batch_create_transfers.asyncio_detailed = original
