from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_backfill_by_id_response_401 import GetBackfillByIdResponse401
from ...models.get_backfill_by_id_response_403 import GetBackfillByIdResponse403
from ...models.get_backfill_by_id_response_429 import GetBackfillByIdResponse429
from ...models.get_backfill_by_id_response_500 import GetBackfillByIdResponse500
from ...models.get_backfill_response import GetBackfillResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    backfill_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/backfills/{backfill_id}".format(
            team_id=quote(str(team_id), safe=""),
            backfill_id=quote(str(backfill_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | GetBackfillByIdResponse401
    | GetBackfillByIdResponse403
    | GetBackfillByIdResponse429
    | GetBackfillByIdResponse500
    | GetBackfillResponse
    | None
):
    if response.status_code == 200:
        response_200 = GetBackfillResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetBackfillByIdResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetBackfillByIdResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetBackfillByIdResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetBackfillByIdResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | GetBackfillByIdResponse401
    | GetBackfillByIdResponse403
    | GetBackfillByIdResponse429
    | GetBackfillByIdResponse500
    | GetBackfillResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    backfill_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | GetBackfillByIdResponse401
    | GetBackfillByIdResponse403
    | GetBackfillByIdResponse429
    | GetBackfillByIdResponse500
    | GetBackfillResponse
]:
    """Get backfill by ID

     Retrieve detailed information about a specific backfill using its unique identifier.
    This endpoint returns the complete backfill object with current status, progress tracking, and error
    details.

    **Returns:** The backfill object with its ID, status, progress information, and error details if
    any.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if the backfill does not exist or does not belong to your team
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        backfill_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetBackfillByIdResponse401 | GetBackfillByIdResponse403 | GetBackfillByIdResponse429 | GetBackfillByIdResponse500 | GetBackfillResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        backfill_id=backfill_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    backfill_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | GetBackfillByIdResponse401
    | GetBackfillByIdResponse403
    | GetBackfillByIdResponse429
    | GetBackfillByIdResponse500
    | GetBackfillResponse
    | None
):
    """Get backfill by ID

     Retrieve detailed information about a specific backfill using its unique identifier.
    This endpoint returns the complete backfill object with current status, progress tracking, and error
    details.

    **Returns:** The backfill object with its ID, status, progress information, and error details if
    any.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if the backfill does not exist or does not belong to your team
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        backfill_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetBackfillByIdResponse401 | GetBackfillByIdResponse403 | GetBackfillByIdResponse429 | GetBackfillByIdResponse500 | GetBackfillResponse
    """

    return sync_detailed(
        team_id=team_id,
        backfill_id=backfill_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    backfill_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | GetBackfillByIdResponse401
    | GetBackfillByIdResponse403
    | GetBackfillByIdResponse429
    | GetBackfillByIdResponse500
    | GetBackfillResponse
]:
    """Get backfill by ID

     Retrieve detailed information about a specific backfill using its unique identifier.
    This endpoint returns the complete backfill object with current status, progress tracking, and error
    details.

    **Returns:** The backfill object with its ID, status, progress information, and error details if
    any.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if the backfill does not exist or does not belong to your team
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        backfill_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetBackfillByIdResponse401 | GetBackfillByIdResponse403 | GetBackfillByIdResponse429 | GetBackfillByIdResponse500 | GetBackfillResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        backfill_id=backfill_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    backfill_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | GetBackfillByIdResponse401
    | GetBackfillByIdResponse403
    | GetBackfillByIdResponse429
    | GetBackfillByIdResponse500
    | GetBackfillResponse
    | None
):
    """Get backfill by ID

     Retrieve detailed information about a specific backfill using its unique identifier.
    This endpoint returns the complete backfill object with current status, progress tracking, and error
    details.

    **Returns:** The backfill object with its ID, status, progress information, and error details if
    any.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.view` permission
    - Returns 404 if the backfill does not exist or does not belong to your team
    - The backfill object includes real-time progress tracking for running backfills

    Args:
        team_id (int):
        backfill_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetBackfillByIdResponse401 | GetBackfillByIdResponse403 | GetBackfillByIdResponse429 | GetBackfillByIdResponse500 | GetBackfillResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            backfill_id=backfill_id,
            client=client,
        )
    ).parsed
