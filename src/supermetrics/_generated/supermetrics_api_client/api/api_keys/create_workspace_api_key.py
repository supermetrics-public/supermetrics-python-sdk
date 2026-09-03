from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_response import ApiKeyResponse
from ...models.create_workspace_api_key_body import CreateWorkspaceApiKeyBody
from ...models.create_workspace_api_key_response_400 import CreateWorkspaceApiKeyResponse400
from ...models.create_workspace_api_key_response_401 import CreateWorkspaceApiKeyResponse401
from ...models.create_workspace_api_key_response_404 import CreateWorkspaceApiKeyResponse404
from ...models.create_workspace_api_key_response_422 import CreateWorkspaceApiKeyResponse422
from ...models.create_workspace_api_key_response_429 import CreateWorkspaceApiKeyResponse429
from ...models.create_workspace_api_key_response_500 import CreateWorkspaceApiKeyResponse500
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    *,
    body: CreateWorkspaceApiKeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/api_keys".format(
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
    ApiKeyResponse
    | CreateWorkspaceApiKeyResponse400
    | CreateWorkspaceApiKeyResponse401
    | CreateWorkspaceApiKeyResponse404
    | CreateWorkspaceApiKeyResponse422
    | CreateWorkspaceApiKeyResponse429
    | CreateWorkspaceApiKeyResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 201:
        response_201 = ApiKeyResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateWorkspaceApiKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateWorkspaceApiKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CreateWorkspaceApiKeyResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = CreateWorkspaceApiKeyResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateWorkspaceApiKeyResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateWorkspaceApiKeyResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ApiKeyResponse
    | CreateWorkspaceApiKeyResponse400
    | CreateWorkspaceApiKeyResponse401
    | CreateWorkspaceApiKeyResponse404
    | CreateWorkspaceApiKeyResponse422
    | CreateWorkspaceApiKeyResponse429
    | CreateWorkspaceApiKeyResponse500
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
    workspace_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateWorkspaceApiKeyBody,
) -> Response[
    ApiKeyResponse
    | CreateWorkspaceApiKeyResponse400
    | CreateWorkspaceApiKeyResponse401
    | CreateWorkspaceApiKeyResponse404
    | CreateWorkspaceApiKeyResponse422
    | CreateWorkspaceApiKeyResponse429
    | CreateWorkspaceApiKeyResponse500
    | ErrorResponse
]:
    """Create an API key for a child workspace

     Create a new API key for a child workspace, using a parent-team credential. The key is scoped to the
    child workspace and can only be created on behalf of a child-workspace user. Requires the
    workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (CreateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | CreateWorkspaceApiKeyResponse400 | CreateWorkspaceApiKeyResponse401 | CreateWorkspaceApiKeyResponse404 | CreateWorkspaceApiKeyResponse422 | CreateWorkspaceApiKeyResponse429 | CreateWorkspaceApiKeyResponse500 | ErrorResponse]
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
    body: CreateWorkspaceApiKeyBody,
) -> (
    ApiKeyResponse
    | CreateWorkspaceApiKeyResponse400
    | CreateWorkspaceApiKeyResponse401
    | CreateWorkspaceApiKeyResponse404
    | CreateWorkspaceApiKeyResponse422
    | CreateWorkspaceApiKeyResponse429
    | CreateWorkspaceApiKeyResponse500
    | ErrorResponse
    | None
):
    """Create an API key for a child workspace

     Create a new API key for a child workspace, using a parent-team credential. The key is scoped to the
    child workspace and can only be created on behalf of a child-workspace user. Requires the
    workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (CreateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | CreateWorkspaceApiKeyResponse400 | CreateWorkspaceApiKeyResponse401 | CreateWorkspaceApiKeyResponse404 | CreateWorkspaceApiKeyResponse422 | CreateWorkspaceApiKeyResponse429 | CreateWorkspaceApiKeyResponse500 | ErrorResponse
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
    body: CreateWorkspaceApiKeyBody,
) -> Response[
    ApiKeyResponse
    | CreateWorkspaceApiKeyResponse400
    | CreateWorkspaceApiKeyResponse401
    | CreateWorkspaceApiKeyResponse404
    | CreateWorkspaceApiKeyResponse422
    | CreateWorkspaceApiKeyResponse429
    | CreateWorkspaceApiKeyResponse500
    | ErrorResponse
]:
    """Create an API key for a child workspace

     Create a new API key for a child workspace, using a parent-team credential. The key is scoped to the
    child workspace and can only be created on behalf of a child-workspace user. Requires the
    workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (CreateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | CreateWorkspaceApiKeyResponse400 | CreateWorkspaceApiKeyResponse401 | CreateWorkspaceApiKeyResponse404 | CreateWorkspaceApiKeyResponse422 | CreateWorkspaceApiKeyResponse429 | CreateWorkspaceApiKeyResponse500 | ErrorResponse]
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
    body: CreateWorkspaceApiKeyBody,
) -> (
    ApiKeyResponse
    | CreateWorkspaceApiKeyResponse400
    | CreateWorkspaceApiKeyResponse401
    | CreateWorkspaceApiKeyResponse404
    | CreateWorkspaceApiKeyResponse422
    | CreateWorkspaceApiKeyResponse429
    | CreateWorkspaceApiKeyResponse500
    | ErrorResponse
    | None
):
    """Create an API key for a child workspace

     Create a new API key for a child workspace, using a parent-team credential. The key is scoped to the
    child workspace and can only be created on behalf of a child-workspace user. Requires the
    workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        body (CreateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | CreateWorkspaceApiKeyResponse400 | CreateWorkspaceApiKeyResponse401 | CreateWorkspaceApiKeyResponse404 | CreateWorkspaceApiKeyResponse422 | CreateWorkspaceApiKeyResponse429 | CreateWorkspaceApiKeyResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            client=client,
            body=body,
        )
    ).parsed
