from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connector_with_configuration import ConnectorWithConfiguration
from ...models.create_connector_body import CreateConnectorBody
from ...models.create_connector_response_401 import CreateConnectorResponse401
from ...models.create_connector_response_404 import CreateConnectorResponse404
from ...models.create_connector_response_429 import CreateConnectorResponse429
from ...models.create_connector_response_500 import CreateConnectorResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: CreateConnectorBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors",
    }

    _kwargs["data"] = body.to_dict()

    headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ConnectorWithConfiguration
    | CreateConnectorResponse401
    | CreateConnectorResponse404
    | CreateConnectorResponse429
    | CreateConnectorResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 201:
        response_201 = ConnectorWithConfiguration.from_dict(response.json())

        return response_201

    if response.status_code == 401:
        response_401 = CreateConnectorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CreateConnectorResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = CreateConnectorResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateConnectorResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ConnectorWithConfiguration
    | CreateConnectorResponse401
    | CreateConnectorResponse404
    | CreateConnectorResponse429
    | CreateConnectorResponse500
    | ErrorResponse
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
    body: CreateConnectorBody,
) -> Response[
    ConnectorWithConfiguration
    | CreateConnectorResponse401
    | CreateConnectorResponse404
    | CreateConnectorResponse429
    | CreateConnectorResponse500
    | ErrorResponse
]:
    """Create connector

     Create a new custom connector. Optionally duplicate an existing connector by providing its
    identifier.

    Args:
        team_id (int):
        body (CreateConnectorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorWithConfiguration | CreateConnectorResponse401 | CreateConnectorResponse404 | CreateConnectorResponse429 | CreateConnectorResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateConnectorBody,
) -> (
    ConnectorWithConfiguration
    | CreateConnectorResponse401
    | CreateConnectorResponse404
    | CreateConnectorResponse429
    | CreateConnectorResponse500
    | ErrorResponse
    | None
):
    """Create connector

     Create a new custom connector. Optionally duplicate an existing connector by providing its
    identifier.

    Args:
        team_id (int):
        body (CreateConnectorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorWithConfiguration | CreateConnectorResponse401 | CreateConnectorResponse404 | CreateConnectorResponse429 | CreateConnectorResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateConnectorBody,
) -> Response[
    ConnectorWithConfiguration
    | CreateConnectorResponse401
    | CreateConnectorResponse404
    | CreateConnectorResponse429
    | CreateConnectorResponse500
    | ErrorResponse
]:
    """Create connector

     Create a new custom connector. Optionally duplicate an existing connector by providing its
    identifier.

    Args:
        team_id (int):
        body (CreateConnectorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorWithConfiguration | CreateConnectorResponse401 | CreateConnectorResponse404 | CreateConnectorResponse429 | CreateConnectorResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateConnectorBody,
) -> (
    ConnectorWithConfiguration
    | CreateConnectorResponse401
    | CreateConnectorResponse404
    | CreateConnectorResponse429
    | CreateConnectorResponse500
    | ErrorResponse
    | None
):
    """Create connector

     Create a new custom connector. Optionally duplicate an existing connector by providing its
    identifier.

    Args:
        team_id (int):
        body (CreateConnectorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorWithConfiguration | CreateConnectorResponse401 | CreateConnectorResponse404 | CreateConnectorResponse429 | CreateConnectorResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
