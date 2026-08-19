"""Unit tests for CustomFieldsResource and CustomFieldsAsyncResource.

These mock at the generated-client boundary and open no socket. Every patch goes
through ``monkeypatch.setattr`` rather than the save-and-restore-by-hand idiom used
elsewhere in this directory: a bare trailing restore statement is skipped when an
assertion fails, which leaks the mock into every later test in the session.
``monkeypatch`` unwinds on failure too, so a red test stays a single red test.
"""

from __future__ import annotations

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.condition_case import ConditionCase
from supermetrics._generated.supermetrics_api_client.models.condition_case_condition import ConditionCaseCondition
from supermetrics._generated.supermetrics_api_client.models.condition_step import ConditionStep
from supermetrics._generated.supermetrics_api_client.models.custom_field_create_request_data_source_item import (
    CustomFieldCreateRequestDataSourceItem,
)
from supermetrics._generated.supermetrics_api_client.models.definition_value import DefinitionValue
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.function_argument import FunctionArgument
from supermetrics._generated.supermetrics_api_client.models.function_specification_output import (
    FunctionSpecificationOutput,
)
from supermetrics._generated.supermetrics_api_client.models.function_step import FunctionStep
from supermetrics._generated.supermetrics_api_client.models.lookup_step import LookupStep
from supermetrics._generated.supermetrics_api_client.models.lookup_step_map import LookupStepMap
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.meta_with_pagination import MetaWithPagination
from supermetrics._generated.supermetrics_api_client.models.metadata_output import MetadataOutput
from supermetrics._generated.supermetrics_api_client.models.metadata_output_data import MetadataOutputData
from supermetrics._generated.supermetrics_api_client.models.metadata_output_data_functions import (
    MetadataOutputDataFunctions,
)
from supermetrics._generated.supermetrics_api_client.models.paginated_transformations_output import (
    PaginatedTransformationsOutput,
)
from supermetrics._generated.supermetrics_api_client.models.paginated_transformations_output_data import (
    PaginatedTransformationsOutputData,
)
from supermetrics._generated.supermetrics_api_client.models.pagination import Pagination
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.models.single_transformation_output import (
    SingleTransformationOutput,
)
from supermetrics._generated.supermetrics_api_client.models.team_transformation_output import TeamTransformationOutput
from supermetrics._generated.supermetrics_api_client.models.team_transformation_output_definition import (
    TeamTransformationOutputDefinition,
)
from supermetrics._generated.supermetrics_api_client.models.transformation_user_output import TransformationUserOutput
from supermetrics._generated.supermetrics_api_client.types import UNSET, Response
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
from supermetrics.resources import custom_fields as module
from supermetrics.resources.custom_fields import CustomFieldsAsyncResource, CustomFieldsResource

TEAM_ID = 12345
FIELD_ID = 8231

#: Every documented failure status for this domain, paired with the upstream error code
#: and the SDK exception it must become. There is deliberately no 422 here: a rejected
#: definition comes back as 400.
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


def _function_step() -> FunctionStep:
    """Build a function step: apply ``upper_case`` to a data source field."""
    return FunctionStep(
        type_="function",
        name="upper_case",
        arguments=[FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))],
    )


def _lookup_step() -> LookupStep:
    """Build a lookup step, whose mapping lives in ``LookupStepMap.additional_properties``."""
    step_map = LookupStepMap()
    step_map.additional_properties = {"GOOGLE": "Google Ads", "FACEBOOK": "Meta Ads"}
    return LookupStep(
        type_="lookup",
        rule="equals",
        map_=step_map,
        source=DefinitionValue(type_="output_from_previous", value="0"),
        default=DefinitionValue(type_="static", value="Other"),
    )


def _condition_step() -> ConditionStep:
    """Build a condition step with one case; note the ``return_`` spelling of ``return``."""
    return ConditionStep(
        type_="condition",
        default=DefinitionValue(type_="static", value="Unknown"),
        cases=[
            ConditionCase(
                return_=DefinitionValue(type_="static", value="Paid"),
                condition=ConditionCaseCondition(
                    type_="rule",
                    rule="greater_than",
                    source=DefinitionValue(type_="data_source_field", value="cost"),
                    target=DefinitionValue(type_="static", value="0"),
                ),
            )
        ],
    )


