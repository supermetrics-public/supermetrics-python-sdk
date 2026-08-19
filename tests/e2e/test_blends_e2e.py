"""End-to-end tests for the Data Blending resource.

Drives all five methods over a real loopback socket. Blends stay on the core API host —
the paths keep their ``/v1`` prefix and there is no re-hosting to the Data Warehouse host
— so one server is the whole story here.

This domain earns a wire-level suite more than most. A blend is not the same shape going
out as coming back: every collection is a **bare array in the request** and an
``{"items": [...]}`` object in the response, at every level of nesting. On top of that,
``create`` sends ``type`` and ``update`` does not, new data sources are addressed by a
temporary ``blend_data_source_key`` while existing ones are addressed by
``blend_data_source_id``, and the response side drops the key entirely. None of that is
observable from a mocked transport: it only exists in the bytes on the socket, so it is
asserted here on ``api_server.last_request`` rather than on a return value.
"""

from __future__ import annotations

import re
import uuid
from datetime import UTC, datetime
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import (
    BlendConfig,
    BlendConfigQueryTable,
    BlendDatasourceFieldRef,
    BlendedDataSourceInput,
    BlendedDataSourceInputAccountsItem,
    BlendedDataSourceInputDataSourceSettingsItem,
    BlendedDataSourceInputReportTypeSettingsItem,
    BlendedDataSourceInputSegmentsItem,
    BlendField,
    BlendJoin,
    BlendJoinCondition,
    BlendJoinJoinTable,
    SupermetricsAsyncClient,
    SupermetricsClient,
)
from supermetrics._generated.supermetrics_api_client.models.blend_datasource_field_ref_output_meta_type_0 import (
    BlendDatasourceFieldRefOutputMetaType0,
)
from supermetrics._generated.supermetrics_api_client.types import Unset

from .conftest import (
    BLEND_EMPTY_LIST_BODY,
    BLEND_JOIN_SINGLE_BODY,
    BLEND_SINGLE_BODY,
    BLENDS_COLLECTION,
    BLENDS_ITEM,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e

#: The create-time aliases for the two data sources. Upstream constrains a
#: ``blend_data_source_key`` to exactly eight lowercase alphanumerics, and the tests below
#: assert the values that actually reach the wire still match that.
_GA4_KEY = "abcd1234"
_GADS_KEY = "efgh5678"

#: The pattern upstream enforces on ``blend_data_source_key``.
_KEY_PATTERN = re.compile(r"^[a-z0-9]{8}$")


def _new_source(key: str, data_source_id: str, display_name: str) -> BlendedDataSourceInput:
    """Build a data source the way a caller creating a blend would.

    ``blend_data_source_id``, ``blend_data_source_key``, ``report_type`` and
    ``report_type_settings`` are required-but-nullable upstream, so the generated model
    makes them positional with no default even though three of them are routinely empty
    on a create. A brand new source has no id yet, so it is named by ``key`` instead and
    every field and join reference in the same request points at that key.
    """
    return BlendedDataSourceInput(
        data_source_id=data_source_id,
        blend_data_source_id=None,
        blend_data_source_key=key,
        report_type=None,
        report_type_settings=[],
        display_name=display_name,
        data_source_settings=[
            BlendedDataSourceInputDataSourceSettingsItem(id="currency", value="EUR"),
            BlendedDataSourceInputDataSourceSettingsItem(id="row_limit", value=1000),
        ],
        accounts=[BlendedDataSourceInputAccountsItem(account_id="1234567890", account_name="Acme Corp")],
        segments=[BlendedDataSourceInputSegmentsItem(id="organic_traffic", name="Organic Traffic")],
    )


def _existing_source(blend_data_source_id: int, data_source_id: str, display_name: str) -> BlendedDataSourceInput:
    """Build a data source that upstream already knows about, addressed by its id.

    The mirror image of :func:`_new_source`: the id is set and the key is null. An update
    body may legitimately carry one of each, which is what
    ``test_update_may_mix_data_source_ids_and_keys`` pins.
    """
    return BlendedDataSourceInput(
        data_source_id=data_source_id,
        blend_data_source_id=blend_data_source_id,
        blend_data_source_key=None,
        report_type="organic_search",
        report_type_settings=[BlendedDataSourceInputReportTypeSettingsItem(id="date_range", value="last_30_days")],
        display_name=display_name,
    )


def _ref_by_key(key: str, field_name: str, field_type: str) -> BlendDatasourceFieldRef:
    """Reference a field on a not-yet-created data source, by its temporary key."""
    return BlendDatasourceFieldRef(
        datasource_field_name=field_name,
        field_source="standard",
        blend_data_source_id=None,
        blend_data_source_key=key,
        datasource_field_display_name=field_name,
        datasource_field_type=field_type,
    )


def _ref_by_id(blend_data_source_id: int, field_name: str, field_type: str) -> BlendDatasourceFieldRef:
    """Reference a field on a data source that already exists, by its id."""
    return BlendDatasourceFieldRef(
        datasource_field_name=field_name,
        field_source="standard",
        blend_data_source_id=blend_data_source_id,
        blend_data_source_key=None,
        datasource_field_display_name=field_name,
        datasource_field_type=field_type,
    )


def _union_config() -> BlendConfig:
    """A union blend's config: ``fields`` and nothing else."""
    return BlendConfig(
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_field_display_name="Impressions",
                blend_datasource_fields=[_ref_by_key(_GA4_KEY, "Impressions", "met")],
            )
        ]
    )


