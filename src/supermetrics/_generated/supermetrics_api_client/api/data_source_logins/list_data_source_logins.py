from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_data_source_logins_response_200 import ListDataSourceLoginsResponse200
from ...models.list_data_source_logins_response_401 import ListDataSourceLoginsResponse401
from ...models.list_data_source_logins_response_422 import ListDataSourceLoginsResponse422
from ...models.list_data_source_logins_response_429 import ListDataSourceLoginsResponse429
from ...models.list_data_source_logins_response_500 import ListDataSourceLoginsResponse500
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ds/logins",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500 | None:
    if response.status_code == 200:
        response_200 = ListDataSourceLoginsResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = ListDataSourceLoginsResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 422:
        response_422 = ListDataSourceLoginsResponse422.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = ListDataSourceLoginsResponse429.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ListDataSourceLoginsResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500]:
    """ List logins

     Retrieve a list of all data source logins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500 | None:
    """ List logins

     Retrieve a list of all data source logins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500]:
    """ List logins

     Retrieve a list of all data source logins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500 | None:
    """ List logins

     Retrieve a list of all data source logins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDataSourceLoginsResponse200 | ListDataSourceLoginsResponse401 | ListDataSourceLoginsResponse422 | ListDataSourceLoginsResponse429 | ListDataSourceLoginsResponse500
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