def _sample_field() -> TeamTransformationOutput:
    """Build a persisted custom field carrying all three step kinds, in order."""
    return TeamTransformationOutput(
        id=FIELD_ID,
        name="cf_platform_upper",
        data_source_id="GAWA",
        display_name="Platform (upper)",
        description="Platform name, upper-cased",
        field_type="dim",
        data_type="string.text.value",
        modified_time_utc=datetime.datetime(2026, 4, 6, 10, 59, 4, tzinfo=datetime.UTC),
        modified_user=TransformationUserOutput(email="ada@example.com", first_name="Ada", last_name="Lovelace"),
        definition=TeamTransformationOutputDefinition(items=[_function_step(), _lookup_step(), _condition_step()]),
        report_types=["AD_PERFORMANCE"],
    )


def _sample_metadata() -> MetadataOutputData:
    """Build the definition building blocks returned by the metadata endpoint."""
    return MetadataOutputData(
        functions=MetadataOutputDataFunctions(
            items=[
                FunctionSpecificationOutput(
                    name="upper_case",
                    display_name="Upper case",
                    group_name="Text",
                    return_types=["string.text.value"],
                )
            ]
        ),
        field_data_types=["string.text.value", "float.number.value"],
        data_transformation_steps_limit=10,
    )


def _paginated(data: PaginatedTransformationsOutputData | object) -> PaginatedTransformationsOutput:
    """Wrap a page of custom fields in the paginated envelope the API sends."""
    return PaginatedTransformationsOutput(
        meta=MetaWithPagination(
            request_id="req_0123456789ab",
            pagination=Pagination(total_count=137, limit=25, offset=0),
        ),
        data=data,  # type: ignore[arg-type]
    )


