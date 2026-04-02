from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datasource_details_response import DatasourceDetailsResponse
from ...models.error_response import ErrorResponse
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
        "url": "/teams/{team_id}/datasource/{data_source_id}".format(
            team_id=quote(str(team_id), safe=""),
            data_source_id=quote(str(data_source_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasourceDetailsResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DatasourceDetailsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

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
) -> Response[DatasourceDetailsResponse | ErrorResponse]:
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
) -> Response[DatasourceDetailsResponse | ErrorResponse]:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasourceDetailsResponse | ErrorResponse]
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
) -> DatasourceDetailsResponse | ErrorResponse | None:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasourceDetailsResponse | ErrorResponse
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
) -> Response[DatasourceDetailsResponse | ErrorResponse]:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasourceDetailsResponse | ErrorResponse]
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
) -> DatasourceDetailsResponse | ErrorResponse | None:
    """Get datasource configuration details

     Retrieve complete configuration details for a data source including report types, settings, and
    authentication requirements

    Args:
        team_id (int):
        data_source_id (str):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasourceDetailsResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            data_source_id=data_source_id,
            client=client,
            sm_app_id=sm_app_id,
        )
    ).parsed
