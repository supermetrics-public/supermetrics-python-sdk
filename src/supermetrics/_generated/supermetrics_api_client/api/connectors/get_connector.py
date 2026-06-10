from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connector_with_configuration import ConnectorWithConfiguration
from ...models.get_connector_response_400 import GetConnectorResponse400
from ...models.get_connector_response_401 import GetConnectorResponse401
from ...models.get_connector_response_403 import GetConnectorResponse403
from ...models.get_connector_response_404 import GetConnectorResponse404
from ...models.get_connector_response_429 import GetConnectorResponse429
from ...models.get_connector_response_500 import GetConnectorResponse500
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
) -> (
    ConnectorWithConfiguration
    | GetConnectorResponse400
    | GetConnectorResponse401
    | GetConnectorResponse403
    | GetConnectorResponse404
    | GetConnectorResponse429
    | GetConnectorResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ConnectorWithConfiguration.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetConnectorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetConnectorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetConnectorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetConnectorResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetConnectorResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetConnectorResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ConnectorWithConfiguration
    | GetConnectorResponse400
    | GetConnectorResponse401
    | GetConnectorResponse403
    | GetConnectorResponse404
    | GetConnectorResponse429
    | GetConnectorResponse500
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
    *,
    client: AuthenticatedClient,
) -> Response[
    ConnectorWithConfiguration
    | GetConnectorResponse400
    | GetConnectorResponse401
    | GetConnectorResponse403
    | GetConnectorResponse404
    | GetConnectorResponse429
    | GetConnectorResponse500
]:
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorWithConfiguration | GetConnectorResponse400 | GetConnectorResponse401 | GetConnectorResponse403 | GetConnectorResponse404 | GetConnectorResponse429 | GetConnectorResponse500]
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
) -> (
    ConnectorWithConfiguration
    | GetConnectorResponse400
    | GetConnectorResponse401
    | GetConnectorResponse403
    | GetConnectorResponse404
    | GetConnectorResponse429
    | GetConnectorResponse500
    | None
):
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorWithConfiguration | GetConnectorResponse400 | GetConnectorResponse401 | GetConnectorResponse403 | GetConnectorResponse404 | GetConnectorResponse429 | GetConnectorResponse500
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
) -> Response[
    ConnectorWithConfiguration
    | GetConnectorResponse400
    | GetConnectorResponse401
    | GetConnectorResponse403
    | GetConnectorResponse404
    | GetConnectorResponse429
    | GetConnectorResponse500
]:
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorWithConfiguration | GetConnectorResponse400 | GetConnectorResponse401 | GetConnectorResponse403 | GetConnectorResponse404 | GetConnectorResponse429 | GetConnectorResponse500]
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
) -> (
    ConnectorWithConfiguration
    | GetConnectorResponse400
    | GetConnectorResponse401
    | GetConnectorResponse403
    | GetConnectorResponse404
    | GetConnectorResponse429
    | GetConnectorResponse500
    | None
):
    """Get connector

     Fetch information for a connector including its configuration.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorWithConfiguration | GetConnectorResponse400 | GetConnectorResponse401 | GetConnectorResponse403 | GetConnectorResponse404 | GetConnectorResponse429 | GetConnectorResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            client=client,
        )
    ).parsed
