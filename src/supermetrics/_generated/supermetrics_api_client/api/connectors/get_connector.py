from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connector_with_configuration import ConnectorWithConfiguration
from ...models.error_response import ErrorResponse
from ...models.get_connector_response_400 import GetConnectorResponse400
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400 | None:
    if response.status_code == 200:
        response_200 = ConnectorWithConfiguration.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetConnectorResponse400.from_dict(response.json())

        return response_400

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
) -> Response[ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400]:
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
) -> Response[ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400]:
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
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
) -> ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400 | None:
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400
    """

    return sync_detailed(
        team_id=team_id,
        connector_identifier=connector_identifier,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
) -> Response[ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400]:
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
) -> ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400 | None:
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorWithConfiguration | ErrorResponse | GetConnectorResponse400
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            client=client,
        )
    ).parsed
