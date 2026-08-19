"""Unit tests for BlendsResource and BlendsAsyncResource.

These mock at the generated-client boundary and open no socket. Every patch goes
through ``monkeypatch.setattr`` rather than the save-and-restore-by-hand idiom used
elsewhere in this directory: a bare trailing restore statement is skipped when an
assertion fails, which leaks the mock into every later test in the session.
``monkeypatch`` unwinds on failure too, so a red test stays a single red test.
"""

from __future__ import annotations

import datetime
import uuid
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.blend_config import BlendConfig
from supermetrics._generated.supermetrics_api_client.models.blend_config_output import BlendConfigOutput
from supermetrics._generated.supermetrics_api_client.models.blend_config_output_fields import BlendConfigOutputFields
from supermetrics._generated.supermetrics_api_client.models.blend_config_query_table import BlendConfigQueryTable
from supermetrics._generated.supermetrics_api_client.models.blend_datasource_field_ref import BlendDatasourceFieldRef
from supermetrics._generated.supermetrics_api_client.models.blend_datasource_field_ref_output import (
    BlendDatasourceFieldRefOutput,
)
from supermetrics._generated.supermetrics_api_client.models.blend_field import BlendField
from supermetrics._generated.supermetrics_api_client.models.blend_field_output import BlendFieldOutput
from supermetrics._generated.supermetrics_api_client.models.blend_field_output_blend_datasource_fields import (
    BlendFieldOutputBlendDatasourceFields,
)
from supermetrics._generated.supermetrics_api_client.models.blend_join import BlendJoin
from supermetrics._generated.supermetrics_api_client.models.blend_join_condition import BlendJoinCondition
from supermetrics._generated.supermetrics_api_client.models.blend_join_join_table import BlendJoinJoinTable
from supermetrics._generated.supermetrics_api_client.models.blend_list_data_source_output import (
    BlendListDataSourceOutput,
)
from supermetrics._generated.supermetrics_api_client.models.blend_list_item_output import BlendListItemOutput
from supermetrics._generated.supermetrics_api_client.models.blend_list_item_output_blended_data_sources import (
    BlendListItemOutputBlendedDataSources,
)
from supermetrics._generated.supermetrics_api_client.models.blend_list_response import BlendListResponse
from supermetrics._generated.supermetrics_api_client.models.blend_list_response_data import BlendListResponseData
from supermetrics._generated.supermetrics_api_client.models.blend_output import BlendOutput
from supermetrics._generated.supermetrics_api_client.models.blend_output_blended_data_sources import (
    BlendOutputBlendedDataSources,
)
from supermetrics._generated.supermetrics_api_client.models.blend_response import BlendResponse
from supermetrics._generated.supermetrics_api_client.models.blended_data_source_input import BlendedDataSourceInput
from supermetrics._generated.supermetrics_api_client.models.blended_data_source_output import BlendedDataSourceOutput
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.types import UNSET, Response, Unset
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
from supermetrics.resources import blends as module
from supermetrics.resources.blends import BlendsAsyncResource, BlendsResource

TEAM_ID = 12345
BLEND_ID = 569
BLEND_UUID = uuid.UUID("71bc0582-31b5-11f1-a55c-4201ac182030")

#: Upstream serializes this with a numeric offset and no colon ("+0000"), which
#: ``datetime.fromisoformat`` accepts from Python 3.11 on, so it arrives aware.
MODIFIED_TIME = datetime.datetime(2026, 4, 7, 10, 0, tzinfo=datetime.UTC)

