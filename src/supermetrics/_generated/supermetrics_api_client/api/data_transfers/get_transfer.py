from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_transfer_response_401 import GetTransferResponse401
from ...models.get_transfer_response_403 import GetTransferResponse403
from ...models.get_transfer_response_404 import GetTransferResponse404
from ...models.get_transfer_response_429 import GetTransferResponse429
from ...models.get_transfer_response_500 import GetTransferResponse500
from ...models.transfer_configuration_response import TransferConfigurationResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfers/{transfer_id}".format(
            team_id=quote(str(team_id), safe=""),
            transfer_id=quote(str(transfer_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetTransferResponse401
    | GetTransferResponse403
    | GetTransferResponse404
    | GetTransferResponse429
    | GetTransferResponse500
    | TransferConfigurationResponse
    | None
):
    if response.status_code == 200:
        response_200 = TransferConfigurationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetTransferResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetTransferResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetTransferResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetTransferResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTransferResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetTransferResponse401
    | GetTransferResponse403
    | GetTransferResponse404
    | GetTransferResponse429
    | GetTransferResponse500
    | TransferConfigurationResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    GetTransferResponse401
    | GetTransferResponse403
    | GetTransferResponse404
    | GetTransferResponse429
    | GetTransferResponse500
    | TransferConfigurationResponse
]:
    """Get transfer configuration

     Returns configuration for an existing Hub transfer.

    **Returns:** Full transfer configuration details.

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTransferResponse401 | GetTransferResponse403 | GetTransferResponse404 | GetTransferResponse429 | GetTransferResponse500 | TransferConfigurationResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    GetTransferResponse401
    | GetTransferResponse403
    | GetTransferResponse404
    | GetTransferResponse429
    | GetTransferResponse500
    | TransferConfigurationResponse
    | None
):
    """Get transfer configuration

     Returns configuration for an existing Hub transfer.

    **Returns:** Full transfer configuration details.

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTransferResponse401 | GetTransferResponse403 | GetTransferResponse404 | GetTransferResponse429 | GetTransferResponse500 | TransferConfigurationResponse
    """

    return sync_detailed(
        team_id=team_id,
        transfer_id=transfer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    GetTransferResponse401
    | GetTransferResponse403
    | GetTransferResponse404
    | GetTransferResponse429
    | GetTransferResponse500
    | TransferConfigurationResponse
]:
    """Get transfer configuration

     Returns configuration for an existing Hub transfer.

    **Returns:** Full transfer configuration details.

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTransferResponse401 | GetTransferResponse403 | GetTransferResponse404 | GetTransferResponse429 | GetTransferResponse500 | TransferConfigurationResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    GetTransferResponse401
    | GetTransferResponse403
    | GetTransferResponse404
    | GetTransferResponse429
    | GetTransferResponse500
    | TransferConfigurationResponse
    | None
):
    """Get transfer configuration

     Returns configuration for an existing Hub transfer.

    **Returns:** Full transfer configuration details.

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTransferResponse401 | GetTransferResponse403 | GetTransferResponse404 | GetTransferResponse429 | GetTransferResponse500 | TransferConfigurationResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
        )
    ).parsed
