"""Destinations resource adapter for Supermetrics Data Warehouse API."""

from __future__ import annotations

from typing import Any, cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_destinations import (
    create_destination,
    delete_destination,
    get_destination,
    get_destination_usage,
    list_destinations,
    test_connection,
    update_destination,
)
from supermetrics._generated.supermetrics_api_client.models.create_destination_request import CreateDestinationRequest
from supermetrics._generated.supermetrics_api_client.models.create_destination_request_fields import (
    CreateDestinationRequestFields,
)
from supermetrics._generated.supermetrics_api_client.models.destination_info import DestinationInfo
from supermetrics._generated.supermetrics_api_client.models.destination_list_item import DestinationListItem
from supermetrics._generated.supermetrics_api_client.models.destination_list_response import DestinationListResponse
from supermetrics._generated.supermetrics_api_client.models.destination_response import DestinationResponse
from supermetrics._generated.supermetrics_api_client.models.destination_usage import DestinationUsage
from supermetrics._generated.supermetrics_api_client.models.destination_usage_response import DestinationUsageResponse
from supermetrics._generated.supermetrics_api_client.models.test_connection_request import TestConnectionRequest
from supermetrics._generated.supermetrics_api_client.models.test_connection_request_fields import (
    TestConnectionRequestFields,
)
from supermetrics._generated.supermetrics_api_client.models.test_connection_response import TestConnectionResponse
from supermetrics._generated.supermetrics_api_client.models.test_connection_result import TestConnectionResult
from supermetrics._generated.supermetrics_api_client.models.update_destination_request import UpdateDestinationRequest
from supermetrics._generated.supermetrics_api_client.models.update_destination_request_fields import (
    UpdateDestinationRequestFields,
)
from supermetrics._generated.supermetrics_api_client.types import UNSET
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

# These classes expose a method named ``list``, which binds ``list`` in the class
# namespace and shadows the builtin for every annotation evaluated in the class body
# after that point. Aliasing the collection types out here, at module scope, is what
# keeps ``list[DestinationListItem]`` in a later method meaning a list of destinations
# rather than a subscript of ``DestinationsResource.list``. Do not inline these back.
DestinationItemList = list[DestinationListItem]
FieldMap = dict[str, Any]


