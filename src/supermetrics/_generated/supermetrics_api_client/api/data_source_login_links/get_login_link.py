from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_login_link_response_401 import GetLoginLinkResponse401
from ...models.get_login_link_response_404 import GetLoginLinkResponse404
from ...models.get_login_link_response_422 import GetLoginLinkResponse422
from ...models.get_login_link_response_429 import GetLoginLinkResponse429
from ...models.get_login_link_response_500 import GetLoginLinkResponse500
from ...models.login_link_response import LoginLinkResponse
from typing import cast



def _get_kwargs(
    link_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ds/login/link/{link_id}".format(link_id=link_id,),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse | None:
    if response.status_code == 200:
        response_200 = LoginLinkResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = GetLoginLinkResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = GetLoginLinkResponse404.from_dict(response.json())



        return response_404

    if response.status_code == 422:
        response_422 = GetLoginLinkResponse422.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = GetLoginLinkResponse429.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = GetLoginLinkResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    link_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse]:
    """ Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse]
     """


    kwargs = _get_kwargs(
        link_id=link_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    link_id: str,
    *,
    client: AuthenticatedClient,

) -> GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse | None:
    """ Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse
     """


    return sync_detailed(
        link_id=link_id,
client=client,

    ).parsed

async def asyncio_detailed(
    link_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse]:
    """ Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse]
     """


    kwargs = _get_kwargs(
        link_id=link_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    link_id: str,
    *,
    client: AuthenticatedClient,

) -> GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse | None:
    """ Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetLoginLinkResponse401 | GetLoginLinkResponse404 | GetLoginLinkResponse422 | GetLoginLinkResponse429 | GetLoginLinkResponse500 | LoginLinkResponse
     """


    return (await asyncio_detailed(
        link_id=link_id,
client=client,

    )).parsed
