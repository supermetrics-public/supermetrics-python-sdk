from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_account_group_response_200 import DeleteAccountGroupResponse200
from ...models.delete_account_group_response_400 import DeleteAccountGroupResponse400
from ...models.delete_account_group_response_401 import DeleteAccountGroupResponse401
from ...models.delete_account_group_response_429 import DeleteAccountGroupResponse429
from ...models.delete_account_group_response_500 import DeleteAccountGroupResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/teams/{team_id}/account_tags/{name}".format(
            team_id=quote(str(team_id), safe=""),
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DeleteAccountGroupResponse200
    | DeleteAccountGroupResponse400
    | DeleteAccountGroupResponse401
    | DeleteAccountGroupResponse429
    | DeleteAccountGroupResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = DeleteAccountGroupResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = DeleteAccountGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = DeleteAccountGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = DeleteAccountGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = DeleteAccountGroupResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DeleteAccountGroupResponse200
    | DeleteAccountGroupResponse400
    | DeleteAccountGroupResponse401
    | DeleteAccountGroupResponse429
    | DeleteAccountGroupResponse500
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
    name: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    DeleteAccountGroupResponse200
    | DeleteAccountGroupResponse400
    | DeleteAccountGroupResponse401
    | DeleteAccountGroupResponse429
    | DeleteAccountGroupResponse500
    | ErrorResponse
]:
    """Delete an account tag

     Delete an account tag

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteAccountGroupResponse200 | DeleteAccountGroupResponse400 | DeleteAccountGroupResponse401 | DeleteAccountGroupResponse429 | DeleteAccountGroupResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    name: str,
    *,
    client: AuthenticatedClient,
) -> (
    DeleteAccountGroupResponse200
    | DeleteAccountGroupResponse400
    | DeleteAccountGroupResponse401
    | DeleteAccountGroupResponse429
    | DeleteAccountGroupResponse500
    | ErrorResponse
    | None
):
    """Delete an account tag

     Delete an account tag

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteAccountGroupResponse200 | DeleteAccountGroupResponse400 | DeleteAccountGroupResponse401 | DeleteAccountGroupResponse429 | DeleteAccountGroupResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    name: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    DeleteAccountGroupResponse200
    | DeleteAccountGroupResponse400
    | DeleteAccountGroupResponse401
    | DeleteAccountGroupResponse429
    | DeleteAccountGroupResponse500
    | ErrorResponse
]:
    """Delete an account tag

     Delete an account tag

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteAccountGroupResponse200 | DeleteAccountGroupResponse400 | DeleteAccountGroupResponse401 | DeleteAccountGroupResponse429 | DeleteAccountGroupResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    name: str,
    *,
    client: AuthenticatedClient,
) -> (
    DeleteAccountGroupResponse200
    | DeleteAccountGroupResponse400
    | DeleteAccountGroupResponse401
    | DeleteAccountGroupResponse429
    | DeleteAccountGroupResponse500
    | ErrorResponse
    | None
):
    """Delete an account tag

     Delete an account tag

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteAccountGroupResponse200 | DeleteAccountGroupResponse400 | DeleteAccountGroupResponse401 | DeleteAccountGroupResponse429 | DeleteAccountGroupResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            name=name,
            client=client,
        )
    ).parsed
