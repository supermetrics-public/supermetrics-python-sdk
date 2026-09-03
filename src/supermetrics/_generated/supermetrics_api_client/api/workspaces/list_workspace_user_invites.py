from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_workspace_user_invites_response_400 import ListWorkspaceUserInvitesResponse400
from ...models.list_workspace_user_invites_response_401 import ListWorkspaceUserInvitesResponse401
from ...models.list_workspace_user_invites_response_404 import ListWorkspaceUserInvitesResponse404
from ...models.list_workspace_user_invites_response_429 import ListWorkspaceUserInvitesResponse429
from ...models.list_workspace_user_invites_response_500 import ListWorkspaceUserInvitesResponse500
from ...models.workspace_invite_list_response import WorkspaceInviteListResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/users/invites".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | ListWorkspaceUserInvitesResponse400
    | ListWorkspaceUserInvitesResponse401
    | ListWorkspaceUserInvitesResponse404
    | ListWorkspaceUserInvitesResponse429
    | ListWorkspaceUserInvitesResponse500
    | WorkspaceInviteListResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceInviteListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ListWorkspaceUserInvitesResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ListWorkspaceUserInvitesResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ListWorkspaceUserInvitesResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ListWorkspaceUserInvitesResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListWorkspaceUserInvitesResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | ListWorkspaceUserInvitesResponse400
    | ListWorkspaceUserInvitesResponse401
    | ListWorkspaceUserInvitesResponse404
    | ListWorkspaceUserInvitesResponse429
    | ListWorkspaceUserInvitesResponse500
    | WorkspaceInviteListResponse
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
) -> Response[
    ErrorResponse
    | ListWorkspaceUserInvitesResponse400
    | ListWorkspaceUserInvitesResponse401
    | ListWorkspaceUserInvitesResponse404
    | ListWorkspaceUserInvitesResponse429
    | ListWorkspaceUserInvitesResponse500
    | WorkspaceInviteListResponse
]:
    """Get pending invitations for a workspace

     Get pending invitations for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListWorkspaceUserInvitesResponse400 | ListWorkspaceUserInvitesResponse401 | ListWorkspaceUserInvitesResponse404 | ListWorkspaceUserInvitesResponse429 | ListWorkspaceUserInvitesResponse500 | WorkspaceInviteListResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
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
) -> (
    ErrorResponse
    | ListWorkspaceUserInvitesResponse400
    | ListWorkspaceUserInvitesResponse401
    | ListWorkspaceUserInvitesResponse404
    | ListWorkspaceUserInvitesResponse429
    | ListWorkspaceUserInvitesResponse500
    | WorkspaceInviteListResponse
    | None
):
    """Get pending invitations for a workspace

     Get pending invitations for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListWorkspaceUserInvitesResponse400 | ListWorkspaceUserInvitesResponse401 | ListWorkspaceUserInvitesResponse404 | ListWorkspaceUserInvitesResponse429 | ListWorkspaceUserInvitesResponse500 | WorkspaceInviteListResponse
    """

    return sync_detailed(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[
    ErrorResponse
    | ListWorkspaceUserInvitesResponse400
    | ListWorkspaceUserInvitesResponse401
    | ListWorkspaceUserInvitesResponse404
    | ListWorkspaceUserInvitesResponse429
    | ListWorkspaceUserInvitesResponse500
    | WorkspaceInviteListResponse
]:
    """Get pending invitations for a workspace

     Get pending invitations for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListWorkspaceUserInvitesResponse400 | ListWorkspaceUserInvitesResponse401 | ListWorkspaceUserInvitesResponse404 | ListWorkspaceUserInvitesResponse429 | ListWorkspaceUserInvitesResponse500 | WorkspaceInviteListResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> (
    ErrorResponse
    | ListWorkspaceUserInvitesResponse400
    | ListWorkspaceUserInvitesResponse401
    | ListWorkspaceUserInvitesResponse404
    | ListWorkspaceUserInvitesResponse429
    | ListWorkspaceUserInvitesResponse500
    | WorkspaceInviteListResponse
    | None
):
    """Get pending invitations for a workspace

     Get pending invitations for a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListWorkspaceUserInvitesResponse400 | ListWorkspaceUserInvitesResponse401 | ListWorkspaceUserInvitesResponse404 | ListWorkspaceUserInvitesResponse429 | ListWorkspaceUserInvitesResponse500 | WorkspaceInviteListResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            client=client,
        )
    ).parsed
