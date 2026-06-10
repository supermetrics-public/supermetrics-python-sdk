from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
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


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorResponse]:
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
) -> Response[Any | ErrorResponse]:
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
        Response[Any | ErrorResponse]
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
) -> Any | ErrorResponse | None:
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
        Any | ErrorResponse
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
) -> Response[Any | ErrorResponse]:
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
        Response[Any | ErrorResponse]
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
) -> Any | ErrorResponse | None:
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
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            secret_placeholder=secret_placeholder,
            client=client,
        )
    ).parsed
