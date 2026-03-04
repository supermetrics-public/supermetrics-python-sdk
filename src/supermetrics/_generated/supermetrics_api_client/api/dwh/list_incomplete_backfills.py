from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_incomplete_backfills_response_200 import ListIncompleteBackfillsResponse200
from ...models.list_incomplete_backfills_response_401 import ListIncompleteBackfillsResponse401
from ...models.list_incomplete_backfills_response_403 import ListIncompleteBackfillsResponse403
from ...models.list_incomplete_backfills_response_429 import ListIncompleteBackfillsResponse429
from ...models.list_incomplete_backfills_response_500 import ListIncompleteBackfillsResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/backfills".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ListIncompleteBackfillsResponse200
    | ListIncompleteBackfillsResponse401
    | ListIncompleteBackfillsResponse403
    | ListIncompleteBackfillsResponse429
    | ListIncompleteBackfillsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ListIncompleteBackfillsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListIncompleteBackfillsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListIncompleteBackfillsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ListIncompleteBackfillsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListIncompleteBackfillsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ListIncompleteBackfillsResponse200
    | ListIncompleteBackfillsResponse401
    | ListIncompleteBackfillsResponse403
    | ListIncompleteBackfillsResponse429
    | ListIncompleteBackfillsResponse500
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
    ListIncompleteBackfillsResponse200
    | ListIncompleteBackfillsResponse401
    | ListIncompleteBackfillsResponse403
    | ListIncompleteBackfillsResponse429
    | ListIncompleteBackfillsResponse500
]:
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - You must have `dwh.transfer.view` permission
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListIncompleteBackfillsResponse200 | ListIncompleteBackfillsResponse401 | ListIncompleteBackfillsResponse403 | ListIncompleteBackfillsResponse429 | ListIncompleteBackfillsResponse500]
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
    ListIncompleteBackfillsResponse200
    | ListIncompleteBackfillsResponse401
    | ListIncompleteBackfillsResponse403
    | ListIncompleteBackfillsResponse429
    | ListIncompleteBackfillsResponse500
    | None
):
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - You must have `dwh.transfer.view` permission
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListIncompleteBackfillsResponse200 | ListIncompleteBackfillsResponse401 | ListIncompleteBackfillsResponse403 | ListIncompleteBackfillsResponse429 | ListIncompleteBackfillsResponse500
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
    ListIncompleteBackfillsResponse200
    | ListIncompleteBackfillsResponse401
    | ListIncompleteBackfillsResponse403
    | ListIncompleteBackfillsResponse429
    | ListIncompleteBackfillsResponse500
]:
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - You must have `dwh.transfer.view` permission
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListIncompleteBackfillsResponse200 | ListIncompleteBackfillsResponse401 | ListIncompleteBackfillsResponse403 | ListIncompleteBackfillsResponse429 | ListIncompleteBackfillsResponse500]
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
    ListIncompleteBackfillsResponse200
    | ListIncompleteBackfillsResponse401
    | ListIncompleteBackfillsResponse403
    | ListIncompleteBackfillsResponse429
    | ListIncompleteBackfillsResponse500
    | None
):
    r"""List incomplete backfills for team

     Retrieve a list of all incomplete backfills for your team.
    This endpoint returns only backfills that are not yet finished.

    **What are \"incomplete\" backfills?**
    - **Included:** Backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`
    - **Excluded:** Backfills with status `COMPLETED` or `CANCELLED`

    **Returns:** Array of backfill objects sorted by creation time (newest first).

    **Important Notes:**
    - You must have `dwh.transfer.view` permission
    - Only backfills belonging to your team are returned
    - The list includes backfills for all transfers in your team
    - Each backfill includes real-time progress tracking for running backfills

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListIncompleteBackfillsResponse200 | ListIncompleteBackfillsResponse401 | ListIncompleteBackfillsResponse403 | ListIncompleteBackfillsResponse429 | ListIncompleteBackfillsResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
