from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_transfers_response_401 import ListTransfersResponse401
from ...models.list_transfers_response_403 import ListTransfersResponse403
from ...models.list_transfers_response_429 import ListTransfersResponse429
from ...models.list_transfers_response_500 import ListTransfersResponse500
from ...models.transfer_list_response import TransferListResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfers".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ListTransfersResponse401
    | ListTransfersResponse403
    | ListTransfersResponse429
    | ListTransfersResponse500
    | TransferListResponse
    | None
):
    if response.status_code == 200:
        response_200 = TransferListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListTransfersResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListTransfersResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ListTransfersResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListTransfersResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ListTransfersResponse401
    | ListTransfersResponse403
    | ListTransfersResponse429
    | ListTransfersResponse500
    | TransferListResponse
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
) -> Response[
    ListTransfersResponse401
    | ListTransfersResponse403
    | ListTransfersResponse429
    | ListTransfersResponse500
    | TransferListResponse
]:
    """List transfers

     Retrieve list of transfers for the authenticated team.

    **Returns:** Array of transfer objects with basic information.

    **Important Notes:**
    - Returns only non-deleted transfers belonging to your team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListTransfersResponse401 | ListTransfersResponse403 | ListTransfersResponse429 | ListTransfersResponse500 | TransferListResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    ListTransfersResponse401
    | ListTransfersResponse403
    | ListTransfersResponse429
    | ListTransfersResponse500
    | TransferListResponse
    | None
):
    """List transfers

     Retrieve list of transfers for the authenticated team.

    **Returns:** Array of transfer objects with basic information.

    **Important Notes:**
    - Returns only non-deleted transfers belonging to your team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListTransfersResponse401 | ListTransfersResponse403 | ListTransfersResponse429 | ListTransfersResponse500 | TransferListResponse
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    ListTransfersResponse401
    | ListTransfersResponse403
    | ListTransfersResponse429
    | ListTransfersResponse500
    | TransferListResponse
]:
    """List transfers

     Retrieve list of transfers for the authenticated team.

    **Returns:** Array of transfer objects with basic information.

    **Important Notes:**
    - Returns only non-deleted transfers belonging to your team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListTransfersResponse401 | ListTransfersResponse403 | ListTransfersResponse429 | ListTransfersResponse500 | TransferListResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    ListTransfersResponse401
    | ListTransfersResponse403
    | ListTransfersResponse429
    | ListTransfersResponse500
    | TransferListResponse
    | None
):
    """List transfers

     Retrieve list of transfers for the authenticated team.

    **Returns:** Array of transfer objects with basic information.

    **Important Notes:**
    - Returns only non-deleted transfers belonging to your team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListTransfersResponse401 | ListTransfersResponse403 | ListTransfersResponse429 | ListTransfersResponse500 | TransferListResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
