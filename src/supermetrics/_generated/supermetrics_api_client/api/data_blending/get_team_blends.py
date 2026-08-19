from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blend_list_response import BlendListResponse
from ...models.error_response import ErrorResponse
from ...models.get_team_blends_response_400 import GetTeamBlendsResponse400
from ...models.get_team_blends_response_401 import GetTeamBlendsResponse401
from ...models.get_team_blends_response_429 import GetTeamBlendsResponse429
from ...models.get_team_blends_response_500 import GetTeamBlendsResponse500
from ...models.get_team_blends_type import GetTeamBlendsType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    *,
    type_: GetTeamBlendsType | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_

    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/data-blending/blends".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    BlendListResponse
    | ErrorResponse
    | GetTeamBlendsResponse400
    | GetTeamBlendsResponse401
    | GetTeamBlendsResponse429
    | GetTeamBlendsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = BlendListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetTeamBlendsResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetTeamBlendsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = GetTeamBlendsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTeamBlendsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BlendListResponse
    | ErrorResponse
    | GetTeamBlendsResponse400
    | GetTeamBlendsResponse401
    | GetTeamBlendsResponse429
    | GetTeamBlendsResponse500
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
    type_: GetTeamBlendsType | Unset = UNSET,
) -> Response[
    BlendListResponse
    | ErrorResponse
    | GetTeamBlendsResponse400
    | GetTeamBlendsResponse401
    | GetTeamBlendsResponse429
    | GetTeamBlendsResponse500
]:
    """List all blends

     Returns all blends for a team, optionally filtered by type.

    Args:
        team_id (int):
        type_ (GetTeamBlendsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendListResponse | ErrorResponse | GetTeamBlendsResponse400 | GetTeamBlendsResponse401 | GetTeamBlendsResponse429 | GetTeamBlendsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    type_: GetTeamBlendsType | Unset = UNSET,
) -> (
    BlendListResponse
    | ErrorResponse
    | GetTeamBlendsResponse400
    | GetTeamBlendsResponse401
    | GetTeamBlendsResponse429
    | GetTeamBlendsResponse500
    | None
):
    """List all blends

     Returns all blends for a team, optionally filtered by type.

    Args:
        team_id (int):
        type_ (GetTeamBlendsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendListResponse | ErrorResponse | GetTeamBlendsResponse400 | GetTeamBlendsResponse401 | GetTeamBlendsResponse429 | GetTeamBlendsResponse500
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    type_: GetTeamBlendsType | Unset = UNSET,
) -> Response[
    BlendListResponse
    | ErrorResponse
    | GetTeamBlendsResponse400
    | GetTeamBlendsResponse401
    | GetTeamBlendsResponse429
    | GetTeamBlendsResponse500
]:
    """List all blends

     Returns all blends for a team, optionally filtered by type.

    Args:
        team_id (int):
        type_ (GetTeamBlendsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendListResponse | ErrorResponse | GetTeamBlendsResponse400 | GetTeamBlendsResponse401 | GetTeamBlendsResponse429 | GetTeamBlendsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    type_: GetTeamBlendsType | Unset = UNSET,
) -> (
    BlendListResponse
    | ErrorResponse
    | GetTeamBlendsResponse400
    | GetTeamBlendsResponse401
    | GetTeamBlendsResponse429
    | GetTeamBlendsResponse500
    | None
):
    """List all blends

     Returns all blends for a team, optionally filtered by type.

    Args:
        team_id (int):
        type_ (GetTeamBlendsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendListResponse | ErrorResponse | GetTeamBlendsResponse400 | GetTeamBlendsResponse401 | GetTeamBlendsResponse429 | GetTeamBlendsResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            type_=type_,
        )
    ).parsed