#: Every documented failure status for this domain, paired with the upstream error code
#: and the SDK exception it must become. The by-id operations (get, update, delete)
#: document 400, 401, 403, 404, 429 and 500; the collection operations (list, create)
#: document the same set minus 404, so a 404 there is undocumented and reaches the
#: caller through the generic path — still classified, which is what these tests pin.
#: There is deliberately no 422 anywhere: a rejected blend comes back as 400.
ERROR_CASES: list[tuple[HTTPStatus, str, type[SupermetricsAPIError]]] = [
    (HTTPStatus.BAD_REQUEST, "BAD_REQUEST", SupermetricsValidationError),
    (HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", SupermetricsAuthError),
    (HTTPStatus.FORBIDDEN, "FORBIDDEN", SupermetricsForbiddenError),
    (HTTPStatus.NOT_FOUND, "NOT_FOUND", SupermetricsNotFoundError),
    (HTTPStatus.TOO_MANY_REQUESTS, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


def _make_success_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=parsed)


def _make_created_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.CREATED, content=b"", headers={}, parsed=parsed)


def _make_no_content_response() -> Response:
    return Response(status_code=HTTPStatus.NO_CONTENT, content=b"", headers={}, parsed=None)


def _make_error_response(status_code: HTTPStatus, code: str, message: str) -> Response:
    return Response(
        status_code=status_code,
        content=b"",
        headers={},
        parsed=ErrorResponse(
            meta=ResponseMeta(request_id="req-id"),
            error=Error(code=code, message=message),
        ),
    )


def _data_source_input() -> BlendedDataSourceInput:
    """Build a create-time data source, named by the 8-character key it has instead of an id."""
    return BlendedDataSourceInput(
        data_source_id="GA4",
        blend_data_source_id=None,
        blend_data_source_key="abcd1234",
        report_type=None,
        report_type_settings=[],
        display_name="Google Analytics 4",
    )


def _field_ref(datasource_field_name: str) -> BlendDatasourceFieldRef:
    """Build a request-side field reference, which points at the data source by key, not by id."""
    return BlendDatasourceFieldRef(
        datasource_field_name=datasource_field_name,
        field_source="standard",
        blend_data_source_key="abcd1234",
        datasource_field_type="met",
    )


def _union_config() -> BlendConfig:
    """Build a union blend's config: fields only, and sent as a bare list rather than an items wrapper."""
    return BlendConfig(
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_datasource_fields=[_field_ref("Impressions")],
                blend_field_display_name="Impressions",
            )
        ]
    )


def _join_config() -> BlendConfig:
    """Build a join blend's config, which adds query_table and joins — absent on a union blend."""
    return BlendConfig(
        query_table=BlendConfigQueryTable(blend_data_source_key="abcd1234"),
        joins=[
            BlendJoin(
                join_table=BlendJoinJoinTable(blend_data_source_key="efgh5678"),
                type_="left",
                conditions=[BlendJoinCondition(operator="=", left=_field_ref("Date"), right=_field_ref("Date"))],
            )
        ],
        fields=[BlendField(blend_field_name="date", blend_datasource_fields=[_field_ref("Date")])],
    )


def _sample_summary() -> BlendListItemOutput:
    """Build a list-shaped blend summary: no config, and a reduced four-attribute data source."""
    return BlendListItemOutput(
        blend_id=BLEND_ID,
        blend_uuid=BLEND_UUID,
        type_="union",
        display_name="My Blend",
        description="Description of the blend",
        modified_time_utc=MODIFIED_TIME,
        last_modify_user_email="user@supermetrics.com",
        blended_data_sources=BlendListItemOutputBlendedDataSources(
            items=[
                BlendListDataSourceOutput(
                    blend_data_source_id=1,
                    data_source_id="GA4",
                    display_name="Google Analytics 4",
                    logo_url="https://cdn.supermetrics.com/images/datasource-logos/GA4.png",
                )
            ]
        ),
    )


def _sample_blend() -> BlendOutput:
    """Build a persisted union blend; every response-side collection sits behind an ``items`` wrapper."""
    return BlendOutput(
        blend_id=BLEND_ID,
        blend_uuid=BLEND_UUID,
        type_="union",
        display_name="My Blend",
        description="Description of the blend",
        modified_time_utc=MODIFIED_TIME,
        last_modify_user_email="user@supermetrics.com",
        blended_data_sources=BlendOutputBlendedDataSources(
            items=[
                BlendedDataSourceOutput(
                    blend_data_source_id=146715,
                    blend_id=BLEND_ID,
                    data_source_id="GA4",
                    display_name="Google Analytics 4",
                    report_type=None,
                )
            ]
        ),
        config=BlendConfigOutput(
            fields=BlendConfigOutputFields(
                items=[
                    BlendFieldOutput(
                        blend_field_name="impressions",
                        blend_field_display_name="Impressions",
                        blend_field_type="met",
                        blend_field_data_type="int.number.value",
                        blend_datasource_fields=BlendFieldOutputBlendDatasourceFields(
                            items=[
                                BlendDatasourceFieldRefOutput(
                                    blend_data_source_id=146715,
                                    datasource_field_name="Impressions",
                                    datasource_field_type="met",
                                    field_source="standard",
                                )
                            ]
                        ),
                    )
                ]
            )
        ),
    )


