from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_workspace_response_400 import UpdateWorkspaceResponse400
from ...models.update_workspace_response_401 import UpdateWorkspaceResponse401
from ...models.update_workspace_response_404 import UpdateWorkspaceResponse404
from ...models.update_workspace_response_429 import UpdateWorkspaceResponse429
from ...models.update_workspace_response_500 import UpdateWorkspaceResponse500
from ...models.workspace_response import WorkspaceResponse
from ...models.workspace_update_request import WorkspaceUpdateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    *,
    body: WorkspaceUpdateRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | UpdateWorkspaceResponse400
    | UpdateWorkspaceResponse401
    | UpdateWorkspaceResponse404
    | UpdateWorkspaceResponse429
    | UpdateWorkspaceResponse500
    | WorkspaceResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateWorkspaceResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateWorkspaceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateWorkspaceResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = UpdateWorkspaceResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateWorkspaceResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | UpdateWorkspaceResponse400
    | UpdateWorkspaceResponse401
    | UpdateWorkspaceResponse404
    | UpdateWorkspaceResponse429
    | UpdateWorkspaceResponse500
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
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: WorkspaceUpdateRequest | Unset = UNSET,
) -> Response[
    ErrorResponse
    | UpdateWorkspaceResponse400
    | UpdateWorkspaceResponse401
    | UpdateWorkspaceResponse404
    | UpdateWorkspaceResponse429
    | UpdateWorkspaceResponse500
    | WorkspaceResponse
]:
    """Update a workspace by UUID

     Update a workspace by UUID

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceUpdateRequest | Unset): Workspace fields to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | UpdateWorkspaceResponse400 | UpdateWorkspaceResponse401 | UpdateWorkspaceResponse404 | UpdateWorkspaceResponse429 | UpdateWorkspaceResponse500 | WorkspaceResponse]
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
    body: WorkspaceUpdateRequest | Unset = UNSET,
) -> (
    ErrorResponse
    | UpdateWorkspaceResponse400
    | UpdateWorkspaceResponse401
    | UpdateWorkspaceResponse404
    | UpdateWorkspaceResponse429
    | UpdateWorkspaceResponse500
    | WorkspaceResponse
    | None
):
    """Update a workspace by UUID

     Update a workspace by UUID

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceUpdateRequest | Unset): Workspace fields to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | UpdateWorkspaceResponse400 | UpdateWorkspaceResponse401 | UpdateWorkspaceResponse404 | UpdateWorkspaceResponse429 | UpdateWorkspaceResponse500 | WorkspaceResponse
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
    body: WorkspaceUpdateRequest | Unset = UNSET,
) -> Response[
    ErrorResponse
    | UpdateWorkspaceResponse400
    | UpdateWorkspaceResponse401
    | UpdateWorkspaceResponse404
    | UpdateWorkspaceResponse429
    | UpdateWorkspaceResponse500
    | WorkspaceResponse
]:
    """Update a workspace by UUID

     Update a workspace by UUID

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceUpdateRequest | Unset): Workspace fields to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | UpdateWorkspaceResponse400 | UpdateWorkspaceResponse401 | UpdateWorkspaceResponse404 | UpdateWorkspaceResponse429 | UpdateWorkspaceResponse500 | WorkspaceResponse]
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
    body: WorkspaceUpdateRequest | Unset = UNSET,
) -> (
    ErrorResponse
    | UpdateWorkspaceResponse400
    | UpdateWorkspaceResponse401
    | UpdateWorkspaceResponse404
    | UpdateWorkspaceResponse429
    | UpdateWorkspaceResponse500
    | WorkspaceResponse
    | None
):
    """Update a workspace by UUID

     Update a workspace by UUID

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (WorkspaceUpdateRequest | Unset): Workspace fields to update.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | UpdateWorkspaceResponse400 | UpdateWorkspaceResponse401 | UpdateWorkspaceResponse404 | UpdateWorkspaceResponse429 | UpdateWorkspaceResponse500 | WorkspaceResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            client=client,
            body=body,
        )
    ).parsed
