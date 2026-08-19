"""End-to-end tests for Data Warehouse host routing.

Transfers, transfer runs, backfills, data source connections and destinations are
served from ``dts-api.supermetrics.com``, not from the core API host. The SDK re-hosts those
requests from an ``httpx`` request event hook so one pooled client can serve both.

That behaviour only exists on the wire, and only a *second* server can prove it: a test
with one server cannot tell "sent to the right host" apart from "sent to the only host
there is". So every test here runs two independent ``MockAPIServer`` instances and
asserts which one received the request.
"""

from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics._transport import DEFAULT_BASE_URL, DEFAULT_DTS_BASE_URL, resolve_dts_base_url

from .conftest import (
    LOGINS_LIST_BODY,
    TRANSFER_RUN_DETAIL_BODY,
    TRANSFERS_LIST_BODY,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e


class TestDtsBaseUrlResolution:
    """Which base URL Data Warehouse traffic is sent to, and when."""

    def test_production_default_routes_to_the_dts_host(self) -> None:
        """An unconfigured production client sends Data Warehouse calls to dts-api."""
        assert resolve_dts_base_url(DEFAULT_BASE_URL, None) == DEFAULT_DTS_BASE_URL

    def test_trailing_slash_is_still_the_default(self) -> None:
        """A trailing slash does not defeat the production check."""
        assert resolve_dts_base_url(DEFAULT_BASE_URL + "/", None) == DEFAULT_DTS_BASE_URL

    def test_custom_base_url_disables_routing(self) -> None:
        """A caller who names a base URL gets all of their traffic sent to it."""
        assert resolve_dts_base_url("http://127.0.0.1:9999", None) is None

    def test_legacy_dts_base_url_is_left_alone(self) -> None:
        """The pre-0.5 backfills workaround keeps working, unmolested.

        Callers were told to build a second client on the dts host. Routing on top of
        that would double the ``/v1`` prefix, so an explicit base URL is taken literally.
        """
        assert resolve_dts_base_url(DEFAULT_DTS_BASE_URL, None) is None

    def test_explicit_override_wins(self) -> None:
        """An explicit dts_base_url is used regardless of the core base URL."""
        assert resolve_dts_base_url("http://127.0.0.1:1", "http://127.0.0.1:2/v1") == "http://127.0.0.1:2/v1"


class TestRequestsReachTheRightHost:
    """Two servers; assert which one got the request."""

    def test_transfers_go_to_the_dts_server(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """A transfers call lands on the Data Warehouse server, under its path prefix."""
        dts_server.route("/v1/teams/42/transfers", ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            transfers = client.transfers.list(team_id=42)

        assert len(transfers) == 1
        assert api_server.requests == [], "the core server must not have seen this request"
        assert dts_server.last_request.path == "/v1/teams/42/transfers"

    def test_core_calls_stay_on_the_core_server(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """A non-Data-Warehouse call is untouched by routing."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY))

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.logins.list()

        assert dts_server.requests == [], "the DTS server must not have seen this request"
        assert api_server.last_request.path == "/ds/logins"

    def test_one_client_serves_both_hosts(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """The whole point: no second client, no second connection pool."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY))
        dts_server.route("/v1/teams/42/transfers", ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.logins.list()
            client.transfers.list(team_id=42)
            client.logins.list()

        assert [r.path for r in api_server.requests] == ["/ds/logins", "/ds/logins"]
        assert [r.path for r in dts_server.requests] == ["/v1/teams/42/transfers"]

    def test_backfills_are_routed_too(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """Backfills share the Data Warehouse host and stop needing a second client.

        Before routing existed, ``client.backfills.*`` on a default client 404'd against
        the core API unless the caller followed the documented base_url workaround.
        """
        dts_server.route(
            "/v1/teams/42/backfills",
            ScriptedResponse(json_body={"meta": {"request_id": "req_0123456789ab"}, "data": []}),
        )

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.backfills.list_incomplete(team_id=42)

        assert api_server.requests == []
        assert dts_server.last_request.path == "/v1/teams/42/backfills"

    def test_destinations_are_routed_too(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """Destinations share the Data Warehouse host with transfers.

        ``_DTS_PATH_PATTERN`` has to name every Data Warehouse segment explicitly, so a
        new resource is only routed once it is added to it. Without that, every
        destinations call resolves the DTS base URL, is never re-hosted, and 404s
        against the core API.
        """
        dts_server.route(
            "/v1/teams/42/destinations",
            ScriptedResponse(
                json_body={
                    "meta": {"request_id": "req_0123456789ab"},
                    "data": [{"id": 8, "display_name": "Analytics warehouse", "type": "DWH_SNOWFLAKE"}],
                }
            ),
        )

        with SupermetricsClient(
            api_key="not-a-real-key",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            destinations = client.destinations.list(team_id=42)

        assert len(destinations) == 1
        assert api_server.requests == [], "the core server must not have seen this request"
        assert dts_server.last_request.path == "/v1/teams/42/destinations"

    def test_destination_usage_is_routed_too(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """A sub-path of a destination item is routed as well, not only the collection.

        The pattern matches on the segment after the team id and then anything below it,
        so ``/destinations/{id}/usage`` has to travel to the same host.
        """
        dts_server.route(
            "/v1/teams/42/destinations/8/usage",
            ScriptedResponse(
                json_body={
                    "meta": {"request_id": "req_0123456789ab"},
                    "data": {"is_used": False, "transfers": []},
                }
            ),
        )

        with SupermetricsClient(
            api_key="not-a-real-key",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            usage = client.destinations.get_usage(team_id=42, destination_id=8)

        assert usage.is_used is False
        assert api_server.requests == [], "the core server must not have seen this request"
        assert dts_server.last_request.path == "/v1/teams/42/destinations/8/usage"

    def test_datasource_details_is_not_routed(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """``/teams/{id}/datasource/...`` shares the prefix but is a core-API route.

        This is the one that a naive ``/teams/`` prefix rule would get wrong.
        """
        api_server.route(
            "/teams/42/datasource/GAWA",
            ScriptedResponse(
                json_body={
                    "meta": {"request_id": "req_0123456789ab"},
                    "data": {
                        "id": "GAWA",
                        "name": "Google Analytics 4",
                        "status": "Released",
                        "is_authentication_required": True,
                        "has_account_list": True,
                        "has_fields": True,
                    },
                }
            ),
        )

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.datasource_details.get(team_id=42, data_source_id="GAWA")

        assert dts_server.requests == []
        assert api_server.last_request.path == "/teams/42/datasource/GAWA"

    def test_account_tags_are_not_routed(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """``/v1/teams/{id}/account_tags`` is a core-API route, not a Data Warehouse one.

        Account tags live on the core host with ``/v1`` in the path, like custom fields.
        The DTS pattern is anchored ``^/teams/`` and its alternation is
        ``transfers|transfer_runs|backfills|data-source-connections`` — so a
        ``/v1/teams/…/account_tags`` path cannot match on either count. This asserts that
        positively, the way transfers assert the opposite, rather than leaving it to
        "there is only one server."
        """
        api_server.route(
            "/v1/teams/42/account_tags",
            ScriptedResponse(json_body={"data": []}),
        )

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.account_tags.list(team_id=42)

        assert dts_server.requests == [], "the DTS server must not have seen this request"
        assert api_server.last_request.path == "/v1/teams/42/account_tags"

    def test_unset_dts_base_url_sends_everything_to_base_url(
        self, api_server: MockAPIServer, dts_server: MockAPIServer
    ) -> None:
        """With a custom base_url and no override, nothing is re-hosted.

        This is what keeps every other e2e test in this suite pointed at one server.
        """
        api_server.route("/teams/42/transfers", ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.list(team_id=42)

        assert dts_server.requests == []
        assert api_server.last_request.path == "/teams/42/transfers"


class TestRoutingPreservesTheRequest:
    """Re-hosting must not lose the query string, the credential, or the headers."""

    def test_query_string_survives(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """Rewriting scheme, host and path keeps the query intact."""
        dts_server.route(
            "/v1/teams/42/transfers/36091/runs",
            ScriptedResponse(json_body={"meta": {"request_id": "req_0123456789ab"}, "data": []}),
        )

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.transfers.list_runs(
                team_id=42,
                transfer_id=36091,
                start_date=datetime(2026, 1, 1, tzinfo=UTC),
                end_date=datetime(2026, 1, 31, tzinfo=UTC),
                limit=25,
                offset=50,
            )

        parts = urlsplit(dts_server.last_request.path)
        assert parts.path == "/v1/teams/42/transfers/36091/runs"
        query = parse_qs(parts.query)
        assert query["limit"] == ["25"]
        assert query["offset"] == ["50"]

    def test_credential_and_headers_survive(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """Auth is applied after routing, and per-request headers still reach the host."""
        dts_server.route("/v1/teams/42/transfers", ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.transfers.list(
                team_id=42,
                auth_token="otok_per_call",
                headers={"X-Span-Id": "span-dts"},
            )

        received = dts_server.last_request
        assert received.bearer_token == "otok_per_call"
        assert received.headers["x-span-id"] == "span-dts"

    def test_host_header_names_the_new_origin(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """The Host header is rewritten, not left pointing at the core API.

        httpx derives Host when it builds the request, so without an explicit fix the
        re-hosted request would arrive advertising the wrong origin — which a real
        virtual-hosted gateway would reject.
        """
        dts_server.route("/v1/teams/42/transfers", ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            client.transfers.list(team_id=42)

        expected = dts_server.base_url.removeprefix("http://")
        assert dts_server.last_request.headers["host"] == expected


class TestAsyncRouting:
    """The async client shares the rule, through its own hook."""

    @pytest.mark.asyncio
    async def test_transfers_go_to_the_dts_server(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """Routing applies on the async path too."""
        dts_server.route("/v1/teams/42/transfers", ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        async with SupermetricsAsyncClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            transfers = await client.transfers.list(team_id=42)

        assert len(transfers) == 1
        assert api_server.requests == []
        assert dts_server.last_request.path == "/v1/teams/42/transfers"

    @pytest.mark.asyncio
    async def test_async_client_serves_both_hosts(self, api_server: MockAPIServer, dts_server: MockAPIServer) -> None:
        """One async client, two origins, one pool."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY))
        dts_server.route("/v1/teams/42/transfer_runs/12345", ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        async with SupermetricsAsyncClient(
            api_key="api_k",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            await client.logins.list()
            run = await client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert run.id == 12345
        assert api_server.last_request.path == "/ds/logins"
        assert dts_server.last_request.path == "/v1/teams/42/transfer_runs/12345"

    @pytest.mark.asyncio
    async def test_destinations_go_to_the_dts_server(
        self, api_server: MockAPIServer, dts_server: MockAPIServer
    ) -> None:
        """The destinations collection is re-hosted on the async client too."""
        dts_server.route(
            "/v1/teams/42/destinations",
            ScriptedResponse(
                json_body={
                    "meta": {"request_id": "req_0123456789ab"},
                    "data": [{"id": 8, "display_name": "Analytics warehouse", "type": "DWH_SNOWFLAKE"}],
                }
            ),
        )

        async with SupermetricsAsyncClient(
            api_key="not-a-real-key",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            destinations = await client.destinations.list(team_id=42)

        assert len(destinations) == 1
        assert api_server.requests == [], "the core server must not have seen this request"
        assert dts_server.last_request.path == "/v1/teams/42/destinations"

    @pytest.mark.asyncio
    async def test_destination_usage_goes_to_the_dts_server(
        self, api_server: MockAPIServer, dts_server: MockAPIServer
    ) -> None:
        """The usage sub-path is re-hosted by the async request hook as well."""
        dts_server.route(
            "/v1/teams/42/destinations/8/usage",
            ScriptedResponse(
                json_body={
                    "meta": {"request_id": "req_0123456789ab"},
                    "data": {
                        "is_used": True,
                        "transfers": [{"transfer_id": 36091, "transfer_name": "Google Ads to BigQuery"}],
                    },
                }
            ),
        )

        async with SupermetricsAsyncClient(
            api_key="not-a-real-key",
            base_url=api_server.base_url,
            dts_base_url=f"{dts_server.base_url}/v1",
        ) as client:
            usage = await client.destinations.get_usage(team_id=42, destination_id=8)

        assert usage.is_used is True
        assert usage.transfers[0].transfer_id == 36091
        assert api_server.requests == [], "the core server must not have seen this request"
        assert dts_server.last_request.path == "/v1/teams/42/destinations/8/usage"
