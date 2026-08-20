"""End-to-end tests for the Backfills resource.

Drives all five methods over a real loopback socket. Backfills are a Data Warehouse
resource, but these tests hand the client a custom ``base_url``, which disables the DTS
host routing and lands every request on the one mock server — host routing is proven
elsewhere, so only the path, method and body matter here.

Every method gets two tests: one on the parsed return value, one on the request that
actually went out. The request half is the point of this layer; a mocked transport
cannot see that ``create`` serializes its dates as bare ISO strings, that ``cancel``
sends a ``PATCH`` with ``{"status": "CANCELLED"}`` rather than a ``PUT``, or that
``list_incomplete`` sends no query string at all.

The wire contract worth noting up front:

* Every response is wrapped in ``{"meta": {...}, "data": ...}``. Both keys are required
  by the generated ``from_dict`` — a bare body would raise ``KeyError``, not parse — so
  the payloads below always carry the envelope.
* ``create`` answers ``200``, not ``201``, despite being a creation.
* ``cancel`` is an ``update_backfill_status`` call under the hood: ``PATCH`` on the by-id
  path, with the status in the body. It shares that path with ``get``.
"""

from __future__ import annotations

from datetime import date
from typing import Any
from urllib.parse import urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

# --- Response payloads --------------------------------------------------------
#
# Defined inline (not in conftest) so parallel edits to conftest cannot collide.

#: The envelope metadata every wrapped response carries.
_META: dict[str, Any] = {"request_id": "req_0123456789abcdef"}

#: A running backfill, as read operations return it. Carries every required field plus
#: the optional timing fields left UNSET (absent) — an in-flight backfill has not been
#: removed and may not have started, so those keys are simply not present.
BACKFILL_PAYLOAD: dict[str, Any] = {
    "transfer_backfill_id": 12345,
    "transfer_id": 456789,
    "range_start_date": "2024-01-01",
    "range_end_date": "2024-01-31",
    "created_time": "2024-02-01T09:00:00Z",
    "created_user_id": 789,
    "status": "RUNNING",
    "transfer_runs_total": 31,
    "transfer_runs_created": 31,
    "transfer_runs_completed": 25,
    "transfer_runs_failed": 2,
    "start_time": "2024-02-01T10:00:00Z",
    "error_report": [],
}

#: The same backfill after a cancel: status flips to CANCELLED and the optional
#: removed_* fields are now populated, exercising the nullable-datetime parse path.
BACKFILL_CANCELLED_PAYLOAD: dict[str, Any] = {
    **BACKFILL_PAYLOAD,
    "status": "CANCELLED",
    "removed_time": "2024-02-01T15:00:00Z",
    "removed_user_id": 790,
}

#: GET / POST / PATCH of a single backfill — wrapped in {meta, data}.
BACKFILL_SINGLE_BODY: dict[str, Any] = {"meta": _META, "data": BACKFILL_PAYLOAD}

#: The cancelled backfill in the same envelope.
BACKFILL_CANCELLED_BODY: dict[str, Any] = {"meta": _META, "data": BACKFILL_CANCELLED_PAYLOAD}

#: GET the incomplete-backfills collection — wrapped, with `data` a bare array.
BACKFILLS_LIST_BODY: dict[str, Any] = {"meta": _META, "data": [BACKFILL_PAYLOAD]}

#: An empty collection. `data` is a required array on this schema, so empty is `[]`,
#: never a body with the key missing.
BACKFILLS_EMPTY_LIST_BODY: dict[str, Any] = {"meta": _META, "data": []}

# --- Routes, for team 42 / transfer 456789 / backfill 12345 -------------------

#: POST here to create; note it nests under the transfer, unlike the list collection.
CREATE_PATH = "/teams/42/transfers/456789/backfills"

#: GET the most recent backfill for a transfer.
GET_LATEST_PATH = "/teams/42/transfers/456789/backfills/latest"

#: GET (fetch) and PATCH (cancel) both address the backfill by id here.
ITEM_PATH = "/teams/42/backfills/12345"

