from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_data_source_login_response_200 import GetDataSourceLoginResponse200
from ...models.get_data_source_login_response_404 import GetDataSourceLoginResponse404
from ...models.get_data_source_login_response_500 import GetDataSourceLoginResponse500
from ...types import Response


def _get_kwargs(
    login_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/ds/login/{login_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500 | None
):
    if response.status_code == 200:
        response_200 = GetDataSourceLoginResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = GetDataSourceLoginResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetDataSourceLoginResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500
]:
    """Get login

     Retrieve details of a specific data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500]
    """

    kwargs = _get_kwargs(
        login_id=login_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500 | None
):
    """Get login

     Retrieve details of a specific data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500
    """

    return sync_detailed(
        login_id=login_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500
]:
    """Get login

     Retrieve details of a specific data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500]
    """

    kwargs = _get_kwargs(
        login_id=login_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500 | None
):
    """Get login

     Retrieve details of a specific data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetDataSourceLoginResponse200 | GetDataSourceLoginResponse404 | GetDataSourceLoginResponse500
    """

    return (
        await asyncio_detailed(
            login_id=login_id,
            client=client,
        )
    ).parsed
