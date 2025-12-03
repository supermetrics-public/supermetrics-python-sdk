"""Unit tests for LoginLinksResource and LoginLinksAsyncResource."""

import datetime
from unittest.mock import MagicMock

import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.login_link import LoginLink
from supermetrics._generated.supermetrics_api_client.models.login_link_response import LoginLinkResponse
from supermetrics._generated.supermetrics_api_client.models.login_link_status_code import LoginLinkStatusCode
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics.resources.login_links import LoginLinksAsyncResource, LoginLinksResource


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
            status_code=LoginLinkStatusCode.OPEN,
            description="Test link",
            ds_id="GA4",
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
        mock_response = LoginLinkResponse(data=sample_login_link, meta=UNSET)
        mock_client.get_httpx_client().request.return_value.json.return_value = mock_response.to_dict()

        # Mock the generated API function
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync
        login_links_module.create_login_link.sync = MagicMock(return_value=mock_response)

        # Act
        link = login_links_resource.create(ds_id="GA4", description="Test link")

        # Assert
        assert link.link_id == "link_123abc"
        assert link.ds_id == "GA4"
        assert link.status_code == LoginLinkStatusCode.OPEN
        assert login_links_module.create_login_link.sync.called

        # Cleanup
        login_links_module.create_login_link.sync = original_create

    def test_create_login_link_with_expiry(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test login link creation with custom expiry time."""
        # Arrange
        custom_expiry = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=12)
        mock_response = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync
        login_links_module.create_login_link.sync = MagicMock(return_value=mock_response)

        # Act
        link = login_links_resource.create(ds_id="GA4", description="Test", expiry_time=custom_expiry)

        # Assert
        assert link is not None
        assert login_links_module.create_login_link.sync.called

        # Cleanup
        login_links_module.create_login_link.sync = original_create

    def test_get_login_link_success(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test successful login link retrieval."""
        # Arrange
        mock_response = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_get = login_links_module.get_login_link.sync
        login_links_module.get_login_link.sync = MagicMock(return_value=mock_response)

        # Act
        link = login_links_resource.get(link_id="link_123abc")

        # Assert
        assert link.link_id == "link_123abc"
        assert link.status_code == LoginLinkStatusCode.OPEN
        assert login_links_module.get_login_link.sync.called

        # Cleanup
        login_links_module.get_login_link.sync = original_get

    def test_list_login_links_success(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test successful listing of login links."""
        # Arrange
        link2 = LoginLink(
            link_id="link_456def",
            status_code=LoginLinkStatusCode.CLOSED,
            ds_id="facebook_ads",
            ds_name="Facebook Ads",
        )
        mock_response = MagicMock()
        mock_response.data = [sample_login_link, link2]

        import supermetrics.resources.login_links as login_links_module

        original_list = login_links_module.list_login_links.sync
        login_links_module.list_login_links.sync = MagicMock(return_value=mock_response)

        # Act
        links = login_links_resource.list()

        # Assert
        assert len(links) == 2
        assert links[0].link_id == "link_123abc"
        assert links[1].link_id == "link_456def"
        assert login_links_module.list_login_links.sync.called

        # Cleanup
        login_links_module.list_login_links.sync = original_list

    def test_list_login_links_empty(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test listing when no login links exist."""
        # Arrange
        mock_response = MagicMock()
        mock_response.data = UNSET

        import supermetrics.resources.login_links as login_links_module

        original_list = login_links_module.list_login_links.sync
        login_links_module.list_login_links.sync = MagicMock(return_value=mock_response)

        # Act
        links = login_links_resource.list()

        # Assert
        assert links == []
        assert login_links_module.list_login_links.sync.called

        # Cleanup
        login_links_module.list_login_links.sync = original_list

    def test_close_login_link_success(self, login_links_resource: LoginLinksResource, mock_client: MagicMock) -> None:
        """Test successful login link closure."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_close = login_links_module.close_login_link.sync
        login_links_module.close_login_link.sync = MagicMock(return_value=None)

        # Act
        result = login_links_resource.close(link_id="link_123abc")

        # Assert
        assert result is None
        assert login_links_module.close_login_link.sync.called

        # Cleanup
        login_links_module.close_login_link.sync = original_close

    def test_create_raises_on_empty_response(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock
    ) -> None:
        """Test that create raises ValueError on empty API response."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.sync
        login_links_module.create_login_link.sync = MagicMock(return_value=None)

        # Act & Assert
        with pytest.raises(ValueError, match="API returned empty response"):
            login_links_resource.create(ds_id="GA4", description="Test")

        # Cleanup
        login_links_module.create_login_link.sync = original_create

    def test_get_raises_on_empty_response(
        self, login_links_resource: LoginLinksResource, mock_client: MagicMock
    ) -> None:
        """Test that get raises ValueError on empty API response."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_get = login_links_module.get_login_link.sync
        login_links_module.get_login_link.sync = MagicMock(return_value=None)

        # Act & Assert
        with pytest.raises(ValueError, match="API returned empty response"):
            login_links_resource.get(link_id="link_123")

        # Cleanup
        login_links_module.get_login_link.sync = original_get


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
            status_code=LoginLinkStatusCode.OPEN,
            description="Async test link",
            ds_id="GA4",
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
        mock_response = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.asyncio

        async def mock_create(*args: object, **kwargs: object) -> LoginLinkResponse:
            return mock_response

        login_links_module.create_login_link.asyncio = mock_create

        # Act
        link = await login_links_async_resource.create(ds_id="GA4", description="Async test")

        # Assert
        assert link.link_id == "link_789xyz"
        assert link.ds_id == "GA4"
        assert link.status_code == LoginLinkStatusCode.OPEN

        # Cleanup
        login_links_module.create_login_link.asyncio = original_create

    @pytest.mark.asyncio
    async def test_get_login_link_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test async login link retrieval."""
        # Arrange
        mock_response = LoginLinkResponse(data=sample_login_link, meta=UNSET)

        import supermetrics.resources.login_links as login_links_module

        original_get = login_links_module.get_login_link.asyncio

        async def mock_get(*args: object, **kwargs: object) -> LoginLinkResponse:
            return mock_response

        login_links_module.get_login_link.asyncio = mock_get

        # Act
        link = await login_links_async_resource.get(link_id="link_789xyz")

        # Assert
        assert link.link_id == "link_789xyz"
        assert link.status_code == LoginLinkStatusCode.OPEN

        # Cleanup
        login_links_module.get_login_link.asyncio = original_get

    @pytest.mark.asyncio
    async def test_list_login_links_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock, sample_login_link: LoginLink
    ) -> None:
        """Test async listing of login links."""
        # Arrange
        mock_response = MagicMock()
        mock_response.data = [sample_login_link]

        import supermetrics.resources.login_links as login_links_module

        original_list = login_links_module.list_login_links.asyncio

        async def mock_list(*args: object, **kwargs: object) -> MagicMock:
            return mock_response

        login_links_module.list_login_links.asyncio = mock_list

        # Act
        links = await login_links_async_resource.list()

        # Assert
        assert len(links) == 1
        assert links[0].link_id == "link_789xyz"

        # Cleanup
        login_links_module.list_login_links.asyncio = original_list

    @pytest.mark.asyncio
    async def test_close_login_link_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock
    ) -> None:
        """Test async login link closure."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_close = login_links_module.close_login_link.asyncio

        async def mock_close(*args: object, **kwargs: object) -> None:
            return None

        login_links_module.close_login_link.asyncio = mock_close

        # Act
        result = await login_links_async_resource.close(link_id="link_789xyz")

        # Assert
        assert result is None

        # Cleanup
        login_links_module.close_login_link.asyncio = original_close

    @pytest.mark.asyncio
    async def test_create_raises_on_empty_response_async(
        self, login_links_async_resource: LoginLinksAsyncResource, mock_client: MagicMock
    ) -> None:
        """Test that async create raises ValueError on empty API response."""
        # Arrange
        import supermetrics.resources.login_links as login_links_module

        original_create = login_links_module.create_login_link.asyncio

        async def mock_create(*args: object, **kwargs: object) -> None:
            return None

        login_links_module.create_login_link.asyncio = mock_create

        # Act & Assert
        with pytest.raises(ValueError, match="API returned empty response"):
            await login_links_async_resource.create(ds_id="GA4", description="Test")

        # Cleanup
        login_links_module.create_login_link.asyncio = original_create
