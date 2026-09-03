from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_team_settings_response_401 import GetTeamSettingsResponse401
from ...models.get_team_settings_response_422 import GetTeamSettingsResponse422
from ...models.get_team_settings_response_429 import GetTeamSettingsResponse429
from ...models.get_team_settings_response_500 import GetTeamSettingsResponse500
from ...models.team_settings_response import TeamSettingsResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/team/settings",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | GetTeamSettingsResponse401
    | GetTeamSettingsResponse422
    | GetTeamSettingsResponse429
    | GetTeamSettingsResponse500
    | TeamSettingsResponse
    | None
):
    if response.status_code == 200:
        response_200 = TeamSettingsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetTeamSettingsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = GetTeamSettingsResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = GetTeamSettingsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTeamSettingsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | GetTeamSettingsResponse401
    | GetTeamSettingsResponse422
    | GetTeamSettingsResponse429
    | GetTeamSettingsResponse500
    | TeamSettingsResponse
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
    | GetTeamSettingsResponse401
    | GetTeamSettingsResponse422
    | GetTeamSettingsResponse429
    | GetTeamSettingsResponse500
    | TeamSettingsResponse
]:
    """Get settings

     Retrieve all general team settings for the current team.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetTeamSettingsResponse401 | GetTeamSettingsResponse422 | GetTeamSettingsResponse429 | GetTeamSettingsResponse500 | TeamSettingsResponse]
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
    | GetTeamSettingsResponse401
    | GetTeamSettingsResponse422
    | GetTeamSettingsResponse429
    | GetTeamSettingsResponse500
    | TeamSettingsResponse
    | None
):
    """Get settings

     Retrieve all general team settings for the current team.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetTeamSettingsResponse401 | GetTeamSettingsResponse422 | GetTeamSettingsResponse429 | GetTeamSettingsResponse500 | TeamSettingsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | GetTeamSettingsResponse401
    | GetTeamSettingsResponse422
    | GetTeamSettingsResponse429
    | GetTeamSettingsResponse500
    | TeamSettingsResponse
]:
    """Get settings

     Retrieve all general team settings for the current team.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetTeamSettingsResponse401 | GetTeamSettingsResponse422 | GetTeamSettingsResponse429 | GetTeamSettingsResponse500 | TeamSettingsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | GetTeamSettingsResponse401
    | GetTeamSettingsResponse422
    | GetTeamSettingsResponse429
    | GetTeamSettingsResponse500
    | TeamSettingsResponse
    | None
):
    """Get settings

     Retrieve all general team settings for the current team.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetTeamSettingsResponse401 | GetTeamSettingsResponse422 | GetTeamSettingsResponse429 | GetTeamSettingsResponse500 | TeamSettingsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
