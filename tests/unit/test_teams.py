"""Unit tests for TeamsResource and TeamsAsyncResource.

These mock at the generated-client boundary and open no socket. Every patch goes through
``monkeypatch.setattr`` rather than the save-and-restore-by-hand idiom: a bare trailing
restore statement is skipped when an assertion fails, which leaks the mock into every later
test in the session. ``monkeypatch`` unwinds on failure too, so a red test stays a single
red test.

Error taxonomy is covered here only far enough to prove that a non-200 is raised rather
than returned; ``tests/e2e/test_teams_errors_e2e.py`` exercises it in depth over a real
socket.
"""

from __future__ import annotations

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.error_response_meta import ErrorResponseMeta
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.team_data import TeamData
from supermetrics._generated.supermetrics_api_client.models.team_response import TeamResponse
from supermetrics._generated.supermetrics_api_client.models.team_user import TeamUser
from supermetrics._generated.supermetrics_api_client.models.team_user_list_response import TeamUserListResponse
from supermetrics._generated.supermetrics_api_client.types import Response
from supermetrics.exceptions import (
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)
from supermetrics.resources import teams as module
from supermetrics.resources.teams import TeamsAsyncResource, TeamsResource

TEAM_ID = 42

#: The documented failures ``get`` maps, including the 404 a team lookup can genuinely hit.
GET_ERROR_CASES: list[tuple[HTTPStatus, str, type[SupermetricsAPIError]]] = [
    (HTTPStatus.BAD_REQUEST, "BAD_REQUEST", SupermetricsValidationError),
    (HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", SupermetricsAuthError),
    (HTTPStatus.FORBIDDEN, "FORBIDDEN", SupermetricsForbiddenError),
    (HTTPStatus.NOT_FOUND, "NOT_FOUND", SupermetricsNotFoundError),
    (HTTPStatus.TOO_MANY_REQUESTS, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]

#: The failures ``list_users`` documents — the same set minus the 404 it does not.
LIST_USERS_ERROR_CASES: list[tuple[HTTPStatus, str, type[SupermetricsAPIError]]] = [
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


def _sample_team() -> TeamData:
    """Build a team as the ``data`` payload of ``getTeam``."""
    return TeamData(
        team_id=42,
        name="My Team",
        display_id="SM_ABC123",
        status=1,
        created_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
    )


def _sample_users() -> list[TeamUser]:
    """Build two team members as the ``data`` array of ``listTeamUsers``."""
    return [
        TeamUser(
            user_id=1,
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            role="ADMIN",
            created_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        ),
        TeamUser(
            user_id=2,
            email="member@example.com",
            first_name="Jane",
            last_name="Roe",
            role="MEMBER",
            created_at=datetime.datetime(2026, 2, 1, tzinfo=datetime.UTC),
        ),
    ]


def _team_response(data: TeamData | None = None) -> TeamResponse:
    """Wrap a team in the single-object envelope the API sends."""
    return TeamResponse(meta=Meta(request_id="req-id"), data=_sample_team() if data is None else data)


def _users_response(data: list[TeamUser] | None = None) -> TeamUserListResponse:
    """Wrap a page of members in the list envelope the API sends."""
    return TeamUserListResponse(meta=Meta(request_id="req-id"), data=_sample_users() if data is None else data)


class TestTeamsResource:
    """Test suite for TeamsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def teams_resource(self, mock_client: MagicMock) -> TeamsResource:
        """Create a TeamsResource instance with a mock client."""
        return TeamsResource(mock_client)

    # --- get() ---

    def test_get_success(self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsResource) -> None:
        """get() unwraps .data into a TeamData carrying the team's identity fields."""
        mock_sync = MagicMock(return_value=_make_success_response(_team_response()))
        monkeypatch.setattr(module.get_team, "sync_detailed", mock_sync)

        team = teams_resource.get(team_id=TEAM_ID)

        assert team.team_id == 42
        assert team.name == "My Team"
        assert team.display_id == "SM_ABC123"
        assert team.status == 1
        assert mock_sync.call_args.kwargs["team_id"] == TEAM_ID

    @pytest.mark.parametrize(("status", "code", "expected"), GET_ERROR_CASES)
    def test_get_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        teams_resource: TeamsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """get() raises the matching SDK exception rather than returning a failure."""
        monkeypatch.setattr(
            module.get_team,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            teams_resource.get(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)
        assert exc_info.value.error_code == code

    def test_get_network_error(self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsResource) -> None:
        """get() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}"
        monkeypatch.setattr(
            module.get_team,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            teams_resource.get(team_id=TEAM_ID)

    # --- list_users() ---

    def test_list_users_success(self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsResource) -> None:
        """list_users() unwraps .data into a list of TeamUser models."""
        mock_sync = MagicMock(return_value=_make_success_response(_users_response()))
        monkeypatch.setattr(module.list_team_users, "sync_detailed", mock_sync)

        users = teams_resource.list_users(team_id=TEAM_ID)

        assert len(users) == 2
        assert users[0].user_id == 1
        assert users[0].email == "user@example.com"
        assert users[0].role == "ADMIN"
        assert users[1].user_id == 2
        assert mock_sync.call_args.kwargs["team_id"] == TEAM_ID

    def test_list_users_returns_empty_when_data_empty(
        self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsResource
    ) -> None:
        """An empty data array degrades to an empty list rather than raising."""
        monkeypatch.setattr(
            module.list_team_users,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_users_response([]))),
        )

        assert teams_resource.list_users(team_id=TEAM_ID) == []

    @pytest.mark.parametrize(("status", "code", "expected"), LIST_USERS_ERROR_CASES)
    def test_list_users_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        teams_resource: TeamsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """list_users() raises the matching SDK exception rather than returning a failure."""
        monkeypatch.setattr(
            module.list_team_users,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            teams_resource.list_users(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    def test_list_users_network_error(self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsResource) -> None:
        """list_users() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/users"
        monkeypatch.setattr(
            module.list_team_users,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            teams_resource.list_users(team_id=TEAM_ID)


class TestTeamsAsyncResource:
    """Test suite for TeamsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def teams_resource(self, mock_client: MagicMock) -> TeamsAsyncResource:
        """Create a TeamsAsyncResource instance with a mock client."""
        return TeamsAsyncResource(mock_client)

    @pytest.mark.asyncio
    async def test_get_success(self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsAsyncResource) -> None:
        """The async get() unwraps .data identically to the sync one."""
        mock_async = AsyncMock(return_value=_make_success_response(_team_response()))
        monkeypatch.setattr(module.get_team, "asyncio_detailed", mock_async)

        team = await teams_resource.get(team_id=TEAM_ID)

        assert team.team_id == 42
        assert team.name == "My Team"
        assert mock_async.call_args.kwargs["team_id"] == TEAM_ID

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), GET_ERROR_CASES)
    async def test_get_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        teams_resource: TeamsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async get() classifies a failing lookup identically."""
        monkeypatch.setattr(
            module.get_team,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await teams_resource.get(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    @pytest.mark.asyncio
    async def test_list_users_success(
        self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsAsyncResource
    ) -> None:
        """The async list_users() unwraps the members array."""
        mock_async = AsyncMock(return_value=_make_success_response(_users_response()))
        monkeypatch.setattr(module.list_team_users, "asyncio_detailed", mock_async)

        users = await teams_resource.list_users(team_id=TEAM_ID)

        assert [u.user_id for u in users] == [1, 2]
        assert mock_async.call_args.kwargs["team_id"] == TEAM_ID

    @pytest.mark.asyncio
    async def test_list_users_returns_empty_when_data_empty(
        self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsAsyncResource
    ) -> None:
        """An empty members array degrades to [] on the async path too."""
        monkeypatch.setattr(
            module.list_team_users,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_users_response([]))),
        )

        assert await teams_resource.list_users(team_id=TEAM_ID) == []

    @pytest.mark.asyncio
    async def test_list_users_network_error(
        self, monkeypatch: pytest.MonkeyPatch, teams_resource: TeamsAsyncResource
    ) -> None:
        """The async list_users() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/users"
        monkeypatch.setattr(
            module.list_team_users,
            "asyncio_detailed",
            AsyncMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            await teams_resource.list_users(team_id=TEAM_ID)