def _join_config() -> BlendConfig:
    """A join blend's config: a primary table, one join per extra source, and the fields.

    Nothing in the generated layer stops a caller putting ``joins`` on a union blend or
    leaving ``query_table`` off a join blend — the spec models all three keys as optional
    on one loose ``BlendConfig`` rather than as a discriminated union, so upstream is what
    rejects a mismatch, with a 400.
    """
    return BlendConfig(
        query_table=BlendConfigQueryTable(blend_data_source_id=None, blend_data_source_key=_GA4_KEY),
        joins=[
            BlendJoin(
                join_table=BlendJoinJoinTable(blend_data_source_id=None, blend_data_source_key=_GADS_KEY),
                type_="left",
                conditions=[
                    BlendJoinCondition(
                        operator="=",
                        left=_ref_by_key(_GA4_KEY, "Date", "dim"),
                        right=_ref_by_key(_GADS_KEY, "Date", "dim"),
                    )
                ],
            )
        ],
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_field_display_name="Impressions",
                blend_datasource_fields=[
                    _ref_by_key(_GA4_KEY, "Impressions", "met"),
                    _ref_by_key(_GADS_KEY, "Impressions", "met"),
                ],
            )
        ],
    )


def _mixed_update_config() -> BlendConfig:
    """A config whose one field maps an existing source and a newly added one at once."""
    return BlendConfig(
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_field_display_name="Impressions",
                blend_datasource_fields=[
                    _ref_by_id(1, "Impressions", "met"),
                    _ref_by_key(_GADS_KEY, "Impressions", "met"),
                ],
            )
        ]
    )


