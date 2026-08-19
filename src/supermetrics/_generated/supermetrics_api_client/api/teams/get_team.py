from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_team_response_400 import GetTeamResponse400
from ...models.get_team_response_401 import GetTeamResponse401
from ...models.get_team_response_404 import GetTeamResponse404
from ...models.get_team_response_429 import GetTeamResponse429
from ...models.get_team_response_500 import GetTeamResponse500
from ...models.team_response import TeamResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | GetTeamResponse400
    | GetTeamResponse401
    | GetTeamResponse404
    | GetTeamResponse429
    | GetTeamResponse500
    | TeamResponse
    | None
):
    if response.status_code == 200:
        response_200 = TeamResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetTeamResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetTeamResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetTeamResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetTeamResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTeamResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | GetTeamResponse400
    | GetTeamResponse401
    | GetTeamResponse404
    | GetTeamResponse429
    | GetTeamResponse500
    | TeamResponse
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
    ErrorResponse
    | GetTeamResponse400
    | GetTeamResponse401
    | GetTeamResponse404
    | GetTeamResponse429
    | GetTeamResponse500
    | TeamResponse
]:
    """Get team details by team ID

     Get team details by team ID

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetTeamResponse400 | GetTeamResponse401 | GetTeamResponse404 | GetTeamResponse429 | GetTeamResponse500 | TeamResponse]
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
    ErrorResponse
    | GetTeamResponse400
    | GetTeamResponse401
    | GetTeamResponse404
    | GetTeamResponse429
    | GetTeamResponse500
    | TeamResponse
    | None
):
    """Get team details by team ID

     Get team details by team ID

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetTeamResponse400 | GetTeamResponse401 | GetTeamResponse404 | GetTeamResponse429 | GetTeamResponse500 | TeamResponse
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
    ErrorResponse
    | GetTeamResponse400
    | GetTeamResponse401
    | GetTeamResponse404
    | GetTeamResponse429
    | GetTeamResponse500
    | TeamResponse
]:
    """Get team details by team ID

     Get team details by team ID

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetTeamResponse400 | GetTeamResponse401 | GetTeamResponse404 | GetTeamResponse429 | GetTeamResponse500 | TeamResponse]
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
    ErrorResponse
    | GetTeamResponse400
    | GetTeamResponse401
    | GetTeamResponse404
    | GetTeamResponse429
    | GetTeamResponse500
    | TeamResponse
    | None
):
    """Get team details by team ID

     Get team details by team ID

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetTeamResponse400 | GetTeamResponse401 | GetTeamResponse404 | GetTeamResponse429 | GetTeamResponse500 | TeamResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
