"""End-to-end tests for the teams error taxonomy.

Every failure here is a real HTTP response with a real status and real headers, driven
through the whole stack over a loopback socket. Error classification, ``Retry-After``
parsing and correlation-header capture only exist on the wire, so a mocked transport
cannot observe any of them.

One asymmetry in this domain is worth pinning: the two operations document different
failure sets. ``get`` (``GET /v1/teams/{team_id}``) documents a 404 — a team can genuinely
be missing — while ``list_users`` (``GET /v1/teams/{team_id}/users``) does not; a request
against an inaccessible team surfaces there as a 403 or a 400, never a 404. Each method's
set is asserted on its own so a regression confined to one adapter cannot hide behind the
other.

The routes are spelled out here rather than taken from ``conftest.py`` because this module
scripts failing responses on them; the happy-path module scripts the same paths for
successes.
"""

from __future__ import annotations

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import (
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: Teams live on the CORE api host under a "/v1" path prefix, so the routes carry the
#: version. A regression that re-hosted them or dropped the "/v1" would fall through to the
#: mock server's default 404 rather than reaching the scripted status.
TEAM_ID = 42
TEAM_ITEM = f"/v1/teams/{TEAM_ID}"
TEAM_USERS = f"/v1/teams/{TEAM_ID}/users"


def _error_envelope(code: str, message: str) -> dict[str, object]:
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


#: Every failure status ``get`` documents, and the class each becomes. ``get`` is the one
#: operation in this domain with a documented 404, because a team can be genuinely missing.
GET_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (404, "NOT_FOUND", SupermetricsNotFoundError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]

#: The failures ``list_users`` documents — the same set minus 404, which it does not.
LIST_USERS_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


class TestTeamsGetErrorTaxonomy:
    """Status-to-exception mapping and preserved transport metadata on ``get``."""

    @pytest.mark.parametrize(("status", "code", "expected"), GET_FAILURES)
    def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Each documented status raises its own class and keeps the upstream code."""
        api_server.route(TEAM_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.teams.get(team_id=TEAM_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == TEAM_ITEM

    def test_missing_team_is_a_not_found_error(self, api_server: MockAPIServer) -> None:
        """A 404 from ``get`` is a documented status, classified as not-found.

        Unlike account tags — where nothing 404s — a team lookup can genuinely miss, so this
        asserts the contract rather than SDK fallback behaviour.
        """
        api_server.route(TEAM_ITEM, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no team")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.teams.get(team_id=TEAM_ID)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"

    def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """X-Request-Id and X-Span-Id on the failing response are reachable on the exception."""
        api_server.route(
            TEAM_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-at-500", "X-Span-Id": "span-at-500"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.teams.get(team_id=TEAM_ID)

        assert exc_info.value.request_id == "req-at-500"
        assert exc_info.value.span_id == "span-at-500"

    @pytest.mark.parametrize(("status", "code"), [(401, "UNAUTHORIZED"), (500, "INTERNAL_SERVER_ERROR")])
    def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer, status: int, code: str) -> None:
        """No exception stringifies the credential, whoever ends up logging it."""
        api_server.route(TEAM_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.teams.get(team_id=TEAM_ID)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestTeamsListUsersErrorTaxonomy:
    """``list_users`` classifies its own documented failures, on its own route."""

    @pytest.mark.parametrize(("status", "code", "expected"), LIST_USERS_FAILURES)
    def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """A failing members GET raises its class rather than degrading to an empty list."""
        api_server.route(TEAM_USERS, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.teams.list_users(team_id=TEAM_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == TEAM_USERS

    def test_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the 429 response rather than guessed."""
        api_server.route(
            TEAM_USERS,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.teams.list_users(team_id=TEAM_ID)

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30
        assert api_server.last_request.path == TEAM_USERS

    def test_an_undocumented_404_still_classifies_by_status(self, api_server: MockAPIServer) -> None:
        """``list_users`` documents no 404, but one from a gateway still keeps its status.

        The generated parser has no 404 branch for this operation, so it returns ``None``
        and the adapter classifies from the transport's recorded status. A caller must not
        have to tell "the API said 404" apart from "something between us and the API did".
        """
        api_server.route(TEAM_USERS, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "gone")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.teams.list_users(team_id=TEAM_ID)

        assert exc_info.value.status_code == 404
        assert api_server.last_request.path == TEAM_USERS


class TestTeamsAsyncErrorTaxonomy:
    """The async surface has its own event hooks and its own error paths."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), GET_FAILURES)
    async def test_get_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async ``get`` classifies a failing lookup identically to the sync one."""
        api_server.route(TEAM_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.teams.get(team_id=TEAM_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == TEAM_ITEM

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), LIST_USERS_FAILURES)
    async def test_list_users_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async ``list_users`` classifies each documented failure on its own route."""
        api_server.route(TEAM_USERS, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.teams.list_users(team_id=TEAM_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.path == TEAM_USERS

    @pytest.mark.asyncio
    async def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """Correlation headers reach the exception on the async path too."""
        api_server.route(
            TEAM_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-at-async-500", "X-Span-Id": "span-at-async-500"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.teams.get(team_id=TEAM_ID)

        assert exc_info.value.request_id == "req-at-async-500"
        assert exc_info.value.span_id == "span-at-async-500"

    @pytest.mark.asyncio
    async def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer) -> None:
        """Credential hygiene holds on the async path."""
        api_server.route(
            TEAM_ITEM,
            ScriptedResponse(status=401, json_body=_error_envelope("ACCESS_TOKEN_INVALID", "expired")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.teams.get(team_id=TEAM_ID)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)
