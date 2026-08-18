from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_data_source_connection_request import CreateDataSourceConnectionRequest
from ...models.create_data_source_connection_response import CreateDataSourceConnectionResponse
from ...models.create_data_source_connection_response_400 import CreateDataSourceConnectionResponse400
from ...models.create_data_source_connection_response_401 import CreateDataSourceConnectionResponse401
from ...models.create_data_source_connection_response_403 import CreateDataSourceConnectionResponse403
from ...models.create_data_source_connection_response_422 import CreateDataSourceConnectionResponse422
from ...models.create_data_source_connection_response_429 import CreateDataSourceConnectionResponse429
from ...models.create_data_source_connection_response_500 import CreateDataSourceConnectionResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: CreateDataSourceConnectionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/data-source-connections".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateDataSourceConnectionResponse
    | CreateDataSourceConnectionResponse400
    | CreateDataSourceConnectionResponse401
    | CreateDataSourceConnectionResponse403
    | CreateDataSourceConnectionResponse422
    | CreateDataSourceConnectionResponse429
    | CreateDataSourceConnectionResponse500
    | None
):
    if response.status_code == 201:
        response_201 = CreateDataSourceConnectionResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateDataSourceConnectionResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateDataSourceConnectionResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CreateDataSourceConnectionResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = CreateDataSourceConnectionResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateDataSourceConnectionResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateDataSourceConnectionResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateDataSourceConnectionResponse
    | CreateDataSourceConnectionResponse400
    | CreateDataSourceConnectionResponse401
    | CreateDataSourceConnectionResponse403
    | CreateDataSourceConnectionResponse422
    | CreateDataSourceConnectionResponse429
    | CreateDataSourceConnectionResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateDataSourceConnectionRequest,
) -> Response[
    CreateDataSourceConnectionResponse
    | CreateDataSourceConnectionResponse400
    | CreateDataSourceConnectionResponse401
    | CreateDataSourceConnectionResponse403
    | CreateDataSourceConnectionResponse422
    | CreateDataSourceConnectionResponse429
    | CreateDataSourceConnectionResponse500
]:
    """Create data source connection

     Creates a data source connection for a Hub transfer. This endpoint establishes a connection
    between a data source and a destination for use in data warehouse transfers.

    **Returns:** Connection object with connection ID and optional OAuth URLs.

    **Important Notes:**
    - The API key must have `dwh_transfers_write` scope
    - Connection credentials are encrypted and stored securely
    - Some data sources may require OAuth authentication (check `login_url` in response)
    - The connection must be created before setting up transfers

    **Legacy Reference:** `POST /data_warehouse/transfer_configuration/connect`

    Args:
        team_id (int):
        body (CreateDataSourceConnectionRequest): Connection configuration specifying the data
            source and destination for a Hub transfer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDataSourceConnectionResponse | CreateDataSourceConnectionResponse400 | CreateDataSourceConnectionResponse401 | CreateDataSourceConnectionResponse403 | CreateDataSourceConnectionResponse422 | CreateDataSourceConnectionResponse429 | CreateDataSourceConnectionResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateDataSourceConnectionRequest,
) -> (
    CreateDataSourceConnectionResponse
    | CreateDataSourceConnectionResponse400
    | CreateDataSourceConnectionResponse401
    | CreateDataSourceConnectionResponse403
    | CreateDataSourceConnectionResponse422
    | CreateDataSourceConnectionResponse429
    | CreateDataSourceConnectionResponse500
    | None
):
    """Create data source connection

     Creates a data source connection for a Hub transfer. This endpoint establishes a connection
    between a data source and a destination for use in data warehouse transfers.

    **Returns:** Connection object with connection ID and optional OAuth URLs.

    **Important Notes:**
    - The API key must have `dwh_transfers_write` scope
    - Connection credentials are encrypted and stored securely
    - Some data sources may require OAuth authentication (check `login_url` in response)
    - The connection must be created before setting up transfers

    **Legacy Reference:** `POST /data_warehouse/transfer_configuration/connect`

    Args:
        team_id (int):
        body (CreateDataSourceConnectionRequest): Connection configuration specifying the data
            source and destination for a Hub transfer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDataSourceConnectionResponse | CreateDataSourceConnectionResponse400 | CreateDataSourceConnectionResponse401 | CreateDataSourceConnectionResponse403 | CreateDataSourceConnectionResponse422 | CreateDataSourceConnectionResponse429 | CreateDataSourceConnectionResponse500
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateDataSourceConnectionRequest,
) -> Response[
    CreateDataSourceConnectionResponse
    | CreateDataSourceConnectionResponse400
    | CreateDataSourceConnectionResponse401
    | CreateDataSourceConnectionResponse403
    | CreateDataSourceConnectionResponse422
    | CreateDataSourceConnectionResponse429
    | CreateDataSourceConnectionResponse500
]:
    """Create data source connection

     Creates a data source connection for a Hub transfer. This endpoint establishes a connection
    between a data source and a destination for use in data warehouse transfers.

    **Returns:** Connection object with connection ID and optional OAuth URLs.

    **Important Notes:**
    - The API key must have `dwh_transfers_write` scope
    - Connection credentials are encrypted and stored securely
    - Some data sources may require OAuth authentication (check `login_url` in response)
    - The connection must be created before setting up transfers

    **Legacy Reference:** `POST /data_warehouse/transfer_configuration/connect`

    Args:
        team_id (int):
        body (CreateDataSourceConnectionRequest): Connection configuration specifying the data
            source and destination for a Hub transfer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDataSourceConnectionResponse | CreateDataSourceConnectionResponse400 | CreateDataSourceConnectionResponse401 | CreateDataSourceConnectionResponse403 | CreateDataSourceConnectionResponse422 | CreateDataSourceConnectionResponse429 | CreateDataSourceConnectionResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateDataSourceConnectionRequest,
) -> (
    CreateDataSourceConnectionResponse
    | CreateDataSourceConnectionResponse400
    | CreateDataSourceConnectionResponse401
    | CreateDataSourceConnectionResponse403
    | CreateDataSourceConnectionResponse422
    | CreateDataSourceConnectionResponse429
    | CreateDataSourceConnectionResponse500
    | None
):
    """Create data source connection

     Creates a data source connection for a Hub transfer. This endpoint establishes a connection
    between a data source and a destination for use in data warehouse transfers.

    **Returns:** Connection object with connection ID and optional OAuth URLs.

    **Important Notes:**
    - The API key must have `dwh_transfers_write` scope
    - Connection credentials are encrypted and stored securely
    - Some data sources may require OAuth authentication (check `login_url` in response)
    - The connection must be created before setting up transfers

    **Legacy Reference:** `POST /data_warehouse/transfer_configuration/connect`

    Args:
        team_id (int):
        body (CreateDataSourceConnectionRequest): Connection configuration specifying the data
            source and destination for a Hub transfer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDataSourceConnectionResponse | CreateDataSourceConnectionResponse400 | CreateDataSourceConnectionResponse401 | CreateDataSourceConnectionResponse403 | CreateDataSourceConnectionResponse422 | CreateDataSourceConnectionResponse429 | CreateDataSourceConnectionResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
