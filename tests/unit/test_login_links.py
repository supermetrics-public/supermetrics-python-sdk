"""Unit tests for LoginLinksResource and LoginLinksAsyncResource."""

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.login_link import LoginLink
from supermetrics._generated.supermetrics_api_client.models.login_link_response import LoginLinkResponse
from supermetrics._generated.supermetrics_api_client.types import UNSET, Response
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.login_links import LoginLinksAsyncResource, LoginLinksResource


def _make_success_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=parsed)


def _make_error_response(status_code: HTTPStatus, parsed: object = None) -> Response:
    return Response(status_code=status_code, content=b"", headers={}, parsed=parsed)


class TestLoginLinksResource:
    """Test suite for LoginLinksResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def login_links_resource(self, mock_client: MagicMock) -> LoginLinksResource:
        """Create a LoginLinksResource instance with mock client."""
        return LoginLinksResource(mock_client)

    @pytest.fixture
    def sample_login_link(self) -> LoginLink:
        """Create a sample LoginLink for testing."""
        return LoginLink(
            link_id="link_123abc",
            status_code="OPEN",
            description="Test link",
            ds_id="GAWA",
            ds_name="Google Analytics 4",
            login_url="https://api.supermetrics.com/login/123",
            created_time=datetime.datetime.now(datetime.UTC),
            expiry_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
            login_id=UNSET,
            login_time=UNSET,
            login_username=UNSET,
        )

    def test_create_login_link_success(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test successful login link creation."""
        # Arrange
        mock_response_obj = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        link = login_links_resource.create(ds_id="GAWA", description="Test link")

        # Assert
        assert link.link_id == "link_123abc"
        assert link.ds_id == "GAWA"
        assert link.status_code == "OPEN"
        assert login_links_module.create_login_link.sync_detailed.called

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_create_login_link_with_expiry(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test login link creation with custom expiry time."""
        # Arrange
        custom_expiry = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=12)
        mock_response_obj = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        link = login_links_resource.create(ds_id="GAWA", description="Test", expiry_time=custom_expiry)

        # Assert
        assert link is not None
        assert login_links_module.create_login_link.sync_detailed.called

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_get_login_link_success(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test successful login link retrieval."""
        # Arrange
        mock_response_obj = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_get = login_links_module.get_login_link.sync_detailed
        login_links_module.get_login_link.sync_detailed = MagicMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        link = login_links_resource.get(link_id="link_123abc")

        # Assert
        assert link.link_id == "link_123abc"
        assert link.status_code == "OPEN"
        assert login_links_module.get_login_link.sync_detailed.called

        # Cleanup
        login_links_module.get_login_link.sync_detailed = original_get

    def test_list_login_links_success(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test successful listing of login links."""
        # Arrange
        from supermetrics._generated.supermetrics_api_client.models.list_login_links_response_200 import (
            ListLoginLinksResponse200,
        )

        link2 = LoginLink(
            link_id="link_456def",
            status_code="CLOSED",
            ds_id="facebook_ads",
            ds_name="Facebook Ads",
        )
        mock_response_obj = ListLoginLinksResponse200(data=[sample_login_link, link2])

        import supermetrics.resources.login_links as login_links_module

        original_list = login_links_module.list_login_links.sync_detailed
        login_links_module.list_login_links.sync_detailed = MagicMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        links = login_links_resource.list()

        # Assert
        assert len(links) == 2
        assert links[0].link_id == "link_123abc"
        assert links[1].link_id == "link_456def"
        assert login_links_module.list_login_links.sync_detailed.called

        # Cleanup
        login_links_module.list_login_links.sync_detailed = original_list

    def test_list_login_links_empty(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test listing when no login links exist."""
        # Arrange
        from supermetrics._generated.supermetrics_api_client.models.list_login_links_response_200 import (
            ListLoginLinksResponse200,
        )

        mock_response_obj = ListLoginLinksResponse200(data=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_list = login_links_module.list_login_links.sync_detailed
        login_links_module.list_login_links.sync_detailed = MagicMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        links = login_links_resource.list()

        # Assert
        assert links == []
        assert login_links_module.list_login_links.sync_detailed.called

        # Cleanup
        login_links_module.list_login_links.sync_detailed = original_list

    def test_close_login_link_success(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test successful login link closure."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_close = login_links_module.close_login_link.sync_detailed
        login_links_module.close_login_link.sync_detailed = MagicMock(return_value=_make_success_response(None))

        # Act
        result = login_links_resource.close(link_id="link_123abc")

        # Assert
        assert result is None
        assert login_links_module.close_login_link.sync_detailed.called

        # Cleanup
        login_links_module.close_login_link.sync_detailed = original_close

    def test_create_raises_on_empty_response(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock
    ) -> None:
        """Test that create raises on empty API response (parsed=None with status 200)."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(return_value=_make_success_response(None))

        # Act & Assert
        with pytest.raises((AttributeError, TypeError)):
            login_links_resource.create(ds_id="GAWA", description="Test")

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_get_raises_on_empty_response(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock
    ) -> None:
        """Test that get raises on empty API response (parsed=None with status 200)."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_get = login_links_module.get_login_link.sync_detailed
        login_links_module.get_login_link.sync_detailed = MagicMock(return_value=_make_success_response(None))

        # Act & Assert
        with pytest.raises((AttributeError, TypeError)):
            login_links_resource.get(link_id="link_123")

        # Cleanup
        login_links_module.get_login_link.sync_detailed = original_get

    def test_authentication_error_on_401(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock
    ) -> None:
        """Test 401 response raises AuthenticationError."""
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED)
        )

        # Verify AuthenticationError is raised
        with pytest.raises(AuthenticationError) as exc_info:
            login_links_resource.create(ds_id="GAWA", description="Test")

        assert exc_info.value.status_code == 401
        assert "Invalid or expired API key" in str(exc_info.value)

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_validation_error_on_400(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test 400 response raises ValidationError."""
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST)
        )

        # Verify ValidationError is raised
        with pytest.raises(ValidationError) as exc_info:
            login_links_resource.create(ds_id="GAWA", description="Test")

        assert exc_info.value.status_code == 400
        assert "Invalid" in str(exc_info.value)

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_api_error_on_404(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test 404 response raises APIError."""
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND)
        )

        # Verify APIError is raised
        with pytest.raises(APIError) as exc_info:
            login_links_resource.create(ds_id="GAWA", description="Test")

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_api_error_on_500(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test 500 response raises APIError."""
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        )

        # Verify APIError is raised
        with pytest.raises(APIError) as exc_info:
            login_links_resource.create(ds_id="GAWA", description="Test")

        assert exc_info.value.status_code == 500
        assert "Supermetrics API error" in str(exc_info.value) or "API error" in str(exc_info.value)

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create

    def test_network_error_on_timeout(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test network timeout raises NetworkError."""
        # Mock httpx.RequestError (not HTTPStatusError)
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/test"

        error = httpx.TimeoutException("Request timeout", request=mock_request)

        # Mock the API method to raise the error
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync_detailed
        login_links_module.create_login_link.sync_detailed = MagicMock(side_effect=error)

        # Verify NetworkError is raised
        with pytest.raises(NetworkError) as exc_info:
            login_links_resource.create(ds_id="GAWA", description="Test")

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None  # Network errors have no HTTP status

        # Cleanup
        login_links_module.create_login_link.sync_detailed = original_create


class TestLoginLinksAsyncResource:
    """Test suite for LoginLinksAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def login_links_async_resource(self, mock_client: MagicMock) -> LoginLinksAsyncResource:
        """Create a LoginLinksAsyncResource instance with mock client."""
        return LoginLinksAsyncResource(mock_client)

    @pytest.fixture
    def sample_login_link(self) -> LoginLink:
        """Create a sample LoginLink for testing."""
        return LoginLink(
            link_id="link_789xyz",
            status_code="OPEN",
            description="Async test link",
            ds_id="GAWA",
            ds_name="Google Analytics 4",
            login_url="https://api.supermetrics.com/login/789",
            created_time=datetime.datetime.now(datetime.UTC),
            expiry_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
        )

    @pytest.mark.asyncio
    async def test_create_login_link_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test async login link creation."""
        # Arrange
        mock_response_obj = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.asyncio_detailed
        login_links_module.create_login_link.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        link = await login_links_async_resource.create(ds_id="GAWA", description="Async test")

        # Assert
        assert link.link_id == "link_789xyz"
        assert link.ds_id == "GAWA"
        assert link.status_code == "OPEN"

        # Cleanup
        login_links_module.create_login_link.asyncio_detailed = original_create

    @pytest.mark.asyncio
    async def test_get_login_link_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test async login link retrieval."""
        # Arrange
        mock_response_obj = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_get = login_links_module.get_login_link.asyncio_detailed
        login_links_module.get_login_link.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        link = await login_links_async_resource.get(link_id="link_789xyz")

        # Assert
        assert link.link_id == "link_789xyz"
        assert link.status_code == "OPEN"

        # Cleanup
        login_links_module.get_login_link.asyncio_detailed = original_get

    @pytest.mark.asyncio
    async def test_list_login_links_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test async listing of login links."""
        # Arrange
        from supermetrics._generated.supermetrics_api_client.models.list_login_links_response_200 import (
            ListLoginLinksResponse200,
        )

        mock_response_obj = ListLoginLinksResponse200(data=[sample_login_link])

        import supermetrics.resources.login_links as login_links_module

        original_list = login_links_module.list_login_links.asyncio_detailed
        login_links_module.list_login_links.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(mock_response_obj)
        )

        # Act
        links = await login_links_async_resource.list()

        # Assert
        assert len(links) == 1
        assert links[0].link_id == "link_789xyz"

        # Cleanup
        login_links_module.list_login_links.asyncio_detailed = original_list

    @pytest.mark.asyncio
    async def test_close_login_link_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock
    ) -> None:
        """Test async login link closure."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_close = login_links_module.close_login_link.asyncio_detailed
        login_links_module.close_login_link.asyncio_detailed = AsyncMock(return_value=_make_success_response(None))

        # Act
        result = await login_links_async_resource.close(link_id="link_789xyz")

        # Assert
        assert result is None

        # Cleanup
        login_links_module.close_login_link.asyncio_detailed = original_close

    @pytest.mark.asyncio
    async def test_create_raises_on_empty_response_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock
    ) -> None:
        """Test that async create raises on empty API response (parsed=None with status 200)."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.asyncio_detailed
        login_links_module.create_login_link.asyncio_detailed = AsyncMock(return_value=_make_success_response(None))

        # Act & Assert
        with pytest.raises((AttributeError, TypeError)):
            await login_links_async_resource.create(ds_id="GAWA", description="Test")

        # Cleanup
        login_links_module.create_login_link.asyncio_detailed = original_create
