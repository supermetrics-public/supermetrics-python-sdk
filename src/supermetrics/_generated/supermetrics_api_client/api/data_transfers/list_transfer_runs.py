import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_transfer_runs_response_401 import ListTransferRunsResponse401
from ...models.list_transfer_runs_response_403 import ListTransferRunsResponse403
from ...models.list_transfer_runs_response_429 import ListTransferRunsResponse429
from ...models.list_transfer_runs_response_500 import ListTransferRunsResponse500
from ...models.list_transfer_runs_sort_direction import (
    ListTransferRunsSortDirection,
)
from ...models.list_transfer_runs_sort_field import ListTransferRunsSortField
from ...models.transfer_run_list_response import TransferRunListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    transfer_id: int,
    *,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    filter_issues_only: bool | Unset = UNSET,
    sort_field: ListTransferRunsSortField | Unset = UNSET,
    sort_direction: ListTransferRunsSortDirection | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params["filter_issues_only"] = filter_issues_only

    json_sort_field: str | Unset = UNSET
    if not isinstance(sort_field, Unset):
        json_sort_field = sort_field

    params["sort_field"] = json_sort_field

    json_sort_direction: str | Unset = UNSET
    if not isinstance(sort_direction, Unset):
        json_sort_direction = sort_direction

    params["sort_direction"] = json_sort_direction

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/teams/{team_id}/transfers/{transfer_id}/runs".format(
            team_id=quote(str(team_id), safe=""),
            transfer_id=quote(str(transfer_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ListTransferRunsResponse401
    | ListTransferRunsResponse403
    | ListTransferRunsResponse429
    | ListTransferRunsResponse500
    | TransferRunListResponse
    | None
):
    if response.status_code == 200:
        response_200 = TransferRunListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListTransferRunsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListTransferRunsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ListTransferRunsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListTransferRunsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ListTransferRunsResponse401
    | ListTransferRunsResponse403
    | ListTransferRunsResponse429
    | ListTransferRunsResponse500
    | TransferRunListResponse
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
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    filter_issues_only: bool | Unset = UNSET,
    sort_field: ListTransferRunsSortField | Unset = UNSET,
    sort_direction: ListTransferRunsSortDirection | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[
    ListTransferRunsResponse401
    | ListTransferRunsResponse403
    | ListTransferRunsResponse429
    | ListTransferRunsResponse500
    | TransferRunListResponse
]:
    """List transfer runs

     Retrieve a paginated, filterable list of transfer runs for a specific transfer.
    Supports date range filtering, issue filtering, sorting, and pagination.

    **Returns:** Array of transfer run objects.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Start date and end date are required parameters
    - Results are paginated (default limit: 100, max: 10000)

    Args:
        team_id (int):
        transfer_id (int):
        start_date (datetime.datetime):
        end_date (datetime.datetime):
        filter_issues_only (bool | Unset):
        sort_field (ListTransferRunsSortField | Unset):
        sort_direction (ListTransferRunsSortDirection | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListTransferRunsResponse401 | ListTransferRunsResponse403 | ListTransferRunsResponse429 | ListTransferRunsResponse500 | TransferRunListResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
        start_date=start_date,
        end_date=end_date,
        filter_issues_only=filter_issues_only,
        sort_field=sort_field,
        sort_direction=sort_direction,
        limit=limit,
        offset=offset,
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
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    filter_issues_only: bool | Unset = UNSET,
    sort_field: ListTransferRunsSortField | Unset = UNSET,
    sort_direction: ListTransferRunsSortDirection | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> (
    ListTransferRunsResponse401
    | ListTransferRunsResponse403
    | ListTransferRunsResponse429
    | ListTransferRunsResponse500
    | TransferRunListResponse
    | None
):
    """List transfer runs

     Retrieve a paginated, filterable list of transfer runs for a specific transfer.
    Supports date range filtering, issue filtering, sorting, and pagination.

    **Returns:** Array of transfer run objects.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Start date and end date are required parameters
    - Results are paginated (default limit: 100, max: 10000)

    Args:
        team_id (int):
        transfer_id (int):
        start_date (datetime.datetime):
        end_date (datetime.datetime):
        filter_issues_only (bool | Unset):
        sort_field (ListTransferRunsSortField | Unset):
        sort_direction (ListTransferRunsSortDirection | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListTransferRunsResponse401 | ListTransferRunsResponse403 | ListTransferRunsResponse429 | ListTransferRunsResponse500 | TransferRunListResponse
    """

    return sync_detailed(
        team_id=team_id,
        transfer_id=transfer_id,
        client=client,
        start_date=start_date,
        end_date=end_date,
        filter_issues_only=filter_issues_only,
        sort_field=sort_field,
        sort_direction=sort_direction,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    filter_issues_only: bool | Unset = UNSET,
    sort_field: ListTransferRunsSortField | Unset = UNSET,
    sort_direction: ListTransferRunsSortDirection | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[
    ListTransferRunsResponse401
    | ListTransferRunsResponse403
    | ListTransferRunsResponse429
    | ListTransferRunsResponse500
    | TransferRunListResponse
]:
    """List transfer runs

     Retrieve a paginated, filterable list of transfer runs for a specific transfer.
    Supports date range filtering, issue filtering, sorting, and pagination.

    **Returns:** Array of transfer run objects.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Start date and end date are required parameters
    - Results are paginated (default limit: 100, max: 10000)

    Args:
        team_id (int):
        transfer_id (int):
        start_date (datetime.datetime):
        end_date (datetime.datetime):
        filter_issues_only (bool | Unset):
        sort_field (ListTransferRunsSortField | Unset):
        sort_direction (ListTransferRunsSortDirection | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListTransferRunsResponse401 | ListTransferRunsResponse403 | ListTransferRunsResponse429 | ListTransferRunsResponse500 | TransferRunListResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
        start_date=start_date,
        end_date=end_date,
        filter_issues_only=filter_issues_only,
        sort_field=sort_field,
        sort_direction=sort_direction,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    filter_issues_only: bool | Unset = UNSET,
    sort_field: ListTransferRunsSortField | Unset = UNSET,
    sort_direction: ListTransferRunsSortDirection | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> (
    ListTransferRunsResponse401
    | ListTransferRunsResponse403
    | ListTransferRunsResponse429
    | ListTransferRunsResponse500
    | TransferRunListResponse
    | None
):
    """List transfer runs

     Retrieve a paginated, filterable list of transfer runs for a specific transfer.
    Supports date range filtering, issue filtering, sorting, and pagination.

    **Returns:** Array of transfer run objects.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Start date and end date are required parameters
    - Results are paginated (default limit: 100, max: 10000)

    Args:
        team_id (int):
        transfer_id (int):
        start_date (datetime.datetime):
        end_date (datetime.datetime):
        filter_issues_only (bool | Unset):
        sort_field (ListTransferRunsSortField | Unset):
        sort_direction (ListTransferRunsSortDirection | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListTransferRunsResponse401 | ListTransferRunsResponse403 | ListTransferRunsResponse429 | ListTransferRunsResponse500 | TransferRunListResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
            start_date=start_date,
            end_date=end_date,
            filter_issues_only=filter_issues_only,
            sort_field=sort_field,
            sort_direction=sort_direction,
            limit=limit,
            offset=offset,
        )
    ).parsed
