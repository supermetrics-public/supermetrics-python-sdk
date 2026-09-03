from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_workspace_user_invite_response_400 import UpdateWorkspaceUserInviteResponse400
from ...models.update_workspace_user_invite_response_401 import UpdateWorkspaceUserInviteResponse401
from ...models.update_workspace_user_invite_response_404 import UpdateWorkspaceUserInviteResponse404
from ...models.update_workspace_user_invite_response_429 import UpdateWorkspaceUserInviteResponse429
from ...models.update_workspace_user_invite_response_500 import UpdateWorkspaceUserInviteResponse500
from ...models.workspace_invite_response import WorkspaceInviteResponse
from ...models.workspace_invite_status_update_request import WorkspaceInviteStatusUpdateRequest
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    *,
    body: WorkspaceInviteStatusUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/users/invites".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
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
    | UpdateWorkspaceUserInviteResponse400
    | UpdateWorkspaceUserInviteResponse401
    | UpdateWorkspaceUserInviteResponse404
    | UpdateWorkspaceUserInviteResponse429
    | UpdateWorkspaceUserInviteResponse500
    | WorkspaceInviteResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceInviteResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateWorkspaceUserInviteResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateWorkspaceUserInviteResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateWorkspaceUserInviteResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = UpdateWorkspaceUserInviteResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateWorkspaceUserInviteResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | UpdateWorkspaceUserInviteResponse400
    | UpdateWorkspaceUserInviteResponse401
    | UpdateWorkspaceUserInviteResponse404
    | UpdateWorkspaceUserInviteResponse429
    | UpdateWorkspaceUserInviteResponse500
    | WorkspaceInviteResponse
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
    *,
    client: AuthenticatedClient,
    body: WorkspaceInviteStatusUpdateRequest,
) -> Response[
    ErrorResponse
    | UpdateWorkspaceUserInviteResponse400
    | UpdateWorkspaceUserInviteResponse401
    | UpdateWorkspaceUserInviteResponse404
    | UpdateWorkspaceUserInviteResponse429
    | UpdateWorkspaceUserInviteResponse500
    | WorkspaceInviteResponse
]:
    """Update invitation status for a workspace

     Update invitation status for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceInviteStatusUpdateRequest): Invitation status update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | UpdateWorkspaceUserInviteResponse400 | UpdateWorkspaceUserInviteResponse401 | UpdateWorkspaceUserInviteResponse404 | UpdateWorkspaceUserInviteResponse429 | UpdateWorkspaceUserInviteResponse500 | WorkspaceInviteResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: WorkspaceInviteStatusUpdateRequest,
) -> (
    ErrorResponse
    | UpdateWorkspaceUserInviteResponse400
    | UpdateWorkspaceUserInviteResponse401
    | UpdateWorkspaceUserInviteResponse404
    | UpdateWorkspaceUserInviteResponse429
    | UpdateWorkspaceUserInviteResponse500
    | WorkspaceInviteResponse
    | None
):
    """Update invitation status for a workspace

     Update invitation status for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceInviteStatusUpdateRequest): Invitation status update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | UpdateWorkspaceUserInviteResponse400 | UpdateWorkspaceUserInviteResponse401 | UpdateWorkspaceUserInviteResponse404 | UpdateWorkspaceUserInviteResponse429 | UpdateWorkspaceUserInviteResponse500 | WorkspaceInviteResponse
    """

    return sync_detailed(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: WorkspaceInviteStatusUpdateRequest,
) -> Response[
    ErrorResponse
    | UpdateWorkspaceUserInviteResponse400
    | UpdateWorkspaceUserInviteResponse401
    | UpdateWorkspaceUserInviteResponse404
    | UpdateWorkspaceUserInviteResponse429
    | UpdateWorkspaceUserInviteResponse500
    | WorkspaceInviteResponse
]:
    """Update invitation status for a workspace

     Update invitation status for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceInviteStatusUpdateRequest): Invitation status update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | UpdateWorkspaceUserInviteResponse400 | UpdateWorkspaceUserInviteResponse401 | UpdateWorkspaceUserInviteResponse404 | UpdateWorkspaceUserInviteResponse429 | UpdateWorkspaceUserInviteResponse500 | WorkspaceInviteResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: WorkspaceInviteStatusUpdateRequest,
) -> (
    ErrorResponse
    | UpdateWorkspaceUserInviteResponse400
    | UpdateWorkspaceUserInviteResponse401
    | UpdateWorkspaceUserInviteResponse404
    | UpdateWorkspaceUserInviteResponse429
    | UpdateWorkspaceUserInviteResponse500
    | WorkspaceInviteResponse
    | None
):
    """Update invitation status for a workspace

     Update invitation status for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceInviteStatusUpdateRequest): Invitation status update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | UpdateWorkspaceUserInviteResponse400 | UpdateWorkspaceUserInviteResponse401 | UpdateWorkspaceUserInviteResponse404 | UpdateWorkspaceUserInviteResponse429 | UpdateWorkspaceUserInviteResponse500 | WorkspaceInviteResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            client=client,
            body=body,
        )
    ).parsed
