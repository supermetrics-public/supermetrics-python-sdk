from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_tag_response import AccountTagResponse
from ...models.append_accounts_to_group_body import AppendAccountsToGroupBody
from ...models.append_accounts_to_group_response_400 import AppendAccountsToGroupResponse400
from ...models.append_accounts_to_group_response_401 import AppendAccountsToGroupResponse401
from ...models.append_accounts_to_group_response_429 import AppendAccountsToGroupResponse429
from ...models.append_accounts_to_group_response_500 import AppendAccountsToGroupResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    name: str,
    *,
    body: AppendAccountsToGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/teams/{team_id}/account_tags/{name}/add".format(
            team_id=quote(str(team_id), safe=""),
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    AccountTagResponse
    | AppendAccountsToGroupResponse400
    | AppendAccountsToGroupResponse401
    | AppendAccountsToGroupResponse429
    | AppendAccountsToGroupResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = AccountTagResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = AppendAccountsToGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = AppendAccountsToGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = AppendAccountsToGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = AppendAccountsToGroupResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    AccountTagResponse
    | AppendAccountsToGroupResponse400
    | AppendAccountsToGroupResponse401
    | AppendAccountsToGroupResponse429
    | AppendAccountsToGroupResponse500
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
    body: AppendAccountsToGroupBody,
) -> Response[
    AccountTagResponse
    | AppendAccountsToGroupResponse400
    | AppendAccountsToGroupResponse401
    | AppendAccountsToGroupResponse429
    | AppendAccountsToGroupResponse500
    | ErrorResponse
]:
    """Add accounts to an account tag

     Add accounts to an account tag

    Args:
        team_id (int):
        name (str):
        body (AppendAccountsToGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | AppendAccountsToGroupResponse400 | AppendAccountsToGroupResponse401 | AppendAccountsToGroupResponse429 | AppendAccountsToGroupResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        name=name,
        body=body,
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
    body: AppendAccountsToGroupBody,
) -> (
    AccountTagResponse
    | AppendAccountsToGroupResponse400
    | AppendAccountsToGroupResponse401
    | AppendAccountsToGroupResponse429
    | AppendAccountsToGroupResponse500
    | ErrorResponse
    | None
):
    """Add accounts to an account tag

     Add accounts to an account tag

    Args:
        team_id (int):
        name (str):
        body (AppendAccountsToGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | AppendAccountsToGroupResponse400 | AppendAccountsToGroupResponse401 | AppendAccountsToGroupResponse429 | AppendAccountsToGroupResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    name: str,
    *,
    client: AuthenticatedClient,
    body: AppendAccountsToGroupBody,
) -> Response[
    AccountTagResponse
    | AppendAccountsToGroupResponse400
    | AppendAccountsToGroupResponse401
    | AppendAccountsToGroupResponse429
    | AppendAccountsToGroupResponse500
    | ErrorResponse
]:
    """Add accounts to an account tag

     Add accounts to an account tag

    Args:
        team_id (int):
        name (str):
        body (AppendAccountsToGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | AppendAccountsToGroupResponse400 | AppendAccountsToGroupResponse401 | AppendAccountsToGroupResponse429 | AppendAccountsToGroupResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    name: str,
    *,
    client: AuthenticatedClient,
    body: AppendAccountsToGroupBody,
) -> (
    AccountTagResponse
    | AppendAccountsToGroupResponse400
    | AppendAccountsToGroupResponse401
    | AppendAccountsToGroupResponse429
    | AppendAccountsToGroupResponse500
    | ErrorResponse
    | None
):
    """Add accounts to an account tag

     Add accounts to an account tag

    Args:
        team_id (int):
        name (str):
        body (AppendAccountsToGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | AppendAccountsToGroupResponse400 | AppendAccountsToGroupResponse401 | AppendAccountsToGroupResponse429 | AppendAccountsToGroupResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            name=name,
            client=client,
            body=body,
        )
    ).parsed
