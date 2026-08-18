from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_connectors_response_200 import ListConnectorsResponse200
from ...models.list_connectors_response_401 import ListConnectorsResponse401
from ...models.list_connectors_response_403 import ListConnectorsResponse403
from ...models.list_connectors_response_429 import ListConnectorsResponse429
from ...models.list_connectors_response_500 import ListConnectorsResponse500
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    *,
    include_configs: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_configs"] = include_configs

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/teams/{team_id}/connector_builder/connectors",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ListConnectorsResponse200
    | ListConnectorsResponse401
    | ListConnectorsResponse403
    | ListConnectorsResponse429
    | ListConnectorsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ListConnectorsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListConnectorsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListConnectorsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ListConnectorsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListConnectorsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ListConnectorsResponse200
    | ListConnectorsResponse401
    | ListConnectorsResponse403
    | ListConnectorsResponse429
    | ListConnectorsResponse500
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
    include_configs: bool | Unset = False,
) -> Response[
    ListConnectorsResponse200
    | ListConnectorsResponse401
    | ListConnectorsResponse403
    | ListConnectorsResponse429
    | ListConnectorsResponse500
]:
    """List connectors

     Fetch information for the connectors you have access to.

    Args:
        team_id (int):
        include_configs (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListConnectorsResponse200 | ListConnectorsResponse401 | ListConnectorsResponse403 | ListConnectorsResponse429 | ListConnectorsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        include_configs=include_configs,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    include_configs: bool | Unset = False,
) -> (
    ListConnectorsResponse200
    | ListConnectorsResponse401
    | ListConnectorsResponse403
    | ListConnectorsResponse429
    | ListConnectorsResponse500
    | None
):
    """List connectors

     Fetch information for the connectors you have access to.

    Args:
        team_id (int):
        include_configs (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListConnectorsResponse200 | ListConnectorsResponse401 | ListConnectorsResponse403 | ListConnectorsResponse429 | ListConnectorsResponse500
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        include_configs=include_configs,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    include_configs: bool | Unset = False,
) -> Response[
    ListConnectorsResponse200
    | ListConnectorsResponse401
    | ListConnectorsResponse403
    | ListConnectorsResponse429
    | ListConnectorsResponse500
]:
    """List connectors

     Fetch information for the connectors you have access to.

    Args:
        team_id (int):
        include_configs (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListConnectorsResponse200 | ListConnectorsResponse401 | ListConnectorsResponse403 | ListConnectorsResponse429 | ListConnectorsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        include_configs=include_configs,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    include_configs: bool | Unset = False,
) -> (
    ListConnectorsResponse200
    | ListConnectorsResponse401
    | ListConnectorsResponse403
    | ListConnectorsResponse429
    | ListConnectorsResponse500
    | None
):
    """List connectors

     Fetch information for the connectors you have access to.

    Args:
        team_id (int):
        include_configs (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListConnectorsResponse200 | ListConnectorsResponse401 | ListConnectorsResponse403 | ListConnectorsResponse429 | ListConnectorsResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            include_configs=include_configs,
        )
    ).parsed
