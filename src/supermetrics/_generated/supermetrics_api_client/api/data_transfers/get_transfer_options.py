from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_transfer_options_response_401 import GetTransferOptionsResponse401
from ...models.get_transfer_options_response_403 import GetTransferOptionsResponse403
from ...models.get_transfer_options_response_429 import GetTransferOptionsResponse429
from ...models.get_transfer_options_response_500 import GetTransferOptionsResponse500
from ...models.transfer_options_response import TransferOptionsResponse
from ...types import UNSET, Response


def _get_kwargs(
    team_id: int,
    *,
    source_id: str,
    destination_id: int,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["source_id"] = source_id

    params["destination_id"] = destination_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfers/available-options".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetTransferOptionsResponse401
    | GetTransferOptionsResponse403
    | GetTransferOptionsResponse429
    | GetTransferOptionsResponse500
    | TransferOptionsResponse
    | None
):
    if response.status_code == 200:
        response_200 = TransferOptionsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetTransferOptionsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetTransferOptionsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = GetTransferOptionsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTransferOptionsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetTransferOptionsResponse401
    | GetTransferOptionsResponse403
    | GetTransferOptionsResponse429
    | GetTransferOptionsResponse500
    | TransferOptionsResponse
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
    source_id: str,
    destination_id: int,
) -> Response[
    GetTransferOptionsResponse401
    | GetTransferOptionsResponse403
    | GetTransferOptionsResponse429
    | GetTransferOptionsResponse500
    | TransferOptionsResponse
]:
    """Get transfer options

     Returns all available options for a Hub transfer, according to specific data source and destination.

    **Returns:** Transfer configuration parameters for the given source/destination combination.

    Args:
        team_id (int):
        source_id (str):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTransferOptionsResponse401 | GetTransferOptionsResponse403 | GetTransferOptionsResponse429 | GetTransferOptionsResponse500 | TransferOptionsResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        source_id=source_id,
        destination_id=destination_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    source_id: str,
    destination_id: int,
) -> (
    GetTransferOptionsResponse401
    | GetTransferOptionsResponse403
    | GetTransferOptionsResponse429
    | GetTransferOptionsResponse500
    | TransferOptionsResponse
    | None
):
    """Get transfer options

     Returns all available options for a Hub transfer, according to specific data source and destination.

    **Returns:** Transfer configuration parameters for the given source/destination combination.

    Args:
        team_id (int):
        source_id (str):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTransferOptionsResponse401 | GetTransferOptionsResponse403 | GetTransferOptionsResponse429 | GetTransferOptionsResponse500 | TransferOptionsResponse
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        source_id=source_id,
        destination_id=destination_id,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    source_id: str,
    destination_id: int,
) -> Response[
    GetTransferOptionsResponse401
    | GetTransferOptionsResponse403
    | GetTransferOptionsResponse429
    | GetTransferOptionsResponse500
    | TransferOptionsResponse
]:
    """Get transfer options

     Returns all available options for a Hub transfer, according to specific data source and destination.

    **Returns:** Transfer configuration parameters for the given source/destination combination.

    Args:
        team_id (int):
        source_id (str):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTransferOptionsResponse401 | GetTransferOptionsResponse403 | GetTransferOptionsResponse429 | GetTransferOptionsResponse500 | TransferOptionsResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        source_id=source_id,
        destination_id=destination_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    source_id: str,
    destination_id: int,
) -> (
    GetTransferOptionsResponse401
    | GetTransferOptionsResponse403
    | GetTransferOptionsResponse429
    | GetTransferOptionsResponse500
    | TransferOptionsResponse
    | None
):
    """Get transfer options

     Returns all available options for a Hub transfer, according to specific data source and destination.

    **Returns:** Transfer configuration parameters for the given source/destination combination.

    Args:
        team_id (int):
        source_id (str):
        destination_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTransferOptionsResponse401 | GetTransferOptionsResponse403 | GetTransferOptionsResponse429 | GetTransferOptionsResponse500 | TransferOptionsResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            source_id=source_id,
            destination_id=destination_id,
        )
    ).parsed
