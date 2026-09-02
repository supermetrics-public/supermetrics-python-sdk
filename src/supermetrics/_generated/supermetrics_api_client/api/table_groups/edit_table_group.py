from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_table_group_body import EditTableGroupBody
from ...models.edit_table_group_response_400 import EditTableGroupResponse400
from ...models.edit_table_group_response_401 import EditTableGroupResponse401
from ...models.edit_table_group_response_403 import EditTableGroupResponse403
from ...models.edit_table_group_response_404 import EditTableGroupResponse404
from ...models.edit_table_group_response_422 import EditTableGroupResponse422
from ...models.edit_table_group_response_429 import EditTableGroupResponse429
from ...models.edit_table_group_response_500 import EditTableGroupResponse500
from ...models.table_group_write_response import TableGroupWriteResponse
from ...types import Response


def _get_kwargs(
    group_id: str,
    *,
    body: EditTableGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/enterprise/v2/table/group/{group_id}".format(
            group_id=quote(str(group_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    EditTableGroupResponse400
    | EditTableGroupResponse401
    | EditTableGroupResponse403
    | EditTableGroupResponse404
    | EditTableGroupResponse422
    | EditTableGroupResponse429
    | EditTableGroupResponse500
    | TableGroupWriteResponse
    | None
):
    if response.status_code == 200:
        response_200 = TableGroupWriteResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = EditTableGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = EditTableGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = EditTableGroupResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = EditTableGroupResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = EditTableGroupResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = EditTableGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = EditTableGroupResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    EditTableGroupResponse400
    | EditTableGroupResponse401
    | EditTableGroupResponse403
    | EditTableGroupResponse404
    | EditTableGroupResponse422
    | EditTableGroupResponse429
    | EditTableGroupResponse500
    | TableGroupWriteResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: EditTableGroupBody,
) -> Response[
    EditTableGroupResponse400
    | EditTableGroupResponse401
    | EditTableGroupResponse403
    | EditTableGroupResponse404
    | EditTableGroupResponse422
    | EditTableGroupResponse429
    | EditTableGroupResponse500
    | TableGroupWriteResponse
]:
    """Edit table group

     Update an existing table group's definition (full replace).
    The request body uses the same `{version, group, tables, fields}` structure that Import accepts and
    Export returns, so the natural workflow is export → edit → PUT.

    This is a full replace — all tables and fields must be provided. Omitting `fields` clears all field
    mappings. Tables and fields are matched to existing records by name. Renaming a table or field is
    equivalent to removing the old one and adding a new one — the old table's settings and query filter
    linkage are lost.

    The `ignore_errors` and `ds_settings` properties are not yet supported on this endpoint and will be
    rejected with 422 if present.

    Args:
        group_id (str):
        body (EditTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EditTableGroupResponse400 | EditTableGroupResponse401 | EditTableGroupResponse403 | EditTableGroupResponse404 | EditTableGroupResponse422 | EditTableGroupResponse429 | EditTableGroupResponse500 | TableGroupWriteResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: EditTableGroupBody,
) -> (
    EditTableGroupResponse400
    | EditTableGroupResponse401
    | EditTableGroupResponse403
    | EditTableGroupResponse404
    | EditTableGroupResponse422
    | EditTableGroupResponse429
    | EditTableGroupResponse500
    | TableGroupWriteResponse
    | None
):
    """Edit table group

     Update an existing table group's definition (full replace).
    The request body uses the same `{version, group, tables, fields}` structure that Import accepts and
    Export returns, so the natural workflow is export → edit → PUT.

    This is a full replace — all tables and fields must be provided. Omitting `fields` clears all field
    mappings. Tables and fields are matched to existing records by name. Renaming a table or field is
    equivalent to removing the old one and adding a new one — the old table's settings and query filter
    linkage are lost.

    The `ignore_errors` and `ds_settings` properties are not yet supported on this endpoint and will be
    rejected with 422 if present.

    Args:
        group_id (str):
        body (EditTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EditTableGroupResponse400 | EditTableGroupResponse401 | EditTableGroupResponse403 | EditTableGroupResponse404 | EditTableGroupResponse422 | EditTableGroupResponse429 | EditTableGroupResponse500 | TableGroupWriteResponse
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: EditTableGroupBody,
) -> Response[
    EditTableGroupResponse400
    | EditTableGroupResponse401
    | EditTableGroupResponse403
    | EditTableGroupResponse404
    | EditTableGroupResponse422
    | EditTableGroupResponse429
    | EditTableGroupResponse500
    | TableGroupWriteResponse
]:
    """Edit table group

     Update an existing table group's definition (full replace).
    The request body uses the same `{version, group, tables, fields}` structure that Import accepts and
    Export returns, so the natural workflow is export → edit → PUT.

    This is a full replace — all tables and fields must be provided. Omitting `fields` clears all field
    mappings. Tables and fields are matched to existing records by name. Renaming a table or field is
    equivalent to removing the old one and adding a new one — the old table's settings and query filter
    linkage are lost.

    The `ignore_errors` and `ds_settings` properties are not yet supported on this endpoint and will be
    rejected with 422 if present.

    Args:
        group_id (str):
        body (EditTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EditTableGroupResponse400 | EditTableGroupResponse401 | EditTableGroupResponse403 | EditTableGroupResponse404 | EditTableGroupResponse422 | EditTableGroupResponse429 | EditTableGroupResponse500 | TableGroupWriteResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: EditTableGroupBody,
) -> (
    EditTableGroupResponse400
    | EditTableGroupResponse401
    | EditTableGroupResponse403
    | EditTableGroupResponse404
    | EditTableGroupResponse422
    | EditTableGroupResponse429
    | EditTableGroupResponse500
    | TableGroupWriteResponse
    | None
):
    """Edit table group

     Update an existing table group's definition (full replace).
    The request body uses the same `{version, group, tables, fields}` structure that Import accepts and
    Export returns, so the natural workflow is export → edit → PUT.

    This is a full replace — all tables and fields must be provided. Omitting `fields` clears all field
    mappings. Tables and fields are matched to existing records by name. Renaming a table or field is
    equivalent to removing the old one and adding a new one — the old table's settings and query filter
    linkage are lost.

    The `ignore_errors` and `ds_settings` properties are not yet supported on this endpoint and will be
    rejected with 422 if present.

    Args:
        group_id (str):
        body (EditTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EditTableGroupResponse400 | EditTableGroupResponse401 | EditTableGroupResponse403 | EditTableGroupResponse404 | EditTableGroupResponse422 | EditTableGroupResponse429 | EditTableGroupResponse500 | TableGroupWriteResponse
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            body=body,
        )
    ).parsed
