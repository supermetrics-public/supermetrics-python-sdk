from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backfill_response import BackfillResponse
from ...models.create_backfill_request import CreateBackfillRequest
from ...models.create_backfill_response_400 import CreateBackfillResponse400
from ...models.create_backfill_response_401 import CreateBackfillResponse401
from ...models.create_backfill_response_403 import CreateBackfillResponse403
from ...models.create_backfill_response_422 import CreateBackfillResponse422
from ...models.create_backfill_response_429 import CreateBackfillResponse429
from ...models.create_backfill_response_500 import CreateBackfillResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_id: int,
    *,
    body: CreateBackfillRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/teams/{team_id}/transfers/{transfer_id}/backfills",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    BackfillResponse
    | CreateBackfillResponse400
    | CreateBackfillResponse401
    | CreateBackfillResponse403
    | CreateBackfillResponse422
    | CreateBackfillResponse429
    | CreateBackfillResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = BackfillResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = CreateBackfillResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateBackfillResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CreateBackfillResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = CreateBackfillResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateBackfillResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateBackfillResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BackfillResponse
    | CreateBackfillResponse400
    | CreateBackfillResponse401
    | CreateBackfillResponse403
    | CreateBackfillResponse422
    | CreateBackfillResponse429
    | CreateBackfillResponse500
    | ErrorResponse
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
    body: CreateBackfillRequest,
) -> Response[
    BackfillResponse
    | CreateBackfillResponse400
    | CreateBackfillResponse401
    | CreateBackfillResponse403
    | CreateBackfillResponse422
    | CreateBackfillResponse429
    | CreateBackfillResponse500
    | ErrorResponse
]:
    r"""Create a backfill

     Schedule a new backfill for a specific transfer. A backfill re-processes
    historical data for a specified date range.

    **Returns:** The created backfill object with its ID, status, and progress information.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Requires scope `dwh_transfers_write`
    - Your account must have `dwh.transfer.edit` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - The date range cannot overlap with an existing active backfill
    - Backfills are processed asynchronously
    - The returned backfill object will have status \"CREATED\" initially

    Args:
        team_id (int):
        transfer_id (int):
        body (CreateBackfillRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackfillResponse | CreateBackfillResponse400 | CreateBackfillResponse401 | CreateBackfillResponse403 | CreateBackfillResponse422 | CreateBackfillResponse429 | CreateBackfillResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
        body=body,
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
    body: CreateBackfillRequest,
) -> (
    BackfillResponse
    | CreateBackfillResponse400
    | CreateBackfillResponse401
    | CreateBackfillResponse403
    | CreateBackfillResponse422
    | CreateBackfillResponse429
    | CreateBackfillResponse500
    | ErrorResponse
    | None
):
    r"""Create a backfill

     Schedule a new backfill for a specific transfer. A backfill re-processes
    historical data for a specified date range.

    **Returns:** The created backfill object with its ID, status, and progress information.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Requires scope `dwh_transfers_write`
    - Your account must have `dwh.transfer.edit` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - The date range cannot overlap with an existing active backfill
    - Backfills are processed asynchronously
    - The returned backfill object will have status \"CREATED\" initially

    Args:
        team_id (int):
        transfer_id (int):
        body (CreateBackfillRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackfillResponse | CreateBackfillResponse400 | CreateBackfillResponse401 | CreateBackfillResponse403 | CreateBackfillResponse422 | CreateBackfillResponse429 | CreateBackfillResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        transfer_id=transfer_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateBackfillRequest,
) -> Response[
    BackfillResponse
    | CreateBackfillResponse400
    | CreateBackfillResponse401
    | CreateBackfillResponse403
    | CreateBackfillResponse422
    | CreateBackfillResponse429
    | CreateBackfillResponse500
    | ErrorResponse
]:
    r"""Create a backfill

     Schedule a new backfill for a specific transfer. A backfill re-processes
    historical data for a specified date range.

    **Returns:** The created backfill object with its ID, status, and progress information.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Requires scope `dwh_transfers_write`
    - Your account must have `dwh.transfer.edit` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - The date range cannot overlap with an existing active backfill
    - Backfills are processed asynchronously
    - The returned backfill object will have status \"CREATED\" initially

    Args:
        team_id (int):
        transfer_id (int):
        body (CreateBackfillRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackfillResponse | CreateBackfillResponse400 | CreateBackfillResponse401 | CreateBackfillResponse403 | CreateBackfillResponse422 | CreateBackfillResponse429 | CreateBackfillResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateBackfillRequest,
) -> (
    BackfillResponse
    | CreateBackfillResponse400
    | CreateBackfillResponse401
    | CreateBackfillResponse403
    | CreateBackfillResponse422
    | CreateBackfillResponse429
    | CreateBackfillResponse500
    | ErrorResponse
    | None
):
    r"""Create a backfill

     Schedule a new backfill for a specific transfer. A backfill re-processes
    historical data for a specified date range.

    **Returns:** The created backfill object with its ID, status, and progress information.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Requires scope `dwh_transfers_write`
    - Your account must have `dwh.transfer.edit` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - The date range cannot overlap with an existing active backfill
    - Backfills are processed asynchronously
    - The returned backfill object will have status \"CREATED\" initially

    Args:
        team_id (int):
        transfer_id (int):
        body (CreateBackfillRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackfillResponse | CreateBackfillResponse400 | CreateBackfillResponse401 | CreateBackfillResponse403 | CreateBackfillResponse422 | CreateBackfillResponse429 | CreateBackfillResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
            body=body,
        )
    ).parsed
