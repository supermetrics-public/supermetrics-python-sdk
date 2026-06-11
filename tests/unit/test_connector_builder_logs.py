"""Unit tests for ConnectorBuilderLogsResource and ConnectorBuilderLogsAsyncResource."""

from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.list_connector_logs_response_200 import (
    ListConnectorLogsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.log_entry import LogEntry
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError
from supermetrics.resources.connector_builder_logs import (
    ConnectorBuilderLogsAsyncResource,
    ConnectorBuilderLogsResource,
)


def _make_error_response(code: str, message: str) -> ErrorResponse:
    """Create an ErrorResponse with the given code and message."""
    return ErrorResponse(
        meta=ResponseMeta(request_id="req-id"),
        error=Error(code=code, message=message),
    )


class TestConnectorBuilderLogsResource:
    """Test suite for ConnectorBuilderLogsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> ConnectorBuilderLogsResource:
        """Create a ConnectorBuilderLogsResource instance with mock client."""
        return ConnectorBuilderLogsResource(mock_client)

    # --- list() ---

    def test_list_success(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test successful listing of connector logs."""
        import supermetrics.resources.connector_builder_logs as logs_module

        expected = ListConnectorLogsResponse200(logs=[])
        original = logs_module.list_connector_logs.sync
        logs_module.list_connector_logs.sync = MagicMock(return_value=expected)

        try:
            result = resource.list(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, ListConnectorLogsResponse200)
            assert logs_module.list_connector_logs.sync.called
        finally:
            logs_module.list_connector_logs.sync = original

    def test_list_passes_correct_params(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that list() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.sync
        mock_sync = MagicMock(return_value=ListConnectorLogsResponse200(logs=[]))
        logs_module.list_connector_logs.sync = mock_sync

        try:
            resource.list(team_id=99999, connector_identifier="test-conn", limit=10, before="2025-06-01T00:00:00Z")
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["connector_identifier"] == "test-conn"
            assert call_kwargs["limit"] == 10
            import datetime

            assert call_kwargs["before"] == datetime.datetime(2025, 6, 1, 0, 0, tzinfo=datetime.UTC)
        finally:
            logs_module.list_connector_logs.sync = original

    def test_list_auth_error_on_401(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that list() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.sync
        logs_module.list_connector_logs.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            logs_module.list_connector_logs.sync = original

    def test_list_api_error_on_error_response(
        self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock
    ) -> None:
        """Test that list() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.sync
        logs_module.list_connector_logs.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Connector not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.list(team_id=12345, connector_identifier="missing")
            assert "not found" in str(exc_info.value).lower()
        finally:
            logs_module.list_connector_logs.sync = original

    def test_list_api_error_on_500_http(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that list() raises APIError on HTTP 500."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.HTTPStatusError("500", request=mock_request, response=mock_response)

        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.sync
        logs_module.list_connector_logs.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(APIError) as exc_info:
                resource.list(team_id=12345, connector_identifier="my-connector")
            assert exc_info.value.status_code == 500
        finally:
            logs_module.list_connector_logs.sync = original

    def test_list_network_error(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that list() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.sync
        logs_module.list_connector_logs.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.list(team_id=12345, connector_identifier="my-connector")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            logs_module.list_connector_logs.sync = original

    # --- get() ---

    def test_get_success(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test successful retrieval of a specific log entry."""
        import supermetrics.resources.connector_builder_logs as logs_module

        expected = LogEntry(id="log-abc123")
        original = logs_module.get_connector_log.sync
        logs_module.get_connector_log.sync = MagicMock(return_value=expected)

        try:
            result = resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc123")
            assert isinstance(result, LogEntry)
            assert logs_module.get_connector_log.sync.called
        finally:
            logs_module.get_connector_log.sync = original

    def test_get_passes_correct_params(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that get() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.sync
        mock_sync = MagicMock(return_value=LogEntry(id="log-xyz"))
        logs_module.get_connector_log.sync = mock_sync

        try:
            resource.get(team_id=12345, connector_identifier="test-conn", log_id="log-xyz")
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["connector_identifier"] == "test-conn"
            assert call_kwargs["log_id"] == "log-xyz"
        finally:
            logs_module.get_connector_log.sync = original

    def test_get_auth_error_on_401(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that get() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.sync
        logs_module.get_connector_log.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc")
        finally:
            logs_module.get_connector_log.sync = original

    def test_get_api_error_on_404(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that get() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.sync
        logs_module.get_connector_log.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Log entry not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.get(team_id=12345, connector_identifier="my-connector", log_id="missing-log")
            assert "not found" in str(exc_info.value).lower()
        finally:
            logs_module.get_connector_log.sync = original

    def test_get_api_error_on_error_response(
        self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock
    ) -> None:
        """Test that get() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.sync
        logs_module.get_connector_log.sync = MagicMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Internal server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc")
            assert "Internal server error" in str(exc_info.value)
        finally:
            logs_module.get_connector_log.sync = original

    def test_get_network_error(self, resource: ConnectorBuilderLogsResource, mock_client: MagicMock) -> None:
        """Test that get() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.sync
        logs_module.get_connector_log.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            logs_module.get_connector_log.sync = original


class TestConnectorBuilderLogsAsyncResource:
    """Test suite for ConnectorBuilderLogsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> ConnectorBuilderLogsAsyncResource:
        """Create a ConnectorBuilderLogsAsyncResource instance with mock client."""
        return ConnectorBuilderLogsAsyncResource(mock_client)

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test successful async listing of connector logs."""
        import supermetrics.resources.connector_builder_logs as logs_module

        expected = ListConnectorLogsResponse200(logs=[])
        original = logs_module.list_connector_logs.asyncio
        logs_module.list_connector_logs.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.list(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, ListConnectorLogsResponse200)
            assert logs_module.list_connector_logs.asyncio.called
        finally:
            logs_module.list_connector_logs.asyncio = original

    @pytest.mark.asyncio
    async def test_list_auth_error_on_401(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test that async list() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.asyncio
        logs_module.list_connector_logs.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            logs_module.list_connector_logs.asyncio = original

    @pytest.mark.asyncio
    async def test_list_api_error_on_error_response(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test that async list() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.asyncio
        logs_module.list_connector_logs.asyncio = AsyncMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Internal server error")
        )

        try:
            with pytest.raises(APIError):
                await resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            logs_module.list_connector_logs.asyncio = original

    @pytest.mark.asyncio
    async def test_list_network_error(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test that async list() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.list_connector_logs.asyncio
        logs_module.list_connector_logs.asyncio = AsyncMock(side_effect=error)

        try:
            with pytest.raises(NetworkError):
                await resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            logs_module.list_connector_logs.asyncio = original

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test successful async retrieval of a specific log entry."""
        import supermetrics.resources.connector_builder_logs as logs_module

        expected = LogEntry(id="log-abc123")
        original = logs_module.get_connector_log.asyncio
        logs_module.get_connector_log.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc123")
            assert isinstance(result, LogEntry)
            assert logs_module.get_connector_log.asyncio.called
        finally:
            logs_module.get_connector_log.asyncio = original

    @pytest.mark.asyncio
    async def test_get_auth_error_on_401(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test that async get() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.asyncio
        logs_module.get_connector_log.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc")
        finally:
            logs_module.get_connector_log.asyncio = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_404(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test that async get() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.asyncio
        logs_module.get_connector_log.asyncio = AsyncMock(
            return_value=_make_error_response("NOT_FOUND", "Log entry not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await resource.get(team_id=12345, connector_identifier="my-connector", log_id="missing")
            assert "not found" in str(exc_info.value).lower()
        finally:
            logs_module.get_connector_log.asyncio = original

    @pytest.mark.asyncio
    async def test_get_network_error(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Test that async get() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_logs as logs_module

        original = logs_module.get_connector_log.asyncio
        logs_module.get_connector_log.asyncio = AsyncMock(side_effect=error)

        try:
            with pytest.raises(NetworkError):
                await resource.get(team_id=12345, connector_identifier="my-connector", log_id="log-abc")
        finally:
            logs_module.get_connector_log.asyncio = original
