"""Unit tests for AccountTagsResource and AccountTagsAsyncResource.

These mock at the generated-client boundary and open no socket. Every patch goes
through ``monkeypatch.setattr`` rather than the save-and-restore-by-hand idiom used
elsewhere in this directory: a bare trailing restore statement is skipped when an
assertion fails, which leaks the mock into every later test in the session.
``monkeypatch`` unwinds on failure too, so a red test stays a single red test.

Error taxonomy is covered here only far enough to prove that a non-200 is raised
rather than returned; ``tests/e2e/test_account_tags_errors_e2e.py`` exercises it in
depth over a real socket.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.account_tag import AccountTag
from supermetrics._generated.supermetrics_api_client.models.account_tag_data_sources_item import (
    AccountTagDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.account_tag_list_response import AccountTagListResponse
from supermetrics._generated.supermetrics_api_client.models.account_tag_list_response_data import (
    AccountTagListResponseData,
)
from supermetrics._generated.supermetrics_api_client.models.account_tag_overview import AccountTagOverview
from supermetrics._generated.supermetrics_api_client.models.account_tag_response import AccountTagResponse
from supermetrics._generated.supermetrics_api_client.models.append_accounts_to_group_body import (
    AppendAccountsToGroupBody,
)
from supermetrics._generated.supermetrics_api_client.models.append_accounts_to_group_body_data_sources_item import (
    AppendAccountsToGroupBodyDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.create_account_group_body import CreateAccountGroupBody
from supermetrics._generated.supermetrics_api_client.models.create_account_group_body_data_sources_item import (
    CreateAccountGroupBodyDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.delete_account_group_response_200 import (
    DeleteAccountGroupResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.delete_account_group_response_200_data import (
    DeleteAccountGroupResponse200Data,
)
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.error_response_meta import ErrorResponseMeta
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.remove_accounts_from_group_body import (
    RemoveAccountsFromGroupBody,
)
from supermetrics._generated.supermetrics_api_client.models.remove_accounts_from_group_body_data_sources_item import (
    RemoveAccountsFromGroupBodyDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.update_account_group_body import UpdateAccountGroupBody
from supermetrics._generated.supermetrics_api_client.types import UNSET, Response
from supermetrics.exceptions import (
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)
from supermetrics.resources import account_tags as module
from supermetrics.resources.account_tags import AccountTagsAsyncResource, AccountTagsResource

TEAM_ID = 936506
TAG_NAME = "a1b2c3d"

#: The documented element shape for ``data_sources``. Upstream declares the array items
#: as a bare ``type: object``, so this shape lives only in the spec's example and the
#: SDK enforces nothing about it.
DATA_SOURCES: list[dict[str, Any]] = [
    {"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]},
    {"data_source_id": "FB", "accounts": [{"account_id": "act_99"}, {"account_id": "act_100"}]},
]

#: Every documented failure status for this domain, paired with the upstream error code
#: and the SDK exception it must become. There is deliberately no 404 here: this domain
#: documents none, and an unknown tag arrives as a 400. 409 is create-only and is pinned
#: separately, because it stays a plain SupermetricsAPIError (plan section 2.3).
ERROR_CASES: list[tuple[HTTPStatus, str, type[SupermetricsAPIError]]] = [
    (HTTPStatus.BAD_REQUEST, "BAD_REQUEST", SupermetricsValidationError),
    (HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", SupermetricsAuthError),
    (HTTPStatus.FORBIDDEN, "FORBIDDEN", SupermetricsForbiddenError),
    (HTTPStatus.TOO_MANY_REQUESTS, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


def _make_success_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=parsed)


def _make_error_response(status_code: HTTPStatus, code: str, message: str) -> Response:
    return Response(
        status_code=status_code,
        content=b"",
        headers={},
        parsed=ErrorResponse(
            meta=ErrorResponseMeta(request_id="req-id"),
            error=Error(code=code, message=message),
        ),
    )


def _sample_tag() -> AccountTag:
    """Build a persisted account tag, membership included as the read-side item type."""
    return AccountTag(
        name=TAG_NAME,
        display_name="EMEA paid media",
        color="#112233",
        data_sources=[AccountTagDataSourcesItem.from_dict(entry) for entry in DATA_SOURCES],
    )


def _sample_overview() -> AccountTagOverview:
    """Build a list-side account tag summary, which counts membership instead of listing it."""
    return AccountTagOverview(
        name=TAG_NAME,
        display_name="EMEA paid media",
        color="#112233",
        data_source_count=2,
        account_count=3,
    )


def _tag_response(data: AccountTag | object = None) -> AccountTagResponse:
    """Wrap a tag in the single-object envelope the API sends."""
    return AccountTagResponse(data=_sample_tag() if data is None else data)  # type: ignore[arg-type]


def _list_response(items: list[AccountTagOverview] | None = None) -> AccountTagListResponse:
    """Wrap a page of tag summaries in the ``{meta, data: {items}}`` envelope the API sends.

    Production double-wraps the page at ``data.items`` (see docs/openapi-spec-fixes.md), so
    the summaries go inside an ``AccountTagListResponseData``. An empty page is ``items=[]``.
    """
    if items is None:
        items = [_sample_overview()]
    return AccountTagListResponse(
        meta=Meta(request_id="req_test"),
        data=AccountTagListResponseData(items=items),
    )


def _delete_response(result: bool | object) -> DeleteAccountGroupResponse200:
    """Wrap a deletion outcome in the delete envelope, whose body is the whole answer."""
    return DeleteAccountGroupResponse200(data=DeleteAccountGroupResponse200Data(result=result))  # type: ignore[arg-type]


class TestAccountTagsResource:
    """Test suite for AccountTagsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def account_tags_resource(self, mock_client: MagicMock) -> AccountTagsResource:
        """Create an AccountTagsResource instance with mock client."""
        return AccountTagsResource(mock_client)

    @pytest.fixture
    def sample_tag(self) -> AccountTag:
        """Create a sample persisted account tag for testing."""
        return _sample_tag()

    @pytest.fixture
    def sample_overview(self) -> AccountTagOverview:
        """Create a sample account tag summary for testing."""
        return _sample_overview()

    # --- list() ---

    def test_list_success(self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource) -> None:
        """Test that list() unwraps .data into overviews carrying the summary counts."""
        mock_sync = MagicMock(return_value=_make_success_response(_list_response()))
        monkeypatch.setattr(module.fetch_available_account_groups, "sync_detailed", mock_sync)

        tags = account_tags_resource.list(team_id=TEAM_ID)

        assert len(tags) == 1
        assert tags[0].name == TAG_NAME
        assert tags[0].display_name == "EMEA paid media"
        assert tags[0].color == "#112233"
        assert tags[0].data_source_count == 2
        assert tags[0].account_count == 3
        assert mock_sync.call_args.kwargs["team_id"] == TEAM_ID

    def test_list_returns_empty_when_items_empty(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that an empty ``data.items`` array degrades to an empty list rather than raising."""
        monkeypatch.setattr(
            module.fetch_available_account_groups,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_list_response([]))),
        )

        assert account_tags_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_list_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        account_tags_resource: AccountTagsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that list() raises the matching SDK exception rather than returning a failure."""
        monkeypatch.setattr(
            module.fetch_available_account_groups,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            account_tags_resource.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    def test_list_network_error(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that list() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/account_tags"
        monkeypatch.setattr(
            module.fetch_available_account_groups,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            account_tags_resource.list(team_id=TEAM_ID)

    # --- get() ---

    def test_get_success(self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource) -> None:
        """Test that get() unwraps .data into an AccountTag carrying its membership."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.fetch_account_group, "sync_detailed", mock_sync)

        tag = account_tags_resource.get(team_id=TEAM_ID, name=TAG_NAME)

        assert tag.name == TAG_NAME
        assert tag.display_name == "EMEA paid media"
        assert [item.to_dict() for item in tag.data_sources] == DATA_SOURCES
        assert tag.data_sources[0]["data_source_id"] == "AW"

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    def test_get_returns_empty_tag_when_data_unset(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that a missing data object becomes an empty AccountTag, never None (plan 2.6)."""
        monkeypatch.setattr(
            module.fetch_account_group,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_tag_response(UNSET))),
        )

        tag = account_tags_resource.get(team_id=TEAM_ID, name=TAG_NAME)

        assert tag is not None
        assert isinstance(tag, AccountTag)
        assert tag.name is UNSET
        assert tag.display_name is UNSET
        assert tag.data_sources is UNSET
        assert tag.to_dict() == {}

    # --- create() ---

    def test_create_success(self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource) -> None:
        """Test that create() returns the tag carrying the server-assigned name."""
        monkeypatch.setattr(
            module.create_account_group,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_tag_response())),
        )

        tag = account_tags_resource.create(
            team_id=TEAM_ID,
            display_name="EMEA paid media",
            color="#112233",
            data_sources=DATA_SOURCES,
        )

        assert tag.name == TAG_NAME

    def test_create_builds_request_body(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that create() sends a CreateAccountGroupBody whose items are the create item type."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.create_account_group, "sync_detailed", mock_sync)

        account_tags_resource.create(
            team_id=TEAM_ID,
            display_name="EMEA paid media",
            color="#112233",
            data_sources=DATA_SOURCES,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        body = call_kwargs["body"]
        assert isinstance(body, CreateAccountGroupBody)
        assert body.display_name == "EMEA paid media"
        assert body.color == "#112233"
        assert all(isinstance(item, CreateAccountGroupBodyDataSourcesItem) for item in body.data_sources)
        assert [item.to_dict() for item in body.data_sources] == DATA_SOURCES
        assert body.to_dict()["data_sources"] == DATA_SOURCES

    def test_create_does_not_send_name(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that create() never sends a name; the slug is the server's to assign (plan 2.4)."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.create_account_group, "sync_detailed", mock_sync)

        account_tags_resource.create(
            team_id=TEAM_ID,
            display_name="EMEA paid media",
            color="#112233",
            data_sources=DATA_SOURCES,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert "name" not in call_kwargs
        assert "name" not in call_kwargs["body"].to_dict()

    def test_create_conflict_stays_a_plain_api_error(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that a duplicate display name raises a base SupermetricsAPIError with 409 (plan 2.3)."""
        monkeypatch.setattr(
            module.create_account_group,
            "sync_detailed",
            MagicMock(
                return_value=_make_error_response(HTTPStatus.CONFLICT, "CONFLICT_ERROR", "Account tag already exists")
            ),
        )

        with pytest.raises(SupermetricsAPIError) as exc_info:
            account_tags_resource.create(
                team_id=TEAM_ID,
                display_name="EMEA paid media",
                color="#112233",
                data_sources=DATA_SOURCES,
            )

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.status_code == 409
        assert exc_info.value.error_code == "CONFLICT_ERROR"

    # --- update() ---

    def test_update_success(self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource) -> None:
        """Test that update() unwraps the 200 response into the updated tag."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.update_account_group, "sync_detailed", mock_sync)

        tag = account_tags_resource.update(team_id=TEAM_ID, name=TAG_NAME, display_name="EMEA paid", color="#445566")

        assert tag.name == TAG_NAME

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    def test_update_body_omits_data_sources(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that update() sends display_name and color only; PUT cannot change membership."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.update_account_group, "sync_detailed", mock_sync)

        account_tags_resource.update(team_id=TEAM_ID, name=TAG_NAME, display_name="EMEA paid", color="#445566")

        body = mock_sync.call_args.kwargs["body"]
        assert isinstance(body, UpdateAccountGroupBody)
        assert body.display_name == "EMEA paid"
        assert body.color == "#445566"
        assert not hasattr(body, "data_sources")
        assert "data_sources" not in body.to_dict()
        assert body.to_dict() == {"display_name": "EMEA paid", "color": "#445566"}

    # --- delete() ---

    def test_delete_returns_true_when_result_true(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that delete() returns True when the body says a tag was removed (plan 2.2)."""
        mock_sync = MagicMock(return_value=_make_success_response(_delete_response(True)))
        monkeypatch.setattr(module.delete_account_group, "sync_detailed", mock_sync)

        assert account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is True

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    def test_delete_returns_false_when_result_false(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that deleting a tag that never existed is a success carrying False, not a 404."""
        monkeypatch.setattr(
            module.delete_account_group,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_delete_response(False))),
        )

        assert account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is False

    def test_delete_returns_false_when_data_unset(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that an absent data object means no claimed deletion, so False."""
        monkeypatch.setattr(
            module.delete_account_group,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(DeleteAccountGroupResponse200(data=UNSET))),
        )

        assert account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is False

    def test_delete_returns_false_when_result_unset(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that a data object with no result means no claimed deletion, so False."""
        monkeypatch.setattr(
            module.delete_account_group,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_delete_response(UNSET))),
        )

        assert account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is False

    # --- add_accounts() ---

    def test_add_accounts_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that add_accounts() unwraps .data into the tag with its updated membership."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.append_accounts_to_group, "sync_detailed", mock_sync)

        tag = account_tags_resource.add_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert tag.name == TAG_NAME

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    def test_add_accounts_builds_append_items(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that add_accounts() builds the append item type, not the create or remove one."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.append_accounts_to_group, "sync_detailed", mock_sync)

        account_tags_resource.add_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        body = mock_sync.call_args.kwargs["body"]
        assert isinstance(body, AppendAccountsToGroupBody)
        assert all(isinstance(item, AppendAccountsToGroupBodyDataSourcesItem) for item in body.data_sources)
        assert [item.to_dict() for item in body.data_sources] == DATA_SOURCES
        assert body.to_dict()["data_sources"] == DATA_SOURCES

    # --- remove_accounts() ---

    def test_remove_accounts_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that remove_accounts() unwraps .data into the tag with its updated membership."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.remove_accounts_from_group, "sync_detailed", mock_sync)

        tag = account_tags_resource.remove_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert tag.name == TAG_NAME

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    def test_remove_accounts_builds_remove_items(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsResource
    ) -> None:
        """Test that remove_accounts() builds the remove item type, not the create or append one."""
        mock_sync = MagicMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.remove_accounts_from_group, "sync_detailed", mock_sync)

        account_tags_resource.remove_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        body = mock_sync.call_args.kwargs["body"]
        assert isinstance(body, RemoveAccountsFromGroupBody)
        assert all(isinstance(item, RemoveAccountsFromGroupBodyDataSourcesItem) for item in body.data_sources)
        assert [item.to_dict() for item in body.data_sources] == DATA_SOURCES
        assert body.to_dict()["data_sources"] == DATA_SOURCES


class TestAccountTagsAsyncResource:
    """Test suite for AccountTagsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def account_tags_resource(self, mock_client: MagicMock) -> AccountTagsAsyncResource:
        """Create an AccountTagsAsyncResource instance with mock client."""
        return AccountTagsAsyncResource(mock_client)

    @pytest.fixture
    def sample_tag(self) -> AccountTag:
        """Create a sample persisted account tag for testing."""
        return _sample_tag()

    @pytest.fixture
    def sample_overview(self) -> AccountTagOverview:
        """Create a sample account tag summary for testing."""
        return _sample_overview()

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async list() unwraps .data into overviews carrying the summary counts."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_list_response()))
        monkeypatch.setattr(module.fetch_available_account_groups, "asyncio_detailed", mock_asyncio)

        tags = await account_tags_resource.list(team_id=TEAM_ID)

        assert len(tags) == 1
        assert tags[0].name == TAG_NAME
        assert tags[0].data_source_count == 2
        assert tags[0].account_count == 3
        assert mock_asyncio.call_args.kwargs["team_id"] == TEAM_ID

    @pytest.mark.asyncio
    async def test_list_returns_empty_when_items_empty(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that an empty ``data.items`` array degrades to an empty list on the async path too."""
        monkeypatch.setattr(
            module.fetch_available_account_groups,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_list_response([]))),
        )

        assert await account_tags_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_list_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        account_tags_resource: AccountTagsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async list() raises the matching SDK exception rather than returning a failure."""
        monkeypatch.setattr(
            module.fetch_available_account_groups,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await account_tags_resource.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    @pytest.mark.asyncio
    async def test_list_network_error(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async list() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/account_tags"
        monkeypatch.setattr(
            module.fetch_available_account_groups,
            "asyncio_detailed",
            AsyncMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            await account_tags_resource.list(team_id=TEAM_ID)

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async get() unwraps .data into an AccountTag carrying its membership."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.fetch_account_group, "asyncio_detailed", mock_asyncio)

        tag = await account_tags_resource.get(team_id=TEAM_ID, name=TAG_NAME)

        assert tag.name == TAG_NAME
        assert [item.to_dict() for item in tag.data_sources] == DATA_SOURCES

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    @pytest.mark.asyncio
    async def test_get_returns_empty_tag_when_data_unset(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that a missing data object becomes an empty AccountTag on the async path too."""
        monkeypatch.setattr(
            module.fetch_account_group,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_tag_response(UNSET))),
        )

        tag = await account_tags_resource.get(team_id=TEAM_ID, name=TAG_NAME)

        assert tag is not None
        assert isinstance(tag, AccountTag)
        assert tag.name is UNSET
        assert tag.to_dict() == {}

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async create() returns the tag carrying the server-assigned name."""
        monkeypatch.setattr(
            module.create_account_group,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_tag_response())),
        )

        tag = await account_tags_resource.create(
            team_id=TEAM_ID,
            display_name="EMEA paid media",
            color="#112233",
            data_sources=DATA_SOURCES,
        )

        assert tag.name == TAG_NAME

    @pytest.mark.asyncio
    async def test_create_builds_request_body(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async create() sends a CreateAccountGroupBody whose items are the create item type."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.create_account_group, "asyncio_detailed", mock_asyncio)

        await account_tags_resource.create(
            team_id=TEAM_ID,
            display_name="EMEA paid media",
            color="#112233",
            data_sources=DATA_SOURCES,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        body = call_kwargs["body"]
        assert isinstance(body, CreateAccountGroupBody)
        assert body.display_name == "EMEA paid media"
        assert body.color == "#112233"
        assert all(isinstance(item, CreateAccountGroupBodyDataSourcesItem) for item in body.data_sources)
        assert [item.to_dict() for item in body.data_sources] == DATA_SOURCES
        assert "name" not in body.to_dict()

    @pytest.mark.asyncio
    async def test_create_conflict_stays_a_plain_api_error(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that a duplicate display name raises a base SupermetricsAPIError with 409 on async too."""
        monkeypatch.setattr(
            module.create_account_group,
            "asyncio_detailed",
            AsyncMock(
                return_value=_make_error_response(HTTPStatus.CONFLICT, "CONFLICT_ERROR", "Account tag already exists")
            ),
        )

        with pytest.raises(SupermetricsAPIError) as exc_info:
            await account_tags_resource.create(
                team_id=TEAM_ID,
                display_name="EMEA paid media",
                color="#112233",
                data_sources=DATA_SOURCES,
            )

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.status_code == 409
        assert exc_info.value.error_code == "CONFLICT_ERROR"

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async update() unwraps the 200 response into the updated tag."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.update_account_group, "asyncio_detailed", mock_asyncio)

        tag = await account_tags_resource.update(
            team_id=TEAM_ID, name=TAG_NAME, display_name="EMEA paid", color="#445566"
        )

        assert tag.name == TAG_NAME

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    @pytest.mark.asyncio
    async def test_update_body_omits_data_sources(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async update() sends display_name and color only; PUT cannot change membership."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.update_account_group, "asyncio_detailed", mock_asyncio)

        await account_tags_resource.update(team_id=TEAM_ID, name=TAG_NAME, display_name="EMEA paid", color="#445566")

        body = mock_asyncio.call_args.kwargs["body"]
        assert isinstance(body, UpdateAccountGroupBody)
        assert not hasattr(body, "data_sources")
        assert "data_sources" not in body.to_dict()
        assert body.to_dict() == {"display_name": "EMEA paid", "color": "#445566"}

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_returns_true_when_result_true(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async delete() returns True when the body says a tag was removed."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_delete_response(True)))
        monkeypatch.setattr(module.delete_account_group, "asyncio_detailed", mock_asyncio)

        assert await account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is True

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_result_false(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that deleting a tag that never existed is a success carrying False on async too."""
        monkeypatch.setattr(
            module.delete_account_group,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_delete_response(False))),
        )

        assert await account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is False

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_data_unset(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that an absent data object means no claimed deletion, so False."""
        monkeypatch.setattr(
            module.delete_account_group,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(DeleteAccountGroupResponse200(data=UNSET))),
        )

        assert await account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is False

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_result_unset(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that a data object with no result means no claimed deletion, so False."""
        monkeypatch.setattr(
            module.delete_account_group,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_delete_response(UNSET))),
        )

        assert await account_tags_resource.delete(team_id=TEAM_ID, name=TAG_NAME) is False

    # --- add_accounts() ---

    @pytest.mark.asyncio
    async def test_add_accounts_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async add_accounts() unwraps .data into the tag with its updated membership."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.append_accounts_to_group, "asyncio_detailed", mock_asyncio)

        tag = await account_tags_resource.add_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert tag.name == TAG_NAME

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    @pytest.mark.asyncio
    async def test_add_accounts_builds_append_items(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async add_accounts() builds the append item type, not the create or remove one."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.append_accounts_to_group, "asyncio_detailed", mock_asyncio)

        await account_tags_resource.add_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        body = mock_asyncio.call_args.kwargs["body"]
        assert isinstance(body, AppendAccountsToGroupBody)
        assert all(isinstance(item, AppendAccountsToGroupBodyDataSourcesItem) for item in body.data_sources)
        assert [item.to_dict() for item in body.data_sources] == DATA_SOURCES

    # --- remove_accounts() ---

    @pytest.mark.asyncio
    async def test_remove_accounts_success(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async remove_accounts() unwraps .data into the tag with its updated membership."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.remove_accounts_from_group, "asyncio_detailed", mock_asyncio)

        tag = await account_tags_resource.remove_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert tag.name == TAG_NAME

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["name"] == TAG_NAME

    @pytest.mark.asyncio
    async def test_remove_accounts_builds_remove_items(
        self, monkeypatch: pytest.MonkeyPatch, account_tags_resource: AccountTagsAsyncResource
    ) -> None:
        """Test that async remove_accounts() builds the remove item type, not the create or append one."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(_tag_response()))
        monkeypatch.setattr(module.remove_accounts_from_group, "asyncio_detailed", mock_asyncio)

        await account_tags_resource.remove_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        body = mock_asyncio.call_args.kwargs["body"]
        assert isinstance(body, RemoveAccountsFromGroupBody)
        assert all(isinstance(item, RemoveAccountsFromGroupBodyDataSourcesItem) for item in body.data_sources)
        assert [item.to_dict() for item in body.data_sources] == DATA_SOURCES
