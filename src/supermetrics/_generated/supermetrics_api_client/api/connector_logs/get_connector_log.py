from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_connector_log_response_401 import GetConnectorLogResponse401
from ...models.get_connector_log_response_403 import GetConnectorLogResponse403
from ...models.get_connector_log_response_404 import GetConnectorLogResponse404
from ...models.get_connector_log_response_429 import GetConnectorLogResponse429
from ...models.get_connector_log_response_500 import GetConnectorLogResponse500
from ...models.log_entry import LogEntry
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
    log_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logs/{log_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetConnectorLogResponse401
    | GetConnectorLogResponse403
    | GetConnectorLogResponse404
    | GetConnectorLogResponse429
    | GetConnectorLogResponse500
    | LogEntry
    | None
):
    if response.status_code == 200:
        response_200 = LogEntry.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetConnectorLogResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetConnectorLogResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetConnectorLogResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetConnectorLogResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetConnectorLogResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetConnectorLogResponse401
    | GetConnectorLogResponse403
    | GetConnectorLogResponse404
    | GetConnectorLogResponse429
    | GetConnectorLogResponse500
    | LogEntry
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    connector_identifier: str,
    log_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    GetConnectorLogResponse401
    | GetConnectorLogResponse403
    | GetConnectorLogResponse404
    | GetConnectorLogResponse429
    | GetConnectorLogResponse500
    | LogEntry
]:
    """Get connector log

     Fetch detailed information for a specific connector log entry.

    Args:
        team_id (int):
        connector_identifier (str):
        log_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetConnectorLogResponse401 | GetConnectorLogResponse403 | GetConnectorLogResponse404 | GetConnectorLogResponse429 | GetConnectorLogResponse500 | LogEntry]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        log_id=log_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    connector_identifier: str,
    log_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    GetConnectorLogResponse401
    | GetConnectorLogResponse403
    | GetConnectorLogResponse404
    | GetConnectorLogResponse429
    | GetConnectorLogResponse500
    | LogEntry
    | None
):
    """Get connector log

     Fetch detailed information for a specific connector log entry.

    Args:
        team_id (int):
        connector_identifier (str):
        log_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetConnectorLogResponse401 | GetConnectorLogResponse403 | GetConnectorLogResponse404 | GetConnectorLogResponse429 | GetConnectorLogResponse500 | LogEntry
    """

    return sync_detailed(
        team_id=team_id,
        connector_identifier=connector_identifier,
        log_id=log_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    connector_identifier: str,
    log_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    GetConnectorLogResponse401
    | GetConnectorLogResponse403
    | GetConnectorLogResponse404
    | GetConnectorLogResponse429
    | GetConnectorLogResponse500
    | LogEntry
]:
    """Get connector log

     Fetch detailed information for a specific connector log entry.

    Args:
        team_id (int):
        connector_identifier (str):
        log_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetConnectorLogResponse401 | GetConnectorLogResponse403 | GetConnectorLogResponse404 | GetConnectorLogResponse429 | GetConnectorLogResponse500 | LogEntry]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        log_id=log_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    connector_identifier: str,
    log_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    GetConnectorLogResponse401
    | GetConnectorLogResponse403
    | GetConnectorLogResponse404
    | GetConnectorLogResponse429
    | GetConnectorLogResponse500
    | LogEntry
    | None
):
    """Get connector log

     Fetch detailed information for a specific connector log entry.

    Args:
        team_id (int):
        connector_identifier (str):
        log_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetConnectorLogResponse401 | GetConnectorLogResponse403 | GetConnectorLogResponse404 | GetConnectorLogResponse429 | GetConnectorLogResponse500 | LogEntry
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            log_id=log_id,
            client=client,
        )
    ).parsed
