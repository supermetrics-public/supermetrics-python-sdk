from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_tag_response import AccountTagResponse
from ...models.create_account_group_body import CreateAccountGroupBody
from ...models.create_account_group_response_400 import CreateAccountGroupResponse400
from ...models.create_account_group_response_401 import CreateAccountGroupResponse401
from ...models.create_account_group_response_409 import CreateAccountGroupResponse409
from ...models.create_account_group_response_429 import CreateAccountGroupResponse429
from ...models.create_account_group_response_500 import CreateAccountGroupResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: CreateAccountGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/teams/{team_id}/account_tags".format(
            team_id=quote(str(team_id), safe=""),
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
    | CreateAccountGroupResponse400
    | CreateAccountGroupResponse401
    | CreateAccountGroupResponse409
    | CreateAccountGroupResponse429
    | CreateAccountGroupResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = AccountTagResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = CreateAccountGroupResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateAccountGroupResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = CreateAccountGroupResponse409.from_dict(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = CreateAccountGroupResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateAccountGroupResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    AccountTagResponse
    | CreateAccountGroupResponse400
    | CreateAccountGroupResponse401
    | CreateAccountGroupResponse409
    | CreateAccountGroupResponse429
    | CreateAccountGroupResponse500
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
    *,
    client: AuthenticatedClient,
    body: CreateAccountGroupBody,
) -> Response[
    AccountTagResponse
    | CreateAccountGroupResponse400
    | CreateAccountGroupResponse401
    | CreateAccountGroupResponse409
    | CreateAccountGroupResponse429
    | CreateAccountGroupResponse500
    | ErrorResponse
]:
    """Create a new account tag

     Create a new account tag

    Args:
        team_id (int):
        body (CreateAccountGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | CreateAccountGroupResponse400 | CreateAccountGroupResponse401 | CreateAccountGroupResponse409 | CreateAccountGroupResponse429 | CreateAccountGroupResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateAccountGroupBody,
) -> (
    AccountTagResponse
    | CreateAccountGroupResponse400
    | CreateAccountGroupResponse401
    | CreateAccountGroupResponse409
    | CreateAccountGroupResponse429
    | CreateAccountGroupResponse500
    | ErrorResponse
    | None
):
    """Create a new account tag

     Create a new account tag

    Args:
        team_id (int):
        body (CreateAccountGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | CreateAccountGroupResponse400 | CreateAccountGroupResponse401 | CreateAccountGroupResponse409 | CreateAccountGroupResponse429 | CreateAccountGroupResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateAccountGroupBody,
) -> Response[
    AccountTagResponse
    | CreateAccountGroupResponse400
    | CreateAccountGroupResponse401
    | CreateAccountGroupResponse409
    | CreateAccountGroupResponse429
    | CreateAccountGroupResponse500
    | ErrorResponse
]:
    """Create a new account tag

     Create a new account tag

    Args:
        team_id (int):
        body (CreateAccountGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTagResponse | CreateAccountGroupResponse400 | CreateAccountGroupResponse401 | CreateAccountGroupResponse409 | CreateAccountGroupResponse429 | CreateAccountGroupResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateAccountGroupBody,
) -> (
    AccountTagResponse
    | CreateAccountGroupResponse400
    | CreateAccountGroupResponse401
    | CreateAccountGroupResponse409
    | CreateAccountGroupResponse429
    | CreateAccountGroupResponse500
    | ErrorResponse
    | None
):
    """Create a new account tag

     Create a new account tag

    Args:
        team_id (int):
        body (CreateAccountGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountTagResponse | CreateAccountGroupResponse400 | CreateAccountGroupResponse401 | CreateAccountGroupResponse409 | CreateAccountGroupResponse429 | CreateAccountGroupResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
