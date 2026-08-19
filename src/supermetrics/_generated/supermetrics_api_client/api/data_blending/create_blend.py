from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blend_create_request import BlendCreateRequest
from ...models.blend_response import BlendResponse
from ...models.create_blend_response_400 import CreateBlendResponse400
from ...models.create_blend_response_401 import CreateBlendResponse401
from ...models.create_blend_response_429 import CreateBlendResponse429
from ...models.create_blend_response_500 import CreateBlendResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: BlendCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/teams/{team_id}/data-blending/blends".format(
            team_id=quote(str(team_id), safe=""),
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
    | CreateBlendResponse400
    | CreateBlendResponse401
    | CreateBlendResponse429
    | CreateBlendResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 201:
        response_201 = BlendResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateBlendResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateBlendResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = CreateBlendResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateBlendResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BlendResponse
    | CreateBlendResponse400
    | CreateBlendResponse401
    | CreateBlendResponse429
    | CreateBlendResponse500
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
    *,
    client: AuthenticatedClient,
    body: BlendCreateRequest,
) -> Response[
    BlendResponse
    | CreateBlendResponse400
    | CreateBlendResponse401
    | CreateBlendResponse429
    | CreateBlendResponse500
    | ErrorResponse
]:
    """Create a blend

     Create a new blend for a team. Returns the full blend resource.

    Args:
        team_id (int):
        body (BlendCreateRequest): Payload for creating a new blend. Extends BlendBaseRequest and
            additionally requires the blend `type`. When creating, new data sources are referenced by
            `blend_data_source_key` rather than `blend_data_source_id`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendResponse | CreateBlendResponse400 | CreateBlendResponse401 | CreateBlendResponse429 | CreateBlendResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: BlendCreateRequest,
) -> (
    BlendResponse
    | CreateBlendResponse400
    | CreateBlendResponse401
    | CreateBlendResponse429
    | CreateBlendResponse500
    | ErrorResponse
    | None
):
    """Create a blend

     Create a new blend for a team. Returns the full blend resource.

    Args:
        team_id (int):
        body (BlendCreateRequest): Payload for creating a new blend. Extends BlendBaseRequest and
            additionally requires the blend `type`. When creating, new data sources are referenced by
            `blend_data_source_key` rather than `blend_data_source_id`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendResponse | CreateBlendResponse400 | CreateBlendResponse401 | CreateBlendResponse429 | CreateBlendResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: BlendCreateRequest,
) -> Response[
    BlendResponse
    | CreateBlendResponse400
    | CreateBlendResponse401
    | CreateBlendResponse429
    | CreateBlendResponse500
    | ErrorResponse
]:
    """Create a blend

     Create a new blend for a team. Returns the full blend resource.

    Args:
        team_id (int):
        body (BlendCreateRequest): Payload for creating a new blend. Extends BlendBaseRequest and
            additionally requires the blend `type`. When creating, new data sources are referenced by
            `blend_data_source_key` rather than `blend_data_source_id`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlendResponse | CreateBlendResponse400 | CreateBlendResponse401 | CreateBlendResponse429 | CreateBlendResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: BlendCreateRequest,
) -> (
    BlendResponse
    | CreateBlendResponse400
    | CreateBlendResponse401
    | CreateBlendResponse429
    | CreateBlendResponse500
    | ErrorResponse
    | None
):
    """Create a blend

     Create a new blend for a team. Returns the full blend resource.

    Args:
        team_id (int):
        body (BlendCreateRequest): Payload for creating a new blend. Extends BlendBaseRequest and
            additionally requires the blend `type`. When creating, new data sources are referenced by
            `blend_data_source_key` rather than `blend_data_source_id`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlendResponse | CreateBlendResponse400 | CreateBlendResponse401 | CreateBlendResponse429 | CreateBlendResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
