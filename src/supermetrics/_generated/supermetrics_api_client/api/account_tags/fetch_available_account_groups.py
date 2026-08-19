from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_tag_list_response import AccountTagListResponse
from ...models.error_response import ErrorResponse
from ...models.fetch_available_account_groups_response_400 import FetchAvailableAccountGroupsResponse400
from ...models.fetch_available_account_groups_response_401 import FetchAvailableAccountGroupsResponse401
from ...models.fetch_available_account_groups_response_429 import FetchAvailableAccountGroupsResponse429
from ...models.fetch_available_account_groups_response_500 import FetchAvailableAccountGroupsResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/account_tags".format(
            team_id=quote(str(team_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    AccountTagListResponse
    | ErrorResponse
    | FetchAvailableAccountGroupsResponse400
    | FetchAvailableAccountGroupsResponse401
    | FetchAvailableAccountGroupsResponse429
    | FetchAvailableAccountGroupsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = AccountTagListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FetchAvailableAccountGroupsResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = FetchAvailableAccountGroupsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = FetchAvailableAccountGroupsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = FetchAvailableAccountGroupsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    AccountTagListResponse
    | ErrorResponse
    | FetchAvailableAccountGroupsResponse400
    | FetchAvailableAccountGroupsResponse401
    | FetchAvailableAccountGroupsResponse429
    | FetchAvailableAccountGroupsResponse500
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
) -> Response[
    AccountTagListResponse
    | ErrorResponse
    | FetchAvailableAccountGroupsResponse400
    | FetchAvailableAccountGroupsResponse401
    | FetchAvailableAccountGroupsResponse429
    | FetchAvailableAccountGroupsResponse500
]:
    """List all account tags in a team

     List all account tags in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagListResponse | ErrorResponse | FetchAvailableAccountGroupsResponse400 | FetchAvailableAccountGroupsResponse401 | FetchAvailableAccountGroupsResponse429 | FetchAvailableAccountGroupsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    AccountTagListResponse
    | ErrorResponse
    | FetchAvailableAccountGroupsResponse400
    | FetchAvailableAccountGroupsResponse401
    | FetchAvailableAccountGroupsResponse429
    | FetchAvailableAccountGroupsResponse500
    | None
):
    """List all account tags in a team

     List all account tags in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagListResponse | ErrorResponse | FetchAvailableAccountGroupsResponse400 | FetchAvailableAccountGroupsResponse401 | FetchAvailableAccountGroupsResponse429 | FetchAvailableAccountGroupsResponse500
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    AccountTagListResponse
    | ErrorResponse
    | FetchAvailableAccountGroupsResponse400
    | FetchAvailableAccountGroupsResponse401
    | FetchAvailableAccountGroupsResponse429
    | FetchAvailableAccountGroupsResponse500
]:
    """List all account tags in a team

     List all account tags in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagListResponse | ErrorResponse | FetchAvailableAccountGroupsResponse400 | FetchAvailableAccountGroupsResponse401 | FetchAvailableAccountGroupsResponse429 | FetchAvailableAccountGroupsResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    AccountTagListResponse
    | ErrorResponse
    | FetchAvailableAccountGroupsResponse400
    | FetchAvailableAccountGroupsResponse401
    | FetchAvailableAccountGroupsResponse429
    | FetchAvailableAccountGroupsResponse500
    | None
):
    """List all account tags in a team

     List all account tags in a team

    Args:
        team_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagListResponse | ErrorResponse | FetchAvailableAccountGroupsResponse400 | FetchAvailableAccountGroupsResponse401 | FetchAvailableAccountGroupsResponse429 | FetchAvailableAccountGroupsResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
        )
    ).parsed
