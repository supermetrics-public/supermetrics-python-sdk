"""Unit tests for ConnectorBuilderSecretsResource and ConnectorBuilderSecretsAsyncResource."""

from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.create_connector_secret_response_201 import (
    CreateConnectorSecretResponse201,
)
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.list_connector_secrets_response_200 import (
    ListConnectorSecretsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError
from supermetrics.resources.connector_builder_secrets import (
    ConnectorBuilderSecretsAsyncResource,
    ConnectorBuilderSecretsResource,
)


def _make_error_response(code: str, message: str) -> ErrorResponse:
    """Create an ErrorResponse with the given code and message."""
    return ErrorResponse(
        meta=ResponseMeta(request_id="req-id"),
        error=Error(code=code, message=message),
    )


class TestConnectorBuilderSecretsResource:
    """Test suite for ConnectorBuilderSecretsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> ConnectorBuilderSecretsResource:
        """Create a ConnectorBuilderSecretsResource instance with mock client."""
        return ConnectorBuilderSecretsResource(mock_client)

    # --- list() ---

    def test_list_success(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test successful listing of connector secrets."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        expected = ListConnectorSecretsResponse200(count=0, secrets=[])
        original = secrets_module.list_connector_secrets.sync
        secrets_module.list_connector_secrets.sync = MagicMock(return_value=expected)

        try:
            result = resource.list(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, ListConnectorSecretsResponse200)
            assert secrets_module.list_connector_secrets.sync.called
        finally:
            secrets_module.list_connector_secrets.sync = original

    def test_list_passes_correct_params(
        self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock
    ) -> None:
        """Test that list() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.sync
        mock_sync = MagicMock(return_value=ListConnectorSecretsResponse200(count=0, secrets=[]))
        secrets_module.list_connector_secrets.sync = mock_sync

        try:
            resource.list(team_id=99999, connector_identifier="test-conn")
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["connector_identifier"] == "test-conn"
        finally:
            secrets_module.list_connector_secrets.sync = original

    def test_list_auth_error_on_401(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that list() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.sync
        secrets_module.list_connector_secrets.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            secrets_module.list_connector_secrets.sync = original

    def test_list_api_error_on_error_response(
        self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock
    ) -> None:
        """Test that list() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.sync
        secrets_module.list_connector_secrets.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Connector not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.list(team_id=12345, connector_identifier="missing")
            assert "not found" in str(exc_info.value).lower()
        finally:
            secrets_module.list_connector_secrets.sync = original

    def test_list_network_error(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that list() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.sync
        secrets_module.list_connector_secrets.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.list(team_id=12345, connector_identifier="my-connector")
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            secrets_module.list_connector_secrets.sync = original

    # --- create() ---

    def test_create_success(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test successful secret creation."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        expected = CreateConnectorSecretResponse201(count=1, secrets=[])
        original = secrets_module.create_connector_secret.sync
        secrets_module.create_connector_secret.sync = MagicMock(return_value=expected)

        try:
            result = resource.create(
                team_id=12345,
                connector_identifier="my-connector",
                secret_name="API_KEY",
                secret_value="sk-abc123",
            )
            assert isinstance(result, CreateConnectorSecretResponse201)
            assert secrets_module.create_connector_secret.sync.called
        finally:
            secrets_module.create_connector_secret.sync = original

    def test_create_passes_correct_params(
        self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock
    ) -> None:
        """Test that create() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.sync
        mock_sync = MagicMock(return_value=CreateConnectorSecretResponse201(count=1, secrets=[]))
        secrets_module.create_connector_secret.sync = mock_sync

        try:
            resource.create(
                team_id=12345,
                connector_identifier="my-connector",
                secret_name="DB_PASSWORD",
                secret_value="s3cret",
            )
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["connector_identifier"] == "my-connector"
            assert call_kwargs["body"].secret_name == "DB_PASSWORD"
            assert call_kwargs["body"].secret_value == "s3cret"
        finally:
            secrets_module.create_connector_secret.sync = original

    def test_create_auth_error_on_401(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that create() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.sync
        secrets_module.create_connector_secret.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.create(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_name="KEY",
                    secret_value="val",
                )
        finally:
            secrets_module.create_connector_secret.sync = original

    def test_create_api_error_on_error_response(
        self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock
    ) -> None:
        """Test that create() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.sync
        secrets_module.create_connector_secret.sync = MagicMock(
            return_value=_make_error_response("CONFLICT", "Secret already exists")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.create(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_name="KEY",
                    secret_value="val",
                )
            assert "Secret already exists" in str(exc_info.value)
        finally:
            secrets_module.create_connector_secret.sync = original

    def test_create_api_error_on_500_http(
        self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock
    ) -> None:
        """Test that create() raises APIError on HTTP 500."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.HTTPStatusError("500", request=mock_request, response=mock_response)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.sync
        secrets_module.create_connector_secret.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(APIError) as exc_info:
                resource.create(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_name="KEY",
                    secret_value="val",
                )
            assert exc_info.value.status_code == 500
        finally:
            secrets_module.create_connector_secret.sync = original

    def test_create_network_error(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that create() raises NetworkError on network timeout."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.sync
        secrets_module.create_connector_secret.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.create(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_name="KEY",
                    secret_value="val",
                )
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            secrets_module.create_connector_secret.sync = original

    # --- update() ---

    def test_update_success(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test successful secret update (204 No Content)."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.sync
        secrets_module.update_connector_secret.sync = MagicMock(return_value=None)

        try:
            result = resource.update(
                team_id=12345,
                connector_identifier="my-connector",
                secret_placeholder="{{API_KEY}}",
                secret_value="sk-new-value",
            )
            assert result is None
            assert secrets_module.update_connector_secret.sync.called
        finally:
            secrets_module.update_connector_secret.sync = original

    def test_update_passes_correct_params(
        self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock
    ) -> None:
        """Test that update() passes correct parameters to the API."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.sync
        mock_sync = MagicMock(return_value=None)
        secrets_module.update_connector_secret.sync = mock_sync

        try:
            resource.update(
                team_id=12345,
                connector_identifier="my-connector",
                secret_placeholder="{{DB_PASS}}",
                secret_value="new-password",
            )
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["connector_identifier"] == "my-connector"
            assert call_kwargs["secret_placeholder"] == "{{DB_PASS}}"
            assert call_kwargs["body"].secret_value == "new-password"
        finally:
            secrets_module.update_connector_secret.sync = original

    def test_update_auth_error_on_401(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that update() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.sync
        secrets_module.update_connector_secret.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                    secret_value="val",
                )
        finally:
            secrets_module.update_connector_secret.sync = original

    def test_update_api_error_on_404(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that update() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.sync
        secrets_module.update_connector_secret.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Secret not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{MISSING}}",
                    secret_value="val",
                )
            assert "not found" in str(exc_info.value).lower()
        finally:
            secrets_module.update_connector_secret.sync = original

    def test_update_network_error(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that update() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.sync
        secrets_module.update_connector_secret.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                    secret_value="val",
                )
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            secrets_module.update_connector_secret.sync = original

    # --- delete() ---

    def test_delete_success(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test successful secret deletion (204 No Content)."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.sync
        secrets_module.delete_connector_secret.sync = MagicMock(return_value=None)

        try:
            result = resource.delete(
                team_id=12345,
                connector_identifier="my-connector",
                secret_placeholder="{{API_KEY}}",
            )
            assert result is None
            assert secrets_module.delete_connector_secret.sync.called
        finally:
            secrets_module.delete_connector_secret.sync = original

    def test_delete_auth_error_on_401(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that delete() raises AuthenticationError on 401 ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.sync
        secrets_module.delete_connector_secret.sync = MagicMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                resource.delete(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                )
        finally:
            secrets_module.delete_connector_secret.sync = original

    def test_delete_api_error_on_404(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that delete() raises APIError on 404 (ErrorResponse)."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.sync
        secrets_module.delete_connector_secret.sync = MagicMock(
            return_value=_make_error_response("NOT_FOUND", "Secret not found")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                resource.delete(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{MISSING}}",
                )
            assert "not found" in str(exc_info.value).lower()
        finally:
            secrets_module.delete_connector_secret.sync = original

    def test_delete_network_error(self, resource: ConnectorBuilderSecretsResource, mock_client: MagicMock) -> None:
        """Test that delete() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.sync
        secrets_module.delete_connector_secret.sync = MagicMock(side_effect=error)

        try:
            with pytest.raises(NetworkError) as exc_info:
                resource.delete(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                )
            assert "Network error" in str(exc_info.value)
            assert exc_info.value.status_code is None
        finally:
            secrets_module.delete_connector_secret.sync = original


class TestConnectorBuilderSecretsAsyncResource:
    """Test suite for ConnectorBuilderSecretsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> ConnectorBuilderSecretsAsyncResource:
        """Create a ConnectorBuilderSecretsAsyncResource instance with mock client."""
        return ConnectorBuilderSecretsAsyncResource(mock_client)

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test successful async listing of connector secrets."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        expected = ListConnectorSecretsResponse200(count=0, secrets=[])
        original = secrets_module.list_connector_secrets.asyncio
        secrets_module.list_connector_secrets.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.list(team_id=12345, connector_identifier="my-connector")
            assert isinstance(result, ListConnectorSecretsResponse200)
            assert secrets_module.list_connector_secrets.asyncio.called
        finally:
            secrets_module.list_connector_secrets.asyncio = original

    @pytest.mark.asyncio
    async def test_list_auth_error_on_401(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async list() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.asyncio
        secrets_module.list_connector_secrets.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            secrets_module.list_connector_secrets.asyncio = original

    @pytest.mark.asyncio
    async def test_list_api_error_on_error_response(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async list() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.asyncio
        secrets_module.list_connector_secrets.asyncio = AsyncMock(
            return_value=_make_error_response("INTERNAL_ERROR", "Internal server error")
        )

        try:
            with pytest.raises(APIError):
                await resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            secrets_module.list_connector_secrets.asyncio = original

    @pytest.mark.asyncio
    async def test_list_network_error(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async list() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.list_connector_secrets.asyncio
        secrets_module.list_connector_secrets.asyncio = AsyncMock(side_effect=error)

        try:
            with pytest.raises(NetworkError):
                await resource.list(team_id=12345, connector_identifier="my-connector")
        finally:
            secrets_module.list_connector_secrets.asyncio = original

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test successful async secret creation."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        expected = CreateConnectorSecretResponse201(count=1, secrets=[])
        original = secrets_module.create_connector_secret.asyncio
        secrets_module.create_connector_secret.asyncio = AsyncMock(return_value=expected)

        try:
            result = await resource.create(
                team_id=12345,
                connector_identifier="my-connector",
                secret_name="API_KEY",
                secret_value="sk-abc123",
            )
            assert isinstance(result, CreateConnectorSecretResponse201)
            assert secrets_module.create_connector_secret.asyncio.called
        finally:
            secrets_module.create_connector_secret.asyncio = original

    @pytest.mark.asyncio
    async def test_create_auth_error_on_401(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async create() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.asyncio
        secrets_module.create_connector_secret.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.create(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_name="KEY",
                    secret_value="val",
                )
        finally:
            secrets_module.create_connector_secret.asyncio = original

    @pytest.mark.asyncio
    async def test_create_api_error_on_error_response(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async create() raises APIError on generic ErrorResponse."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.create_connector_secret.asyncio
        secrets_module.create_connector_secret.asyncio = AsyncMock(
            return_value=_make_error_response("CONFLICT", "Secret already exists")
        )

        try:
            with pytest.raises(APIError):
                await resource.create(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_name="KEY",
                    secret_value="val",
                )
        finally:
            secrets_module.create_connector_secret.asyncio = original

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test successful async secret update (204 No Content)."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.asyncio
        secrets_module.update_connector_secret.asyncio = AsyncMock(return_value=None)

        try:
            result = await resource.update(
                team_id=12345,
                connector_identifier="my-connector",
                secret_placeholder="{{API_KEY}}",
                secret_value="sk-new",
            )
            assert result is None
            assert secrets_module.update_connector_secret.asyncio.called
        finally:
            secrets_module.update_connector_secret.asyncio = original

    @pytest.mark.asyncio
    async def test_update_auth_error_on_401(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async update() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.update_connector_secret.asyncio
        secrets_module.update_connector_secret.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.update(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                    secret_value="val",
                )
        finally:
            secrets_module.update_connector_secret.asyncio = original

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_success(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test successful async secret deletion (204 No Content)."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.asyncio
        secrets_module.delete_connector_secret.asyncio = AsyncMock(return_value=None)

        try:
            result = await resource.delete(
                team_id=12345,
                connector_identifier="my-connector",
                secret_placeholder="{{API_KEY}}",
            )
            assert result is None
            assert secrets_module.delete_connector_secret.asyncio.called
        finally:
            secrets_module.delete_connector_secret.asyncio = original

    @pytest.mark.asyncio
    async def test_delete_auth_error_on_401(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async delete() raises AuthenticationError on 401."""
        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.asyncio
        secrets_module.delete_connector_secret.asyncio = AsyncMock(
            return_value=_make_error_response("UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError):
                await resource.delete(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                )
        finally:
            secrets_module.delete_connector_secret.asyncio = original

    @pytest.mark.asyncio
    async def test_delete_network_error(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Test that async delete() raises NetworkError on network failure."""
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"
        error = httpx.TimeoutException("Request timeout", request=mock_request)

        import supermetrics.resources.connector_builder_secrets as secrets_module

        original = secrets_module.delete_connector_secret.asyncio
        secrets_module.delete_connector_secret.asyncio = AsyncMock(side_effect=error)

        try:
            with pytest.raises(NetworkError):
                await resource.delete(
                    team_id=12345,
                    connector_identifier="my-connector",
                    secret_placeholder="{{KEY}}",
                )
        finally:
            secrets_module.delete_connector_secret.asyncio = original
