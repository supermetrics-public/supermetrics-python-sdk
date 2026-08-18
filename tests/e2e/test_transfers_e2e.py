"""End-to-end tests for the Transfers resource.

Drives the whole stack over a real loopback socket. Every test asserts on what went
*out* — verb, path, query string, body, credential — not only on what came back, because
the request is the half a mocked transport cannot check.

The response envelope is deliberately inconsistent upstream: ``list``, ``create``,
``list_runs`` and ``create_datasource_connection`` answer ``{"meta": ..., "data": ...}``
and the adapter returns ``.data``, while ``get``, ``update``, ``set_state``, the two
validations and the two lookups answer bare. Both shapes are pinned here.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from urllib.parse import parse_qs, urlsplit
from uuid import UUID

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics._generated.supermetrics_api_client.models.transfer_account import TransferAccount
from supermetrics._generated.supermetrics_api_client.models.transfer_schedule import TransferSchedule
from supermetrics.exceptions import (
    NetworkError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

from .conftest import (
    AVAILABLE_SOURCES_BODY,
    DATA_SOURCE_CONNECTION_BODY,
    TRANSFER_CREATED_BODY,
    TRANSFER_DETAIL_BODY,
    TRANSFER_OPTIONS_BODY,
    TRANSFER_RUNS_LIST_BODY,
    TRANSFER_STATE_BODY,
    TRANSFER_UPDATED_BODY,
    TRANSFERS_LIST_BODY,
    VALIDATION_FAILED_BODY,
    VALIDATION_OK_BODY,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e

TEAM_ID = 42
TRANSFER_ID = 36091

#: One route serves every verb, so paths that collections and items share — ``TRANSFERS``
#: for GET and POST, ``TRANSFER`` for GET, PUT and DELETE — need a response *sequence*
#: whenever a single test exercises more than one of them.
TRANSFERS = f"/teams/{TEAM_ID}/transfers"
TRANSFER = f"{TRANSFERS}/{TRANSFER_ID}"
STATE = f"{TRANSFER}/state"
VALIDATIONS = f"{TRANSFERS}/validations"
UPDATE_VALIDATIONS = f"{TRANSFER}/validations"
AVAILABLE_SOURCES = f"{TRANSFERS}/available-sources"
AVAILABLE_OPTIONS = f"{TRANSFERS}/available-options"
RUNS = f"{TRANSFER}/runs"
CONNECTIONS = f"/teams/{TEAM_ID}/data-source-connections"

START_DATE = datetime(2026, 1, 1, tzinfo=UTC)
END_DATE = datetime(2026, 1, 31, tzinfo=UTC)

#: The exact JSON a configuration built from :func:`_configuration` serialises to. Every
#: optional field is left ``UNSET`` and must therefore be absent from the wire body.
EXPECTED_CONFIG_BODY: dict[str, Any] = {
    "data_source_id": "AW",
    "schema_id": 99999,
    "destination_id": 8,
    "display_name": "Google Ads to BigQuery",
    "schedule": [{"run_interval": "daily", "run_hour": 22, "refresh_window": 1}],
    "accounts": [{"data_source_username": "ads@example.com", "login_id": 2682599, "account_id": "8733197711"}],
}


def _configuration() -> dict[str, Any]:
    """Build the six required configuration arguments shared by create/update/validate."""
    return {
        "data_source_id": "AW",
        "schema_id": 99999,
        "destination_id": 8,
        "display_name": "Google Ads to BigQuery",
        "schedule": [TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)],
        "accounts": [
            TransferAccount(data_source_username="ads@example.com", login_id=2682599, account_id="8733197711")
        ],
    }


def _error_envelope(code: str, message: str) -> dict[str, object]:
    """Build an upstream error payload in the envelope the generated models require."""
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


def _query(path: str) -> dict[str, list[str]]:
    """Parse the query string off a recorded request path."""
    return parse_qs(urlsplit(path).query)


class TestTransfersResource:
    """Synchronous transfers — all twelve methods, both directions on the wire."""

    def test_list_returns_the_unwrapped_list_items(self, api_server: MockAPIServer) -> None:
        """The envelope is stripped and the items keep their list-item shape."""
        api_server.route(TRANSFERS, ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            transfers = client.transfers.list(team_id=TEAM_ID)

        assert len(transfers) == 1
        # The list item is identified by dwh_transfer_id; only the detail object below
        # calls it transfer_id. Conflating the two is the bug this pins down.
        assert transfers[0].dwh_transfer_id == TRANSFER_ID
        assert not hasattr(transfers[0], "transfer_id")
        assert transfers[0].display_name == "Google Ads to BigQuery"
        assert transfers[0].schedule == "daily"
        assert transfers[0].accounts == ["8733197711"]

    def test_list_sends_a_get_to_the_collection(self, api_server: MockAPIServer) -> None:
        """No query string, no body, client credential."""
        api_server.route(TRANSFERS, ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.list(team_id=TEAM_ID)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == TRANSFERS
        assert request.body == b""
        assert request.bearer_token == "api_k"

    def test_get_returns_the_bare_configuration(self, api_server: MockAPIServer) -> None:
        """The detail response has no envelope; the model itself comes back."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            configuration = client.transfers.get(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        assert configuration.transfer_id == TRANSFER_ID
        assert configuration.schema_id == 99999
        assert configuration.destination_id == 8
        assert configuration.schedule[0].run_interval == "daily"
        assert configuration.accounts[0].account_id == "8733197711"

    def test_get_sends_a_get_to_the_item(self, api_server: MockAPIServer) -> None:
        """Path carries the transfer id, verb is GET."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.get(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == TRANSFER
        assert request.body == b""
        assert request.bearer_token == "api_k"

    def test_create_succeeds_on_201(self, api_server: MockAPIServer) -> None:
        """Creation answers 201, not 200, and the envelope is unwrapped."""
        api_server.route(TRANSFERS, ScriptedResponse(status=201, json_body=TRANSFER_CREATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            created = client.transfers.create(team_id=TEAM_ID, **_configuration())

        assert created.transfer_id == TRANSFER_ID
        assert created.transfer_name == "Google Ads to BigQuery"

    def test_create_sends_the_six_required_fields(self, api_server: MockAPIServer) -> None:
        """The body carries every required field and nothing that was left unset."""
        api_server.route(TRANSFERS, ScriptedResponse(status=201, json_body=TRANSFER_CREATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.create(team_id=TEAM_ID, **_configuration())

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == TRANSFERS
        assert request.json() == EXPECTED_CONFIG_BODY
        assert request.bearer_token == "api_k"

    def test_create_sends_the_optional_fields_when_given(self, api_server: MockAPIServer) -> None:
        """Optional arguments are only serialised when the caller supplies them."""
        api_server.route(TRANSFERS, ScriptedResponse(status=201, json_body=TRANSFER_CREATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.create(
                team_id=TEAM_ID,
                **_configuration(),
                notification_recipients=["ops@example.com"],
                transfer_type=1,
            )

        body = api_server.last_request.json()
        assert body["notification_recipients"] == ["ops@example.com"]
        assert body["transfer_type"] == 1
        assert "segments" not in body
        assert "data_source_settings" not in body

    def test_update_returns_the_bare_body(self, api_server: MockAPIServer) -> None:
        """Update answers bare even though create is wrapped."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_UPDATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            updated = client.transfers.update(team_id=TEAM_ID, transfer_id=TRANSFER_ID, **_configuration())

        assert updated.transfer_id == TRANSFER_ID
        assert updated.transfer_name == "Google Ads to BigQuery"

    def test_update_sends_a_put_with_the_whole_configuration(self, api_server: MockAPIServer) -> None:
        """The configuration is replaced wholesale, so the full body goes out on a PUT."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_UPDATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.update(team_id=TEAM_ID, transfer_id=TRANSFER_ID, **_configuration())

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == TRANSFER
        assert request.json() == EXPECTED_CONFIG_BODY
        assert request.bearer_token == "api_k"

    def test_delete_returns_none_on_a_real_204(self, api_server: MockAPIServer) -> None:
        """An empty 204 body is a success, not a parse failure."""
        api_server.route(TRANSFER, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.transfers.delete(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        assert result is None
        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == TRANSFER
        assert request.body == b""
        assert request.bearer_token == "api_k"

    def test_set_state_returns_the_new_state(self, api_server: MockAPIServer) -> None:
        """The response state is a free string, and uppercase where the verb was not."""
        api_server.route(STATE, ScriptedResponse(json_body=TRANSFER_STATE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            state = client.transfers.set_state(team_id=TEAM_ID, transfer_id=TRANSFER_ID, state="pause")

        assert state.result is True
        assert state.state == "PAUSED"

    def test_set_state_sends_the_lowercase_verb(self, api_server: MockAPIServer) -> None:
        """The request body is exactly {"transfer_state": "pause"}."""
        api_server.route(STATE, ScriptedResponse(json_body=TRANSFER_STATE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.set_state(team_id=TEAM_ID, transfer_id=TRANSFER_ID, state="pause")

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == STATE
        assert request.json() == {"transfer_state": "pause"}
        assert request.bearer_token == "api_k"

    def test_set_state_unpause_sends_the_other_verb(self, api_server: MockAPIServer) -> None:
        """The second half of the enum reaches the wire unchanged too."""
        api_server.route(STATE, ScriptedResponse(json_body={"result": True, "state": "ACTIVE"}))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            state = client.transfers.set_state(team_id=TEAM_ID, transfer_id=TRANSFER_ID, state="unpause")

        assert state.state == "ACTIVE"
        assert api_server.last_request.json() == {"transfer_state": "unpause"}

    def test_validate_accepts_a_valid_configuration(self, api_server: MockAPIServer) -> None:
        """A clean dry run returns is_valid True and no errors."""
        api_server.route(VALIDATIONS, ScriptedResponse(json_body=VALIDATION_OK_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.transfers.validate(team_id=TEAM_ID, **_configuration())

        assert result.is_valid is True
        assert result.errors == []

    def test_validate_reports_failure_without_raising(self, api_server: MockAPIServer) -> None:
        """An invalid configuration is a successful call: HTTP 200, is_valid False.

        Raising here would defeat the whole point of a dry run, so the adapter must hand
        the field-level errors back instead.
        """
        api_server.route(VALIDATIONS, ScriptedResponse(json_body=VALIDATION_FAILED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.transfers.validate(team_id=TEAM_ID, **_configuration())

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].field_id == "display_name"
        assert result.errors[0].error_code == "isEmpty"

    def test_validate_sends_a_post_to_the_validations_path(self, api_server: MockAPIServer) -> None:
        """The dry run posts the same body create would have sent."""
        api_server.route(VALIDATIONS, ScriptedResponse(json_body=VALIDATION_OK_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.validate(team_id=TEAM_ID, **_configuration())

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == VALIDATIONS
        assert request.json() == EXPECTED_CONFIG_BODY
        assert request.bearer_token == "api_k"

    def test_validate_update_reports_failure_without_raising(self, api_server: MockAPIServer) -> None:
        """The update dry run behaves identically, against an existing transfer."""
        api_server.route(UPDATE_VALIDATIONS, ScriptedResponse(json_body=VALIDATION_FAILED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.transfers.validate_update(team_id=TEAM_ID, transfer_id=TRANSFER_ID, **_configuration())

        assert result.is_valid is False
        assert result.errors[0].field_id == "display_name"
        assert result.errors[0].error_code == "isEmpty"

    def test_validate_update_posts_under_the_transfer(self, api_server: MockAPIServer) -> None:
        """Its path nests under the transfer, unlike the create dry run."""
        api_server.route(UPDATE_VALIDATIONS, ScriptedResponse(json_body=VALIDATION_OK_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.validate_update(team_id=TEAM_ID, transfer_id=TRANSFER_ID, **_configuration())

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == UPDATE_VALIDATIONS
        assert request.json() == EXPECTED_CONFIG_BODY
        assert request.bearer_token == "api_k"

    def test_list_available_sources_returns_the_bare_body(self, api_server: MockAPIServer) -> None:
        """Sources, destinations and destination types all parse."""
        api_server.route(AVAILABLE_SOURCES, ScriptedResponse(json_body=AVAILABLE_SOURCES_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            available = client.transfers.list_available_sources(team_id=TEAM_ID)

        assert available.data_sources[0].data_source_id == "AW"
        assert available.data_sources[0].applicable_destinations == ["SQL_BQ"]
        assert available.destinations[0].destination_id == 8
        assert available.destination_types[0].type_ == "SQL_BQ"

    def test_list_available_sources_sends_a_get(self, api_server: MockAPIServer) -> None:
        """A hyphenated sub-collection of transfers, with no query string."""
        api_server.route(AVAILABLE_SOURCES, ScriptedResponse(json_body=AVAILABLE_SOURCES_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.list_available_sources(team_id=TEAM_ID)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == AVAILABLE_SOURCES
        assert request.bearer_token == "api_k"

    def test_get_available_options_returns_the_bare_body(self, api_server: MockAPIServer) -> None:
        """The options object is returned as-is, with no envelope to strip."""
        api_server.route(AVAILABLE_OPTIONS, ScriptedResponse(json_body=TRANSFER_OPTIONS_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            options = client.transfers.get_available_options(team_id=TEAM_ID, source_id="AW", destination_id=8)

        assert options.data_source.data_source_id == "AW"
        assert options.data_source.service_name == "Google Ads"
        assert options.schemas == []

    def test_get_available_options_sends_both_query_params(self, api_server: MockAPIServer) -> None:
        """source_id and destination_id travel in the query string, not the path."""
        api_server.route(AVAILABLE_OPTIONS, ScriptedResponse(json_body=TRANSFER_OPTIONS_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.get_available_options(team_id=TEAM_ID, source_id="AW", destination_id=8)

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == AVAILABLE_OPTIONS
        assert _query(request.path) == {"source_id": ["AW"], "destination_id": ["8"]}
        assert request.bearer_token == "api_k"

    def test_list_runs_returns_the_unwrapped_runs(self, api_server: MockAPIServer) -> None:
        """Runs come back wrapped; the adapter hands back the list."""
        api_server.route(RUNS, ScriptedResponse(json_body=TRANSFER_RUNS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            runs = client.transfers.list_runs(
                team_id=TEAM_ID, transfer_id=TRANSFER_ID, start_date=START_DATE, end_date=END_DATE
            )

        assert len(runs) == 1
        assert runs[0].id == 12345
        assert runs[0].status == "COMPLETED"
        assert runs[0].type_ == "Recurring"
        assert runs[0].total_rows == 4821

    def test_list_runs_sends_the_range_and_paging_params(self, api_server: MockAPIServer) -> None:
        """Dates, sort and paging all reach the wire as query parameters."""
        api_server.route(RUNS, ScriptedResponse(json_body=TRANSFER_RUNS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.list_runs(
                team_id=TEAM_ID,
                transfer_id=TRANSFER_ID,
                start_date=START_DATE,
                end_date=END_DATE,
                filter_issues_only=True,
                sort_field="data_date",
                sort_direction="DESC",
                limit=25,
                offset=50,
            )

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == RUNS
        assert _query(request.path) == {
            "start_date": [START_DATE.isoformat()],
            "end_date": [END_DATE.isoformat()],
            "filter_issues_only": ["true"],
            "sort_field": ["data_date"],
            "sort_direction": ["DESC"],
            "limit": ["25"],
            "offset": ["50"],
        }
        assert request.bearer_token == "api_k"

    def test_list_runs_omits_the_optional_params(self, api_server: MockAPIServer) -> None:
        """Only the two required dates go out when nothing else is asked for."""
        api_server.route(RUNS, ScriptedResponse(json_body=TRANSFER_RUNS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.list_runs(
                team_id=TEAM_ID, transfer_id=TRANSFER_ID, start_date=START_DATE, end_date=END_DATE
            )

        assert set(_query(api_server.last_request.path)) == {"start_date", "end_date"}

    def test_create_datasource_connection_succeeds_on_201(self, api_server: MockAPIServer) -> None:
        """The connection is created with 201 and the envelope is unwrapped."""
        api_server.route(CONNECTIONS, ScriptedResponse(status=201, json_body=DATA_SOURCE_CONNECTION_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            connection = client.transfers.create_datasource_connection(
                team_id=TEAM_ID, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
            )

        assert connection.connection_id == UUID("019461A0-0000-7000-8000-000000000001")
        assert connection.login_url is None
        assert connection.connect_url is None

    def test_create_datasource_connection_never_sends_an_api_key(self, api_server: MockAPIServer) -> None:
        """The credential lives in the Authorization header and nowhere else.

        The generated request model has an ``api_key`` field; the adapter deliberately
        leaves it UNSET so a secret is never duplicated into a request body.
        """
        api_server.route(CONNECTIONS, ScriptedResponse(status=201, json_body=DATA_SOURCE_CONNECTION_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.create_datasource_connection(
                team_id=TEAM_ID, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
            )

        request = api_server.last_request
        body = request.json()
        assert "api_key" not in body
        assert body == {"data_source_id": "ADM", "destination_type": "DWH_SNOWFLAKE"}
        assert request.method == "POST"
        assert request.path == CONNECTIONS
        assert request.bearer_token == "api_k"


class TestTransfersAsyncResource:
    """Asynchronous transfers — same wire behaviour, own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_the_unwrapped_list_items(self, api_server: MockAPIServer) -> None:
        """The async path unwraps the envelope and keeps the list-item shape."""
        api_server.route(TRANSFERS, ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            transfers = await client.transfers.list(team_id=TEAM_ID)

        assert transfers[0].dwh_transfer_id == TRANSFER_ID
        assert not hasattr(transfers[0], "transfer_id")
        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == TRANSFERS
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_get_returns_the_bare_configuration(self, api_server: MockAPIServer) -> None:
        """No envelope on the detail response, on either client."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_DETAIL_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            configuration = await client.transfers.get(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        assert configuration.transfer_id == TRANSFER_ID
        assert configuration.schedule[0].run_hour == 4
        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == TRANSFER

    @pytest.mark.asyncio
    async def test_create_succeeds_on_201(self, api_server: MockAPIServer) -> None:
        """201 is the success status here too, and the body matches the sync one."""
        api_server.route(TRANSFERS, ScriptedResponse(status=201, json_body=TRANSFER_CREATED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            created = await client.transfers.create(team_id=TEAM_ID, **_configuration())

        assert created.transfer_id == TRANSFER_ID
        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == TRANSFERS
        assert request.json() == EXPECTED_CONFIG_BODY
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_update_sends_a_put_with_the_whole_configuration(self, api_server: MockAPIServer) -> None:
        """Update replaces wholesale on the async surface as well."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_UPDATED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            updated = await client.transfers.update(team_id=TEAM_ID, transfer_id=TRANSFER_ID, **_configuration())

        assert updated.transfer_id == TRANSFER_ID
        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == TRANSFER
        assert request.json() == EXPECTED_CONFIG_BODY

    @pytest.mark.asyncio
    async def test_delete_returns_none_on_a_real_204(self, api_server: MockAPIServer) -> None:
        """An empty 204 body is a success on the async client too."""
        api_server.route(TRANSFER, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.transfers.delete(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        assert result is None
        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == TRANSFER
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_set_state_sends_the_lowercase_verb(self, api_server: MockAPIServer) -> None:
        """Lowercase verb out, free-form state back."""
        api_server.route(STATE, ScriptedResponse(json_body=TRANSFER_STATE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            state = await client.transfers.set_state(team_id=TEAM_ID, transfer_id=TRANSFER_ID, state="pause")

        assert state.state == "PAUSED"
        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == STATE
        assert request.json() == {"transfer_state": "pause"}

    @pytest.mark.asyncio
    async def test_validate_reports_failure_without_raising(self, api_server: MockAPIServer) -> None:
        """An invalid dry run stays a 200 on the async path."""
        api_server.route(VALIDATIONS, ScriptedResponse(json_body=VALIDATION_FAILED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.transfers.validate(team_id=TEAM_ID, **_configuration())

        assert result.is_valid is False
        assert result.errors[0].field_id == "display_name"
        assert result.errors[0].error_code == "isEmpty"
        assert api_server.last_request.path == VALIDATIONS

    @pytest.mark.asyncio
    async def test_validate_update_reports_failure_without_raising(self, api_server: MockAPIServer) -> None:
        """Same for the update dry run, under the transfer's own path."""
        api_server.route(UPDATE_VALIDATIONS, ScriptedResponse(json_body=VALIDATION_FAILED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.transfers.validate_update(
                team_id=TEAM_ID, transfer_id=TRANSFER_ID, **_configuration()
            )

        assert result.is_valid is False
        assert result.errors[0].error_code == "isEmpty"
        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == UPDATE_VALIDATIONS

    @pytest.mark.asyncio
    async def test_list_available_sources_returns_the_bare_body(self, api_server: MockAPIServer) -> None:
        """The lookup parses identically on the async surface."""
        api_server.route(AVAILABLE_SOURCES, ScriptedResponse(json_body=AVAILABLE_SOURCES_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            available = await client.transfers.list_available_sources(team_id=TEAM_ID)

        assert available.destinations[0].destination_type == "SQL_BQ"
        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == AVAILABLE_SOURCES

    @pytest.mark.asyncio
    async def test_get_available_options_sends_both_query_params(self, api_server: MockAPIServer) -> None:
        """Query parameters survive the async request builder."""
        api_server.route(AVAILABLE_OPTIONS, ScriptedResponse(json_body=TRANSFER_OPTIONS_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            options = await client.transfers.get_available_options(team_id=TEAM_ID, source_id="AW", destination_id=8)

        assert options.data_source.data_source_id == "AW"
        request = api_server.last_request
        assert urlsplit(request.path).path == AVAILABLE_OPTIONS
        assert _query(request.path) == {"source_id": ["AW"], "destination_id": ["8"]}

    @pytest.mark.asyncio
    async def test_list_runs_sends_the_range_and_paging_params(self, api_server: MockAPIServer) -> None:
        """The whole query string is reproduced by the async path."""
        api_server.route(RUNS, ScriptedResponse(json_body=TRANSFER_RUNS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            runs = await client.transfers.list_runs(
                team_id=TEAM_ID,
                transfer_id=TRANSFER_ID,
                start_date=START_DATE,
                end_date=END_DATE,
                filter_issues_only=True,
                sort_field="created_time",
                sort_direction="ASC",
                limit=10,
                offset=5,
            )

        assert runs[0].id == 12345
        request = api_server.last_request
        assert urlsplit(request.path).path == RUNS
        assert _query(request.path) == {
            "start_date": [START_DATE.isoformat()],
            "end_date": [END_DATE.isoformat()],
            "filter_issues_only": ["true"],
            "sort_field": ["created_time"],
            "sort_direction": ["ASC"],
            "limit": ["10"],
            "offset": ["5"],
        }

    @pytest.mark.asyncio
    async def test_create_datasource_connection_never_sends_an_api_key(self, api_server: MockAPIServer) -> None:
        """201, unwrapped, and still no secret in the body."""
        api_server.route(CONNECTIONS, ScriptedResponse(status=201, json_body=DATA_SOURCE_CONNECTION_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            connection = await client.transfers.create_datasource_connection(
                team_id=TEAM_ID, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
            )

        assert connection.connection_id == UUID("019461A0-0000-7000-8000-000000000001")
        body = api_server.last_request.json()
        assert "api_key" not in body
        assert body == {"data_source_id": "ADM", "destination_type": "DWH_SNOWFLAKE"}


class TestTransfersRequestOptions:
    """Per-request overrides and the raw-response envelope, on transfers routes."""

    def test_auth_token_override_reaches_the_wire(self, api_server: MockAPIServer) -> None:
        """auth_token replaces the client credential for one call only."""
        api_server.route(TRANSFERS, ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.list(team_id=TEAM_ID, auth_token="otok_scoped")
            client.transfers.list(team_id=TEAM_ID)

        assert [r.bearer_token for r in api_server.requests] == ["otok_scoped", "api_k"]

    def test_headers_override_reaches_the_wire(self, api_server: MockAPIServer) -> None:
        """Per-request headers are merged in by the transport event hook."""
        api_server.route(TRANSFER, ScriptedResponse(json_body=TRANSFER_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfers.get(
                team_id=TEAM_ID,
                transfer_id=TRANSFER_ID,
                headers={"X-Span-Id": "span-transfers", "Idempotency-Key": "idem-transfers"},
            )

        request = api_server.last_request
        assert request.headers["x-span-id"] == "span-transfers"
        assert request.headers["idempotency-key"] == "idem-transfers"

    def test_timeout_override_fires_against_a_slow_transfer_route(self, api_server: MockAPIServer) -> None:
        """A tight per-request timeout beats a generous client-level one, for real."""
        api_server.route(TRANSFERS, ScriptedResponse(json_body=TRANSFERS_LIST_BODY, delay=1.5))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.transfers.list(team_id=TEAM_ID, timeout=0.3)

    def test_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response carries the status, correlation id and undecoded body."""
        api_server.route(
            TRANSFERS,
            ScriptedResponse(json_body=TRANSFERS_LIST_BODY, headers={"X-Request-Id": "req-transfers-1"}),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.transfers.list(team_id=TEAM_ID)

        assert response.status_code == 200
        assert response.request_id == "req-transfers-1"
        assert response.json_body == TRANSFERS_LIST_BODY
        assert response.data[0].dwh_transfer_id == TRANSFER_ID

    def test_raw_response_reports_the_201_of_create(self, api_server: MockAPIServer) -> None:
        """The raw envelope surfaces the real created status, not a normalised 200."""
        api_server.route(TRANSFERS, ScriptedResponse(status=201, json_body=TRANSFER_CREATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.transfers.create(team_id=TEAM_ID, **_configuration())

        assert response.status_code == 201
        assert response.json_body == TRANSFER_CREATED_BODY
        assert response.data.transfer_id == TRANSFER_ID

    @pytest.mark.asyncio
    async def test_async_overrides_reach_the_wire(self, api_server: MockAPIServer) -> None:
        """The async hook applies the per-request credential and headers too."""
        api_server.route(TRANSFERS, ScriptedResponse(json_body=TRANSFERS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.transfers.list(team_id=TEAM_ID, auth_token="otok_async", headers={"X-Span-Id": "span-async"})

        request = api_server.last_request
        assert request.bearer_token == "otok_async"
        assert request.headers["x-span-id"] == "span-async"

    @pytest.mark.asyncio
    async def test_async_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response works on the async mirror of the resource."""
        api_server.route(
            TRANSFERS,
            ScriptedResponse(json_body=TRANSFERS_LIST_BODY, headers={"X-Span-Id": "async-transfers-span"}),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.transfers.list(team_id=TEAM_ID)

        assert response.status_code == 200
        assert response.span_id == "async-transfers-span"
        assert response.data[0].dwh_transfer_id == TRANSFER_ID


class TestTransfersErrorTaxonomy:
    """Failure statuses on a transfers route map to their own exception classes."""

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, code: str, expected: type[Exception]
    ) -> None:
        """Every status documented for the transfer lookup maps to its own class."""
        api_server.route(TRANSFER, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.transfers.get(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code

    def test_422_is_a_validation_error(self, api_server: MockAPIServer) -> None:
        """A rejected create payload raises the validation class, not a bare APIError."""
        api_server.route(
            TRANSFERS,
            ScriptedResponse(status=422, json_body=_error_envelope("UNPROCESSABLE_ENTITY", "schema_id is unknown")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.transfers.create(team_id=TEAM_ID, **_configuration())

        assert exc_info.value.status_code == 422
        assert exc_info.value.error_code == "UNPROCESSABLE_ENTITY"

    def test_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the response headers, not guessed."""
        api_server.route(
            TRANSFERS,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.transfers.list(team_id=TEAM_ID)

        assert exc_info.value.retry_after == 30

    def test_delete_failure_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """Only a real 204 counts as success; anything else still raises."""
        api_server.route(TRANSFER, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "gone")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.transfers.delete(team_id=TEAM_ID, transfer_id=TRANSFER_ID)

        assert exc_info.value.status_code == 404
        assert api_server.last_request.method == "DELETE"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    async def test_async_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, code: str, expected: type[Exception]
    ) -> None:
        """Error classification is identical on the async path."""
        api_server.route(TRANSFERS, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.transfers.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code

    @pytest.mark.asyncio
    async def test_async_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """The async client keeps Retry-After as well."""
        api_server.route(
            RUNS,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "17"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                await client.transfers.list_runs(
                    team_id=TEAM_ID, transfer_id=TRANSFER_ID, start_date=START_DATE, end_date=END_DATE
                )

        assert exc_info.value.retry_after == 17
