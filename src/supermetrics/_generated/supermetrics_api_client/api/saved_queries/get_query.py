from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_query_response_401 import GetQueryResponse401
from ...models.get_query_response_404 import GetQueryResponse404
from ...models.get_query_response_422 import GetQueryResponse422
from ...models.get_query_response_429 import GetQueryResponse429
from ...models.get_query_response_500 import GetQueryResponse500
from ...models.query_response import QueryResponse
from ...types import Response


def _get_kwargs(
    query_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/query/{query_id}".format(
            query_id=quote(str(query_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | GetQueryResponse401
    | GetQueryResponse404
    | GetQueryResponse422
    | GetQueryResponse429
    | GetQueryResponse500
    | QueryResponse
    | None
):
    if response.status_code == 200:
        response_200 = QueryResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetQueryResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetQueryResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = GetQueryResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = GetQueryResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetQueryResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | GetQueryResponse401
    | GetQueryResponse404
    | GetQueryResponse422
    | GetQueryResponse429
    | GetQueryResponse500
    | QueryResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    query_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | GetQueryResponse401
    | GetQueryResponse404
    | GetQueryResponse422
    | GetQueryResponse429
    | GetQueryResponse500
    | QueryResponse
]:
    """Get query

     Get query

    Args:
        query_id (str):  Example: example.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetQueryResponse401 | GetQueryResponse404 | GetQueryResponse422 | GetQueryResponse429 | GetQueryResponse500 | QueryResponse]
    """

    kwargs = _get_kwargs(
        query_id=query_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    query_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | GetQueryResponse401
    | GetQueryResponse404
    | GetQueryResponse422
    | GetQueryResponse429
    | GetQueryResponse500
    | QueryResponse
    | None
):
    """Get query

     Get query

    Args:
        query_id (str):  Example: example.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetQueryResponse401 | GetQueryResponse404 | GetQueryResponse422 | GetQueryResponse429 | GetQueryResponse500 | QueryResponse
    """

    return sync_detailed(
        query_id=query_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    query_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | GetQueryResponse401
    | GetQueryResponse404
    | GetQueryResponse422
    | GetQueryResponse429
    | GetQueryResponse500
    | QueryResponse
]:
    """Get query

     Get query

    Args:
        query_id (str):  Example: example.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetQueryResponse401 | GetQueryResponse404 | GetQueryResponse422 | GetQueryResponse429 | GetQueryResponse500 | QueryResponse]
    """

    kwargs = _get_kwargs(
        query_id=query_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    query_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | GetQueryResponse401
    | GetQueryResponse404
    | GetQueryResponse422
    | GetQueryResponse429
    | GetQueryResponse500
    | QueryResponse
    | None
):
    """Get query

     Get query

    Args:
        query_id (str):  Example: example.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetQueryResponse401 | GetQueryResponse404 | GetQueryResponse422 | GetQueryResponse429 | GetQueryResponse500 | QueryResponse
    """

    return (
        await asyncio_detailed(
            query_id=query_id,
            client=client,
        )
    ).parsed
