from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_connector_secret_response_400 import UpdateConnectorSecretResponse400
from ...models.update_secret_request import UpdateSecretRequest
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
    *,
    body: UpdateSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}/secrets/{secret_placeholder}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorResponse | UpdateConnectorSecretResponse400 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = UpdateConnectorSecretResponse400.from_dict(response.json())

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

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

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
) -> Response[Any | ErrorResponse | UpdateConnectorSecretResponse400]:
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
    body: UpdateSecretRequest,
) -> Response[Any | ErrorResponse | UpdateConnectorSecretResponse400]:
    """Update connector secret

     Overwrite the value of an existing secret. The previous value cannot be recovered.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):
        body (UpdateSecretRequest): New secret value to overwrite the existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse | UpdateConnectorSecretResponse400]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        secret_placeholder=secret_placeholder,
        body=body,
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
    body: UpdateSecretRequest,
) -> Any | ErrorResponse | UpdateConnectorSecretResponse400 | None:
    """Update connector secret

     Overwrite the value of an existing secret. The previous value cannot be recovered.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):
        body (UpdateSecretRequest): New secret value to overwrite the existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse | UpdateConnectorSecretResponse400
    """

    return sync_detailed(
        team_id=team_id,
        connector_identifier=connector_identifier,
        secret_placeholder=secret_placeholder,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
    *,
    client: AuthenticatedClient,
    body: UpdateSecretRequest,
) -> Response[Any | ErrorResponse | UpdateConnectorSecretResponse400]:
    """Update connector secret

     Overwrite the value of an existing secret. The previous value cannot be recovered.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):
        body (UpdateSecretRequest): New secret value to overwrite the existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse | UpdateConnectorSecretResponse400]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        connector_identifier=connector_identifier,
        secret_placeholder=secret_placeholder,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    connector_identifier: str,
    secret_placeholder: str,
    *,
    client: AuthenticatedClient,
    body: UpdateSecretRequest,
) -> Any | ErrorResponse | UpdateConnectorSecretResponse400 | None:
    """Update connector secret

     Overwrite the value of an existing secret. The previous value cannot be recovered.

    Args:
        team_id (int):
        connector_identifier (str):
        secret_placeholder (str):
        body (UpdateSecretRequest): New secret value to overwrite the existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse | UpdateConnectorSecretResponse400
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            secret_placeholder=secret_placeholder,
            client=client,
            body=body,
        )
    ).parsed
