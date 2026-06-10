from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_login_link_body import CreateLoginLinkBody
from ...models.create_login_link_response_403 import CreateLoginLinkResponse403
from ...models.error_response import ErrorResponse
from ...models.login_link_response import LoginLinkResponse
from ...types import Response


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


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse | None:
    if response.status_code == 201:
        response_201 = LoginLinkResponse.from_dict(response.json())

        return response_201

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CreateLoginLinkResponse403.from_dict(response.json())

        return response_403

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
) -> Response[CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse]:
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
) -> Response[CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse]:
    """Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse]
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
) -> CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse | None:
    """Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLoginLinkBody,
) -> Response[CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse]:
    """Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateLoginLinkBody,
) -> CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse | None:
    """Create login link

     Create a new data source login link

    Args:
        body (CreateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateLoginLinkResponse403 | ErrorResponse | LoginLinkResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
