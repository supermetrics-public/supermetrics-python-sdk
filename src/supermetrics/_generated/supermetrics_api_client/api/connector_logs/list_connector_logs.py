import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_connector_logs_response_200 import ListConnectorLogsResponse200
from ...models.list_connector_logs_response_400 import ListConnectorLogsResponse400
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
    *,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    json_before: str | Unset = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400 | None:
    if response.status_code == 200:
        response_200 = ListConnectorLogsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ListConnectorLogsResponse400.from_dict(response.json())

        return response_400

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
) -> Response[ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
) -> Response[ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400]:
    """List connector logs

     Fetch execution logs for a connector. Returns logs in reverse chronological order.

    Args:
        team_id (int):
        connector_identifier (str):
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        limit=limit,
        before=before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
) -> ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400 | None:
    """List connector logs

     Fetch execution logs for a connector. Returns logs in reverse chronological order.

    Args:
        team_id (int):
        connector_identifier (str):
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400
    """

    return sync_detailed(
        team_id=team_id,
        connector_identifier=connector_identifier,
        client=client,
        limit=limit,
        before=before,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
) -> Response[ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400]:
    """List connector logs

     Fetch execution logs for a connector. Returns logs in reverse chronological order.

    Args:
        team_id (int):
        connector_identifier (str):
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        limit=limit,
        before=before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
) -> ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400 | None:
    """List connector logs

     Fetch execution logs for a connector. Returns logs in reverse chronological order.

    Args:
        team_id (int):
        connector_identifier (str):
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListConnectorLogsResponse200 | ListConnectorLogsResponse400
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            client=client,
            limit=limit,
            before=before,
        )
    ).parsed
