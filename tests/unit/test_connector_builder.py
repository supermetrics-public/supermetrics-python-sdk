"""Unit tests for ConnectorBuilderResource and ConnectorBuilderAsyncResource."""

import io
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.connector import Connector
from supermetrics._generated.supermetrics_api_client.models.connector_with_configuration import (
    ConnectorWithConfiguration,
)
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.get_connector_logo_response_200 import (
    GetConnectorLogoResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_connectors_response_200 import (
    ListConnectorsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.models.upload_connector_logo_response_201 import (
    UploadConnectorLogoResponse201,
)
from supermetrics._generated.supermetrics_api_client.types import File
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError
from supermetrics.resources.connector_builder import ConnectorBuilderAsyncResource, ConnectorBuilderResource


def _make_error_response(code: str, message: str) -> ErrorResponse:
    """Create an ErrorResponse with the given code and message."""
    return ErrorResponse(
        meta=ResponseMeta(request_id="req-id"),
        error=Error(code=code, message=message),
    )


class TestConnectorBuilderResource:
    """Test suite for ConnectorBuilderResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> ConnectorBuilderResource:
        """Create a ConnectorBuilderResource instance with mock client."""
        return ConnectorBuilderResource(mock_client)

    # --- list() ---

    def test_list_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful listing of connectors."""
        import supermetrics.resources.connector_builder as cb_module

        expected = ListConnectorsResponse200(count=1, connectors=[Connector(name="Test")])
        original = cb_module.list_connectors.sync
        cb_module.list_connectors.sync = MagicMock(return_value=expected)

        try:
            result = resource.list(team_id=12345)
            assert isinstance(result, ListConnectorsResponse200)
            assert cb_module.list_connectors.sync.called
        finally:
            cb_module.list_connectors.sync = original

    def test_list_passes_correct_params(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that list() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.sync
        mock_sync = MagicMock(return_value=ListConnectorsResponse200(count=0, connectors=[]))
        cb_module.list_connectors.sync = mock_sync

        try:
            resource.list(team_id=99999, include_configs=True)
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["include_configs"] is True
        finally:
            cb_module.list_connectors.sync = original

    def test_list_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that list() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.sync
        cb_module.list_connectors.sync = MagicMock(return_value=_make_error_response("UNAUTHORIZED", "Invalid API key"))

        try:
            with pytest.raises(AuthenticationError):
                resource.list(team_id=12345)
        finally:
            cb_module.list_connectors.sync = original

    def test_list_api_error_on_error_response(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that list() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.sync
        cb_module.list_connectors.sync = MagicMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Internal server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.list(team_id=12345)
            assert "Internal server error" in str(exc_info.value)
        finally:
            cb_module.list_connectors.sync = original

    def test_list_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that list() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.sync
        cb_module.list_connectors.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.list(team_id=12345)
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.list_connectors.sync = original

    # --- get() ---

    def test_get_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful retrieval of a connector."""
        import supermetrics.resources.connector_builder as cb_module

        expected = ConnectorWithConfiguration(name="My Connector")
        original = cb_module.get_connector.sync
        cb_module.get_connector.sync = MagicMock(return_value=expected)

        try:
            result = resource.get(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, ConnectorWithConfiguration)
            assert cb_module.get_connector.sync.called
        finally:
            cb_module.get_connector.sync = original

    def test_get_passes_correct_params(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector.sync
        mock_sync = MagicMock(return_value=ConnectorWithConfiguration(name="My Connector"))
        cb_module.get_connector.sync = mock_sync

        try:
            resource.get(team_id=12345, connector_identifier="test-conn")
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["connector_identifier"] == "test-conn"
        finally:
            cb_module.get_connector.sync = original

    def test_get_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector.sync
        cb_module.get_connector.sync = MagicMock(return_value=_make_error_response("UNAUTHORIZED", "Invalid API key"))

        try:
            with pytest.raises(AuthenticationError):
                resource.get(team_id=12345, connector_identifier="my-connector")
        finally:
            cb_module.get_connector.sync = original

    def test_get_api_error_on_404(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector.sync
        cb_module.get_connector.sync = MagicMock(return_value=_make_error_response("NOT_FOUND", "Connector not found"))

        try:
            with pytest.raises(APIError) as exc_info:
                resource.get(team_id=12345, connector_identifier="missing")
            assert "not found" in str(exc_info.value).lower()
        finally:
            cb_module.get_connector.sync = original

    def test_get_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector.sync
        cb_module.get_connector.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.get(team_id=12345, connector_identifier="my-connector")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.get_connector.sync = original

    # --- create() ---

    def test_create_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful connector creation."""
        import supermetrics.resources.connector_builder as cb_module

        expected = ConnectorWithConfiguration(name="My Connector")
        original = cb_module.create_connector.sync
        cb_module.create_connector.sync = MagicMock(return_value=expected)

        try:
            result = resource.create(team_id=12345, title="My Connector", description="A test connector")
            assert isinstance(result, ConnectorWithConfiguration)
            assert cb_module.create_connector.sync.called
        finally:
            cb_module.create_connector.sync = original

    def test_create_passes_correct_params(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that create() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.sync
        mock_sync = MagicMock(return_value=ConnectorWithConfiguration(name="My Connector"))
        cb_module.create_connector.sync = mock_sync

        try:
            resource.create(team_id=12345, title="My Connector", description="desc", connector_identifier="dup-from")
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["body"].title == "My Connector"
            assert call_kwargs["body"].description == "desc"
            assert call_kwargs["body"].connector_identifier == "dup-from"
        finally:
            cb_module.create_connector.sync = original

    def test_create_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that create() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.sync
        cb_module.create_connector.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.create(team_id=12345, title="Test")
        finally:
            cb_module.create_connector.sync = original

    def test_create_api_error_on_error_response(
        self, resource: ConnectorBuilderResource, mock_client: MagicMock
    ) -> None:
        """Test that create() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.sync
        cb_module.create_connector.sync = MagicMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Invalid request parameters")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.create(team_id=12345, title="Test")
            assert "Invalid request parameters" in str(exc_info.value)
        finally:
            cb_module.create_connector.sync = original

    def test_create_api_error_on_500_http(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that create() raises APIError on HTTP 500."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.HTTPStatusError("500", request=mock_request, response=mock_response)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.sync
        cb_module.create_connector.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(APIError) as exc_info:
                resource.create(team_id=12345, title="Test")
            assert exc_info.value.status_code == 500
        finally:
            cb_module.create_connector.sync = original

    def test_create_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that create() raises NetworkError on network timeout."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.sync
        cb_module.create_connector.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.create(team_id=12345, title="Test")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.create_connector.sync = original

    # --- update() ---

    def test_update_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful connector update (204 No Content)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.update_connector.sync
        cb_module.update_connector.sync = MagicMock(return_value=None)

        try:
            result = resource.update(
                team_id=12345,
                connector_identifier="my-connector",
                connector={"name": "Updated Name", "description": "Updated description"},
                configuration={"configuration_json": {}},
            )
            assert result is None
            assert cb_module.update_connector.sync.called
        finally:
            cb_module.update_connector.sync = original

    def test_update_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that update() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.update_connector.sync
        cb_module.update_connector.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    connector={"name": "Test", "description": "desc"},
                    configuration={"configuration_json": {}},
                )
        finally:
            cb_module.update_connector.sync = original

    def test_update_api_error_on_404(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that update() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.update_connector.sync
        cb_module.update_connector.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Connector not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.update(
                    team_id=12345,
                    connector_identifier="missing",
                    connector={"name": "Test", "description": "desc"},
                    configuration={"configuration_json": {"id": "cfg-1"}},
                )
            assert "not found" in str(exc_info.value).lower()
        finally:
            cb_module.update_connector.sync = original

    def test_update_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that update() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.update_connector.sync
        cb_module.update_connector.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    connector={"name": "Test", "description": "desc"},
                    configuration={"configuration_json": {"id": "cfg-1"}},
                )
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.update_connector.sync = original

    # --- delete() ---

    def test_delete_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful connector deletion (204 No Content)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.delete_connector.sync
        cb_module.delete_connector.sync = MagicMock(return_value=None)

        try:
            result = resource.delete(team_id=12345, connector_identifier="my-connector")
            assert result is None
            assert cb_module.delete_connector.sync.called
        finally:
            cb_module.delete_connector.sync = original

    def test_delete_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that delete() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.delete_connector.sync
        cb_module.delete_connector.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.delete(team_id=12345, connector_identifier="my-connector")
        finally:
            cb_module.delete_connector.sync = original

    def test_delete_api_error_on_404(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that delete() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.delete_connector.sync
        cb_module.delete_connector.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Connector not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.delete(team_id=12345, connector_identifier="missing")
            assert "not found" in str(exc_info.value).lower()
        finally:
            cb_module.delete_connector.sync = original

    def test_delete_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that delete() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.delete_connector.sync
        cb_module.delete_connector.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.delete(team_id=12345, connector_identifier="my-connector")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.delete_connector.sync = original

    # --- get_logo() ---

    def test_get_logo_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful retrieval of connector logo."""
        import supermetrics.resources.connector_builder as cb_module

        expected = GetConnectorLogoResponse200(logo_url="https://cdn.example.com/logo.png")
        original = cb_module.get_connector_logo.sync
        cb_module.get_connector_logo.sync = MagicMock(return_value=expected)

        try:
            result = resource.get_logo(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, GetConnectorLogoResponse200)
            assert result.logo_url == "https://cdn.example.com/logo.png"
            assert cb_module.get_connector_logo.sync.called
        finally:
            cb_module.get_connector_logo.sync = original

    def test_get_logo_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get_logo() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector_logo.sync
        cb_module.get_connector_logo.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.get_logo(team_id=12345, connector_identifier="my-connector")
        finally:
            cb_module.get_connector_logo.sync = original

    def test_get_logo_api_error_on_404(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get_logo() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector_logo.sync
        cb_module.get_connector_logo.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Connector not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.get_logo(team_id=12345, connector_identifier="missing")
            assert "not found" in str(exc_info.value).lower()
        finally:
            cb_module.get_connector_logo.sync = original

    def test_get_logo_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that get_logo() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector_logo.sync
        cb_module.get_connector_logo.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.get_logo(team_id=12345, connector_identifier="my-connector")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.get_connector_logo.sync = original

    # --- upload_logo() ---

    def test_upload_logo_success(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test successful logo upload."""
        import supermetrics.resources.connector_builder as cb_module

        expected = UploadConnectorLogoResponse201(logo_url="https://cdn.example.com/new-logo.png")
        original = cb_module.upload_connector_logo.sync
        cb_module.upload_connector_logo.sync = MagicMock(return_value=expected)

        try:
            logo_file = File(payload=io.BytesIO(b"fake-png-data"), file_name="logo.png", mime_type="image/png")
            result = resource.upload_logo(team_id=12345, connector_identifier="my-connector", logo=logo_file)
            assert isinstance(result, UploadConnectorLogoResponse201)
            assert result.logo_url == "https://cdn.example.com/new-logo.png"
            assert cb_module.upload_connector_logo.sync.called
        finally:
            cb_module.upload_connector_logo.sync = original

    def test_upload_logo_auth_error_on_401(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that upload_logo() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.upload_connector_logo.sync
        cb_module.upload_connector_logo.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            logo_file = File(payload=io.BytesIO(b"data"), file_name="logo.png", mime_type="image/png")
            with pytest.raises(AuthenticationError):
                resource.upload_logo(team_id=12345, connector_identifier="my-connector", logo=logo_file)
        finally:
            cb_module.upload_connector_logo.sync = original

    def test_upload_logo_api_error_on_error_response(
        self, resource: ConnectorBuilderResource, mock_client: MagicMock
    ) -> None:
        """Test that upload_logo() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.upload_connector_logo.sync
        cb_module.upload_connector_logo.sync = MagicMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Invalid logo file")
        )

        try:
            logo_file = File(payload=io.BytesIO(b"data"), file_name="logo.bmp", mime_type="image/bmp")
            with pytest.raises(APIError) as exc_info:
                resource.upload_logo(team_id=12345, connector_identifier="my-connector", logo=logo_file)
            assert "Invalid logo file" in str(exc_info.value)
        finally:
            cb_module.upload_connector_logo.sync = original

    def test_upload_logo_network_error(self, resource: ConnectorBuilderResource, mock_client: MagicMock) -> None:
        """Test that upload_logo() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.upload_connector_logo.sync
        cb_module.upload_connector_logo.sync = MagicMock(side_effect=error)

        try:
            logo_file = File(payload=io.BytesIO(b"data"), file_name="logo.png", mime_type="image/png")
            with pytest.raises(NetworkError) as exc_info:
                resource.upload_logo(team_id=12345, connector_identifier="my-connector", logo=logo_file)
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            cb_module.upload_connector_logo.sync = original


class TestConnectorBuilderAsyncResource:
    """Test suite for ConnectorBuilderAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> ConnectorBuilderAsyncResource:
        """Create a ConnectorBuilderAsyncResource instance with mock client."""
        return ConnectorBuilderAsyncResource(mock_client)

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async listing of connectors."""
        import supermetrics.resources.connector_builder as cb_module

        expected = ListConnectorsResponse200(count=0, connectors=[])
        original = cb_module.list_connectors.asyncio
        cb_module.list_connectors.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.list(team_id=12345)
            assert isinstance(result, ListConnectorsResponse200)
            assert cb_module.list_connectors.asyncio.called
        finally:
            cb_module.list_connectors.asyncio = original

    @pytest.mark.asyncio
    async def test_list_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async list() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.asyncio
        cb_module.list_connectors.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.list(team_id=12345)
        finally:
            cb_module.list_connectors.asyncio = original

    @pytest.mark.asyncio
    async def test_list_api_error_on_error_response(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async list() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.asyncio
        cb_module.list_connectors.asyncio = AsyncMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Internal server error")
        )

        try:
            with pytest.raises(APIError):
                await resource.list(team_id=12345)
        finally:
            cb_module.list_connectors.asyncio = original

    @pytest.mark.asyncio
    async def test_list_network_error(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async list() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.list_connectors.asyncio
        cb_module.list_connectors.asyncio = AsyncMock(side_effect=error)

        try:
            with pytest.raises(NetworkError):
                await resource.list(team_id=12345)
        finally:
            cb_module.list_connectors.asyncio = original

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async connector creation."""
        import supermetrics.resources.connector_builder as cb_module

        expected = ConnectorWithConfiguration(name="My Async Connector")
        original = cb_module.create_connector.asyncio
        cb_module.create_connector.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.create(team_id=12345, title="My Async Connector")
            assert isinstance(result, ConnectorWithConfiguration)
            assert cb_module.create_connector.asyncio.called
        finally:
            cb_module.create_connector.asyncio = original

    @pytest.mark.asyncio
    async def test_create_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async create() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.asyncio
        cb_module.create_connector.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.create(team_id=12345, title="Test")
        finally:
            cb_module.create_connector.asyncio = original

    @pytest.mark.asyncio
    async def test_create_api_error_on_error_response(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async create() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.create_connector.asyncio
        cb_module.create_connector.asyncio = AsyncMock(
            return_value=_make_error_response("RATE_LIMIT", "Rate limit exceeded")
        )

        try:
            with pytest.raises(APIError):
                await resource.create(team_id=12345, title="Test")
        finally:
            cb_module.create_connector.asyncio = original

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async retrieval of a connector."""
        import supermetrics.resources.connector_builder as cb_module

        expected = ConnectorWithConfiguration(name="My Connector")
        original = cb_module.get_connector.asyncio
        cb_module.get_connector.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.get(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, ConnectorWithConfiguration)
            assert cb_module.get_connector.asyncio.called
        finally:
            cb_module.get_connector.asyncio = original

    @pytest.mark.asyncio
    async def test_get_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async get() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector.asyncio
        cb_module.get_connector.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.get(team_id=12345, connector_identifier="my-connector")
        finally:
            cb_module.get_connector.asyncio = original

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async connector update (204 No Content)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.update_connector.asyncio
        cb_module.update_connector.asyncio = AsyncMock(return_value=None)

        try:
            result = await resource.update(
                team_id=12345,
                connector_identifier="my-connector",
                connector={"name": "Updated", "description": "desc"},
                configuration={"configuration_json": {"id": "cfg-1"}},
            )
            assert result is None
            assert cb_module.update_connector.asyncio.called
        finally:
            cb_module.update_connector.asyncio = original

    @pytest.mark.asyncio
    async def test_update_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async update() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.update_connector.asyncio
        cb_module.update_connector.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    connector={"name": "Test", "description": "desc"},
                    configuration={"configuration_json": {"id": "cfg-1"}},
                )
        finally:
            cb_module.update_connector.asyncio = original

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async connector deletion (204 No Content)."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.delete_connector.asyncio
        cb_module.delete_connector.asyncio = AsyncMock(return_value=None)

        try:
            result = await resource.delete(team_id=12345, connector_identifier="my-connector")
            assert result is None
            assert cb_module.delete_connector.asyncio.called
        finally:
            cb_module.delete_connector.asyncio = original

    @pytest.mark.asyncio
    async def test_delete_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async delete() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.delete_connector.asyncio
        cb_module.delete_connector.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.delete(team_id=12345, connector_identifier="my-connector")
        finally:
            cb_module.delete_connector.asyncio = original

    # --- get_logo() ---

    @pytest.mark.asyncio
    async def test_get_logo_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async retrieval of connector logo."""
        import supermetrics.resources.connector_builder as cb_module

        expected = GetConnectorLogoResponse200(logo_url="https://cdn.example.com/logo.png")
        original = cb_module.get_connector_logo.asyncio
        cb_module.get_connector_logo.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.get_logo(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, GetConnectorLogoResponse200)
            assert result.logo_url == "https://cdn.example.com/logo.png"
            assert cb_module.get_connector_logo.asyncio.called
        finally:
            cb_module.get_connector_logo.asyncio = original

    @pytest.mark.asyncio
    async def test_get_logo_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async get_logo() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.get_connector_logo.asyncio
        cb_module.get_connector_logo.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.get_logo(team_id=12345, connector_identifier="my-connector")
        finally:
            cb_module.get_connector_logo.asyncio = original

    # --- upload_logo() ---

    @pytest.mark.asyncio
    async def test_upload_logo_success(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test successful async logo upload."""
        import supermetrics.resources.connector_builder as cb_module

        expected = UploadConnectorLogoResponse201(logo_url="https://cdn.example.com/new-logo.png")
        original = cb_module.upload_connector_logo.asyncio
        cb_module.upload_connector_logo.asyncio = AsyncMock(return_value=expected)

        try:
            logo_file = File(payload=io.BytesIO(b"fake-png-data"), file_name="logo.png", mime_type="image/png")
            result = await resource.upload_logo(team_id=12345, connector_identifier="my-connector", logo=logo_file)
            assert isinstance(result, UploadConnectorLogoResponse201)
            assert result.logo_url == "https://cdn.example.com/new-logo.png"
            assert cb_module.upload_connector_logo.asyncio.called
        finally:
            cb_module.upload_connector_logo.asyncio = original

    @pytest.mark.asyncio
    async def test_upload_logo_auth_error_on_401(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Test that async upload_logo() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder as cb_module

        original = cb_module.upload_connector_logo.asyncio
        cb_module.upload_connector_logo.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            logo_file = File(payload=io.BytesIO(b"data"), file_name="logo.png", mime_type="image/png")
            with pytest.raises(AuthenticationError):
                await resource.upload_logo(team_id=12345, connector_identifier="my-connector", logo=logo_file)
        finally:
            cb_module.upload_connector_logo.asyncio = original
