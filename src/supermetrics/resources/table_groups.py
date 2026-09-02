"""Table Groups resource adapter for Supermetrics Data Warehouse API."""

from __future__ import annotations

import json
from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.table_groups import (
    edit_table_group,
    export_table_group,
    import_table_group,
    list_table_groups,
)
from supermetrics._generated.supermetrics_api_client.models.edit_table_group_body import EditTableGroupBody
from supermetrics._generated.supermetrics_api_client.models.export_table_group_response_200 import (
    ExportTableGroupResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.import_table_group_body import ImportTableGroupBody
from supermetrics._generated.supermetrics_api_client.models.list_table_groups_response_200 import (
    ListTableGroupsResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.table_group import TableGroup
from supermetrics._generated.supermetrics_api_client.models.table_group_response import TableGroupResponse
from supermetrics._generated.supermetrics_api_client.types import Response as GenResponse
from supermetrics._generated.supermetrics_api_client.types import Unset
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

TableGroupList = list[TableGroup]


def _unwrap_table_group(response: object) -> TableGroup:
    """Extract a TableGroup from an import/edit response.

    The spec declares these responses as ``TableGroupResponse`` (``{meta, data}``
    envelope), but the API actually returns a flat ``{group_id, group_name, links}``
    object. The generated parser builds a ``TableGroupResponse`` whose ``data`` is
    ``UNSET`` because no ``data`` key exists in the flat response.

    Stopgap: when ``data`` is UNSET, parse the raw response body directly as a
    ``TableGroup``. Remove once the spec is corrected upstream.
    """
    resp = cast(GenResponse[object], response)
    parsed = resp.parsed
    if isinstance(parsed, TableGroupResponse) and not isinstance(parsed.data, Unset):
        return parsed.data
    return TableGroup.from_dict(json.loads(resp.content))


class TableGroupsAsyncResource:
    """Asynchronous resource adapter for Table Group operations.

    Async version of TableGroupsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> groups = await client.table_groups.list()
        >>> export = await client.table_groups.export(group_id="tg_123", version=1)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TableGroupList:
        """List all table groups available for the team.

        Async version of TableGroupsResource.list(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only.
            timeout: Timeout override for this request only.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 422, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = "/enterprise/v2/table/groups"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = await list_table_groups.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
            )
            if response.status_code == 200:
                return cast(TableGroupList, cast(ListTableGroupsResponse200, response.parsed).data)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                headers=response.headers,
                raw_body=response.content,
            )

    async def export(
        self,
        group_id: str,
        *,
        version: int,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ExportTableGroupResponse200:
        """Export a table group's data model.

        Async version of TableGroupsResource.export(). See sync version for full documentation.

        Args:
            group_id: Supermetrics table group ID (e.g. ``"tg_123"``).
            version: Data model version for the returned data.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only.
            timeout: Timeout override for this request only.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the table group is not found or API error (HTTP 404, 422, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/enterprise/v2/table/group/{group_id}/export"
        with (
            api_error_handler(endpoint, context_404="Table group not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await export_table_group.asyncio_detailed(
                group_id=group_id,
                client=cast(AuthenticatedClient, self._client),
                version=version,
            )
            if response.status_code == 200:
                return cast(ExportTableGroupResponse200, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Table group not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    async def import_(
        self,
        *,
        body: ImportTableGroupBody,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TableGroup:
        """Import (create) a new table group from a data model.

        Async version of TableGroupsResource.import_(). See sync version for full documentation.

        Args:
            body: The import payload containing version, group config, tables, and
                optionally fields.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only.
            timeout: Timeout override for this request only.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the import data is invalid (HTTP 400).
            APIError: If a name conflict occurs (HTTP 409) or other API error
                (HTTP 404, 422, 429).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = "/enterprise/v2/table/group/import"
        with (
            api_error_handler(endpoint, context_400="Invalid table group import data"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await import_table_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                body=body,
            )
            if response.status_code == 201:
                return _unwrap_table_group(response)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid table group import data",
                headers=response.headers,
                raw_body=response.content,
            )

    async def edit(
        self,
        group_id: str,
        *,
        version: int,
        body: EditTableGroupBody,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TableGroup:
        """Update an existing table group (full replace).

        Async version of TableGroupsResource.edit(). See sync version for full documentation.

        Args:
            group_id: Supermetrics table group ID (e.g. ``"tg_123"``).
            version: Data model version for the request data.
            body: The edit payload containing group config, tables, and optionally
                fields.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only.
            timeout: Timeout override for this request only.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the edit data is invalid (HTTP 400).
            APIError: If the table group is not found or API error (HTTP 403, 404, 422,
                429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/enterprise/v2/table/group/{group_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid table group configuration",
                context_404="Table group not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await edit_table_group.asyncio_detailed(
                group_id=group_id,
                client=cast(AuthenticatedClient, self._client),
                body=body,
                version=version,
            )
            if response.status_code == 200:
                return _unwrap_table_group(response)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Table group not found or you do not have access to it",
                bad_request_msg="Invalid table group configuration",
                headers=response.headers,
                raw_body=response.content,
            )


class TableGroupsResource:
    """Synchronous resource adapter for Table Group operations.

    Provides a clean, Pythonic interface for managing table groups — the schema
    definitions that control how data is structured in the warehouse. Table groups
    define tables, fields, and their mappings for each data source.

    The team identity comes from the API key, not a path parameter, so no
    ``team_id`` is needed on these methods.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> groups = client.table_groups.list()
        >>> export = client.table_groups.export(group_id="tg_123", version=1)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the TableGroupsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TableGroupList:
        """List all table groups available for the team.

        Returns every table group configured for the team. Each item includes
        the ``group_id`` (string, e.g. ``"tg_123"``), ``schema_id`` (numeric,
        used as the ``schema_id`` parameter when creating a transfer), and the
        group's display name.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[TableGroup]: The team's table groups.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the API returns a server error (HTTP 422, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> groups = client.table_groups.list()
            >>> for g in groups:
            ...     print(f"{g.group_id} (schema {g.schema_id}): {g.name}")
        """
        endpoint = "/enterprise/v2/table/groups"
        with api_error_handler(endpoint), request_options(auth_token=auth_token, headers=headers, timeout=timeout):
            response = list_table_groups.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
            )
            if response.status_code == 200:
                return cast(TableGroupList, cast(ListTableGroupsResponse200, response.parsed).data)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                headers=response.headers,
                raw_body=response.content,
            )

    def export(
        self,
        group_id: str,
        *,
        version: int,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> ExportTableGroupResponse200:
        """Export a table group's data model.

        Returns the full definition of a table group including its tables and
        field mappings. The natural workflow is export → edit locally → PUT back
        via :meth:`edit`.

        The response is returned as-is (not unwrapped) because it has multiple
        top-level fields: ``version``, ``group``, ``tables``, and ``fields``.

        Args:
            group_id: Supermetrics table group ID (e.g. ``"tg_123"``).
            version: Data model version for the returned data.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            ExportTableGroupResponse200: The exported data model with version,
            group metadata, tables, and fields.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the table group is not found or API error (HTTP 404, 422, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> export = client.table_groups.export(group_id="tg_123", version=1)
            >>> print(f"Group: {export.group.group_name}")
            >>> for table in export.tables:
            ...     print(f"  Table: {table.table_name} ({len(table.fields)} fields)")
        """
        endpoint = f"/enterprise/v2/table/group/{group_id}/export"
        with (
            api_error_handler(endpoint, context_404="Table group not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = export_table_group.sync_detailed(
                group_id=group_id,
                client=cast(AuthenticatedClient, self._client),
                version=version,
            )
            if response.status_code == 200:
                return cast(ExportTableGroupResponse200, response.parsed)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Table group not found or you do not have access to it",
                headers=response.headers,
                raw_body=response.content,
            )

    def import_(
        self,
        *,
        body: ImportTableGroupBody,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TableGroup:
        """Import (create) a new table group from a data model.

        Creates a new table group with the provided definition. The ``body``
        must include ``version``, ``group`` (name, data source, prefix), and
        ``tables`` (with their fields). Optionally include ``fields`` for
        field-level target name mappings.

        Args:
            body: The import payload. Build with ``ImportTableGroupBody``:
                ``version`` (int), ``group`` (``TableGroupImport``),
                ``tables`` (list of ``TableDefinition``), and optionally
                ``fields`` (list of ``FieldDefinition``).
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TableGroup: The created table group with its assigned ``group_id``
            and ``schema_id``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the import data is invalid (HTTP 400).
            APIError: If a name conflict occurs (HTTP 409) or other API error
                (HTTP 404, 422, 429).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics._generated.supermetrics_api_client.models.import_table_group_body import (
            ...     ImportTableGroupBody,
            ... )
            >>> from supermetrics._generated.supermetrics_api_client.models.table_group_import import TableGroupImport
            >>> from supermetrics._generated.supermetrics_api_client.models.table_definition import TableDefinition
            >>> body = ImportTableGroupBody(
            ...     version=1,
            ...     group=TableGroupImport(group_name="My Group", ds_id="AW"),
            ...     tables=[TableDefinition(table_name="CAMPAIGNS", fields=["campaign_id", "date"])],
            ... )
            >>> created = client.table_groups.import_(body=body)
            >>> print(f"Created: {created.group_id} (schema {created.schema_id})")
        """
        endpoint = "/enterprise/v2/table/group/import"
        with (
            api_error_handler(endpoint, context_400="Invalid table group import data"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = import_table_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                body=body,
            )
            if response.status_code == 201:
                return _unwrap_table_group(response)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid table group import data",
                headers=response.headers,
                raw_body=response.content,
            )

    def edit(
        self,
        group_id: str,
        *,
        version: int,
        body: EditTableGroupBody,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TableGroup:
        """Update an existing table group (full replace).

        This is a full replacement of the table group's definition. All tables
        and fields must be provided. Omitting ``fields`` from the body clears
        all field mappings.

        The natural workflow is :meth:`export` → edit locally → :meth:`edit`.

        Args:
            group_id: Supermetrics table group ID (e.g. ``"tg_123"``).
            version: Data model version for the request data.
            body: The edit payload. Build with ``EditTableGroupBody``:
                ``group`` (``TableGroupImport``), ``tables`` (list of
                ``TableDefinition``), and optionally ``fields`` (list of
                ``FieldDefinition``).
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TableGroup: The updated table group.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If the edit data is invalid (HTTP 400).
            APIError: If the table group is not found or API error (HTTP 403, 404, 422,
                429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> from supermetrics._generated.supermetrics_api_client.models.edit_table_group_body import (
            ...     EditTableGroupBody,
            ... )
            >>> export = client.table_groups.export(group_id="tg_123", version=1)
            >>> body = EditTableGroupBody(
            ...     group=export.group,
            ...     tables=export.tables,
            ...     fields=export.fields,
            ... )
            >>> updated = client.table_groups.edit(group_id="tg_123", version=1, body=body)
        """
        endpoint = f"/enterprise/v2/table/group/{group_id}"
        with (
            api_error_handler(
                endpoint,
                context_400="Invalid table group configuration",
                context_404="Table group not found",
            ),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = edit_table_group.sync_detailed(
                group_id=group_id,
                client=cast(AuthenticatedClient, self._client),
                body=body,
                version=version,
            )
            if response.status_code == 200:
                return _unwrap_table_group(response)
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Table group not found or you do not have access to it",
                bad_request_msg="Invalid table group configuration",
                headers=response.headers,
                raw_body=response.content,
            )
