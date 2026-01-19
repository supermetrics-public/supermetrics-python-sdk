from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.data_query import DataQuery
from ...models.data_response import DataResponse
from ...models.get_data_response_400 import GetDataResponse400
from ...models.get_data_response_401 import GetDataResponse401
from ...models.get_data_response_403 import GetDataResponse403
from ...models.get_data_response_422 import GetDataResponse422
from ...models.get_data_response_429 import GetDataResponse429
from ...models.get_data_response_500 import GetDataResponse500
from typing import cast



def _get_kwargs(
    *,
    json: DataQuery,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_json = json.to_dict()
    params.update(json_json)



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/query/data/json",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500 | None:
    if response.status_code == 200:
        response_200 = DataResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = GetDataResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = GetDataResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = GetDataResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 422:
        response_422 = GetDataResponse422.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = GetDataResponse429.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = GetDataResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json: DataQuery,

) -> Response[DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500]:
    """ Query data

     Execute a query to retrieve data from a specified data source

    Args:
        json (DataQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500]
     """


    kwargs = _get_kwargs(
        json=json,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    json: DataQuery,

) -> DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500 | None:
    """ Query data

     Execute a query to retrieve data from a specified data source

    Args:
        json (DataQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500
     """


    return sync_detailed(
        client=client,
json=json,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json: DataQuery,

) -> Response[DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500]:
    """ Query data

     Execute a query to retrieve data from a specified data source

    Args:
        json (DataQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500]
     """


    kwargs = _get_kwargs(
        json=json,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    json: DataQuery,

) -> DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500 | None:
    """ Query data

     Execute a query to retrieve data from a specified data source

    Args:
        json (DataQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataResponse | GetDataResponse400 | GetDataResponse401 | GetDataResponse403 | GetDataResponse422 | GetDataResponse429 | GetDataResponse500
     """


    return (await asyncio_detailed(
        client=client,
json=json,

    )).parsed
