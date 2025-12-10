"""Unit tests for AccountsResource and AccountsAsyncResource."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200 import GetAccountsResponse200
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200_data_item import (
    GetAccountsResponse200DataItem,
)
from supermetrics._generated.supermetrics_api_client.models.get_accounts_response_200_data_item_accounts_item import (
    GetAccountsResponse200DataItemAccountsItem,
)
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics.resources.accounts import AccountsAsyncResource, AccountsResource


class TestAccountsResource:
    """Test suite for AccountsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def accounts_resource(self, mock_client: MagicMock) -> AccountsResource:
        """Create an AccountsResource instance with mock client."""
        return AccountsResource(mock_client)

    @pytest.fixture
    def sample_account1(self) -> GetAccountsResponse200DataItemAccountsItem:
        """Create a sample account for testing."""
        return GetAccountsResponse200DataItemAccountsItem(
            account_id="acc_123",
            account_name="Account 123",
            group_name="Group A",
        )

    @pytest.fixture
    def sample_account2(self) -> GetAccountsResponse200DataItemAccountsItem:
        """Create another sample account for testing."""
        return GetAccountsResponse200DataItemAccountsItem(
            account_id="acc_456",
            account_name="Account 456",
            group_name="Group B",
        )

    @pytest.fixture
    def sample_account3(self) -> GetAccountsResponse200DataItemAccountsItem:
        """Create a third sample account for testing."""
        return GetAccountsResponse200DataItemAccountsItem(
            account_id="acc_789",
            account_name="Account 789",
            group_name="",
        )

    @pytest.fixture
    def sample_account4(self) -> GetAccountsResponse200DataItemAccountsItem:
        """Create a fourth sample account for testing."""
        return GetAccountsResponse200DataItemAccountsItem(
            account_id="acc_999",
            account_name="Account 999",
            group_name="Group A",
        )

    def test_list_without_filters_flattens_accounts(
        self,
        accounts_resource: AccountsResource,
        mock_client: MagicMock,
        sample_account1: GetAccountsResponse200DataItemAccountsItem,
        sample_account2: GetAccountsResponse200DataItemAccountsItem,
        sample_account3: GetAccountsResponse200DataItemAccountsItem,
        sample_account4: GetAccountsResponse200DataItemAccountsItem,
    ) -> None:
        """Test list() without filters flattens nested account structure."""
        # Arrange: 2 data items, each with 2 accounts = 4 total accounts
        data_item1 = GetAccountsResponse200DataItem(
            ds_user="user1@example.com",
            display_name="User One",
            accounts=[sample_account1, sample_account2],
        )
        data_item2 = GetAccountsResponse200DataItem(
            ds_user="user2@example.com",
            display_name="User Two",
            accounts=[sample_account3, sample_account4],
        )
        mock_response = GetAccountsResponse200(data=[data_item1, data_item2], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        accounts_module.get_accounts.sync = MagicMock(return_value=mock_response)

        # Act
        accounts = accounts_resource.list(ds_id="GA4")

        # Assert
        assert len(accounts) == 4
        assert accounts[0].account_id == "acc_123"
        assert accounts[1].account_id == "acc_456"
        assert accounts[2].account_id == "acc_789"
        assert accounts[3].account_id == "acc_999"
        assert accounts_module.get_accounts.sync.called

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts

    def test_list_with_single_login_username_filter(
        self,
        accounts_resource: AccountsResource,
        mock_client: MagicMock,
        sample_account1: GetAccountsResponse200DataItemAccountsItem,
    ) -> None:
        """Test list() with single login username filter."""
        # Arrange
        data_item = GetAccountsResponse200DataItem(
            ds_user="user1@example.com",
            display_name="User One",
            accounts=[sample_account1],
        )
        mock_response = GetAccountsResponse200(data=[data_item], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        mock_sync = MagicMock(return_value=mock_response)
        accounts_module.get_accounts.sync = mock_sync

        # Act
        accounts = accounts_resource.list(ds_id="GA4", login_usernames="user1@example.com")

        # Assert
        assert len(accounts) == 1
        assert accounts[0].account_id == "acc_123"

        # Verify the GetAccountsJson was created with correct ds_users parameter
        call_args = mock_sync.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.ds_id == "GA4"
        assert json_param.ds_users == "user1@example.com"

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts

    def test_list_with_multiple_login_usernames(
        self,
        accounts_resource: AccountsResource,
        mock_client: MagicMock,
        sample_account1: GetAccountsResponse200DataItemAccountsItem,
        sample_account2: GetAccountsResponse200DataItemAccountsItem,
    ) -> None:
        """Test list() with list of login usernames."""
        # Arrange
        data_item1 = GetAccountsResponse200DataItem(
            ds_user="user1@example.com",
            accounts=[sample_account1],
        )
        data_item2 = GetAccountsResponse200DataItem(
            ds_user="user2@example.com",
            accounts=[sample_account2],
        )
        mock_response = GetAccountsResponse200(data=[data_item1, data_item2], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        mock_sync = MagicMock(return_value=mock_response)
        accounts_module.get_accounts.sync = mock_sync

        # Act
        accounts = accounts_resource.list(
            ds_id="GA4", login_usernames=["user1@example.com", "user2@example.com"]
        )

        # Assert
        assert len(accounts) == 2

        # Verify list of usernames passed correctly
        call_args = mock_sync.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.ds_users == ["user1@example.com", "user2@example.com"]

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts

    def test_list_with_cache_minutes(
        self,
        accounts_resource: AccountsResource,
        mock_client: MagicMock,
        sample_account1: GetAccountsResponse200DataItemAccountsItem,
    ) -> None:
        """Test list() with cache_minutes parameter."""
        # Arrange
        data_item = GetAccountsResponse200DataItem(accounts=[sample_account1])
        mock_response = GetAccountsResponse200(data=[data_item], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        mock_sync = MagicMock(return_value=mock_response)
        accounts_module.get_accounts.sync = mock_sync

        # Act
        accounts = accounts_resource.list(ds_id="GA4", cache_minutes=30)

        # Assert
        assert len(accounts) == 1

        # Verify cache_minutes passed correctly
        call_args = mock_sync.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.cache_minutes == 30

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts

    def test_list_with_empty_response(
        self, accounts_resource: AccountsResource, mock_client: MagicMock
    ) -> None:
        """Test list() with empty response returns empty list."""
        # Arrange
        mock_response = GetAccountsResponse200(data=[], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        accounts_module.get_accounts.sync = MagicMock(return_value=mock_response)

        # Act
        accounts = accounts_resource.list(ds_id="GA4")

        # Assert
        assert accounts == []

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts

    def test_list_with_data_items_but_empty_accounts(
        self, accounts_resource: AccountsResource, mock_client: MagicMock
    ) -> None:
        """Test list() with data items but empty accounts lists."""
        # Arrange
        data_item1 = GetAccountsResponse200DataItem(
            ds_user="user1@example.com",
            accounts=[],
        )
        data_item2 = GetAccountsResponse200DataItem(
            ds_user="user2@example.com",
            accounts=[],
        )
        mock_response = GetAccountsResponse200(data=[data_item1, data_item2], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        accounts_module.get_accounts.sync = MagicMock(return_value=mock_response)

        # Act
        accounts = accounts_resource.list(ds_id="GA4")

        # Assert
        assert accounts == []

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts

    def test_list_with_none_response(
        self, accounts_resource: AccountsResource, mock_client: MagicMock
    ) -> None:
        """Test list() with None response returns empty list."""
        # Arrange
        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.sync
        accounts_module.get_accounts.sync = MagicMock(return_value=None)

        # Act
        accounts = accounts_resource.list(ds_id="GA4")

        # Assert
        assert accounts == []

        # Cleanup
        accounts_module.get_accounts.sync = original_get_accounts


class TestAccountsAsyncResource:
    """Test suite for AccountsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def accounts_async_resource(self, mock_client: MagicMock) -> AccountsAsyncResource:
        """Create an AccountsAsyncResource instance with mock client."""
        return AccountsAsyncResource(mock_client)

    @pytest.fixture
    def sample_account1(self) -> GetAccountsResponse200DataItemAccountsItem:
        """Create a sample account for testing."""
        return GetAccountsResponse200DataItemAccountsItem(
            account_id="acc_123",
            account_name="Account 123",
            group_name="Group A",
        )

    @pytest.fixture
    def sample_account2(self) -> GetAccountsResponse200DataItemAccountsItem:
        """Create another sample account for testing."""
        return GetAccountsResponse200DataItemAccountsItem(
            account_id="acc_456",
            account_name="Account 456",
            group_name="Group B",
        )

    @pytest.mark.asyncio
    async def test_list_async_flattens_accounts(
        self,
        accounts_async_resource: AccountsAsyncResource,
        mock_client: MagicMock,
        sample_account1: GetAccountsResponse200DataItemAccountsItem,
        sample_account2: GetAccountsResponse200DataItemAccountsItem,
    ) -> None:
        """Test async list() method flattens accounts."""
        # Arrange
        data_item = GetAccountsResponse200DataItem(
            ds_user="user1@example.com",
            accounts=[sample_account1, sample_account2],
        )
        mock_response = GetAccountsResponse200(data=[data_item], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.asyncio
        accounts_module.get_accounts.asyncio = AsyncMock(return_value=mock_response)

        # Act
        accounts = await accounts_async_resource.list(ds_id="GA4")

        # Assert
        assert len(accounts) == 2
        assert accounts[0].account_id == "acc_123"
        assert accounts[1].account_id == "acc_456"
        assert accounts_module.get_accounts.asyncio.called

        # Cleanup
        accounts_module.get_accounts.asyncio = original_get_accounts

    @pytest.mark.asyncio
    async def test_list_async_with_filters(
        self,
        accounts_async_resource: AccountsAsyncResource,
        mock_client: MagicMock,
        sample_account1: GetAccountsResponse200DataItemAccountsItem,
    ) -> None:
        """Test async list() with filters."""
        # Arrange
        data_item = GetAccountsResponse200DataItem(
            ds_user="user1@example.com",
            accounts=[sample_account1],
        )
        mock_response = GetAccountsResponse200(data=[data_item], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.asyncio
        mock_asyncio = AsyncMock(return_value=mock_response)
        accounts_module.get_accounts.asyncio = mock_asyncio

        # Act
        accounts = await accounts_async_resource.list(
            ds_id="GA4", login_usernames=["user1@example.com"], cache_minutes=60
        )

        # Assert
        assert len(accounts) == 1

        # Verify parameters passed correctly
        call_args = mock_asyncio.call_args
        json_param = call_args.kwargs["json"]
        assert json_param.ds_id == "GA4"
        assert json_param.ds_users == ["user1@example.com"]
        assert json_param.cache_minutes == 60

        # Cleanup
        accounts_module.get_accounts.asyncio = original_get_accounts

    @pytest.mark.asyncio
    async def test_list_async_with_empty_response(
        self, accounts_async_resource: AccountsAsyncResource, mock_client: MagicMock
    ) -> None:
        """Test async list() with empty response."""
        # Arrange
        mock_response = GetAccountsResponse200(data=[], meta=UNSET)

        import supermetrics.resources.accounts as accounts_module

        original_get_accounts = accounts_module.get_accounts.asyncio
        accounts_module.get_accounts.asyncio = AsyncMock(return_value=mock_response)

        # Act
        accounts = await accounts_async_resource.list(ds_id="GA4")

        # Assert
        assert accounts == []

        # Cleanup
        accounts_module.get_accounts.asyncio = original_get_accounts
