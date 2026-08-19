"""End-to-end tests for per-request overrides on team calls.

Both team methods are bodyless reads, but they derive their URLs from two independently
generated modules (``teams.get_team`` and ``team_users.list_team_users``), so the override
machinery — which lives in the client's transport event hooks, not in the adapter — is
proven on each. These tests pin ``auth_token``, ``headers`` and ``timeout`` down on both
methods, on both clients, asserting on what the server received rather than on what the
client returned.
"""

from __future__ import annotations

import httpx
import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import NetworkError

from .conftest import TEAM_GET_BODY, TEAM_ITEM, TEAM_USERS, TEAM_USERS_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

TEAM_ID = 42


class TestTeamsAuthTokenOverrideResource:
    """``auth_token=`` beats the client credential, for exactly one call."""

    def test_auth_token_overrides_the_client_credential_on_get(self, teams_server: MockAPIServer) -> None:
        """The scoped token is used for that call only; the next reverts to the client key."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.get(TEAM_ID, auth_token="otok_scoped")
            client.teams.get(TEAM_ID)

        assert [r.bearer_token for r in teams_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in teams_server.requests] == ["GET", "GET"]

    def test_auth_token_overrides_the_client_credential_on_list_users(self, teams_server: MockAPIServer) -> None:
        """``list_users`` is a separately generated read, so the override is proven on it too."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.list_users(TEAM_ID, auth_token="otok_scoped")
            client.teams.list_users(TEAM_ID)

        assert [r.bearer_token for r in teams_server.requests] == ["otok_scoped", "api_k"]
        assert [r.path for r in teams_server.requests] == [TEAM_USERS, TEAM_USERS]


class TestTeamsHeaderOverrideResource:
    """``headers=`` reaches the wire and outranks the client's own defaults."""

    def test_headers_reach_the_wire_on_get(self, teams_server: MockAPIServer) -> None:
        """Correlation and idempotency headers are sent, recorded lower-cased."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.get(TEAM_ID, headers={"X-Span-Id": "span-t-1", "Idempotency-Key": "idem-t-1"})

        received = teams_server.last_request.headers
        assert received["x-span-id"] == "span-t-1"
        assert received["idempotency-key"] == "idem-t-1"

    def test_headers_merge_over_client_defaults_case_insensitively(self, teams_server: MockAPIServer) -> None:
        """A lower-cased per-request header replaces a differently-cased client one."""
        with SupermetricsClient(
            api_key="api_k",
            base_url=teams_server.base_url,
            custom_headers={"X-Team-ID": "client-level", "X-Tenant": "acme"},
        ) as client:
            client.teams.get(TEAM_ID)
            client.teams.get(TEAM_ID, headers={"x-team-id": "request-level"})

        first, second = teams_server.requests
        assert first.headers["x-team-id"] == "client-level"
        # The collision is resolved in the request's favour, and only that header moves:
        # the untouched client default and the SDK's own User-Agent both survive.
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-tenant"] == "acme"
        assert second.headers["user-agent"].startswith("supermetrics-sdk/")

    def test_headers_do_not_leak_into_the_next_call(self, teams_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=teams_server.base_url) as client:
            client.teams.list_users(TEAM_ID, headers={"X-Span-Id": "only-once"})
            client.teams.list_users(TEAM_ID)

        assert teams_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in teams_server.requests[1].headers


class TestTeamsTimeoutOverrideResource:
    """``timeout=`` overrides the client budget in both directions, against a real delay."""

    def test_short_override_times_out_a_slow_get(self, api_server: MockAPIServer) -> None:
        """A 0.2s override fails against an endpoint the 30s client budget would tolerate."""
        api_server.route(TEAM_ITEM, ScriptedResponse(json_body=TEAM_GET_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.teams.get(TEAM_ID, timeout=0.2)

    def test_generous_override_beats_a_tight_client_timeout_on_list_users(self, api_server: MockAPIServer) -> None:
        """Against a 0.6s endpoint, the client's 0.2s budget fails and 10s succeeds."""
        api_server.route(TEAM_USERS, ScriptedResponse(json_body=TEAM_USERS_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=0.2) as client:
            with pytest.raises(NetworkError):
                client.teams.list_users(TEAM_ID)
            users = client.teams.list_users(TEAM_ID, timeout=httpx.Timeout(10.0))

        assert [u.user_id for u in users] == [1, 2]

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout failure the client-level budget applies again."""
        api_server.route(
            TEAM_ITEM,
            ScriptedResponse(json_body=TEAM_GET_BODY, delay=0.6),
            ScriptedResponse(json_body=TEAM_GET_BODY),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.teams.get(TEAM_ID, timeout=0.2)
            assert client.teams.get(TEAM_ID).team_id == 42


class TestTeamsOverridesAsyncResource:
    """The async surface applies every one of the same overrides."""

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_on_get(self, teams_server: MockAPIServer) -> None:
        """The async client scopes the override to a single awaited call."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=teams_server.base_url) as client:
            await client.teams.get(TEAM_ID, auth_token="otok_scoped")
            await client.teams.get(TEAM_ID)

        assert [r.bearer_token for r in teams_server.requests] == ["otok_scoped", "api_k"]

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_on_list_users(self, teams_server: MockAPIServer) -> None:
        """The async ``list_users`` scopes and then reverts the credential too."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=teams_server.base_url) as client:
            await client.teams.list_users(TEAM_ID, auth_token="otok_scoped")
            await client.teams.list_users(TEAM_ID)

        assert [r.bearer_token for r in teams_server.requests] == ["otok_scoped", "api_k"]
        assert [r.path for r in teams_server.requests] == [TEAM_USERS, TEAM_USERS]

    @pytest.mark.asyncio
    async def test_headers_merge_over_client_defaults_case_insensitively(self, teams_server: MockAPIServer) -> None:
        """Async header merging resolves a cased collision in the request's favour."""
        async with SupermetricsAsyncClient(
            api_key="api_k", base_url=teams_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            await client.teams.get(TEAM_ID)
            await client.teams.get(TEAM_ID, headers={"x-team-id": "request-level", "X-Span-Id": "async-span"})

        first, second = teams_server.requests
        assert first.headers["x-team-id"] == "client-level"
        assert "x-span-id" not in first.headers
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-span-id"] == "async-span"

    @pytest.mark.asyncio
    async def test_timeout_override_in_both_directions_on_list_users(self, api_server: MockAPIServer) -> None:
        """Against one 0.6s route the async client fails at 0.2s and succeeds at 10s."""
        api_server.route(TEAM_USERS, ScriptedResponse(json_body=TEAM_USERS_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.teams.list_users(TEAM_ID, timeout=0.2)
            users = await client.teams.list_users(TEAM_ID, timeout=10.0)

        assert [u.user_id for u in users] == [1, 2]
