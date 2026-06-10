from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_login_link_response_404 import GetLoginLinkResponse404
from ...models.login_link_response import LoginLinkResponse
from ...types import Response


def _get_kwargs(
    link_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/ds/login/link/{link_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse | None:
    if response.status_code == 200:
        response_200 = LoginLinkResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = GetLoginLinkResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse]:
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
) -> Response[ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse]:
    """Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse]
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
) -> ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse | None:
    """Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse
    """

    return sync_detailed(
        link_id=link_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    link_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse]:
    """Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse]
    """

    kwargs = _get_kwargs(
        link_id=link_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    link_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse | None:
    """Get login link

     Get details of a specific login link

    Args:
        link_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetLoginLinkResponse404 | LoginLinkResponse
    """

    return (
        await asyncio_detailed(
            link_id=link_id,
            client=client,
        )
    ).parsed
