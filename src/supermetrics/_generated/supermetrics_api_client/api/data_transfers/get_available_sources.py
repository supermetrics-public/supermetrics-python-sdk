from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.available_sources_response import AvailableSourcesResponse
from ...models.get_available_sources_response_401 import GetAvailableSourcesResponse401
from ...models.get_available_sources_response_403 import GetAvailableSourcesResponse403
from ...models.get_available_sources_response_429 import GetAvailableSourcesResponse429
from ...models.get_available_sources_response_500 import GetAvailableSourcesResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfers/available-sources".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    AvailableSourcesResponse
    | GetAvailableSourcesResponse401
    | GetAvailableSourcesResponse403
    | GetAvailableSourcesResponse429
    | GetAvailableSourcesResponse500
    | None
):
    if response.status_code == 200:
        response_200 = AvailableSourcesResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetAvailableSourcesResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetAvailableSourcesResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = GetAvailableSourcesResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetAvailableSourcesResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    AvailableSourcesResponse
    | GetAvailableSourcesResponse401
    | GetAvailableSourcesResponse403
    | GetAvailableSourcesResponse429
    | GetAvailableSourcesResponse500
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
    AvailableSourcesResponse
    | GetAvailableSourcesResponse401
    | GetAvailableSourcesResponse403
    | GetAvailableSourcesResponse429
    | GetAvailableSourcesResponse500
]:
    """Get available sources

     Returns all available data sources and destinations for a Hub transfer.

    **Returns:** Initial configuration data including available sources and destinations.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AvailableSourcesResponse | GetAvailableSourcesResponse401 | GetAvailableSourcesResponse403 | GetAvailableSourcesResponse429 | GetAvailableSourcesResponse500]
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
    AvailableSourcesResponse
    | GetAvailableSourcesResponse401
    | GetAvailableSourcesResponse403
    | GetAvailableSourcesResponse429
    | GetAvailableSourcesResponse500
    | None
):
    """Get available sources

     Returns all available data sources and destinations for a Hub transfer.

    **Returns:** Initial configuration data including available sources and destinations.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AvailableSourcesResponse | GetAvailableSourcesResponse401 | GetAvailableSourcesResponse403 | GetAvailableSourcesResponse429 | GetAvailableSourcesResponse500
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
    AvailableSourcesResponse
    | GetAvailableSourcesResponse401
    | GetAvailableSourcesResponse403
    | GetAvailableSourcesResponse429
    | GetAvailableSourcesResponse500
]:
    """Get available sources

     Returns all available data sources and destinations for a Hub transfer.

    **Returns:** Initial configuration data including available sources and destinations.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AvailableSourcesResponse | GetAvailableSourcesResponse401 | GetAvailableSourcesResponse403 | GetAvailableSourcesResponse429 | GetAvailableSourcesResponse500]
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
    AvailableSourcesResponse
    | GetAvailableSourcesResponse401
    | GetAvailableSourcesResponse403
    | GetAvailableSourcesResponse429
    | GetAvailableSourcesResponse500
    | None
):
    """Get available sources

     Returns all available data sources and destinations for a Hub transfer.

    **Returns:** Initial configuration data including available sources and destinations.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AvailableSourcesResponse | GetAvailableSourcesResponse401 | GetAvailableSourcesResponse403 | GetAvailableSourcesResponse429 | GetAvailableSourcesResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
