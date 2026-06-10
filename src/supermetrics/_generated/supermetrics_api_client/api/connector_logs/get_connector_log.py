from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
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
) -> ErrorResponse | LogEntry | None:
    if response.status_code == 200:
        response_200 = LogEntry.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

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
) -> Response[ErrorResponse | LogEntry]:
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
) -> Response[ErrorResponse | LogEntry]:
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
        Response[ErrorResponse | LogEntry]
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
) -> ErrorResponse | LogEntry | None:
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
        ErrorResponse | LogEntry
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
) -> Response[ErrorResponse | LogEntry]:
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
        Response[ErrorResponse | LogEntry]
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
) -> ErrorResponse | LogEntry | None:
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
        ErrorResponse | LogEntry
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            log_id=log_id,
            client=client,
        )
    ).parsed
