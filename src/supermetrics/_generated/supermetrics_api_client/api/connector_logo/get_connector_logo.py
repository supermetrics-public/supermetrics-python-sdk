from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_connector_logo_response_200 import GetConnectorLogoResponse200
from ...models.get_connector_logo_response_401 import GetConnectorLogoResponse401
from ...models.get_connector_logo_response_403 import GetConnectorLogoResponse403
from ...models.get_connector_logo_response_404 import GetConnectorLogoResponse404
from ...models.get_connector_logo_response_429 import GetConnectorLogoResponse429
from ...models.get_connector_logo_response_500 import GetConnectorLogoResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    connector_identifier: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors/{connector_identifier}/logo",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetConnectorLogoResponse200
    | GetConnectorLogoResponse401
    | GetConnectorLogoResponse403
    | GetConnectorLogoResponse404
    | GetConnectorLogoResponse429
    | GetConnectorLogoResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetConnectorLogoResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetConnectorLogoResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetConnectorLogoResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetConnectorLogoResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetConnectorLogoResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetConnectorLogoResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetConnectorLogoResponse200
    | GetConnectorLogoResponse401
    | GetConnectorLogoResponse403
    | GetConnectorLogoResponse404
    | GetConnectorLogoResponse429
    | GetConnectorLogoResponse500
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
    GetConnectorLogoResponse200
    | GetConnectorLogoResponse401
    | GetConnectorLogoResponse403
    | GetConnectorLogoResponse404
    | GetConnectorLogoResponse429
    | GetConnectorLogoResponse500
]:
    """Get connector logo

     Get the logo URL for a connector.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetConnectorLogoResponse200 | GetConnectorLogoResponse401 | GetConnectorLogoResponse403 | GetConnectorLogoResponse404 | GetConnectorLogoResponse429 | GetConnectorLogoResponse500]
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
    GetConnectorLogoResponse200
    | GetConnectorLogoResponse401
    | GetConnectorLogoResponse403
    | GetConnectorLogoResponse404
    | GetConnectorLogoResponse429
    | GetConnectorLogoResponse500
    | None
):
    """Get connector logo

     Get the logo URL for a connector.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetConnectorLogoResponse200 | GetConnectorLogoResponse401 | GetConnectorLogoResponse403 | GetConnectorLogoResponse404 | GetConnectorLogoResponse429 | GetConnectorLogoResponse500
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
    GetConnectorLogoResponse200
    | GetConnectorLogoResponse401
    | GetConnectorLogoResponse403
    | GetConnectorLogoResponse404
    | GetConnectorLogoResponse429
    | GetConnectorLogoResponse500
]:
    """Get connector logo

     Get the logo URL for a connector.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetConnectorLogoResponse200 | GetConnectorLogoResponse401 | GetConnectorLogoResponse403 | GetConnectorLogoResponse404 | GetConnectorLogoResponse429 | GetConnectorLogoResponse500]
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
    GetConnectorLogoResponse200
    | GetConnectorLogoResponse401
    | GetConnectorLogoResponse403
    | GetConnectorLogoResponse404
    | GetConnectorLogoResponse429
    | GetConnectorLogoResponse500
    | None
):
    """Get connector logo

     Get the logo URL for a connector.

    Args:
        team_id (int):
        connector_identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetConnectorLogoResponse200 | GetConnectorLogoResponse401 | GetConnectorLogoResponse403 | GetConnectorLogoResponse404 | GetConnectorLogoResponse429 | GetConnectorLogoResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            connector_identifier=connector_identifier,
            client=client,
        )
    ).parsed
