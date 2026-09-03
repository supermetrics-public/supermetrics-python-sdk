from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_response import ApiKeyResponse
from ...models.create_team_api_key_body import CreateTeamApiKeyBody
from ...models.create_team_api_key_response_400 import CreateTeamApiKeyResponse400
from ...models.create_team_api_key_response_401 import CreateTeamApiKeyResponse401
from ...models.create_team_api_key_response_422 import CreateTeamApiKeyResponse422
from ...models.create_team_api_key_response_429 import CreateTeamApiKeyResponse429
from ...models.create_team_api_key_response_500 import CreateTeamApiKeyResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: CreateTeamApiKeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/teams/{team_id}/api_keys".format(
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
    ApiKeyResponse
    | CreateTeamApiKeyResponse400
    | CreateTeamApiKeyResponse401
    | CreateTeamApiKeyResponse422
    | CreateTeamApiKeyResponse429
    | CreateTeamApiKeyResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 201:
        response_201 = ApiKeyResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateTeamApiKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateTeamApiKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = CreateTeamApiKeyResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateTeamApiKeyResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateTeamApiKeyResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiKeyResponse
    | CreateTeamApiKeyResponse400
    | CreateTeamApiKeyResponse401
    | CreateTeamApiKeyResponse422
    | CreateTeamApiKeyResponse429
    | CreateTeamApiKeyResponse500
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
    body: CreateTeamApiKeyBody,
) -> Response[
    ApiKeyResponse
    | CreateTeamApiKeyResponse400
    | CreateTeamApiKeyResponse401
    | CreateTeamApiKeyResponse422
    | CreateTeamApiKeyResponse429
    | CreateTeamApiKeyResponse500
    | ErrorResponse
]:
    """Create an API key for a team

     Create a new API key for a team. Creating a new API key through this endpoint is recorded to the
    audit logs.

    Args:
        team_id (int):
        body (CreateTeamApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | CreateTeamApiKeyResponse400 | CreateTeamApiKeyResponse401 | CreateTeamApiKeyResponse422 | CreateTeamApiKeyResponse429 | CreateTeamApiKeyResponse500 | ErrorResponse]
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
    body: CreateTeamApiKeyBody,
) -> (
    ApiKeyResponse
    | CreateTeamApiKeyResponse400
    | CreateTeamApiKeyResponse401
    | CreateTeamApiKeyResponse422
    | CreateTeamApiKeyResponse429
    | CreateTeamApiKeyResponse500
    | ErrorResponse
    | None
):
    """Create an API key for a team

     Create a new API key for a team. Creating a new API key through this endpoint is recorded to the
    audit logs.

    Args:
        team_id (int):
        body (CreateTeamApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | CreateTeamApiKeyResponse400 | CreateTeamApiKeyResponse401 | CreateTeamApiKeyResponse422 | CreateTeamApiKeyResponse429 | CreateTeamApiKeyResponse500 | ErrorResponse
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
    body: CreateTeamApiKeyBody,
) -> Response[
    ApiKeyResponse
    | CreateTeamApiKeyResponse400
    | CreateTeamApiKeyResponse401
    | CreateTeamApiKeyResponse422
    | CreateTeamApiKeyResponse429
    | CreateTeamApiKeyResponse500
    | ErrorResponse
]:
    """Create an API key for a team

     Create a new API key for a team. Creating a new API key through this endpoint is recorded to the
    audit logs.

    Args:
        team_id (int):
        body (CreateTeamApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | CreateTeamApiKeyResponse400 | CreateTeamApiKeyResponse401 | CreateTeamApiKeyResponse422 | CreateTeamApiKeyResponse429 | CreateTeamApiKeyResponse500 | ErrorResponse]
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
    body: CreateTeamApiKeyBody,
) -> (
    ApiKeyResponse
    | CreateTeamApiKeyResponse400
    | CreateTeamApiKeyResponse401
    | CreateTeamApiKeyResponse422
    | CreateTeamApiKeyResponse429
    | CreateTeamApiKeyResponse500
    | ErrorResponse
    | None
):
    """Create an API key for a team

     Create a new API key for a team. Creating a new API key through this endpoint is recorded to the
    audit logs.

    Args:
        team_id (int):
        body (CreateTeamApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | CreateTeamApiKeyResponse400 | CreateTeamApiKeyResponse401 | CreateTeamApiKeyResponse422 | CreateTeamApiKeyResponse429 | CreateTeamApiKeyResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
