"""Unit tests for LoginsResource and LoginsAsyncResource."""

import datetime
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.data_source import DataSource
from supermetrics._generated.supermetrics_api_client.models.data_source_login import DataSourceLogin
from supermetrics._generated.supermetrics_api_client.models.data_source_login_type import DataSourceLoginType
from supermetrics._generated.supermetrics_api_client.models.get_data_source_login_response_200 import (
    GetDataSourceLoginResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.list_data_source_logins_response_200 import (
    ListDataSourceLoginsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.user import User
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.logins import LoginsAsyncResource, LoginsResource


class TestLoginsResource:
    """Test suite for LoginsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def logins_resource(self, mock_client: MagicMock) -> LoginsResource:
        """Create a LoginsResource instance with mock client."""
        return LoginsResource(mock_client)

    @pytest.fixture
    def sample_data_source(self) -> DataSource:
        """Create a sample DataSource for testing."""
        return DataSource(
            type_=UNSET,
            ds_id="GAWA",
            name="Google Analytics 4",
        )

    @pytest.fixture
    def sample_user(self) -> User:
        """Create a sample User for testing."""
        return User(
            type_=UNSET,
            user_id="user_123",
            email="user@example.com",
        )

    @pytest.fixture
    def sample_login(self, sample_data_source: DataSource, sample_user: User) -> DataSourceLogin:
        """Create a sample DataSourceLogin for testing."""
        return DataSourceLogin(
            type_=DataSourceLoginType.DS_LOGIN,
            login_id="login_abc123",
            login_type="oauth2",
            username="user@example.com",
            display_name="User Example",
            ds_info=sample_data_source,
            default_scopes=["read_data"],
            additional_scopes=["write_data"],
            auth_time=datetime.datetime.now(datetime.UTC),
            auth_user_info=sample_user,
            expiry_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30),
            revoked_time=None,
            is_refreshable=True,
            is_shared=False,
        )

    def test_get_login_success(
        self, logins_resource: LoginsResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test successful login retrieval by login ID."""
        # Arrange
        mock_response = GetDataSourceLoginResponse200(data=sample_login, meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(return_value=mock_response)

        # Act
        login = logins_resource.get("login_abc123")

        # Assert
        assert login.login_id == "login_abc123"
        assert login.username == "user@example.com"
        assert login.ds_info.ds_id == "GAWA"
        assert logins_module.get_data_source_login.sync.called

        # Cleanup
        logins_module.get_data_source_login.sync = original_get

    def test_get_login_empty_response(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
        """Test get() with empty response raises ValueError."""
        # Arrange
        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(return_value=None)

        # Act & Assert
        with pytest.raises(ValueError, match="API returned empty response"):
            logins_resource.get("login_123")

        # Cleanup
        logins_module.get_data_source_login.sync = original_get

    def test_list_logins_success(
        self, logins_resource: LoginsResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test successful listing of all logins."""
        # Arrange
        login2 = DataSourceLogin(
            login_id="login_xyz789",
            username="another@example.com",
            ds_info=sample_login.ds_info,
            login_type="api_key",
        )
        mock_response = ListDataSourceLoginsResponse200(data=[sample_login, login2], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.sync
        logins_module.list_data_source_logins.sync = MagicMock(return_value=mock_response)

        # Act
        logins = logins_resource.list()

        # Assert
        assert len(logins) == 2
        assert logins[0].login_id == "login_abc123"
        assert logins[1].login_id == "login_xyz789"
        assert logins_module.list_data_source_logins.sync.called

        # Cleanup
        logins_module.list_data_source_logins.sync = original_list

    def test_list_logins_empty_list(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
        """Test list() with empty list returns empty list."""
        # Arrange
        mock_response = ListDataSourceLoginsResponse200(data=[], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.sync
        logins_module.list_data_source_logins.sync = MagicMock(return_value=mock_response)

        # Act
        logins = logins_resource.list()

        # Assert
        assert logins == []
        assert logins_module.list_data_source_logins.sync.called

        # Cleanup
        logins_module.list_data_source_logins.sync = original_list

    def test_get_by_username_success(
        self, logins_resource: LoginsResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test successful login retrieval by username."""
        # Arrange
        login2 = DataSourceLogin(
            login_id="login_xyz789",
            username="another@example.com",
            ds_info=sample_login.ds_info,
        )
        mock_response = ListDataSourceLoginsResponse200(data=[sample_login, login2], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.sync
        logins_module.list_data_source_logins.sync = MagicMock(return_value=mock_response)

        # Act
        login = logins_resource.get_by_username("user@example.com")

        # Assert
        assert login.login_id == "login_abc123"
        assert login.username == "user@example.com"
        assert logins_module.list_data_source_logins.sync.called

        # Cleanup
        logins_module.list_data_source_logins.sync = original_list

    def test_get_by_username_not_found(
        self, logins_resource: LoginsResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test get_by_username() raises ValueError when username not found."""
        # Arrange
        mock_response = ListDataSourceLoginsResponse200(data=[sample_login], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.sync
        logins_module.list_data_source_logins.sync = MagicMock(return_value=mock_response)

        # Act & Assert
        with pytest.raises(ValueError, match="No login found with username: notfound@example.com"):
            logins_resource.get_by_username("notfound@example.com")

        # Cleanup
        logins_module.list_data_source_logins.sync = original_list

    def test_authentication_error_on_401(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
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
        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(side_effect=error)

        # Verify AuthenticationError is raised
        with pytest.raises(AuthenticationError) as exc_info:
            logins_resource.get("login_123")

        assert exc_info.value.status_code == 401
        assert "Invalid or expired API key" in str(exc_info.value)

        # Cleanup
        logins_module.get_data_source_login.sync = original_get

    def test_validation_error_on_400(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
        """Test 400 response raises ValidationError."""
        # Mock httpx to raise HTTPStatusError with 400
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request: Invalid parameter"

        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.HTTPStatusError(
            "400 Bad Request",
            request=mock_request,
            response=mock_response
        )

        # Mock the API method to raise the error
        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(side_effect=error)

        # Verify ValidationError is raised
        with pytest.raises(ValidationError) as exc_info:
            logins_resource.get("login_123")

        assert exc_info.value.status_code == 400
        assert "Invalid parameter" in str(exc_info.value)

        # Cleanup
        logins_module.get_data_source_login.sync = original_get

    def test_api_error_on_404(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
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
        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(side_effect=error)

        # Verify APIError is raised
        with pytest.raises(APIError) as exc_info:
            logins_resource.get("login_123")

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        # Cleanup
        logins_module.get_data_source_login.sync = original_get

    def test_api_error_on_500(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
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
        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(side_effect=error)

        # Verify APIError is raised
        with pytest.raises(APIError) as exc_info:
            logins_resource.get("login_123")

        assert exc_info.value.status_code == 500
        assert "Supermetrics API error" in str(exc_info.value)

        # Cleanup
        logins_module.get_data_source_login.sync = original_get

    def test_network_error_on_timeout(self, logins_resource: LoginsResource, mock_client: MagicMock) -> None:
        """Test network timeout raises NetworkError."""
        # Mock httpx.RequestError (not HTTPStatusError)
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.TimeoutException("Request timeout", request=mock_request)

        # Mock the API method to raise the error
        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.sync
        logins_module.get_data_source_login.sync = MagicMock(side_effect=error)

        # Verify NetworkError is raised
        with pytest.raises(NetworkError) as exc_info:
            logins_resource.get("login_123")

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None  # Network errors have no HTTP status

        # Cleanup
        logins_module.get_data_source_login.sync = original_get


class TestLoginsAsyncResource:
    """Test suite for LoginsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def logins_async_resource(self, mock_client: MagicMock) -> LoginsAsyncResource:
        """Create a LoginsAsyncResource instance with mock client."""
        return LoginsAsyncResource(mock_client)

    @pytest.fixture
    def sample_data_source(self) -> DataSource:
        """Create a sample DataSource for testing."""
        return DataSource(
            type_=UNSET,
            ds_id="GAWA",
            name="Google Analytics 4",
        )

    @pytest.fixture
    def sample_user(self) -> User:
        """Create a sample User for testing."""
        return User(
            type_=UNSET,
            user_id="user_123",
            email="user@example.com",
        )

    @pytest.fixture
    def sample_login(self, sample_data_source: DataSource, sample_user: User) -> DataSourceLogin:
        """Create a sample DataSourceLogin for testing."""
        return DataSourceLogin(
            type_=DataSourceLoginType.DS_LOGIN,
            login_id="login_abc123",
            login_type="oauth2",
            username="user@example.com",
            display_name="User Example",
            ds_info=sample_data_source,
            default_scopes=["read_data"],
            additional_scopes=["write_data"],
            auth_time=datetime.datetime.now(datetime.UTC),
            auth_user_info=sample_user,
            expiry_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30),
            revoked_time=None,
            is_refreshable=True,
            is_shared=False,
        )

    @pytest.mark.asyncio
    async def test_get_login_async(
        self, logins_async_resource: LoginsAsyncResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test async login retrieval by login ID."""
        # Arrange
        mock_response = GetDataSourceLoginResponse200(data=sample_login, meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_get = logins_module.get_data_source_login.asyncio
        logins_module.get_data_source_login.asyncio = AsyncMock(return_value=mock_response)

        # Act
        login = await logins_async_resource.get("login_abc123")

        # Assert
        assert login.login_id == "login_abc123"
        assert login.username == "user@example.com"
        assert logins_module.get_data_source_login.asyncio.called

        # Cleanup
        logins_module.get_data_source_login.asyncio = original_get

    @pytest.mark.asyncio
    async def test_list_logins_async(
        self, logins_async_resource: LoginsAsyncResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test async listing of all logins."""
        # Arrange
        login2 = DataSourceLogin(
            login_id="login_xyz789",
            username="another@example.com",
            ds_info=sample_login.ds_info,
        )
        mock_response = ListDataSourceLoginsResponse200(data=[sample_login, login2], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.asyncio
        logins_module.list_data_source_logins.asyncio = AsyncMock(return_value=mock_response)

        # Act
        logins = await logins_async_resource.list()

        # Assert
        assert len(logins) == 2
        assert logins[0].login_id == "login_abc123"
        assert logins_module.list_data_source_logins.asyncio.called

        # Cleanup
        logins_module.list_data_source_logins.asyncio = original_list

    @pytest.mark.asyncio
    async def test_get_by_username_async(
        self, logins_async_resource: LoginsAsyncResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test async login retrieval by username."""
        # Arrange
        login2 = DataSourceLogin(
            login_id="login_xyz789",
            username="another@example.com",
            ds_info=sample_login.ds_info,
        )
        mock_response = ListDataSourceLoginsResponse200(data=[sample_login, login2], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.asyncio
        logins_module.list_data_source_logins.asyncio = AsyncMock(return_value=mock_response)

        # Act
        login = await logins_async_resource.get_by_username("user@example.com")

        # Assert
        assert login.login_id == "login_abc123"
        assert login.username == "user@example.com"
        assert logins_module.list_data_source_logins.asyncio.called

        # Cleanup
        logins_module.list_data_source_logins.asyncio = original_list

    @pytest.mark.asyncio
    async def test_get_by_username_not_found_async(
        self, logins_async_resource: LoginsAsyncResource, mock_client: MagicMock, sample_login: DataSourceLogin
    ) -> None:
        """Test async get_by_username() raises ValueError when username not found."""
        # Arrange
        mock_response = ListDataSourceLoginsResponse200(data=[sample_login], meta=UNSET)

        import supermetrics.resources.logins as logins_module

        original_list = logins_module.list_data_source_logins.asyncio
        logins_module.list_data_source_logins.asyncio = AsyncMock(return_value=mock_response)

        # Act & Assert
        with pytest.raises(ValueError, match="No login found with username: notfound@example.com"):
            await logins_async_resource.get_by_username("notfound@example.com")

        # Cleanup
        logins_module.list_data_source_logins.asyncio = original_list
