from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_list_response import ApiKeyListResponse
from ...models.error_response import ErrorResponse
from ...models.get_team_api_keys_response_400 import GetTeamApiKeysResponse400
from ...models.get_team_api_keys_response_401 import GetTeamApiKeysResponse401
from ...models.get_team_api_keys_response_429 import GetTeamApiKeysResponse429
from ...models.get_team_api_keys_response_500 import GetTeamApiKeysResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/api_keys".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiKeyListResponse
    | ErrorResponse
    | GetTeamApiKeysResponse400
    | GetTeamApiKeysResponse401
    | GetTeamApiKeysResponse429
    | GetTeamApiKeysResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ApiKeyListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetTeamApiKeysResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetTeamApiKeysResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = GetTeamApiKeysResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTeamApiKeysResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiKeyListResponse
    | ErrorResponse
    | GetTeamApiKeysResponse400
    | GetTeamApiKeysResponse401
    | GetTeamApiKeysResponse429
    | GetTeamApiKeysResponse500
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
    ApiKeyListResponse
    | ErrorResponse
    | GetTeamApiKeysResponse400
    | GetTeamApiKeysResponse401
    | GetTeamApiKeysResponse429
    | GetTeamApiKeysResponse500
]:
    """List API keys for a team

     Retrieve a list of all API keys belonging to a team.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyListResponse | ErrorResponse | GetTeamApiKeysResponse400 | GetTeamApiKeysResponse401 | GetTeamApiKeysResponse429 | GetTeamApiKeysResponse500]
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
    ApiKeyListResponse
    | ErrorResponse
    | GetTeamApiKeysResponse400
    | GetTeamApiKeysResponse401
    | GetTeamApiKeysResponse429
    | GetTeamApiKeysResponse500
    | None
):
    """List API keys for a team

     Retrieve a list of all API keys belonging to a team.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyListResponse | ErrorResponse | GetTeamApiKeysResponse400 | GetTeamApiKeysResponse401 | GetTeamApiKeysResponse429 | GetTeamApiKeysResponse500
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
    ApiKeyListResponse
    | ErrorResponse
    | GetTeamApiKeysResponse400
    | GetTeamApiKeysResponse401
    | GetTeamApiKeysResponse429
    | GetTeamApiKeysResponse500
]:
    """List API keys for a team

     Retrieve a list of all API keys belonging to a team.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyListResponse | ErrorResponse | GetTeamApiKeysResponse400 | GetTeamApiKeysResponse401 | GetTeamApiKeysResponse429 | GetTeamApiKeysResponse500]
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
    ApiKeyListResponse
    | ErrorResponse
    | GetTeamApiKeysResponse400
    | GetTeamApiKeysResponse401
    | GetTeamApiKeysResponse429
    | GetTeamApiKeysResponse500
    | None
):
    """List API keys for a team

     Retrieve a list of all API keys belonging to a team.

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyListResponse | ErrorResponse | GetTeamApiKeysResponse400 | GetTeamApiKeysResponse401 | GetTeamApiKeysResponse429 | GetTeamApiKeysResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
