from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_response import ApiKeyResponse
from ...models.error_response import ErrorResponse
from ...models.get_team_api_key_response_400 import GetTeamApiKeyResponse400
from ...models.get_team_api_key_response_401 import GetTeamApiKeyResponse401
from ...models.get_team_api_key_response_404 import GetTeamApiKeyResponse404
from ...models.get_team_api_key_response_429 import GetTeamApiKeyResponse429
from ...models.get_team_api_key_response_500 import GetTeamApiKeyResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    api_key_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/api_keys/{api_key_id}".format(
            team_id=quote(str(team_id), safe=""),
            api_key_id=quote(str(api_key_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiKeyResponse
    | ErrorResponse
    | GetTeamApiKeyResponse400
    | GetTeamApiKeyResponse401
    | GetTeamApiKeyResponse404
    | GetTeamApiKeyResponse429
    | GetTeamApiKeyResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ApiKeyResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetTeamApiKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetTeamApiKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetTeamApiKeyResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetTeamApiKeyResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTeamApiKeyResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | GetTeamApiKeyResponse400
    | GetTeamApiKeyResponse401
    | GetTeamApiKeyResponse404
    | GetTeamApiKeyResponse429
    | GetTeamApiKeyResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | GetTeamApiKeyResponse400
    | GetTeamApiKeyResponse401
    | GetTeamApiKeyResponse404
    | GetTeamApiKeyResponse429
    | GetTeamApiKeyResponse500
]:
    """Get an API key for a team

     Retrieve details of a specific API key belonging to a team.

    Args:
        team_id (int):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | ErrorResponse | GetTeamApiKeyResponse400 | GetTeamApiKeyResponse401 | GetTeamApiKeyResponse404 | GetTeamApiKeyResponse429 | GetTeamApiKeyResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        api_key_id=api_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ApiKeyResponse
    | ErrorResponse
    | GetTeamApiKeyResponse400
    | GetTeamApiKeyResponse401
    | GetTeamApiKeyResponse404
    | GetTeamApiKeyResponse429
    | GetTeamApiKeyResponse500
    | None
):
    """Get an API key for a team

     Retrieve details of a specific API key belonging to a team.

    Args:
        team_id (int):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | ErrorResponse | GetTeamApiKeyResponse400 | GetTeamApiKeyResponse401 | GetTeamApiKeyResponse404 | GetTeamApiKeyResponse429 | GetTeamApiKeyResponse500
    """

    return sync_detailed(
        team_id=team_id,
        api_key_id=api_key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | GetTeamApiKeyResponse400
    | GetTeamApiKeyResponse401
    | GetTeamApiKeyResponse404
    | GetTeamApiKeyResponse429
    | GetTeamApiKeyResponse500
]:
    """Get an API key for a team

     Retrieve details of a specific API key belonging to a team.

    Args:
        team_id (int):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | ErrorResponse | GetTeamApiKeyResponse400 | GetTeamApiKeyResponse401 | GetTeamApiKeyResponse404 | GetTeamApiKeyResponse429 | GetTeamApiKeyResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        api_key_id=api_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ApiKeyResponse
    | ErrorResponse
    | GetTeamApiKeyResponse400
    | GetTeamApiKeyResponse401
    | GetTeamApiKeyResponse404
    | GetTeamApiKeyResponse429
    | GetTeamApiKeyResponse500
    | None
):
    """Get an API key for a team

     Retrieve details of a specific API key belonging to a team.

    Args:
        team_id (int):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | ErrorResponse | GetTeamApiKeyResponse400 | GetTeamApiKeyResponse401 | GetTeamApiKeyResponse404 | GetTeamApiKeyResponse429 | GetTeamApiKeyResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            api_key_id=api_key_id,
            client=client,
        )
    ).parsed
