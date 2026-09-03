"""End-to-end tests for the Destinations resource.

Drives the whole stack over a real loopback socket. Every test asserts on what went
*out* — verb, path, body, credential — as well as on what came back, because the request
is the half a mocked transport cannot check.

Unlike Transfers, this domain has no wrapped/bare split: every one of the four response
schemas is ``{"meta": ..., "data": ...}`` and every method returns ``.data``. What *is*
irregular here is pinned below — ``create`` answers 201, ``delete`` answers 204 with no
body, and a failed connection test is an HTTP 200 carrying ``success: false``.

Every credential in these fixtures is deliberately, visibly fake: ``MockAPIServer``
records whole request bodies and a failing assertion prints them.
"""

from __future__ import annotations

from typing import Any

import pytest

from supermetrics import BatchUpdateDestinationsBodyUpdatesItem, SupermetricsAsyncClient, SupermetricsClient
from supermetrics._generated.supermetrics_api_client.models.destination_info import DestinationInfo
from supermetrics._generated.supermetrics_api_client.models.destination_usage import DestinationUsage

# ``TestConnectionResult`` starts with "Test", so pytest would try to collect it as a
# test class if it were imported under its own name.
from supermetrics._generated.supermetrics_api_client.models.test_connection_result import (
    TestConnectionResult as ConnectionTestResult,
)
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

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

TEAM_ID = 42
DESTINATION_ID = 8

#: One route serves every verb, so a path shared by a collection and its verbs —
#: ``DESTINATIONS`` for GET and POST, ``DESTINATION`` for GET, PUT and DELETE — needs a
#: response *sequence* whenever a single test exercises more than one of them.
DESTINATIONS = f"/teams/{TEAM_ID}/destinations"
DESTINATION = f"{DESTINATIONS}/{DESTINATION_ID}"
CONNECTION_TEST = f"{DESTINATIONS}/test-connection"
USAGE = f"{DESTINATION}/usage"
BATCH = f"{DESTINATIONS}/batch"

#: Every wrapped response carries this envelope metadata.
META: dict[str, Any] = {"request_id": "req_0123456789ab"}

DESTINATION_TYPE = "DWH_SNOWFLAKE"
DISPLAY_NAME = "Analytics warehouse"

#: Destination-specific configuration. ``private_key`` and ``passphrase`` are real wire
#: fields on this type, so the values must be unmistakably fake.
SNOWFLAKE_FIELDS: dict[str, Any] = {
    "hostname": "not-a-real-host.snowflakecomputing.example",
    "warehouse": "DEMO_WH",
    "database_name": "TEST_DB",
    "schema": "PUBLIC",
    "role": "ACCOUNTADMIN",
    "username": "not-a-real-user",
    "private_key": "not-a-real-key",
    "passphrase": "not-a-real-passphrase",
}

NEW_PASSWORD = "not-a-real-new-password"

#: The exact JSON a call built from :func:`_configuration` serialises to. ``auth_method``,
#: ``destination_id`` and ``new_password`` are left UNSET and must be absent from the wire.
EXPECTED_REQUEST_BODY: dict[str, Any] = {
    "type": DESTINATION_TYPE,
    "display_name": DISPLAY_NAME,
    "fields": SNOWFLAKE_FIELDS,
}

#: GET /teams/{team_id}/destinations — wrapped. The list item is a flat summary.
DESTINATION_LIST_ITEM: dict[str, Any] = {
    "id": DESTINATION_ID,
    "display_name": DISPLAY_NAME,
    "type": DESTINATION_TYPE,
}
DESTINATIONS_LIST_BODY: dict[str, Any] = {"meta": META, "data": [DESTINATION_LIST_ITEM]}

#: GET/POST/PUT of a single destination — wrapped. Note that the read shape is a *form
#: description* (``destination_type`` + ``edit_settings``), not the flat ``fields`` map
#: that was written; the two genuinely do not match upstream.
DESTINATION_INFO_PAYLOAD: dict[str, Any] = {
    "id": DESTINATION_ID,
    "display_name": DISPLAY_NAME,
    "destination_type": {
        "type": DESTINATION_TYPE,
        "title": "Snowflake",
        "icon_url": "https://cdn.example.invalid/snowflake.svg",
        "is_internal": False,
    },
    "edit_settings": [
        {
            "id": "hostname",
            "input_type": "text",
            "is_required": True,
            "label": "Hostname",
            "value": "not-a-real-host.snowflakecomputing.example",
        },
        {
            "id": "warehouse",
            "input_type": "text",
            "is_required": True,
            "label": "Warehouse",
            "value": "DEMO_WH",
        },
        {
            "id": "passphrase",
            "input_type": "password",
            "is_required": False,
            "label": "Passphrase",
            "value": None,
        },
    ],
}
DESTINATION_BODY: dict[str, Any] = {"meta": META, "data": DESTINATION_INFO_PAYLOAD}

