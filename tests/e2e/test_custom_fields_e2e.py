"""End-to-end tests for the Custom Fields resource.

Drives all six methods over a real loopback socket. Custom fields stay on the core API
host — the paths keep their ``/v1`` prefix and there is no re-hosting to the Data
Warehouse host — so one server is the whole story here.

Every method gets two tests: one on the parsed return value, one on the request that
actually went out. The request half is the point of this layer; a mocked transport
cannot see that ``update`` omits ``field_type`` or that ``list`` sends no query string.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import (
    ConditionCase,
    ConditionCaseCondition,
    ConditionStep,
    CustomFieldCreateRequestDataSourceItem,
    DefinitionValue,
    FunctionArgument,
    FunctionStep,
    LookupStep,
    LookupStepMap,
    SupermetricsAsyncClient,
    SupermetricsClient,
)

from .conftest import (
    CUSTOM_FIELD_EMPTY_LIST_BODY,
    CUSTOM_FIELD_SINGLE_BODY,
    CUSTOM_FIELDS_COLLECTION,
    CUSTOM_FIELDS_ITEM,
    CUSTOM_FIELDS_METADATA,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e


def _definition_in_python() -> list[ConditionStep | FunctionStep | LookupStep]:
    """Build one of each step kind the way a caller would.

    ``LookupStepMap`` declares its mapping ``init=False``, so the map has to be
    constructed empty and populated by item assignment.
    """
    lookup_map = LookupStepMap()
    lookup_map["1"] = "2"
    lookup_map["a"] = "b"

    return [
        FunctionStep(
            type_="function",
            name="upper_case",
            arguments=[
                FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))
            ],
        ),
        LookupStep(
            type_="lookup",
            rule="equals",
            map_=lookup_map,
            source=DefinitionValue(type_="output_from_previous"),
            default=DefinitionValue(type_="static", value="other"),
        ),
        ConditionStep(
            type_="condition",
            default=DefinitionValue(type_="static", value="none"),
            cases=[
                ConditionCase(
                    return_=DefinitionValue(type_="output_from_previous"),
                    condition=ConditionCaseCondition(
                        type_="rule",
                        rule="equals",
                        source=DefinitionValue(type_="output_from_previous"),
                        target=DefinitionValue(type_="static", value="1"),
                    ),
                )
            ],
        ),
    ]


class TestCustomFieldsResource:
    """Synchronous custom field CRUD, metadata and listing."""

    def test_list_returns_the_page_from_data_items(self, custom_fields_server: MockAPIServer) -> None:
        """The page lives at ``data.items``; the adapter hands back the fields themselves."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            fields = client.custom_fields.list(team_id=42)

        assert len(fields) == 1
        assert fields[0].id == 42
        assert fields[0].display_name == "Spec Example Field"
        assert fields[0].field_type == "dim"

    def test_list_without_options_sends_an_empty_query_string(self, custom_fields_server: MockAPIServer) -> None:
        """No optional argument means no query string at all.

        The generated layer defaults ``limit`` to 25. The adapter deliberately does not
        forward that default, so the server sees whatever *it* considers the default
        page size rather than a number the SDK invented.
        """
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.list(team_id=42)

        request = custom_fields_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == CUSTOM_FIELDS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_serializes_every_optional_filter(self, custom_fields_server: MockAPIServer) -> None:
        """All five filters reach the wire: ints as strings, the bool as ``"true"``."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.list(
                team_id=42,
                data_source_id="GAWA",
                display_name="Spec Example Field",
                page=2,
                limit=50,
                include_total_count=True,
            )

        query = parse_qs(urlsplit(custom_fields_server.last_request.path).query)
        assert query == {
            "data_source_id": ["GAWA"],
            "display_name": ["Spec Example Field"],
            "page": ["2"],
            "limit": ["50"],
            "include_total_count": ["true"],
        }

    def test_list_returns_an_empty_list_when_the_page_is_empty(self, api_server: MockAPIServer) -> None:
        """``data`` and ``data.items`` are both optional upstream — an empty page is not an error."""
        api_server.route(CUSTOM_FIELDS_COLLECTION, ScriptedResponse(json_body=CUSTOM_FIELD_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            fields = client.custom_fields.list(team_id=42)

        assert fields == []

    def test_get_unwraps_the_data_envelope(self, custom_fields_server: MockAPIServer) -> None:
        """The response is ``{meta, data}``; the adapter returns the field itself."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            field = client.custom_fields.get(team_id=42, custom_field_id=42)

        assert field.id == 42
        assert field.name == "spec_example_field"
        assert field.data_source_id == "GAWA"
        assert field.data_type == "string.text.value"
        assert field.report_types == ["Default"]

    def test_get_sends_a_get_to_the_by_id_path(self, custom_fields_server: MockAPIServer) -> None:
        """GET on ``/v1/teams/{team}/custom-fields/{id}`` with no body."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.get(team_id=42, custom_field_id=42)

        request = custom_fields_server.last_request
        assert request.method == "GET"
        assert request.path == CUSTOM_FIELDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_modified_time_parses_to_an_aware_datetime(self, custom_fields_server: MockAPIServer) -> None:
        """``"2026-04-06T10:59:04+0000"`` uses a numeric offset, not a trailing ``Z``."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            field = client.custom_fields.get(team_id=42, custom_field_id=42)

        assert field.modified_time_utc == datetime(2026, 4, 6, 10, 59, 4, tzinfo=UTC)
        assert field.modified_user.email == "user@supermetrics.com"

    def test_definition_round_trips_all_three_step_kinds(self, custom_fields_server: MockAPIServer) -> None:
        """Reading a mixed definition back yields the right concrete classes, in order.

        The generated layer discriminates this ``oneOf`` with a try/except cascade rather
        than by reading the ``type`` discriminator, so nothing but an actual round trip
        proves a step is not being silently parsed as the wrong kind.
        """
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            field = client.custom_fields.get(team_id=42, custom_field_id=42)

        steps = field.definition.items
        assert [type(step) for step in steps] == [FunctionStep, LookupStep, ConditionStep]

        function_step, lookup_step, condition_step = steps

        assert function_step.name == "upper_case"
        argument = function_step.arguments[0]
        assert argument.name == "value"
        assert isinstance(argument.value, DefinitionValue)
        assert argument.value.type_ == "data_source_field"
        assert argument.value.value == "platform"

        assert lookup_step.rule == "equals"
        assert lookup_step.map_.additional_properties == {"1": "2", "a": "b"}
        assert lookup_step.map_["1"] == "2"
        assert lookup_step.default.value == "other"

        case = condition_step.cases[0]
        assert isinstance(case.return_, DefinitionValue)
        assert case.return_.type_ == "output_from_previous"
        assert case.condition.rule == "equals"
        assert case.condition.target.value == "1"

    def test_get_metadata_unwraps_the_data_envelope(self, custom_fields_server: MockAPIServer) -> None:
        """Functions, data types and the step limit all survive the round trip."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            metadata = client.custom_fields.get_metadata(team_id=42)

        assert metadata.functions.items[0].name == "upper_case"
        assert metadata.functions.items[0].display_name == "Upper Case"
        assert metadata.field_data_types == ["string.text.value"]
        assert metadata.data_transformation_steps_limit == 10
        assert metadata.rules.condition.items[0].name == "equals"

    def test_get_metadata_hits_the_metadata_path_not_the_by_id_path(self, custom_fields_server: MockAPIServer) -> None:
        """``/metadata`` is a sibling of ``/{id}``, and ``metadata`` is not an id."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.get_metadata(team_id=42)

        request = custom_fields_server.last_request
        assert request.method == "GET"
        assert request.path == CUSTOM_FIELDS_METADATA
        assert request.path != CUSTOM_FIELDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_create_returns_the_field_from_a_201(self, api_server: MockAPIServer) -> None:
        """Creation answers ``201 Created`` — not 200 — and returns the persisted field."""
        api_server.route(
            CUSTOM_FIELDS_COLLECTION,
            ScriptedResponse(
                status=201,
                json_body=CUSTOM_FIELD_SINGLE_BODY,
                headers={"Location": "https://api.supermetrics.com/v1/teams/42/custom-fields/42"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            field = client.custom_fields.create(
                team_id=42,
                display_name="Spec Example Field",
                field_type="dim",
                data_type="string.text.value",
                definition=_definition_in_python(),
            )

        assert field.id == 42
        assert field.name == "spec_example_field"

    def test_create_sends_field_type_in_the_body(self, api_server: MockAPIServer) -> None:
        """POST to the collection, with ``field_type`` in the payload."""
        api_server.route(CUSTOM_FIELDS_COLLECTION, ScriptedResponse(status=201, json_body=CUSTOM_FIELD_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.custom_fields.create(
                team_id=42,
                display_name="Spec Example Field",
                field_type="met",
                data_type="float.number.value",
                definition=_definition_in_python(),
                description="Temporary transformation for spec examples",
                data_source=[CustomFieldCreateRequestDataSourceItem(data_source_id="GAWA", report_type="Default")],
            )

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == CUSTOM_FIELDS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body["field_type"] == "met"
        assert body["display_name"] == "Spec Example Field"
        assert body["data_type"] == "float.number.value"
        assert body["description"] == "Temporary transformation for spec examples"
        assert body["data_source"] == [{"data_source_id": "GAWA", "report_type": "Default"}]

    def test_create_serializes_all_three_step_kinds(self, api_server: MockAPIServer) -> None:
        """Steps built in Python go back out onto the wire in their upstream shape.

        ``definition`` is a bare list on the way out (responses nest it under ``items``),
        and ``ConditionCase.return_`` has to serialize as the reserved word ``"return"``.
        """
        api_server.route(CUSTOM_FIELDS_COLLECTION, ScriptedResponse(status=201, json_body=CUSTOM_FIELD_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.custom_fields.create(
                team_id=42,
                display_name="Spec Example Field",
                field_type="dim",
                data_type="string.text.value",
                definition=_definition_in_python(),
            )

        definition = api_server.last_request.json()["definition"]
        assert [step["type"] for step in definition] == ["function", "lookup", "condition"]

        assert definition[0]["arguments"] == [
            {"name": "value", "value": {"type": "data_source_field", "value": "platform"}}
        ]
        assert definition[1]["map"] == {"1": "2", "a": "b"}

        case = definition[2]["cases"][0]
        assert "return" in case
        assert "return_" not in case
        assert case["return"] == {"type": "output_from_previous"}
        assert case["condition"]["rule"] == "equals"

    def test_update_returns_the_field_from_a_200(self, api_server: MockAPIServer) -> None:
        """A replace answers 200 and returns the updated field."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(json_body=CUSTOM_FIELD_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            field = client.custom_fields.update(
                team_id=42,
                custom_field_id=42,
                display_name="Renamed Field",
                data_type="string.text.value",
                definition=_definition_in_python(),
            )

        assert field.id == 42
        assert field.display_name == "Spec Example Field"

    def test_update_omits_field_type_and_data_source(self, api_server: MockAPIServer) -> None:
        """The create/update asymmetry: a field's type cannot be changed after creation.

        ``update`` takes no ``field_type`` and no ``data_source``, and neither may leak
        into the PUT body — upstream rejects the request if they do.
        """
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(json_body=CUSTOM_FIELD_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.custom_fields.update(
                team_id=42,
                custom_field_id=42,
                display_name="Renamed Field",
                data_type="string.text.value",
                definition=_definition_in_python(),
                description="Now with a description",
            )

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == CUSTOM_FIELDS_ITEM
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "field_type" not in body
        assert "data_source" not in body
        assert set(body) == {"display_name", "data_type", "definition", "description"}
        assert body["display_name"] == "Renamed Field"
        assert [step["type"] for step in body["definition"]] == ["function", "lookup", "condition"]

    def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """Deletion answers ``204 No Content`` with a genuinely empty body."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.custom_fields.delete(team_id=42, custom_field_id=42)

        assert result is None

    def test_delete_sends_a_delete_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """DELETE on the by-id path, with no body of its own."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.custom_fields.delete(team_id=42, custom_field_id=42)

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == CUSTOM_FIELDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""


class TestCustomFieldsAsyncResource:
    """Asynchronous custom fields — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_the_page_from_data_items(self, custom_fields_server: MockAPIServer) -> None:
        """The async path unwraps ``data.items`` identically."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            fields = await client.custom_fields.list(team_id=42)

        assert len(fields) == 1
        assert fields[0].id == 42

        request = custom_fields_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == CUSTOM_FIELDS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_list_serializes_every_optional_filter(self, custom_fields_server: MockAPIServer) -> None:
        """Filter serialization does not differ between the two clients."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            await client.custom_fields.list(
                team_id=42,
                data_source_id="GAWA",
                display_name="Spec Example Field",
                page=2,
                limit=50,
                include_total_count=True,
            )

        query = parse_qs(urlsplit(custom_fields_server.last_request.path).query)
        assert query == {
            "data_source_id": ["GAWA"],
            "display_name": ["Spec Example Field"],
            "page": ["2"],
            "limit": ["50"],
            "include_total_count": ["true"],
        }

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_list_when_the_page_is_empty(self, api_server: MockAPIServer) -> None:
        """An absent ``data.items`` is an empty page on the async path too."""
        api_server.route(CUSTOM_FIELDS_COLLECTION, ScriptedResponse(json_body=CUSTOM_FIELD_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            fields = await client.custom_fields.list(team_id=42)

        assert fields == []

    @pytest.mark.asyncio
    async def test_get_unwraps_the_data_envelope(self, custom_fields_server: MockAPIServer) -> None:
        """GET on the by-id path, unwrapped to the field itself."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            field = await client.custom_fields.get(team_id=42, custom_field_id=42)

        assert field.id == 42
        assert field.modified_time_utc == datetime(2026, 4, 6, 10, 59, 4, tzinfo=UTC)

        request = custom_fields_server.last_request
        assert request.method == "GET"
        assert request.path == CUSTOM_FIELDS_ITEM
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_definition_round_trips_all_three_step_kinds(self, custom_fields_server: MockAPIServer) -> None:
        """The ``oneOf`` cascade discriminates the same way on the async path."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            field = await client.custom_fields.get(team_id=42, custom_field_id=42)

        steps = field.definition.items
        assert [type(step) for step in steps] == [FunctionStep, LookupStep, ConditionStep]
        assert steps[0].arguments[0].value.value == "platform"
        assert steps[1].map_.additional_properties == {"1": "2", "a": "b"}
        assert steps[2].cases[0].condition.rule == "equals"
        assert isinstance(steps[2].cases[0].return_, DefinitionValue)

    @pytest.mark.asyncio
    async def test_get_metadata_hits_the_metadata_path(self, custom_fields_server: MockAPIServer) -> None:
        """``metadata`` is its own route, not a custom field id."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            metadata = await client.custom_fields.get_metadata(team_id=42)

        assert metadata.functions.items[0].name == "upper_case"
        assert metadata.field_data_types == ["string.text.value"]
        assert metadata.data_transformation_steps_limit == 10

        request = custom_fields_server.last_request
        assert request.method == "GET"
        assert request.path == CUSTOM_FIELDS_METADATA
        assert request.path != CUSTOM_FIELDS_ITEM

    @pytest.mark.asyncio
    async def test_create_returns_the_field_and_sends_field_type(self, api_server: MockAPIServer) -> None:
        """201 on the async path, with ``field_type`` and all three step kinds on the wire."""
        api_server.route(
            CUSTOM_FIELDS_COLLECTION,
            ScriptedResponse(
                status=201,
                json_body=CUSTOM_FIELD_SINGLE_BODY,
                headers={"Location": "https://api.supermetrics.com/v1/teams/42/custom-fields/42"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            field = await client.custom_fields.create(
                team_id=42,
                display_name="Spec Example Field",
                field_type="dim",
                data_type="string.text.value",
                definition=_definition_in_python(),
            )

        assert field.id == 42

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == CUSTOM_FIELDS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body["field_type"] == "dim"
        assert [step["type"] for step in body["definition"]] == ["function", "lookup", "condition"]
        assert "return" in body["definition"][2]["cases"][0]

    @pytest.mark.asyncio
    async def test_update_omits_field_type_and_data_source(self, api_server: MockAPIServer) -> None:
        """The create/update asymmetry holds on the async client as well."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(json_body=CUSTOM_FIELD_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            field = await client.custom_fields.update(
                team_id=42,
                custom_field_id=42,
                display_name="Renamed Field",
                data_type="string.text.value",
                definition=_definition_in_python(),
            )

        assert field.id == 42

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == CUSTOM_FIELDS_ITEM

        body: dict[str, Any] = request.json()
        assert "field_type" not in body
        assert "data_source" not in body
        assert set(body) == {"display_name", "data_type", "definition"}

    @pytest.mark.asyncio
    async def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """204 with an empty body means ``None``, not a parse error."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.custom_fields.delete(team_id=42, custom_field_id=42)

        assert result is None

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == CUSTOM_FIELDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""
