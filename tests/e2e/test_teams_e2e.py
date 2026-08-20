"""End-to-end tests for the Teams resource.

Drives both methods — ``get`` and ``list_users`` — over a real loopback socket. Teams stay
on the core API host: the paths keep their ``/v1`` prefix and nothing is re-hosted to the
Data Warehouse host, so one server is the whole story here.

Every test asserts on both directions: the parsed return value, and the request that
actually went out. The outbound half is the point of this layer, and three things in this
domain exist only on the wire:

* the path carries ``/v1`` and addresses the core host, which no unit test can see;
* the ``team_id`` is percent-encoded into the path with ``safe=""`` by the generated
  layer, and both endpoints derive their URL independently;
* the response is wrapped in ``{"meta": ..., "data": ...}`` and the adapter hands back the
  ``data`` payload — a :class:`TeamData` for ``get``, a bare ``list[TeamUser]`` for
  ``list_users`` — never the envelope.

Error mapping lives in ``test_teams_errors_e2e.py`` and per-request overrides in
``test_teams_overrides_e2e.py``; neither is repeated here.
"""

from __future__ import annotations

from urllib.parse import urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import (
    TEAM_ITEM,
    TEAM_USERS,
    TEAM_USERS_EMPTY_BODY,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e

#: The team these tests address. It reaches the wire as a path segment, not a query param.
TEAM_ID = 42


class TestTeamsResource:
    """Synchronous team lookup and member listing."""

    def test_get_returns_the_team_from_the_data_envelope(self, teams_server: MockAPIServer) -> None:
        """The envelope is ``{"meta": ..., "data": {...}}``; the adapter hands back the team."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            team = client.teams.get(team_id=TEAM_ID)

        assert team.team_id == 42
        assert team.name == "My Team"
        assert team.display_id == "SM_ABC123"
        assert team.status == 1
        assert team.created_at.year == 2026

        request = teams_server.last_request
        assert request.method == "GET"
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_get_requests_the_v1_item_path_with_no_query_string(self, teams_server: MockAPIServer) -> None:
        """The literal outbound path, spelled out.

        This is the highest-value assertion in the file. Teams are served from the core API
        host with ``/v1`` in the path; a ``rewrite_path`` slip that dropped the prefix, or
        one that reshaped the path into the ``^/teams/...`` form the transport inspects when
        deciding to re-host to the Data Warehouse host, would be invisible to every unit
        test in the repo. There are also no query parameters in this domain, so an empty
        query string is part of the contract.
        """
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.get(team_id=TEAM_ID)

        path = teams_server.last_request.path
        assert urlsplit(path).path == TEAM_ITEM
        assert urlsplit(path).query == ""
        # The team id is one path segment, not two.
        assert path.split("/")[1:] == ["v1", "teams", "42"]

    def test_list_users_returns_the_members_from_the_data_array(self, teams_server: MockAPIServer) -> None:
        """``list_users`` unwraps the bare ``data`` array into ``TeamUser`` models."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            users = client.teams.list_users(team_id=TEAM_ID)

        assert len(users) == 2
        assert users[0].user_id == 1
        assert users[0].email == "user@example.com"
        assert users[0].first_name == "John"
        assert users[0].last_name == "Doe"
        assert users[0].role == "ADMIN"
        assert users[0].created_at.year == 2026
        assert users[1].user_id == 2
        assert users[1].role == "MEMBER"

        request = teams_server.last_request
        assert request.method == "GET"
        assert request.path == TEAM_USERS
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_users_returns_an_empty_list_when_the_team_has_no_members(self, api_server: MockAPIServer) -> None:
        """An empty ``data`` array is not an error, and not ``None``."""
        api_server.route(TEAM_USERS, ScriptedResponse(json_body=TEAM_USERS_EMPTY_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            users = client.teams.list_users(team_id=TEAM_ID)

        assert users == []

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == TEAM_USERS

    def test_list_users_requests_the_v1_users_path_with_no_query_string(self, teams_server: MockAPIServer) -> None:
        """The members path is its own ``/v1`` route, distinct from the item path."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.list_users(team_id=TEAM_ID)

        path = teams_server.last_request.path
        assert urlsplit(path).path == TEAM_USERS
        assert urlsplit(path).query == ""
        assert path.split("/")[1:] == ["v1", "teams", "42", "users"]

    def test_get_and_list_users_are_distinct_routes(self, teams_server: MockAPIServer) -> None:
        """The two methods address different paths; neither falls back to the other."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.get(team_id=TEAM_ID)
            client.teams.list_users(team_id=TEAM_ID)

        assert [urlsplit(r.path).path for r in teams_server.requests] == [TEAM_ITEM, TEAM_USERS]


class TestTeamsAsyncResource:
    """Asynchronous teams — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_get_returns_the_team_from_the_data_envelope(self, teams_server: MockAPIServer) -> None:
        """The async path unwraps ``data`` and hits the same ``/v1`` core-host path."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=teams_server.base_url) as client:
            team = await client.teams.get(team_id=TEAM_ID)

        assert team.team_id == 42
        assert team.name == "My Team"
        assert team.display_id == "SM_ABC123"
        assert team.status == 1

        request = teams_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == TEAM_ITEM
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_list_users_returns_the_members_from_the_data_array(self, teams_server: MockAPIServer) -> None:
        """The async client unwraps the users array identically."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=teams_server.base_url) as client:
            users = await client.teams.list_users(team_id=TEAM_ID)

        assert len(users) == 2
        assert users[0].user_id == 1
        assert users[0].role == "ADMIN"
        assert users[1].user_id == 2
        assert users[1].email == "member@example.com"

        request = teams_server.last_request
        assert request.method == "GET"
        assert request.path == TEAM_USERS
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_list_users_returns_an_empty_list_when_the_team_has_no_members(
        self, api_server: MockAPIServer
    ) -> None:
        """An empty ``data`` array is an empty team on the async path too."""
        api_server.route(TEAM_USERS, ScriptedResponse(json_body=TEAM_USERS_EMPTY_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            users = await client.teams.list_users(team_id=TEAM_ID)

        assert users == []
        assert urlsplit(api_server.last_request.path).path == TEAM_USERS
