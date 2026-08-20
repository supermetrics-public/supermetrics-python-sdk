"""End-to-end tests for the Queries resource.

Drives both public methods — ``execute`` and ``get_results`` — over a real loopback
socket. Queries stay on the core API host and both methods hit the single endpoint
``GET /query/data/json``; there is no re-hosting to the Data Warehouse host, so one
server is the whole story here.

The one fact this layer exists to pin down: despite the resource building a ``DataQuery``
that reads like a request *body*, the generated endpoint serializes that model into the
**query string** of a **GET** and sends an empty body. A mocked transport cannot see that
``ds_accounts`` and ``fields`` go out as repeated query params, that ``execute`` forwards
``max_rows`` as a bare int, or that ``get_results`` sends ``schedule_id`` alongside an
empty ``ds_id``. So every method gets a return-value test and an outgoing-request test.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: The single endpoint both methods hit. Both `execute` and `get_results` are GETs here.
QUERY_ENDPOINT = "/query/data/json"

#: A completed query as `GET /query/data/json` answers it. `data` is a list of rows, each
#: row a list of strings — the API returns every cell as a string, numbers included.
DATA_RESPONSE_BODY: dict[str, Any] = {
    "meta": {
        "request_id": "req_0123456789abcdef",
        "schedule_id": "sched_abc123",
        "status_code": "success",
    },
    "data": [
        ["2025-01-01", "1200", "800"],
        ["2025-01-02", "1500", "950"],
    ],
}

#: A query that completed with no matching rows. `data` is an empty list, not absent — the
#: adapter must hand that straight back rather than mistake it for "no response".
EMPTY_DATA_RESPONSE_BODY: dict[str, Any] = {
    "meta": {"request_id": "req_empty", "status_code": "success"},
    "data": [],
}

#: An async query still running. `status_code` is "pending" and there is no `data` key at
#: all — this is the response a caller polls `get_results` against.
PENDING_RESPONSE_BODY: dict[str, Any] = {
    "meta": {"request_id": "req_pending_1", "status_code": "pending"},
}

#: The same query, now finished, as `get_results` retrieves it. `schedule_id` echoes the
#: id the poll asked for.
RESULTS_RESPONSE_BODY: dict[str, Any] = {
    "meta": {
        "request_id": "req_pending_1",
        "schedule_id": "req_pending_1",
        "status_code": "success",
    },
    "data": [
        ["2025-01-01", "42"],
    ],
}


class TestQueriesResource:
    """Synchronous query execution and result polling."""

    def test_execute_returns_meta_and_data(self, api_server: MockAPIServer) -> None:
        """A 200 parses into a ``DataResponse`` with metadata and the row grid."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=DATA_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345", "67890"],
                fields=["sessions", "users"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert result is not None
        assert result.meta.request_id == "req_0123456789abcdef"
        assert result.meta.status_code == "success"
        assert result.data == [
            ["2025-01-01", "1200", "800"],
            ["2025-01-02", "1500", "950"],
        ]

    def test_execute_sends_a_get_with_the_query_in_the_query_string(self, api_server: MockAPIServer) -> None:
        """The ``DataQuery`` goes out as query params on a GET with an empty body.

        This is the whole point of the layer: the resource builds a model that reads like
        a request body, but the generated endpoint serializes it into the query string of
        a GET. ``ds_accounts`` and ``fields`` are lists, so each becomes a repeated param.
        """
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=DATA_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345", "67890"],
                fields=["sessions", "users"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == QUERY_ENDPOINT
        assert request.bearer_token == "api_k"
        assert request.body == b""

        query = parse_qs(urlsplit(request.path).query)
        assert query == {
            "ds_id": ["GAWA"],
            "ds_accounts": ["12345", "67890"],
            "fields": ["sessions", "users"],
            "start_date": ["2025-01-01"],
            "end_date": ["2025-01-31"],
        }

    def test_execute_forwards_extra_kwargs_as_query_params(self, api_server: MockAPIServer) -> None:
        """``**kwargs`` map onto declared ``DataQuery`` fields and reach the wire.

        ``max_rows`` and ``cache_minutes`` are ints upstream, so they serialize as their
        decimal strings; ``filter_`` is renamed to the reserved word ``filter`` on the way
        out. The three transport-override keywords are consumed by the SDK and must not
        leak into the query string.
        """
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=DATA_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345"],
                fields=["sessions"],
                start_date="yesterday",
                end_date="yesterday",
                max_rows=1000,
                cache_minutes=30,
                filter_="sessions>100",
            )

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query["max_rows"] == ["1000"]
        assert query["cache_minutes"] == ["30"]
        assert query["filter"] == ["sessions>100"]
        assert "filter_" not in query
        # The reserved transport overrides never travel as query params.
        assert "auth_token" not in query
        assert "headers" not in query
        assert "timeout" not in query

    def test_execute_returns_an_empty_grid_when_the_query_matched_no_rows(self, api_server: MockAPIServer) -> None:
        """An empty ``data`` array is a real result, not a missing response."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=EMPTY_DATA_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert result is not None
        assert result.data == []
        assert result.meta.status_code == "success"

    def test_execute_surfaces_a_pending_status_for_async_queries(self, api_server: MockAPIServer) -> None:
        """A pending query returns a request id to poll and no data grid.

        The status drives the async polling contract documented on ``execute``: a caller
        reads ``meta.status_code == "pending"`` and feeds ``meta.request_id`` to
        ``get_results``.
        """
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=PENDING_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert result is not None
        assert result.meta.status_code == "pending"
        assert result.meta.request_id == "req_pending_1"

    def test_get_results_returns_the_completed_data(self, api_server: MockAPIServer) -> None:
        """Polling a finished query yields its rows and a non-pending status."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=RESULTS_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.queries.get_results(query_id="req_pending_1")

        assert result is not None
        assert result.meta.status_code == "success"
        assert result.meta.schedule_id == "req_pending_1"
        assert result.data == [["2025-01-01", "42"]]

    def test_get_results_sends_schedule_id_with_an_empty_ds_id(self, api_server: MockAPIServer) -> None:
        """Result retrieval is a GET carrying ``schedule_id`` and a blank ``ds_id``.

        The adapter reuses the same ``DataQuery`` model, setting ``schedule_id`` to the
        query id and leaving ``ds_id`` as the empty string it is required to send. Because
        the empty string is neither ``UNSET`` nor ``None``, it survives the endpoint's
        param filter and reaches the wire as a blank-valued key — so ``keep_blank_values``
        is needed to see it.
        """
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=RESULTS_RESPONSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.queries.get_results(query_id="req_pending_1")

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == QUERY_ENDPOINT
        assert request.bearer_token == "api_k"
        assert request.body == b""

        query = parse_qs(urlsplit(request.path).query, keep_blank_values=True)
        assert query == {"ds_id": [""], "schedule_id": ["req_pending_1"]}


class TestQueriesAsyncResource:
    """Asynchronous query execution — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_execute_returns_meta_and_data(self, api_server: MockAPIServer) -> None:
        """The async path parses the ``DataResponse`` identically."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=DATA_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345", "67890"],
                fields=["sessions", "users"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert result is not None
        assert result.meta.request_id == "req_0123456789abcdef"
        assert result.data == [
            ["2025-01-01", "1200", "800"],
            ["2025-01-02", "1500", "950"],
        ]

    @pytest.mark.asyncio
    async def test_execute_sends_a_get_with_the_query_in_the_query_string(self, api_server: MockAPIServer) -> None:
        """GET with the model serialized into repeated query params and an empty body."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=DATA_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345", "67890"],
                fields=["sessions", "users"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == QUERY_ENDPOINT
        assert request.bearer_token == "api_k"
        assert request.body == b""

        query = parse_qs(urlsplit(request.path).query)
        assert query == {
            "ds_id": ["GAWA"],
            "ds_accounts": ["12345", "67890"],
            "fields": ["sessions", "users"],
            "start_date": ["2025-01-01"],
            "end_date": ["2025-01-31"],
        }

    @pytest.mark.asyncio
    async def test_execute_returns_an_empty_grid_when_the_query_matched_no_rows(
        self, api_server: MockAPIServer
    ) -> None:
        """An empty ``data`` array is a real result on the async path too."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=EMPTY_DATA_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.queries.execute(
                ds_id="GAWA",
                ds_accounts=["12345"],
                fields=["sessions"],
                start_date="2025-01-01",
                end_date="2025-01-31",
            )

        assert result is not None
        assert result.data == []

    @pytest.mark.asyncio
    async def test_get_results_returns_the_completed_data(self, api_server: MockAPIServer) -> None:
        """Polling a finished query yields its rows on the async client."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=RESULTS_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.queries.get_results(query_id="req_pending_1")

        assert result is not None
        assert result.meta.status_code == "success"
        assert result.data == [["2025-01-01", "42"]]

    @pytest.mark.asyncio
    async def test_get_results_sends_schedule_id_with_an_empty_ds_id(self, api_server: MockAPIServer) -> None:
        """The ``schedule_id`` + blank ``ds_id`` contract holds on the async client."""
        api_server.route(QUERY_ENDPOINT, ScriptedResponse(json_body=RESULTS_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.queries.get_results(query_id="req_pending_1")

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == QUERY_ENDPOINT
        assert request.bearer_token == "api_k"
        assert request.body == b""

        query = parse_qs(urlsplit(request.path).query, keep_blank_values=True)
        assert query == {"ds_id": [""], "schedule_id": ["req_pending_1"]}