#: POST .../test-connection — HTTP 200 either way; the verdict is in the body.
CONNECTION_OK_BODY: dict[str, Any] = {"meta": META, "data": {"success": True, "error": None}}
CONNECTION_FAILED_BODY: dict[str, Any] = {
    "meta": META,
    "data": {"success": False, "error": "Could not authenticate against the warehouse"},
}

#: GET .../{destination_id}/usage — wrapped.
USAGE_IN_USE_BODY: dict[str, Any] = {
    "meta": META,
    "data": {
        "is_used": True,
        "transfers": [{"transfer_id": 36091, "transfer_name": "Google Ads to BigQuery"}],
    },
}
USAGE_UNUSED_BODY: dict[str, Any] = {"meta": META, "data": {"is_used": False, "transfers": []}}

#: PATCH .../destinations/batch — wrapped.
BATCH_SUCCESS_BODY: dict[str, Any] = {
    "meta": META,
    "data": {
        "has_errors": False,
        "results": [
            {"destination_id": 8, "status": "success"},
            {"destination_id": 9, "status": "success"},
        ],
    },
}
BATCH_PARTIAL_FAILURE_BODY: dict[str, Any] = {
    "meta": META,
    "data": {
        "has_errors": True,
        "results": [
            {"destination_id": 8, "status": "success"},
            {
                "destination_id": 9,
                "status": "error",
                "error_code": "INVALID_SECRET",
                "message": "Secret validation failed",
            },
        ],
    },
}


def _configuration() -> dict[str, Any]:
    """Build the three required arguments shared by create, update and test_connection."""
    return {"type": DESTINATION_TYPE, "display_name": DISPLAY_NAME, "fields": dict(SNOWFLAKE_FIELDS)}


def _error_envelope(code: str, message: str) -> dict[str, object]:
    """Build an upstream error payload in the envelope the generated models require."""
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


