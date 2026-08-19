"""Custom Fields resource adapter for the Supermetrics Management API."""

from __future__ import annotations

from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.custom_fields import (
    create_transformation,
    delete_transformation,
    fetch_metadata,
    fetch_transformation,
    fetch_transformation_list,
    update_transformation,
)
from supermetrics._generated.supermetrics_api_client.models.condition_step import ConditionStep
from supermetrics._generated.supermetrics_api_client.models.custom_field_create_request import CustomFieldCreateRequest
from supermetrics._generated.supermetrics_api_client.models.custom_field_create_request_data_source_item import (
    CustomFieldCreateRequestDataSourceItem,
)
from supermetrics._generated.supermetrics_api_client.models.custom_field_create_request_field_type import (
    CustomFieldCreateRequestFieldType,
)
from supermetrics._generated.supermetrics_api_client.models.custom_field_update_request import CustomFieldUpdateRequest
from supermetrics._generated.supermetrics_api_client.models.function_step import FunctionStep
from supermetrics._generated.supermetrics_api_client.models.lookup_step import LookupStep
from supermetrics._generated.supermetrics_api_client.models.metadata_output import MetadataOutput
from supermetrics._generated.supermetrics_api_client.models.metadata_output_data import MetadataOutputData
from supermetrics._generated.supermetrics_api_client.models.paginated_transformations_output import (
    PaginatedTransformationsOutput,
)
from supermetrics._generated.supermetrics_api_client.models.single_transformation_output import (
    SingleTransformationOutput,
)
from supermetrics._generated.supermetrics_api_client.models.team_transformation_output import TeamTransformationOutput
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

# These classes expose a method named ``list``, which binds ``list`` in the class
# namespace and shadows the builtin for every annotation evaluated in the class body
# after that point. Aliasing the collection types out here, at module scope, is what
# keeps ``list[TeamTransformationOutput]`` in a later method meaning a list of custom
# fields rather than a subscript of ``CustomFieldsResource.list``. Do not inline these
# back.
TransformationStepList = list[ConditionStep | FunctionStep | LookupStep]
TeamTransformationList = list[TeamTransformationOutput]
DataSourceList = list[CustomFieldCreateRequestDataSourceItem]


def _page_items(parsed: PaginatedTransformationsOutput) -> TeamTransformationList:
    """Pull the page of custom fields out of a paginated response.

    Upstream marks ``data`` and ``data.items`` optional, so both can legitimately be
    absent on an empty page. An empty page is not an error, so this returns an empty
    list rather than raising.

    Args:
        parsed: The deserialized paginated response.

    Returns:
        list[TeamTransformationOutput]: The custom fields on this page, possibly empty.
    """
    data = parsed.data
    if isinstance(data, Unset) or isinstance(data.items, Unset):
        return []
    return data.items


