from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_blend_response_400 import DeleteBlendResponse400
from ...models.delete_blend_response_401 import DeleteBlendResponse401
from ...models.delete_blend_response_404 import DeleteBlendResponse404
from ...models.delete_blend_response_429 import DeleteBlendResponse429
from ...models.delete_blend_response_500 import DeleteBlendResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    blend_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/teams/{team_id}/data-blending/blends/{blend_id}".format(
            team_id=quote(str(team_id), safe=""),
            blend_id=quote(str(blend_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | DeleteBlendResponse400
    | DeleteBlendResponse401
    | DeleteBlendResponse404
    | DeleteBlendResponse429
    | DeleteBlendResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = DeleteBlendResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = DeleteBlendResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = DeleteBlendResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = DeleteBlendResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = DeleteBlendResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | DeleteBlendResponse400
    | DeleteBlendResponse401
    | DeleteBlendResponse404
    | DeleteBlendResponse429
    | DeleteBlendResponse500
    | ErrorResponse
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
    Any
    | DeleteBlendResponse400
    | DeleteBlendResponse401
    | DeleteBlendResponse404
    | DeleteBlendResponse429
    | DeleteBlendResponse500
    | ErrorResponse
]:
    """Delete a blend

     Delete a blend by ID.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteBlendResponse400 | DeleteBlendResponse401 | DeleteBlendResponse404 | DeleteBlendResponse429 | DeleteBlendResponse500 | ErrorResponse]
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
    Any
    | DeleteBlendResponse400
    | DeleteBlendResponse401
    | DeleteBlendResponse404
    | DeleteBlendResponse429
    | DeleteBlendResponse500
    | ErrorResponse
    | None
):
    """Delete a blend

     Delete a blend by ID.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteBlendResponse400 | DeleteBlendResponse401 | DeleteBlendResponse404 | DeleteBlendResponse429 | DeleteBlendResponse500 | ErrorResponse
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
    Any
    | DeleteBlendResponse400
    | DeleteBlendResponse401
    | DeleteBlendResponse404
    | DeleteBlendResponse429
    | DeleteBlendResponse500
    | ErrorResponse
]:
    """Delete a blend

     Delete a blend by ID.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteBlendResponse400 | DeleteBlendResponse401 | DeleteBlendResponse404 | DeleteBlendResponse429 | DeleteBlendResponse500 | ErrorResponse]
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
    Any
    | DeleteBlendResponse400
    | DeleteBlendResponse401
    | DeleteBlendResponse404
    | DeleteBlendResponse429
    | DeleteBlendResponse500
    | ErrorResponse
    | None
):
    """Delete a blend

     Delete a blend by ID.

    Args:
        team_id (int):
        blend_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteBlendResponse400 | DeleteBlendResponse401 | DeleteBlendResponse404 | DeleteBlendResponse429 | DeleteBlendResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            blend_id=blend_id,
            client=client,
        )
    ).parsed
