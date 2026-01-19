from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_accounts_json import GetAccountsJson
from ...models.get_accounts_response_200 import GetAccountsResponse200
from ...models.get_accounts_response_400 import GetAccountsResponse400
from ...models.get_accounts_response_401 import GetAccountsResponse401
from ...models.get_accounts_response_403 import GetAccountsResponse403
from ...models.get_accounts_response_422 import GetAccountsResponse422
from ...models.get_accounts_response_429 import GetAccountsResponse429
from ...models.get_accounts_response_500 import GetAccountsResponse500
from typing import cast



def _get_kwargs(
    *,
    json: GetAccountsJson,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_json = json.to_dict()
    params.update(json_json)



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/query/accounts",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500 | None:
    if response.status_code == 200:
        response_200 = GetAccountsResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = GetAccountsResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = GetAccountsResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = GetAccountsResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 422:
        response_422 = GetAccountsResponse422.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = GetAccountsResponse429.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = GetAccountsResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json: GetAccountsJson,

) -> Response[GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500]:
    """ Get accounts

     Retrieve a list of available data source logins (authentications) and their accounts

    Args:
        json (GetAccountsJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500]
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
    json: GetAccountsJson,

) -> GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500 | None:
    """ Get accounts

     Retrieve a list of available data source logins (authentications) and their accounts

    Args:
        json (GetAccountsJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500
     """


    return sync_detailed(
        client=client,
json=json,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json: GetAccountsJson,

) -> Response[GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500]:
    """ Get accounts

     Retrieve a list of available data source logins (authentications) and their accounts

    Args:
        json (GetAccountsJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500]
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
    json: GetAccountsJson,

) -> GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500 | None:
    """ Get accounts

     Retrieve a list of available data source logins (authentications) and their accounts

    Args:
        json (GetAccountsJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAccountsResponse200 | GetAccountsResponse400 | GetAccountsResponse401 | GetAccountsResponse403 | GetAccountsResponse422 | GetAccountsResponse429 | GetAccountsResponse500
     """


    return (await asyncio_detailed(
        client=client,
json=json,

    )).parsed
