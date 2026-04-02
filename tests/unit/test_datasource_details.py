"""Unit tests for DatasourceDetailsResource and DatasourceDetailsAsyncResource."""

from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.models.datasource_details import DatasourceDetails
from supermetrics._generated.supermetrics_api_client.models.datasource_details_response import DatasourceDetailsResponse
from supermetrics._generated.supermetrics_api_client.models.datasource_details_status import DatasourceDetailsStatus
from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.models.error_response_error import ErrorResponseError
from supermetrics._generated.supermetrics_api_client.models.meta import Meta
from supermetrics._generated.supermetrics_api_client.types import Response
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from supermetrics.resources.datasource_details import DatasourceDetailsAsyncResource, DatasourceDetailsResource


def _make_success_response(details: DatasourceDetails) -> Response:
    return Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=DatasourceDetailsResponse(data=details),
    )


def _make_error_response(status_code: HTTPStatus, code: str, message: str) -> Response:
    return Response(
        status_code=status_code,
        content=b"",
        headers={},
        parsed=ErrorResponse(
            meta=Meta(request_id="req-id"),
            error=ErrorResponseError(code=code, message=message),
        ),
    )


class TestDatasourceDetailsResource:
    """Test suite for DatasourceDetailsResource (synchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> DatasourceDetailsResource:
        return DatasourceDetailsResource(mock_client)

    @pytest.fixture
    def sample_details(self) -> DatasourceDetails:
        return DatasourceDetails(
            id="GAWA",
            name="Google Analytics 4",
            status=DatasourceDetailsStatus.RELEASED,
            is_authentication_required=True,
            has_account_list=True,
            has_fields=True,
        )

    # --- get() success ---

    def test_get_success(
        self,
        resource: DatasourceDetailsResource,
        sample_details: DatasourceDetails,
    ) -> None:
        """Test successful datasource details retrieval."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_success_response(sample_details)
        )

        result = resource.get(team_id=12345, data_source_id="GAWA")

        assert result.id == "GAWA"
        assert result.name == "Google Analytics 4"
        assert result.status == DatasourceDetailsStatus.RELEASED

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_passes_correct_params(
        self,
        resource: DatasourceDetailsResource,
        sample_details: DatasourceDetails,
    ) -> None:
        """Test that get() passes the correct parameters to the generated client."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_details))
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = mock_sync

        resource.get(team_id=12345, data_source_id="GAWA")

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["team_id"] == 12345
        assert call_kwargs["data_source_id"] == "GAWA"

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_passes_sm_app_id_header(
        self,
        resource: DatasourceDetailsResource,
        sample_details: DatasourceDetails,
    ) -> None:
        """Test that sm_app_id is forwarded when provided."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        mock_sync = MagicMock(return_value=_make_success_response(sample_details))
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = mock_sync

        resource.get(team_id=12345, data_source_id="GAWA", sm_app_id="my-app")

        call_kwargs = mock_sync.call_args.kwargs
        assert call_kwargs["sm_app_id"] == "my-app"

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    # --- get() error responses ---

    def test_get_auth_error_on_401(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises AuthenticationError on 401."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 401
        assert "Invalid or expired API key" in str(exc_info.value)

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_validation_error_on_400(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises ValidationError on 400."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Invalid request")
        )

        with pytest.raises(ValidationError) as exc_info:
            resource.get(team_id=12345, data_source_id="")

        assert exc_info.value.status_code == 400

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_api_error_on_403(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises APIError on 403."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 403
        assert "Forbidden" in str(exc_info.value)

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_api_error_on_404(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises APIError on 404."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Datasource not found")
        )

        with pytest.raises(APIError) as exc_info:
            resource.get(team_id=12345, data_source_id="UNKNOWN")

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value).lower()

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_api_error_on_429(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises APIError on 429 (rate limit)."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMITED", "Too many requests")
        )

        with pytest.raises(APIError) as exc_info:
            resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 429
        assert "Rate limit" in str(exc_info.value)

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_api_error_on_500(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises APIError on 500."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 500

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original

    def test_get_network_error(self, resource: DatasourceDetailsResource) -> None:
        """Test that get() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.sync_detailed
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/teams/12345/datasource/GAWA"
        module.get_teams_team_id_datasource_data_source_id.sync_detailed = MagicMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        with pytest.raises(NetworkError):
            resource.get(team_id=12345, data_source_id="GAWA")

        module.get_teams_team_id_datasource_data_source_id.sync_detailed = original


class TestDatasourceDetailsAsyncResource:
    """Test suite for DatasourceDetailsAsyncResource (asynchronous)."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock(spec=GeneratedClient)

    @pytest.fixture
    def resource(self, mock_client: MagicMock) -> DatasourceDetailsAsyncResource:
        return DatasourceDetailsAsyncResource(mock_client)

    @pytest.fixture
    def sample_details(self) -> DatasourceDetails:
        return DatasourceDetails(
            id="AW",
            name="Google Ads",
            status=DatasourceDetailsStatus.RELEASED,
            is_authentication_required=True,
        )

    # --- get() success ---

    @pytest.mark.asyncio
    async def test_get_success(
        self,
        resource: DatasourceDetailsAsyncResource,
        sample_details: DatasourceDetails,
    ) -> None:
        """Test successful async datasource details retrieval."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_success_response(sample_details)
        )

        result = await resource.get(team_id=12345, data_source_id="AW")

        assert result.id == "AW"
        assert result.name == "Google Ads"

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_passes_correct_params(
        self,
        resource: DatasourceDetailsAsyncResource,
        sample_details: DatasourceDetails,
    ) -> None:
        """Test that async get() passes correct parameters."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        mock_asyncio = AsyncMock(return_value=_make_success_response(sample_details))
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = mock_asyncio

        await resource.get(team_id=99999, data_source_id="SA360")

        call_kwargs = mock_asyncio.call_args.kwargs
        assert call_kwargs["team_id"] == 99999
        assert call_kwargs["data_source_id"] == "SA360"

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    # --- get() error responses ---

    @pytest.mark.asyncio
    async def test_get_auth_error_on_401(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises AuthenticationError on 401."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Invalid API key")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 401

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_validation_error_on_400(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises ValidationError on 400."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "Invalid request")
        )

        with pytest.raises(ValidationError) as exc_info:
            await resource.get(team_id=12345, data_source_id="")

        assert exc_info.value.status_code == 400

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_403(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises APIError on 403."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.FORBIDDEN, "FORBIDDEN", "Forbidden")
        )

        with pytest.raises(APIError) as exc_info:
            await resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 403

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_404(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises APIError on 404."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Not found")
        )

        with pytest.raises(APIError) as exc_info:
            await resource.get(team_id=12345, data_source_id="UNKNOWN")

        assert exc_info.value.status_code == 404

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_429(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises APIError on 429."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.TOO_MANY_REQUESTS, "RATE_LIMITED", "Too many requests")
        )

        with pytest.raises(APIError) as exc_info:
            await resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 429

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_api_error_on_500(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises APIError on 500."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            return_value=_make_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Server error")
        )

        with pytest.raises(APIError) as exc_info:
            await resource.get(team_id=12345, data_source_id="GAWA")

        assert exc_info.value.status_code == 500

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original

    @pytest.mark.asyncio
    async def test_get_network_error(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Test that async get() raises NetworkError on httpx.RequestError."""
        import supermetrics.resources.datasource_details as module

        original = module.get_teams_team_id_datasource_data_source_id.asyncio_detailed
        mock_request = Mock()
        mock_request.url = "https://api.supermetrics.com/teams/12345/datasource/GAWA"
        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = AsyncMock(
            side_effect=httpx.ConnectError("Connection refused", request=mock_request)
        )

        with pytest.raises(NetworkError):
            await resource.get(team_id=12345, data_source_id="GAWA")

        module.get_teams_team_id_datasource_data_source_id.asyncio_detailed = original
