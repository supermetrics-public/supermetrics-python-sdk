from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_backfill_response import GetBackfillResponse
from ...models.update_backfill_status_body import UpdateBackfillStatusBody
from ...models.update_backfill_status_response_400 import UpdateBackfillStatusResponse400
from ...models.update_backfill_status_response_401 import UpdateBackfillStatusResponse401
from ...models.update_backfill_status_response_403 import UpdateBackfillStatusResponse403
from ...models.update_backfill_status_response_429 import UpdateBackfillStatusResponse429
from ...models.update_backfill_status_response_500 import UpdateBackfillStatusResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    backfill_id: int,
    *,
    body: UpdateBackfillStatusBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/teams/{team_id}/backfills/{backfill_id}".format(
            team_id=quote(str(team_id), safe=""),
            backfill_id=quote(str(backfill_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | GetBackfillResponse
    | UpdateBackfillStatusResponse400
    | UpdateBackfillStatusResponse401
    | UpdateBackfillStatusResponse403
    | UpdateBackfillStatusResponse429
    | UpdateBackfillStatusResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetBackfillResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateBackfillStatusResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateBackfillStatusResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UpdateBackfillStatusResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateBackfillStatusResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateBackfillStatusResponse500.from_dict(response.json())

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
    | UpdateBackfillStatusResponse400
    | UpdateBackfillStatusResponse401
    | UpdateBackfillStatusResponse403
    | UpdateBackfillStatusResponse429
    | UpdateBackfillStatusResponse500
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
    body: UpdateBackfillStatusBody,
) -> Response[
    ErrorResponse
    | GetBackfillResponse
    | UpdateBackfillStatusResponse400
    | UpdateBackfillStatusResponse401
    | UpdateBackfillStatusResponse403
    | UpdateBackfillStatusResponse429
    | UpdateBackfillStatusResponse500
]:
    r"""Update backfill status

     Update the status of a backfill. Currently, the only supported operation is
    cancelling a backfill by setting status to \"CANCELLED\".

    **What happens when you cancel:**
    - Backfill status is changed to \"CANCELLED\"
    - All pending/queued transfer runs associated with this backfill are cancelled
    - Transfer runs that are already running will complete
    - The backfill's `end_time` is set to the cancellation time
    - The `removed_time` and `removed_user_id` fields are set

    **Important: This endpoint does NOT delete the backfill.**
    - The backfill record remains in the system with status \"CANCELLED\"
    - You can still retrieve the backfill information using GET
    /v1/teams/{team_id}/backfills/{backfill_id}

    **Returns:** The updated backfill object with the new status and updated timestamps.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.edit` permission
    - Only backfills with incomplete status (CREATED, SCHEDULED, RUNNING, FAILED) can be cancelled
    - Returns 404 if the backfill does not exist or does not belong to your team
    - Returns 422 if the backfill cannot be updated (e.g., already in a final state)

    Args:
        team_id (int):
        backfill_id (int):
        body (UpdateBackfillStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetBackfillResponse | UpdateBackfillStatusResponse400 | UpdateBackfillStatusResponse401 | UpdateBackfillStatusResponse403 | UpdateBackfillStatusResponse429 | UpdateBackfillStatusResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        backfill_id=backfill_id,
        body=body,
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
    body: UpdateBackfillStatusBody,
) -> (
    ErrorResponse
    | GetBackfillResponse
    | UpdateBackfillStatusResponse400
    | UpdateBackfillStatusResponse401
    | UpdateBackfillStatusResponse403
    | UpdateBackfillStatusResponse429
    | UpdateBackfillStatusResponse500
    | None
):
    r"""Update backfill status

     Update the status of a backfill. Currently, the only supported operation is
    cancelling a backfill by setting status to \"CANCELLED\".

    **What happens when you cancel:**
    - Backfill status is changed to \"CANCELLED\"
    - All pending/queued transfer runs associated with this backfill are cancelled
    - Transfer runs that are already running will complete
    - The backfill's `end_time` is set to the cancellation time
    - The `removed_time` and `removed_user_id` fields are set

    **Important: This endpoint does NOT delete the backfill.**
    - The backfill record remains in the system with status \"CANCELLED\"
    - You can still retrieve the backfill information using GET
    /v1/teams/{team_id}/backfills/{backfill_id}

    **Returns:** The updated backfill object with the new status and updated timestamps.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.edit` permission
    - Only backfills with incomplete status (CREATED, SCHEDULED, RUNNING, FAILED) can be cancelled
    - Returns 404 if the backfill does not exist or does not belong to your team
    - Returns 422 if the backfill cannot be updated (e.g., already in a final state)

    Args:
        team_id (int):
        backfill_id (int):
        body (UpdateBackfillStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetBackfillResponse | UpdateBackfillStatusResponse400 | UpdateBackfillStatusResponse401 | UpdateBackfillStatusResponse403 | UpdateBackfillStatusResponse429 | UpdateBackfillStatusResponse500
    """

    return sync_detailed(
        team_id=team_id,
        backfill_id=backfill_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    backfill_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateBackfillStatusBody,
) -> Response[
    ErrorResponse
    | GetBackfillResponse
    | UpdateBackfillStatusResponse400
    | UpdateBackfillStatusResponse401
    | UpdateBackfillStatusResponse403
    | UpdateBackfillStatusResponse429
    | UpdateBackfillStatusResponse500
]:
    r"""Update backfill status

     Update the status of a backfill. Currently, the only supported operation is
    cancelling a backfill by setting status to \"CANCELLED\".

    **What happens when you cancel:**
    - Backfill status is changed to \"CANCELLED\"
    - All pending/queued transfer runs associated with this backfill are cancelled
    - Transfer runs that are already running will complete
    - The backfill's `end_time` is set to the cancellation time
    - The `removed_time` and `removed_user_id` fields are set

    **Important: This endpoint does NOT delete the backfill.**
    - The backfill record remains in the system with status \"CANCELLED\"
    - You can still retrieve the backfill information using GET
    /v1/teams/{team_id}/backfills/{backfill_id}

    **Returns:** The updated backfill object with the new status and updated timestamps.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.edit` permission
    - Only backfills with incomplete status (CREATED, SCHEDULED, RUNNING, FAILED) can be cancelled
    - Returns 404 if the backfill does not exist or does not belong to your team
    - Returns 422 if the backfill cannot be updated (e.g., already in a final state)

    Args:
        team_id (int):
        backfill_id (int):
        body (UpdateBackfillStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetBackfillResponse | UpdateBackfillStatusResponse400 | UpdateBackfillStatusResponse401 | UpdateBackfillStatusResponse403 | UpdateBackfillStatusResponse429 | UpdateBackfillStatusResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        backfill_id=backfill_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    backfill_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateBackfillStatusBody,
) -> (
    ErrorResponse
    | GetBackfillResponse
    | UpdateBackfillStatusResponse400
    | UpdateBackfillStatusResponse401
    | UpdateBackfillStatusResponse403
    | UpdateBackfillStatusResponse429
    | UpdateBackfillStatusResponse500
    | None
):
    r"""Update backfill status

     Update the status of a backfill. Currently, the only supported operation is
    cancelling a backfill by setting status to \"CANCELLED\".

    **What happens when you cancel:**
    - Backfill status is changed to \"CANCELLED\"
    - All pending/queued transfer runs associated with this backfill are cancelled
    - Transfer runs that are already running will complete
    - The backfill's `end_time` is set to the cancellation time
    - The `removed_time` and `removed_user_id` fields are set

    **Important: This endpoint does NOT delete the backfill.**
    - The backfill record remains in the system with status \"CANCELLED\"
    - You can still retrieve the backfill information using GET
    /v1/teams/{team_id}/backfills/{backfill_id}

    **Returns:** The updated backfill object with the new status and updated timestamps.

    **Important Notes:**
    - The backfill must exist and belong to your team
    - You must have `dwh.transfer.edit` permission
    - Only backfills with incomplete status (CREATED, SCHEDULED, RUNNING, FAILED) can be cancelled
    - Returns 404 if the backfill does not exist or does not belong to your team
    - Returns 422 if the backfill cannot be updated (e.g., already in a final state)

    Args:
        team_id (int):
        backfill_id (int):
        body (UpdateBackfillStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetBackfillResponse | UpdateBackfillStatusResponse400 | UpdateBackfillStatusResponse401 | UpdateBackfillStatusResponse403 | UpdateBackfillStatusResponse429 | UpdateBackfillStatusResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            backfill_id=backfill_id,
            client=client,
            body=body,
        )
    ).parsed
