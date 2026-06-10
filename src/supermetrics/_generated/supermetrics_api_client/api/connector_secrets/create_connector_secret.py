from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_connector_secret_response_201 import CreateConnectorSecretResponse201
from ...models.create_connector_secret_response_400 import CreateConnectorSecretResponse400
from ...models.create_connector_secret_response_401 import CreateConnectorSecretResponse401
from ...models.create_connector_secret_response_404 import CreateConnectorSecretResponse404
from ...models.create_connector_secret_response_409 import CreateConnectorSecretResponse409
from ...models.create_connector_secret_response_429 import CreateConnectorSecretResponse429
from ...models.create_connector_secret_response_500 import CreateConnectorSecretResponse500
from ...models.create_secret_request import CreateSecretRequest
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
    *,
    body: CreateSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateConnectorSecretResponse201
    | CreateConnectorSecretResponse400
    | CreateConnectorSecretResponse401
    | CreateConnectorSecretResponse404
    | CreateConnectorSecretResponse409
    | CreateConnectorSecretResponse429
    | CreateConnectorSecretResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 201:
        response_201 = CreateConnectorSecretResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateConnectorSecretResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateConnectorSecretResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CreateConnectorSecretResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = CreateConnectorSecretResponse409.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateConnectorSecretResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateConnectorSecretResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateConnectorSecretResponse201
    | CreateConnectorSecretResponse400
    | CreateConnectorSecretResponse401
    | CreateConnectorSecretResponse404
    | CreateConnectorSecretResponse409
    | CreateConnectorSecretResponse429
    | CreateConnectorSecretResponse500
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
    connector_identifier: str,
    *,
    client: AuthenticatedClient,
    body: CreateSecretRequest,
) -> Response[
    CreateConnectorSecretResponse201
    | CreateConnectorSecretResponse400
    | CreateConnectorSecretResponse401
    | CreateConnectorSecretResponse404
    | CreateConnectorSecretResponse409
    | CreateConnectorSecretResponse429
    | CreateConnectorSecretResponse500
    | ErrorResponse
]:
    """Create connector secret

     Create a new encrypted secret for a connector. The secret placeholder is generated server-side.
    Returns the updated list of secrets.

    Args:
        team_id (int):
        connector_identifier (str):
        body (CreateSecretRequest): Secret name and value to encrypt and store.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateConnectorSecretResponse201 | CreateConnectorSecretResponse400 | CreateConnectorSecretResponse401 | CreateConnectorSecretResponse404 | CreateConnectorSecretResponse409 | CreateConnectorSecretResponse429 | CreateConnectorSecretResponse500 | ErrorResponse]
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
    body: CreateSecretRequest,
) -> (
    CreateConnectorSecretResponse201
    | CreateConnectorSecretResponse400
    | CreateConnectorSecretResponse401
    | CreateConnectorSecretResponse404
    | CreateConnectorSecretResponse409
    | CreateConnectorSecretResponse429
    | CreateConnectorSecretResponse500
    | ErrorResponse
    | None
):
    """Create connector secret

     Create a new encrypted secret for a connector. The secret placeholder is generated server-side.
    Returns the updated list of secrets.

    Args:
        team_id (int):
        connector_identifier (str):
        body (CreateSecretRequest): Secret name and value to encrypt and store.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateConnectorSecretResponse201 | CreateConnectorSecretResponse400 | CreateConnectorSecretResponse401 | CreateConnectorSecretResponse404 | CreateConnectorSecretResponse409 | CreateConnectorSecretResponse429 | CreateConnectorSecretResponse500 | ErrorResponse
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
    body: CreateSecretRequest,
) -> Response[
    CreateConnectorSecretResponse201
    | CreateConnectorSecretResponse400
    | CreateConnectorSecretResponse401
    | CreateConnectorSecretResponse404
    | CreateConnectorSecretResponse409
    | CreateConnectorSecretResponse429
    | CreateConnectorSecretResponse500
    | ErrorResponse
]:
    """Create connector secret

     Create a new encrypted secret for a connector. The secret placeholder is generated server-side.
    Returns the updated list of secrets.

    Args:
        team_id (int):
        connector_identifier (str):
        body (CreateSecretRequest): Secret name and value to encrypt and store.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateConnectorSecretResponse201 | CreateConnectorSecretResponse400 | CreateConnectorSecretResponse401 | CreateConnectorSecretResponse404 | CreateConnectorSecretResponse409 | CreateConnectorSecretResponse429 | CreateConnectorSecretResponse500 | ErrorResponse]
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
    body: CreateSecretRequest,
) -> (
    CreateConnectorSecretResponse201
    | CreateConnectorSecretResponse400
    | CreateConnectorSecretResponse401
    | CreateConnectorSecretResponse404
    | CreateConnectorSecretResponse409
    | CreateConnectorSecretResponse429
    | CreateConnectorSecretResponse500
    | ErrorResponse
    | None
):
    """Create connector secret

     Create a new encrypted secret for a connector. The secret placeholder is generated server-side.
    Returns the updated list of secrets.

    Args:
        team_id (int):
        connector_identifier (str):
        body (CreateSecretRequest): Secret name and value to encrypt and store.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateConnectorSecretResponse201 | CreateConnectorSecretResponse400 | CreateConnectorSecretResponse401 | CreateConnectorSecretResponse404 | CreateConnectorSecretResponse409 | CreateConnectorSecretResponse429 | CreateConnectorSecretResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            client=client,
            body=body,
        )
    ).parsed
