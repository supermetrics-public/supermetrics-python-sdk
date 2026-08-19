from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blend_response import BlendResponse
from ...models.error_response import ErrorResponse
from ...models.get_blend_response_400 import GetBlendResponse400
from ...models.get_blend_response_401 import GetBlendResponse401
from ...models.get_blend_response_404 import GetBlendResponse404
from ...models.get_blend_response_429 import GetBlendResponse429
from ...models.get_blend_response_500 import GetBlendResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    blend_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/data-blending/blends/{blend_id}".format(
            team_id=quote(str(team_id), safe=""),
            blend_id=quote(str(blend_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    BlendResponse
    | ErrorResponse
    | GetBlendResponse400
    | GetBlendResponse401
    | GetBlendResponse404
    | GetBlendResponse429
    | GetBlendResponse500
    | None
):
    if response.status_code == 200:
        response_200 = BlendResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetBlendResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetBlendResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetBlendResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetBlendResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetBlendResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BlendResponse
    | ErrorResponse
    | GetBlendResponse400
    | GetBlendResponse401
    | GetBlendResponse404
    | GetBlendResponse429
    | GetBlendResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    blend_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    BlendResponse
    | ErrorResponse
    | GetBlendResponse400
    | GetBlendResponse401
    | GetBlendResponse404
    | GetBlendResponse429
    | GetBlendResponse500
]:
    """Get a blend by ID

     Returns a single blend by ID, including all active data sources.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendResponse | ErrorResponse | GetBlendResponse400 | GetBlendResponse401 | GetBlendResponse404 | GetBlendResponse429 | GetBlendResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        blend_id=blend_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    blend_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    BlendResponse
    | ErrorResponse
    | GetBlendResponse400
    | GetBlendResponse401
    | GetBlendResponse404
    | GetBlendResponse429
    | GetBlendResponse500
    | None
):
    """Get a blend by ID

     Returns a single blend by ID, including all active data sources.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendResponse | ErrorResponse | GetBlendResponse400 | GetBlendResponse401 | GetBlendResponse404 | GetBlendResponse429 | GetBlendResponse500
    """

    return sync_detailed(
        team_id=team_id,
        blend_id=blend_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    blend_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    BlendResponse
    | ErrorResponse
    | GetBlendResponse400
    | GetBlendResponse401
    | GetBlendResponse404
    | GetBlendResponse429
    | GetBlendResponse500
]:
    """Get a blend by ID

     Returns a single blend by ID, including all active data sources.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendResponse | ErrorResponse | GetBlendResponse400 | GetBlendResponse401 | GetBlendResponse404 | GetBlendResponse429 | GetBlendResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        blend_id=blend_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    blend_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    BlendResponse
    | ErrorResponse
    | GetBlendResponse400
    | GetBlendResponse401
    | GetBlendResponse404
    | GetBlendResponse429
    | GetBlendResponse500
    | None
):
    """Get a blend by ID

     Returns a single blend by ID, including all active data sources.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendResponse | ErrorResponse | GetBlendResponse400 | GetBlendResponse401 | GetBlendResponse404 | GetBlendResponse429 | GetBlendResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            blend_id=blend_id,
            client=client,
        )
    ).parsed