class TestCustomFieldsResource:
    """Test suite for CustomFieldsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def custom_fields_resource(self, mock_client: MagicMock) -> CustomFieldsResource:
        """Create a CustomFieldsResource instance with mock client."""
        return CustomFieldsResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_field(self) -> TeamTransformationOutput:
        """Create a sample persisted custom field for testing."""
        return _sample_field()

    @pytest.fixture
    def sample_metadata(self) -> MetadataOutputData:
        """Create sample custom field metadata for testing."""
        return _sample_metadata()

    @pytest.fixture
    def sample_definition(self) -> list[ConditionStep | FunctionStep | LookupStep]:
        """Create a sample request-shaped definition: a bare list of steps."""
        return [_function_step(), _condition_step()]

    # --- list() ---

    def test_list_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
    ) -> None:
        """Test that list() unwraps data.items and preserves the discriminated step kinds."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "sync_detailed",
            MagicMock(
                return_value=_make_success_response(
                    _paginated(PaginatedTransformationsOutputData(items=[sample_field]))
                )
            ),
        )

        fields = custom_fields_resource.list(team_id=TEAM_ID)

        assert len(fields) == 1
        assert fields[0].id == FIELD_ID
        assert fields[0].display_name == "Platform (upper)"
        assert fields[0].field_type == "dim"
        assert fields[0].modified_time_utc == datetime.datetime(2026, 4, 6, 10, 59, 4, tzinfo=datetime.UTC)
        assert [type(step) for step in fields[0].definition.items] == [FunctionStep, LookupStep, ConditionStep]

    def test_list_passes_supplied_query_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
    ) -> None:
        """Test that every filter the caller supplies reaches the generated function verbatim."""
        mock_sync = MagicMock(
            return_value=_make_success_response(_paginated(PaginatedTransformationsOutputData(items=[sample_field])))
        )
        monkeypatch.setattr(module.fetch_transformation_list, "sync_detailed", mock_sync)

        custom_fields_resource.list(
            team_id=TEAM_ID,
            data_source_id="GAWA",
            display_name="Platform (upper)",
            page=3,
            limit=50,
            include_total_count=True,
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["data_source_id"] == "GAWA"
        assert call_kwargs["display_name"] == "Platform (upper)"
        assert call_kwargs["page"] == 3
        assert call_kwargs["limit"] == 50
        assert call_kwargs["include_total_count"] is True

    def test_list_omits_unsupplied_query_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
    ) -> None:
        """Test that unsupplied filters are passed as UNSET, so limit does not default to 25."""
        mock_sync = MagicMock(
            return_value=_make_success_response(_paginated(PaginatedTransformationsOutputData(items=[sample_field])))
        )
        monkeypatch.setattr(module.fetch_transformation_list, "sync_detailed", mock_sync)

        custom_fields_resource.list(team_id=TEAM_ID)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["data_source_id"] is UNSET
        assert call_kwargs["display_name"] is UNSET
        assert call_kwargs["page"] is UNSET
        assert call_kwargs["limit"] is UNSET
        assert call_kwargs["include_total_count"] is UNSET

    def test_list_returns_empty_when_data_unset(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that an absent data object degrades to an empty list rather than raising."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_paginated(UNSET))),
        )

        assert custom_fields_resource.list(team_id=TEAM_ID) == []

    def test_list_returns_empty_when_items_unset(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that a data object with no items degrades to an empty list rather than raising."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(_paginated(PaginatedTransformationsOutputData()))),
        )

        assert custom_fields_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_list_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that list() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            custom_fields_resource.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    def test_list_bad_request_carries_query_context(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that a 400 from list() is labelled as a bad list query, not a bad definition."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "limit too large")),
        )

        with pytest.raises(SupermetricsValidationError) as exc_info:
            custom_fields_resource.list(team_id=TEAM_ID, limit=500)

        assert "Invalid custom field list query" in str(exc_info.value)

    def test_list_network_error(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that list() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/custom-fields"
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            custom_fields_resource.list(team_id=TEAM_ID)

    # --- get() ---

    def test_get_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        meta: Meta,
    ) -> None:
        """Test that get() unwraps the .data envelope into a TeamTransformationOutput."""
        monkeypatch.setattr(
            module.fetch_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))),
        )

        field = custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        assert field.id == FIELD_ID
        assert field.name == "cf_platform_upper"
        assert field.data_type == "string.text.value"
        lookup = field.definition.items[1]
        assert isinstance(lookup, LookupStep)
        assert lookup.map_.additional_properties == {"GOOGLE": "Google Ads", "FACEBOOK": "Meta Ads"}

    def test_get_passes_correct_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        meta: Meta,
    ) -> None:
        """Test that get() passes the team and custom field ids to the generated client."""
        mock_sync = MagicMock(
            return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.fetch_transformation, "sync_detailed", mock_sync)

        custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["custom_field_id"] == FIELD_ID

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_get_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that get() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.fetch_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        assert exc_info.value.status_code == int(status)

    def test_get_not_found_message(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that a 404 from get() names the custom field rather than the team."""
        monkeypatch.setattr(
            module.fetch_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "nope")),
        )

        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=999)

        assert "Custom field not found" in str(exc_info.value)

    # --- get_metadata() ---

    def test_get_metadata_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_metadata: MetadataOutputData,
        meta: Meta,
    ) -> None:
        """Test that get_metadata() unwraps .data into a MetadataOutputData."""
        monkeypatch.setattr(
            module.fetch_metadata,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(MetadataOutput(meta=meta, data=sample_metadata))),
        )

        metadata = custom_fields_resource.get_metadata(team_id=TEAM_ID)

        assert metadata.data_transformation_steps_limit == 10
        assert metadata.field_data_types == ["string.text.value", "float.number.value"]
        assert metadata.functions.items[0].name == "upper_case"

    def test_get_metadata_passes_correct_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_metadata: MetadataOutputData,
        meta: Meta,
    ) -> None:
        """Test that get_metadata() passes only the team id to the generated client."""
        mock_sync = MagicMock(return_value=_make_success_response(MetadataOutput(meta=meta, data=sample_metadata)))
        monkeypatch.setattr(module.fetch_metadata, "sync_detailed", mock_sync)

        custom_fields_resource.get_metadata(team_id=TEAM_ID)

        assert mock_sync.call_args.kwargs["team_id"] == TEAM_ID

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_get_metadata_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that get_metadata() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.fetch_metadata,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            custom_fields_resource.get_metadata(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    # --- create() ---

    def test_create_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that create() accepts the 201 status and unwraps the created field."""
        monkeypatch.setattr(
            module.create_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_created_response(SingleTransformationOutput(meta=meta, data=sample_field))),
        )

        field = custom_fields_resource.create(
            team_id=TEAM_ID,
            display_name="Platform (upper)",
            field_type="dim",
            data_type="string.text.value",
            definition=sample_definition,
        )

        assert field.id == FIELD_ID
        assert field.name == "cf_platform_upper"

    def test_create_builds_request_body(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that create() sends field_type plus every optional the caller supplied."""
        mock_sync = MagicMock(
            return_value=_make_created_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.create_transformation, "sync_detailed", mock_sync)

        custom_fields_resource.create(
            team_id=TEAM_ID,
            display_name="Platform (upper)",
            field_type="met",
            data_type="float.number.value",
            definition=sample_definition,
            description="Upper-cased platform",
            data_source=[CustomFieldCreateRequestDataSourceItem(data_source_id="GAWA", report_type="AD_PERFORMANCE")],
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        body = call_kwargs["body"]
        assert body.display_name == "Platform (upper)"
        assert body.field_type == "met"
        assert body.data_type == "float.number.value"
        assert body.definition == sample_definition
        assert body.description == "Upper-cased platform"
        assert body.data_source[0].data_source_id == "GAWA"
        assert body.to_dict()["field_type"] == "met"

    def test_create_omits_unsupplied_optionals(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that create() leaves description and data_source UNSET when not supplied."""
        mock_sync = MagicMock(
            return_value=_make_created_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.create_transformation, "sync_detailed", mock_sync)

        custom_fields_resource.create(
            team_id=TEAM_ID,
            display_name="Platform (upper)",
            field_type="dim",
            data_type="string.text.value",
            definition=sample_definition,
        )

        body = mock_sync.call_args.kwargs["body"]
        assert body.description is UNSET
        assert body.data_source is UNSET
        assert "description" not in body.to_dict()
        assert "data_source" not in body.to_dict()

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_create_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that create() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.create_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            custom_fields_resource.create(
                team_id=TEAM_ID,
                display_name="Platform (upper)",
                field_type="dim",
                data_type="string.text.value",
                definition=sample_definition,
            )

        assert exc_info.value.status_code == int(status)

    def test_create_rejected_definition_is_400_not_422(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
    ) -> None:
        """Test that a rejected definition surfaces as a 400 validation error with definition context."""
        monkeypatch.setattr(
            module.create_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "unknown function")),
        )

        with pytest.raises(SupermetricsValidationError) as exc_info:
            custom_fields_resource.create(
                team_id=TEAM_ID,
                display_name="Platform (upper)",
                field_type="dim",
                data_type="string.text.value",
                definition=sample_definition,
            )

        assert exc_info.value.status_code == 400
        assert "Invalid custom field definition" in str(exc_info.value)

    # --- update() ---

    def test_update_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that update() unwraps the 200 response into the updated field."""
        monkeypatch.setattr(
            module.update_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))),
        )

        field = custom_fields_resource.update(
            team_id=TEAM_ID,
            custom_field_id=FIELD_ID,
            display_name="Platform (upper), revised",
            data_type="string.text.value",
            definition=sample_definition,
        )

        assert field.id == FIELD_ID

    def test_update_body_omits_field_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that update() never sends field_type, which upstream forbids changing."""
        mock_sync = MagicMock(
            return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.update_transformation, "sync_detailed", mock_sync)

        custom_fields_resource.update(
            team_id=TEAM_ID,
            custom_field_id=FIELD_ID,
            display_name="Platform (upper), revised",
            data_type="string.text.value",
            definition=sample_definition,
            description="Revised",
        )

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["custom_field_id"] == FIELD_ID
        body = call_kwargs["body"]
        assert body.display_name == "Platform (upper), revised"
        assert body.definition == sample_definition
        assert body.description == "Revised"
        assert not hasattr(body, "field_type")
        assert "field_type" not in body.to_dict()

    def test_update_omits_unsupplied_description(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that update() leaves description UNSET when the caller did not supply one."""
        mock_sync = MagicMock(
            return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.update_transformation, "sync_detailed", mock_sync)

        custom_fields_resource.update(
            team_id=TEAM_ID,
            custom_field_id=FIELD_ID,
            display_name="Platform (upper), revised",
            data_type="string.text.value",
            definition=sample_definition,
        )

        body = mock_sync.call_args.kwargs["body"]
        assert body.description is UNSET
        assert "description" not in body.to_dict()

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_update_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that update() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.update_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            custom_fields_resource.update(
                team_id=TEAM_ID,
                custom_field_id=FIELD_ID,
                display_name="Platform (upper), revised",
                data_type="string.text.value",
                definition=sample_definition,
            )

        assert exc_info.value.status_code == int(status)

    # --- delete() ---

    def test_delete_success(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that delete() accepts the 204 status and returns None."""
        mock_sync = MagicMock(return_value=_make_no_content_response())
        monkeypatch.setattr(module.delete_transformation, "sync_detailed", mock_sync)

        assert custom_fields_resource.delete(team_id=TEAM_ID, custom_field_id=FIELD_ID) is None

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["custom_field_id"] == FIELD_ID

    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    def test_delete_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that delete() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.delete_transformation,
            "sync_detailed",
            MagicMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            custom_fields_resource.delete(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        assert exc_info.value.status_code == int(status)

    def test_delete_network_error(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsResource
    ) -> None:
        """Test that delete() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/custom-fields/{FIELD_ID}"
        monkeypatch.setattr(
            module.delete_transformation,
            "sync_detailed",
            MagicMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            custom_fields_resource.delete(team_id=TEAM_ID, custom_field_id=FIELD_ID)


class TestCustomFieldsAsyncResource:
    """Test suite for CustomFieldsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def custom_fields_resource(self, mock_client: MagicMock) -> CustomFieldsAsyncResource:
        """Create a CustomFieldsAsyncResource instance with mock client."""
        return CustomFieldsAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_field(self) -> TeamTransformationOutput:
        """Create a sample persisted custom field for testing."""
        return _sample_field()

    @pytest.fixture
    def sample_metadata(self) -> MetadataOutputData:
        """Create sample custom field metadata for testing."""
        return _sample_metadata()

    @pytest.fixture
    def sample_definition(self) -> list[ConditionStep | FunctionStep | LookupStep]:
        """Create a sample request-shaped definition: a bare list of steps."""
        return [_function_step(), _lookup_step()]

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
    ) -> None:
        """Test that async list() unwraps data.items and preserves the discriminated step kinds."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "asyncio_detailed",
            AsyncMock(
                return_value=_make_success_response(
                    _paginated(PaginatedTransformationsOutputData(items=[sample_field]))
                )
            ),
        )

        fields = await custom_fields_resource.list(team_id=TEAM_ID)

        assert len(fields) == 1
        assert fields[0].id == FIELD_ID
        assert [type(step) for step in fields[0].definition.items] == [FunctionStep, LookupStep, ConditionStep]

    @pytest.mark.asyncio
    async def test_list_passes_supplied_query_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
    ) -> None:
        """Test that async list() forwards every filter the caller supplied."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(_paginated(PaginatedTransformationsOutputData(items=[sample_field])))
        )
        monkeypatch.setattr(module.fetch_transformation_list, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.list(
            team_id=TEAM_ID,
            data_source_id="GAWA",
            display_name="Platform (upper)",
            page=3,
            limit=50,
            include_total_count=True,
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["data_source_id"] == "GAWA"
        assert call_kwargs["display_name"] == "Platform (upper)"
        assert call_kwargs["page"] == 3
        assert call_kwargs["limit"] == 50
        assert call_kwargs["include_total_count"] is True

    @pytest.mark.asyncio
    async def test_list_omits_unsupplied_query_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
    ) -> None:
        """Test that async list() passes UNSET for unsupplied filters, so limit does not default to 25."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(_paginated(PaginatedTransformationsOutputData(items=[sample_field])))
        )
        monkeypatch.setattr(module.fetch_transformation_list, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.list(team_id=TEAM_ID)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["data_source_id"] is UNSET
        assert call_kwargs["display_name"] is UNSET
        assert call_kwargs["page"] is UNSET
        assert call_kwargs["limit"] is UNSET
        assert call_kwargs["include_total_count"] is UNSET

    @pytest.mark.asyncio
    async def test_list_returns_empty_when_data_unset(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsAsyncResource
    ) -> None:
        """Test that an absent data object degrades to an empty list on the async path too."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_paginated(UNSET))),
        )

        assert await custom_fields_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.asyncio
    async def test_list_returns_empty_when_items_unset(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsAsyncResource
    ) -> None:
        """Test that a data object with no items degrades to an empty list on the async path too."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(_paginated(PaginatedTransformationsOutputData()))),
        )

        assert await custom_fields_resource.list(team_id=TEAM_ID) == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_list_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async list() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await custom_fields_resource.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    @pytest.mark.asyncio
    async def test_list_network_error(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsAsyncResource
    ) -> None:
        """Test that async list() raises NetworkError on httpx.RequestError."""
        mock_request = Mock()
        mock_request.url = f"https://api.supermetrics.com/v1/teams/{TEAM_ID}/custom-fields"
        monkeypatch.setattr(
            module.fetch_transformation_list,
            "asyncio_detailed",
            AsyncMock(side_effect=httpx.ConnectError("Connection refused", request=mock_request)),
        )

        with pytest.raises(NetworkError):
            await custom_fields_resource.list(team_id=TEAM_ID)

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        meta: Meta,
    ) -> None:
        """Test that async get() unwraps the .data envelope into a TeamTransformationOutput."""
        monkeypatch.setattr(
            module.fetch_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))),
        )

        field = await custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        assert field.id == FIELD_ID
        assert field.modified_time_utc == datetime.datetime(2026, 4, 6, 10, 59, 4, tzinfo=datetime.UTC)

    @pytest.mark.asyncio
    async def test_get_passes_correct_params(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        meta: Meta,
    ) -> None:
        """Test that async get() passes the team and custom field ids to the generated client."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.fetch_transformation, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["custom_field_id"] == FIELD_ID

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_get_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async get() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.fetch_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await custom_fields_resource.get(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        assert exc_info.value.status_code == int(status)

    # --- get_metadata() ---

    @pytest.mark.asyncio
    async def test_get_metadata_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_metadata: MetadataOutputData,
        meta: Meta,
    ) -> None:
        """Test that async get_metadata() unwraps .data into a MetadataOutputData."""
        mock_asyncio = AsyncMock(return_value=_make_success_response(MetadataOutput(meta=meta, data=sample_metadata)))
        monkeypatch.setattr(module.fetch_metadata, "asyncio_detailed", mock_asyncio)

        metadata = await custom_fields_resource.get_metadata(team_id=TEAM_ID)

        assert metadata.data_transformation_steps_limit == 10
        assert metadata.functions.items[0].name == "upper_case"
        assert mock_asyncio.call_args.kwargs["team_id"] == TEAM_ID

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_get_metadata_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async get_metadata() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.fetch_metadata,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await custom_fields_resource.get_metadata(team_id=TEAM_ID)

        assert exc_info.value.status_code == int(status)

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that async create() accepts the 201 status and unwraps the created field."""
        monkeypatch.setattr(
            module.create_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_created_response(SingleTransformationOutput(meta=meta, data=sample_field))),
        )

        field = await custom_fields_resource.create(
            team_id=TEAM_ID,
            display_name="Platform (upper)",
            field_type="dim",
            data_type="string.text.value",
            definition=sample_definition,
        )

        assert field.id == FIELD_ID

    @pytest.mark.asyncio
    async def test_create_builds_request_body(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that async create() sends field_type plus every optional the caller supplied."""
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.create_transformation, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.create(
            team_id=TEAM_ID,
            display_name="Platform (upper)",
            field_type="met",
            data_type="float.number.value",
            definition=sample_definition,
            description="Upper-cased platform",
            data_source=[CustomFieldCreateRequestDataSourceItem(data_source_id="GAWA")],
        )

        body = mock_asyncio.call_args.kwargs["body"]
        assert body.field_type == "met"
        assert body.definition == sample_definition
        assert body.description == "Upper-cased platform"
        assert body.data_source[0].data_source_id == "GAWA"

    @pytest.mark.asyncio
    async def test_create_omits_unsupplied_optionals(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that async create() leaves description and data_source UNSET when not supplied."""
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.create_transformation, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.create(
            team_id=TEAM_ID,
            display_name="Platform (upper)",
            field_type="dim",
            data_type="string.text.value",
            definition=sample_definition,
        )

        body = mock_asyncio.call_args.kwargs["body"]
        assert body.description is UNSET
        assert body.data_source is UNSET

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_create_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async create() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.create_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await custom_fields_resource.create(
                team_id=TEAM_ID,
                display_name="Platform (upper)",
                field_type="dim",
                data_type="string.text.value",
                definition=sample_definition,
            )

        assert exc_info.value.status_code == int(status)

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that async update() unwraps the 200 response into the updated field."""
        monkeypatch.setattr(
            module.update_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))),
        )

        field = await custom_fields_resource.update(
            team_id=TEAM_ID,
            custom_field_id=FIELD_ID,
            display_name="Platform (upper), revised",
            data_type="string.text.value",
            definition=sample_definition,
        )

        assert field.id == FIELD_ID

    @pytest.mark.asyncio
    async def test_update_body_omits_field_type(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that async update() never sends field_type, which upstream forbids changing."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.update_transformation, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.update(
            team_id=TEAM_ID,
            custom_field_id=FIELD_ID,
            display_name="Platform (upper), revised",
            data_type="string.text.value",
            definition=sample_definition,
            description="Revised",
        )

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["custom_field_id"] == FIELD_ID
        body = call_kwargs["body"]
        assert not hasattr(body, "field_type")
        assert "field_type" not in body.to_dict()
        assert body.description == "Revised"

    @pytest.mark.asyncio
    async def test_update_omits_unsupplied_description(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_field: TeamTransformationOutput,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        meta: Meta,
    ) -> None:
        """Test that async update() leaves description UNSET when the caller did not supply one."""
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(SingleTransformationOutput(meta=meta, data=sample_field))
        )
        monkeypatch.setattr(module.update_transformation, "asyncio_detailed", mock_asyncio)

        await custom_fields_resource.update(
            team_id=TEAM_ID,
            custom_field_id=FIELD_ID,
            display_name="Platform (upper), revised",
            data_type="string.text.value",
            definition=sample_definition,
        )

        assert mock_asyncio.call_args.kwargs["body"].description is UNSET

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_update_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        sample_definition: list[ConditionStep | FunctionStep | LookupStep],
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async update() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.update_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await custom_fields_resource.update(
                team_id=TEAM_ID,
                custom_field_id=FIELD_ID,
                display_name="Platform (upper), revised",
                data_type="string.text.value",
                definition=sample_definition,
            )

        assert exc_info.value.status_code == int(status)

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_success(
        self, monkeypatch: pytest.MonkeyPatch, custom_fields_resource: CustomFieldsAsyncResource
    ) -> None:
        """Test that async delete() accepts the 204 status and returns None."""
        mock_asyncio = AsyncMock(return_value=_make_no_content_response())
        monkeypatch.setattr(module.delete_transformation, "asyncio_detailed", mock_asyncio)

        assert await custom_fields_resource.delete(team_id=TEAM_ID, custom_field_id=FIELD_ID) is None

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == TEAM_ID
        assert call_kwargs["custom_field_id"] == FIELD_ID

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), ERROR_CASES)
    async def test_delete_error_mapping(
        self,
        monkeypatch: pytest.MonkeyPatch,
        custom_fields_resource: CustomFieldsAsyncResource,
        status: HTTPStatus,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Test that async delete() maps each documented failure status to its SDK exception."""
        monkeypatch.setattr(
            module.delete_transformation,
            "asyncio_detailed",
            AsyncMock(return_value=_make_error_response(status, code, "boom")),
        )

        with pytest.raises(expected) as exc_info:
            await custom_fields_resource.delete(team_id=TEAM_ID, custom_field_id=FIELD_ID)

        assert exc_info.value.status_code == int(status)
