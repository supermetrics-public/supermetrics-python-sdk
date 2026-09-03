from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_queries_response_401 import ListQueriesResponse401
from ...models.list_queries_response_422 import ListQueriesResponse422
from ...models.list_queries_response_429 import ListQueriesResponse429
from ...models.list_queries_response_500 import ListQueriesResponse500
from ...models.query_list_response import QueryListResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/queries",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | ListQueriesResponse401
    | ListQueriesResponse422
    | ListQueriesResponse429
    | ListQueriesResponse500
    | QueryListResponse
    | None
):
    if response.status_code == 200:
        response_200 = QueryListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListQueriesResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = ListQueriesResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ListQueriesResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListQueriesResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | ListQueriesResponse401
    | ListQueriesResponse422
    | ListQueriesResponse429
    | ListQueriesResponse500
    | QueryListResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | ListQueriesResponse401
    | ListQueriesResponse422
    | ListQueriesResponse429
    | ListQueriesResponse500
    | QueryListResponse
]:
    """List queries

     List queries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListQueriesResponse401 | ListQueriesResponse422 | ListQueriesResponse429 | ListQueriesResponse500 | QueryListResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | ListQueriesResponse401
    | ListQueriesResponse422
    | ListQueriesResponse429
    | ListQueriesResponse500
    | QueryListResponse
    | None
):
    """List queries

     List queries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListQueriesResponse401 | ListQueriesResponse422 | ListQueriesResponse429 | ListQueriesResponse500 | QueryListResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | ListQueriesResponse401
    | ListQueriesResponse422
    | ListQueriesResponse429
    | ListQueriesResponse500
    | QueryListResponse
]:
    """List queries

     List queries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListQueriesResponse401 | ListQueriesResponse422 | ListQueriesResponse429 | ListQueriesResponse500 | QueryListResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | ListQueriesResponse401
    | ListQueriesResponse422
    | ListQueriesResponse429
    | ListQueriesResponse500
    | QueryListResponse
    | None
):
    """List queries

     List queries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListQueriesResponse401 | ListQueriesResponse422 | ListQueriesResponse429 | ListQueriesResponse500 | QueryListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
