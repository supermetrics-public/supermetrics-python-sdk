from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.destination_response import DestinationResponse
from ...models.update_destination_request import UpdateDestinationRequest
from ...models.update_destination_response_400 import UpdateDestinationResponse400
from ...models.update_destination_response_401 import UpdateDestinationResponse401
from ...models.update_destination_response_403 import UpdateDestinationResponse403
from ...models.update_destination_response_404 import UpdateDestinationResponse404
from ...models.update_destination_response_422 import UpdateDestinationResponse422
from ...models.update_destination_response_429 import UpdateDestinationResponse429
from ...models.update_destination_response_500 import UpdateDestinationResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    destination_id: int,
    *,
    body: UpdateDestinationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/teams/{team_id}/destinations/{destination_id}".format(
            team_id=quote(str(team_id), safe=""),
            destination_id=quote(str(destination_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DestinationResponse
    | UpdateDestinationResponse400
    | UpdateDestinationResponse401
    | UpdateDestinationResponse403
    | UpdateDestinationResponse404
    | UpdateDestinationResponse422
    | UpdateDestinationResponse429
    | UpdateDestinationResponse500
    | None
):
    if response.status_code == 200:
        response_200 = DestinationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateDestinationResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateDestinationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UpdateDestinationResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateDestinationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = UpdateDestinationResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateDestinationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateDestinationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DestinationResponse
    | UpdateDestinationResponse400
    | UpdateDestinationResponse401
    | UpdateDestinationResponse403
    | UpdateDestinationResponse404
    | UpdateDestinationResponse422
    | UpdateDestinationResponse429
    | UpdateDestinationResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateDestinationRequest,
) -> Response[
    DestinationResponse
    | UpdateDestinationResponse400
    | UpdateDestinationResponse401
    | UpdateDestinationResponse403
    | UpdateDestinationResponse404
    | UpdateDestinationResponse422
    | UpdateDestinationResponse429
    | UpdateDestinationResponse500
]:
    """Update destination

     Update a destinations details

    Args:
        team_id (int):
        destination_id (int):
        body (UpdateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DestinationResponse | UpdateDestinationResponse400 | UpdateDestinationResponse401 | UpdateDestinationResponse403 | UpdateDestinationResponse404 | UpdateDestinationResponse422 | UpdateDestinationResponse429 | UpdateDestinationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        destination_id=destination_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateDestinationRequest,
) -> (
    DestinationResponse
    | UpdateDestinationResponse400
    | UpdateDestinationResponse401
    | UpdateDestinationResponse403
    | UpdateDestinationResponse404
    | UpdateDestinationResponse422
    | UpdateDestinationResponse429
    | UpdateDestinationResponse500
    | None
):
    """Update destination

     Update a destinations details

    Args:
        team_id (int):
        destination_id (int):
        body (UpdateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DestinationResponse | UpdateDestinationResponse400 | UpdateDestinationResponse401 | UpdateDestinationResponse403 | UpdateDestinationResponse404 | UpdateDestinationResponse422 | UpdateDestinationResponse429 | UpdateDestinationResponse500
    """

    return sync_detailed(
        team_id=team_id,
        destination_id=destination_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateDestinationRequest,
) -> Response[
    DestinationResponse
    | UpdateDestinationResponse400
    | UpdateDestinationResponse401
    | UpdateDestinationResponse403
    | UpdateDestinationResponse404
    | UpdateDestinationResponse422
    | UpdateDestinationResponse429
    | UpdateDestinationResponse500
]:
    """Update destination

     Update a destinations details

    Args:
        team_id (int):
        destination_id (int):
        body (UpdateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DestinationResponse | UpdateDestinationResponse400 | UpdateDestinationResponse401 | UpdateDestinationResponse403 | UpdateDestinationResponse404 | UpdateDestinationResponse422 | UpdateDestinationResponse429 | UpdateDestinationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        destination_id=destination_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateDestinationRequest,
) -> (
    DestinationResponse
    | UpdateDestinationResponse400
    | UpdateDestinationResponse401
    | UpdateDestinationResponse403
    | UpdateDestinationResponse404
    | UpdateDestinationResponse422
    | UpdateDestinationResponse429
    | UpdateDestinationResponse500
    | None
):
    """Update destination

     Update a destinations details

    Args:
        team_id (int):
        destination_id (int):
        body (UpdateDestinationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DestinationResponse | UpdateDestinationResponse400 | UpdateDestinationResponse401 | UpdateDestinationResponse403 | UpdateDestinationResponse404 | UpdateDestinationResponse422 | UpdateDestinationResponse429 | UpdateDestinationResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            destination_id=destination_id,
            client=client,
            body=body,
        )
    ).parsed
