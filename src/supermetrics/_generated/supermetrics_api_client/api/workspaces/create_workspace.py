from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_workspace_response_400 import CreateWorkspaceResponse400
from ...models.create_workspace_response_401 import CreateWorkspaceResponse401
from ...models.create_workspace_response_404 import CreateWorkspaceResponse404
from ...models.create_workspace_response_429 import CreateWorkspaceResponse429
from ...models.create_workspace_response_500 import CreateWorkspaceResponse500
from ...models.error_response import ErrorResponse
from ...models.workspace_create_request import WorkspaceCreateRequest
from ...models.workspace_response import WorkspaceResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: WorkspaceCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/teams/{team_id}/workspaces".format(
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
    CreateWorkspaceResponse400
    | CreateWorkspaceResponse401
    | CreateWorkspaceResponse404
    | CreateWorkspaceResponse429
    | CreateWorkspaceResponse500
    | ErrorResponse
    | WorkspaceResponse
    | None
):
    if response.status_code == 201:
        response_201 = WorkspaceResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateWorkspaceResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateWorkspaceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CreateWorkspaceResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = CreateWorkspaceResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateWorkspaceResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateWorkspaceResponse400
    | CreateWorkspaceResponse401
    | CreateWorkspaceResponse404
    | CreateWorkspaceResponse429
    | CreateWorkspaceResponse500
    | ErrorResponse
    | WorkspaceResponse
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
    body: WorkspaceCreateRequest,
) -> Response[
    CreateWorkspaceResponse400
    | CreateWorkspaceResponse401
    | CreateWorkspaceResponse404
    | CreateWorkspaceResponse429
    | CreateWorkspaceResponse500
    | ErrorResponse
    | WorkspaceResponse
]:
    """Create a new sub-workspace

     Create a new sub-workspace

    Args:
        team_id (int):
        body (WorkspaceCreateRequest): Payload for creating a new sub-workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateWorkspaceResponse400 | CreateWorkspaceResponse401 | CreateWorkspaceResponse404 | CreateWorkspaceResponse429 | CreateWorkspaceResponse500 | ErrorResponse | WorkspaceResponse]
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
    body: WorkspaceCreateRequest,
) -> (
    CreateWorkspaceResponse400
    | CreateWorkspaceResponse401
    | CreateWorkspaceResponse404
    | CreateWorkspaceResponse429
    | CreateWorkspaceResponse500
    | ErrorResponse
    | WorkspaceResponse
    | None
):
    """Create a new sub-workspace

     Create a new sub-workspace

    Args:
        team_id (int):
        body (WorkspaceCreateRequest): Payload for creating a new sub-workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateWorkspaceResponse400 | CreateWorkspaceResponse401 | CreateWorkspaceResponse404 | CreateWorkspaceResponse429 | CreateWorkspaceResponse500 | ErrorResponse | WorkspaceResponse
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
    body: WorkspaceCreateRequest,
) -> Response[
    CreateWorkspaceResponse400
    | CreateWorkspaceResponse401
    | CreateWorkspaceResponse404
    | CreateWorkspaceResponse429
    | CreateWorkspaceResponse500
    | ErrorResponse
    | WorkspaceResponse
]:
    """Create a new sub-workspace

     Create a new sub-workspace

    Args:
        team_id (int):
        body (WorkspaceCreateRequest): Payload for creating a new sub-workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateWorkspaceResponse400 | CreateWorkspaceResponse401 | CreateWorkspaceResponse404 | CreateWorkspaceResponse429 | CreateWorkspaceResponse500 | ErrorResponse | WorkspaceResponse]
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
    body: WorkspaceCreateRequest,
) -> (
    CreateWorkspaceResponse400
    | CreateWorkspaceResponse401
    | CreateWorkspaceResponse404
    | CreateWorkspaceResponse429
    | CreateWorkspaceResponse500
    | ErrorResponse
    | WorkspaceResponse
    | None
):
    """Create a new sub-workspace

     Create a new sub-workspace

    Args:
        team_id (int):
        body (WorkspaceCreateRequest): Payload for creating a new sub-workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateWorkspaceResponse400 | CreateWorkspaceResponse401 | CreateWorkspaceResponse404 | CreateWorkspaceResponse429 | CreateWorkspaceResponse500 | ErrorResponse | WorkspaceResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