class TestDestinationsResource:
    """Synchronous destinations — all eight methods, both directions on the wire."""

    def test_list_unwraps_the_envelope_and_gets_the_collection(self, api_server: MockAPIServer) -> None:
        """The envelope is stripped and the items keep their flat list-item shape."""
        api_server.route(DESTINATIONS, ScriptedResponse(json_body=DESTINATIONS_LIST_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destinations = client.destinations.list(team_id=TEAM_ID)

        assert len(destinations) == 1
        assert destinations[0].id == DESTINATION_ID
        assert destinations[0].display_name == DISPLAY_NAME
        # The wire field is `type`; the generated attribute is `type_` because `type`
        # is a builtin. Conflating the two is the bug this pins down.
        assert destinations[0].type_ == DESTINATION_TYPE

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == DESTINATIONS
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    def test_get_unwraps_to_destination_info_and_gets_the_item(self, api_server: MockAPIServer) -> None:
        """The item response is unwrapped into DestinationInfo, and the path carries the id."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destination = client.destinations.get(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert isinstance(destination, DestinationInfo)
        assert destination.id == DESTINATION_ID
        assert destination.display_name == DISPLAY_NAME
        assert destination.destination_type.type_ == DESTINATION_TYPE
        assert destination.destination_type.title == "Snowflake"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == DESTINATION
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    def test_get_preserves_the_edit_settings_form(self, api_server: MockAPIServer) -> None:
        """``edit_settings`` is a form description, and every descriptor survives parsing.

        The read shape and the write shape do not match: ``create``/``update`` take a flat
        ``fields`` mapping, while ``get`` answers with per-setting ``{id, label, value,
        input_type, is_required}`` descriptors. That asymmetry is real, so it is pinned.
        """
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destination = client.destinations.get(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert [setting.id for setting in destination.edit_settings] == ["hostname", "warehouse", "passphrase"]
        assert destination.edit_settings[0].label == "Hostname"
        assert destination.edit_settings[0].value == "not-a-real-host.snowflakecomputing.example"
        assert destination.edit_settings[0].is_required is True
        assert destination.edit_settings[2].input_type == "password"
        assert destination.edit_settings[2].is_required is False
        # A password descriptor comes back with a null value, not the stored secret.
        assert destination.edit_settings[2].value is None
        assert api_server.last_request.path == DESTINATION

    def test_create_succeeds_on_201_and_posts_the_configuration(self, api_server: MockAPIServer) -> None:
        """Creation answers 201, not 200, and sends exactly the three required fields."""
        api_server.route(DESTINATIONS, ScriptedResponse(status=201, json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            created = client.destinations.create(team_id=TEAM_ID, **_configuration())

        assert isinstance(created, DestinationInfo)
        assert created.id == DESTINATION_ID
        assert created.display_name == DISPLAY_NAME

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == DESTINATIONS
        assert request.json() == EXPECTED_REQUEST_BODY
        # Left unset by the caller, so it must not appear on the wire at all.
        assert "auth_method" not in request.json()
        assert request.bearer_token == "not-a-real-key"

    def test_create_sends_auth_method_when_given(self, api_server: MockAPIServer) -> None:
        """The optional auth_method is serialised only when the caller supplies it."""
        api_server.route(DESTINATIONS, ScriptedResponse(status=201, json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            created = client.destinations.create(
                team_id=TEAM_ID, **_configuration(), auth_method="AUTH_METHOD_KEY_PAIR"
            )

        assert created.id == DESTINATION_ID

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == DESTINATIONS
        assert request.json() == {**EXPECTED_REQUEST_BODY, "auth_method": "AUTH_METHOD_KEY_PAIR"}
        assert request.bearer_token == "not-a-real-key"

    def test_update_puts_the_configuration_to_the_item(self, api_server: MockAPIServer) -> None:
        """Update replaces the configuration wholesale, on a PUT to the item path."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            updated = client.destinations.update(team_id=TEAM_ID, destination_id=DESTINATION_ID, **_configuration())

        assert isinstance(updated, DestinationInfo)
        assert updated.id == DESTINATION_ID

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == DESTINATION
        assert request.json() == EXPECTED_REQUEST_BODY
        assert "new_password" not in request.json()
        assert request.bearer_token == "not-a-real-key"

    def test_update_round_trips_new_password(self, api_server: MockAPIServer) -> None:
        """A secret rotation reaches the wire as its own top-level field."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            updated = client.destinations.update(
                team_id=TEAM_ID,
                destination_id=DESTINATION_ID,
                **_configuration(),
                auth_method="AUTH_METHOD_KEY_PAIR",
                new_password=NEW_PASSWORD,
            )

        assert updated.display_name == DISPLAY_NAME

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == DESTINATION
        assert request.json() == {
            **EXPECTED_REQUEST_BODY,
            "auth_method": "AUTH_METHOD_KEY_PAIR",
            "new_password": NEW_PASSWORD,
        }
        assert request.bearer_token == "not-a-real-key"

    def test_delete_returns_none_on_a_real_204(self, api_server: MockAPIServer) -> None:
        """An empty 204 body is a success, not a parse failure."""
        api_server.route(DESTINATION, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = client.destinations.delete(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert result is None

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == DESTINATION
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    def test_test_connection_returns_a_successful_result(self, api_server: MockAPIServer) -> None:
        """A working connection posts the create payload to the test-connection path."""
        api_server.route(CONNECTION_TEST, ScriptedResponse(json_body=CONNECTION_OK_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = client.destinations.test_connection(team_id=TEAM_ID, **_configuration())

        assert isinstance(result, ConnectionTestResult)
        assert result.success is True
        assert result.error is None

        request = api_server.last_request
        assert request.method == "POST"
        # A hyphenated sub-path of the collection, not an item id.
        assert request.path == CONNECTION_TEST
        assert request.json() == EXPECTED_REQUEST_BODY
        assert request.bearer_token == "not-a-real-key"

    def test_test_connection_reports_failure_without_raising(self, api_server: MockAPIServer) -> None:
        """A connection that does not work is HTTP 200 with success False.

        Raising here would defeat the whole point of a dry run, so the adapter must hand
        the verdict back instead.
        """
        api_server.route(CONNECTION_TEST, ScriptedResponse(json_body=CONNECTION_FAILED_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = client.destinations.test_connection(team_id=TEAM_ID, **_configuration())

        assert result.success is False
        assert result.error == "Could not authenticate against the warehouse"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTION_TEST
        assert request.json() == EXPECTED_REQUEST_BODY
        assert request.bearer_token == "not-a-real-key"

    def test_test_connection_sends_the_optional_fields(self, api_server: MockAPIServer) -> None:
        """destination_id and new_password reach the body when supplied."""
        api_server.route(CONNECTION_TEST, ScriptedResponse(json_body=CONNECTION_OK_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = client.destinations.test_connection(
                team_id=TEAM_ID,
                **_configuration(),
                auth_method="AUTH_METHOD_KEY_PAIR",
                destination_id=DESTINATION_ID,
                new_password=NEW_PASSWORD,
            )

        assert result.success is True

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTION_TEST
        assert request.json() == {
            **EXPECTED_REQUEST_BODY,
            "auth_method": "AUTH_METHOD_KEY_PAIR",
            "destination_id": DESTINATION_ID,
            "new_password": NEW_PASSWORD,
        }
        assert request.bearer_token == "not-a-real-key"

    def test_get_usage_unwraps_the_usage_report(self, api_server: MockAPIServer) -> None:
        """is_used and the referencing transfers survive the round trip."""
        api_server.route(USAGE, ScriptedResponse(json_body=USAGE_IN_USE_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            usage = client.destinations.get_usage(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert isinstance(usage, DestinationUsage)
        assert usage.is_used is True
        assert len(usage.transfers) == 1
        assert usage.transfers[0].transfer_id == 36091
        assert usage.transfers[0].transfer_name == "Google Ads to BigQuery"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == USAGE
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    def test_get_usage_reports_an_unused_destination(self, api_server: MockAPIServer) -> None:
        """An empty transfers list is a valid answer, not a missing field."""
        api_server.route(USAGE, ScriptedResponse(json_body=USAGE_UNUSED_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            usage = client.destinations.get_usage(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert usage.is_used is False
        assert usage.transfers == []

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == USAGE
        assert request.bearer_token == "not-a-real-key"

    # ── batch_update ────────────────────────────────────────────────────

    def test_batch_update_sends_patch_and_unwraps_results(self, api_server: MockAPIServer) -> None:
        """batch_update sends a PATCH with type and updates, and returns the data envelope."""
        api_server.route(BATCH, ScriptedResponse(json_body=BATCH_SUCCESS_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = client.destinations.batch_update(
                team_id=TEAM_ID,
                destination_type="DWH_SNOWFLAKE",
                updates=[
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=8, new_secret="not-a-real-secret-1"),
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=9, new_secret="not-a-real-secret-2"),
                ],
            )

        assert result.has_errors is False
        assert len(result.results) == 2
        assert result.results[0].destination_id == 8
        assert result.results[0].status == "success"

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == BATCH
        assert request.bearer_token == "not-a-real-key"
        body = request.json()
        assert body["type"] == "DWH_SNOWFLAKE"
        assert len(body["updates"]) == 2
        assert body["updates"][0]["destination_id"] == 8
        assert body["updates"][0]["new_secret"] == "not-a-real-secret-1"

    def test_batch_update_partial_failure_surfaces_per_item_errors(self, api_server: MockAPIServer) -> None:
        """A partial-failure batch returns has_errors=True with error details on failed items."""
        api_server.route(BATCH, ScriptedResponse(json_body=BATCH_PARTIAL_FAILURE_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = client.destinations.batch_update(
                team_id=TEAM_ID,
                destination_type="DWH_SNOWFLAKE",
                updates=[
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=8, new_secret="not-a-real-secret-1"),
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=9, new_secret="not-a-real-secret-2"),
                ],
            )

        assert result.has_errors is True
        assert result.results[0].status == "success"
        assert result.results[1].status == "error"
        assert result.results[1].error_code == "INVALID_SECRET"
        assert result.results[1].message == "Secret validation failed"

    def test_batch_update_validation_error_on_400(self, api_server: MockAPIServer) -> None:
        """A 400 from the batch endpoint raises SupermetricsValidationError."""
        api_server.route(
            BATCH,
            ScriptedResponse(status=400, json_body=_error_envelope("INVALID_REQUEST", "Duplicate destination_id")),
        )

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.destinations.batch_update(team_id=TEAM_ID, destination_type="DWH_SNOWFLAKE", updates=[])

        assert exc_info.value.status_code == 400
        assert api_server.last_request.method == "PATCH"


class TestDestinationsAsyncResource:
    """Asynchronous destinations — same wire behaviour, own event hooks."""

    @pytest.mark.asyncio
    async def test_list_unwraps_the_envelope_and_gets_the_collection(self, api_server: MockAPIServer) -> None:
        """The async path strips the envelope identically."""
        api_server.route(DESTINATIONS, ScriptedResponse(json_body=DESTINATIONS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destinations = await client.destinations.list(team_id=TEAM_ID)

        assert len(destinations) == 1
        assert destinations[0].id == DESTINATION_ID
        assert destinations[0].type_ == DESTINATION_TYPE

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == DESTINATIONS
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_get_unwraps_to_destination_info_and_gets_the_item(self, api_server: MockAPIServer) -> None:
        """The async item lookup unwraps into DestinationInfo too."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destination = await client.destinations.get(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert isinstance(destination, DestinationInfo)
        assert destination.id == DESTINATION_ID
        assert destination.destination_type.type_ == DESTINATION_TYPE

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == DESTINATION
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_get_preserves_the_edit_settings_form(self, api_server: MockAPIServer) -> None:
        """The form descriptors survive parsing on the async path as well."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destination = await client.destinations.get(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert [setting.id for setting in destination.edit_settings] == ["hostname", "warehouse", "passphrase"]
        assert destination.edit_settings[1].value == "DEMO_WH"
        assert destination.edit_settings[2].input_type == "password"
        assert api_server.last_request.path == DESTINATION

    @pytest.mark.asyncio
    async def test_create_succeeds_on_201_and_posts_the_configuration(self, api_server: MockAPIServer) -> None:
        """201 is the success status on the async client too."""
        api_server.route(DESTINATIONS, ScriptedResponse(status=201, json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            created = await client.destinations.create(team_id=TEAM_ID, **_configuration())

        assert isinstance(created, DestinationInfo)
        assert created.id == DESTINATION_ID

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == DESTINATIONS
        assert request.json() == EXPECTED_REQUEST_BODY
        assert "auth_method" not in request.json()
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_create_sends_auth_method_when_given(self, api_server: MockAPIServer) -> None:
        """The optional auth_method is serialised on the async path when supplied."""
        api_server.route(DESTINATIONS, ScriptedResponse(status=201, json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            created = await client.destinations.create(
                team_id=TEAM_ID, **_configuration(), auth_method="AUTH_METHOD_KEY_PAIR"
            )

        assert created.display_name == DISPLAY_NAME

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == DESTINATIONS
        assert request.json() == {**EXPECTED_REQUEST_BODY, "auth_method": "AUTH_METHOD_KEY_PAIR"}
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_update_puts_the_configuration_to_the_item(self, api_server: MockAPIServer) -> None:
        """The async update sends the whole configuration on a PUT."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            updated = await client.destinations.update(
                team_id=TEAM_ID, destination_id=DESTINATION_ID, **_configuration()
            )

        assert updated.id == DESTINATION_ID

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == DESTINATION
        assert request.json() == EXPECTED_REQUEST_BODY
        assert "new_password" not in request.json()
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_update_round_trips_new_password(self, api_server: MockAPIServer) -> None:
        """A secret rotation reaches the wire from the async client as well."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            updated = await client.destinations.update(
                team_id=TEAM_ID,
                destination_id=DESTINATION_ID,
                **_configuration(),
                new_password=NEW_PASSWORD,
            )

        assert updated.display_name == DISPLAY_NAME

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == DESTINATION
        assert request.json() == {**EXPECTED_REQUEST_BODY, "new_password": NEW_PASSWORD}
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_delete_returns_none_on_a_real_204(self, api_server: MockAPIServer) -> None:
        """The async delete treats an empty 204 as success."""
        api_server.route(DESTINATION, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = await client.destinations.delete(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert result is None

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == DESTINATION
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_test_connection_returns_a_successful_result(self, api_server: MockAPIServer) -> None:
        """The async dry run posts to the hyphenated sub-path."""
        api_server.route(CONNECTION_TEST, ScriptedResponse(json_body=CONNECTION_OK_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = await client.destinations.test_connection(team_id=TEAM_ID, **_configuration())

        assert isinstance(result, ConnectionTestResult)
        assert result.success is True
        assert result.error is None

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTION_TEST
        assert request.json() == EXPECTED_REQUEST_BODY
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_test_connection_reports_failure_without_raising(self, api_server: MockAPIServer) -> None:
        """success False is returned, not raised, on the async path too."""
        api_server.route(CONNECTION_TEST, ScriptedResponse(json_body=CONNECTION_FAILED_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = await client.destinations.test_connection(team_id=TEAM_ID, **_configuration())

        assert result.success is False
        assert result.error == "Could not authenticate against the warehouse"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTION_TEST
        assert request.json() == EXPECTED_REQUEST_BODY
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_test_connection_sends_the_optional_fields(self, api_server: MockAPIServer) -> None:
        """destination_id and new_password reach the async body when supplied."""
        api_server.route(CONNECTION_TEST, ScriptedResponse(json_body=CONNECTION_OK_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = await client.destinations.test_connection(
                team_id=TEAM_ID,
                **_configuration(),
                destination_id=DESTINATION_ID,
                new_password=NEW_PASSWORD,
            )

        assert result.success is True

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTION_TEST
        assert request.json() == {
            **EXPECTED_REQUEST_BODY,
            "destination_id": DESTINATION_ID,
            "new_password": NEW_PASSWORD,
        }
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_get_usage_unwraps_the_usage_report(self, api_server: MockAPIServer) -> None:
        """The async usage lookup unwraps DestinationUsage."""
        api_server.route(USAGE, ScriptedResponse(json_body=USAGE_IN_USE_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            usage = await client.destinations.get_usage(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert isinstance(usage, DestinationUsage)
        assert usage.is_used is True
        assert usage.transfers[0].transfer_id == 36091

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == USAGE
        assert request.bearer_token == "not-a-real-key"

    @pytest.mark.asyncio
    async def test_get_usage_reports_an_unused_destination(self, api_server: MockAPIServer) -> None:
        """An unused destination answers is_used False and an empty list."""
        api_server.route(USAGE, ScriptedResponse(json_body=USAGE_UNUSED_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            usage = await client.destinations.get_usage(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert usage.is_used is False
        assert usage.transfers == []

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == USAGE
        assert request.bearer_token == "not-a-real-key"

    # ── batch_update (async) ────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_batch_update_sends_patch_and_unwraps_results(self, api_server: MockAPIServer) -> None:
        """Async batch_update sends PATCH with type and updates, returns data."""
        api_server.route(BATCH, ScriptedResponse(json_body=BATCH_SUCCESS_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = await client.destinations.batch_update(
                team_id=TEAM_ID,
                destination_type="DWH_SNOWFLAKE",
                updates=[
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=8, new_secret="not-a-real-secret-1"),
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=9, new_secret="not-a-real-secret-2"),
                ],
            )

        assert result.has_errors is False
        assert len(result.results) == 2

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == BATCH
        body = request.json()
        assert body["type"] == "DWH_SNOWFLAKE"
        assert len(body["updates"]) == 2

    @pytest.mark.asyncio
    async def test_batch_update_partial_failure(self, api_server: MockAPIServer) -> None:
        """Async partial-failure batch surfaces per-item errors."""
        api_server.route(BATCH, ScriptedResponse(json_body=BATCH_PARTIAL_FAILURE_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            result = await client.destinations.batch_update(
                team_id=TEAM_ID,
                destination_type="DWH_SNOWFLAKE",
                updates=[
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=8, new_secret="not-a-real-secret-1"),
                    BatchUpdateDestinationsBodyUpdatesItem(destination_id=9, new_secret="not-a-real-secret-2"),
                ],
            )

        assert result.has_errors is True
        assert result.results[1].status == "error"
        assert result.results[1].error_code == "INVALID_SECRET"


class TestDestinationsRequestOptions:
    """Per-request overrides and the raw-response envelope, on destinations routes."""

    def test_auth_token_override_reaches_the_wire(self, api_server: MockAPIServer) -> None:
        """auth_token replaces the client credential for one call only."""
        api_server.route(DESTINATIONS, ScriptedResponse(json_body=DESTINATIONS_LIST_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            client.destinations.list(team_id=TEAM_ID, auth_token="not-a-real-scoped-token")
            client.destinations.list(team_id=TEAM_ID)

        assert [r.bearer_token for r in api_server.requests] == ["not-a-real-scoped-token", "not-a-real-key"]
        assert [r.path for r in api_server.requests] == [DESTINATIONS, DESTINATIONS]

    def test_headers_override_reaches_the_wire(self, api_server: MockAPIServer) -> None:
        """Per-request headers are merged in by the transport event hook."""
        api_server.route(DESTINATION, ScriptedResponse(json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            destination = client.destinations.get(
                team_id=TEAM_ID,
                destination_id=DESTINATION_ID,
                headers={"X-Span-Id": "span-destinations", "Idempotency-Key": "idem-destinations"},
            )

        assert destination.id == DESTINATION_ID

        request = api_server.last_request
        assert request.path == DESTINATION
        assert request.headers["x-span-id"] == "span-destinations"
        assert request.headers["idempotency-key"] == "idem-destinations"

    def test_timeout_override_fires_against_a_slow_destinations_route(self, api_server: MockAPIServer) -> None:
        """A tight per-request timeout beats a generous client-level one, for real."""
        api_server.route(DESTINATIONS, ScriptedResponse(json_body=DESTINATIONS_LIST_BODY, delay=1.5))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.destinations.list(team_id=TEAM_ID, timeout=0.3)

        assert api_server.last_request.path == DESTINATIONS

    def test_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response carries the status, correlation id and undecoded body."""
        api_server.route(
            DESTINATIONS,
            ScriptedResponse(json_body=DESTINATIONS_LIST_BODY, headers={"X-Request-Id": "req-destinations-1"}),
        )

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            response = client.with_raw_response.destinations.list(team_id=TEAM_ID)

        assert response.status_code == 200
        assert response.request_id == "req-destinations-1"
        assert response.json_body == DESTINATIONS_LIST_BODY
        assert response.data[0].id == DESTINATION_ID
        assert api_server.last_request.path == DESTINATIONS

    def test_raw_response_reports_the_201_of_create(self, api_server: MockAPIServer) -> None:
        """The raw envelope surfaces the real created status, not a normalised 200."""
        api_server.route(DESTINATIONS, ScriptedResponse(status=201, json_body=DESTINATION_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            response = client.with_raw_response.destinations.create(team_id=TEAM_ID, **_configuration())

        assert response.status_code == 201
        assert response.json_body == DESTINATION_BODY
        assert response.data.id == DESTINATION_ID
        assert api_server.last_request.json() == EXPECTED_REQUEST_BODY

    @pytest.mark.asyncio
    async def test_async_overrides_reach_the_wire(self, api_server: MockAPIServer) -> None:
        """The async hook applies the per-request credential and headers too."""
        api_server.route(USAGE, ScriptedResponse(json_body=USAGE_IN_USE_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            usage = await client.destinations.get_usage(
                team_id=TEAM_ID,
                destination_id=DESTINATION_ID,
                auth_token="not-a-real-async-token",
                headers={"X-Span-Id": "span-async-destinations"},
            )

        assert usage.is_used is True

        request = api_server.last_request
        assert request.path == USAGE
        assert request.bearer_token == "not-a-real-async-token"
        assert request.headers["x-span-id"] == "span-async-destinations"

    @pytest.mark.asyncio
    async def test_async_timeout_override_fires_against_a_slow_destinations_route(
        self, api_server: MockAPIServer
    ) -> None:
        """A tight per-request timeout beats a generous client-level one on the async client."""
        api_server.route(DESTINATIONS, ScriptedResponse(json_body=DESTINATIONS_LIST_BODY, delay=1.5))

        async with SupermetricsAsyncClient(
            api_key="not-a-real-key", base_url=api_server.base_url, timeout=30.0
        ) as client:
            with pytest.raises(NetworkError):
                await client.destinations.list(team_id=TEAM_ID, timeout=0.3)

        assert api_server.last_request.path == DESTINATIONS

    @pytest.mark.asyncio
    async def test_async_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response works on the async mirror of the resource."""
        api_server.route(
            DESTINATION,
            ScriptedResponse(json_body=DESTINATION_BODY, headers={"X-Span-Id": "async-destinations-span"}),
        )

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.destinations.get(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert response.status_code == 200
        assert response.span_id == "async-destinations-span"
        assert response.data.id == DESTINATION_ID
        assert api_server.last_request.path == DESTINATION

    @pytest.mark.asyncio
    async def test_async_raw_response_reports_the_201_of_create(self, api_server: MockAPIServer) -> None:
        """The async raw envelope reports 201 for a created destination."""
        api_server.route(DESTINATIONS, ScriptedResponse(status=201, json_body=DESTINATION_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.destinations.create(team_id=TEAM_ID, **_configuration())

        assert response.status_code == 201
        assert response.data.id == DESTINATION_ID
        assert api_server.last_request.json() == EXPECTED_REQUEST_BODY


class TestDestinationsErrorTaxonomy:
    """Failure statuses on a destinations route map to their own exception classes."""

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (422, "UNPROCESSABLE_ENTITY", SupermetricsValidationError),
            (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, code: str, expected: type[Exception]
    ) -> None:
        """Every status the destination update documents maps to its own class.

        ``update`` is the endpoint that documents all six, which is why the whole
        taxonomy is exercised through it.
        """
        api_server.route(DESTINATION, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.destinations.update(team_id=TEAM_ID, destination_id=DESTINATION_ID, **_configuration())

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "PUT"
        assert api_server.last_request.path == DESTINATION

    def test_409_conflict_is_a_generic_api_error(self, api_server: MockAPIServer) -> None:
        """409 has no dedicated subclass, so it must surface as a plain APIError.

        The status is still readable on the exception, which is what a caller retrying a
        name clash needs.
        """
        api_server.route(
            DESTINATIONS,
            ScriptedResponse(status=409, json_body=_error_envelope("CONFLICT", "destination already exists")),
        )

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.destinations.create(team_id=TEAM_ID, **_configuration())

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.status_code == 409
        assert exc_info.value.error_code == "CONFLICT"
        assert api_server.last_request.method == "POST"

    def test_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the response headers, not guessed."""
        api_server.route(
            DESTINATIONS,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.destinations.list(team_id=TEAM_ID)

        assert exc_info.value.retry_after == 30
        assert api_server.last_request.path == DESTINATIONS

    def test_delete_failure_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """Only a real 204 counts as success; anything else still raises."""
        api_server.route(DESTINATION, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "gone")))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.destinations.delete(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert exc_info.value.status_code == 404
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == DESTINATION

    def test_test_connection_still_raises_on_a_transport_failure(self, api_server: MockAPIServer) -> None:
        """A returned ``success=False`` is not a licence to swallow real errors.

        The 200-with-a-negative-verdict contract must not extend to HTTP failures.
        """
        api_server.route(
            CONNECTION_TEST,
            ScriptedResponse(status=422, json_body=_error_envelope("UNPROCESSABLE_ENTITY", "unknown field")),
        )

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.destinations.test_connection(team_id=TEAM_ID, **_configuration())

        assert exc_info.value.status_code == 422
        assert exc_info.value.error_code == "UNPROCESSABLE_ENTITY"
        assert api_server.last_request.path == CONNECTION_TEST

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (422, "UNPROCESSABLE_ENTITY", SupermetricsValidationError),
            (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    async def test_async_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, code: str, expected: type[Exception]
    ) -> None:
        """Error classification is identical on the async path."""
        api_server.route(DESTINATION, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.destinations.update(team_id=TEAM_ID, destination_id=DESTINATION_ID, **_configuration())

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "PUT"

    @pytest.mark.asyncio
    async def test_async_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """The async client reads Retry-After off the response as well."""
        api_server.route(
            USAGE,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "17"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                await client.destinations.get_usage(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert exc_info.value.retry_after == 17
        assert api_server.last_request.path == USAGE

    @pytest.mark.asyncio
    async def test_async_delete_failure_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """The async delete raises on anything that is not a real 204."""
        api_server.route(DESTINATION, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "gone")))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await client.destinations.delete(team_id=TEAM_ID, destination_id=DESTINATION_ID)

        assert exc_info.value.status_code == 404
        assert api_server.last_request.method == "DELETE"