class DestinationsAsyncResource:
    """Asynchronous resource adapter for Data Warehouse Destination operations.

    Async version of DestinationsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> destinations = await client.destinations.list(team_id=12345)
        >>> destination = await client.destinations.get(team_id=12345, destination_id=8)
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
    ) -> DestinationItemList:
        """List the destinations belonging to a team.

        Async version of DestinationsResource.list(). See sync version for full documentation.

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
        endpoint = f"/teams/{team_id}/destinations"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = await list_destinations.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(DestinationListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                headers=response.headers,
                raw_body=response.content,
            )

    async def get(
        self,
        team_id: int,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationInfo:
        """Retrieve a destination and its editable form settings by ID.

        Async version of DestinationsResource.get(). See sync version for full documentation.

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
            APIError: If the destination is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}"
        with (
            api_error_handler(endpoint, context_404="Destination not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_destination.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
            )
            if response.status_code == 200:
                return cast(DestinationResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def create(
        self,
        team_id: int,
        type: str,
        display_name: str,
        fields: FieldMap,
        *,
        auth_method: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationInfo:
        """Create a new destination.

        Async version of DestinationsResource.create(). See sync version for full documentation.

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
            ValidationError: If the destination configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 409, 429, 5xx). A
                conflict is HTTP 409 and surfaces as a generic ``APIError`` carrying
                ``status_code == 409``.
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/destinations"
        with (
            api_error_handler(endpoint, context_400="Invalid destination configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            # ``fields`` is a plain dict on the public signature because the generated
            # ``*Fields`` classes hold their storage in an ``_attrs_field(init=False)``
            # attribute, so a caller cannot construct one; ``from_dict`` is the way in.
            request = CreateDestinationRequest(
                type_=type,
                display_name=display_name,
                fields=CreateDestinationRequestFields.from_dict(fields),
                auth_method=auth_method if auth_method is not None else UNSET,
            )
            response = await create_destination.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(DestinationResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid destination configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def update(
        self,
        team_id: int,
        destination_id: int,
        type: str,
        display_name: str,
        fields: FieldMap,
        *,
        auth_method: str | None = None,
        new_password: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationInfo:
        """Update an existing destination.

        Async version of DestinationsResource.update(). See sync version for full documentation.

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
            ValidationError: If the destination configuration is invalid (HTTP 400, 422).
            APIError: If the destination is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid destination configuration",
                context_404="Destination not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            # ``fields`` is a plain dict on the public signature because the generated
            # ``*Fields`` classes hold their storage in an ``_attrs_field(init=False)``
            # attribute, so a caller cannot construct one; ``from_dict`` is the way in.
            request = UpdateDestinationRequest(
                type_=type,
                display_name=display_name,
                fields=UpdateDestinationRequestFields.from_dict(fields),
                auth_method=auth_method if auth_method is not None else UNSET,
                new_password=new_password if new_password is not None else UNSET,
            )
            response = await update_destination.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(DestinationResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                bad_request_msg="Invalid destination configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def delete(
        self,
        team_id: int,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a destination.

        Async version of DestinationsResource.delete(). See sync version for full documentation.

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
            APIError: If the destination is not found or API error (HTTP 403, 404, 409,
                429, 5xx). A conflict is HTTP 409 and surfaces as a generic ``APIError``
                carrying ``status_code == 409``.
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}"
        with (
            api_error_handler(endpoint, context_404="Destination not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_destination.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def test_connection(
        self,
        team_id: int,
        type: str,
        display_name: str,
        fields: FieldMap,
        *,
        auth_method: str | None = None,
        destination_id: int | None = None,
        new_password: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TestConnectionResult:
        """Test destination credentials, returning the result rather than raising.

        Async version of DestinationsResource.test_connection(). See sync version for full documentation.

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
            ValidationError: If the connection payload is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/destinations/test-connection"
        with (
            api_error_handler(endpoint, context_400="Invalid destination configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            # ``fields`` is a plain dict on the public signature because the generated
            # ``*Fields`` classes hold their storage in an ``_attrs_field(init=False)``
            # attribute, so a caller cannot construct one; ``from_dict`` is the way in.
            request = TestConnectionRequest(
                type_=type,
                display_name=display_name,
                fields=TestConnectionRequestFields.from_dict(fields),
                auth_method=auth_method if auth_method is not None else UNSET,
                destination_id=destination_id if destination_id is not None else UNSET,
                new_password=new_password if new_password is not None else UNSET,
            )
            response = await test_connection.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(TestConnectionResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid destination configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get_usage(
        self,
        team_id: int,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationUsage:
        """Report which transfers still use a destination.

        Async version of DestinationsResource.get_usage(). See sync version for full documentation.

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
            APIError: If the destination is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}/usage"
        with (
            api_error_handler(endpoint, context_404="Destination not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_destination_usage.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
            )
            if response.status_code == 200:
                return cast(DestinationUsageResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )


class DestinationsResource:
    """Synchronous resource adapter for Data Warehouse Destination operations.

    Provides a clean, Pythonic interface for the warehouse and storage destinations
    that transfers write into: listing and inspecting them, creating, updating and
    deleting them, testing a set of credentials before committing to it, and checking
    which transfers still depend on one.

    These endpoints are served by the Data Warehouse API, which lives on a separate
    host from the core Supermetrics API. The SDK routes them there automatically, so
    the same client and the same credential cover both.

    The read shape and the write shape of a destination genuinely differ. :meth:`create`
    and :meth:`update` take a flat ``fields`` mapping, while :meth:`get` answers with a
    ``DestinationInfo`` whose ``edit_settings`` is a list of UI form descriptors. What
    comes back from ``get`` cannot be handed straight to ``update``; see :meth:`get`.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # List the destinations of a team
        >>> destinations = client.destinations.list(team_id=12345)
        >>> # Inspect one destination
        >>> destination = client.destinations.get(team_id=12345, destination_id=8)
        >>> # Check what still depends on it, then remove it
        >>> usage = client.destinations.get_usage(team_id=12345, destination_id=8)
        >>> if not usage.is_used:
        ...     client.destinations.delete(team_id=12345, destination_id=8)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the DestinationsResource.

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
    ) -> DestinationItemList:
        """List the destinations belonging to a team.

        Returns every destination configured for the team as a summary of identifier,
        display name and type. The endpoint declares no pagination and no filtering
        parameters, so the whole set arrives in a single call.

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
            List[DestinationListItem]: The team's destinations.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> destinations = client.destinations.list(team_id=12345)
            >>> for destination in destinations:
            ...     print(f"{destination.id}: {destination.display_name} ({destination.type_})")
        """
        endpoint = f"/teams/{team_id}/destinations"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = list_destinations.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(DestinationListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                headers=response.headers,
                raw_body=response.content,
            )

    def get(
        self,
        team_id: int,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationInfo:
        """Retrieve a destination and its editable form settings by ID.

        Fetches the destination's display name, the descriptor of its type, and the
        settings that can be edited on it.

        What comes back is not what :meth:`create` and :meth:`update` take in.
        ``edit_settings`` is a list of ``SetupSetting`` form descriptors - each one an
        ``id`` / ``label`` / ``value`` / ``input_type`` / ``is_required`` record
        describing a single UI control - and **not** the flat ``fields`` mapping the
        write methods accept. The read shape and the write shape genuinely differ; the
        SDK surfaces the API's own model rather than inventing a symmetrical one. To
        feed an edit back into :meth:`update`, project the settings yourself, for
        example with ``{setting.id: setting.value for setting in destination.edit_settings}``,
        and re-supply anything the API does not hand back.

        Args:
            team_id: The unique identifier of the team.
            destination_id: The unique identifier of the destination.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DestinationInfo: The destination's name, type descriptor and editable settings.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the destination is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> destination = client.destinations.get(team_id=12345, destination_id=8)
            >>> print(destination.display_name, destination.destination_type.title)
            >>> for setting in destination.edit_settings:
            ...     print(f"{setting.id} ({setting.input_type}): {setting.value}")
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}"
        with (
            api_error_handler(endpoint, context_404="Destination not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_destination.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
            )
            if response.status_code == 200:
                return cast(DestinationResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def create(
        self,
        team_id: int,
        type: str,
        display_name: str,
        fields: FieldMap,
        *,
        auth_method: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationInfo:
        """Create a new destination.

        The destination becomes available to transfers immediately. It is worth calling
        :meth:`test_connection` first with the same ``type``, ``display_name`` and
        ``fields``, which exercises the credentials without storing anything.

        Args:
            team_id: The unique identifier of the team.
            type: Destination type identifier, for example ``"DWH_SNOWFLAKE"`` or
                ``"DWH_BIGQUERY"``. This is a free-form string on the wire, not an enum.
            display_name: Human-readable name for the destination.
            fields: Destination-specific configuration, as a flat mapping of setting
                name to value. The accepted keys vary by ``type`` - for Snowflake they
                include ``hostname``, ``warehouse``, ``database_name``, ``schema``,
                ``role``, ``username`` and the credential fields.
            auth_method: Authentication method for the destination, for example
                ``"AUTH_METHOD_KEY_PAIR"``. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DestinationInfo: The created destination. Note that this is the *read* shape
            described in :meth:`get`, with ``edit_settings`` rather than ``fields``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the destination configuration is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 409, 429, 5xx). The
                API documents HTTP 409 Conflict here; the error taxonomy has no
                dedicated conflict subclass, so it surfaces as a generic ``APIError``
                carrying ``status_code == 409``.
            NetworkError: If a network error occurs during the request.

        Example:
            >>> destination = client.destinations.create(
            ...     team_id=12345,
            ...     type="DWH_SNOWFLAKE",
            ...     display_name="My Snowflake Destination",
            ...     fields={
            ...         "hostname": "any-domain.my-region.snowflakecomputing.com",
            ...         "warehouse": "DEMO_WH",
            ...         "database_name": "TEST_DB",
            ...         "schema": "PUBLIC",
            ...         "role": "ACCOUNTADMIN",
            ...         "username": "USER",
            ...     },
            ...     auth_method="AUTH_METHOD_KEY_PAIR",
            ... )
            >>> print(destination.id)
        """
        endpoint = f"/teams/{team_id}/destinations"
        with (
            api_error_handler(endpoint, context_400="Invalid destination configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            # ``fields`` is a plain dict on the public signature because the generated
            # ``*Fields`` classes hold their storage in an ``_attrs_field(init=False)``
            # attribute, so a caller cannot construct one; ``from_dict`` is the way in.
            request = CreateDestinationRequest(
                type_=type,
                display_name=display_name,
                fields=CreateDestinationRequestFields.from_dict(fields),
                auth_method=auth_method if auth_method is not None else UNSET,
            )
            response = create_destination.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(DestinationResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid destination configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def update(
        self,
        team_id: int,
        destination_id: int,
        type: str,
        display_name: str,
        fields: FieldMap,
        *,
        auth_method: str | None = None,
        new_password: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationInfo:
        """Update an existing destination.

        This is a full replacement of the destination's configuration, so ``type``,
        ``display_name`` and ``fields`` are all required even when only one of them
        changes. The ``fields`` mapping is the same flat write shape :meth:`create`
        takes, not the ``edit_settings`` descriptors :meth:`get` returns - see
        :meth:`get` before trying to round-trip one into the other.

        Args:
            team_id: The unique identifier of the team.
            destination_id: The unique identifier of the destination to update.
            type: Destination type identifier, for example ``"DWH_SNOWFLAKE"``.
            display_name: Human-readable name for the destination.
            fields: Destination-specific configuration, as a flat mapping of setting
                name to value. The accepted keys vary by ``type``.
            auth_method: Authentication method for the destination, for example
                ``"AUTH_METHOD_KEY_PAIR"``. Optional.
            new_password: New secret value, for rotating a credential. The wire field
                the API applies it to depends on the authentication method (for
                key-pair auth it stands in for a new private key). Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DestinationInfo: The updated destination, in the read shape described in
            :meth:`get`.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the destination configuration is invalid (HTTP 400, 422).
            APIError: If the destination is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> destination = client.destinations.update(
            ...     team_id=12345,
            ...     destination_id=8,
            ...     type="DWH_SNOWFLAKE",
            ...     display_name="Renamed destination",
            ...     fields={"warehouse": "PROD_WH", "database_name": "PROD_DB"},
            ... )
            >>> print(destination.display_name)
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid destination configuration",
                context_404="Destination not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            # ``fields`` is a plain dict on the public signature because the generated
            # ``*Fields`` classes hold their storage in an ``_attrs_field(init=False)``
            # attribute, so a caller cannot construct one; ``from_dict`` is the way in.
            request = UpdateDestinationRequest(
                type_=type,
                display_name=display_name,
                fields=UpdateDestinationRequestFields.from_dict(fields),
                auth_method=auth_method if auth_method is not None else UNSET,
                new_password=new_password if new_password is not None else UNSET,
            )
            response = update_destination.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(DestinationResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                bad_request_msg="Invalid destination configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def delete(
        self,
        team_id: int,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a destination.

        A destination that transfers still depend on may not be removable; call
        :meth:`get_usage` first to see what is attached to it.

        Args:
            team_id: The unique identifier of the team.
            destination_id: The unique identifier of the destination to delete.
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
            APIError: If the destination is not found or API error (HTTP 403, 404, 409,
                429, 5xx). The API documents HTTP 409 Conflict here; the error taxonomy
                has no dedicated conflict subclass, so it surfaces as a generic
                ``APIError`` carrying ``status_code == 409``.
            NetworkError: If a network error occurs during the request.

        Example:
            >>> usage = client.destinations.get_usage(team_id=12345, destination_id=8)
            >>> if not usage.is_used:
            ...     client.destinations.delete(team_id=12345, destination_id=8)
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}"
        with (
            api_error_handler(endpoint, context_404="Destination not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_destination.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def test_connection(
        self,
        team_id: int,
        type: str,
        display_name: str,
        fields: FieldMap,
        *,
        auth_method: str | None = None,
        destination_id: int | None = None,
        new_password: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TestConnectionResult:
        """Test destination credentials without saving them.

        This is a dry run for :meth:`create`, and it takes the same ``type``,
        ``display_name`` and ``fields``. Nothing is stored.

        A connection that does not work is a successful call, not an error: the API
        answers HTTP 200 with ``success`` set to ``False`` and an ``error`` message,
        and this method **returns** that result rather than raising. Check
        ``result.success``; only transport, authorization and malformed-payload
        failures raise.

        Pass ``destination_id`` to test new credentials against a destination that
        already exists, for example before rotating a secret with :meth:`update`.

        Args:
            team_id: The unique identifier of the team.
            type: Destination type identifier to test, for example ``"DWH_SNOWFLAKE"``.
            display_name: Display name for the connection being tested.
            fields: Connection settings and credentials to test, as a flat mapping of
                setting name to value. The accepted keys vary by ``type``.
            auth_method: Authentication method to test, for example
                ``"AUTH_METHOD_KEY_PAIR"``. Optional.
            destination_id: Identifier of an existing destination to test with these
                credentials. Optional.
            new_password: New secret value to test before rotating it. The wire field
                the API applies it to depends on the authentication method. Optional.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TestConnectionResult: Whether the connection succeeded, and the error
            message when it did not.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the connection payload is invalid (HTTP 400, 422).
            APIError: If the API returns a server error (HTTP 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> result = client.destinations.test_connection(
            ...     team_id=12345,
            ...     type="DWH_SNOWFLAKE",
            ...     display_name="Test Connection",
            ...     fields={
            ...         "hostname": "any-domain.my-region.snowflakecomputing.com",
            ...         "warehouse": "DEMO_WH",
            ...         "username": "USER",
            ...     },
            ... )
            >>> if not result.success:
            ...     print(result.error)
        """
        endpoint = f"/teams/{team_id}/destinations/test-connection"
        with (
            api_error_handler(endpoint, context_400="Invalid destination configuration"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            # ``fields`` is a plain dict on the public signature because the generated
            # ``*Fields`` classes hold their storage in an ``_attrs_field(init=False)``
            # attribute, so a caller cannot construct one; ``from_dict`` is the way in.
            request = TestConnectionRequest(
                type_=type,
                display_name=display_name,
                fields=TestConnectionRequestFields.from_dict(fields),
                auth_method=auth_method if auth_method is not None else UNSET,
                destination_id=destination_id if destination_id is not None else UNSET,
                new_password=new_password if new_password is not None else UNSET,
            )
            response = test_connection.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(TestConnectionResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid destination configuration",
                headers=response.headers,
                raw_body=response.content,
            )

    def get_usage(
        self,
        team_id: int,
        destination_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> DestinationUsage:
        """Report which transfers still use a destination.

        Answers whether anything currently depends on the destination and, if so, names
        the transfers. Worth calling before :meth:`delete`.

        Args:
            team_id: The unique identifier of the team.
            destination_id: The unique identifier of the destination.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``X-Team-ID``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            DestinationUsage: Whether the destination is in use, and the transfers
            using it.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the destination is not found or API error (HTTP 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> usage = client.destinations.get_usage(team_id=12345, destination_id=8)
            >>> if usage.is_used:
            ...     for transfer in usage.transfers:
            ...         print(f"{transfer.transfer_id}: {transfer.transfer_name}")
        """
        endpoint = f"/teams/{team_id}/destinations/{destination_id}/usage"
        with (
            api_error_handler(endpoint, context_404="Destination not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_destination_usage.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                destination_id=destination_id,
            )
            if response.status_code == 200:
                return cast(DestinationUsageResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Destination not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )
