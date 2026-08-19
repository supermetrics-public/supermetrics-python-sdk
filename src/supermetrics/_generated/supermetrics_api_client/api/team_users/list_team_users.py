from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_team_users_response_400 import ListTeamUsersResponse400
from ...models.list_team_users_response_401 import ListTeamUsersResponse401
from ...models.list_team_users_response_429 import ListTeamUsersResponse429
from ...models.list_team_users_response_500 import ListTeamUsersResponse500
from ...models.team_user_list_response import TeamUserListResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/users".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | ListTeamUsersResponse400
    | ListTeamUsersResponse401
    | ListTeamUsersResponse429
    | ListTeamUsersResponse500
    | TeamUserListResponse
    | None
):
    if response.status_code == 200:
        response_200 = TeamUserListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ListTeamUsersResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ListTeamUsersResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ListTeamUsersResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListTeamUsersResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | ListTeamUsersResponse400
    | ListTeamUsersResponse401
    | ListTeamUsersResponse429
    | ListTeamUsersResponse500
    | TeamUserListResponse
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
    | ListTeamUsersResponse400
    | ListTeamUsersResponse401
    | ListTeamUsersResponse429
    | ListTeamUsersResponse500
    | TeamUserListResponse
]:
    """List all users in a team

     List all users in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListTeamUsersResponse400 | ListTeamUsersResponse401 | ListTeamUsersResponse429 | ListTeamUsersResponse500 | TeamUserListResponse]
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
    | ListTeamUsersResponse400
    | ListTeamUsersResponse401
    | ListTeamUsersResponse429
    | ListTeamUsersResponse500
    | TeamUserListResponse
    | None
):
    """List all users in a team

     List all users in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListTeamUsersResponse400 | ListTeamUsersResponse401 | ListTeamUsersResponse429 | ListTeamUsersResponse500 | TeamUserListResponse
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
    | ListTeamUsersResponse400
    | ListTeamUsersResponse401
    | ListTeamUsersResponse429
    | ListTeamUsersResponse500
    | TeamUserListResponse
]:
    """List all users in a team

     List all users in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListTeamUsersResponse400 | ListTeamUsersResponse401 | ListTeamUsersResponse429 | ListTeamUsersResponse500 | TeamUserListResponse]
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
    | ListTeamUsersResponse400
    | ListTeamUsersResponse401
    | ListTeamUsersResponse429
    | ListTeamUsersResponse500
    | TeamUserListResponse
    | None
):
    """List all users in a team

     List all users in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListTeamUsersResponse400 | ListTeamUsersResponse401 | ListTeamUsersResponse429 | ListTeamUsersResponse500 | TeamUserListResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
