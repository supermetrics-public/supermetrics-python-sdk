"""End-to-end tests for the Connector Builder Logs resource.

Drives both public methods — ``list`` and ``get`` — over a real loopback socket.
Connector builder logs stay on the core API host, so the paths keep their ``/v1``
prefix and there is no re-hosting to the Data Warehouse host; one server is the
whole story here.

Two facts about this endpoint that only the wire can prove, and which these tests
pin down:

* The list response is a *bare* ``{"logs": [...]}`` object — not the ``{"data": ...}``
  or ``{"meta": ..., "data": ...}`` envelope most other resources use — and ``logs``
  is a required field, so an empty page is ``{"logs": []}`` rather than an absent key.
* ``limit`` defaults to ``100`` down in the generated layer, but the adapter forwards
  ``UNSET`` when the caller omits it, so a bare ``list()`` must send *no* query string
  at all rather than a ``limit=100`` the SDK invented.

Every method gets a return-value test and an outgoing-request test; the request half
is the point of this layer, since a mocked transport cannot see the ``/v1`` prefix, the
query serialization, or the bearer token that actually went out.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from urllib.parse import parse_qs, urlsplit
from uuid import UUID

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

# --- Routes -------------------------------------------------------------------
#
# The ``/v1`` prefix is load-bearing: it is added by the generated endpoint, not by
# the adapter's own ``endpoint`` string (which is used only for error context). A
# dropped prefix would surface as the server's default 404, not an obvious mistake.
LOGS_COLLECTION = "/v1/teams/42/connector_builder/connectors/my-connector/logs"
LOGS_ITEM = "/v1/teams/42/connector_builder/connectors/my-connector/logs/log-abc123"

# --- Payloads -----------------------------------------------------------------

#: One log entry with every field populated. ``request_id`` is a UUID upstream, so the
#: generated model parses it into a :class:`uuid.UUID`; ``log_time`` uses a trailing
#: ``Z`` which ``datetime.fromisoformat`` accepts on Python 3.11+.
LOG_ENTRY_PAYLOAD: dict[str, Any] = {
    "id": "123-foo",
    "log_time": "2025-01-01T00:00:00Z",
    "status": 200,
    "event": "auth.token.refresh",
    "request": "POST /api/oauth/token_refresh",
    "duration_ms": 253,
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
}

#: The detail entry returned by ``get``. ``status`` and ``event`` are null here to
#: exercise the nullable unions — both must parse to ``None``, not to ``UNSET`` or a
#: parse error.
LOG_ENTRY_DETAIL_PAYLOAD: dict[str, Any] = {
    "id": "log-abc123",
    "log_time": "2025-01-02T12:30:45Z",
    "status": None,
    "event": None,
    "request": "GET /api/data",
    "duration_ms": 42,
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
}

#: GET the collection — a bare ``{"logs": [...]}`` object, no ``data`` envelope.
LOGS_LIST_BODY: dict[str, Any] = {"logs": [LOG_ENTRY_PAYLOAD]}

#: An empty page. ``logs`` is required upstream, so empty is ``[]``, never an absent key.
LOGS_EMPTY_LIST_BODY: dict[str, Any] = {"logs": []}

#: GET a single entry — the ``LogEntry`` object itself, unwrapped.
LOG_GET_BODY: dict[str, Any] = LOG_ENTRY_DETAIL_PAYLOAD


class TestConnectorBuilderLogsResource:
    """Synchronous connector builder log listing and retrieval."""

    def test_list_returns_the_logs(self, api_server: MockAPIServer) -> None:
        """The bare ``{"logs": [...]}`` body is unwrapped to typed ``LogEntry`` objects."""
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_logs.list(team_id=42, connector_identifier="my-connector")

        assert len(result.logs) == 1
        entry = result.logs[0]
        assert entry.id == "123-foo"
        assert entry.log_time == datetime(2025, 1, 1, tzinfo=UTC)
        assert entry.status == 200
        assert entry.event == "auth.token.refresh"
        assert entry.request == "POST /api/oauth/token_refresh"
        assert entry.duration_ms == 253
        assert entry.request_id == UUID("550e8400-e29b-41d4-a716-446655440000")

    def test_list_without_options_sends_no_query_string(self, api_server: MockAPIServer) -> None:
        """A bare ``list()`` sends no query string at all.

        The generated layer defaults ``limit`` to 100, but the adapter forwards
        ``UNSET`` when the caller omits it, so the server sees whatever *it* considers
        the default page size rather than a number the SDK invented.
        """
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_logs.list(team_id=42, connector_identifier="my-connector")

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_serializes_limit_and_before(self, api_server: MockAPIServer) -> None:
        """A string ``before`` is round-tripped through ``fromisoformat``/``isoformat``.

        The adapter accepts ``before`` as an ISO string, parses it to a ``datetime`` and
        the generated layer serializes it back with ``isoformat()``; ``limit`` is an int
        that reaches the wire as a string.
        """
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_logs.list(
                team_id=42,
                connector_identifier="my-connector",
                limit=10,
                before="2026-01-01T00:00:00+00:00",
            )

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {
            "limit": ["10"],
            "before": ["2026-01-01T00:00:00+00:00"],
        }

    def test_list_serializes_a_datetime_before(self, api_server: MockAPIServer) -> None:
        """An aware ``datetime`` ``before`` serializes identically to the string form."""
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_logs.list(
                team_id=42,
                connector_identifier="my-connector",
                before=datetime(2026, 1, 1, tzinfo=UTC),
            )

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {"before": ["2026-01-01T00:00:00+00:00"]}

    def test_list_returns_an_empty_list_when_there_are_no_logs(self, api_server: MockAPIServer) -> None:
        """``{"logs": []}`` yields an empty ``logs`` list, not an error."""
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_logs.list(team_id=42, connector_identifier="my-connector")

        assert result.logs == []

    def test_get_returns_the_log_entry(self, api_server: MockAPIServer) -> None:
        """The response is a bare ``LogEntry``; nullable ``status``/``event`` parse to ``None``."""
        api_server.route(LOGS_ITEM, ScriptedResponse(json_body=LOG_GET_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            entry = client.connector_builder_logs.get(
                team_id=42, connector_identifier="my-connector", log_id="log-abc123"
            )

        assert entry.id == "log-abc123"
        assert entry.log_time == datetime(2025, 1, 2, 12, 30, 45, tzinfo=UTC)
        assert entry.status is None
        assert entry.event is None
        assert entry.request == "GET /api/data"
        assert entry.duration_ms == 42
        assert entry.request_id == UUID("550e8400-e29b-41d4-a716-446655440000")

    def test_get_sends_a_get_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """GET on ``.../logs/{log_id}`` with no query string and no body."""
        api_server.route(LOGS_ITEM, ScriptedResponse(json_body=LOG_GET_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_logs.get(team_id=42, connector_identifier="my-connector", log_id="log-abc123")

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGS_ITEM
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""


class TestConnectorBuilderLogsAsyncResource:
    """Asynchronous connector builder logs — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_the_logs(self, api_server: MockAPIServer) -> None:
        """The async path unwraps the bare ``logs`` array identically."""
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_logs.list(team_id=42, connector_identifier="my-connector")

        assert len(result.logs) == 1
        assert result.logs[0].id == "123-foo"
        assert result.logs[0].request_id == UUID("550e8400-e29b-41d4-a716-446655440000")

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_list_serializes_limit_and_before(self, api_server: MockAPIServer) -> None:
        """Query serialization does not differ between the two clients."""
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.connector_builder_logs.list(
                team_id=42,
                connector_identifier="my-connector",
                limit=10,
                before="2026-01-01T00:00:00+00:00",
            )

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {
            "limit": ["10"],
            "before": ["2026-01-01T00:00:00+00:00"],
        }

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_list_when_there_are_no_logs(self, api_server: MockAPIServer) -> None:
        """An empty ``logs`` array is an empty page on the async path too."""
        api_server.route(LOGS_COLLECTION, ScriptedResponse(json_body=LOGS_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_logs.list(team_id=42, connector_identifier="my-connector")

        assert result.logs == []

    @pytest.mark.asyncio
    async def test_get_returns_the_log_entry(self, api_server: MockAPIServer) -> None:
        """GET on the by-id path, unwrapped to the ``LogEntry`` itself."""
        api_server.route(LOGS_ITEM, ScriptedResponse(json_body=LOG_GET_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            entry = await client.connector_builder_logs.get(
                team_id=42, connector_identifier="my-connector", log_id="log-abc123"
            )

        assert entry.id == "log-abc123"
        assert entry.log_time == datetime(2025, 1, 2, 12, 30, 45, tzinfo=UTC)
        assert entry.status is None
        assert entry.event is None

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGS_ITEM
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_get_sends_a_get_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """The by-id path and empty body hold on the async client as well."""
        api_server.route(LOGS_ITEM, ScriptedResponse(json_body=LOG_GET_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.connector_builder_logs.get(
                team_id=42, connector_identifier="my-connector", log_id="log-abc123"
            )

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGS_ITEM
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""
