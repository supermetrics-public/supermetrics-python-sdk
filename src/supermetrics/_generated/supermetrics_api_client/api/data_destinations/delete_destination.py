from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_destination_response_401 import DeleteDestinationResponse401
from ...models.delete_destination_response_403 import DeleteDestinationResponse403
from ...models.delete_destination_response_404 import DeleteDestinationResponse404
from ...models.delete_destination_response_409 import DeleteDestinationResponse409
from ...models.delete_destination_response_429 import DeleteDestinationResponse429
from ...models.delete_destination_response_500 import DeleteDestinationResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    destination_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/teams/{team_id}/destinations/{destination_id}".format(
            team_id=quote(str(team_id), safe=""),
            destination_id=quote(str(destination_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | DeleteDestinationResponse401
    | DeleteDestinationResponse403
    | DeleteDestinationResponse404
    | DeleteDestinationResponse409
    | DeleteDestinationResponse429
    | DeleteDestinationResponse500
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 401:
        response_401 = DeleteDestinationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = DeleteDestinationResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = DeleteDestinationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = DeleteDestinationResponse409.from_dict(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = DeleteDestinationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = DeleteDestinationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | DeleteDestinationResponse401
    | DeleteDestinationResponse403
    | DeleteDestinationResponse404
    | DeleteDestinationResponse409
    | DeleteDestinationResponse429
    | DeleteDestinationResponse500
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
) -> Response[
    Any
    | DeleteDestinationResponse401
    | DeleteDestinationResponse403
    | DeleteDestinationResponse404
    | DeleteDestinationResponse409
    | DeleteDestinationResponse429
    | DeleteDestinationResponse500
]:
    """Delete destination

     Remove a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteDestinationResponse401 | DeleteDestinationResponse403 | DeleteDestinationResponse404 | DeleteDestinationResponse409 | DeleteDestinationResponse429 | DeleteDestinationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        destination_id=destination_id,
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
) -> (
    Any
    | DeleteDestinationResponse401
    | DeleteDestinationResponse403
    | DeleteDestinationResponse404
    | DeleteDestinationResponse409
    | DeleteDestinationResponse429
    | DeleteDestinationResponse500
    | None
):
    """Delete destination

     Remove a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteDestinationResponse401 | DeleteDestinationResponse403 | DeleteDestinationResponse404 | DeleteDestinationResponse409 | DeleteDestinationResponse429 | DeleteDestinationResponse500
    """

    return sync_detailed(
        team_id=team_id,
        destination_id=destination_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | DeleteDestinationResponse401
    | DeleteDestinationResponse403
    | DeleteDestinationResponse404
    | DeleteDestinationResponse409
    | DeleteDestinationResponse429
    | DeleteDestinationResponse500
]:
    """Delete destination

     Remove a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteDestinationResponse401 | DeleteDestinationResponse403 | DeleteDestinationResponse404 | DeleteDestinationResponse409 | DeleteDestinationResponse429 | DeleteDestinationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        destination_id=destination_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    destination_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | DeleteDestinationResponse401
    | DeleteDestinationResponse403
    | DeleteDestinationResponse404
    | DeleteDestinationResponse409
    | DeleteDestinationResponse429
    | DeleteDestinationResponse500
    | None
):
    """Delete destination

     Remove a destination

    Args:
        team_id (int):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteDestinationResponse401 | DeleteDestinationResponse403 | DeleteDestinationResponse404 | DeleteDestinationResponse409 | DeleteDestinationResponse429 | DeleteDestinationResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            destination_id=destination_id,
            client=client,
        )
    ).parsed
