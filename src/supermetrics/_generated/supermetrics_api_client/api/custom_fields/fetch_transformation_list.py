from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.fetch_transformation_list_response_400 import FetchTransformationListResponse400
from ...models.fetch_transformation_list_response_401 import FetchTransformationListResponse401
from ...models.fetch_transformation_list_response_429 import FetchTransformationListResponse429
from ...models.fetch_transformation_list_response_500 import FetchTransformationListResponse500
from ...models.paginated_transformations_output import PaginatedTransformationsOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    *,
    data_source_id: str | Unset = UNSET,
    display_name: str | Unset = UNSET,
    page: int | Unset = UNSET,
    limit: int | Unset = 25,
    include_total_count: bool | Unset = UNSET,
    sm_app_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(sm_app_id, Unset):
        headers["Sm-App-Id"] = sm_app_id

    params: dict[str, Any] = {}

    params["data_source_id"] = data_source_id

    params["display_name"] = display_name

    params["page"] = page

    params["limit"] = limit

    params["include_total_count"] = include_total_count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/custom-fields".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | FetchTransformationListResponse400
    | FetchTransformationListResponse401
    | FetchTransformationListResponse429
    | FetchTransformationListResponse500
    | PaginatedTransformationsOutput
    | None
):
    if response.status_code == 200:
        response_200 = PaginatedTransformationsOutput.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FetchTransformationListResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = FetchTransformationListResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = FetchTransformationListResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = FetchTransformationListResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | FetchTransformationListResponse400
    | FetchTransformationListResponse401
    | FetchTransformationListResponse429
    | FetchTransformationListResponse500
    | PaginatedTransformationsOutput
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
    data_source_id: str | Unset = UNSET,
    display_name: str | Unset = UNSET,
    page: int | Unset = UNSET,
    limit: int | Unset = 25,
    include_total_count: bool | Unset = UNSET,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    ErrorResponse
    | FetchTransformationListResponse400
    | FetchTransformationListResponse401
    | FetchTransformationListResponse429
    | FetchTransformationListResponse500
    | PaginatedTransformationsOutput
]:
    """Fetch custom fields list

     Fetch custom fields list

    Args:
        team_id (int):
        data_source_id (str | Unset):
        display_name (str | Unset):
        page (int | Unset):
        limit (int | Unset):  Default: 25.
        include_total_count (bool | Unset):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FetchTransformationListResponse400 | FetchTransformationListResponse401 | FetchTransformationListResponse429 | FetchTransformationListResponse500 | PaginatedTransformationsOutput]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        data_source_id=data_source_id,
        display_name=display_name,
        page=page,
        limit=limit,
        include_total_count=include_total_count,
        sm_app_id=sm_app_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    data_source_id: str | Unset = UNSET,
    display_name: str | Unset = UNSET,
    page: int | Unset = UNSET,
    limit: int | Unset = 25,
    include_total_count: bool | Unset = UNSET,
    sm_app_id: str | Unset = UNSET,
) -> (
    ErrorResponse
    | FetchTransformationListResponse400
    | FetchTransformationListResponse401
    | FetchTransformationListResponse429
    | FetchTransformationListResponse500
    | PaginatedTransformationsOutput
    | None
):
    """Fetch custom fields list

     Fetch custom fields list

    Args:
        team_id (int):
        data_source_id (str | Unset):
        display_name (str | Unset):
        page (int | Unset):
        limit (int | Unset):  Default: 25.
        include_total_count (bool | Unset):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FetchTransformationListResponse400 | FetchTransformationListResponse401 | FetchTransformationListResponse429 | FetchTransformationListResponse500 | PaginatedTransformationsOutput
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        data_source_id=data_source_id,
        display_name=display_name,
        page=page,
        limit=limit,
        include_total_count=include_total_count,
        sm_app_id=sm_app_id,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    data_source_id: str | Unset = UNSET,
    display_name: str | Unset = UNSET,
    page: int | Unset = UNSET,
    limit: int | Unset = 25,
    include_total_count: bool | Unset = UNSET,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    ErrorResponse
    | FetchTransformationListResponse400
    | FetchTransformationListResponse401
    | FetchTransformationListResponse429
    | FetchTransformationListResponse500
    | PaginatedTransformationsOutput
]:
    """Fetch custom fields list

     Fetch custom fields list

    Args:
        team_id (int):
        data_source_id (str | Unset):
        display_name (str | Unset):
        page (int | Unset):
        limit (int | Unset):  Default: 25.
        include_total_count (bool | Unset):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FetchTransformationListResponse400 | FetchTransformationListResponse401 | FetchTransformationListResponse429 | FetchTransformationListResponse500 | PaginatedTransformationsOutput]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        data_source_id=data_source_id,
        display_name=display_name,
        page=page,
        limit=limit,
        include_total_count=include_total_count,
        sm_app_id=sm_app_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    data_source_id: str | Unset = UNSET,
    display_name: str | Unset = UNSET,
    page: int | Unset = UNSET,
    limit: int | Unset = 25,
    include_total_count: bool | Unset = UNSET,
    sm_app_id: str | Unset = UNSET,
) -> (
    ErrorResponse
    | FetchTransformationListResponse400
    | FetchTransformationListResponse401
    | FetchTransformationListResponse429
    | FetchTransformationListResponse500
    | PaginatedTransformationsOutput
    | None
):
    """Fetch custom fields list

     Fetch custom fields list

    Args:
        team_id (int):
        data_source_id (str | Unset):
        display_name (str | Unset):
        page (int | Unset):
        limit (int | Unset):  Default: 25.
        include_total_count (bool | Unset):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FetchTransformationListResponse400 | FetchTransformationListResponse401 | FetchTransformationListResponse429 | FetchTransformationListResponse500 | PaginatedTransformationsOutput
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            data_source_id=data_source_id,
            display_name=display_name,
            page=page,
            limit=limit,
            include_total_count=include_total_count,
            sm_app_id=sm_app_id,
        )
    ).parsed
