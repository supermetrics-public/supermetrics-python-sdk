"""End-to-end tests for the Table Groups resource.

Drives the full stack over a real loopback socket. Every test asserts both on what
went *out* (verb, path, body, credential) and what came back (parsed model).

Table Groups is served from ``/enterprise/v2/table/...`` (not ``/teams/{id}/...``),
so the routes include the ``/enterprise/v2`` prefix that the ``rewrite_path`` in the
allowlist produces. The team identity comes from the API key, not a path parameter.
"""

from __future__ import annotations

from typing import Any

import pytest

from supermetrics import (
    EditTableGroupBody,
    FieldDefinition,
    ImportTableGroupBody,
    SupermetricsAsyncClient,
    SupermetricsClient,
    TableDefinition,
    TableGroupImport,
)
from supermetrics._generated.supermetrics_api_client.models.export_table_group_response_200 import (
    ExportTableGroupResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.table_group_write_response import TableGroupWriteResponse
from supermetrics.exceptions import (
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsNotFoundError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

GROUP_ID = "tg_100"

LIST_PATH = "/enterprise/v2/table/groups"
EXPORT_PATH = f"/enterprise/v2/table/group/{GROUP_ID}/export"
IMPORT_PATH = "/enterprise/v2/table/group/import"
EDIT_PATH = f"/enterprise/v2/table/group/{GROUP_ID}"

META: dict[str, Any] = {"request_id": "req_0123456789ab"}

LIST_BODY: dict[str, Any] = {
    "meta": META,
    "data": [
        {"@type": "table_group", "group_id": "tg_100", "schema_id": 354, "name": "Google Ads Standard"},
        {"@type": "table_group", "group_id": "tg_200", "schema_id": 68, "name": "Pinterest Ads Standard"},
    ],
}

EXPORT_BODY: dict[str, Any] = {
    "version": 1,
    "group": {"group_id": "tg_100", "group_name": "Google Ads Standard", "ds_id": "AW", "table_prefix": "AW"},
    "tables": [
        {"table_name": "CAMPAIGNS", "table_partition": "date", "fields": ["campaign_id", "date", "impressions"]},
    ],
    "fields": [
        {"field_id": "campaign_id", "target_name": "campaign_id"},
        {"field_id": "date", "target_name": "report_date"},
        {"field_id": "impressions", "target_name": "impressions"},
    ],
}

WRITE_RESPONSE_BODY: dict[str, Any] = {
    "@type": "table_group",
    "group_id": "tg_300",
    "group_name": "SDK Test (auto-delete)",
    "links": {
        "enclosure": {
            "href": "https://api.supermetrics.com/enterprise/table/group/tg_300/export?version=1",
        },
    },
}


def _import_body() -> ImportTableGroupBody:
    return ImportTableGroupBody(
        version=1,
        group=TableGroupImport(group_name="Test Group", ds_id="AW", table_prefix="TST"),
        tables=[TableDefinition(table_name="CAMPAIGNS", table_partition="date", fields=["campaign_id", "date"])],
        fields=[FieldDefinition(field_id="campaign_id", target_name="campaign_id")],
    )


def _edit_body() -> EditTableGroupBody:
    return EditTableGroupBody(
        version=1,
        group=TableGroupImport(group_name="Updated Group", ds_id="AW", table_prefix="TST"),
        tables=[
            TableDefinition(table_name="CAMPAIGNS", table_partition="date", fields=["campaign_id", "date", "clicks"]),
        ],
        fields=[
            FieldDefinition(field_id="campaign_id", target_name="campaign_id"),
            FieldDefinition(field_id="clicks", target_name="clicks"),
        ],
    )


def _error_envelope(code: str, message: str) -> dict[str, Any]:
    return {"meta": META, "error": {"code": code, "message": message}}


# ---------------------------------------------------------------------------
# Synchronous
# ---------------------------------------------------------------------------


class TestTableGroupsResource:
    """Synchronous table groups — all four methods, both directions on the wire."""

    def test_list_unwraps_the_envelope_and_gets_the_collection(self, api_server: MockAPIServer) -> None:
        api_server.route(LIST_PATH, ScriptedResponse(json_body=LIST_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            groups = client.table_groups.list()

        assert len(groups) == 2
        assert groups[0].group_id == "tg_100"
        assert groups[0].schema_id == 354
        assert groups[0].name == "Google Ads Standard"
        assert groups[1].group_id == "tg_200"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LIST_PATH
        assert request.json() is None
        assert request.bearer_token == "not-a-real-key"

    def test_export_returns_full_data_model(self, api_server: MockAPIServer) -> None:
        api_server.route(EXPORT_PATH, ScriptedResponse(json_body=EXPORT_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            export = client.table_groups.export(group_id=GROUP_ID, version=1)

        assert isinstance(export, ExportTableGroupResponse200)
        assert export.version == 1
        assert export.group.group_name == "Google Ads Standard"
        assert export.group.ds_id == "AW"
        assert len(export.tables) == 1
        assert export.tables[0].table_name == "CAMPAIGNS"
        assert len(export.fields) == 3

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path.startswith(EXPORT_PATH)
        assert "version=1" in request.path

    def test_import_succeeds_on_201_and_posts_the_body(self, api_server: MockAPIServer) -> None:
        api_server.route(IMPORT_PATH, ScriptedResponse(status=201, json_body=WRITE_RESPONSE_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            created = client.table_groups.import_(body=_import_body())

        assert isinstance(created, TableGroupWriteResponse)
        assert created.group_id == "tg_300"
        assert created.group_name == "SDK Test (auto-delete)"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == IMPORT_PATH
        body = request.json()
        assert body["version"] == 1
        assert body["group"]["group_name"] == "Test Group"
        assert body["group"]["ds_id"] == "AW"
        assert len(body["tables"]) == 1

    def test_import_sends_fields_when_provided(self, api_server: MockAPIServer) -> None:
        api_server.route(IMPORT_PATH, ScriptedResponse(status=201, json_body=WRITE_RESPONSE_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            client.table_groups.import_(body=_import_body())

        body = api_server.last_request.json()
        assert len(body["fields"]) == 1
        assert body["fields"][0]["field_id"] == "campaign_id"
        assert body["fields"][0]["target_name"] == "campaign_id"

    def test_edit_puts_full_replacement_to_the_group(self, api_server: MockAPIServer) -> None:
        api_server.route(EDIT_PATH, ScriptedResponse(json_body=WRITE_RESPONSE_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            updated = client.table_groups.edit(group_id=GROUP_ID, body=_edit_body())

        assert isinstance(updated, TableGroupWriteResponse)
        assert updated.group_id == "tg_300"

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == EDIT_PATH
        body = request.json()
        assert body["version"] == 1
        assert body["group"]["group_name"] == "Updated Group"
        assert len(body["tables"]) == 1
        assert len(body["fields"]) == 2

    def test_edit_sends_version_in_request_body(self, api_server: MockAPIServer) -> None:
        api_server.route(EDIT_PATH, ScriptedResponse(json_body=WRITE_RESPONSE_BODY))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            client.table_groups.edit(group_id=GROUP_ID, body=_edit_body())

        request = api_server.last_request
        assert "version" not in request.path
        assert request.json()["version"] == 1


# ---------------------------------------------------------------------------
# Asynchronous
# ---------------------------------------------------------------------------


class TestTableGroupsAsyncResource:
    """Asynchronous table groups — mirrors the sync tests."""

    @pytest.mark.asyncio
    async def test_list_unwraps_the_envelope_and_gets_the_collection(self, api_server: MockAPIServer) -> None:
        api_server.route(LIST_PATH, ScriptedResponse(json_body=LIST_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            groups = await client.table_groups.list()

        assert len(groups) == 2
        assert groups[0].group_id == "tg_100"
        assert groups[1].group_id == "tg_200"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LIST_PATH

    @pytest.mark.asyncio
    async def test_export_returns_full_data_model(self, api_server: MockAPIServer) -> None:
        api_server.route(EXPORT_PATH, ScriptedResponse(json_body=EXPORT_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            export = await client.table_groups.export(group_id=GROUP_ID, version=1)

        assert isinstance(export, ExportTableGroupResponse200)
        assert export.version == 1
        assert export.group.group_name == "Google Ads Standard"
        assert len(export.tables) == 1
        assert len(export.fields) == 3

    @pytest.mark.asyncio
    async def test_import_succeeds_on_201(self, api_server: MockAPIServer) -> None:
        api_server.route(IMPORT_PATH, ScriptedResponse(status=201, json_body=WRITE_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            created = await client.table_groups.import_(body=_import_body())

        assert isinstance(created, TableGroupWriteResponse)
        assert created.group_id == "tg_300"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == IMPORT_PATH

    @pytest.mark.asyncio
    async def test_edit_puts_full_replacement(self, api_server: MockAPIServer) -> None:
        api_server.route(EDIT_PATH, ScriptedResponse(json_body=WRITE_RESPONSE_BODY))

        async with SupermetricsAsyncClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            updated = await client.table_groups.edit(group_id=GROUP_ID, body=_edit_body())

        assert isinstance(updated, TableGroupWriteResponse)
        assert updated.group_id == "tg_300"

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == EDIT_PATH


# ---------------------------------------------------------------------------
# Error taxonomy
# ---------------------------------------------------------------------------


class TestTableGroupsErrorTaxonomy:
    """Failure statuses map to the correct exception classes."""

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (422, "UNPROCESSABLE_ENTITY", SupermetricsValidationError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[Exception],
    ) -> None:
        """Edit documents 401/400/403/404/422/429/500 — exercise the taxonomy through it."""
        api_server.route(EDIT_PATH, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.table_groups.edit(group_id=GROUP_ID, body=_edit_body())

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code

    def test_409_conflict_on_import_is_a_generic_api_error(self, api_server: MockAPIServer) -> None:
        """409 has no dedicated subclass — it surfaces as a plain SupermetricsAPIError."""
        api_server.route(
            IMPORT_PATH,
            ScriptedResponse(status=409, json_body=_error_envelope("TABLE_GROUP_NAME_CONFLICT", "name taken")),
        )

        with SupermetricsClient(api_key="not-a-real-key", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.table_groups.import_(body=_import_body())

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.status_code == 409
        assert exc_info.value.error_code == "TABLE_GROUP_NAME_CONFLICT"
