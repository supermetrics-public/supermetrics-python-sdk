from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_login_links_response_200 import ListLoginLinksResponse200
from ...models.list_login_links_response_401 import ListLoginLinksResponse401
from ...models.list_login_links_response_422 import ListLoginLinksResponse422
from ...models.list_login_links_response_429 import ListLoginLinksResponse429
from ...models.list_login_links_response_500 import ListLoginLinksResponse500
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ds/login/links",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500 | None:
    if response.status_code == 200:
        response_200 = ListLoginLinksResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = ListLoginLinksResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 422:
        response_422 = ListLoginLinksResponse422.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = ListLoginLinksResponse429.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ListLoginLinksResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500]:
    """ List login links

     List all data source login links

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500]
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

) -> ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500 | None:
    """ List login links

     List all data source login links

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500]:
    """ List login links

     List all data source login links

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500]
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

) -> ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500 | None:
    """ List login links

     List all data source login links

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListLoginLinksResponse200 | ListLoginLinksResponse401 | ListLoginLinksResponse422 | ListLoginLinksResponse429 | ListLoginLinksResponse500
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
