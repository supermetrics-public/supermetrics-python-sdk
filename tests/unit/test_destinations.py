"""Unit tests for DestinationsResource and DestinationsAsyncResource."""

from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.batch_update_destinations_body_updates_item import (
    BatchUpdateDestinationsBodyUpdatesItem as _BatchUpdateItem,
)
from supermetrics._generated.supermetrics_api_client.models.batch_update_destinations_response_200 import (
    BatchUpdateDestinationsResponse200 as _BatchResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.batch_update_destinations_response_200_data import (
    BatchUpdateDestinationsResponse200Data as _BatchData,
)
from supermetrics._generated.supermetrics_api_client.models.batch_update_destinations_response_200_data_results_item import (  # noqa: E501
    BatchUpdateDestinationsResponse200DataResultsItem as _BatchResultItem,
)
from supermetrics._generated.supermetrics_api_client.models.destination_info import DestinationInfo
from supermetrics._generated.supermetrics_api_client.models.destination_list_item import DestinationListItem
from supermetrics._generated.supermetrics_api_client.models.destination_list_response import DestinationListResponse
from supermetrics._generated.supermetrics_api_client.models.destination_response import DestinationResponse
from supermetrics._generated.supermetrics_api_client.models.destination_type import DestinationType
from supermetrics._generated.supermetrics_api_client.models.destination_usage import DestinationUsage
from supermetrics._generated.supermetrics_api_client.models.destination_usage_response import DestinationUsageResponse
from supermetrics._generated.supermetrics_api_client.models.destination_usage_transfers_item import (
    DestinationUsageTransfersItem,
)
from supermetrics._generated.supermetrics_api_client.models.error import Error
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.models.response_meta import ResponseMeta
from supermetrics._generated.supermetrics_api_client.models.setup_setting import SetupSetting

# ``TestConnectionRequest``/``TestConnectionResponse``/``TestConnectionResult`` all start with
# ``Test``, so importing them under their real names makes pytest try to collect them as test
# classes (PytestCollectionWarning, and their ``__init__`` makes them uncollectable). Alias them.
from supermetrics._generated.supermetrics_api_client.models.test_connection_response import (
    TestConnectionResponse as ConnectionTestResponse,
)
from supermetrics._generated.supermetrics_api_client.models.test_connection_result import (
    TestConnectionResult as ConnectionTestResult,
)
from supermetrics._generated.supermetrics_api_client.types import UNSET, Response
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, SupermetricsNotFoundError
from supermetrics.resources.destinations import DestinationsAsyncResource, DestinationsResource

# Destination payloads carry ``private_key``, ``passphrase`` and ``new_password``, and a failing
# assertion prints whole request bodies. Every credential-shaped value in this module is therefore
# obviously fake, never something that could be mistaken for a redacted real secret.
SNOWFLAKE_FIELDS: dict[str, Any] = {
    "hostname": "example.eu-north-1.snowflakecomputing.test",
    "warehouse": "DEMO_WH",
    "database_name": "TEST_DB",
    "schema": "PUBLIC",
    "role": "ACCOUNTADMIN",
    "username": "not-a-real-user",
    "private_key": "not-a-real-key",
    "passphrase": "not-a-real-passphrase",
}

BIGQUERY_FIELDS: dict[str, Any] = {
    "project_id": "not-a-real-project",
    "dataset_id": "not_a_real_dataset",
    "service_account_key": "not-a-real-key",
}


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


class TestDestinationsResource:
    """Test suite for DestinationsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def destinations_resource(self, mock_client: MagicMock) -> DestinationsResource:
        """Create a DestinationsResource instance with mock client."""
        return DestinationsResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_0123456789ab")

    @pytest.fixture
    def destination_items(self) -> list[DestinationListItem]:
        """Create the compact items the collection endpoint returns."""
        return [
            DestinationListItem(id=8, display_name="Snowflake analytics", type_="DWH_SNOWFLAKE"),
            DestinationListItem(id=9, display_name="BigQuery warehouse", type_="DWH_BIGQUERY"),
        ]

    @pytest.fixture
    def sample_destination(self) -> DestinationInfo:
        """Create a sample destination, which the API describes as an editable form."""
        return DestinationInfo(
            display_name="Snowflake analytics",
            destination_type=DestinationType(
                type_="DWH_SNOWFLAKE",
                title="Snowflake",
                icon_url="https://cdn.example.test/snowflake.svg",
            ),
            edit_settings=[
                SetupSetting(id="warehouse", input_type="text", is_required=True, label="Warehouse", value="DEMO_WH"),
                SetupSetting(id="role", input_type="text", is_required=False, label="Role", value="ACCOUNTADMIN"),
            ],
            id=8,
        )

    @pytest.fixture
    def sample_usage(self) -> DestinationUsage:
        """Create a sample usage report naming the transfers that still write to a destination."""
        return DestinationUsage(
            is_used=True,
            transfers=[DestinationUsageTransfersItem(transfer_id=36091, transfer_name="AW enhanced")],
        )

    # --- list() ---

    def test_list_success(
        self,
        destinations_resource: DestinationsResource,
        destination_items: list[DestinationListItem],
        meta: Meta,
    ) -> None:
        """Test successful destination listing, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.sync_detailed
        module.list_destinations.sync_detailed = MagicMock(
            return_value=_make_success_response(DestinationListResponse(meta=meta, data=destination_items))
        )

        try:
            destinations = destinations_resource.list(team_id=12345)

            assert len(destinations) == 2
            assert destinations[0].id == 8
            assert destinations[0].display_name == "Snowflake analytics"
            assert destinations[0].type_ == "DWH_SNOWFLAKE"
            assert destinations[1].id == 9
            assert destinations[1].type_ == "DWH_BIGQUERY"
        finally:
            module.list_destinations.sync_detailed = original

    def test_list_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        destination_items: list[DestinationListItem],
        meta: Meta,
    ) -> None:
        """Test that list() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(DestinationListResponse(meta=meta, data=destination_items))
        )
        module.list_destinations.sync_detailed = mock_sync

        try:
            destinations_resource.list(team_id=12345)

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            # The endpoint declares no query parameters, so nothing else may be sent.
            assert set(call_kwargs) == {"client", "team_id"}
        finally:
            module.list_destinations.sync_detailed = original

    def test_list_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that list() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.sync_detailed
        module.list_destinations.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.list(team_id=12345)

            assert exc_info.value.status_code == 401
            assert "Invalid or expired API key" in str(exc_info.value)
        finally:
            module.list_destinations.sync_detailed = original

    def test_list_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that list() surfaces an undocumented 404 as the not-found APIError."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.sync_detailed
        module.list_destinations.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Team not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.list(team_id=999)

            assert exc_info.value.status_code == 404
            assert isinstance(exc_info.value, APIError)
        finally:
            module.list_destinations.sync_detailed = original

    def test_list_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that list() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.sync_detailed
        module.list_destinations.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.list(team_id=12345)

            assert exc_info.value.status_code == 500
        finally:
            module.list_destinations.sync_detailed = original

    def test_list_network_error(self, destinations_resource: DestinationsResource) -> None:
        """Test that list() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.sync_detailed
        mock_request = Mock()
        mock_request.url = "https://dts-api.supermetrics.com/v1/teams/12345/destinations"
        module.list_destinations.sync_detailed = MagicMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        try:
            with pytest.raises(NetworkError):
                destinations_resource.list(team_id=12345)
        finally:
            module.list_destinations.sync_detailed = original

    # --- get() ---

    def test_get_success(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test successful destination retrieval, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.sync_detailed
        module.get_destination.sync_detailed = MagicMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            destination = destinations_resource.get(team_id=12345, destination_id=8)

            assert destination.id == 8
            assert destination.display_name == "Snowflake analytics"
            assert destination.destination_type.type_ == "DWH_SNOWFLAKE"
            assert [setting.id for setting in destination.edit_settings] == ["warehouse", "role"]
            assert destination.edit_settings[0].value == "DEMO_WH"
        finally:
            module.get_destination.sync_detailed = original

    def test_get_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that get() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.get_destination.sync_detailed = mock_sync

        try:
            destinations_resource.get(team_id=12345, destination_id=8)

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["destination_id"] == 8
        finally:
            module.get_destination.sync_detailed = original

    def test_get_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that get() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.sync_detailed
        module.get_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.get(team_id=12345, destination_id=8)

            assert exc_info.value.status_code == 401
        finally:
            module.get_destination.sync_detailed = original

    def test_get_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that get() raises the not-found APIError on 404 with destination context."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.sync_detailed
        module.get_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.get(team_id=12345, destination_id=999)

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.get_destination.sync_detailed = original

    def test_get_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that get() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.sync_detailed
        module.get_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.get(team_id=12345, destination_id=8)

            assert exc_info.value.status_code == 500
        finally:
            module.get_destination.sync_detailed = original

    # --- create() ---

    def test_create_success(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test successful destination creation, which the API answers with HTTP 201."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        module.create_destination.sync_detailed = MagicMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            created = destinations_resource.create(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            assert created.id == 8
            assert created.display_name == "Snowflake analytics"
            assert created.destination_type.type_ == "DWH_SNOWFLAKE"
        finally:
            module.create_destination.sync_detailed = original

    def test_create_treats_200_as_an_error(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that create() accepts only 201; a 200 is not the documented success status."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        module.create_destination.sync_detailed = MagicMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.create(
                    team_id=12345,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 200
        finally:
            module.create_destination.sync_detailed = original

    def test_create_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that create() passes the correct body to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.create_destination.sync_detailed = mock_sync

        try:
            destinations_resource.create(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
                auth_method="AUTH_METHOD_KEY_PAIR",
            )

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert body.display_name == "Snowflake analytics"
            assert body.auth_method == "AUTH_METHOD_KEY_PAIR"
            assert body.to_dict()["auth_method"] == "AUTH_METHOD_KEY_PAIR"
        finally:
            module.create_destination.sync_detailed = original

    def test_create_fields_round_trip(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that the plain fields dict survives the trip through the generated Fields model."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.create_destination.sync_detailed = mock_sync

        try:
            destinations_resource.create(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            body = mock_sync.call_args.kwargs["body"]
            assert body.fields.to_dict() == SNOWFLAKE_FIELDS
            assert body.to_dict()["fields"] == SNOWFLAKE_FIELDS
        finally:
            module.create_destination.sync_detailed = original

    def test_create_omits_optional_fields(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that create() leaves an omitted auth_method UNSET rather than null."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.create_destination.sync_detailed = mock_sync

        try:
            destinations_resource.create(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            body = mock_sync.call_args.kwargs["body"]
            assert body.auth_method is UNSET
            assert "auth_method" not in body.to_dict()
        finally:
            module.create_destination.sync_detailed = original

    def test_create_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that create() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        module.create_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.create(
                    team_id=12345,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 401
        finally:
            module.create_destination.sync_detailed = original

    def test_create_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that create() raises the not-found APIError on 404."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        module.create_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Team not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.create(
                    team_id=999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 404
        finally:
            module.create_destination.sync_detailed = original

    def test_create_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that create() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.sync_detailed
        module.create_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.create(
                    team_id=12345,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 500
        finally:
            module.create_destination.sync_detailed = original

    # --- update() ---

    def test_update_success(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test successful destination update, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.sync_detailed
        module.update_destination.sync_detailed = MagicMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            updated = destinations_resource.update(
                team_id=12345,
                destination_id=8,
                type="DWH_SNOWFLAKE",
                display_name="Renamed destination",
                fields=SNOWFLAKE_FIELDS,
            )

            assert updated.id == 8
            assert updated.destination_type.title == "Snowflake"
        finally:
            module.update_destination.sync_detailed = original

    def test_update_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that update() passes the correct body to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.update_destination.sync_detailed = mock_sync

        try:
            destinations_resource.update(
                team_id=12345,
                destination_id=8,
                type="DWH_SNOWFLAKE",
                display_name="Renamed destination",
                fields=SNOWFLAKE_FIELDS,
                auth_method="AUTH_METHOD_KEY_PAIR",
                new_password="not-a-real-passphrase",
            )

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["destination_id"] == 8
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert body.display_name == "Renamed destination"
            assert body.fields.to_dict() == SNOWFLAKE_FIELDS
            assert body.auth_method == "AUTH_METHOD_KEY_PAIR"
            assert body.new_password == "not-a-real-passphrase"
            assert body.to_dict()["new_password"] == "not-a-real-passphrase"
        finally:
            module.update_destination.sync_detailed = original

    def test_update_omits_optional_fields(
        self,
        destinations_resource: DestinationsResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that update() leaves an omitted new_password UNSET rather than null."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.update_destination.sync_detailed = mock_sync

        try:
            destinations_resource.update(
                team_id=12345,
                destination_id=8,
                type="DWH_SNOWFLAKE",
                display_name="Renamed destination",
                fields=SNOWFLAKE_FIELDS,
            )

            body = mock_sync.call_args.kwargs["body"]
            assert body.auth_method is UNSET
            assert body.new_password is UNSET
            assert "auth_method" not in body.to_dict()
            assert "new_password" not in body.to_dict()
        finally:
            module.update_destination.sync_detailed = original

    def test_update_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that update() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.sync_detailed
        module.update_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.update(
                    team_id=12345,
                    destination_id=8,
                    type="DWH_SNOWFLAKE",
                    display_name="Renamed destination",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 401
        finally:
            module.update_destination.sync_detailed = original

    def test_update_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that update() raises the not-found APIError on 404 with destination context."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.sync_detailed
        module.update_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.update(
                    team_id=12345,
                    destination_id=999,
                    type="DWH_SNOWFLAKE",
                    display_name="Renamed destination",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.update_destination.sync_detailed = original

    def test_update_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that update() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.sync_detailed
        module.update_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.update(
                    team_id=12345,
                    destination_id=8,
                    type="DWH_SNOWFLAKE",
                    display_name="Renamed destination",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 500
        finally:
            module.update_destination.sync_detailed = original

    # --- delete() ---

    def test_delete_success(self, destinations_resource: DestinationsResource) -> None:
        """Test that delete() returns None on the API's 204 No Content."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.sync_detailed
        module.delete_destination.sync_detailed = MagicMock(return_value=_make_no_content_response())

        try:
            result = destinations_resource.delete(team_id=12345, destination_id=8)

            assert result is None
        finally:
            module.delete_destination.sync_detailed = original

    def test_delete_passes_correct_params(self, destinations_resource: DestinationsResource) -> None:
        """Test that delete() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.sync_detailed
        mock_sync = MagicMock(return_value=_make_no_content_response())
        module.delete_destination.sync_detailed = mock_sync

        try:
            destinations_resource.delete(team_id=12345, destination_id=8)

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["destination_id"] == 8
        finally:
            module.delete_destination.sync_detailed = original

    def test_delete_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that delete() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.sync_detailed
        module.delete_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.delete(team_id=12345, destination_id=8)

            assert exc_info.value.status_code == 401
        finally:
            module.delete_destination.sync_detailed = original

    def test_delete_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that a 404 on delete() raises rather than being swallowed by the 204 check."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.sync_detailed
        module.delete_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.delete(team_id=12345, destination_id=999)

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.delete_destination.sync_detailed = original

    def test_delete_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that delete() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.sync_detailed
        module.delete_destination.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.delete(team_id=12345, destination_id=8)

            assert exc_info.value.status_code == 500
        finally:
            module.delete_destination.sync_detailed = original

    # --- test_connection() ---

    def test_test_connection_success(self, destinations_resource: DestinationsResource, meta: Meta) -> None:
        """Test that a working connection comes back as a result object, unwrapped."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        module.test_connection.sync_detailed = MagicMock(
            return_value=_make_success_response(
                ConnectionTestResponse(meta=meta, data=ConnectionTestResult(success=True, error=None))
            )
        )

        try:
            result = destinations_resource.test_connection(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            assert isinstance(result, ConnectionTestResult)
            assert result.success is True
            assert result.error is None
        finally:
            module.test_connection.sync_detailed = original

    def test_test_connection_returns_failure_without_raising(
        self,
        destinations_resource: DestinationsResource,
        meta: Meta,
    ) -> None:
        """Test that a failed connection test is a returned result, not an exception."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        module.test_connection.sync_detailed = MagicMock(
            return_value=_make_success_response(
                ConnectionTestResponse(
                    meta=meta,
                    data=ConnectionTestResult(success=False, error="Could not authenticate with the warehouse"),
                )
            )
        )

        try:
            result = destinations_resource.test_connection(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            assert result.success is False
            assert result.error == "Could not authenticate with the warehouse"
        finally:
            module.test_connection.sync_detailed = original

    def test_test_connection_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        meta: Meta,
    ) -> None:
        """Test that test_connection() passes the correct body to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(
                ConnectionTestResponse(meta=meta, data=ConnectionTestResult(success=True, error=None))
            )
        )
        module.test_connection.sync_detailed = mock_sync

        try:
            destinations_resource.test_connection(
                team_id=12345,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
                auth_method="AUTH_METHOD_KEY_PAIR",
                destination_id=8,
                new_password="not-a-real-passphrase",
            )

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert body.display_name == "Snowflake analytics"
            assert body.fields.to_dict() == SNOWFLAKE_FIELDS
            assert body.auth_method == "AUTH_METHOD_KEY_PAIR"
            assert body.destination_id == 8
            assert body.new_password == "not-a-real-passphrase"
            assert body.to_dict()["destination_id"] == 8
        finally:
            module.test_connection.sync_detailed = original

    def test_test_connection_omits_optional_fields(
        self,
        destinations_resource: DestinationsResource,
        meta: Meta,
    ) -> None:
        """Test that test_connection() leaves an omitted destination_id UNSET rather than null."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(
                ConnectionTestResponse(meta=meta, data=ConnectionTestResult(success=True, error=None))
            )
        )
        module.test_connection.sync_detailed = mock_sync

        try:
            destinations_resource.test_connection(
                team_id=12345,
                type="DWH_BIGQUERY",
                display_name="BigQuery warehouse",
                fields=BIGQUERY_FIELDS,
            )

            body = mock_sync.call_args.kwargs["body"]
            assert body.auth_method is UNSET
            assert body.destination_id is UNSET
            assert body.new_password is UNSET
            assert "destination_id" not in body.to_dict()
            assert body.fields.to_dict() == BIGQUERY_FIELDS
        finally:
            module.test_connection.sync_detailed = original

    def test_test_connection_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that test_connection() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        module.test_connection.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.test_connection(
                    team_id=12345,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 401
        finally:
            module.test_connection.sync_detailed = original

    def test_test_connection_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that test_connection() raises the not-found APIError on 404."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        module.test_connection.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.test_connection(
                    team_id=12345,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                    destination_id=999,
                )

            assert exc_info.value.status_code == 404
        finally:
            module.test_connection.sync_detailed = original

    def test_test_connection_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that test_connection() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.sync_detailed
        module.test_connection.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.test_connection(
                    team_id=12345,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 500
        finally:
            module.test_connection.sync_detailed = original

    # --- get_usage() ---

    def test_get_usage_success(
        self,
        destinations_resource: DestinationsResource,
        sample_usage: DestinationUsage,
        meta: Meta,
    ) -> None:
        """Test successful usage retrieval, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.sync_detailed
        module.get_destination_usage.sync_detailed = MagicMock(
            return_value=_make_success_response(DestinationUsageResponse(meta=meta, data=sample_usage))
        )

        try:
            usage = destinations_resource.get_usage(team_id=12345, destination_id=8)

            assert usage.is_used is True
            assert len(usage.transfers) == 1
            assert usage.transfers[0].transfer_id == 36091
            assert usage.transfers[0].transfer_name == "AW enhanced"
        finally:
            module.get_destination_usage.sync_detailed = original

    def test_get_usage_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        sample_usage: DestinationUsage,
        meta: Meta,
    ) -> None:
        """Test that get_usage() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.sync_detailed
        mock_sync = MagicMock(
            return_value=_make_success_response(DestinationUsageResponse(meta=meta, data=sample_usage))
        )
        module.get_destination_usage.sync_detailed = mock_sync

        try:
            destinations_resource.get_usage(team_id=12345, destination_id=8)

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            assert call_kwargs["destination_id"] == 8
        finally:
            module.get_destination_usage.sync_detailed = original

    def test_get_usage_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that get_usage() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.sync_detailed
        module.get_destination_usage.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.get_usage(team_id=12345, destination_id=8)

            assert exc_info.value.status_code == 401
        finally:
            module.get_destination_usage.sync_detailed = original

    def test_get_usage_not_found_on_404(self, destinations_resource: DestinationsResource) -> None:
        """Test that get_usage() raises the not-found APIError on 404 with destination context."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.sync_detailed
        module.get_destination_usage.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                destinations_resource.get_usage(team_id=12345, destination_id=999)

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.get_destination_usage.sync_detailed = original

    def test_get_usage_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that get_usage() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.sync_detailed
        module.get_destination_usage.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.get_usage(team_id=12345, destination_id=8)

            assert exc_info.value.status_code == 500
        finally:
            module.get_destination_usage.sync_detailed = original

    # ── batch_update ────────────────────────────────────────────────────

    def test_batch_update_success(
        self,
        destinations_resource: DestinationsResource,
        meta: Meta,
    ) -> None:
        """Test successful batch update returns the data envelope."""
        import supermetrics.resources.destinations as module

        data = _BatchData(has_errors=False, results=[])
        original = module.batch_update_destinations.sync_detailed
        module.batch_update_destinations.sync_detailed = MagicMock(
            return_value=_make_success_response(_BatchResponse200(meta=meta, data=data))
        )

        try:
            result = destinations_resource.batch_update(
                team_id=12345,
                destination_type="DWH_SNOWFLAKE",
                updates=[_BatchUpdateItem(destination_id=8, new_secret="new-pw-123")],
            )

            assert result.has_errors is False
            assert result.results == []
        finally:
            module.batch_update_destinations.sync_detailed = original

    def test_batch_update_partial_failure(
        self,
        destinations_resource: DestinationsResource,
        meta: Meta,
    ) -> None:
        """Test batch update with partial failure reports has_errors and per-item results."""
        import supermetrics.resources.destinations as module

        results_items = [
            _BatchResultItem(destination_id=8, status="success"),
            _BatchResultItem(destination_id=9, status="error", error_code="INVALID_SECRET", message="Secret too short"),
        ]
        data = _BatchData(has_errors=True, results=results_items)
        original = module.batch_update_destinations.sync_detailed
        module.batch_update_destinations.sync_detailed = MagicMock(
            return_value=_make_success_response(_BatchResponse200(meta=meta, data=data))
        )

        try:
            result = destinations_resource.batch_update(
                team_id=12345,
                destination_type="DWH_SNOWFLAKE",
                updates=[
                    _BatchUpdateItem(destination_id=8, new_secret="new-pw-123"),
                    _BatchUpdateItem(destination_id=9, new_secret="x"),
                ],
            )

            assert result.has_errors is True
            assert len(result.results) == 2
            assert result.results[0].status == "success"
            assert result.results[1].status == "error"
            assert result.results[1].error_code == "INVALID_SECRET"
        finally:
            module.batch_update_destinations.sync_detailed = original

    def test_batch_update_passes_correct_params(
        self,
        destinations_resource: DestinationsResource,
        meta: Meta,
    ) -> None:
        """Test that batch_update() forwards destination_type and updates to the generated client."""
        import supermetrics.resources.destinations as module

        data = _BatchData(has_errors=False, results=[])
        original = module.batch_update_destinations.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(_BatchResponse200(meta=meta, data=data)))
        module.batch_update_destinations.sync_detailed = mock_sync

        try:
            destinations_resource.batch_update(
                team_id=12345,
                destination_type="DWH_SNOWFLAKE",
                updates=[_BatchUpdateItem(destination_id=8, new_secret="new-pw-123")],
            )

            call_kwargs = mock_sync.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert len(body.updates) == 1
            assert body.updates[0].destination_id == 8
            assert body.updates[0].new_secret == "new-pw-123"
        finally:
            module.batch_update_destinations.sync_detailed = original

    def test_batch_update_auth_error_on_401(self, destinations_resource: DestinationsResource) -> None:
        """Test that batch_update() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.batch_update_destinations.sync_detailed
        module.batch_update_destinations.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                destinations_resource.batch_update(team_id=12345, destination_type="DWH_SNOWFLAKE", updates=[])

            assert exc_info.value.status_code == 401
        finally:
            module.batch_update_destinations.sync_detailed = original

    def test_batch_update_validation_error_on_400(self, destinations_resource: DestinationsResource) -> None:
        """Test that batch_update() raises ValidationError on 400."""
        import supermetrics.resources.destinations as module
        from supermetrics.exceptions import SupermetricsValidationError

        original = module.batch_update_destinations.sync_detailed
        module.batch_update_destinations.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "INVALID_REQUEST", "Duplicate destination_id")
        )

        try:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                destinations_resource.batch_update(team_id=12345, destination_type="DWH_SNOWFLAKE", updates=[])

            assert exc_info.value.status_code == 400
        finally:
            module.batch_update_destinations.sync_detailed = original

    def test_batch_update_api_error_on_500(self, destinations_resource: DestinationsResource) -> None:
        """Test that batch_update() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.batch_update_destinations.sync_detailed
        module.batch_update_destinations.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                destinations_resource.batch_update(team_id=12345, destination_type="DWH_SNOWFLAKE", updates=[])

            assert exc_info.value.status_code == 500
        finally:
            module.batch_update_destinations.sync_detailed = original


class TestDestinationsAsyncResource:
    """Test suite for DestinationsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock generated client."""
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def destinations_resource(self, mock_client: MagicMock) -> DestinationsAsyncResource:
        """Create a DestinationsAsyncResource instance with mock client."""
        return DestinationsAsyncResource(mock_client)

    @pytest.fixture
    def meta(self) -> Meta:
        """Create the response envelope metadata, which always carries a request_id."""
        return Meta(request_id="req_ba9876543210")

    @pytest.fixture
    def destination_items(self) -> list[DestinationListItem]:
        """Create the compact items the collection endpoint returns."""
        return [
            DestinationListItem(id=8, display_name="Snowflake analytics", type_="DWH_SNOWFLAKE"),
            DestinationListItem(id=9, display_name="BigQuery warehouse", type_="DWH_BIGQUERY"),
        ]

    @pytest.fixture
    def sample_destination(self) -> DestinationInfo:
        """Create a sample destination, which the API describes as an editable form."""
        return DestinationInfo(
            display_name="Snowflake analytics",
            destination_type=DestinationType(
                type_="DWH_SNOWFLAKE",
                title="Snowflake",
                icon_url="https://cdn.example.test/snowflake.svg",
            ),
            edit_settings=[
                SetupSetting(id="warehouse", input_type="text", is_required=True, label="Warehouse", value="DEMO_WH"),
                SetupSetting(id="role", input_type="text", is_required=False, label="Role", value="ACCOUNTADMIN"),
            ],
            id=8,
        )

    @pytest.fixture
    def sample_usage(self) -> DestinationUsage:
        """Create a sample usage report naming the transfers that still write to a destination."""
        return DestinationUsage(
            is_used=True,
            transfers=[DestinationUsageTransfersItem(transfer_id=36091, transfer_name="AW enhanced")],
        )

    # --- list() ---

    @pytest.mark.asyncio
    async def test_list_success(
        self,
        destinations_resource: DestinationsAsyncResource,
        destination_items: list[DestinationListItem],
        meta: Meta,
    ) -> None:
        """Test successful async destination listing, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.asyncio_detailed
        module.list_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(DestinationListResponse(meta=meta, data=destination_items))
        )

        try:
            destinations = await destinations_resource.list(team_id=99999)

            assert len(destinations) == 2
            assert destinations[0].id == 8
            assert destinations[0].display_name == "Snowflake analytics"
            assert destinations[0].type_ == "DWH_SNOWFLAKE"
            assert destinations[1].id == 9
            assert destinations[1].type_ == "DWH_BIGQUERY"
        finally:
            module.list_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        destination_items: list[DestinationListItem],
        meta: Meta,
    ) -> None:
        """Test that async list() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(DestinationListResponse(meta=meta, data=destination_items))
        )
        module.list_destinations.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.list(team_id=99999)

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            # The endpoint declares no query parameters, so nothing else may be sent.
            assert set(call_kwargs) == {"client", "team_id"}
        finally:
            module.list_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async list() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.asyncio_detailed
        module.list_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.list(team_id=99999)

            assert exc_info.value.status_code == 401
            assert "Invalid or expired API key" in str(exc_info.value)
        finally:
            module.list_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async list() surfaces an undocumented 404 as the not-found APIError."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.asyncio_detailed
        module.list_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Team not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.list(team_id=999)

            assert exc_info.value.status_code == 404
            assert isinstance(exc_info.value, APIError)
        finally:
            module.list_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async list() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.asyncio_detailed
        module.list_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.list(team_id=99999)

            assert exc_info.value.status_code == 500
        finally:
            module.list_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_list_network_error(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async list() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.destinations as module

        original = module.list_destinations.asyncio_detailed
        mock_request = Mock()
        mock_request.url = "https://dts-api.supermetrics.com/v1/teams/99999/destinations"
        module.list_destinations.asyncio_detailed = AsyncMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        try:
            with pytest.raises(NetworkError):
                await destinations_resource.list(team_id=99999)
        finally:
            module.list_destinations.asyncio_detailed = original

    # --- get() ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test successful async destination retrieval, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.asyncio_detailed
        module.get_destination.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            destination = await destinations_resource.get(team_id=99999, destination_id=8)

            assert destination.id == 8
            assert destination.display_name == "Snowflake analytics"
            assert destination.destination_type.type_ == "DWH_SNOWFLAKE"
            assert [setting.id for setting in destination.edit_settings] == ["warehouse", "role"]
            assert destination.edit_settings[0].value == "DEMO_WH"
        finally:
            module.get_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that async get() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.get_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.get(team_id=99999, destination_id=8)

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["destination_id"] == 8
        finally:
            module.get_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async get() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.asyncio_detailed
        module.get_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.get(team_id=99999, destination_id=8)

            assert exc_info.value.status_code == 401
        finally:
            module.get_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async get() raises the not-found APIError on 404 with destination context."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.asyncio_detailed
        module.get_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.get(team_id=99999, destination_id=999)

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.get_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async get() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.get_destination.asyncio_detailed
        module.get_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.get(team_id=99999, destination_id=8)

            assert exc_info.value.status_code == 500
        finally:
            module.get_destination.asyncio_detailed = original

    # --- create() ---

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test successful async destination creation, which the API answers with HTTP 201."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        module.create_destination.asyncio_detailed = AsyncMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            created = await destinations_resource.create(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            assert created.id == 8
            assert created.display_name == "Snowflake analytics"
            assert created.destination_type.type_ == "DWH_SNOWFLAKE"
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_treats_200_as_an_error(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that async create() accepts only 201; a 200 is not the documented success status."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        module.create_destination.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.create(
                    team_id=99999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 200
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that async create() passes the correct body to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.create_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.create(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
                auth_method="AUTH_METHOD_KEY_PAIR",
            )

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert body.display_name == "Snowflake analytics"
            assert body.auth_method == "AUTH_METHOD_KEY_PAIR"
            assert body.to_dict()["auth_method"] == "AUTH_METHOD_KEY_PAIR"
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_fields_round_trip(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that the plain fields dict survives the async trip through the generated Fields model."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.create_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.create(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            body = mock_asyncio.call_args.kwargs["body"]
            assert body.fields.to_dict() == SNOWFLAKE_FIELDS
            assert body.to_dict()["fields"] == SNOWFLAKE_FIELDS
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_omits_optional_fields(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that async create() leaves an omitted auth_method UNSET rather than null."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_created_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.create_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.create(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            body = mock_asyncio.call_args.kwargs["body"]
            assert body.auth_method is UNSET
            assert "auth_method" not in body.to_dict()
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async create() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        module.create_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.create(
                    team_id=99999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 401
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async create() raises the not-found APIError on 404."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        module.create_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Team not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.create(
                    team_id=999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 404
        finally:
            module.create_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_create_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async create() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.create_destination.asyncio_detailed
        module.create_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.create(
                    team_id=99999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 500
        finally:
            module.create_destination.asyncio_detailed = original

    # --- update() ---

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test successful async destination update, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.asyncio_detailed
        module.update_destination.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )

        try:
            updated = await destinations_resource.update(
                team_id=99999,
                destination_id=8,
                type="DWH_SNOWFLAKE",
                display_name="Renamed destination",
                fields=SNOWFLAKE_FIELDS,
            )

            assert updated.id == 8
            assert updated.destination_type.title == "Snowflake"
        finally:
            module.update_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that async update() passes the correct body to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.update_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.update(
                team_id=99999,
                destination_id=8,
                type="DWH_SNOWFLAKE",
                display_name="Renamed destination",
                fields=SNOWFLAKE_FIELDS,
                auth_method="AUTH_METHOD_KEY_PAIR",
                new_password="not-a-real-passphrase",
            )

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["destination_id"] == 8
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert body.display_name == "Renamed destination"
            assert body.fields.to_dict() == SNOWFLAKE_FIELDS
            assert body.auth_method == "AUTH_METHOD_KEY_PAIR"
            assert body.new_password == "not-a-real-passphrase"
            assert body.to_dict()["new_password"] == "not-a-real-passphrase"
        finally:
            module.update_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_omits_optional_fields(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_destination: DestinationInfo,
        meta: Meta,
    ) -> None:
        """Test that async update() leaves an omitted new_password UNSET rather than null."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(DestinationResponse(meta=meta, data=sample_destination))
        )
        module.update_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.update(
                team_id=99999,
                destination_id=8,
                type="DWH_SNOWFLAKE",
                display_name="Renamed destination",
                fields=SNOWFLAKE_FIELDS,
            )

            body = mock_asyncio.call_args.kwargs["body"]
            assert body.auth_method is UNSET
            assert body.new_password is UNSET
            assert "auth_method" not in body.to_dict()
            assert "new_password" not in body.to_dict()
        finally:
            module.update_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async update() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.asyncio_detailed
        module.update_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.update(
                    team_id=99999,
                    destination_id=8,
                    type="DWH_SNOWFLAKE",
                    display_name="Renamed destination",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 401
        finally:
            module.update_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async update() raises the not-found APIError on 404 with destination context."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.asyncio_detailed
        module.update_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.update(
                    team_id=99999,
                    destination_id=999,
                    type="DWH_SNOWFLAKE",
                    display_name="Renamed destination",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.update_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_update_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async update() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.update_destination.asyncio_detailed
        module.update_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.update(
                    team_id=99999,
                    destination_id=8,
                    type="DWH_SNOWFLAKE",
                    display_name="Renamed destination",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 500
        finally:
            module.update_destination.asyncio_detailed = original

    # --- delete() ---

    @pytest.mark.asyncio
    async def test_delete_success(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async delete() returns None on the API's 204 No Content."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.asyncio_detailed
        module.delete_destination.asyncio_detailed = AsyncMock(return_value=_make_no_content_response())

        try:
            result = await destinations_resource.delete(team_id=99999, destination_id=8)

            assert result is None
        finally:
            module.delete_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_delete_passes_correct_params(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async delete() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_no_content_response())
        module.delete_destination.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.delete(team_id=99999, destination_id=8)

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["destination_id"] == 8
        finally:
            module.delete_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_delete_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async delete() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.asyncio_detailed
        module.delete_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.delete(team_id=99999, destination_id=8)

            assert exc_info.value.status_code == 401
        finally:
            module.delete_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_delete_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that a 404 on async delete() raises rather than being swallowed by the 204 check."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.asyncio_detailed
        module.delete_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.delete(team_id=99999, destination_id=999)

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.delete_destination.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_delete_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async delete() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.delete_destination.asyncio_detailed
        module.delete_destination.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.delete(team_id=99999, destination_id=8)

            assert exc_info.value.status_code == 500
        finally:
            module.delete_destination.asyncio_detailed = original

    # --- test_connection() ---

    @pytest.mark.asyncio
    async def test_test_connection_success(self, destinations_resource: DestinationsAsyncResource, meta: Meta) -> None:
        """Test that a working connection comes back from async test_connection() unwrapped."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        module.test_connection.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(
                ConnectionTestResponse(meta=meta, data=ConnectionTestResult(success=True, error=None))
            )
        )

        try:
            result = await destinations_resource.test_connection(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            assert isinstance(result, ConnectionTestResult)
            assert result.success is True
            assert result.error is None
        finally:
            module.test_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_test_connection_returns_failure_without_raising(
        self,
        destinations_resource: DestinationsAsyncResource,
        meta: Meta,
    ) -> None:
        """Test that a failed async connection test is a returned result, not an exception."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        module.test_connection.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(
                ConnectionTestResponse(
                    meta=meta,
                    data=ConnectionTestResult(success=False, error="Could not authenticate with the warehouse"),
                )
            )
        )

        try:
            result = await destinations_resource.test_connection(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
            )

            assert result.success is False
            assert result.error == "Could not authenticate with the warehouse"
        finally:
            module.test_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_test_connection_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        meta: Meta,
    ) -> None:
        """Test that async test_connection() passes the correct body to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(
                ConnectionTestResponse(meta=meta, data=ConnectionTestResult(success=True, error=None))
            )
        )
        module.test_connection.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.test_connection(
                team_id=99999,
                type="DWH_SNOWFLAKE",
                display_name="Snowflake analytics",
                fields=SNOWFLAKE_FIELDS,
                auth_method="AUTH_METHOD_KEY_PAIR",
                destination_id=8,
                new_password="not-a-real-passphrase",
            )

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert body.display_name == "Snowflake analytics"
            assert body.fields.to_dict() == SNOWFLAKE_FIELDS
            assert body.auth_method == "AUTH_METHOD_KEY_PAIR"
            assert body.destination_id == 8
            assert body.new_password == "not-a-real-passphrase"
            assert body.to_dict()["destination_id"] == 8
        finally:
            module.test_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_test_connection_omits_optional_fields(
        self,
        destinations_resource: DestinationsAsyncResource,
        meta: Meta,
    ) -> None:
        """Test that async test_connection() leaves an omitted destination_id UNSET rather than null."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(
                ConnectionTestResponse(meta=meta, data=ConnectionTestResult(success=True, error=None))
            )
        )
        module.test_connection.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.test_connection(
                team_id=99999,
                type="DWH_BIGQUERY",
                display_name="BigQuery warehouse",
                fields=BIGQUERY_FIELDS,
            )

            body = mock_asyncio.call_args.kwargs["body"]
            assert body.auth_method is UNSET
            assert body.destination_id is UNSET
            assert body.new_password is UNSET
            assert "destination_id" not in body.to_dict()
            assert body.fields.to_dict() == BIGQUERY_FIELDS
        finally:
            module.test_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_test_connection_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async test_connection() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        module.test_connection.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.test_connection(
                    team_id=99999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 401
        finally:
            module.test_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_test_connection_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async test_connection() raises the not-found APIError on 404."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        module.test_connection.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.test_connection(
                    team_id=99999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                    destination_id=999,
                )

            assert exc_info.value.status_code == 404
        finally:
            module.test_connection.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_test_connection_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async test_connection() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.test_connection.asyncio_detailed
        module.test_connection.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.test_connection(
                    team_id=99999,
                    type="DWH_SNOWFLAKE",
                    display_name="Snowflake analytics",
                    fields=SNOWFLAKE_FIELDS,
                )

            assert exc_info.value.status_code == 500
        finally:
            module.test_connection.asyncio_detailed = original

    # --- get_usage() ---

    @pytest.mark.asyncio
    async def test_get_usage_success(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_usage: DestinationUsage,
        meta: Meta,
    ) -> None:
        """Test successful async usage retrieval, unwrapped from the meta/data envelope."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.asyncio_detailed
        module.get_destination_usage.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(DestinationUsageResponse(meta=meta, data=sample_usage))
        )

        try:
            usage = await destinations_resource.get_usage(team_id=99999, destination_id=8)

            assert usage.is_used is True
            assert len(usage.transfers) == 1
            assert usage.transfers[0].transfer_id == 36091
            assert usage.transfers[0].transfer_name == "AW enhanced"
        finally:
            module.get_destination_usage.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_usage_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        sample_usage: DestinationUsage,
        meta: Meta,
    ) -> None:
        """Test that async get_usage() passes the correct parameters to the generated client."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.asyncio_detailed
        mock_asyncio = AsyncMock(
            return_value=_make_success_response(DestinationUsageResponse(meta=meta, data=sample_usage))
        )
        module.get_destination_usage.asyncio_detailed = mock_asyncio

        try:
            await destinations_resource.get_usage(team_id=99999, destination_id=8)

            call_kwargs = mock_asyncio.call_args.kwargs
            assert call_kwargs["team_id"] == 99999
            assert call_kwargs["destination_id"] == 8
        finally:
            module.get_destination_usage.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_usage_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async get_usage() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.asyncio_detailed
        module.get_destination_usage.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.get_usage(team_id=99999, destination_id=8)

            assert exc_info.value.status_code == 401
        finally:
            module.get_destination_usage.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_usage_not_found_on_404(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async get_usage() raises the not-found APIError on 404 with destination context."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.asyncio_detailed
        module.get_destination_usage.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Destination not found")
        )

        try:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await destinations_resource.get_usage(team_id=99999, destination_id=999)

            assert exc_info.value.status_code == 404
            assert "Destination not found or you do not have access to it" in str(exc_info.value)
        finally:
            module.get_destination_usage.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_usage_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test that async get_usage() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.get_destination_usage.asyncio_detailed
        module.get_destination_usage.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.get_usage(team_id=99999, destination_id=8)

            assert exc_info.value.status_code == 500
        finally:
            module.get_destination_usage.asyncio_detailed = original

    # ── batch_update (async) ────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_batch_update_success(
        self,
        destinations_resource: DestinationsAsyncResource,
        meta: Meta,
    ) -> None:
        """Test async batch update returns the data envelope."""
        import supermetrics.resources.destinations as module

        data = _BatchData(has_errors=False, results=[])
        original = module.batch_update_destinations.asyncio_detailed
        module.batch_update_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(_BatchResponse200(meta=meta, data=data))
        )

        try:
            result = await destinations_resource.batch_update(
                team_id=12345,
                destination_type="DWH_SNOWFLAKE",
                updates=[_BatchUpdateItem(destination_id=8, new_secret="new-pw-123")],
            )

            assert result.has_errors is False
            assert result.results == []
        finally:
            module.batch_update_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_update_partial_failure(
        self,
        destinations_resource: DestinationsAsyncResource,
        meta: Meta,
    ) -> None:
        """Test async batch update with partial failure."""
        import supermetrics.resources.destinations as module

        results_items = [
            _BatchResultItem(destination_id=8, status="success"),
            _BatchResultItem(destination_id=9, status="error", error_code="INVALID_SECRET", message="Secret too short"),
        ]
        data = _BatchData(has_errors=True, results=results_items)
        original = module.batch_update_destinations.asyncio_detailed
        module.batch_update_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(_BatchResponse200(meta=meta, data=data))
        )

        try:
            result = await destinations_resource.batch_update(
                team_id=12345,
                destination_type="DWH_SNOWFLAKE",
                updates=[
                    _BatchUpdateItem(destination_id=8, new_secret="new-pw-123"),
                    _BatchUpdateItem(destination_id=9, new_secret="x"),
                ],
            )

            assert result.has_errors is True
            assert len(result.results) == 2
            assert result.results[0].status == "success"
            assert result.results[1].status == "error"
            assert result.results[1].error_code == "INVALID_SECRET"
        finally:
            module.batch_update_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_update_passes_correct_params(
        self,
        destinations_resource: DestinationsAsyncResource,
        meta: Meta,
    ) -> None:
        """Test async batch_update() forwards destination_type and updates."""
        import supermetrics.resources.destinations as module

        data = _BatchData(has_errors=False, results=[])
        original = module.batch_update_destinations.asyncio_detailed
        mock_async = AsyncMock(return_value=_make_success_response(_BatchResponse200(meta=meta, data=data)))
        module.batch_update_destinations.asyncio_detailed = mock_async

        try:
            await destinations_resource.batch_update(
                team_id=12345,
                destination_type="DWH_SNOWFLAKE",
                updates=[_BatchUpdateItem(destination_id=8, new_secret="new-pw-123")],
            )

            call_kwargs = mock_async.call_args.kwargs
            assert call_kwargs["team_id"] == 12345
            body = call_kwargs["body"]
            assert body.type_ == "DWH_SNOWFLAKE"
            assert len(body.updates) == 1
            assert body.updates[0].destination_id == 8
            assert body.updates[0].new_secret == "new-pw-123"
        finally:
            module.batch_update_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_update_auth_error_on_401(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test async batch_update() raises AuthenticationError on 401."""
        import supermetrics.resources.destinations as module

        original = module.batch_update_destinations.asyncio_detailed
        module.batch_update_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                await destinations_resource.batch_update(team_id=12345, destination_type="DWH_SNOWFLAKE", updates=[])

            assert exc_info.value.status_code == 401
        finally:
            module.batch_update_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_update_validation_error_on_400(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test async batch_update() raises ValidationError on 400."""
        import supermetrics.resources.destinations as module
        from supermetrics.exceptions import SupermetricsValidationError

        original = module.batch_update_destinations.asyncio_detailed
        module.batch_update_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "INVALID_REQUEST", "Duplicate destination_id")
        )

        try:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                await destinations_resource.batch_update(team_id=12345, destination_type="DWH_SNOWFLAKE", updates=[])

            assert exc_info.value.status_code == 400
        finally:
            module.batch_update_destinations.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_batch_update_api_error_on_500(self, destinations_resource: DestinationsAsyncResource) -> None:
        """Test async batch_update() raises APIError on 500."""
        import supermetrics.resources.destinations as module

        original = module.batch_update_destinations.asyncio_detailed
        module.batch_update_destinations.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        try:
            with pytest.raises(APIError) as exc_info:
                await destinations_resource.batch_update(team_id=12345, destination_type="DWH_SNOWFLAKE", updates=[])

            assert exc_info.value.status_code == 500
        finally:
            module.batch_update_destinations.asyncio_detailed = original
