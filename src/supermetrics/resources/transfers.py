"""Transfers resource adapter for Supermetrics Data Warehouse API."""

from __future__ import annotations

import datetime
import json
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_transfers import (
    batch_create_transfers,
    change_transfer_state,
    clone_transfer,
    create_data_source_connection,
    create_transfer,
    delete_transfer,
    get_available_sources,
    get_transfer,
    get_transfer_options,
    list_transfer_runs,
    list_transfers,
    update_transfer,
    validate_transfer,
    validate_transfer_update,
)
from supermetrics._generated.supermetrics_api_client.models.available_sources_response import AvailableSourcesResponse
from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_body import (
    BatchCreateTransfersBody,
)
from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200 import (
    BatchCreateTransfersResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.batch_create_transfers_response_200_data import (
    BatchCreateTransfersResponse200Data,
)
from supermetrics._generated.supermetrics_api_client.models.change_transfer_state_request import (
    ChangeTransferStateRequest,
)
from supermetrics._generated.supermetrics_api_client.models.change_transfer_state_request_transfer_state import (
    ChangeTransferStateRequestTransferState,
)
from supermetrics._generated.supermetrics_api_client.models.clone_transfer_body import CloneTransferBody
from supermetrics._generated.supermetrics_api_client.models.create_data_source_connection_request import (
    CreateDataSourceConnectionRequest,
)
from supermetrics._generated.supermetrics_api_client.models.create_data_source_connection_response import (
    CreateDataSourceConnectionResponse,
)
from supermetrics._generated.supermetrics_api_client.models.data_source_connection import DataSourceConnection
from supermetrics._generated.supermetrics_api_client.models.list_transfer_runs_sort_direction import (
    ListTransferRunsSortDirection,
)
from supermetrics._generated.supermetrics_api_client.models.list_transfer_runs_sort_field import (
    ListTransferRunsSortField,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_account import TransferAccount
from supermetrics._generated.supermetrics_api_client.models.transfer_configuration_request import (
    TransferConfigurationRequest,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_configuration_response import (
    TransferConfigurationResponse,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_created_envelope import TransferCreatedEnvelope
from supermetrics._generated.supermetrics_api_client.models.transfer_created_response import TransferCreatedResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_data_source_setting import (
    TransferDataSourceSetting,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_info_response import TransferInfoResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_list_response import TransferListResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_options_response import TransferOptionsResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_run_item import TransferRunItem
from supermetrics._generated.supermetrics_api_client.models.transfer_run_list_response import TransferRunListResponse
from supermetrics._generated.supermetrics_api_client.models.transfer_schedule import TransferSchedule
from supermetrics._generated.supermetrics_api_client.models.transfer_segment import TransferSegment
from supermetrics._generated.supermetrics_api_client.models.transfer_state_update_response import (
    TransferStateUpdateResponse,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_updated_response import TransferUpdatedResponse
from supermetrics._generated.supermetrics_api_client.models.validation_errors_response import ValidationErrorsResponse
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

# These classes expose a method named ``list``, which binds ``list`` in the class
# namespace and shadows the builtin for every annotation evaluated in the class body
# after that point. Aliasing the collection types out here, at module scope, is what
# keeps ``list[TransferSchedule]`` in a later method meaning a list of schedules rather
# than a subscript of ``TransfersResource.list``. Do not inline these back.
ScheduleList = list[TransferSchedule]
AccountList = list[TransferAccount]
SegmentList = list[TransferSegment]
DataSourceSettingList = list[TransferDataSourceSetting]
RecipientList = list[str]
TransferInfoList = list[TransferInfoResponse]
TransferRunItemList = list[TransferRunItem]
TransferConfigRequestList = list[TransferConfigurationRequest]


class TransfersAsyncResource:
    """Asynchronous resource adapter for Data Warehouse Transfers operations.

    Async version of TransfersResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> transfers = await client.transfers.list(team_id=12345)
        >>> configuration = await client.transfers.get(team_id=12345, transfer_id=36091)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferInfoList:
        """List the transfers belonging to a team.

        Async version of TransfersResource.list(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = await list_transfers.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(TransferListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="No transfers found for this team",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get(
        self,
        team_id: int,
        transfer_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferConfigurationResponse:
        """Retrieve the full configuration of a transfer.

        Async version of TransfersResource.get(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_transfer.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if response.status_code == 200:
                return cast(TransferConfigurationResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def create(
        self,
        team_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferCreatedResponse:
        """Create a new transfer.

        Async version of TransfersResource.create(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the transfer configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 409, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers"
        with (
            api_error_handler(endpoint, context_400="Invalid transfer configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = await create_transfer.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(TransferCreatedEnvelope, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid transfer configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def update(
        self,
        team_id: int,
        transfer_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferUpdatedResponse:
        """Replace the configuration of an existing transfer.

        Async version of TransfersResource.update(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the transfer configuration is invalid (HTTP 400, 422).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}"
        with (
            api_error_handler(endpoint, context_400="Invalid transfer configuration", context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = await update_transfer.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(TransferUpdatedResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg="Invalid transfer configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def delete(
        self,
        team_id: int,
        transfer_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a transfer.

        Async version of TransfersResource.delete(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_transfer.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def set_state(
        self,
        team_id: int,
        transfer_id: int,
        state: ChangeTransferStateRequestTransferState,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferStateUpdateResponse:
        """Pause or resume a transfer.

        Async version of TransfersResource.set_state(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the requested state is invalid (HTTP 400).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/state"
        with (
            api_error_handler(endpoint, context_400="Cannot change transfer state", context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = ChangeTransferStateRequest(transfer_state=state)
            response = await change_transfer_state.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(TransferStateUpdateResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg="Cannot change transfer state",
                headers=response.headers,
                raw_body=response.content,
            )

    async def validate(
        self,
        team_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ValidationErrorsResponse:
        """Validate a configuration for a new transfer without creating it.

        Async version of TransfersResource.validate(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/validations"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = await validate_transfer.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(ValidationErrorsResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def validate_update(
        self,
        team_id: int,
        transfer_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ValidationErrorsResponse:
        """Validate a configuration change against an existing transfer without applying it.

        Async version of TransfersResource.validate_update(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/validations"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = await validate_transfer_update.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(ValidationErrorsResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def list_available_sources(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AvailableSourcesResponse:
        """List the data sources and destinations available to a team.

        Async version of TransfersResource.list_available_sources(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/available-sources"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = await get_available_sources.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(AvailableSourcesResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get_available_options(
        self,
        team_id: int,
        source_id: str,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferOptionsResponse:
        """Get the configuration options for a source and destination combination.

        Async version of TransfersResource.get_available_options(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/available-options"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = await get_transfer_options.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                source_id=source_id,
                destination_id=destination_id,
            )
            if response.status_code == 200:
                return cast(TransferOptionsResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="No options found for this source and destination combination",
                headers=response.headers,
                raw_body=response.content,
            )

    async def list_runs(
        self,
        team_id: int,
        transfer_id: int,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        *,
        filter_issues_only: bool | None = None,
        sort_field: ListTransferRunsSortField | None = None,
        sort_direction: ListTransferRunsSortDirection | None = None,
        limit: int | None = None,
        offset: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferRunItemList:
        """List the runs of a transfer within a date range.

        Async version of TransfersResource.list_runs(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/runs"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await list_transfer_runs.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                start_date=start_date,
                end_date=end_date,
                filter_issues_only=filter_issues_only if filter_issues_only is not None else UNSET,
                sort_field=sort_field if sort_field is not None else UNSET,
                sort_direction=sort_direction if sort_direction is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                offset=offset if offset is not None else UNSET,
            )
            if response.status_code == 200:
                return cast(TransferRunListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def create_datasource_connection(
        self,
        team_id: int,
        data_source_id: str,
        destination_type: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceConnection:
        """Create a data source connection for a transfer.

        Async version of TransfersResource.create_datasource_connection(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the connection configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/data-source-connections"
        with (
            api_error_handler(endpoint, context_400="Invalid connection configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CreateDataSourceConnectionRequest(
                data_source_id=data_source_id,
                destination_type=destination_type,
            )
            response = await create_data_source_connection.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(CreateDataSourceConnectionResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid connection configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def clone(
        self,
        team_id: int,
        transfer_id: int,
        *,
        overrides: CloneTransferBody | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferCreatedResponse:
        """Clone an existing transfer.

        Async version of TransfersResource.clone(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the clone configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/clone"
        with (
            api_error_handler(endpoint, context_400="Invalid clone configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = overrides if overrides is not None else UNSET
            response = await clone_transfer.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=body,
            )
            if response.status_code in (200, 201):
                parsed = response.parsed
                if parsed is None:
                    # Stopgap: spec declares clone as 201-only, so the generated
                    # client returns parsed=None on 200. Remove once 200 is added
                    # to the canonical spec upstream.
                    parsed = TransferCreatedEnvelope.from_dict(json.loads(response.content))
                return cast(TransferCreatedEnvelope, parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg="Invalid clone configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def batch_create(
        self,
        team_id: int,
        transfers: TransferConfigRequestList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BatchCreateTransfersResponse200Data:
        """Create multiple transfers in a single request.

        Async version of TransfersResource.batch_create(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the batch configuration is invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/transfers/batch"
        with (
            api_error_handler(endpoint, context_400="Invalid batch transfer configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = BatchCreateTransfersBody(transfers=transfers)
            response = await batch_create_transfers.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=body,
            )
            if response.status_code == 200:
                parsed = cast(BatchCreateTransfersResponse200, response.parsed)
                return cast(BatchCreateTransfersResponse200Data, parsed.data)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid batch transfer configuration",
                headers=response.headers,
                raw_body=response.content,
            )


class TransfersResource:
    """Synchronous resource adapter for Data Warehouse Transfers operations.

    Provides a clean, Pythonic interface for the transfers that move data from a
    source into a data warehouse destination: listing and inspecting them, creating
    and updating their configuration, pausing and resuming them, reviewing their
    runs, and the option lookups, validation dry runs, and data source connections
    used to assemble a configuration in the first place.

    These endpoints are served by the Data Warehouse API, which lives on a separate
    host from the core Supermetrics API. The SDK routes them there automatically, so
    the same client and the same credential cover both.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # List the transfers of a team
        >>> transfers = client.transfers.list(team_id=12345)
        >>> # Inspect one transfer's configuration
        >>> configuration = client.transfers.get(team_id=12345, transfer_id=36091)
        >>> # Pause and resume a transfer
        >>> client.transfers.set_state(team_id=12345, transfer_id=36091, state="pause")
        >>> client.transfers.set_state(team_id=12345, transfer_id=36091, state="unpause")
        >>> # Delete a transfer
        >>> client.transfers.delete(team_id=12345, transfer_id=36091)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the TransfersResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferInfoList:
        """List the transfers belonging to a team.

        Returns a summary of every non-deleted transfer owned by the team, including
        its state, schedule, data source, destination, and latest backfill statistics.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            List[TransferInfoResponse]: The team's transfers.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> transfers = client.transfers.list(team_id=12345)
            >>> for transfer in transfers:
            ...     print(f"{transfer.dwh_transfer_id}: {transfer.display_name} ({transfer.state})")
        """
        endpoint = f"/teams/{team_id}/transfers"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = list_transfers.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(TransferListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="No transfers found for this team",
                headers=response.headers,
                raw_body=response.content,
            )

    def get(
        self,
        team_id: int,
        transfer_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferConfigurationResponse:
        """Retrieve the full configuration of a transfer.

        Fetches everything needed to render or reproduce a transfer: its schedule,
        accounts, segments, data source settings, destination, and license context.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TransferConfigurationResponse: The full transfer configuration.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> configuration = client.transfers.get(team_id=12345, transfer_id=36091)
            >>> print(configuration.display_name)
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_transfer.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if response.status_code == 200:
                return cast(TransferConfigurationResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def create(
        self,
        team_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferCreatedResponse:
        """Create a new transfer.

        The transfer starts running on the schedule given here. A connection to the
        data source must already exist - see
        :meth:`create_datasource_connection` - and it is worth calling
        :meth:`validate` first, which checks the same configuration without creating
        anything.

        Args:
            team_id: The unique identifier of the team.
            data_source_id: Data source identifier, for example ``"AW"``.
            schema_id: Numeric data warehouse schema identifier of the table group
                this transfer writes into. Take it from the ``schema_id`` field of the
                List table groups endpoint (``GET /table/groups``). The table group's
                prefixed ``group_id``, for example ``"tg_99999"``, is **not** accepted
                here.
            destination_id: Destination identifier.
            display_name: Human-readable name for the transfer.
            schedule: Execution schedule for the transfer.
            accounts: Data source accounts to include in the transfer.
            segments: Data segments to include in the transfer. Optional.
            data_source_settings: Source-specific configuration settings. Optional.
            notification_recipients: Email addresses to notify on transfer events. Optional.
            transfer_type: Transfer type identifier. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TransferCreatedResponse: The identifier and display name of the new transfer.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the transfer configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 409, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics import TransferAccount, TransferSchedule
            >>> created = client.transfers.create(
            ...     team_id=12345,
            ...     data_source_id="AW",
            ...     schema_id=2,
            ...     destination_id=8,
            ...     display_name="AW enhanced",
            ...     schedule=[TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)],
            ...     accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
            ... )
            >>> print(created.transfer_id)
        """
        endpoint = f"/teams/{team_id}/transfers"
        with (
            api_error_handler(endpoint, context_400="Invalid transfer configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = create_transfer.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(TransferCreatedEnvelope, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid transfer configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def update(
        self,
        team_id: int,
        transfer_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferUpdatedResponse:
        """Replace the configuration of an existing transfer.

        The configuration is replaced wholesale rather than merged, so send every
        field the transfer should keep, not only the ones that change. Call
        :meth:`validate_update` first to check the same payload without applying it.

        Two fields cannot be fed straight back from a read, because the API returns
        them in a different shape from the one it accepts. ``notification_recipients``
        comes back from :meth:`get` as objects with an ``email`` attribute but is sent
        here as plain strings. ``schedule`` and ``accounts`` come back from
        :meth:`list` as a string and a list of strings respectively and have to be
        rebuilt as ``TransferSchedule`` and ``TransferAccount`` objects; :meth:`get`
        returns those two already in the shape this method accepts.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer to update.
            data_source_id: Data source identifier, for example ``"AW"``.
            schema_id: Numeric data warehouse schema identifier of the table group
                this transfer writes into. Take it from the ``schema_id`` field of the
                List table groups endpoint (``GET /table/groups``). The table group's
                prefixed ``group_id``, for example ``"tg_99999"``, is **not** accepted
                here.
            destination_id: Destination identifier.
            display_name: Human-readable name for the transfer.
            schedule: Execution schedule for the transfer.
            accounts: Data source accounts to include in the transfer.
            segments: Data segments to include in the transfer. Optional.
            data_source_settings: Source-specific configuration settings. Optional.
            notification_recipients: Email addresses to notify on transfer events. Optional.
            transfer_type: Transfer type identifier. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TransferUpdatedResponse: The identifier and display name of the updated transfer.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the transfer configuration is invalid (HTTP 400, 422).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics import TransferAccount, TransferSchedule
            >>> updated = client.transfers.update(
            ...     team_id=12345,
            ...     transfer_id=36091,
            ...     data_source_id="AW",
            ...     schema_id=2,
            ...     destination_id=8,
            ...     display_name="AW enhanced (hourly)",
            ...     schedule=[TransferSchedule(run_interval="hourly", refresh_window=1)],
            ...     accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
            ... )
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}"
        with (
            api_error_handler(endpoint, context_400="Invalid transfer configuration", context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = update_transfer.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(TransferUpdatedResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg="Invalid transfer configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def delete(
        self,
        team_id: int,
        transfer_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a transfer.

        This is a soft delete: the transfer stops running and disappears from
        :meth:`list`, but the data it already wrote is preserved, along with its
        associated table settings being cleaned up.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer to delete.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            None: The API returns 204 No Content on success.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.transfers.delete(team_id=12345, transfer_id=36091)
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_transfer.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def set_state(
        self,
        team_id: int,
        transfer_id: int,
        state: ChangeTransferStateRequestTransferState,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferStateUpdateResponse:
        """Pause or resume a transfer.

        Pausing stops scheduled runs while preserving the configuration; unpausing
        restarts them from the next scheduled time. Runs already in progress are
        unaffected either way.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer.
            state: The action to perform, either ``"pause"`` or ``"unpause"``.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TransferStateUpdateResponse: The outcome and the transfer's new state.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the requested state is invalid (HTTP 400).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> paused = client.transfers.set_state(team_id=12345, transfer_id=36091, state="pause")
            >>> print(paused.state)
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/state"
        with (
            api_error_handler(endpoint, context_400="Cannot change transfer state", context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = ChangeTransferStateRequest(transfer_state=state)
            response = change_transfer_state.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(TransferStateUpdateResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg="Cannot change transfer state",
                headers=response.headers,
                raw_body=response.content,
            )

    def validate(
        self,
        team_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ValidationErrorsResponse:
        """Validate a configuration for a new transfer without creating it.

        This is a dry run for :meth:`create`, taking exactly the same arguments. An
        invalid configuration is a successful call, not an error: the API answers
        HTTP 200 with ``is_valid`` set to ``False`` and a list of field-level errors,
        and this method returns that response rather than raising.

        Args:
            team_id: The unique identifier of the team.
            data_source_id: Data source identifier, for example ``"AW"``.
            schema_id: Numeric data warehouse schema identifier of the table group
                this transfer would write into. Take it from the ``schema_id`` field of the
                List table groups endpoint (``GET /table/groups``). The table group's
                prefixed ``group_id``, for example ``"tg_99999"``, is **not** accepted
                here.
            destination_id: Destination identifier.
            display_name: Human-readable name for the transfer.
            schedule: Execution schedule for the transfer.
            accounts: Data source accounts to include in the transfer.
            segments: Data segments to include in the transfer. Optional.
            data_source_settings: Source-specific configuration settings. Optional.
            notification_recipients: Email addresses to notify on transfer events. Optional.
            transfer_type: Transfer type identifier. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ValidationErrorsResponse: Whether the configuration is valid, and the
            field-level errors when it is not.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics import TransferAccount, TransferSchedule
            >>> result = client.transfers.validate(
            ...     team_id=12345,
            ...     data_source_id="AW",
            ...     schema_id=2,
            ...     destination_id=8,
            ...     display_name="AW enhanced",
            ...     schedule=[TransferSchedule(run_interval="daily", run_hour=22)],
            ...     accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
            ... )
            >>> if not result.is_valid:
            ...     print(result.errors)
        """
        endpoint = f"/teams/{team_id}/transfers/validations"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = validate_transfer.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(ValidationErrorsResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def validate_update(
        self,
        team_id: int,
        transfer_id: int,
        data_source_id: str,
        schema_id: int,
        destination_id: int,
        display_name: str,
        schedule: ScheduleList,
        accounts: AccountList,
        *,
        segments: SegmentList | None = None,
        data_source_settings: DataSourceSettingList | None = None,
        notification_recipients: RecipientList | None = None,
        transfer_type: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ValidationErrorsResponse:
        """Validate a configuration change against an existing transfer without applying it.

        This is a dry run for :meth:`update`, taking exactly the same arguments. An
        invalid configuration is a successful call, not an error: the API answers
        HTTP 200 with ``is_valid`` set to ``False`` and a list of field-level errors,
        and this method returns that response rather than raising.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer the change targets.
            data_source_id: Data source identifier, for example ``"AW"``.
            schema_id: Numeric data warehouse schema identifier of the table group
                this transfer would write into. Take it from the ``schema_id`` field of the
                List table groups endpoint (``GET /table/groups``). The table group's
                prefixed ``group_id``, for example ``"tg_99999"``, is **not** accepted
                here.
            destination_id: Destination identifier.
            display_name: Human-readable name for the transfer.
            schedule: Execution schedule for the transfer.
            accounts: Data source accounts to include in the transfer.
            segments: Data segments to include in the transfer. Optional.
            data_source_settings: Source-specific configuration settings. Optional.
            notification_recipients: Email addresses to notify on transfer events. Optional.
            transfer_type: Transfer type identifier. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ValidationErrorsResponse: Whether the configuration is valid, and the
            field-level errors when it is not.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics import TransferAccount, TransferSchedule
            >>> result = client.transfers.validate_update(
            ...     team_id=12345,
            ...     transfer_id=36091,
            ...     data_source_id="AW",
            ...     schema_id=2,
            ...     destination_id=8,
            ...     display_name="AW enhanced (hourly)",
            ...     schedule=[TransferSchedule(run_interval="hourly")],
            ...     accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
            ... )
            >>> print(result.is_valid)
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/validations"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = TransferConfigurationRequest(
                data_source_id=data_source_id,
                schema_id=schema_id,
                destination_id=destination_id,
                display_name=display_name,
                schedule=schedule,
                accounts=accounts,
                segments=segments if segments is not None else UNSET,
                data_source_settings=data_source_settings if data_source_settings is not None else UNSET,
                notification_recipients=notification_recipients if notification_recipients is not None else UNSET,
                transfer_type=transfer_type if transfer_type is not None else UNSET,
            )
            response = validate_transfer_update.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(ValidationErrorsResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def list_available_sources(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AvailableSourcesResponse:
        """List the data sources and destinations available to a team.

        This is the first step in building a transfer configuration: it returns the
        data sources the team may transfer from, the destinations it may write to,
        and the setup settings and auth methods of each destination type. Feed the
        chosen pair into :meth:`get_available_options` to get the rest.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            AvailableSourcesResponse: The available data sources, destinations, and
            destination types.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> available = client.transfers.list_available_sources(team_id=12345)
            >>> for destination in available.destinations:
            ...     print(destination)
        """
        endpoint = f"/teams/{team_id}/transfers/available-sources"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = get_available_sources.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(AvailableSourcesResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def get_available_options(
        self,
        team_id: int,
        source_id: str,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferOptionsResponse:
        """Get the configuration options for a source and destination combination.

        Returns the schedule options, schemas, logins, accounts, segments, and data
        source settings that a transfer between this particular source and
        destination may use - the values that make a :meth:`create` call valid.

        Args:
            team_id: The unique identifier of the team.
            source_id: Data source identifier, for example ``"AW"``.
            destination_id: Destination identifier.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TransferOptionsResponse: The options available for this combination.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> options = client.transfers.get_available_options(
            ...     team_id=12345, source_id="AW", destination_id=8
            ... )
            >>> for schema in options.schemas:
            ...     print(schema)
        """
        endpoint = f"/teams/{team_id}/transfers/available-options"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = get_transfer_options.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                source_id=source_id,
                destination_id=destination_id,
            )
            if response.status_code == 200:
                return cast(TransferOptionsResponse, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="No options found for this source and destination combination",
                headers=response.headers,
                raw_body=response.content,
            )

    def list_runs(
        self,
        team_id: int,
        transfer_id: int,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        *,
        filter_issues_only: bool | None = None,
        sort_field: ListTransferRunsSortField | None = None,
        sort_direction: ListTransferRunsSortDirection | None = None,
        limit: int | None = None,
        offset: int | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferRunItemList:
        """List the runs of a transfer within a date range.

        The date range is required. Results are paginated, defaulting to 100 runs per
        page, and can be narrowed to runs that reported a problem. The API documents a
        maximum of 10000 per page, but that ceiling is prose in the specification with
        no schema constraint behind it, so neither the SDK nor the generated layer
        enforces it.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the transfer.
            start_date: Start of the range to list runs for.
            end_date: End of the range to list runs for.
            filter_issues_only: Return only runs that reported an issue. Optional.
            sort_field: Field to sort by - ``"created_time"``, ``"data_date"``, or
                ``"ended_time"``. Optional.
            sort_direction: Sort direction, ``"ASC"`` or ``"DESC"``. Optional.
            limit: Maximum number of runs to return. Optional; the API defaults to 100.
            offset: Number of runs to skip. Optional; the API defaults to 0.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            List[TransferRunItem]: The matching transfer runs.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the transfer is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> import datetime
            >>> runs = client.transfers.list_runs(
            ...     team_id=12345,
            ...     transfer_id=36091,
            ...     start_date=datetime.datetime(2024, 1, 1),
            ...     end_date=datetime.datetime(2024, 1, 31),
            ...     filter_issues_only=True,
            ...     sort_field="data_date",
            ...     sort_direction="DESC",
            ... )
            >>> for run in runs:
            ...     print(f"{run.id}: {run.status}")
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/runs"
        with (
            api_error_handler(endpoint, context_404="Transfer not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = list_transfer_runs.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                start_date=start_date,
                end_date=end_date,
                filter_issues_only=filter_issues_only if filter_issues_only is not None else UNSET,
                sort_field=sort_field if sort_field is not None else UNSET,
                sort_direction=sort_direction if sort_direction is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                offset=offset if offset is not None else UNSET,
            )
            if response.status_code == 200:
                return cast(TransferRunListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def create_datasource_connection(
        self,
        team_id: int,
        data_source_id: str,
        destination_type: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DataSourceConnection:
        """Create a data source connection for a transfer.

        A connection ties a data source to a destination type and must exist before a
        transfer using that pair can be created. Credentials are taken from the
        client's own authorization, encrypted, and stored by the API; the SDK never
        sends an API key in the request body.

        This is the only operation in this resource with a documented scope
        requirement: the credential must carry ``dwh_transfers_write``, or the API
        answers 403.

        Args:
            team_id: The unique identifier of the team.
            data_source_id: Data source identifier, for example ``"GA"`` or ``"ADM"``.
            destination_type: Destination type identifier, for example ``"SQL_BQ"``
                or ``"DWH_SNOWFLAKE"``.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DataSourceConnection: The created connection, with its identifier and any
            OAuth or connection URLs the data source requires.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the connection configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> connection = client.transfers.create_datasource_connection(
            ...     team_id=12345, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
            ... )
            >>> print(connection.connection_id)
        """
        endpoint = f"/teams/{team_id}/data-source-connections"
        with (
            api_error_handler(endpoint, context_400="Invalid connection configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CreateDataSourceConnectionRequest(
                data_source_id=data_source_id,
                destination_type=destination_type,
            )
            response = create_data_source_connection.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(CreateDataSourceConnectionResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid connection configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def clone(
        self,
        team_id: int,
        transfer_id: int,
        *,
        overrides: CloneTransferBody | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TransferCreatedResponse:
        """Clone an existing transfer, optionally overriding selected fields.

        The clone is a fully independent transfer — editing or deleting it never
        affects the source. Pass a ``CloneTransferBody`` to override fields; omit
        it or pass ``None`` to clone as-is. Fields not provided are copied from
        the source. Notification recipients are deliberately not copied (default
        to empty) but can be overridden explicitly.

        Restrictions:
        - The data source is always inherited and cannot be overridden.
        - The destination can be changed only to one of the same type.

        Args:
            team_id: The unique identifier of the team.
            transfer_id: The unique identifier of the source transfer to clone.
            overrides: Optional ``CloneTransferBody`` with fields to override in
                the clone. Omit to clone the transfer as-is.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only.
            timeout: Timeout override for this request only.

        Returns:
            TransferCreatedResponse: The identifier and display name of the cloned transfer.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the clone configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> cloned = client.transfers.clone(
            ...     team_id=12345,
            ...     transfer_id=36091,
            ... )
            >>> print(cloned.transfer_id)
        """
        endpoint = f"/teams/{team_id}/transfers/{transfer_id}/clone"
        with (
            api_error_handler(endpoint, context_400="Invalid clone configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = overrides if overrides is not None else UNSET
            response = clone_transfer.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                transfer_id=transfer_id,
                body=body,
            )
            if response.status_code in (200, 201):
                parsed = response.parsed
                if parsed is None:
                    # Stopgap: spec declares clone as 201-only, so the generated
                    # client returns parsed=None on 200. Remove once 200 is added
                    # to the canonical spec upstream.
                    parsed = TransferCreatedEnvelope.from_dict(json.loads(response.content))
                return cast(TransferCreatedEnvelope, parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Transfer not found or you do not have access to it",
                bad_request_msg="Invalid clone configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def batch_create(
        self,
        team_id: int,
        transfers: TransferConfigRequestList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BatchCreateTransfersResponse200Data:
        """Create multiple transfers in a single request.

        Each transfer configuration is created independently — if one fails, the
        others still succeed. Mixed data source types are allowed within a single
        batch.

        The batch must contain between 1 and 100 items. Empty batches, batches
        exceeding 100 items, and exact-duplicate configurations within the same
        batch are rejected. To create copies of an existing transfer, use
        :meth:`clone` instead.

        Args:
            team_id: The unique identifier of the team.
            transfers: List of transfer configurations, each using the same
                structure as the single-create endpoint.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only.
            timeout: Timeout override for this request only.

        Returns:
            BatchCreateTransfersResponse200Data: Results with ``has_errors`` flag
                and per-item ``results``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the batch configuration is invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics import TransferConfigurationRequest
            >>> results = client.transfers.batch_create(
            ...     team_id=12345,
            ...     transfers=[config1, config2],
            ... )
            >>> print(f"Errors: {results.has_errors}, Items: {len(results.results)}")
        """
        endpoint = f"/teams/{team_id}/transfers/batch"
        with (
            api_error_handler(endpoint, context_400="Invalid batch transfer configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            body = BatchCreateTransfersBody(transfers=transfers)
            response = batch_create_transfers.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=body,
            )
            if response.status_code == 200:
                parsed = cast(BatchCreateTransfersResponse200, response.parsed)
                return cast(BatchCreateTransfersResponse200Data, parsed.data)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid batch transfer configuration",
                headers=response.headers,
                raw_body=response.content,
            )