class CustomFieldsAsyncResource:
    """Asynchronous resource adapter for Custom Field operations.

    Async version of CustomFieldsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> fields = await client.custom_fields.list(team_id=12345)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: int,
        *,
        data_source_id: str | None = None,
        display_name: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        include_total_count: bool | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationList:
        """List the custom fields defined for a team.

        Async version of CustomFieldsResource.list(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/custom-fields"
        with (
            api_error_handler(endpoint, context_400="Invalid custom field list query"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await fetch_transformation_list.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                data_source_id=data_source_id if data_source_id is not None else UNSET,
                display_name=display_name if display_name is not None else UNSET,
                page=page if page is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                include_total_count=include_total_count if include_total_count is not None else UNSET,
            )
            if response.status_code == 200:
                return _page_items(cast(PaginatedTransformationsOutput, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid custom field list query",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get(
        self,
        team_id: int,
        custom_field_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationOutput:
        """Retrieve a single custom field by ID.

        Async version of CustomFieldsResource.get(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the custom field is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/custom-fields/{custom_field_id}"
        with (
            api_error_handler(endpoint, context_404="Custom field not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await fetch_transformation.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                custom_field_id=custom_field_id,
            )
            if response.status_code == 200:
                return cast(SingleTransformationOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Custom field not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get_metadata(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> MetadataOutputData:
        """Retrieve the building blocks available for custom field definitions.

        Async version of CustomFieldsResource.get_metadata(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/custom-fields/metadata"
        with (
            api_error_handler(endpoint),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await fetch_metadata.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(MetadataOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def create(
        self,
        team_id: int,
        display_name: str,
        field_type: CustomFieldCreateRequestFieldType,
        data_type: str,
        definition: TransformationStepList,
        *,
        description: str | None = None,
        data_source: DataSourceList | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationOutput:
        """Create a custom field.

        Async version of CustomFieldsResource.create(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the definition is rejected or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/custom-fields"
        with (
            api_error_handler(endpoint, context_400="Invalid custom field definition"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CustomFieldCreateRequest(
                display_name=display_name,
                field_type=field_type,
                data_type=data_type,
                definition=definition,
                description=description if description is not None else UNSET,
                data_source=data_source if data_source is not None else UNSET,
            )
            response = await create_transformation.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(SingleTransformationOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid custom field definition",
                headers=response.headers,
                raw_body=response.content,
            )

    async def update(
        self,
        team_id: int,
        custom_field_id: int,
        display_name: str,
        data_type: str,
        definition: TransformationStepList,
        *,
        description: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationOutput:
        """Replace an existing custom field.

        Async version of CustomFieldsResource.update(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the definition is rejected or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/custom-fields/{custom_field_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid custom field definition",
                context_404="Custom field not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CustomFieldUpdateRequest(
                display_name=display_name,
                data_type=data_type,
                definition=definition,
                description=description if description is not None else UNSET,
            )
            response = await update_transformation.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                custom_field_id=custom_field_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(SingleTransformationOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Custom field not found or you do not have access to it",
                bad_request_msg="Invalid custom field definition",
                headers=response.headers,
                raw_body=response.content,
            )

    async def delete(
        self,
        team_id: int,
        custom_field_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a custom field.

        Async version of CustomFieldsResource.delete(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the custom field is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/custom-fields/{custom_field_id}"
        with (
            api_error_handler(endpoint, context_404="Custom field not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_transformation.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                custom_field_id=custom_field_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Custom field not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )


class CustomFieldsResource:
    """Synchronous resource adapter for Custom Field operations.

    Custom fields (called *field transformations* upstream) are calculated
    dimensions and metrics defined per team. Each one carries a ``definition``: an
    ordered pipeline of steps that is evaluated to produce the field's value.

    A step is one of three kinds, distinguished by its ``type``:

    - :class:`FunctionStep` — applies a named function to its arguments.
    - :class:`LookupStep` — maps input values to output values through a lookup table.
    - :class:`ConditionStep` — evaluates ordered cases and returns the first match.

    Call :meth:`get_metadata` to discover which functions, rules and data types the
    team is allowed to use before building a definition.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Note:
        The ``definition`` is asymmetric between request and response. It is *sent* as
        a bare list of steps and *returned* wrapped in an object with an ``items``
        attribute, so a read-modify-write cycle reads ``field.definition.items`` and
        passes that list back to :meth:`update`.

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> fields = client.custom_fields.list(team_id=12345)
        >>> for field in fields:
        ...     print(field.display_name, field.data_type)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the CustomFieldsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        *,
        data_source_id: str | None = None,
        display_name: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        include_total_count: bool | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationList:
        """List the custom fields defined for a team.

        Results are paginated. Only the page itself is returned; the pagination
        metadata the API sends alongside it (``total_count``, ``limit``, ``offset`` and
        the next/previous links) is available through the raw-response accessor::

            response = client.with_raw_response.custom_fields.list(team_id=12345)
            total = response.json_body["meta"]["pagination"]["total_count"]

        ``total_count`` is only present when ``include_total_count=True`` is passed;
        the API omits it by default for performance.

        Args:
            team_id: The unique identifier of the team.
            data_source_id: Only return fields belonging to this data source, for
                example ``"GAWA"``.
            display_name: Only return fields with this user-facing name.
            page: 1-based page number to fetch.
            limit: Maximum number of fields to return, 1 to 100. When omitted the
                server applies its own default of 25.
            include_total_count: Ask the API to report the total number of matching
                fields. Off by default upstream because counting costs time.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[TeamTransformationOutput]: The custom fields on this page. Empty when
            the page has no results.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> fields = client.custom_fields.list(team_id=12345, data_source_id="GAWA")
            >>> for field in fields:
            ...     print(f"{field.id}: {field.display_name}")
        """
        endpoint = f"/teams/{team_id}/custom-fields"
        with (
            api_error_handler(endpoint, context_400="Invalid custom field list query"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = fetch_transformation_list.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                data_source_id=data_source_id if data_source_id is not None else UNSET,
                display_name=display_name if display_name is not None else UNSET,
                page=page if page is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                include_total_count=include_total_count if include_total_count is not None else UNSET,
            )
            if response.status_code == 200:
                return _page_items(cast(PaginatedTransformationsOutput, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid custom field list query",
                headers=response.headers,
                raw_body=response.content,
            )

    def get(
        self,
        team_id: int,
        custom_field_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationOutput:
        """Retrieve a single custom field by ID.

        Args:
            team_id: The unique identifier of the team.
            custom_field_id: The unique identifier of the custom field.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TeamTransformationOutput: The custom field, including its definition,
            data type and last-modified metadata.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the custom field is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> field = client.custom_fields.get(team_id=12345, custom_field_id=42)
            >>> print(field.display_name)
            >>> for step in field.definition.items:
            ...     print(step.type_)
        """
        endpoint = f"/teams/{team_id}/custom-fields/{custom_field_id}"
        with (
            api_error_handler(endpoint, context_404="Custom field not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = fetch_transformation.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                custom_field_id=custom_field_id,
            )
            if response.status_code == 200:
                return cast(SingleTransformationOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Custom field not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def get_metadata(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> MetadataOutputData:
        """Retrieve the building blocks available for custom field definitions.

        Returns the functions the team may call, the rules available to condition and
        lookup steps, the field data types that can be referenced, the output data
        types a field may declare, and the team's limit on steps per definition. Call
        this before constructing a ``definition`` rather than guessing at names.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            MetadataOutputData: The functions, rules and data types available to this team.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> metadata = client.custom_fields.get_metadata(team_id=12345)
            >>> for function in metadata.functions.items:
            ...     print(function.name, function.return_types)
        """
        endpoint = f"/teams/{team_id}/custom-fields/metadata"
        with (
            api_error_handler(endpoint),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = fetch_metadata.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(MetadataOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def create(
        self,
        team_id: int,
        display_name: str,
        field_type: CustomFieldCreateRequestFieldType,
        data_type: str,
        definition: TransformationStepList,
        *,
        description: str | None = None,
        data_source: DataSourceList | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationOutput:
        """Create a custom field.

        The API answers ``201 Created`` and returns the persisted field, including the
        ``id`` and machine ``name`` it assigned.

        Args:
            team_id: The unique identifier of the team.
            display_name: User-facing name shown in the UI.
            field_type: ``"dim"`` for a dimension or ``"met"`` for a metric. This
                cannot be changed later — :meth:`update` does not accept it.
            data_type: Data type of the field, for example ``"string.text.value"``,
                ``"float.number.value"``, ``"int.number.value"`` or ``"bool"``.
            definition: Ordered pipeline of transformation steps. Each element is a
                :class:`FunctionStep`, :class:`LookupStep` or :class:`ConditionStep`.
            description: Free-text description of the field.
            data_source: Data sources the field applies to, each pairing a
                ``data_source_id`` with an optional ``report_type``.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TeamTransformationOutput: The created custom field.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the definition is rejected or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Note:
            An invalid definition comes back as HTTP 400, not 422 — this domain
            documents no 422 at all.

        Example:
            >>> from supermetrics import DefinitionValue, FunctionArgument, FunctionStep
            >>> step = FunctionStep(
            ...     type_="function",
            ...     name="upper_case",
            ...     arguments=[
            ...         FunctionArgument(
            ...             name="value",
            ...             value=DefinitionValue(type_="data_source_field", value="platform"),
            ...         )
            ...     ],
            ... )
            >>> field = client.custom_fields.create(
            ...     team_id=12345,
            ...     display_name="Platform (upper)",
            ...     field_type="dim",
            ...     data_type="string.text.value",
            ...     definition=[step],
            ... )
            >>> print(field.id)
        """
        endpoint = f"/teams/{team_id}/custom-fields"
        with (
            api_error_handler(endpoint, context_400="Invalid custom field definition"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CustomFieldCreateRequest(
                display_name=display_name,
                field_type=field_type,
                data_type=data_type,
                definition=definition,
                description=description if description is not None else UNSET,
                data_source=data_source if data_source is not None else UNSET,
            )
            response = create_transformation.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(SingleTransformationOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid custom field definition",
                headers=response.headers,
                raw_body=response.content,
            )

    def update(
        self,
        team_id: int,
        custom_field_id: int,
        display_name: str,
        data_type: str,
        definition: TransformationStepList,
        *,
        description: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamTransformationOutput:
        """Replace an existing custom field.

        This is a whole-object replace: there is no PATCH endpoint, so every field
        listed here is resent on every call and anything omitted reverts to unset.

        Args:
            team_id: The unique identifier of the team.
            custom_field_id: The unique identifier of the custom field to replace.
            display_name: User-facing name shown in the UI.
            data_type: Data type of the field, for example ``"string.text.value"``.
            definition: Ordered pipeline of transformation steps. Reading the current
                pipeline back means ``field.definition.items`` — the response wraps it
                in an object while the request takes a bare list.
            description: Free-text description of the field.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TeamTransformationOutput: The updated custom field.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the definition is rejected or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Note:
            ``field_type`` and ``data_source`` are deliberately absent. Upstream states
            that the field kind cannot be changed after creation, so unlike most
            update methods this one is not :meth:`create` with an id attached.

        Example:
            >>> current = client.custom_fields.get(team_id=12345, custom_field_id=42)
            >>> updated = client.custom_fields.update(
            ...     team_id=12345,
            ...     custom_field_id=42,
            ...     display_name="Platform (upper), revised",
            ...     data_type=current.data_type,
            ...     definition=current.definition.items,
            ... )
        """
        endpoint = f"/teams/{team_id}/custom-fields/{custom_field_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid custom field definition",
                context_404="Custom field not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CustomFieldUpdateRequest(
                display_name=display_name,
                data_type=data_type,
                definition=definition,
                description=description if description is not None else UNSET,
            )
            response = update_transformation.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                custom_field_id=custom_field_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(SingleTransformationOutput, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Custom field not found or you do not have access to it",
                bad_request_msg="Invalid custom field definition",
                headers=response.headers,
                raw_body=response.content,
            )

    def delete(
        self,
        team_id: int,
        custom_field_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a custom field.

        Args:
            team_id: The unique identifier of the team.
            custom_field_id: The unique identifier of the custom field to delete.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            None: The API returns 204 No Content on success.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the custom field is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.custom_fields.delete(team_id=12345, custom_field_id=42)
        """
        endpoint = f"/teams/{team_id}/custom-fields/{custom_field_id}"
        with (
            api_error_handler(endpoint, context_404="Custom field not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_transformation.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                custom_field_id=custom_field_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Custom field not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )
