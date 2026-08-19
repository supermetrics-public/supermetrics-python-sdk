"""Data Blending resource adapter for the Supermetrics Management API."""

from __future__ import annotations

from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.data_blending import (
    create_blend,
    delete_blend,
    get_blend,
    get_team_blends,
    update_blend,
)
from supermetrics._generated.supermetrics_api_client.models.blend_config import BlendConfig
from supermetrics._generated.supermetrics_api_client.models.blend_create_request import BlendCreateRequest
from supermetrics._generated.supermetrics_api_client.models.blend_create_request_type import BlendCreateRequestType
from supermetrics._generated.supermetrics_api_client.models.blend_list_item_output import BlendListItemOutput
from supermetrics._generated.supermetrics_api_client.models.blend_list_response import BlendListResponse
from supermetrics._generated.supermetrics_api_client.models.blend_output import BlendOutput
from supermetrics._generated.supermetrics_api_client.models.blend_response import BlendResponse
from supermetrics._generated.supermetrics_api_client.models.blend_update_request import BlendUpdateRequest
from supermetrics._generated.supermetrics_api_client.models.blended_data_source_input import BlendedDataSourceInput
from supermetrics._generated.supermetrics_api_client.models.get_team_blends_type import GetTeamBlendsType
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

# These classes expose a method named ``list``, which binds ``list`` in the class
# namespace and shadows the builtin for every annotation evaluated in the class body
# after that point. Aliasing the collection types out here, at module scope, is what
# keeps ``list[BlendedDataSourceInput]`` in a later method meaning a list of data
# sources rather than a subscript of ``BlendsResource.list``. Do not inline these back.
BlendSummaryList = list[BlendListItemOutput]
BlendedDataSourceInputList = list[BlendedDataSourceInput]


def _list_items(parsed: BlendListResponse) -> BlendSummaryList:
    """Pull the blends out of a list response.

    Upstream marks ``data.items`` optional, so it is legitimately absent when a team has
    no blends. That is not an error, so this returns an empty list rather than raising.

    ``data`` itself is required, which is why it is dereferenced without a guard: a body
    that omits it never reaches here, because the generated ``from_dict`` raises first and
    ``api_error_handler`` turns that into an SDK error. If a regeneration ever makes
    ``data`` optional, this line needs an ``isinstance(..., Unset)`` check.

    Args:
        parsed: The deserialized list response.

    Returns:
        list[BlendListItemOutput]: The team's blends, possibly empty.
    """
    items = parsed.data.items
    if isinstance(items, Unset):
        return []
    return items


class BlendsAsyncResource:
    """Asynchronous resource adapter for Data Blending operations.

    Async version of BlendsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> blends = await client.blends.list(team_id=12345)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: int,
        *,
        blend_type: GetTeamBlendsType | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendSummaryList:
        """List the blends defined for a team.

        Async version of BlendsResource.list(). See sync version for full documentation.

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
        endpoint = f"/teams/{team_id}/data-blending/blends"
        with (
            api_error_handler(endpoint, context_400="Invalid blend list query"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_team_blends.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                type_=blend_type if blend_type is not None else UNSET,
            )
            if response.status_code == 200:
                return _list_items(cast(BlendListResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid blend list query",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get(
        self,
        team_id: int,
        blend_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendOutput:
        """Retrieve a single blend, including its full configuration.

        Async version of BlendsResource.get(). See sync version for full documentation.

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
            APIError: If the blend is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/data-blending/blends/{blend_id}"
        with (
            api_error_handler(endpoint, context_404="Blend not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_blend.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                blend_id=blend_id,
            )
            if response.status_code == 200:
                return cast(BlendResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Blend not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def create(
        self,
        team_id: int,
        display_name: str,
        blend_type: BlendCreateRequestType,
        blended_data_sources: BlendedDataSourceInputList,
        config: BlendConfig,
        *,
        description: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendOutput:
        """Create a blend.

        Async version of BlendsResource.create(). See sync version for full documentation.

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
            APIError: If the blend is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/data-blending/blends"
        with (
            api_error_handler(endpoint, context_400="Invalid blend definition"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = BlendCreateRequest(
                type_=blend_type,
                display_name=display_name,
                blended_data_sources=blended_data_sources,
                config=config,
                description=description if description is not None else UNSET,
            )
            response = await create_blend.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(BlendResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid blend definition",
                headers=response.headers,
                raw_body=response.content,
            )

    async def update(
        self,
        team_id: int,
        blend_id: int,
        display_name: str,
        blended_data_sources: BlendedDataSourceInputList,
        config: BlendConfig,
        *,
        description: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendOutput:
        """Replace an existing blend.

        Async version of BlendsResource.update(). See sync version for full documentation.

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
            APIError: If the blend is rejected or not found (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/data-blending/blends/{blend_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid blend definition",
                context_404="Blend not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = BlendUpdateRequest(
                display_name=display_name,
                blended_data_sources=blended_data_sources,
                config=config,
                description=description if description is not None else UNSET,
            )
            response = await update_blend.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                blend_id=blend_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(BlendResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Blend not found or you do not have access to it",
                bad_request_msg="Invalid blend definition",
                headers=response.headers,
                raw_body=response.content,
            )

    async def delete(
        self,
        team_id: int,
        blend_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a blend.

        Async version of BlendsResource.delete(). See sync version for full documentation.

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
            APIError: If the blend is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/data-blending/blends/{blend_id}"
        with (
            api_error_handler(endpoint, context_404="Blend not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_blend.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                blend_id=blend_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Blend not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )


class BlendsResource:
    """Synchronous resource adapter for Data Blending operations.

    A *blend* combines several data sources into one queryable table. There are two
    kinds, fixed at creation and named by ``blend_type``:

    - ``"union"`` stacks rows from each source under a shared set of blend fields.
    - ``"join"`` joins the sources on shared fields, with one primary table
      (``config.query_table``) and one :class:`BlendJoin` per additional source.

    A blend is described by two things. ``blended_data_sources`` lists the sources it
    draws on, and ``config`` maps each source's native fields onto the blend's own
    fields — and, for a join blend, says how the sources are joined.

    New data sources have no id yet, so a create request names each one with a
    ``blend_data_source_key``: eight lowercase alphanumerics that every field and join
    reference in the same request points at. On update, sources that already exist are
    addressed by ``blend_data_source_id`` instead, and a single update body may
    legitimately mix the two.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Note:
        Requests and responses are not the same shape. Collections are sent as bare
        lists and come back wrapped in an object with an ``items`` attribute — at every
        level, so a round trip reads ``blend.config.fields.items``,
        ``blend.blended_data_sources.items`` and ``join.conditions.items``. The response
        also drops ``blend_data_source_key`` and adds ``blend_field_type`` and
        ``blend_field_data_type``, which upstream infers from the mapped fields. A blend
        therefore cannot be read back and resent unchanged; it has to be translated.

    Note:
        :meth:`list` returns summaries, not whole blends. A :class:`BlendListItemOutput`
        has no ``config`` and a reduced data-source shape. Call :meth:`get` for a
        blend's fields and joins.

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> for summary in client.blends.list(team_id=12345):
        ...     print(summary.blend_id, summary.display_name, summary.type_)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the BlendsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        *,
        blend_type: GetTeamBlendsType | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendSummaryList:
        """List the blends defined for a team.

        This endpoint is not paginated: it answers with every matching blend in one
        response, so there is no page size to choose and no cursor to follow.

        Args:
            team_id: The unique identifier of the team.
            blend_type: Only return blends of this kind, ``"join"`` or ``"union"``.
                Sent as the ``type`` query parameter; omitted entirely when not given,
                which returns both kinds.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[BlendListItemOutput]: The team's blends. Empty when it has none.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Note:
            The summaries carry no ``config``. Call :meth:`get` for a blend's fields
            and joins.

        Example:
            >>> for summary in client.blends.list(team_id=12345, blend_type="join"):
            ...     print(f"{summary.blend_id}: {summary.display_name}")
        """
        endpoint = f"/teams/{team_id}/data-blending/blends"
        with (
            api_error_handler(endpoint, context_400="Invalid blend list query"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_team_blends.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                type_=blend_type if blend_type is not None else UNSET,
            )
            if response.status_code == 200:
                return _list_items(cast(BlendListResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid blend list query",
                headers=response.headers,
                raw_body=response.content,
            )

    def get(
        self,
        team_id: int,
        blend_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendOutput:
        """Retrieve a single blend, including its full configuration.

        Args:
            team_id: The unique identifier of the team.
            blend_id: The unique identifier of the blend.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            BlendOutput: The blend, with its data sources and configuration.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the blend is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Note:
            Everything nested here is wrapped: the sources are at
            ``blend.blended_data_sources.items``, the fields at
            ``blend.config.fields.items`` and, on a join blend, the joins at
            ``blend.config.joins.items``.

        Example:
            >>> blend = client.blends.get(team_id=12345, blend_id=569)
            >>> print(blend.display_name, blend.type_)
            >>> for field in blend.config.fields.items:
            ...     print(field.blend_field_name, field.blend_field_type)
        """
        endpoint = f"/teams/{team_id}/data-blending/blends/{blend_id}"
        with (
            api_error_handler(endpoint, context_404="Blend not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_blend.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                blend_id=blend_id,
            )
            if response.status_code == 200:
                return cast(BlendResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Blend not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def create(
        self,
        team_id: int,
        display_name: str,
        blend_type: BlendCreateRequestType,
        blended_data_sources: BlendedDataSourceInputList,
        config: BlendConfig,
        *,
        description: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendOutput:
        """Create a blend.

        The API answers ``201 Created`` and returns the persisted blend, including the
        ``blend_id`` and ``blend_uuid`` it assigned and the ``blend_data_source_id`` it
        gave each source.

        Because none of the sources exist yet, each one is named by a
        ``blend_data_source_key`` — exactly eight lowercase alphanumerics — and every
        field and join reference in ``config`` points at that key rather than at an id.

        Args:
            team_id: The unique identifier of the team.
            display_name: User-facing name shown in the UI.
            blend_type: ``"union"`` to stack rows, ``"join"`` to join sources on shared
                fields. Sent as ``type`` and returned as ``.type_``. This cannot be
                changed later — :meth:`update` does not accept it.
            blended_data_sources: The data sources the blend draws on.
            config: Field mappings, and for a join blend the primary table and joins.
                A union blend sets ``fields`` only.
            description: Free-text description of the blend.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            BlendOutput: The created blend.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the blend is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Note:
            A rejected blend comes back as HTTP 400, not 422 — this domain documents no
            422 at all. Nothing in the SDK checks that a ``union`` blend omits ``joins``
            or that a ``join`` blend supplies ``query_table``; upstream is what rejects
            those, and it does so with a 400.

        Example:
            >>> from supermetrics import (
            ...     BlendConfig,
            ...     BlendDatasourceFieldRef,
            ...     BlendedDataSourceInput,
            ...     BlendField,
            ... )
            >>> source = BlendedDataSourceInput(
            ...     data_source_id="GA4",
            ...     blend_data_source_id=None,
            ...     blend_data_source_key="abcd1234",
            ...     report_type=None,
            ...     report_type_settings=[],
            ...     display_name="Google Analytics 4",
            ... )
            >>> config = BlendConfig(
            ...     fields=[
            ...         BlendField(
            ...             blend_field_name="impressions",
            ...             blend_field_display_name="Impressions",
            ...             blend_datasource_fields=[
            ...                 BlendDatasourceFieldRef(
            ...                     blend_data_source_key="abcd1234",
            ...                     datasource_field_name="Impressions",
            ...                     field_source="standard",
            ...                 )
            ...             ],
            ...         )
            ...     ],
            ... )
            >>> blend = client.blends.create(
            ...     team_id=12345,
            ...     display_name="GA4 impressions",
            ...     blend_type="union",
            ...     blended_data_sources=[source],
            ...     config=config,
            ... )
            >>> print(blend.blend_id)
        """
        endpoint = f"/teams/{team_id}/data-blending/blends"
        with (
            api_error_handler(endpoint, context_400="Invalid blend definition"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = BlendCreateRequest(
                type_=blend_type,
                display_name=display_name,
                blended_data_sources=blended_data_sources,
                config=config,
                description=description if description is not None else UNSET,
            )
            response = create_blend.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 201:
                return cast(BlendResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found or you do not have access to it",
                bad_request_msg="Invalid blend definition",
                headers=response.headers,
                raw_body=response.content,
            )

    def update(
        self,
        team_id: int,
        blend_id: int,
        display_name: str,
        blended_data_sources: BlendedDataSourceInputList,
        config: BlendConfig,
        *,
        description: str | None = None,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> BlendOutput:
        """Replace an existing blend.

        This is a whole-object replace: there is no PATCH endpoint. ``display_name``,
        ``blended_data_sources`` and ``config`` are required and are resent in full on
        every call, so a source left out of ``blended_data_sources`` or a field left out
        of ``config`` is dropped from the blend. ``description`` is the only optional
        field; omit it and no ``description`` key is sent.

        Sources that already exist are addressed by ``blend_data_source_id``; sources
        being added in the same call have no id yet and are named by a fresh
        ``blend_data_source_key``. One body may carry both.

        Args:
            team_id: The unique identifier of the team.
            blend_id: The unique identifier of the blend to replace.
            display_name: User-facing name shown in the UI.
            blended_data_sources: The complete set of sources the blend draws on. A
                source left out of this list is removed from the blend.
            config: Field mappings, and for a join blend the primary table and joins.
            description: Free-text description of the blend. Omit it to send no
                ``description`` key.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``, ``Sm-App-Id``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            BlendOutput: The updated blend.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the blend is rejected or not found (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Note:
            ``blend_type`` is deliberately absent. Upstream states a blend's kind cannot
            be changed after creation and the request body does not carry it, so unlike
            most update methods this one is not :meth:`create` with an id attached.

        Example:
            >>> current = client.blends.get(team_id=12345, blend_id=569)
            >>> updated = client.blends.update(
            ...     team_id=12345,
            ...     blend_id=569,
            ...     display_name="GA4 impressions, revised",
            ...     blended_data_sources=[source],
            ...     config=config,
            ...     description=current.description,
            ... )
        """
        endpoint = f"/teams/{team_id}/data-blending/blends/{blend_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid blend definition",
                context_404="Blend not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = BlendUpdateRequest(
                display_name=display_name,
                blended_data_sources=blended_data_sources,
                config=config,
                description=description if description is not None else UNSET,
            )
            response = update_blend.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                blend_id=blend_id,
                body=request,
            )
            if response.status_code == 200:
                return cast(BlendResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Blend not found or you do not have access to it",
                bad_request_msg="Invalid blend definition",
                headers=response.headers,
                raw_body=response.content,
            )

    def delete(
        self,
        team_id: int,
        blend_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        """Delete a blend.

        Args:
            team_id: The unique identifier of the team.
            blend_id: The unique identifier of the blend to delete.
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
            APIError: If the blend is not found or API error (HTTP 400, 403, 404, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.blends.delete(team_id=12345, blend_id=569)
        """
        endpoint = f"/teams/{team_id}/data-blending/blends/{blend_id}"
        with (
            api_error_handler(endpoint, context_404="Blend not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_blend.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                blend_id=blend_id,
            )
            if response.status_code == 204:
                return None
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Blend not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )
