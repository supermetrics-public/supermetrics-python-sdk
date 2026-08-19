from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blend_response import BlendResponse
from ...models.blend_update_request import BlendUpdateRequest
from ...models.error_response import ErrorResponse
from ...models.update_blend_response_400 import UpdateBlendResponse400
from ...models.update_blend_response_401 import UpdateBlendResponse401
from ...models.update_blend_response_404 import UpdateBlendResponse404
from ...models.update_blend_response_429 import UpdateBlendResponse429
from ...models.update_blend_response_500 import UpdateBlendResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    blend_id: int,
    *,
    body: BlendUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/teams/{team_id}/data-blending/blends/{blend_id}".format(
            team_id=quote(str(team_id), safe=""),
            blend_id=quote(str(blend_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    BlendResponse
    | ErrorResponse
    | UpdateBlendResponse400
    | UpdateBlendResponse401
    | UpdateBlendResponse404
    | UpdateBlendResponse429
    | UpdateBlendResponse500
    | None
):
    if response.status_code == 200:
        response_200 = BlendResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateBlendResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateBlendResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateBlendResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = UpdateBlendResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateBlendResponse500.from_dict(response.json())

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
    | UpdateBlendResponse400
    | UpdateBlendResponse401
    | UpdateBlendResponse404
    | UpdateBlendResponse429
    | UpdateBlendResponse500
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
    body: BlendUpdateRequest,
) -> Response[
    BlendResponse
    | ErrorResponse
    | UpdateBlendResponse400
    | UpdateBlendResponse401
    | UpdateBlendResponse404
    | UpdateBlendResponse429
    | UpdateBlendResponse500
]:
    """Update a blend

     Update an existing blend. Returns the full updated blend resource.

    Args:
        team_id (int):
        blend_id (int):
        body (BlendUpdateRequest): Payload for updating an existing blend. Extends
            BlendBaseRequest. The blend `type` cannot be changed and is therefore omitted. Existing
            data sources are referenced by `blend_data_source_id`; newly added ones use
            `blend_data_source_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendResponse | ErrorResponse | UpdateBlendResponse400 | UpdateBlendResponse401 | UpdateBlendResponse404 | UpdateBlendResponse429 | UpdateBlendResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        blend_id=blend_id,
        body=body,
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
    body: BlendUpdateRequest,
) -> (
    BlendResponse
    | ErrorResponse
    | UpdateBlendResponse400
    | UpdateBlendResponse401
    | UpdateBlendResponse404
    | UpdateBlendResponse429
    | UpdateBlendResponse500
    | None
):
    """Update a blend

     Update an existing blend. Returns the full updated blend resource.

    Args:
        team_id (int):
        blend_id (int):
        body (BlendUpdateRequest): Payload for updating an existing blend. Extends
            BlendBaseRequest. The blend `type` cannot be changed and is therefore omitted. Existing
            data sources are referenced by `blend_data_source_id`; newly added ones use
            `blend_data_source_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendResponse | ErrorResponse | UpdateBlendResponse400 | UpdateBlendResponse401 | UpdateBlendResponse404 | UpdateBlendResponse429 | UpdateBlendResponse500
    """

    return sync_detailed(
        team_id=team_id,
        blend_id=blend_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    blend_id: int,
    *,
    client: AuthenticatedClient,
    body: BlendUpdateRequest,
) -> Response[
    BlendResponse
    | ErrorResponse
    | UpdateBlendResponse400
    | UpdateBlendResponse401
    | UpdateBlendResponse404
    | UpdateBlendResponse429
    | UpdateBlendResponse500
]:
    """Update a blend

     Update an existing blend. Returns the full updated blend resource.

    Args:
        team_id (int):
        blend_id (int):
        body (BlendUpdateRequest): Payload for updating an existing blend. Extends
            BlendBaseRequest. The blend `type` cannot be changed and is therefore omitted. Existing
            data sources are referenced by `blend_data_source_id`; newly added ones use
            `blend_data_source_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendResponse | ErrorResponse | UpdateBlendResponse400 | UpdateBlendResponse401 | UpdateBlendResponse404 | UpdateBlendResponse429 | UpdateBlendResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        blend_id=blend_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    blend_id: int,
    *,
    client: AuthenticatedClient,
    body: BlendUpdateRequest,
) -> (
    BlendResponse
    | ErrorResponse
    | UpdateBlendResponse400
    | UpdateBlendResponse401
    | UpdateBlendResponse404
    | UpdateBlendResponse429
    | UpdateBlendResponse500
    | None
):
    """Update a blend

     Update an existing blend. Returns the full updated blend resource.

    Args:
        team_id (int):
        blend_id (int):
        body (BlendUpdateRequest): Payload for updating an existing blend. Extends
            BlendBaseRequest. The blend `type` cannot be changed and is therefore omitted. Existing
            data sources are referenced by `blend_data_source_id`; newly added ones use
            `blend_data_source_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendResponse | ErrorResponse | UpdateBlendResponse400 | UpdateBlendResponse401 | UpdateBlendResponse404 | UpdateBlendResponse429 | UpdateBlendResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            blend_id=blend_id,
            client=client,
            body=body,
        )
    ).parsed
