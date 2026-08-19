from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_tag_response import AccountTagResponse
from ...models.error_response import ErrorResponse
from ...models.fetch_account_group_response_400 import FetchAccountGroupResponse400
from ...models.fetch_account_group_response_401 import FetchAccountGroupResponse401
from ...models.fetch_account_group_response_429 import FetchAccountGroupResponse429
from ...models.fetch_account_group_response_500 import FetchAccountGroupResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/account_tags/{name}".format(
            team_id=quote(str(team_id), safe=""),
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    AccountTagResponse
    | ErrorResponse
    | FetchAccountGroupResponse400
    | FetchAccountGroupResponse401
    | FetchAccountGroupResponse429
    | FetchAccountGroupResponse500
    | None
):
    if response.status_code == 200:
        response_200 = AccountTagResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FetchAccountGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = FetchAccountGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = FetchAccountGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = FetchAccountGroupResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    AccountTagResponse
    | ErrorResponse
    | FetchAccountGroupResponse400
    | FetchAccountGroupResponse401
    | FetchAccountGroupResponse429
    | FetchAccountGroupResponse500
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
    AccountTagResponse
    | ErrorResponse
    | FetchAccountGroupResponse400
    | FetchAccountGroupResponse401
    | FetchAccountGroupResponse429
    | FetchAccountGroupResponse500
]:
    """Fetch a single account tag by name

     Fetch a single account tag by name

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | ErrorResponse | FetchAccountGroupResponse400 | FetchAccountGroupResponse401 | FetchAccountGroupResponse429 | FetchAccountGroupResponse500]
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
    AccountTagResponse
    | ErrorResponse
    | FetchAccountGroupResponse400
    | FetchAccountGroupResponse401
    | FetchAccountGroupResponse429
    | FetchAccountGroupResponse500
    | None
):
    """Fetch a single account tag by name

     Fetch a single account tag by name

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | ErrorResponse | FetchAccountGroupResponse400 | FetchAccountGroupResponse401 | FetchAccountGroupResponse429 | FetchAccountGroupResponse500
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
    AccountTagResponse
    | ErrorResponse
    | FetchAccountGroupResponse400
    | FetchAccountGroupResponse401
    | FetchAccountGroupResponse429
    | FetchAccountGroupResponse500
]:
    """Fetch a single account tag by name

     Fetch a single account tag by name

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | ErrorResponse | FetchAccountGroupResponse400 | FetchAccountGroupResponse401 | FetchAccountGroupResponse429 | FetchAccountGroupResponse500]
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
    AccountTagResponse
    | ErrorResponse
    | FetchAccountGroupResponse400
    | FetchAccountGroupResponse401
    | FetchAccountGroupResponse429
    | FetchAccountGroupResponse500
    | None
):
    """Fetch a single account tag by name

     Fetch a single account tag by name

    Args:
        team_id (int):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | ErrorResponse | FetchAccountGroupResponse400 | FetchAccountGroupResponse401 | FetchAccountGroupResponse429 | FetchAccountGroupResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            name=name,
            client=client,
        )
    ).parsed
