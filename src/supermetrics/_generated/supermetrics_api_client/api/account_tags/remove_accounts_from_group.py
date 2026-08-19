from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_tag_response import AccountTagResponse
from ...models.error_response import ErrorResponse
from ...models.remove_accounts_from_group_body import RemoveAccountsFromGroupBody
from ...models.remove_accounts_from_group_response_400 import RemoveAccountsFromGroupResponse400
from ...models.remove_accounts_from_group_response_401 import RemoveAccountsFromGroupResponse401
from ...models.remove_accounts_from_group_response_429 import RemoveAccountsFromGroupResponse429
from ...models.remove_accounts_from_group_response_500 import RemoveAccountsFromGroupResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    name: str,
    *,
    body: RemoveAccountsFromGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/teams/{team_id}/account_tags/{name}/remove".format(
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
    | ErrorResponse
    | RemoveAccountsFromGroupResponse400
    | RemoveAccountsFromGroupResponse401
    | RemoveAccountsFromGroupResponse429
    | RemoveAccountsFromGroupResponse500
    | None
):
    if response.status_code == 200:
        response_200 = AccountTagResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = RemoveAccountsFromGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = RemoveAccountsFromGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = RemoveAccountsFromGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = RemoveAccountsFromGroupResponse500.from_dict(response.json())

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
    | RemoveAccountsFromGroupResponse400
    | RemoveAccountsFromGroupResponse401
    | RemoveAccountsFromGroupResponse429
    | RemoveAccountsFromGroupResponse500
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
    body: RemoveAccountsFromGroupBody,
) -> Response[
    AccountTagResponse
    | ErrorResponse
    | RemoveAccountsFromGroupResponse400
    | RemoveAccountsFromGroupResponse401
    | RemoveAccountsFromGroupResponse429
    | RemoveAccountsFromGroupResponse500
]:
    """Remove accounts from an account tag

     Remove accounts from an account tag

    Args:
        team_id (int):
        name (str):
        body (RemoveAccountsFromGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | ErrorResponse | RemoveAccountsFromGroupResponse400 | RemoveAccountsFromGroupResponse401 | RemoveAccountsFromGroupResponse429 | RemoveAccountsFromGroupResponse500]
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
    body: RemoveAccountsFromGroupBody,
) -> (
    AccountTagResponse
    | ErrorResponse
    | RemoveAccountsFromGroupResponse400
    | RemoveAccountsFromGroupResponse401
    | RemoveAccountsFromGroupResponse429
    | RemoveAccountsFromGroupResponse500
    | None
):
    """Remove accounts from an account tag

     Remove accounts from an account tag

    Args:
        team_id (int):
        name (str):
        body (RemoveAccountsFromGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | ErrorResponse | RemoveAccountsFromGroupResponse400 | RemoveAccountsFromGroupResponse401 | RemoveAccountsFromGroupResponse429 | RemoveAccountsFromGroupResponse500
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
    body: RemoveAccountsFromGroupBody,
) -> Response[
    AccountTagResponse
    | ErrorResponse
    | RemoveAccountsFromGroupResponse400
    | RemoveAccountsFromGroupResponse401
    | RemoveAccountsFromGroupResponse429
    | RemoveAccountsFromGroupResponse500
]:
    """Remove accounts from an account tag

     Remove accounts from an account tag

    Args:
        team_id (int):
        name (str):
        body (RemoveAccountsFromGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | ErrorResponse | RemoveAccountsFromGroupResponse400 | RemoveAccountsFromGroupResponse401 | RemoveAccountsFromGroupResponse429 | RemoveAccountsFromGroupResponse500]
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
    body: RemoveAccountsFromGroupBody,
) -> (
    AccountTagResponse
    | ErrorResponse
    | RemoveAccountsFromGroupResponse400
    | RemoveAccountsFromGroupResponse401
    | RemoveAccountsFromGroupResponse429
    | RemoveAccountsFromGroupResponse500
    | None
):
    """Remove accounts from an account tag

     Remove accounts from an account tag

    Args:
        team_id (int):
        name (str):
        body (RemoveAccountsFromGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | ErrorResponse | RemoveAccountsFromGroupResponse400 | RemoveAccountsFromGroupResponse401 | RemoveAccountsFromGroupResponse429 | RemoveAccountsFromGroupResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            name=name,
            client=client,
            body=body,
        )
    ).parsed
