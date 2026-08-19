from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.destination_list_response import DestinationListResponse
from ...models.list_destinations_response_401 import ListDestinationsResponse401
from ...models.list_destinations_response_403 import ListDestinationsResponse403
from ...models.list_destinations_response_429 import ListDestinationsResponse429
from ...models.list_destinations_response_500 import ListDestinationsResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/destinations".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DestinationListResponse
    | ListDestinationsResponse401
    | ListDestinationsResponse403
    | ListDestinationsResponse429
    | ListDestinationsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = DestinationListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListDestinationsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListDestinationsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ListDestinationsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListDestinationsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DestinationListResponse
    | ListDestinationsResponse401
    | ListDestinationsResponse403
    | ListDestinationsResponse429
    | ListDestinationsResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    DestinationListResponse
    | ListDestinationsResponse401
    | ListDestinationsResponse403
    | ListDestinationsResponse429
    | ListDestinationsResponse500
]:
    """List destinations

     List all data warehouse destinations for a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DestinationListResponse | ListDestinationsResponse401 | ListDestinationsResponse403 | ListDestinationsResponse429 | ListDestinationsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    DestinationListResponse
    | ListDestinationsResponse401
    | ListDestinationsResponse403
    | ListDestinationsResponse429
    | ListDestinationsResponse500
    | None
):
    """List destinations

     List all data warehouse destinations for a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DestinationListResponse | ListDestinationsResponse401 | ListDestinationsResponse403 | ListDestinationsResponse429 | ListDestinationsResponse500
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    DestinationListResponse
    | ListDestinationsResponse401
    | ListDestinationsResponse403
    | ListDestinationsResponse429
    | ListDestinationsResponse500
]:
    """List destinations

     List all data warehouse destinations for a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DestinationListResponse | ListDestinationsResponse401 | ListDestinationsResponse403 | ListDestinationsResponse429 | ListDestinationsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    DestinationListResponse
    | ListDestinationsResponse401
    | ListDestinationsResponse403
    | ListDestinationsResponse429
    | ListDestinationsResponse500
    | None
):
    """List destinations

     List all data warehouse destinations for a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DestinationListResponse | ListDestinationsResponse401 | ListDestinationsResponse403 | ListDestinationsResponse429 | ListDestinationsResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
