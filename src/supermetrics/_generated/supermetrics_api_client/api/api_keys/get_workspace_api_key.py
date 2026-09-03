from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_response import ApiKeyResponse
from ...models.error_response import ErrorResponse
from ...models.get_workspace_api_key_response_400 import GetWorkspaceApiKeyResponse400
from ...models.get_workspace_api_key_response_401 import GetWorkspaceApiKeyResponse401
from ...models.get_workspace_api_key_response_404 import GetWorkspaceApiKeyResponse404
from ...models.get_workspace_api_key_response_429 import GetWorkspaceApiKeyResponse429
from ...models.get_workspace_api_key_response_500 import GetWorkspaceApiKeyResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/api_keys/{api_key_id}".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
            api_key_id=quote(str(api_key_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ApiKeyResponse
    | ErrorResponse
    | GetWorkspaceApiKeyResponse400
    | GetWorkspaceApiKeyResponse401
    | GetWorkspaceApiKeyResponse404
    | GetWorkspaceApiKeyResponse429
    | GetWorkspaceApiKeyResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ApiKeyResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetWorkspaceApiKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetWorkspaceApiKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetWorkspaceApiKeyResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = GetWorkspaceApiKeyResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = GetWorkspaceApiKeyResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | GetWorkspaceApiKeyResponse400
    | GetWorkspaceApiKeyResponse401
    | GetWorkspaceApiKeyResponse404
    | GetWorkspaceApiKeyResponse429
    | GetWorkspaceApiKeyResponse500
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
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | GetWorkspaceApiKeyResponse400
    | GetWorkspaceApiKeyResponse401
    | GetWorkspaceApiKeyResponse404
    | GetWorkspaceApiKeyResponse429
    | GetWorkspaceApiKeyResponse500
]:
    """Get an API key for a child workspace

     Retrieve details of a specific API key belonging to a child workspace, using a parent-team
    credential. Requires the workspaces_read scope in addition to api_keys_read.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | ErrorResponse | GetWorkspaceApiKeyResponse400 | GetWorkspaceApiKeyResponse401 | GetWorkspaceApiKeyResponse404 | GetWorkspaceApiKeyResponse429 | GetWorkspaceApiKeyResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        api_key_id=api_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ApiKeyResponse
    | ErrorResponse
    | GetWorkspaceApiKeyResponse400
    | GetWorkspaceApiKeyResponse401
    | GetWorkspaceApiKeyResponse404
    | GetWorkspaceApiKeyResponse429
    | GetWorkspaceApiKeyResponse500
    | None
):
    """Get an API key for a child workspace

     Retrieve details of a specific API key belonging to a child workspace, using a parent-team
    credential. Requires the workspaces_read scope in addition to api_keys_read.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | ErrorResponse | GetWorkspaceApiKeyResponse400 | GetWorkspaceApiKeyResponse401 | GetWorkspaceApiKeyResponse404 | GetWorkspaceApiKeyResponse429 | GetWorkspaceApiKeyResponse500
    """

    return sync_detailed(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        api_key_id=api_key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | GetWorkspaceApiKeyResponse400
    | GetWorkspaceApiKeyResponse401
    | GetWorkspaceApiKeyResponse404
    | GetWorkspaceApiKeyResponse429
    | GetWorkspaceApiKeyResponse500
]:
    """Get an API key for a child workspace

     Retrieve details of a specific API key belonging to a child workspace, using a parent-team
    credential. Requires the workspaces_read scope in addition to api_keys_read.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | ErrorResponse | GetWorkspaceApiKeyResponse400 | GetWorkspaceApiKeyResponse401 | GetWorkspaceApiKeyResponse404 | GetWorkspaceApiKeyResponse429 | GetWorkspaceApiKeyResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        api_key_id=api_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    ApiKeyResponse
    | ErrorResponse
    | GetWorkspaceApiKeyResponse400
    | GetWorkspaceApiKeyResponse401
    | GetWorkspaceApiKeyResponse404
    | GetWorkspaceApiKeyResponse429
    | GetWorkspaceApiKeyResponse500
    | None
):
    """Get an API key for a child workspace

     Retrieve details of a specific API key belonging to a child workspace, using a parent-team
    credential. Requires the workspaces_read scope in addition to api_keys_read.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | ErrorResponse | GetWorkspaceApiKeyResponse400 | GetWorkspaceApiKeyResponse401 | GetWorkspaceApiKeyResponse404 | GetWorkspaceApiKeyResponse429 | GetWorkspaceApiKeyResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            api_key_id=api_key_id,
            client=client,
        )
    ).parsed
