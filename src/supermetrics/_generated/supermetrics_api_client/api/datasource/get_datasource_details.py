from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import ApiError
from ...models.datasource_details_response import DatasourceDetailsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    data_source_id: str,
    *,
    sm_app_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(sm_app_id, Unset):
        headers["Sm-App-Id"] = sm_app_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/teams/{team_id}/datasource/{data_source_id}",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiError | DatasourceDetailsResponse | None:
    if response.status_code == 200:
        response_200 = DatasourceDetailsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiError.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ApiError.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ApiError.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ApiError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiError | DatasourceDetailsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    data_source_id: str,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> Response[ApiError | DatasourceDetailsResponse]:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements.

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | DatasourceDetailsResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        data_source_id=data_source_id,
        sm_app_id=sm_app_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    data_source_id: str,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> ApiError | DatasourceDetailsResponse | None:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements.

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | DatasourceDetailsResponse
    """

    return sync_detailed(
        team_id=team_id,
        data_source_id=data_source_id,
        client=client,
        sm_app_id=sm_app_id,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    data_source_id: str,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> Response[ApiError | DatasourceDetailsResponse]:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements.

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiError | DatasourceDetailsResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        data_source_id=data_source_id,
        sm_app_id=sm_app_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    data_source_id: str,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> ApiError | DatasourceDetailsResponse | None:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements.

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiError | DatasourceDetailsResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            data_source_id=data_source_id,
            client=client,
            sm_app_id=sm_app_id,
        )
    ).parsed