class TestBlendsResource:
    """Synchronous blend CRUD and listing."""

    def test_list_returns_both_summaries_from_data_items(self, blends_server: MockAPIServer) -> None:
        """The collection lives at ``data.items``; the adapter hands back the summaries."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blends = client.blends.list(team_id=42)

        assert len(blends) == 2
        assert [blend.blend_id for blend in blends] == [569, 570]
        assert [blend.type_ for blend in blends] == ["union", "join"]
        assert blends[0].display_name == "GA4 impressions"
        assert blends[1].display_name == "GA4 joined to Google Ads"

    def test_list_without_a_filter_sends_an_empty_query_string(self, blends_server: MockAPIServer) -> None:
        """No ``blend_type`` means no query string at all.

        This endpoint is not paginated, so unlike custom fields there is no ``limit``
        default in the generated layer to suppress. The adapter passes ``UNSET`` and the
        generated ``_get_kwargs`` drops it, which has to leave the URL bare.
        """
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.list(team_id=42)

        request = blends_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == BLENDS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_by_type_sends_exactly_one_query_parameter(self, blends_server: MockAPIServer) -> None:
        """``blend_type`` is spelled ``type`` on the wire, and it is the only parameter."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.list(team_id=42, blend_type="join")

        request = blends_server.last_request
        assert urlsplit(request.path).path == BLENDS_COLLECTION
        assert parse_qs(urlsplit(request.path).query) == {"type": ["join"]}

    def test_list_returns_an_empty_list_when_data_omits_items(self, api_server: MockAPIServer) -> None:
        """``data.items`` is optional upstream — a team with no blends is not an error."""
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(json_body=BLEND_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            blends = client.blends.list(team_id=42)

        assert blends == []

    def test_a_list_summary_carries_no_config(self, blends_server: MockAPIServer) -> None:
        """List and get return different types, and the difference is visible here.

        ``BlendListItemOutput`` has no ``config`` attribute at all — not an unset one — and
        its data sources are the reduced four-key ``BlendListDataSourceOutput`` rather than
        the full source shape. A caller who wants a blend's fields has to ``get`` it.
        """
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            summary = client.blends.list(team_id=42)[0]

        assert not hasattr(summary, "config")

        source = summary.blended_data_sources.items[0]
        assert source.blend_data_source_id == 1
        assert source.data_source_id == "GA4"
        assert source.display_name == "Google Analytics 4"
        assert source.logo_url == "https://cdn.supermetrics.com/images/datasource-logos/GA4.png"
        assert not hasattr(source, "data_source_settings")

    def test_get_unwraps_the_data_envelope(self, blends_server: MockAPIServer) -> None:
        """The response is ``{meta, data}``; the adapter returns the blend itself."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        assert blend.blend_id == 569
        assert blend.type_ == "union"
        assert blend.display_name == "GA4 impressions"
        assert blend.description == "Example blend description"
        assert blend.last_modify_user_email == "user@supermetrics.com"

    def test_get_sends_a_get_to_the_by_id_path(self, blends_server: MockAPIServer) -> None:
        """GET on ``/v1/teams/{team}/data-blending/blends/{id}`` with no body."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.get(team_id=42, blend_id=569)

        request = blends_server.last_request
        assert request.method == "GET"
        assert request.path == BLENDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_modified_time_parses_to_an_aware_datetime(self, blends_server: MockAPIServer) -> None:
        """``"2026-04-07T10:00:00+0000"`` uses a numeric offset — no colon, no trailing ``Z``.

        The generated model hands that string to ``datetime.fromisoformat``, which only
        learned to accept the colon-less offset in Python 3.11. That is the SDK's floor, so
        this passes today and would fail loudly if the floor ever slipped. ``blend_uuid``
        is likewise parsed rather than passed through as a string.
        """
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        assert blend.modified_time_utc == datetime(2026, 4, 7, 10, 0, tzinfo=UTC)
        assert blend.modified_time_utc.tzinfo is not None
        assert blend.blend_uuid == uuid.UUID("71bc0582-31b5-11f1-a55c-4201ac182030")
        assert isinstance(blend.blend_uuid, uuid.UUID)

    def test_union_config_has_no_query_table_or_joins(self, blends_server: MockAPIServer) -> None:
        """On a union blend the two join-only keys are absent, and absent means ``Unset``.

        The generated layer distinguishes "the server did not send this" from "the server
        sent null", so these have to be tested with ``isinstance(..., Unset)``. ``is None``
        would pass for a null and silently stop catching a regression that started sending
        one.
        """
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        assert blend.type_ == "union"
        assert isinstance(blend.config.query_table, Unset)
        assert isinstance(blend.config.joins, Unset)

        field = blend.config.fields.items[0]
        assert field.blend_field_name == "impressions"
        assert field.blend_field_type == "met"
        assert field.blend_field_data_type == "int.number.value"

    def test_join_config_carries_the_query_table_and_joins(self, blends_server: MockAPIServer) -> None:
        """A join blend adds a primary table and one join, both addressed by id.

        The response never speaks in ``blend_data_source_key``: it is a request-scoped
        alias, so the tables here name their sources by the ids upstream assigned.
        """
        blends_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_JOIN_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        assert blend.type_ == "join"
        assert blend.config.query_table.blend_data_source_id == 1

        join = blend.config.joins.items[0]
        assert join.type_ == "left"
        assert join.join_table.blend_data_source_id == 2

        condition = join.conditions.items[0]
        assert condition.operator == "="
        assert condition.left.blend_data_source_id == 1
        assert condition.left.datasource_field_name == "Date"
        assert condition.left.datasource_field_type == "dim"
        assert condition.right.blend_data_source_id == 2
        assert condition.right.datasource_field_name == "Date"
        assert not hasattr(condition.left, "blend_data_source_key")

    def test_every_response_collection_is_wrapped_in_items(self, blends_server: MockAPIServer) -> None:
        """The defining quirk of this domain, walked end to end on one blend.

        Requests send bare arrays; responses wrap every one of them in an object with a
        single ``items`` key — data sources, fields, per-field references, joins and join
        conditions alike. A blend therefore cannot be read back and resent unchanged, and
        pinning all five levels in one place is what keeps that asymmetry from being
        mistaken for a bug in the adapter.
        """
        blends_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_JOIN_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        sources = blend.blended_data_sources.items
        assert [source.data_source_id for source in sources] == ["GA4", "GADS"]

        fields = blend.config.fields.items
        assert len(fields) == 1

        references = fields[0].blend_datasource_fields.items
        assert [reference.blend_data_source_id for reference in references] == [1, 2]

        joins = blend.config.joins.items
        assert len(joins) == 1

        conditions = joins[0].conditions.items
        assert [condition.operator for condition in conditions] == ["="]

    def test_response_settings_items_are_untyped_objects(self, blends_server: MockAPIServer) -> None:
        """Response-side settings, accounts and segments come back as free-form models.

        Only the *request* side has typed items with ``.id`` and ``.value``; upstream
        declares the response items as bare objects, so the generated layer parses them
        into models whose entire content lives in ``additional_properties``. The value is a
        three-way ``anyOf`` that nothing discriminates — the generated parser is a bare
        ``cast`` — so all four kinds are round-tripped here to prove the JSON types survive
        intact rather than being coerced.
        """
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        settings = blend.blended_data_sources.items[0].data_source_settings.items
        assert settings[0].additional_properties == {"id": "currency", "value": "EUR"}
        assert isinstance(settings[0].additional_properties["value"], str)

        assert settings[1].additional_properties == {"id": "row_limit", "value": 1000}
        assert type(settings[1].additional_properties["value"]) is int

        assert settings[2].additional_properties["value"] is True
        assert settings[3].additional_properties["value"] is None

        source = blend.blended_data_sources.items[0]
        assert source.accounts.items[0].additional_properties == {
            "account_id": "1234567890",
            "account_name": "Acme Corp",
        }
        assert source.segments.items[0].additional_properties == {"id": "organic_traffic", "name": "Organic Traffic"}
        assert source.report_type_settings.items == []

    def test_a_field_reference_meta_is_null_or_a_free_form_object(self, blends_server: MockAPIServer) -> None:
        """``meta`` is parsed by a try/except cascade, so both branches need exercising.

        JSON ``null`` has to arrive as ``None`` and an object as a model carrying the
        contents in ``additional_properties``. The join payload's one field maps both
        sources, with a null ``meta`` on the first and an object on the second, so a single
        blend covers both arms.
        """
        blends_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_JOIN_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = client.blends.get(team_id=42, blend_id=569)

        ga4_ref, gads_ref = blend.config.fields.items[0].blend_datasource_fields.items

        assert ga4_ref.meta is None

        assert isinstance(gads_ref.meta, BlendDatasourceFieldRefOutputMetaType0)
        assert gads_ref.meta.additional_properties == {"account_override": "1234567890"}

    def test_create_returns_the_blend_from_a_201(self, api_server: MockAPIServer) -> None:
        """Creation answers ``201 Created`` — not 200 — and returns the persisted blend."""
        api_server.route(
            BLENDS_COLLECTION,
            ScriptedResponse(
                status=201,
                json_body=BLEND_SINGLE_BODY,
                headers={"Location": "https://api.supermetrics.com/v1/teams/42/data-blending/blends/569"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            blend = client.blends.create(
                team_id=42,
                display_name="GA4 impressions",
                blend_type="union",
                blended_data_sources=[_new_source(_GA4_KEY, "GA4", "Google Analytics 4")],
                config=_union_config(),
            )

        assert blend.blend_id == 569
        assert blend.blend_uuid == uuid.UUID("71bc0582-31b5-11f1-a55c-4201ac182030")
        assert blend.blended_data_sources.items[0].blend_data_source_id == 1

    def test_create_sends_bare_arrays_and_addresses_sources_by_key(self, api_server: MockAPIServer) -> None:
        """The request half of the asymmetry, plus the create-time alias.

        ``blended_data_sources`` and ``config.fields`` go out as bare JSON arrays even
        though they come back wrapped in ``items``, the blend kind is spelled ``type`` and
        not ``type_``, and every reference names its source by the temporary
        ``blend_data_source_key`` with ``blend_data_source_id`` explicitly null, because
        the source does not exist yet and has no id to point at.
        """
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=201, json_body=BLEND_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.create(
                team_id=42,
                display_name="GA4 impressions",
                blend_type="union",
                blended_data_sources=[_new_source(_GA4_KEY, "GA4", "Google Analytics 4")],
                config=_union_config(),
                description="Example blend description",
            )

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == BLENDS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert set(body) == {"display_name", "blended_data_sources", "config", "type", "description"}
        assert body["type"] == "union"
        assert "type_" not in body
        assert body["display_name"] == "GA4 impressions"
        assert body["description"] == "Example blend description"

        sources = body["blended_data_sources"]
        assert isinstance(sources, list)
        assert sources[0]["blend_data_source_id"] is None
        assert sources[0]["blend_data_source_key"] == _GA4_KEY
        assert _KEY_PATTERN.fullmatch(sources[0]["blend_data_source_key"])
        assert sources[0]["report_type"] is None
        assert sources[0]["report_type_settings"] == []
        assert sources[0]["data_source_settings"] == [
            {"id": "currency", "value": "EUR"},
            {"id": "row_limit", "value": 1000},
        ]
        assert sources[0]["accounts"] == [{"account_id": "1234567890", "account_name": "Acme Corp"}]
        assert sources[0]["segments"] == [{"id": "organic_traffic", "name": "Organic Traffic"}]

        fields = body["config"]["fields"]
        assert isinstance(fields, list)
        assert set(body["config"]) == {"fields"}

        reference = fields[0]["blend_datasource_fields"]
        assert isinstance(reference, list)
        assert reference[0]["blend_data_source_key"] == _GA4_KEY
        assert reference[0]["blend_data_source_id"] is None

    def test_create_omits_description_when_it_is_not_given(self, api_server: MockAPIServer) -> None:
        """An omitted description is absent from the body, not sent as ``null``.

        The adapter turns ``None`` into ``UNSET`` rather than passing it through, which is
        the difference between "leave this alone" and "clear this".
        """
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=201, json_body=BLEND_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.create(
                team_id=42,
                display_name="GA4 impressions",
                blend_type="union",
                blended_data_sources=[_new_source(_GA4_KEY, "GA4", "Google Analytics 4")],
                config=_union_config(),
                description=None,
            )

        body: dict[str, Any] = api_server.last_request.json()
        assert "description" not in body
        assert set(body) == {"display_name", "blended_data_sources", "config", "type"}

    def test_create_of_a_join_blend_sends_the_query_table_and_joins(self, api_server: MockAPIServer) -> None:
        """A join blend's config carries two more keys, and they nest bare arrays too.

        ``config.joins`` is a bare array of joins, and each join's ``conditions`` is a bare
        array of its own — the wrapping only ever happens on the way back.
        """
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=201, json_body=BLEND_JOIN_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            blend = client.blends.create(
                team_id=42,
                display_name="GA4 joined to Google Ads",
                blend_type="join",
                blended_data_sources=[
                    _new_source(_GA4_KEY, "GA4", "Google Analytics 4"),
                    _new_source(_GADS_KEY, "GADS", "Google Ads"),
                ],
                config=_join_config(),
            )

        assert blend.type_ == "join"

        body: dict[str, Any] = api_server.last_request.json()
        assert body["type"] == "join"
        assert set(body["config"]) == {"query_table", "joins", "fields"}
        assert body["config"]["query_table"] == {"blend_data_source_id": None, "blend_data_source_key": _GA4_KEY}

        joins = body["config"]["joins"]
        assert isinstance(joins, list)
        assert joins[0]["type"] == "left"
        assert "type_" not in joins[0]
        assert joins[0]["join_table"] == {"blend_data_source_id": None, "blend_data_source_key": _GADS_KEY}

        conditions = joins[0]["conditions"]
        assert isinstance(conditions, list)
        assert conditions[0]["operator"] == "="
        assert conditions[0]["left"]["blend_data_source_key"] == _GA4_KEY
        assert conditions[0]["left"]["datasource_field_name"] == "Date"
        assert conditions[0]["right"]["blend_data_source_key"] == _GADS_KEY
        assert conditions[0]["right"]["datasource_field_name"] == "Date"

    def test_update_returns_the_blend_from_a_200(self, api_server: MockAPIServer) -> None:
        """A replace answers 200 — not 201 — and returns the updated blend."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            blend = client.blends.update(
                team_id=42,
                blend_id=569,
                display_name="GA4 impressions, revised",
                blended_data_sources=[_existing_source(1, "GA4", "Google Analytics 4")],
                config=_mixed_update_config(),
            )

        assert blend.blend_id == 569
        assert blend.display_name == "GA4 impressions"

    def test_update_omits_the_blend_type(self, api_server: MockAPIServer) -> None:
        """The create/update asymmetry: a blend's kind cannot be changed after creation.

        ``update`` takes no ``blend_type`` argument at all, and ``type`` must not leak into
        the PUT body — upstream states the kind is fixed and the request schema does not
        carry it, so unlike most update methods this one is not create with an id attached.
        """
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.update(
                team_id=42,
                blend_id=569,
                display_name="GA4 impressions, revised",
                blended_data_sources=[_existing_source(1, "GA4", "Google Analytics 4")],
                config=_union_config(),
                description="Now with a description",
            )

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == BLENDS_ITEM
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "type" not in body
        assert set(body) == {"display_name", "blended_data_sources", "config", "description"}
        assert body["display_name"] == "GA4 impressions, revised"

    def test_update_may_mix_data_source_ids_and_keys(self, api_server: MockAPIServer) -> None:
        """One update body can address an existing source by id and a new one by key.

        Adding a source to a blend is an update, and the new source has no id yet, so it
        needs the same temporary key a create would use while its established sibling
        keeps being addressed by id. Both spellings have to survive into the same body, and
        the field references have to follow suit.
        """
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_JOIN_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.update(
                team_id=42,
                blend_id=569,
                display_name="GA4 joined to Google Ads",
                blended_data_sources=[
                    _existing_source(1, "GA4", "Google Analytics 4"),
                    _new_source(_GADS_KEY, "GADS", "Google Ads"),
                ],
                config=_mixed_update_config(),
            )

        body: dict[str, Any] = api_server.last_request.json()

        existing, added = body["blended_data_sources"]
        assert existing["blend_data_source_id"] == 1
        assert existing["blend_data_source_key"] is None
        assert added["blend_data_source_id"] is None
        assert added["blend_data_source_key"] == _GADS_KEY
        assert _KEY_PATTERN.fullmatch(added["blend_data_source_key"])

        by_id, by_key = body["config"]["fields"][0]["blend_datasource_fields"]
        assert by_id["blend_data_source_id"] == 1
        assert by_id["blend_data_source_key"] is None
        assert by_key["blend_data_source_id"] is None
        assert by_key["blend_data_source_key"] == _GADS_KEY

    def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """Deletion answers ``204 No Content`` with a genuinely empty body."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.blends.delete(team_id=42, blend_id=569)

        assert result is None

    def test_delete_sends_a_delete_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """DELETE on the by-id path, with no body of its own."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.delete(team_id=42, blend_id=569)

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == BLENDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""


class TestBlendsAsyncResource:
    """Asynchronous blends — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_both_summaries_and_sends_no_query_string(self, blends_server: MockAPIServer) -> None:
        """The async path unwraps ``data.items`` and leaves the URL bare, identically."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blends = await client.blends.list(team_id=42)

        assert [blend.blend_id for blend in blends] == [569, 570]
        assert not hasattr(blends[0], "config")

        request = blends_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == BLENDS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_list_by_type_sends_exactly_one_query_parameter(self, blends_server: MockAPIServer) -> None:
        """Filter serialization does not differ between the two clients."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            await client.blends.list(team_id=42, blend_type="union")

        assert parse_qs(urlsplit(blends_server.last_request.path).query) == {"type": ["union"]}

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_list_when_data_omits_items(self, api_server: MockAPIServer) -> None:
        """An absent ``data.items`` is an empty collection on the async path too."""
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(json_body=BLEND_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            blends = await client.blends.list(team_id=42)

        assert blends == []

    @pytest.mark.asyncio
    async def test_get_unwraps_the_data_envelope(self, blends_server: MockAPIServer) -> None:
        """GET on the by-id path, unwrapped to the blend itself, dates and uuids parsed."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = await client.blends.get(team_id=42, blend_id=569)

        assert blend.blend_id == 569
        assert blend.display_name == "GA4 impressions"
        assert blend.modified_time_utc == datetime(2026, 4, 7, 10, 0, tzinfo=UTC)
        assert isinstance(blend.blend_uuid, uuid.UUID)

        request = blends_server.last_request
        assert request.method == "GET"
        assert request.path == BLENDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_union_config_has_no_query_table_or_joins(self, blends_server: MockAPIServer) -> None:
        """``Unset``, not ``None``, on the async path as well."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = await client.blends.get(team_id=42, blend_id=569)

        assert isinstance(blend.config.query_table, Unset)
        assert isinstance(blend.config.joins, Unset)
        assert blend.config.fields.items[0].blend_field_name == "impressions"

    @pytest.mark.asyncio
    async def test_join_config_carries_the_query_table_and_joins(self, blends_server: MockAPIServer) -> None:
        """Every wrapped collection in a join blend, walked on the async client."""
        blends_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_JOIN_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = await client.blends.get(team_id=42, blend_id=569)

        assert blend.type_ == "join"
        assert blend.config.query_table.blend_data_source_id == 1
        assert [source.data_source_id for source in blend.blended_data_sources.items] == ["GA4", "GADS"]

        join = blend.config.joins.items[0]
        assert join.type_ == "left"
        assert join.join_table.blend_data_source_id == 2

        condition = join.conditions.items[0]
        assert condition.operator == "="
        assert condition.left.blend_data_source_id == 1
        assert condition.right.blend_data_source_id == 2

        ga4_ref, gads_ref = blend.config.fields.items[0].blend_datasource_fields.items
        assert ga4_ref.meta is None
        assert gads_ref.meta.additional_properties == {"account_override": "1234567890"}

    @pytest.mark.asyncio
    async def test_response_settings_items_are_untyped_objects(self, blends_server: MockAPIServer) -> None:
        """All four JSON value kinds survive the async round trip with their types intact."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            blend = await client.blends.get(team_id=42, blend_id=569)

        settings = blend.blended_data_sources.items[0].data_source_settings.items
        assert settings[0].additional_properties == {"id": "currency", "value": "EUR"}
        assert type(settings[1].additional_properties["value"]) is int
        assert settings[2].additional_properties["value"] is True
        assert settings[3].additional_properties["value"] is None

    @pytest.mark.asyncio
    async def test_create_returns_the_blend_and_sends_a_bare_array(self, api_server: MockAPIServer) -> None:
        """201 on the async path, with ``type`` present and the collections unwrapped."""
        api_server.route(
            BLENDS_COLLECTION,
            ScriptedResponse(
                status=201,
                json_body=BLEND_SINGLE_BODY,
                headers={"Location": "https://api.supermetrics.com/v1/teams/42/data-blending/blends/569"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            blend = await client.blends.create(
                team_id=42,
                display_name="GA4 impressions",
                blend_type="union",
                blended_data_sources=[_new_source(_GA4_KEY, "GA4", "Google Analytics 4")],
                config=_union_config(),
            )

        assert blend.blend_id == 569

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == BLENDS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert set(body) == {"display_name", "blended_data_sources", "config", "type"}
        assert body["type"] == "union"
        assert isinstance(body["blended_data_sources"], list)
        assert isinstance(body["config"]["fields"], list)
        assert body["blended_data_sources"][0]["blend_data_source_key"] == _GA4_KEY
        assert body["config"]["fields"][0]["blend_datasource_fields"][0]["blend_data_source_id"] is None

    @pytest.mark.asyncio
    async def test_create_of_a_join_blend_sends_the_query_table_and_joins(self, api_server: MockAPIServer) -> None:
        """Nested bare arrays — ``joins`` and each join's ``conditions`` — on the async path."""
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=201, json_body=BLEND_JOIN_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            blend = await client.blends.create(
                team_id=42,
                display_name="GA4 joined to Google Ads",
                blend_type="join",
                blended_data_sources=[
                    _new_source(_GA4_KEY, "GA4", "Google Analytics 4"),
                    _new_source(_GADS_KEY, "GADS", "Google Ads"),
                ],
                config=_join_config(),
            )

        assert blend.type_ == "join"

        body: dict[str, Any] = api_server.last_request.json()
        assert body["config"]["query_table"] == {"blend_data_source_id": None, "blend_data_source_key": _GA4_KEY}

        joins = body["config"]["joins"]
        assert isinstance(joins, list)
        assert joins[0]["type"] == "left"
        assert isinstance(joins[0]["conditions"], list)
        assert joins[0]["conditions"][0]["left"]["blend_data_source_key"] == _GA4_KEY
        assert joins[0]["conditions"][0]["right"]["blend_data_source_key"] == _GADS_KEY

    @pytest.mark.asyncio
    async def test_update_omits_the_blend_type(self, api_server: MockAPIServer) -> None:
        """The create/update asymmetry holds on the async client as well."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            blend = await client.blends.update(
                team_id=42,
                blend_id=569,
                display_name="GA4 impressions, revised",
                blended_data_sources=[_existing_source(1, "GA4", "Google Analytics 4")],
                config=_union_config(),
            )

        assert blend.blend_id == 569

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == BLENDS_ITEM

        body: dict[str, Any] = request.json()
        assert "type" not in body
        assert set(body) == {"display_name", "blended_data_sources", "config"}

    @pytest.mark.asyncio
    async def test_update_may_mix_data_source_ids_and_keys(self, api_server: MockAPIServer) -> None:
        """Both ways of addressing a source reach the wire in one async update body."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_JOIN_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.blends.update(
                team_id=42,
                blend_id=569,
                display_name="GA4 joined to Google Ads",
                blended_data_sources=[
                    _existing_source(1, "GA4", "Google Analytics 4"),
                    _new_source(_GADS_KEY, "GADS", "Google Ads"),
                ],
                config=_mixed_update_config(),
            )

        body: dict[str, Any] = api_server.last_request.json()

        existing, added = body["blended_data_sources"]
        assert existing["blend_data_source_id"] == 1
        assert added["blend_data_source_key"] == _GADS_KEY

        by_id, by_key = body["config"]["fields"][0]["blend_datasource_fields"]
        assert by_id["blend_data_source_id"] == 1
        assert by_key["blend_data_source_key"] == _GADS_KEY

    @pytest.mark.asyncio
    async def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """204 with an empty body means ``None``, not a parse error."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.blends.delete(team_id=42, blend_id=569)

        assert result is None

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == BLENDS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""
