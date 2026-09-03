from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.remove_workspace_user_response_400 import RemoveWorkspaceUserResponse400
from ...models.remove_workspace_user_response_401 import RemoveWorkspaceUserResponse401
from ...models.remove_workspace_user_response_404 import RemoveWorkspaceUserResponse404
from ...models.remove_workspace_user_response_429 import RemoveWorkspaceUserResponse429
from ...models.remove_workspace_user_response_500 import RemoveWorkspaceUserResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/users/{user_id}".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | ErrorResponse
    | RemoveWorkspaceUserResponse400
    | RemoveWorkspaceUserResponse401
    | RemoveWorkspaceUserResponse404
    | RemoveWorkspaceUserResponse429
    | RemoveWorkspaceUserResponse500
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = RemoveWorkspaceUserResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = RemoveWorkspaceUserResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = RemoveWorkspaceUserResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = RemoveWorkspaceUserResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = RemoveWorkspaceUserResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | ErrorResponse
    | RemoveWorkspaceUserResponse400
    | RemoveWorkspaceUserResponse401
    | RemoveWorkspaceUserResponse404
    | RemoveWorkspaceUserResponse429
    | RemoveWorkspaceUserResponse500
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
) -> Response[
    Any
    | ErrorResponse
    | RemoveWorkspaceUserResponse400
    | RemoveWorkspaceUserResponse401
    | RemoveWorkspaceUserResponse404
    | RemoveWorkspaceUserResponse429
    | RemoveWorkspaceUserResponse500
]:
    """Remove a user from a workspace

     Remove a user from a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse | RemoveWorkspaceUserResponse400 | RemoveWorkspaceUserResponse401 | RemoveWorkspaceUserResponse404 | RemoveWorkspaceUserResponse429 | RemoveWorkspaceUserResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        user_id=user_id,
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
) -> (
    Any
    | ErrorResponse
    | RemoveWorkspaceUserResponse400
    | RemoveWorkspaceUserResponse401
    | RemoveWorkspaceUserResponse404
    | RemoveWorkspaceUserResponse429
    | RemoveWorkspaceUserResponse500
    | None
):
    """Remove a user from a workspace

     Remove a user from a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse | RemoveWorkspaceUserResponse400 | RemoveWorkspaceUserResponse401 | RemoveWorkspaceUserResponse404 | RemoveWorkspaceUserResponse429 | RemoveWorkspaceUserResponse500
    """

    return sync_detailed(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        user_id=user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | ErrorResponse
    | RemoveWorkspaceUserResponse400
    | RemoveWorkspaceUserResponse401
    | RemoveWorkspaceUserResponse404
    | RemoveWorkspaceUserResponse429
    | RemoveWorkspaceUserResponse500
]:
    """Remove a user from a workspace

     Remove a user from a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse | RemoveWorkspaceUserResponse400 | RemoveWorkspaceUserResponse401 | RemoveWorkspaceUserResponse404 | RemoveWorkspaceUserResponse429 | RemoveWorkspaceUserResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    workspace_uuid: UUID,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | ErrorResponse
    | RemoveWorkspaceUserResponse400
    | RemoveWorkspaceUserResponse401
    | RemoveWorkspaceUserResponse404
    | RemoveWorkspaceUserResponse429
    | RemoveWorkspaceUserResponse500
    | None
):
    """Remove a user from a workspace

     Remove a user from a workspace

    Args:
        team_id (int):
        workspace_uuid (UUID):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse | RemoveWorkspaceUserResponse400 | RemoveWorkspaceUserResponse401 | RemoveWorkspaceUserResponse404 | RemoveWorkspaceUserResponse429 | RemoveWorkspaceUserResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            user_id=user_id,
            client=client,
        )
    ).parsed
