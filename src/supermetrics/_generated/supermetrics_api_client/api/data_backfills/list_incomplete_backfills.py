from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_incomplete_backfills_response_200 import ListIncompleteBackfillsResponse200
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/teams/{team_id}/backfills",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ListIncompleteBackfillsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListIncompleteBackfillsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | ListIncompleteBackfillsResponse200]:
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
) -> Response[ErrorResponse | ListIncompleteBackfillsResponse200]:
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - Requires scope `dwh_transfers_read`
    - Your account must have `dwh.transfer.view` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListIncompleteBackfillsResponse200]
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
) -> ErrorResponse | ListIncompleteBackfillsResponse200 | None:
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - Requires scope `dwh_transfers_read`
    - Your account must have `dwh.transfer.view` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListIncompleteBackfillsResponse200
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | ListIncompleteBackfillsResponse200]:
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - Requires scope `dwh_transfers_read`
    - Your account must have `dwh.transfer.view` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListIncompleteBackfillsResponse200]
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
) -> ErrorResponse | ListIncompleteBackfillsResponse200 | None:
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - Requires scope `dwh_transfers_read`
    - Your account must have `dwh.transfer.view` permission. See [roles and
    permissions](https://docs.supermetrics.com/docs/about-supermetrics-teams-and-user-roles#user-roles).
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListIncompleteBackfillsResponse200
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
