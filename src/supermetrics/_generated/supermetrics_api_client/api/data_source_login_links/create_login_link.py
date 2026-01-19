from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_login_link_body import CreateLoginLinkBody
from ...models.create_login_link_response_401 import CreateLoginLinkResponse401
from ...models.create_login_link_response_403 import CreateLoginLinkResponse403
from ...models.create_login_link_response_422 import CreateLoginLinkResponse422
from ...models.create_login_link_response_429 import CreateLoginLinkResponse429
from ...models.create_login_link_response_500 import CreateLoginLinkResponse500
from ...models.login_link_response import LoginLinkResponse
from typing import cast



def _get_kwargs(
    *,
    body: CreateLoginLinkBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/ds/login/link",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse | None:
    if response.status_code == 201:
        response_201 = LoginLinkResponse.from_dict(response.json())



        return response_201

    if response.status_code == 401:
        response_401 = CreateLoginLinkResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = CreateLoginLinkResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 422:
        response_422 = CreateLoginLinkResponse422.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = CreateLoginLinkResponse429.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = CreateLoginLinkResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLoginLinkBody,

) -> Response[CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse]:
    """ Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse]
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
    body: CreateLoginLinkBody,

) -> CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse | None:
    """ Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLoginLinkBody,

) -> Response[CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse]:
    """ Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateLoginLinkBody,

) -> CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse | None:
    """ Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateLoginLinkResponse401 | CreateLoginLinkResponse403 | CreateLoginLinkResponse422 | CreateLoginLinkResponse429 | CreateLoginLinkResponse500 | LoginLinkResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
