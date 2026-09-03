"""Unit tests for TableGroupsResource and TableGroupsAsyncResource."""

from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock

import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.edit_table_group_body import EditTableGroupBody
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.export_table_group_response_200 import (
    ExportTableGroupResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.field_definition import FieldDefinition
from supermetrics._generated.supermetrics_api_client.models.import_table_group_body import ImportTableGroupBody
from supermetrics._generated.supermetrics_api_client.models.list_table_groups_response_200 import (
    ListTableGroupsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.models.table_definition import TableDefinition
from supermetrics._generated.supermetrics_api_client.models.table_group import TableGroup
from supermetrics._generated.supermetrics_api_client.models.table_group_export import TableGroupExport
from supermetrics._generated.supermetrics_api_client.models.table_group_import import TableGroupImport
from supermetrics._generated.supermetrics_api_client.models.table_group_write_response import TableGroupWriteResponse
from supermetrics._generated.supermetrics_api_client.types import Response
from supermetrics.exceptions import APIError, AuthenticationError, SupermetricsNotFoundError
from supermetrics.resources.table_groups import TableGroupsAsyncResource, TableGroupsResource


def _make_success_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=parsed)


def _make_created_response(parsed: object) -> Response:
    return Response(status_code=HTTPStatus.CREATED, content=b"", headers={}, parsed=parsed)


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


def _sample_write_response() -> TableGroupWriteResponse:
    return TableGroupWriteResponse(group_id="tg_100", group_name="Google Ads Standard")


class TestTableGroupsResource:
    """Test suite for TableGroupsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> TableGroupsResource:
        return TableGroupsResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_groups(self) -> list[TableGroup]:
        return [
            TableGroup(group_id="tg_100", schema_id=354, name="Google Ads Standard"),
            TableGroup(group_id="tg_200", schema_id=68, name="Pinterest Ads Standard"),
        ]

    @pytest.fixture
    def sample_export(self) -> ExportTableGroupResponse200:
        return ExportTableGroupResponse200(
            version=1,
            group=TableGroupExport(group_id="tg_100", group_name="Google Ads Standard", ds_id="AW", table_prefix="AW"),
            tables=[
                TableDefinition(table_name="CAMPAIGNS", table_partition="date", fields=["campaign_id", "date"]),
            ],
            fields=[
                FieldDefinition(field_id="campaign_id", target_name="campaign_id"),
                FieldDefinition(field_id="date", target_name="report_date"),
            ],
        )

    @pytest.fixture
    def sample_import_body(self) -> ImportTableGroupBody:
        return ImportTableGroupBody(
            version=1,
            group=TableGroupImport(group_name="Test Group", ds_id="AW", table_prefix="TST"),
            tables=[TableDefinition(table_name="CAMPAIGNS", fields=["campaign_id", "date"])],
            fields=[FieldDefinition(field_id="campaign_id", target_name="campaign_id")],
        )

    @pytest.fixture
    def sample_edit_body(self) -> EditTableGroupBody:
        return EditTableGroupBody(
            version=1,
            group=TableGroupImport(group_name="Updated Group", ds_id="AW", table_prefix="TST"),
            tables=[TableDefinition(table_name="CAMPAIGNS", fields=["campaign_id", "date", "clicks"])],
            fields=[
                FieldDefinition(field_id="campaign_id", target_name="campaign_id"),
                FieldDefinition(field_id="clicks", target_name="clicks"),
            ],
        )

    # --- list() ---

    def test_list_success(
        self,
        resource: TableGroupsResource,
        sample_groups: list[TableGroup],
        meta: Meta,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.sync_detailed
        module.list_table_groups.sync_detailed = MagicMock(
            return_value=_make_success_response(ListTableGroupsResponse200(meta=meta, data=sample_groups))
        )
        try:
            groups = resource.list()
            assert len(groups) == 2
            assert groups[0].group_id == "tg_100"
            assert groups[0].schema_id == 354
            assert groups[0].name == "Google Ads Standard"
            assert groups[1].group_id == "tg_200"
        finally:
            module.list_table_groups.sync_detailed = original

    def test_list_passes_correct_params(
        self,
        resource: TableGroupsResource,
        sample_groups: list[TableGroup],
        meta: Meta,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(ListTableGroupsResponse200(meta=meta, data=sample_groups))
        )
        module.list_table_groups.sync_detailed = mock_sync
        try:
            resource.list()
            call_kwargs = mock_sync.call_args.kwargs
            assert set(call_kwargs) == {"client"}
        finally:
            module.list_table_groups.sync_detailed = original

    def test_list_auth_error_on_401(self, resource: TableGroupsResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.sync_detailed
        module.list_table_groups.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError) as exc_info:
                resource.list()
            assert exc_info.value.status_code == 401
        finally:
            module.list_table_groups.sync_detailed = original

    def test_list_api_error_on_500(self, resource: TableGroupsResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.sync_detailed
        module.list_table_groups.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )
        try:
            with pytest.raises(APIError) as exc_info:
                resource.list()
            assert exc_info.value.status_code == 500
        finally:
            module.list_table_groups.sync_detailed = original

    # --- export() ---

    def test_export_success(
        self,
        resource: TableGroupsResource,
        sample_export: ExportTableGroupResponse200,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.sync_detailed
        module.export_table_group.sync_detailed = MagicMock(return_value=_make_success_response(sample_export))
        try:
            result = resource.export(group_id="tg_100", version=1)
            assert result.version == 1
            assert result.group.group_name == "Google Ads Standard"
            assert result.group.ds_id == "AW"
            assert len(result.tables) == 1
            assert result.tables[0].table_name == "CAMPAIGNS"
            assert len(result.fields) == 2
        finally:
            module.export_table_group.sync_detailed = original

    def test_export_passes_correct_params(
        self,
        resource: TableGroupsResource,
        sample_export: ExportTableGroupResponse200,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_export))
        module.export_table_group.sync_detailed = mock_sync
        try:
            resource.export(group_id="tg_100", version=1)
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["group_id"] == "tg_100"
            assert call_kwargs["version"] == 1
        finally:
            module.export_table_group.sync_detailed = original

    def test_export_auth_error_on_401(self, resource: TableGroupsResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.sync_detailed
        module.export_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                resource.export(group_id="tg_100", version=1)
        finally:
            module.export_table_group.sync_detailed = original

    def test_export_not_found_on_404(self, resource: TableGroupsResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.sync_detailed
        module.export_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Table group not found")
        )
        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                resource.export(group_id="tg_999", version=1)
            assert exc_info.value.status_code == 404
        finally:
            module.export_table_group.sync_detailed = original

    # --- import_() ---

    def test_import_success(
        self,
        resource: TableGroupsResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.sync_detailed
        module.import_table_group.sync_detailed = MagicMock(
            return_value=_make_created_response(_sample_write_response())
        )
        try:
            created = resource.import_(body=sample_import_body)
            assert created.group_id == "tg_100"
            assert created.group_name == "Google Ads Standard"
        finally:
            module.import_table_group.sync_detailed = original

    def test_import_passes_correct_params(
        self,
        resource: TableGroupsResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.sync_detailed
        mock_sync = MagicMock(return_value=_make_created_response(_sample_write_response()))
        module.import_table_group.sync_detailed = mock_sync
        try:
            resource.import_(body=sample_import_body)
            call_kwargs = mock_sync.call_args.kwargs
            body = call_kwargs["body"]
            assert body.version == 1
            assert body.group.group_name == "Test Group"
            assert body.group.ds_id == "AW"
            assert len(body.tables) == 1
        finally:
            module.import_table_group.sync_detailed = original

    def test_import_auth_error_on_401(
        self,
        resource: TableGroupsResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.sync_detailed
        module.import_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                resource.import_(body=sample_import_body)
        finally:
            module.import_table_group.sync_detailed = original

    def test_import_not_found_on_404(
        self,
        resource: TableGroupsResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.sync_detailed
        module.import_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Not found")
        )
        try:
            with pytest.raises(SupermetricsNotFoundError):
                resource.import_(body=sample_import_body)
        finally:
            module.import_table_group.sync_detailed = original

    def test_import_api_error_on_409_conflict(
        self,
        resource: TableGroupsResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.sync_detailed
        module.import_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.CONFLICT, "TABLE_GROUP_NAME_CONFLICT", "Name already exists")
        )
        try:
            with pytest.raises(APIError) as exc_info:
                resource.import_(body=sample_import_body)
            assert exc_info.value.status_code == 409
        finally:
            module.import_table_group.sync_detailed = original

    # --- edit() ---

    def test_edit_success(
        self,
        resource: TableGroupsResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.sync_detailed
        module.edit_table_group.sync_detailed = MagicMock(return_value=_make_success_response(_sample_write_response()))
        try:
            updated = resource.edit(group_id="tg_100", body=sample_edit_body)
            assert updated.group_id == "tg_100"
            assert updated.group_name == "Google Ads Standard"
        finally:
            module.edit_table_group.sync_detailed = original

    def test_edit_passes_correct_params(
        self,
        resource: TableGroupsResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(_sample_write_response()))
        module.edit_table_group.sync_detailed = mock_sync
        try:
            resource.edit(group_id="tg_100", body=sample_edit_body)
            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["group_id"] == "tg_100"
            assert "version" not in call_kwargs
            body = call_kwargs["body"]
            assert body.version == 1
            assert body.group.group_name == "Updated Group"
            assert len(body.tables) == 1
        finally:
            module.edit_table_group.sync_detailed = original

    def test_edit_auth_error_on_401(
        self,
        resource: TableGroupsResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.sync_detailed
        module.edit_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                resource.edit(group_id="tg_100", body=sample_edit_body)
        finally:
            module.edit_table_group.sync_detailed = original

    def test_edit_not_found_on_404(
        self,
        resource: TableGroupsResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.sync_detailed
        module.edit_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Table group not found")
        )
        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                resource.edit(group_id="tg_999", body=sample_edit_body)
            assert exc_info.value.status_code == 404
        finally:
            module.edit_table_group.sync_detailed = original

    def test_edit_api_error_on_500(
        self,
        resource: TableGroupsResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.sync_detailed
        module.edit_table_group.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )
        try:
            with pytest.raises(APIError) as exc_info:
                resource.edit(group_id="tg_100", body=sample_edit_body)
            assert exc_info.value.status_code == 500
        finally:
            module.edit_table_group.sync_detailed = original


class TestTableGroupsAsyncResource:
    """Test suite for TableGroupsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> TableGroupsAsyncResource:
        return TableGroupsAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def sample_groups(self) -> list[TableGroup]:
        return [
            TableGroup(group_id="tg_100", schema_id=354, name="Google Ads Standard"),
            TableGroup(group_id="tg_200", schema_id=68, name="Pinterest Ads Standard"),
        ]

    @pytest.fixture
    def sample_export(self) -> ExportTableGroupResponse200:
        return ExportTableGroupResponse200(
            version=1,
            group=TableGroupExport(group_id="tg_100", group_name="Google Ads Standard", ds_id="AW", table_prefix="AW"),
            tables=[
                TableDefinition(table_name="CAMPAIGNS", table_partition="date", fields=["campaign_id", "date"]),
            ],
            fields=[
                FieldDefinition(field_id="campaign_id", target_name="campaign_id"),
                FieldDefinition(field_id="date", target_name="report_date"),
            ],
        )

    @pytest.fixture
    def sample_import_body(self) -> ImportTableGroupBody:
        return ImportTableGroupBody(
            version=1,
            group=TableGroupImport(group_name="Test Group", ds_id="AW", table_prefix="TST"),
            tables=[TableDefinition(table_name="CAMPAIGNS", fields=["campaign_id", "date"])],
            fields=[FieldDefinition(field_id="campaign_id", target_name="campaign_id")],
        )

    @pytest.fixture
    def sample_edit_body(self) -> EditTableGroupBody:
        return EditTableGroupBody(
            version=1,
            group=TableGroupImport(group_name="Updated Group", ds_id="AW", table_prefix="TST"),
            tables=[TableDefinition(table_name="CAMPAIGNS", fields=["campaign_id", "date", "clicks"])],
            fields=[
                FieldDefinition(field_id="campaign_id", target_name="campaign_id"),
                FieldDefinition(field_id="clicks", target_name="clicks"),
            ],
        )

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(
        self,
        resource: TableGroupsAsyncResource,
        sample_groups: list[TableGroup],
        meta: Meta,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.asyncio_detailed
        module.list_table_groups.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(ListTableGroupsResponse200(meta=meta, data=sample_groups))
        )
        try:
            groups = await resource.list()
            assert len(groups) == 2
            assert groups[0].group_id == "tg_100"
            assert groups[1].group_id == "tg_200"
        finally:
            module.list_table_groups.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_passes_correct_params(
        self,
        resource: TableGroupsAsyncResource,
        sample_groups: list[TableGroup],
        meta: Meta,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.asyncio_detailed
        mock_async = AsyncMock(
            return_value=_make_success_response(ListTableGroupsResponse200(meta=meta, data=sample_groups))
        )
        module.list_table_groups.asyncio_detailed = mock_async
        try:
            await resource.list()
            call_kwargs = mock_async.call_args.kwargs
            assert set(call_kwargs) == {"client"}
        finally:
            module.list_table_groups.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_auth_error_on_401(self, resource: TableGroupsAsyncResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.asyncio_detailed
        module.list_table_groups.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                await resource.list()
        finally:
            module.list_table_groups.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_api_error_on_500(self, resource: TableGroupsAsyncResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.list_table_groups.asyncio_detailed
        module.list_table_groups.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )
        try:
            with pytest.raises(APIError) as exc_info:
                await resource.list()
            assert exc_info.value.status_code == 500
        finally:
            module.list_table_groups.asyncio_detailed = original

    # --- export() ---

    @pytest.mark.asyncio
    async def test_export_success(
        self,
        resource: TableGroupsAsyncResource,
        sample_export: ExportTableGroupResponse200,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.asyncio_detailed
        module.export_table_group.asyncio_detailed = AsyncMock(return_value=_make_success_response(sample_export))
        try:
            result = await resource.export(group_id="tg_100", version=1)
            assert result.version == 1
            assert result.group.group_name == "Google Ads Standard"
            assert len(result.tables) == 1
            assert len(result.fields) == 2
        finally:
            module.export_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_export_passes_correct_params(
        self,
        resource: TableGroupsAsyncResource,
        sample_export: ExportTableGroupResponse200,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.asyncio_detailed
        mock_async = AsyncMock(return_value=_make_success_response(sample_export))
        module.export_table_group.asyncio_detailed = mock_async
        try:
            await resource.export(group_id="tg_100", version=1)
            call_kwargs = mock_async.call_args.kwargs
            assert call_kwargs["group_id"] == "tg_100"
            assert call_kwargs["version"] == 1
        finally:
            module.export_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_export_auth_error_on_401(self, resource: TableGroupsAsyncResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.asyncio_detailed
        module.export_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                await resource.export(group_id="tg_100", version=1)
        finally:
            module.export_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_export_not_found_on_404(self, resource: TableGroupsAsyncResource) -> None:
        import supermetrics.resources.table_groups as module

        original = module.export_table_group.asyncio_detailed
        module.export_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Table group not found")
        )
        try:
            with pytest.raises(SupermetricsNotFoundError):
                await resource.export(group_id="tg_999", version=1)
        finally:
            module.export_table_group.asyncio_detailed = original

    # --- import_() ---

    @pytest.mark.asyncio
    async def test_import_success(
        self,
        resource: TableGroupsAsyncResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.asyncio_detailed
        module.import_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_created_response(_sample_write_response())
        )
        try:
            created = await resource.import_(body=sample_import_body)
            assert created.group_id == "tg_100"
            assert created.group_name == "Google Ads Standard"
        finally:
            module.import_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_import_passes_correct_params(
        self,
        resource: TableGroupsAsyncResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.asyncio_detailed
        mock_async = AsyncMock(return_value=_make_created_response(_sample_write_response()))
        module.import_table_group.asyncio_detailed = mock_async
        try:
            await resource.import_(body=sample_import_body)
            call_kwargs = mock_async.call_args.kwargs
            body = call_kwargs["body"]
            assert body.version == 1
            assert body.group.group_name == "Test Group"
        finally:
            module.import_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_import_auth_error_on_401(
        self,
        resource: TableGroupsAsyncResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.asyncio_detailed
        module.import_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                await resource.import_(body=sample_import_body)
        finally:
            module.import_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_import_api_error_on_409_conflict(
        self,
        resource: TableGroupsAsyncResource,
        sample_import_body: ImportTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.import_table_group.asyncio_detailed
        module.import_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.CONFLICT, "TABLE_GROUP_NAME_CONFLICT", "Name already exists")
        )
        try:
            with pytest.raises(APIError) as exc_info:
                await resource.import_(body=sample_import_body)
            assert exc_info.value.status_code == 409
        finally:
            module.import_table_group.asyncio_detailed = original

    # --- edit() ---

    @pytest.mark.asyncio
    async def test_edit_success(
        self,
        resource: TableGroupsAsyncResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.asyncio_detailed
        module.edit_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(_sample_write_response())
        )
        try:
            updated = await resource.edit(group_id="tg_100", body=sample_edit_body)
            assert updated.group_id == "tg_100"
        finally:
            module.edit_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_edit_passes_correct_params(
        self,
        resource: TableGroupsAsyncResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.asyncio_detailed
        mock_async = AsyncMock(return_value=_make_success_response(_sample_write_response()))
        module.edit_table_group.asyncio_detailed = mock_async
        try:
            await resource.edit(group_id="tg_100", body=sample_edit_body)
            call_kwargs = mock_async.call_args.kwargs
            assert call_kwargs["group_id"] == "tg_100"
            assert "version" not in call_kwargs
            assert call_kwargs["body"].version == 1
            assert call_kwargs["body"].group.group_name == "Updated Group"
        finally:
            module.edit_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_edit_auth_error_on_401(
        self,
        resource: TableGroupsAsyncResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.asyncio_detailed
        module.edit_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )
        try:
            with pytest.raises(AuthenticationError):
                await resource.edit(group_id="tg_100", body=sample_edit_body)
        finally:
            module.edit_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_edit_not_found_on_404(
        self,
        resource: TableGroupsAsyncResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.asyncio_detailed
        module.edit_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Table group not found")
        )
        try:
            with pytest.raises(SupermetricsNotFoundError):
                await resource.edit(group_id="tg_999", body=sample_edit_body)
        finally:
            module.edit_table_group.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_edit_api_error_on_500(
        self,
        resource: TableGroupsAsyncResource,
        sample_edit_body: EditTableGroupBody,
    ) -> None:
        import supermetrics.resources.table_groups as module

        original = module.edit_table_group.asyncio_detailed
        module.edit_table_group.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )
        try:
            with pytest.raises(APIError) as exc_info:
                await resource.edit(group_id="tg_100", body=sample_edit_body)
            assert exc_info.value.status_code == 500
        finally:
            module.edit_table_group.asyncio_detailed = original
