"""Unit tests for TransferRunsResource and TransferRunsAsyncResource."""

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.query_details import QueryDetails
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.models.transfer_run_detail import TransferRunDetail
from supermetrics._generated.supermetrics_api_client.models.transfer_run_detail_response import (
    TransferRunDetailResponse,
)
from supermetrics._generated.supermetrics_api_client.types import Response
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError
from supermetrics.resources.transfer_runs import TransferRunsAsyncResource, TransferRunsResource


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


class TestTransferRunsResource:
    """Test suite for TransferRunsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def transfer_runs_resource(self, mock_client: MagicMock) -> TransferRunsResource:
        """Create a TransferRunsResource instance with mock client."""
        return TransferRunsResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_run(self) -> TransferRunDetail:
        """Create a sample transfer run detail for testing."""
        return TransferRunDetail(
            id=98765,
            status="SUCCESS",
            query_details=[QueryDetails(status="SUCCESS", rows=4200, duration=12.5)],
            external_id="run-abc-123",
            message="",
            started_time=datetime.datetime(2024, 1, 15, 22, 0, 0, tzinfo=datetime.UTC),
            ended_time=datetime.datetime(2024, 1, 15, 22, 3, 20, tzinfo=datetime.UTC),
            total_duration=200.0,
            total_rows=4200,
            data_date=datetime.date(2024, 1, 15),
        )

    # --- get() ---

    def test_get_success(
        self,
        transfer_runs_resource: TransferRunsResource,
        sample_run: TransferRunDetail,
        meta: Meta,
    ) -> None:
        """Test successful transfer run retrieval, unwrapped from the meta/data envelope."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.sync_detailed
        module.get_transfer_run.sync_detailed = MagicMock(
            return_value=_make_success_response(TransferRunDetailResponse(meta=meta, data=sample_run))
        )

        run = transfer_runs_resource.get(team_id=12345, transfer_run_id=98765)

        assert run.id == 98765
        assert run.status == "SUCCESS"
        assert run.external_id == "run-abc-123"
        assert run.total_rows == 4200
        assert run.query_details[0].rows == 4200

        module.get_transfer_run.sync_detailed = original

    def test_get_passes_correct_params(
        self,
        transfer_runs_resource: TransferRunsResource,
        sample_run: TransferRunDetail,
        meta: Meta,
    ) -> None:
        """Test that get() passes the correct parameters to the generated client."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(TransferRunDetailResponse(meta=meta, data=sample_run))
        )
        module.get_transfer_run.sync_detailed = mock_sync

        transfer_runs_resource.get(team_id=12345, transfer_run_id=98765)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["transfer_run_id"] == 98765

        module.get_transfer_run.sync_detailed = original

    def test_get_auth_error_on_401(self, transfer_runs_resource: TransferRunsResource) -> None:
        """Test that get() raises AuthenticationError on 401."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.sync_detailed
        module.get_transfer_run.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            transfer_runs_resource.get(team_id=12345, transfer_run_id=98765)

        assert exc_info.value.status_code == 401
        assert "Invalid or expired API key" in str(exc_info.value)

        module.get_transfer_run.sync_detailed = original

    def test_get_not_found_on_404(self, transfer_runs_resource: TransferRunsResource) -> None:
        """Test that get() raises APIError on 404 with the transfer run context."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.sync_detailed
        module.get_transfer_run.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer run not found")
        )

        with pytest.raises(APIError) as exc_info:
            transfer_runs_resource.get(team_id=12345, transfer_run_id=999)

        assert exc_info.value.status_code == 404
        assert "Transfer run not found" in str(exc_info.value)

        module.get_transfer_run.sync_detailed = original

    def test_get_api_error_on_500(self, transfer_runs_resource: TransferRunsResource) -> None:
        """Test that get() raises APIError on 500."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.sync_detailed
        module.get_transfer_run.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            transfer_runs_resource.get(team_id=12345, transfer_run_id=98765)

        assert exc_info.value.status_code == 500

        module.get_transfer_run.sync_detailed = original

    def test_get_network_error(self, transfer_runs_resource: TransferRunsResource) -> None:
        """Test that get() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.sync_detailed
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/teams/12345/transfer_runs/98765"
        module.get_transfer_run.sync_detailed = MagicMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        with pytest.raises(NetworkError):
            transfer_runs_resource.get(team_id=12345, transfer_run_id=98765)

        module.get_transfer_run.sync_detailed = original


class TestTransferRunsAsyncResource:
    """Test suite for TransferRunsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def transfer_runs_resource(self, mock_client: MagicMock) -> TransferRunsAsyncResource:
        """Create a TransferRunsAsyncResource instance with mock client."""
        return TransferRunsAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_run(self) -> TransferRunDetail:
        """Create a sample failed transfer run detail for testing."""
        return TransferRunDetail(
            id=98765,
            status="FAILED",
            query_details=[QueryDetails(status="FAILED", rows=0, error_description="Permission denied")],
            external_id="run-def-456",
            message="Query failed",
            failed_query_amount=1,
            query_amount=1,
            total_rows=0,
            data_date=datetime.date(2024, 1, 16),
        )

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        transfer_runs_resource: TransferRunsAsyncResource,
        sample_run: TransferRunDetail,
        meta: Meta,
    ) -> None:
        """Test successful async transfer run retrieval, unwrapped from the meta/data envelope."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.asyncio_detailed
        module.get_transfer_run.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(TransferRunDetailResponse(meta=meta, data=sample_run))
        )

        run = await transfer_runs_resource.get(team_id=99999, transfer_run_id=98765)

        assert run.id == 98765
        assert run.status == "FAILED"
        assert run.message == "Query failed"
        assert run.query_details[0].error_description == "Permission denied"

        module.get_transfer_run.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_passes_correct_params(
        self,
        transfer_runs_resource: TransferRunsAsyncResource,
        sample_run: TransferRunDetail,
        meta: Meta,
    ) -> None:
        """Test that async get() passes correct parameters."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(TransferRunDetailResponse(meta=meta, data=sample_run))
        )
        module.get_transfer_run.asyncio_detailed = mock_asyncio

        await transfer_runs_resource.get(team_id=99999, transfer_run_id=98765)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["transfer_run_id"] == 98765

        module.get_transfer_run.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_auth_error_on_401(self, transfer_runs_resource: TransferRunsAsyncResource) -> None:
        """Test that async get() raises AuthenticationError on 401."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.asyncio_detailed
        module.get_transfer_run.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await transfer_runs_resource.get(team_id=99999, transfer_run_id=98765)

        assert exc_info.value.status_code == 401

        module.get_transfer_run.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_not_found_on_404(self, transfer_runs_resource: TransferRunsAsyncResource) -> None:
        """Test that async get() raises APIError on 404 with the transfer run context."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.asyncio_detailed
        module.get_transfer_run.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Transfer run not found")
        )

        with pytest.raises(APIError) as exc_info:
            await transfer_runs_resource.get(team_id=99999, transfer_run_id=999)

        assert exc_info.value.status_code == 404
        assert "Transfer run not found" in str(exc_info.value)

        module.get_transfer_run.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_500(self, transfer_runs_resource: TransferRunsAsyncResource) -> None:
        """Test that async get() raises APIError on 500."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.asyncio_detailed
        module.get_transfer_run.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            await transfer_runs_resource.get(team_id=99999, transfer_run_id=98765)

        assert exc_info.value.status_code == 500

        module.get_transfer_run.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_network_error(self, transfer_runs_resource: TransferRunsAsyncResource) -> None:
        """Test that async get() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.transfer_runs as module

        original = module.get_transfer_run.asyncio_detailed
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/teams/99999/transfer_runs/98765"
        module.get_transfer_run.asyncio_detailed = AsyncMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        with pytest.raises(NetworkError):
            await transfer_runs_resource.get(team_id=99999, transfer_run_id=98765)

        module.get_transfer_run.asyncio_detailed = original
