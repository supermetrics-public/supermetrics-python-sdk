from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_destination_request import CreateDestinationRequest
from ...models.create_destination_response_400 import CreateDestinationResponse400
from ...models.create_destination_response_401 import CreateDestinationResponse401
from ...models.create_destination_response_403 import CreateDestinationResponse403
from ...models.create_destination_response_409 import CreateDestinationResponse409
from ...models.create_destination_response_422 import CreateDestinationResponse422
from ...models.create_destination_response_429 import CreateDestinationResponse429
from ...models.create_destination_response_500 import CreateDestinationResponse500
from ...models.destination_response import DestinationResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: CreateDestinationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/destinations".format(
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
    CreateDestinationResponse400
    | CreateDestinationResponse401
    | CreateDestinationResponse403
    | CreateDestinationResponse409
    | CreateDestinationResponse422
    | CreateDestinationResponse429
    | CreateDestinationResponse500
    | DestinationResponse
    | None
):
    if response.status_code == 201:
        response_201 = DestinationResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateDestinationResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateDestinationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CreateDestinationResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = CreateDestinationResponse409.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = CreateDestinationResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateDestinationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateDestinationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateDestinationResponse400
    | CreateDestinationResponse401
    | CreateDestinationResponse403
    | CreateDestinationResponse409
    | CreateDestinationResponse422
    | CreateDestinationResponse429
    | CreateDestinationResponse500
    | DestinationResponse
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
    body: CreateDestinationRequest,
) -> Response[
    CreateDestinationResponse400
    | CreateDestinationResponse401
    | CreateDestinationResponse403
    | CreateDestinationResponse409
    | CreateDestinationResponse422
    | CreateDestinationResponse429
    | CreateDestinationResponse500
    | DestinationResponse
]:
    """Create destination

     Create a new data warehouse destination

    Args:
        team_id (int):
        body (CreateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDestinationResponse400 | CreateDestinationResponse401 | CreateDestinationResponse403 | CreateDestinationResponse409 | CreateDestinationResponse422 | CreateDestinationResponse429 | CreateDestinationResponse500 | DestinationResponse]
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
    body: CreateDestinationRequest,
) -> (
    CreateDestinationResponse400
    | CreateDestinationResponse401
    | CreateDestinationResponse403
    | CreateDestinationResponse409
    | CreateDestinationResponse422
    | CreateDestinationResponse429
    | CreateDestinationResponse500
    | DestinationResponse
    | None
):
    """Create destination

     Create a new data warehouse destination

    Args:
        team_id (int):
        body (CreateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDestinationResponse400 | CreateDestinationResponse401 | CreateDestinationResponse403 | CreateDestinationResponse409 | CreateDestinationResponse422 | CreateDestinationResponse429 | CreateDestinationResponse500 | DestinationResponse
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
    body: CreateDestinationRequest,
) -> Response[
    CreateDestinationResponse400
    | CreateDestinationResponse401
    | CreateDestinationResponse403
    | CreateDestinationResponse409
    | CreateDestinationResponse422
    | CreateDestinationResponse429
    | CreateDestinationResponse500
    | DestinationResponse
]:
    """Create destination

     Create a new data warehouse destination

    Args:
        team_id (int):
        body (CreateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDestinationResponse400 | CreateDestinationResponse401 | CreateDestinationResponse403 | CreateDestinationResponse409 | CreateDestinationResponse422 | CreateDestinationResponse429 | CreateDestinationResponse500 | DestinationResponse]
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
    body: CreateDestinationRequest,
) -> (
    CreateDestinationResponse400
    | CreateDestinationResponse401
    | CreateDestinationResponse403
    | CreateDestinationResponse409
    | CreateDestinationResponse422
    | CreateDestinationResponse429
    | CreateDestinationResponse500
    | DestinationResponse
    | None
):
    """Create destination

     Create a new data warehouse destination

    Args:
        team_id (int):
        body (CreateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDestinationResponse400 | CreateDestinationResponse401 | CreateDestinationResponse403 | CreateDestinationResponse409 | CreateDestinationResponse422 | CreateDestinationResponse429 | CreateDestinationResponse500 | DestinationResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