#: GET the incomplete backfills for a team — a sibling of the by-id path, not a parent
#: of it, so a create that dropped the transfer segment would land here by mistake.
COLLECTION_PATH = "/teams/42/backfills"


class TestBackfillsResource:
    """Synchronous backfill create, fetch, latest, list and cancel."""

    def test_create_returns_the_backfill(self, api_server: MockAPIServer) -> None:
        """Creation answers 200 and returns the persisted backfill, unwrapped."""
        api_server.route(CREATE_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = client.backfills.create(
                team_id=42,
                transfer_id=456789,
                range_start=date(2024, 1, 1),
                range_end=date(2024, 1, 31),
            )

        assert backfill.transfer_backfill_id == 12345
        assert backfill.transfer_id == 456789
        assert backfill.status == "RUNNING"
        assert backfill.range_start_date == date(2024, 1, 1)
        assert backfill.range_end_date == date(2024, 1, 31)

    def test_create_posts_the_date_range_in_the_body(self, api_server: MockAPIServer) -> None:
        """POST to the nested collection, with the range as bare ISO date strings.

        ``range_start`` / ``range_end`` are ``date`` objects on the way in and serialize
        to ``"YYYY-MM-DD"`` — no time component, no envelope — which is what upstream
        expects. The body keys are the request field names, not the response's
        ``range_start_date`` / ``range_end_date``.
        """
        api_server.route(CREATE_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.backfills.create(
                team_id=42,
                transfer_id=456789,
                range_start=date(2024, 1, 1),
                range_end=date(2024, 1, 31),
            )

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == CREATE_PATH
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body == {"range_start": "2024-01-01", "range_end": "2024-01-31"}

    def test_get_returns_the_backfill(self, api_server: MockAPIServer) -> None:
        """The response is ``{meta, data}``; the adapter hands back the backfill itself."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = client.backfills.get(team_id=42, backfill_id=12345)

        assert backfill.transfer_backfill_id == 12345
        assert backfill.transfer_runs_completed == 25
        assert backfill.transfer_runs_failed == 2
        assert backfill.error_report == []

    def test_get_sends_a_get_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """GET on ``/teams/{team}/backfills/{id}`` with no body of its own."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.backfills.get(team_id=42, backfill_id=12345)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_get_latest_returns_the_backfill(self, api_server: MockAPIServer) -> None:
        """``/latest`` returns the most recent backfill for a transfer, unwrapped."""
        api_server.route(GET_LATEST_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = client.backfills.get_latest(team_id=42, transfer_id=456789)

        assert backfill.transfer_backfill_id == 12345
        assert backfill.status == "RUNNING"

    def test_get_latest_hits_the_latest_path_under_the_transfer(self, api_server: MockAPIServer) -> None:
        """GET on the transfer-scoped ``/backfills/latest`` — ``latest`` is not an id."""
        api_server.route(GET_LATEST_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.backfills.get_latest(team_id=42, transfer_id=456789)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == GET_LATEST_PATH
        assert request.path != ITEM_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_incomplete_returns_the_backfills(self, api_server: MockAPIServer) -> None:
        """The list lives under ``data``; the adapter returns the backfills themselves."""
        api_server.route(COLLECTION_PATH, ScriptedResponse(json_body=BACKFILLS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfills = client.backfills.list_incomplete(team_id=42)

        assert len(backfills) == 1
        assert backfills[0].transfer_backfill_id == 12345
        assert backfills[0].status == "RUNNING"

    def test_list_incomplete_sends_no_query_string(self, api_server: MockAPIServer) -> None:
        """The team-scoped collection takes no filters, so no query string goes out.

        This is also where a dropped-transfer-segment bug in ``create`` would surface:
        the two share nothing but this path, and only one of them is a plain GET.
        """
        api_server.route(COLLECTION_PATH, ScriptedResponse(json_body=BACKFILLS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.backfills.list_incomplete(team_id=42)

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == COLLECTION_PATH
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_incomplete_returns_an_empty_list(self, api_server: MockAPIServer) -> None:
        """A team with nothing in flight answers ``{"data": []}`` — an empty list, not an error."""
        api_server.route(COLLECTION_PATH, ScriptedResponse(json_body=BACKFILLS_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfills = client.backfills.list_incomplete(team_id=42)

        assert backfills == []

    def test_cancel_returns_the_cancelled_backfill(self, api_server: MockAPIServer) -> None:
        """Cancel answers 200 with the updated backfill, its removed_* fields now populated."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=BACKFILL_CANCELLED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = client.backfills.cancel(team_id=42, backfill_id=12345)

        assert backfill.status == "CANCELLED"
        assert backfill.removed_user_id == 790
        assert backfill.removed_time is not None

    def test_cancel_patches_the_status_to_cancelled(self, api_server: MockAPIServer) -> None:
        """Cancel is a ``PATCH`` on the by-id path carrying ``{"status": "CANCELLED"}``.

        The caller passes no status — the adapter fixes it to ``CANCELLED``, the only
        value upstream accepts — so the body is asserted in full to prove exactly that
        one key goes out and nothing else.
        """
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=BACKFILL_CANCELLED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.backfills.cancel(team_id=42, backfill_id=12345)

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"
        assert request.json() == {"status": "CANCELLED"}


class TestBackfillsAsyncResource:
    """Asynchronous backfills — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_create_returns_the_backfill_and_posts_the_range(self, api_server: MockAPIServer) -> None:
        """200 on the async path, with the date range serialized on the wire."""
        api_server.route(CREATE_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = await client.backfills.create(
                team_id=42,
                transfer_id=456789,
                range_start=date(2024, 1, 1),
                range_end=date(2024, 1, 31),
            )

        assert backfill.transfer_backfill_id == 12345
        assert backfill.transfer_id == 456789

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == CREATE_PATH
        assert request.bearer_token == "api_k"
        assert request.json() == {"range_start": "2024-01-01", "range_end": "2024-01-31"}

    @pytest.mark.asyncio
    async def test_get_returns_the_backfill(self, api_server: MockAPIServer) -> None:
        """GET on the by-id path, unwrapped to the backfill itself."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = await client.backfills.get(team_id=42, backfill_id=12345)

        assert backfill.transfer_backfill_id == 12345
        assert backfill.transfer_runs_completed == 25

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_get_latest_hits_the_latest_path(self, api_server: MockAPIServer) -> None:
        """``latest`` is its own segment under the transfer, not a backfill id."""
        api_server.route(GET_LATEST_PATH, ScriptedResponse(json_body=BACKFILL_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = await client.backfills.get_latest(team_id=42, transfer_id=456789)

        assert backfill.transfer_backfill_id == 12345

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == GET_LATEST_PATH
        assert request.path != ITEM_PATH

    @pytest.mark.asyncio
    async def test_list_incomplete_returns_the_backfills(self, api_server: MockAPIServer) -> None:
        """The async path unwraps ``data`` and sends no query string identically."""
        api_server.route(COLLECTION_PATH, ScriptedResponse(json_body=BACKFILLS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfills = await client.backfills.list_incomplete(team_id=42)

        assert len(backfills) == 1
        assert backfills[0].transfer_backfill_id == 12345

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == COLLECTION_PATH
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_list_incomplete_returns_an_empty_list(self, api_server: MockAPIServer) -> None:
        """An absent-in-flight team answers ``[]`` on the async path too."""
        api_server.route(COLLECTION_PATH, ScriptedResponse(json_body=BACKFILLS_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfills = await client.backfills.list_incomplete(team_id=42)

        assert backfills == []

    @pytest.mark.asyncio
    async def test_cancel_patches_the_status_to_cancelled(self, api_server: MockAPIServer) -> None:
        """The PATCH-with-``CANCELLED`` contract holds on the async client as well."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=BACKFILL_CANCELLED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            backfill = await client.backfills.cancel(team_id=42, backfill_id=12345)

        assert backfill.status == "CANCELLED"
        assert backfill.removed_user_id == 790

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"
        assert request.json() == {"status": "CANCELLED"}
