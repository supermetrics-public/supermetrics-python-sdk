from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_transfer_run_response_401 import GetTransferRunResponse401
from ...models.get_transfer_run_response_403 import GetTransferRunResponse403
from ...models.get_transfer_run_response_404 import GetTransferRunResponse404
from ...models.get_transfer_run_response_429 import GetTransferRunResponse429
from ...models.get_transfer_run_response_500 import GetTransferRunResponse500
from ...models.transfer_run_detail_response import TransferRunDetailResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_run_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfer_runs/{transfer_run_id}".format(
            team_id=quote(str(team_id), safe=""),
            transfer_run_id=quote(str(transfer_run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetTransferRunResponse401
    | GetTransferRunResponse403
    | GetTransferRunResponse404
    | GetTransferRunResponse429
    | GetTransferRunResponse500
    | TransferRunDetailResponse
    | None
):
    if response.status_code == 200:
        response_200 = TransferRunDetailResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetTransferRunResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetTransferRunResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetTransferRunResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetTransferRunResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetTransferRunResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetTransferRunResponse401
    | GetTransferRunResponse403
    | GetTransferRunResponse404
    | GetTransferRunResponse429
    | GetTransferRunResponse500
    | TransferRunDetailResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    transfer_run_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    GetTransferRunResponse401
    | GetTransferRunResponse403
    | GetTransferRunResponse404
    | GetTransferRunResponse429
    | GetTransferRunResponse500
    | TransferRunDetailResponse
]:
    """Get transfer run details

     Retrieve detailed information about a specific transfer run, including status,
    timestamps, duration, row counts, and per-query execution details.

    **Returns:** The transfer run object with its ID, status, timing information, and query details.

    **Important Notes:**
    - The transfer run must exist and belong to your team
    - Returns 404 if the transfer run does not exist or does not belong to your team

    Args:
        team_id (int):
        transfer_run_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTransferRunResponse401 | GetTransferRunResponse403 | GetTransferRunResponse404 | GetTransferRunResponse429 | GetTransferRunResponse500 | TransferRunDetailResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_run_id=transfer_run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    transfer_run_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    GetTransferRunResponse401
    | GetTransferRunResponse403
    | GetTransferRunResponse404
    | GetTransferRunResponse429
    | GetTransferRunResponse500
    | TransferRunDetailResponse
    | None
):
    """Get transfer run details

     Retrieve detailed information about a specific transfer run, including status,
    timestamps, duration, row counts, and per-query execution details.

    **Returns:** The transfer run object with its ID, status, timing information, and query details.

    **Important Notes:**
    - The transfer run must exist and belong to your team
    - Returns 404 if the transfer run does not exist or does not belong to your team

    Args:
        team_id (int):
        transfer_run_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTransferRunResponse401 | GetTransferRunResponse403 | GetTransferRunResponse404 | GetTransferRunResponse429 | GetTransferRunResponse500 | TransferRunDetailResponse
    """

    return sync_detailed(
        team_id=team_id,
        transfer_run_id=transfer_run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    transfer_run_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    GetTransferRunResponse401
    | GetTransferRunResponse403
    | GetTransferRunResponse404
    | GetTransferRunResponse429
    | GetTransferRunResponse500
    | TransferRunDetailResponse
]:
    """Get transfer run details

     Retrieve detailed information about a specific transfer run, including status,
    timestamps, duration, row counts, and per-query execution details.

    **Returns:** The transfer run object with its ID, status, timing information, and query details.

    **Important Notes:**
    - The transfer run must exist and belong to your team
    - Returns 404 if the transfer run does not exist or does not belong to your team

    Args:
        team_id (int):
        transfer_run_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTransferRunResponse401 | GetTransferRunResponse403 | GetTransferRunResponse404 | GetTransferRunResponse429 | GetTransferRunResponse500 | TransferRunDetailResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_run_id=transfer_run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    transfer_run_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    GetTransferRunResponse401
    | GetTransferRunResponse403
    | GetTransferRunResponse404
    | GetTransferRunResponse429
    | GetTransferRunResponse500
    | TransferRunDetailResponse
    | None
):
    """Get transfer run details

     Retrieve detailed information about a specific transfer run, including status,
    timestamps, duration, row counts, and per-query execution details.

    **Returns:** The transfer run object with its ID, status, timing information, and query details.

    **Important Notes:**
    - The transfer run must exist and belong to your team
    - Returns 404 if the transfer run does not exist or does not belong to your team

    Args:
        team_id (int):
        transfer_run_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTransferRunResponse401 | GetTransferRunResponse403 | GetTransferRunResponse404 | GetTransferRunResponse429 | GetTransferRunResponse500 | TransferRunDetailResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_run_id=transfer_run_id,
            client=client,
        )
    ).parsed
