from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.import_table_group_body import ImportTableGroupBody
from ...models.import_table_group_response_400 import ImportTableGroupResponse400
from ...models.import_table_group_response_401 import ImportTableGroupResponse401
from ...models.import_table_group_response_404 import ImportTableGroupResponse404
from ...models.import_table_group_response_409 import ImportTableGroupResponse409
from ...models.import_table_group_response_422 import ImportTableGroupResponse422
from ...models.import_table_group_response_429 import ImportTableGroupResponse429
from ...models.import_table_group_response_500 import ImportTableGroupResponse500
from ...models.table_group_write_response import TableGroupWriteResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ImportTableGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/enterprise/v2/table/group/import",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ImportTableGroupResponse400
    | ImportTableGroupResponse401
    | ImportTableGroupResponse404
    | ImportTableGroupResponse409
    | ImportTableGroupResponse422
    | ImportTableGroupResponse429
    | ImportTableGroupResponse500
    | TableGroupWriteResponse
    | None
):
    if response.status_code == 201:
        response_201 = TableGroupWriteResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ImportTableGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ImportTableGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ImportTableGroupResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ImportTableGroupResponse409.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ImportTableGroupResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ImportTableGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ImportTableGroupResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ImportTableGroupResponse400
    | ImportTableGroupResponse401
    | ImportTableGroupResponse404
    | ImportTableGroupResponse409
    | ImportTableGroupResponse422
    | ImportTableGroupResponse429
    | ImportTableGroupResponse500
    | TableGroupWriteResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ImportTableGroupBody,
) -> Response[
    ImportTableGroupResponse400
    | ImportTableGroupResponse401
    | ImportTableGroupResponse404
    | ImportTableGroupResponse409
    | ImportTableGroupResponse422
    | ImportTableGroupResponse429
    | ImportTableGroupResponse500
    | TableGroupWriteResponse
]:
    """Import table group

     Create a new table group from a data model.

    Args:
        body (ImportTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImportTableGroupResponse400 | ImportTableGroupResponse401 | ImportTableGroupResponse404 | ImportTableGroupResponse409 | ImportTableGroupResponse422 | ImportTableGroupResponse429 | ImportTableGroupResponse500 | TableGroupWriteResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ImportTableGroupBody,
) -> (
    ImportTableGroupResponse400
    | ImportTableGroupResponse401
    | ImportTableGroupResponse404
    | ImportTableGroupResponse409
    | ImportTableGroupResponse422
    | ImportTableGroupResponse429
    | ImportTableGroupResponse500
    | TableGroupWriteResponse
    | None
):
    """Import table group

     Create a new table group from a data model.

    Args:
        body (ImportTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImportTableGroupResponse400 | ImportTableGroupResponse401 | ImportTableGroupResponse404 | ImportTableGroupResponse409 | ImportTableGroupResponse422 | ImportTableGroupResponse429 | ImportTableGroupResponse500 | TableGroupWriteResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ImportTableGroupBody,
) -> Response[
    ImportTableGroupResponse400
    | ImportTableGroupResponse401
    | ImportTableGroupResponse404
    | ImportTableGroupResponse409
    | ImportTableGroupResponse422
    | ImportTableGroupResponse429
    | ImportTableGroupResponse500
    | TableGroupWriteResponse
]:
    """Import table group

     Create a new table group from a data model.

    Args:
        body (ImportTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImportTableGroupResponse400 | ImportTableGroupResponse401 | ImportTableGroupResponse404 | ImportTableGroupResponse409 | ImportTableGroupResponse422 | ImportTableGroupResponse429 | ImportTableGroupResponse500 | TableGroupWriteResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ImportTableGroupBody,
) -> (
    ImportTableGroupResponse400
    | ImportTableGroupResponse401
    | ImportTableGroupResponse404
    | ImportTableGroupResponse409
    | ImportTableGroupResponse422
    | ImportTableGroupResponse429
    | ImportTableGroupResponse500
    | TableGroupWriteResponse
    | None
):
    """Import table group

     Create a new table group from a data model.

    Args:
        body (ImportTableGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImportTableGroupResponse400 | ImportTableGroupResponse401 | ImportTableGroupResponse404 | ImportTableGroupResponse409 | ImportTableGroupResponse422 | ImportTableGroupResponse429 | ImportTableGroupResponse500 | TableGroupWriteResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
