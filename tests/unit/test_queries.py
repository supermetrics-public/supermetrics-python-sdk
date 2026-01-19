"""Unit tests for QueriesResource and QueriesAsyncResource."""

from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.data_response import DataResponse
from supermetrics._generated.supermetrics_api_client.models.data_response_meta import DataResponseMeta
from supermetrics._generated.supermetrics_api_client.models.get_data_response_400 import GetDataResponse400
from supermetrics._generated.supermetrics_api_client.models.get_data_response_401 import GetDataResponse401
from supermetrics._generated.supermetrics_api_client.models.get_data_response_403 import GetDataResponse403
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.queries import QueriesAsyncResource, QueriesResource


class TestQueriesResource:
    """Test suite for QueriesResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def queries_resource(self, mock_client: MagicMock) -> QueriesResource:
        """Create a QueriesResource instance with mock client."""
        return QueriesResource(mock_client)

    @pytest.fixture
    def sample_completed_response(self) -> DataResponse:
        """Create a sample completed query response."""
        meta = DataResponseMeta(
            request_id="req_123",
            schedule_id="schedule_456",
            status_code="completed",
        )
        return DataResponse(
            meta=meta,
            data=[
                ["2025-01-01", "1000", "500"],
                ["2025-01-02", "1200", "600"],
                ["2025-01-03", "1100", "550"],
            ],
        )

    @pytest.fixture
    def sample_pending_response(self) -> DataResponse:
        """Create a sample pending query response."""
        meta = DataResponseMeta(
            request_id="req_pending_789",
            schedule_id="schedule_789",
            status_code="pending",
        )
        return DataResponse(
            meta=meta,
            data=UNSET,
        )

    def test_execute_query_success(
        self,
        queries_resource: QueriesResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test execute() with successful completed query."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(return_value=sample_completed_response)

        # Act
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions", "users"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"
        assert result.meta.request_id == "req_123"
        assert len(result.data) == 3
        assert result.data[0] == ["2025-01-01", "1000", "500"]
        assert queries_module.get_data.sync.called

        # Verify DataQuery was created with correct parameters
        call_args = queries_module.get_data.sync.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.ds_id == "GAWA"
        assert json_param.ds_accounts == ["account_123"]
        assert json_param.fields == ["sessions", "users"]
        assert json_param.start_date == "2025-01-01"
        assert json_param.end_date == "2025-01-31"

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_execute_query_pending_status(
        self,
        queries_resource: QueriesResource,
        mock_client: MagicMock,
        sample_pending_response: DataResponse,
    ) -> None:
        """Test execute() with pending query status."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(return_value=sample_pending_response)

        # Act
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "pending"
        assert result.meta.request_id == "req_pending_789"

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_execute_query_with_all_parameters(
        self,
        queries_resource: QueriesResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test execute() with all optional parameters."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        mock_sync = MagicMock(return_value=sample_completed_response)
        queries_module.get_data.sync = mock_sync

        # Act
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123", "account_456"],
            fields=["sessions", "users", "pageviews"],
            start_date="2025-01-01",
            end_date="2025-01-31",
            max_rows=1000,
            cache_minutes=30,
            filter_="sessions > 100",
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"

        # Verify all parameters passed correctly including kwargs
        call_args = mock_sync.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.ds_id == "GAWA"
        assert json_param.ds_accounts == ["account_123", "account_456"]
        assert json_param.fields == ["sessions", "users", "pageviews"]
        assert json_param.start_date == "2025-01-01"
        assert json_param.end_date == "2025-01-31"
        assert json_param.max_rows == 1000
        assert json_param.cache_minutes == 30
        assert json_param.filter_ == "sessions > 100"

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_execute_query_with_minimal_parameters(
        self,
        queries_resource: QueriesResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test execute() with only required parameters."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(return_value=sample_completed_response)

        # Act
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="yesterday",
            end_date="yesterday",
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_get_results_for_pending_query(
        self,
        queries_resource: QueriesResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test get_results() retrieves completed results for a pending query."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        mock_sync = MagicMock(return_value=sample_completed_response)
        queries_module.get_data.sync = mock_sync

        # Act
        result = queries_resource.get_results(query_id="req_pending_789")

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"
        assert len(result.data) == 3

        # Verify schedule_id was set to the query_id
        call_args = mock_sync.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.schedule_id == "req_pending_789"

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_execute_query_with_none_response(
        self, queries_resource: QueriesResource, mock_client: MagicMock
    ) -> None:
        """Test execute() with None response returns None."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(return_value=None)

        # Act
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is None

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_execute_query_with_unset_response(
        self, queries_resource: QueriesResource, mock_client: MagicMock
    ) -> None:
        """Test execute() with UNSET response returns None."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(return_value=UNSET)

        # Act
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is None

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_get_results_with_none_response(
        self, queries_resource: QueriesResource, mock_client: MagicMock
    ) -> None:
        """Test get_results() with None response returns None."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(return_value=None)

        # Act
        result = queries_resource.get_results(query_id="req_123")

        # Assert
        assert result is None

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_async_query_polling_workflow(
        self,
        queries_resource: QueriesResource,
        mock_client: MagicMock,
        sample_pending_response: DataResponse,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test complete async query polling workflow."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync

        # First call returns pending, second call returns completed
        mock_sync = MagicMock()
        mock_sync.side_effect = [sample_pending_response, sample_completed_response]
        queries_module.get_data.sync = mock_sync

        # Act - Step 1: Execute query (returns pending)
        result = queries_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert - Step 1: Verify pending status
        assert result is not None
        assert result.meta.status_code == "pending"
        query_id = result.meta.request_id

        # Act - Step 2: Poll for results
        result = queries_resource.get_results(query_id=query_id)

        # Assert - Step 2: Verify completed status
        assert result is not None
        assert result.meta.status_code == "completed"
        assert len(result.data) == 3

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_authentication_error_on_401(self, queries_resource: QueriesResource, mock_client: MagicMock) -> None:
        """Test 401 response raises AuthenticationError."""
        # Mock httpx to raise HTTPStatusError with 401
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=mock_request,
            response=mock_response
        )

        # Mock the API method to raise the error
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(side_effect=error)

        # Verify AuthenticationError is raised
        with pytest.raises(AuthenticationError) as exc_info:
            queries_resource.execute(
                ds_id="GAWA",
                ds_accounts=["account_123"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert exc_info.value.status_code == 401
        assert "Invalid or expired API key" in str(exc_info.value)

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_validation_error_on_400(self, queries_resource: QueriesResource, mock_client: MagicMock) -> None:
        """Test 400 response raises ValidationError."""
        # Mock API to return GetDataResponse400 (generated client behavior)
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync

        # Create a GetDataResponse400 instance with required fields
        error_response = GetDataResponse400(
            type_="about:blank",
            title="Bad Request",
            status=400
        )
        queries_module.get_data.sync = MagicMock(return_value=error_response)

        # Verify ValidationError is raised
        with pytest.raises(ValidationError) as exc_info:
            queries_resource.execute(
                ds_id="GAWA",
                ds_accounts=["account_123"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert exc_info.value.status_code == 400
        assert "Invalid request parameters" in str(exc_info.value)

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_api_error_on_404(self, queries_resource: QueriesResource, mock_client: MagicMock) -> None:
        """Test 404 response raises APIError."""
        # Mock httpx to raise HTTPStatusError with 404
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.HTTPStatusError(
            "404 Not Found",
            request=mock_request,
            response=mock_response
        )

        # Mock the API method to raise the error
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(side_effect=error)

        # Verify APIError is raised
        with pytest.raises(APIError) as exc_info:
            queries_resource.execute(
                ds_id="GAWA",
                ds_accounts=["account_123"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_api_error_on_500(self, queries_resource: QueriesResource, mock_client: MagicMock) -> None:
        """Test 500 response raises APIError."""
        # Mock httpx to raise HTTPStatusError with 500
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.HTTPStatusError(
            "500 Internal Server Error",
            request=mock_request,
            response=mock_response
        )

        # Mock the API method to raise the error
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(side_effect=error)

        # Verify APIError is raised
        with pytest.raises(APIError) as exc_info:
            queries_resource.execute(
                ds_id="GAWA",
                ds_accounts=["account_123"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert exc_info.value.status_code == 500
        assert "Supermetrics API error" in str(exc_info.value)

        # Cleanup
        queries_module.get_data.sync = original_get_data

    def test_network_error_on_timeout(self, queries_resource: QueriesResource, mock_client: MagicMock) -> None:
        """Test network timeout raises NetworkError."""
        # Mock httpx.RequestError (not HTTPStatusError)
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.TimeoutException("Request timeout", request=mock_request)

        # Mock the API method to raise the error
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.sync
        queries_module.get_data.sync = MagicMock(side_effect=error)

        # Verify NetworkError is raised
        with pytest.raises(NetworkError) as exc_info:
            queries_resource.execute(
                ds_id="GAWA",
                ds_accounts=["account_123"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None  # Network errors have no HTTP status

        # Cleanup
        queries_module.get_data.sync = original_get_data


class TestQueriesAsyncResource:
    """Test suite for QueriesAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def queries_async_resource(self, mock_client: MagicMock) -> QueriesAsyncResource:
        """Create a QueriesAsyncResource instance with mock client."""
        return QueriesAsyncResource(mock_client)

    @pytest.fixture
    def sample_completed_response(self) -> DataResponse:
        """Create a sample completed query response."""
        meta = DataResponseMeta(
            request_id="req_async_123",
            schedule_id="schedule_async_456",
            status_code="completed",
        )
        return DataResponse(
            meta=meta,
            data=[
                ["2025-01-01", "2000", "1000"],
                ["2025-01-02", "2400", "1200"],
            ],
        )

    @pytest.fixture
    def sample_pending_response(self) -> DataResponse:
        """Create a sample pending query response."""
        meta = DataResponseMeta(
            request_id="req_async_pending_999",
            schedule_id="schedule_async_999",
            status_code="pending",
        )
        return DataResponse(
            meta=meta,
            data=UNSET,
        )

    @pytest.mark.asyncio
    async def test_execute_async_query(
        self,
        queries_async_resource: QueriesAsyncResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test async execute() method."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.asyncio
        queries_module.get_data.asyncio = AsyncMock(return_value=sample_completed_response)

        # Act
        result = await queries_async_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions", "users"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"
        assert result.meta.request_id == "req_async_123"
        assert len(result.data) == 2
        assert queries_module.get_data.asyncio.called

        # Cleanup
        queries_module.get_data.asyncio = original_get_data

    @pytest.mark.asyncio
    async def test_execute_async_query_with_filters(
        self,
        queries_async_resource: QueriesAsyncResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test async execute() with additional parameters."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.asyncio
        mock_asyncio = AsyncMock(return_value=sample_completed_response)
        queries_module.get_data.asyncio = mock_asyncio

        # Act
        result = await queries_async_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123", "account_456"],
            fields=["sessions", "users"],
            start_date="2025-01-01",
            end_date="2025-01-31",
            max_rows=500,
            cache_minutes=60,
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"

        # Verify parameters passed correctly
        call_args = mock_asyncio.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.ds_id == "GAWA"
        assert json_param.ds_accounts == ["account_123", "account_456"]
        assert json_param.max_rows == 500
        assert json_param.cache_minutes == 60

        # Cleanup
        queries_module.get_data.asyncio = original_get_data

    @pytest.mark.asyncio
    async def test_get_results_async(
        self,
        queries_async_resource: QueriesAsyncResource,
        mock_client: MagicMock,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test async get_results() method."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.asyncio
        mock_asyncio = AsyncMock(return_value=sample_completed_response)
        queries_module.get_data.asyncio = mock_asyncio

        # Act
        result = await queries_async_resource.get_results(query_id="req_async_pending_999")

        # Assert
        assert result is not None
        assert result.meta.status_code == "completed"
        assert len(result.data) == 2

        # Verify schedule_id was set
        call_args = mock_asyncio.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.schedule_id == "req_async_pending_999"

        # Cleanup
        queries_module.get_data.asyncio = original_get_data

    @pytest.mark.asyncio
    async def test_execute_async_pending_query(
        self,
        queries_async_resource: QueriesAsyncResource,
        mock_client: MagicMock,
        sample_pending_response: DataResponse,
    ) -> None:
        """Test async execute() returns pending status."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.asyncio
        queries_module.get_data.asyncio = AsyncMock(return_value=sample_pending_response)

        # Act
        result = await queries_async_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is not None
        assert result.meta.status_code == "pending"
        assert result.meta.request_id == "req_async_pending_999"

        # Cleanup
        queries_module.get_data.asyncio = original_get_data

    @pytest.mark.asyncio
    async def test_execute_async_with_empty_response(
        self, queries_async_resource: QueriesAsyncResource, mock_client: MagicMock
    ) -> None:
        """Test async execute() with empty response."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.asyncio
        queries_module.get_data.asyncio = AsyncMock(return_value=None)

        # Act
        result = await queries_async_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        assert result is None

        # Cleanup
        queries_module.get_data.asyncio = original_get_data

    @pytest.mark.asyncio
    async def test_async_query_polling_workflow(
        self,
        queries_async_resource: QueriesAsyncResource,
        mock_client: MagicMock,
        sample_pending_response: DataResponse,
        sample_completed_response: DataResponse,
    ) -> None:
        """Test complete async query polling workflow with async/await."""
        # Arrange
        import supermetrics.resources.queries as queries_module

        original_get_data = queries_module.get_data.asyncio

        # First call returns pending, second call returns completed
        mock_asyncio = AsyncMock()
        mock_asyncio.side_effect = [sample_pending_response, sample_completed_response]
        queries_module.get_data.asyncio = mock_asyncio

        # Act - Step 1: Execute query (returns pending)
        result = await queries_async_resource.execute(
            ds_id="GAWA",
            ds_accounts=["account_123"],
            fields=["sessions"],
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert - Step 1: Verify pending status
        assert result is not None
        assert result.meta.status_code == "pending"
        query_id = result.meta.request_id

        # Act - Step 2: Poll for results
        result = await queries_async_resource.get_results(query_id=query_id)

        # Assert - Step 2: Verify completed status
        assert result is not None
        assert result.meta.status_code == "completed"
        assert len(result.data) == 2

        # Cleanup
        queries_module.get_data.asyncio = original_get_data