def _list_response(data: BlendListResponseData) -> BlendListResponse:
    """Wrap blend summaries in the list envelope, whose meta is the plain Meta: no pagination block."""
    return BlendListResponse(meta=Meta(request_id="req_0123456789ab"), data=data)


class TestBlendsResource:
    """Test suite for BlendsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def blends_resource(self, mock_client: MagicMock) -> BlendsResource:
        """Create a BlendsResource instance with mock client."""
        return BlendsResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_summary(self) -> BlendListItemOutput:
        """Create a sample blend summary as the list endpoint returns it."""
        return _sample_summary()

    @pytest.fixture
    def sample_blend(self) -> BlendOutput:
        """Create a sample persisted blend, config included, for testing."""
        return _sample_blend()

    @pytest.fixture
    def blended_data_sources(self) -> list[BlendedDataSourceInput]:
        """Create a request-shaped data source list: a bare list, keyed rather than identified."""
        return [_data_source_input()]

    @pytest.fixture
    def blend_config(self) -> BlendConfig:
        """Create a request-shaped union config."""
        return _union_config()

    # --- list() ---

    def test_list_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_summary: BlendListItemOutput,
    ) -> None:
        """Test that list() unwraps data.items and preserves the parsed UUID and aware timestamp."""
        monkeypatch.setattr(
            module.get_team_blends,
            "sync_detailed",
            MagicMock(
                return_value=_make_success_response(_list_response(BlendListResponseData(items=[sample_summary])))
            ),
        )

        summaries = blends_resource.list(team_id=TEAM_ID)

        assert len(summaries) == 1
        assert summaries[0].blend_id == BLEND_ID
        assert summaries[0].display_name == "My Blend"
        assert summaries[0].type_ == "union"
        assert summaries[0].last_modify_user_email == "user@supermetrics.com"
        assert isinstance(summaries[0].blend_uuid, uuid.UUID)
        assert summaries[0].blend_uuid == BLEND_UUID
        assert summaries[0].modified_time_utc == MODIFIED_TIME
        assert summaries[0].modified_time_utc.utcoffset() is not None
        assert summaries[0].blended_data_sources.items[0].data_source_id == "GA4"

    def test_list_passes_supplied_blend_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_summary: BlendListItemOutput,
    ) -> None:
        """Test that a supplied blend_type reaches the generated function as type_."""
        mock_sync = MagicMock(
            return_value=_make_success_response(_list_response(BlendListResponseData(items=[sample_summary])))
        )
        monkeypatch.setattr(module.get_team_blends, "sync_detailed", mock_sync)

        blends_resource.list(team_id=TEAM_ID, blend_type="join")

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["type_"] == "join"

    def test_list_omits_unsupplied_blend_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_summary: BlendListItemOutput,
    ) -> None:
        """Test that an unsupplied blend_type is passed as UNSET, so no filter is pinned on the caller."""
        mock_sync = MagicMock(
            return_value=_make_success_response(_list_response(BlendListResponseData(items=[sample_summary])))
        )
        monkeypatch.setattr(module.get_team_blends, "sync_detailed", mock_sync)

        blends_resource.list(team_id=TEAM_ID)

        assert mock_sync.call_args.kwargs["type_"] is UNSET

    def test_list_returns_empty_when_items_unset(
        self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsResource
    ) -> None:
        """Test that a team with no blends degrades to an empty list rather than raising."""
        monkeypatch.setattr(
            module.get_team_blends,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_list_response(BlendListResponseData()))),
        )

        assert blends_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_list_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that list() maps each failure status to its SDK exception."""
        monkeypatch.setattr(
            module.get_team_blends,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            blends_resource.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    def test_list_bad_request_carries_query_context(
        self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsResource
    ) -> None:
        """Test that a 400 from list() is labelled as a bad list query, not a bad blend definition."""
        monkeypatch.setattr(
            module.get_team_blends,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "unknown type")),
        )

        with pytest.raises(SupermetricsValidationError) as exc_info:
            blends_resource.list(team_id=TEAM_ID, blend_type="union")

        assert "Invalid blend list query" in str(exc_info.value)
        assert "Invalid blend definition" not in str(exc_info.value)

    def test_list_network_error(self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsResource) -> None:
        """Test that list() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/data-blending/blends"
        monkeypatch.setattr(
            module.get_team_blends,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            blends_resource.list(team_id=TEAM_ID)

    # --- get() ---

    def test_get_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        meta: Meta,
    ) -> None:
        """Test that get() unwraps .data and that every response collection keeps its items wrapper."""
        monkeypatch.setattr(
            module.get_blend,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend))),
        )

        blend = blends_resource.get(team_id=TEAM_ID, blend_id=BLEND_ID)

        assert blend.blend_id == BLEND_ID
        assert blend.type_ == "union"
        assert blend.blended_data_sources.items[0].blend_data_source_id == 146715
        field = blend.config.fields.items[0]
        assert field.blend_field_name == "impressions"
        assert field.blend_field_type == "met"
        assert field.blend_datasource_fields.items[0].datasource_field_name == "Impressions"
        # A union blend leaves these Unset rather than None, so they must not be tested with `is None`.
        assert isinstance(blend.config.query_table, Unset)
        assert isinstance(blend.config.joins, Unset)

    def test_get_passes_correct_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        meta: Meta,
    ) -> None:
        """Test that get() passes the team and blend ids to the generated client."""
        mock_sync = MagicMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.get_blend, "sync_detailed", mock_sync)

        blends_resource.get(team_id=TEAM_ID, blend_id=BLEND_ID)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["blend_id"] == BLEND_ID

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_get_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that get() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.get_blend,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            blends_resource.get(team_id=TEAM_ID, blend_id=BLEND_ID)

        assert exc_info.value.status_code == int(status)

    def test_get_not_found_message(self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsResource) -> None:
        """Test that a 404 from get() names the blend rather than the team."""
        monkeypatch.setattr(
            module.get_blend,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "nope")),
        )

        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            blends_resource.get(team_id=TEAM_ID, blend_id=999)

        assert "Blend not found" in str(exc_info.value)
        assert "Team not found" not in str(exc_info.value)

    # --- create() ---

    def test_create_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that create() accepts the 201 status and unwraps the created blend."""
        monkeypatch.setattr(
            module.create_blend,
            "sync_detailed",
            MagicMock(return_value=_make_created_response(BlendResponse(meta=meta, data=sample_blend))),
        )

        blend = blends_resource.create(
            team_id=TEAM_ID,
            display_name="My Blend",
            blend_type="union",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        assert blend.blend_id == BLEND_ID
        assert blend.display_name == "My Blend"

    def test_create_builds_request_body(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that create() sends the blend type as the JSON key "type" and collections as bare lists."""
        mock_sync = MagicMock(return_value=_make_created_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.create_blend, "sync_detailed", mock_sync)

        blends_resource.create(
            team_id=TEAM_ID,
            display_name="My Blend",
            blend_type="union",
            blended_data_sources=blended_data_sources,
            config=blend_config,
            description="Description of the blend",
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        body = call_kwargs["body"]
        assert body.type_ == "union"
        assert body.display_name == "My Blend"
        assert body.blended_data_sources == blended_data_sources
        assert body.config is blend_config
        assert body.description == "Description of the blend"

        payload = body.to_dict()
        assert payload["type"] == "union"
        assert isinstance(payload["blended_data_sources"], list)
        assert payload["blended_data_sources"][0]["blend_data_source_key"] == "abcd1234"
        assert isinstance(payload["config"]["fields"], list)

    def test_create_omits_unsupplied_description(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that create() leaves description UNSET and out of the body when the caller omits it."""
        mock_sync = MagicMock(return_value=_make_created_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.create_blend, "sync_detailed", mock_sync)

        blends_resource.create(
            team_id=TEAM_ID,
            display_name="My Blend",
            blend_type="union",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        body = mock_sync.call_args.kwargs["body"]
        assert body.description is UNSET
        assert "description" not in body.to_dict()

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_create_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that create() maps each failure status to its SDK exception."""
        monkeypatch.setattr(
            module.create_blend,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            blends_resource.create(
                team_id=TEAM_ID,
                display_name="My Blend",
                blend_type="union",
                blended_data_sources=blended_data_sources,
                config=blend_config,
            )

        assert exc_info.value.status_code == int(status)

    def test_create_rejected_blend_is_400_not_422(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
    ) -> None:
        """Test that a rejected blend surfaces as a 400 validation error with definition context."""
        monkeypatch.setattr(
            module.create_blend,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "joins on a union")),
        )

        with pytest.raises(SupermetricsValidationError) as exc_info:
            blends_resource.create(
                team_id=TEAM_ID,
                display_name="My Blend",
                blend_type="union",
                blended_data_sources=blended_data_sources,
                config=blend_config,
            )

        assert exc_info.value.status_code == 400
        assert "Invalid blend definition" in str(exc_info.value)

    # --- update() ---

    def test_update_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that update() accepts the 200 status and unwraps the replaced blend."""
        monkeypatch.setattr(
            module.update_blend,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend))),
        )

        blend = blends_resource.update(
            team_id=TEAM_ID,
            blend_id=BLEND_ID,
            display_name="My Blend, revised",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        assert blend.blend_id == BLEND_ID

    def test_update_body_omits_blend_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that update() never sends the blend type, which upstream forbids changing."""
        mock_sync = MagicMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.update_blend, "sync_detailed", mock_sync)

        blends_resource.update(
            team_id=TEAM_ID,
            blend_id=BLEND_ID,
            display_name="My Blend, revised",
            blended_data_sources=blended_data_sources,
            config=blend_config,
            description="Revised",
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["blend_id"] == BLEND_ID
        body = call_kwargs["body"]
        assert body.display_name == "My Blend, revised"
        assert body.description == "Revised"
        assert not hasattr(body, "type_")
        assert "type" not in body.to_dict()

    def test_update_omits_unsupplied_description(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that update() leaves description UNSET and out of the body when the caller omits it."""
        mock_sync = MagicMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.update_blend, "sync_detailed", mock_sync)

        blends_resource.update(
            team_id=TEAM_ID,
            blend_id=BLEND_ID,
            display_name="My Blend, revised",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        body = mock_sync.call_args.kwargs["body"]
        assert body.description is UNSET
        assert "description" not in body.to_dict()

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_update_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that update() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.update_blend,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            blends_resource.update(
                team_id=TEAM_ID,
                blend_id=BLEND_ID,
                display_name="My Blend, revised",
                blended_data_sources=blended_data_sources,
                config=blend_config,
            )

        assert exc_info.value.status_code == int(status)

    # --- delete() ---

    def test_delete_success(self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsResource) -> None:
        """Test that delete() accepts the 204 status and returns None."""
        mock_sync = MagicMock(return_value=_make_no_content_response())
        monkeypatch.setattr(module.delete_blend, "sync_detailed", mock_sync)

        assert blends_resource.delete(team_id=TEAM_ID, blend_id=BLEND_ID) is None

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["blend_id"] == BLEND_ID

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_delete_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that delete() maps each documented failure status to its SDK exception, 404 included."""
        monkeypatch.setattr(
            module.delete_blend,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            blends_resource.delete(team_id=TEAM_ID, blend_id=BLEND_ID)

        assert exc_info.value.status_code == int(status)

    def test_delete_network_error(self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsResource) -> None:
        """Test that delete() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/data-blending/blends/{BLEND_ID}"
        monkeypatch.setattr(
            module.delete_blend,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            blends_resource.delete(team_id=TEAM_ID, blend_id=BLEND_ID)


class TestBlendsAsyncResource:
    """Test suite for BlendsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def blends_resource(self, mock_client: MagicMock) -> BlendsAsyncResource:
        """Create a BlendsAsyncResource instance with mock client."""
        return BlendsAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_summary(self) -> BlendListItemOutput:
        """Create a sample blend summary as the list endpoint returns it."""
        return _sample_summary()

    @pytest.fixture
    def sample_blend(self) -> BlendOutput:
        """Create a sample persisted blend, config included, for testing."""
        return _sample_blend()

    @pytest.fixture
    def blended_data_sources(self) -> list[BlendedDataSourceInput]:
        """Create a request-shaped data source list: a bare list, keyed rather than identified."""
        return [_data_source_input()]

    @pytest.fixture
    def blend_config(self) -> BlendConfig:
        """Create a request-shaped join config, which carries query_table and joins as well as fields."""
        return _join_config()

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_summary: BlendListItemOutput,
    ) -> None:
        """Test that async list() unwraps data.items and preserves the parsed UUID and aware timestamp."""
        monkeypatch.setattr(
            module.get_team_blends,
            "asyncio_detailed",
            AsyncMock(
                return_value=_make_success_response(_list_response(BlendListResponseData(items=[sample_summary])))
            ),
        )

        summaries = await blends_resource.list(team_id=TEAM_ID)

        assert len(summaries) == 1
        assert summaries[0].blend_id == BLEND_ID
        assert isinstance(summaries[0].blend_uuid, uuid.UUID)
        assert summaries[0].modified_time_utc == MODIFIED_TIME
        assert summaries[0].modified_time_utc.utcoffset() is not None

    @pytest.mark.asyncio
    async def test_list_passes_supplied_blend_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_summary: BlendListItemOutput,
    ) -> None:
        """Test that async list() forwards a supplied blend_type as type_."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(_list_response(BlendListResponseData(items=[sample_summary])))
        )
        monkeypatch.setattr(module.get_team_blends, "asyncio_detailed", mock_asyncio)

        await blends_resource.list(team_id=TEAM_ID, blend_type="union")

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["type_"] == "union"

    @pytest.mark.asyncio
    async def test_list_omits_unsupplied_blend_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_summary: BlendListItemOutput,
    ) -> None:
        """Test that async list() passes UNSET when no blend_type was supplied."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(_list_response(BlendListResponseData(items=[sample_summary])))
        )
        monkeypatch.setattr(module.get_team_blends, "asyncio_detailed", mock_asyncio)

        await blends_resource.list(team_id=TEAM_ID)

        assert mock_asyncio.call_args.kwargs["type_"] is UNSET

    @pytest.mark.asyncio
    async def test_list_returns_empty_when_items_unset(
        self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsAsyncResource
    ) -> None:
        """Test that a team with no blends degrades to an empty list on the async path too."""
        monkeypatch.setattr(
            module.get_team_blends,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_list_response(BlendListResponseData()))),
        )

        assert await blends_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_list_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async list() maps each failure status to its SDK exception."""
        monkeypatch.setattr(
            module.get_team_blends,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await blends_resource.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    @pytest.mark.asyncio
    async def test_list_network_error(
        self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsAsyncResource
    ) -> None:
        """Test that async list() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/data-blending/blends"
        monkeypatch.setattr(
            module.get_team_blends,
            "asyncio_detailed",
            AsyncMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            await blends_resource.list(team_id=TEAM_ID)

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        meta: Meta,
    ) -> None:
        """Test that async get() unwraps .data and keeps the nested items wrappers intact."""
        monkeypatch.setattr(
            module.get_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend))),
        )

        blend = await blends_resource.get(team_id=TEAM_ID, blend_id=BLEND_ID)

        assert blend.blend_id == BLEND_ID
        assert blend.blended_data_sources.items[0].data_source_id == "GA4"
        assert blend.config.fields.items[0].blend_field_name == "impressions"

    @pytest.mark.asyncio
    async def test_get_passes_correct_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        meta: Meta,
    ) -> None:
        """Test that async get() passes the team and blend ids to the generated client."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.get_blend, "asyncio_detailed", mock_asyncio)

        await blends_resource.get(team_id=TEAM_ID, blend_id=BLEND_ID)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["blend_id"] == BLEND_ID

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_get_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async get() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.get_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await blends_resource.get(team_id=TEAM_ID, blend_id=BLEND_ID)

        assert exc_info.value.status_code == int(status)

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that async create() accepts the 201 status and unwraps the created blend."""
        monkeypatch.setattr(
            module.create_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_created_response(BlendResponse(meta=meta, data=sample_blend))),
        )

        blend = await blends_resource.create(
            team_id=TEAM_ID,
            display_name="My Blend",
            blend_type="join",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        assert blend.blend_id == BLEND_ID

    @pytest.mark.asyncio
    async def test_create_builds_request_body(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that async create() serializes type_ to the JSON key "type" and sends bare lists."""
        mock_asyncio = AsyncMock(return_value=_make_created_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.create_blend, "asyncio_detailed", mock_asyncio)

        await blends_resource.create(
            team_id=TEAM_ID,
            display_name="My Blend",
            blend_type="join",
            blended_data_sources=blended_data_sources,
            config=blend_config,
            description="Description of the blend",
        )

        body = mock_asyncio.call_args.kwargs["body"]
        assert body.type_ == "join"
        assert body.blended_data_sources == blended_data_sources
        assert body.config is blend_config
        assert body.description == "Description of the blend"

        payload = body.to_dict()
        assert payload["type"] == "join"
        assert isinstance(payload["blended_data_sources"], list)
        assert isinstance(payload["config"]["joins"], list)

    @pytest.mark.asyncio
    async def test_create_omits_unsupplied_description(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that async create() leaves description UNSET and out of the body when the caller omits it."""
        mock_asyncio = AsyncMock(return_value=_make_created_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.create_blend, "asyncio_detailed", mock_asyncio)

        await blends_resource.create(
            team_id=TEAM_ID,
            display_name="My Blend",
            blend_type="join",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        body = mock_asyncio.call_args.kwargs["body"]
        assert body.description is UNSET
        assert "description" not in body.to_dict()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_create_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async create() maps each failure status to its SDK exception."""
        monkeypatch.setattr(
            module.create_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await blends_resource.create(
                team_id=TEAM_ID,
                display_name="My Blend",
                blend_type="join",
                blended_data_sources=blended_data_sources,
                config=blend_config,
            )

        assert exc_info.value.status_code == int(status)

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that async update() accepts the 200 status and unwraps the replaced blend."""
        monkeypatch.setattr(
            module.update_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend))),
        )

        blend = await blends_resource.update(
            team_id=TEAM_ID,
            blend_id=BLEND_ID,
            display_name="My Blend, revised",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        assert blend.blend_id == BLEND_ID

    @pytest.mark.asyncio
    async def test_update_body_omits_blend_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that async update() never sends the blend type, which upstream forbids changing."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.update_blend, "asyncio_detailed", mock_asyncio)

        await blends_resource.update(
            team_id=TEAM_ID,
            blend_id=BLEND_ID,
            display_name="My Blend, revised",
            blended_data_sources=blended_data_sources,
            config=blend_config,
            description="Revised",
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["blend_id"] == BLEND_ID
        body = call_kwargs["body"]
        assert body.description == "Revised"
        assert not hasattr(body, "type_")
        assert "type" not in body.to_dict()

    @pytest.mark.asyncio
    async def test_update_omits_unsupplied_description(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        sample_blend: BlendOutput,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        meta: Meta,
    ) -> None:
        """Test that async update() leaves description UNSET when the caller did not supply one."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(BlendResponse(meta=meta, data=sample_blend)))
        monkeypatch.setattr(module.update_blend, "asyncio_detailed", mock_asyncio)

        await blends_resource.update(
            team_id=TEAM_ID,
            blend_id=BLEND_ID,
            display_name="My Blend, revised",
            blended_data_sources=blended_data_sources,
            config=blend_config,
        )

        assert mock_asyncio.call_args.kwargs["body"].description is UNSET

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_update_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        blended_data_sources: list[BlendedDataSourceInput],
        blend_config: BlendConfig,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async update() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.update_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await blends_resource.update(
                team_id=TEAM_ID,
                blend_id=BLEND_ID,
                display_name="My Blend, revised",
                blended_data_sources=blended_data_sources,
                config=blend_config,
            )

        assert exc_info.value.status_code == int(status)

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_success(self, monkeypatch: pytest.MonkeyPatch, blends_resource: BlendsAsyncResource) -> None:
        """Test that async delete() accepts the 204 status and returns None."""
        mock_asyncio = AsyncMock(return_value=_make_no_content_response())
        monkeypatch.setattr(module.delete_blend, "asyncio_detailed", mock_asyncio)

        assert await blends_resource.delete(team_id=TEAM_ID, blend_id=BLEND_ID) is None

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["blend_id"] == BLEND_ID

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_delete_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        blends_resource: BlendsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async delete() maps each documented failure status to its SDK exception, 404 included."""
        monkeypatch.setattr(
            module.delete_blend,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await blends_resource.delete(team_id=TEAM_ID, blend_id=BLEND_ID)

        assert exc_info.value.status_code == int(status)
