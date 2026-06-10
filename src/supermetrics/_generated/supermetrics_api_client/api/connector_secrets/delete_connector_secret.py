from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_connector_secret_response_401 import DeleteConnectorSecretResponse401
from ...models.delete_connector_secret_response_403 import DeleteConnectorSecretResponse403
from ...models.delete_connector_secret_response_404 import DeleteConnectorSecretResponse404
from ...models.delete_connector_secret_response_429 import DeleteConnectorSecretResponse429
from ...models.delete_connector_secret_response_500 import DeleteConnectorSecretResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | DeleteConnectorSecretResponse401
    | DeleteConnectorSecretResponse403
    | DeleteConnectorSecretResponse404
    | DeleteConnectorSecretResponse429
    | DeleteConnectorSecretResponse500
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 401:
        response_401 = DeleteConnectorSecretResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = DeleteConnectorSecretResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = DeleteConnectorSecretResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = DeleteConnectorSecretResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = DeleteConnectorSecretResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | DeleteConnectorSecretResponse401
    | DeleteConnectorSecretResponse403
    | DeleteConnectorSecretResponse404
    | DeleteConnectorSecretResponse429
    | DeleteConnectorSecretResponse500
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
    secret_placeholder: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | DeleteConnectorSecretResponse401
    | DeleteConnectorSecretResponse403
    | DeleteConnectorSecretResponse404
    | DeleteConnectorSecretResponse429
    | DeleteConnectorSecretResponse500
]:
    """Delete connector secret

     Delete a secret from a connector.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteConnectorSecretResponse401 | DeleteConnectorSecretResponse403 | DeleteConnectorSecretResponse404 | DeleteConnectorSecretResponse429 | DeleteConnectorSecretResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        secret_placeholder=secret_placeholder,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | DeleteConnectorSecretResponse401
    | DeleteConnectorSecretResponse403
    | DeleteConnectorSecretResponse404
    | DeleteConnectorSecretResponse429
    | DeleteConnectorSecretResponse500
    | None
):
    """Delete connector secret

     Delete a secret from a connector.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteConnectorSecretResponse401 | DeleteConnectorSecretResponse403 | DeleteConnectorSecretResponse404 | DeleteConnectorSecretResponse429 | DeleteConnectorSecretResponse500
    """

    return sync_detailed(
        team_id=team_id,
        connector_identifier=connector_identifier,
        secret_placeholder=secret_placeholder,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | DeleteConnectorSecretResponse401
    | DeleteConnectorSecretResponse403
    | DeleteConnectorSecretResponse404
    | DeleteConnectorSecretResponse429
    | DeleteConnectorSecretResponse500
]:
    """Delete connector secret

     Delete a secret from a connector.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteConnectorSecretResponse401 | DeleteConnectorSecretResponse403 | DeleteConnectorSecretResponse404 | DeleteConnectorSecretResponse429 | DeleteConnectorSecretResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        secret_placeholder=secret_placeholder,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | DeleteConnectorSecretResponse401
    | DeleteConnectorSecretResponse403
    | DeleteConnectorSecretResponse404
    | DeleteConnectorSecretResponse429
    | DeleteConnectorSecretResponse500
    | None
):
    """Delete connector secret

     Delete a secret from a connector.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteConnectorSecretResponse401 | DeleteConnectorSecretResponse403 | DeleteConnectorSecretResponse404 | DeleteConnectorSecretResponse429 | DeleteConnectorSecretResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            secret_placeholder=secret_placeholder,
            client=client,
        )
    ).parsed
