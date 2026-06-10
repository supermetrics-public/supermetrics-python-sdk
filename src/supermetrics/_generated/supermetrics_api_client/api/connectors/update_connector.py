from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_connector_request import UpdateConnectorRequest
from ...models.update_connector_response_400 import UpdateConnectorResponse400
from ...models.update_connector_response_401 import UpdateConnectorResponse401
from ...models.update_connector_response_403 import UpdateConnectorResponse403
from ...models.update_connector_response_404 import UpdateConnectorResponse404
from ...models.update_connector_response_422 import UpdateConnectorResponse422
from ...models.update_connector_response_429 import UpdateConnectorResponse429
from ...models.update_connector_response_500 import UpdateConnectorResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
    *,
    body: UpdateConnectorRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | UpdateConnectorResponse400
    | UpdateConnectorResponse401
    | UpdateConnectorResponse403
    | UpdateConnectorResponse404
    | UpdateConnectorResponse422
    | UpdateConnectorResponse429
    | UpdateConnectorResponse500
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = UpdateConnectorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateConnectorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UpdateConnectorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateConnectorResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = UpdateConnectorResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateConnectorResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateConnectorResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | UpdateConnectorResponse400
    | UpdateConnectorResponse401
    | UpdateConnectorResponse403
    | UpdateConnectorResponse404
    | UpdateConnectorResponse422
    | UpdateConnectorResponse429
    | UpdateConnectorResponse500
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
    body: UpdateConnectorRequest,
) -> Response[
    Any
    | UpdateConnectorResponse400
    | UpdateConnectorResponse401
    | UpdateConnectorResponse403
    | UpdateConnectorResponse404
    | UpdateConnectorResponse422
    | UpdateConnectorResponse429
    | UpdateConnectorResponse500
]:
    """Update connector

     Update a connector's name, description, and configuration.

    Args:
        team_id (int):
        connector_identifier (str):
        body (UpdateConnectorRequest): Connector metadata and configuration to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UpdateConnectorResponse400 | UpdateConnectorResponse401 | UpdateConnectorResponse403 | UpdateConnectorResponse404 | UpdateConnectorResponse422 | UpdateConnectorResponse429 | UpdateConnectorResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        body=body,
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
    body: UpdateConnectorRequest,
) -> (
    Any
    | UpdateConnectorResponse400
    | UpdateConnectorResponse401
    | UpdateConnectorResponse403
    | UpdateConnectorResponse404
    | UpdateConnectorResponse422
    | UpdateConnectorResponse429
    | UpdateConnectorResponse500
    | None
):
    """Update connector

     Update a connector's name, description, and configuration.

    Args:
        team_id (int):
        connector_identifier (str):
        body (UpdateConnectorRequest): Connector metadata and configuration to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | UpdateConnectorResponse400 | UpdateConnectorResponse401 | UpdateConnectorResponse403 | UpdateConnectorResponse404 | UpdateConnectorResponse422 | UpdateConnectorResponse429 | UpdateConnectorResponse500
    """

    return sync_detailed(
        team_id=team_id,
        connector_identifier=connector_identifier,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    body: UpdateConnectorRequest,
) -> Response[
    Any
    | UpdateConnectorResponse400
    | UpdateConnectorResponse401
    | UpdateConnectorResponse403
    | UpdateConnectorResponse404
    | UpdateConnectorResponse422
    | UpdateConnectorResponse429
    | UpdateConnectorResponse500
]:
    """Update connector

     Update a connector's name, description, and configuration.

    Args:
        team_id (int):
        connector_identifier (str):
        body (UpdateConnectorRequest): Connector metadata and configuration to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UpdateConnectorResponse400 | UpdateConnectorResponse401 | UpdateConnectorResponse403 | UpdateConnectorResponse404 | UpdateConnectorResponse422 | UpdateConnectorResponse429 | UpdateConnectorResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    body: UpdateConnectorRequest,
) -> (
    Any
    | UpdateConnectorResponse400
    | UpdateConnectorResponse401
    | UpdateConnectorResponse403
    | UpdateConnectorResponse404
    | UpdateConnectorResponse422
    | UpdateConnectorResponse429
    | UpdateConnectorResponse500
    | None
):
    """Update connector

     Update a connector's name, description, and configuration.

    Args:
        team_id (int):
        connector_identifier (str):
        body (UpdateConnectorRequest): Connector metadata and configuration to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | UpdateConnectorResponse400 | UpdateConnectorResponse401 | UpdateConnectorResponse403 | UpdateConnectorResponse404 | UpdateConnectorResponse422 | UpdateConnectorResponse429 | UpdateConnectorResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            client=client,
            body=body,
        )
    ).parsed
