from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.destination_response import DestinationResponse
from ...models.get_destination_response_401 import GetDestinationResponse401
from ...models.get_destination_response_403 import GetDestinationResponse403
from ...models.get_destination_response_404 import GetDestinationResponse404
from ...models.get_destination_response_429 import GetDestinationResponse429
from ...models.get_destination_response_500 import GetDestinationResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    destination_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/destinations/{destination_id}".format(
            team_id=quote(str(team_id), safe=""),
            destination_id=quote(str(destination_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DestinationResponse
    | GetDestinationResponse401
    | GetDestinationResponse403
    | GetDestinationResponse404
    | GetDestinationResponse429
    | GetDestinationResponse500
    | None
):
    if response.status_code == 200:
        response_200 = DestinationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetDestinationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetDestinationResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetDestinationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetDestinationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetDestinationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DestinationResponse
    | GetDestinationResponse401
    | GetDestinationResponse403
    | GetDestinationResponse404
    | GetDestinationResponse429
    | GetDestinationResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    DestinationResponse
    | GetDestinationResponse401
    | GetDestinationResponse403
    | GetDestinationResponse404
    | GetDestinationResponse429
    | GetDestinationResponse500
]:
    """Get destination details

     Fetch data about a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DestinationResponse | GetDestinationResponse401 | GetDestinationResponse403 | GetDestinationResponse404 | GetDestinationResponse429 | GetDestinationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        destination_id=destination_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    DestinationResponse
    | GetDestinationResponse401
    | GetDestinationResponse403
    | GetDestinationResponse404
    | GetDestinationResponse429
    | GetDestinationResponse500
    | None
):
    """Get destination details

     Fetch data about a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DestinationResponse | GetDestinationResponse401 | GetDestinationResponse403 | GetDestinationResponse404 | GetDestinationResponse429 | GetDestinationResponse500
    """

    return sync_detailed(
        team_id=team_id,
        destination_id=destination_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    DestinationResponse
    | GetDestinationResponse401
    | GetDestinationResponse403
    | GetDestinationResponse404
    | GetDestinationResponse429
    | GetDestinationResponse500
]:
    """Get destination details

     Fetch data about a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DestinationResponse | GetDestinationResponse401 | GetDestinationResponse403 | GetDestinationResponse404 | GetDestinationResponse429 | GetDestinationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        destination_id=destination_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    DestinationResponse
    | GetDestinationResponse401
    | GetDestinationResponse403
    | GetDestinationResponse404
    | GetDestinationResponse429
    | GetDestinationResponse500
    | None
):
    """Get destination details

     Fetch data about a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DestinationResponse | GetDestinationResponse401 | GetDestinationResponse403 | GetDestinationResponse404 | GetDestinationResponse429 | GetDestinationResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            destination_id=destination_id,
            client=client,
        )
    ).parsed
