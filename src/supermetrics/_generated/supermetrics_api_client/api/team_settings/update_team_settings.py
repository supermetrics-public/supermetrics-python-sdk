from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.team_settings import TeamSettings
from ...models.team_settings_response import TeamSettingsResponse
from ...models.update_team_settings_response_401 import UpdateTeamSettingsResponse401
from ...models.update_team_settings_response_422 import UpdateTeamSettingsResponse422
from ...models.update_team_settings_response_429 import UpdateTeamSettingsResponse429
from ...models.update_team_settings_response_500 import UpdateTeamSettingsResponse500
from ...types import Response


def _get_kwargs(
    *,
    body: TeamSettings,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/team/settings",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | TeamSettingsResponse
    | UpdateTeamSettingsResponse401
    | UpdateTeamSettingsResponse422
    | UpdateTeamSettingsResponse429
    | UpdateTeamSettingsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = TeamSettingsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = UpdateTeamSettingsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = UpdateTeamSettingsResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateTeamSettingsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateTeamSettingsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | TeamSettingsResponse
    | UpdateTeamSettingsResponse401
    | UpdateTeamSettingsResponse422
    | UpdateTeamSettingsResponse429
    | UpdateTeamSettingsResponse500
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
    body: TeamSettings,
) -> Response[
    ErrorResponse
    | TeamSettingsResponse
    | UpdateTeamSettingsResponse401
    | UpdateTeamSettingsResponse422
    | UpdateTeamSettingsResponse429
    | UpdateTeamSettingsResponse500
]:
    """Update settings

     Update specific general team settings for the current team.

    Args:
        body (TeamSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TeamSettingsResponse | UpdateTeamSettingsResponse401 | UpdateTeamSettingsResponse422 | UpdateTeamSettingsResponse429 | UpdateTeamSettingsResponse500]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: TeamSettings,
) -> (
    ErrorResponse
    | TeamSettingsResponse
    | UpdateTeamSettingsResponse401
    | UpdateTeamSettingsResponse422
    | UpdateTeamSettingsResponse429
    | UpdateTeamSettingsResponse500
    | None
):
    """Update settings

     Update specific general team settings for the current team.

    Args:
        body (TeamSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TeamSettingsResponse | UpdateTeamSettingsResponse401 | UpdateTeamSettingsResponse422 | UpdateTeamSettingsResponse429 | UpdateTeamSettingsResponse500
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TeamSettings,
) -> Response[
    ErrorResponse
    | TeamSettingsResponse
    | UpdateTeamSettingsResponse401
    | UpdateTeamSettingsResponse422
    | UpdateTeamSettingsResponse429
    | UpdateTeamSettingsResponse500
]:
    """Update settings

     Update specific general team settings for the current team.

    Args:
        body (TeamSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TeamSettingsResponse | UpdateTeamSettingsResponse401 | UpdateTeamSettingsResponse422 | UpdateTeamSettingsResponse429 | UpdateTeamSettingsResponse500]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TeamSettings,
) -> (
    ErrorResponse
    | TeamSettingsResponse
    | UpdateTeamSettingsResponse401
    | UpdateTeamSettingsResponse422
    | UpdateTeamSettingsResponse429
    | UpdateTeamSettingsResponse500
    | None
):
    """Update settings

     Update specific general team settings for the current team.

    Args:
        body (TeamSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TeamSettingsResponse | UpdateTeamSettingsResponse401 | UpdateTeamSettingsResponse422 | UpdateTeamSettingsResponse429 | UpdateTeamSettingsResponse500
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
