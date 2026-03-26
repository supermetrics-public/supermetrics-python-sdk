from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_backfill_response import GetBackfillResponse
from ...models.get_latest_backfill_response_401 import GetLatestBackfillResponse401
from ...models.get_latest_backfill_response_403 import GetLatestBackfillResponse403
from ...models.get_latest_backfill_response_429 import GetLatestBackfillResponse429
from ...models.get_latest_backfill_response_500 import GetLatestBackfillResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfers/{transfer_id}/backfills/latest".format(
            team_id=quote(str(team_id), safe=""),
            transfer_id=quote(str(transfer_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | GetBackfillResponse
    | GetLatestBackfillResponse401
    | GetLatestBackfillResponse403
    | GetLatestBackfillResponse429
    | GetLatestBackfillResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetBackfillResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetLatestBackfillResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetLatestBackfillResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetLatestBackfillResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetLatestBackfillResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | GetBackfillResponse
    | GetLatestBackfillResponse401
    | GetLatestBackfillResponse403
    | GetLatestBackfillResponse429
    | GetLatestBackfillResponse500
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
    ErrorResponse
    | GetBackfillResponse
    | GetLatestBackfillResponse401
    | GetLatestBackfillResponse403
    | GetLatestBackfillResponse429
    | GetLatestBackfillResponse500
]:
    """Get latest backfill for a transfer

     Retrieve information about the most recent backfill for a specific transfer.
    This endpoint returns the latest backfill regardless of its status (pending, running, completed,
    failed, or cancelled).

    **Returns:** The latest backfill object with its ID, status, progress information, and error details
    if any.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if no backfill has ever been created for this transfer
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetBackfillResponse | GetLatestBackfillResponse401 | GetLatestBackfillResponse403 | GetLatestBackfillResponse429 | GetLatestBackfillResponse500]
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
    ErrorResponse
    | GetBackfillResponse
    | GetLatestBackfillResponse401
    | GetLatestBackfillResponse403
    | GetLatestBackfillResponse429
    | GetLatestBackfillResponse500
    | None
):
    """Get latest backfill for a transfer

     Retrieve information about the most recent backfill for a specific transfer.
    This endpoint returns the latest backfill regardless of its status (pending, running, completed,
    failed, or cancelled).

    **Returns:** The latest backfill object with its ID, status, progress information, and error details
    if any.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if no backfill has ever been created for this transfer
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetBackfillResponse | GetLatestBackfillResponse401 | GetLatestBackfillResponse403 | GetLatestBackfillResponse429 | GetLatestBackfillResponse500
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
    ErrorResponse
    | GetBackfillResponse
    | GetLatestBackfillResponse401
    | GetLatestBackfillResponse403
    | GetLatestBackfillResponse429
    | GetLatestBackfillResponse500
]:
    """Get latest backfill for a transfer

     Retrieve information about the most recent backfill for a specific transfer.
    This endpoint returns the latest backfill regardless of its status (pending, running, completed,
    failed, or cancelled).

    **Returns:** The latest backfill object with its ID, status, progress information, and error details
    if any.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if no backfill has ever been created for this transfer
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetBackfillResponse | GetLatestBackfillResponse401 | GetLatestBackfillResponse403 | GetLatestBackfillResponse429 | GetLatestBackfillResponse500]
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
    ErrorResponse
    | GetBackfillResponse
    | GetLatestBackfillResponse401
    | GetLatestBackfillResponse403
    | GetLatestBackfillResponse429
    | GetLatestBackfillResponse500
    | None
):
    """Get latest backfill for a transfer

     Retrieve information about the most recent backfill for a specific transfer.
    This endpoint returns the latest backfill regardless of its status (pending, running, completed,
    failed, or cancelled).

    **Returns:** The latest backfill object with its ID, status, progress information, and error details
    if any.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if no backfill has ever been created for this transfer
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetBackfillResponse | GetLatestBackfillResponse401 | GetLatestBackfillResponse403 | GetLatestBackfillResponse429 | GetLatestBackfillResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
        )
    ).parsed
