from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_workspace_user_response_400 import UpdateWorkspaceUserResponse400
from ...models.update_workspace_user_response_401 import UpdateWorkspaceUserResponse401
from ...models.update_workspace_user_response_404 import UpdateWorkspaceUserResponse404
from ...models.update_workspace_user_response_429 import UpdateWorkspaceUserResponse429
from ...models.update_workspace_user_response_500 import UpdateWorkspaceUserResponse500
from ...models.workspace_user_response import WorkspaceUserResponse
from ...models.workspace_user_role_update_request import WorkspaceUserRoleUpdateRequest
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    body: WorkspaceUserRoleUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/users/{user_id}".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | UpdateWorkspaceUserResponse400
    | UpdateWorkspaceUserResponse401
    | UpdateWorkspaceUserResponse404
    | UpdateWorkspaceUserResponse429
    | UpdateWorkspaceUserResponse500
    | WorkspaceUserResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceUserResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateWorkspaceUserResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateWorkspaceUserResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateWorkspaceUserResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = UpdateWorkspaceUserResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateWorkspaceUserResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | UpdateWorkspaceUserResponse400
    | UpdateWorkspaceUserResponse401
    | UpdateWorkspaceUserResponse404
    | UpdateWorkspaceUserResponse429
    | UpdateWorkspaceUserResponse500
    | WorkspaceUserResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: WorkspaceUserRoleUpdateRequest,
) -> Response[
    ErrorResponse
    | UpdateWorkspaceUserResponse400
    | UpdateWorkspaceUserResponse401
    | UpdateWorkspaceUserResponse404
    | UpdateWorkspaceUserResponse429
    | UpdateWorkspaceUserResponse500
    | WorkspaceUserResponse
]:
    """Update a workspace user's role

     Update a workspace user's role

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):
        body (WorkspaceUserRoleUpdateRequest): New role to assign to a workspace user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | UpdateWorkspaceUserResponse400 | UpdateWorkspaceUserResponse401 | UpdateWorkspaceUserResponse404 | UpdateWorkspaceUserResponse429 | UpdateWorkspaceUserResponse500 | WorkspaceUserResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: WorkspaceUserRoleUpdateRequest,
) -> (
    ErrorResponse
    | UpdateWorkspaceUserResponse400
    | UpdateWorkspaceUserResponse401
    | UpdateWorkspaceUserResponse404
    | UpdateWorkspaceUserResponse429
    | UpdateWorkspaceUserResponse500
    | WorkspaceUserResponse
    | None
):
    """Update a workspace user's role

     Update a workspace user's role

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):
        body (WorkspaceUserRoleUpdateRequest): New role to assign to a workspace user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | UpdateWorkspaceUserResponse400 | UpdateWorkspaceUserResponse401 | UpdateWorkspaceUserResponse404 | UpdateWorkspaceUserResponse429 | UpdateWorkspaceUserResponse500 | WorkspaceUserResponse
    """

    return sync_detailed(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: WorkspaceUserRoleUpdateRequest,
) -> Response[
    ErrorResponse
    | UpdateWorkspaceUserResponse400
    | UpdateWorkspaceUserResponse401
    | UpdateWorkspaceUserResponse404
    | UpdateWorkspaceUserResponse429
    | UpdateWorkspaceUserResponse500
    | WorkspaceUserResponse
]:
    """Update a workspace user's role

     Update a workspace user's role

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):
        body (WorkspaceUserRoleUpdateRequest): New role to assign to a workspace user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | UpdateWorkspaceUserResponse400 | UpdateWorkspaceUserResponse401 | UpdateWorkspaceUserResponse404 | UpdateWorkspaceUserResponse429 | UpdateWorkspaceUserResponse500 | WorkspaceUserResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: WorkspaceUserRoleUpdateRequest,
) -> (
    ErrorResponse
    | UpdateWorkspaceUserResponse400
    | UpdateWorkspaceUserResponse401
    | UpdateWorkspaceUserResponse404
    | UpdateWorkspaceUserResponse429
    | UpdateWorkspaceUserResponse500
    | WorkspaceUserResponse
    | None
):
    """Update a workspace user's role

     Update a workspace user's role

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):
        body (WorkspaceUserRoleUpdateRequest): New role to assign to a workspace user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | UpdateWorkspaceUserResponse400 | UpdateWorkspaceUserResponse401 | UpdateWorkspaceUserResponse404 | UpdateWorkspaceUserResponse429 | UpdateWorkspaceUserResponse500 | WorkspaceUserResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
