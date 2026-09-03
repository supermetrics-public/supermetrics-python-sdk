from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_response import ApiKeyResponse
from ...models.error_response import ErrorResponse
from ...models.update_workspace_api_key_body import UpdateWorkspaceApiKeyBody
from ...models.update_workspace_api_key_response_400 import UpdateWorkspaceApiKeyResponse400
from ...models.update_workspace_api_key_response_401 import UpdateWorkspaceApiKeyResponse401
from ...models.update_workspace_api_key_response_404 import UpdateWorkspaceApiKeyResponse404
from ...models.update_workspace_api_key_response_422 import UpdateWorkspaceApiKeyResponse422
from ...models.update_workspace_api_key_response_429 import UpdateWorkspaceApiKeyResponse429
from ...models.update_workspace_api_key_response_500 import UpdateWorkspaceApiKeyResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
    *,
    body: UpdateWorkspaceApiKeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/teams/{team_id}/workspaces/{workspace_uuid}/api_keys/{api_key_id}".format(
            team_id=quote(str(team_id), safe=""),
            workspace_uuid=quote(str(workspace_uuid), safe=""),
            api_key_id=quote(str(api_key_id), safe=""),
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
    | ErrorResponse
    | UpdateWorkspaceApiKeyResponse400
    | UpdateWorkspaceApiKeyResponse401
    | UpdateWorkspaceApiKeyResponse404
    | UpdateWorkspaceApiKeyResponse422
    | UpdateWorkspaceApiKeyResponse429
    | UpdateWorkspaceApiKeyResponse500
    | None
):
    if response.status_code == 200:
        response_200 = ApiKeyResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateWorkspaceApiKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateWorkspaceApiKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateWorkspaceApiKeyResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = UpdateWorkspaceApiKeyResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateWorkspaceApiKeyResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateWorkspaceApiKeyResponse500.from_dict(response.json())

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
    | UpdateWorkspaceApiKeyResponse400
    | UpdateWorkspaceApiKeyResponse401
    | UpdateWorkspaceApiKeyResponse404
    | UpdateWorkspaceApiKeyResponse422
    | UpdateWorkspaceApiKeyResponse429
    | UpdateWorkspaceApiKeyResponse500
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
    body: UpdateWorkspaceApiKeyBody,
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | UpdateWorkspaceApiKeyResponse400
    | UpdateWorkspaceApiKeyResponse401
    | UpdateWorkspaceApiKeyResponse404
    | UpdateWorkspaceApiKeyResponse422
    | UpdateWorkspaceApiKeyResponse429
    | UpdateWorkspaceApiKeyResponse500
]:
    """Update an API key for a child workspace

     Update an existing API key belonging to a child workspace, using a parent-team credential. Requires
    the workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):
        body (UpdateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | ErrorResponse | UpdateWorkspaceApiKeyResponse400 | UpdateWorkspaceApiKeyResponse401 | UpdateWorkspaceApiKeyResponse404 | UpdateWorkspaceApiKeyResponse422 | UpdateWorkspaceApiKeyResponse429 | UpdateWorkspaceApiKeyResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        api_key_id=api_key_id,
        body=body,
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
    body: UpdateWorkspaceApiKeyBody,
) -> (
    ApiKeyResponse
    | ErrorResponse
    | UpdateWorkspaceApiKeyResponse400
    | UpdateWorkspaceApiKeyResponse401
    | UpdateWorkspaceApiKeyResponse404
    | UpdateWorkspaceApiKeyResponse422
    | UpdateWorkspaceApiKeyResponse429
    | UpdateWorkspaceApiKeyResponse500
    | None
):
    """Update an API key for a child workspace

     Update an existing API key belonging to a child workspace, using a parent-team credential. Requires
    the workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):
        body (UpdateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | ErrorResponse | UpdateWorkspaceApiKeyResponse400 | UpdateWorkspaceApiKeyResponse401 | UpdateWorkspaceApiKeyResponse404 | UpdateWorkspaceApiKeyResponse422 | UpdateWorkspaceApiKeyResponse429 | UpdateWorkspaceApiKeyResponse500
    """

    return sync_detailed(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        api_key_id=api_key_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateWorkspaceApiKeyBody,
) -> Response[
    ApiKeyResponse
    | ErrorResponse
    | UpdateWorkspaceApiKeyResponse400
    | UpdateWorkspaceApiKeyResponse401
    | UpdateWorkspaceApiKeyResponse404
    | UpdateWorkspaceApiKeyResponse422
    | UpdateWorkspaceApiKeyResponse429
    | UpdateWorkspaceApiKeyResponse500
]:
    """Update an API key for a child workspace

     Update an existing API key belonging to a child workspace, using a parent-team credential. Requires
    the workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):
        body (UpdateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyResponse | ErrorResponse | UpdateWorkspaceApiKeyResponse400 | UpdateWorkspaceApiKeyResponse401 | UpdateWorkspaceApiKeyResponse404 | UpdateWorkspaceApiKeyResponse422 | UpdateWorkspaceApiKeyResponse429 | UpdateWorkspaceApiKeyResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        workspace_uuid=workspace_uuid,
        api_key_id=api_key_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    workspace_uuid: UUID,
    api_key_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateWorkspaceApiKeyBody,
) -> (
    ApiKeyResponse
    | ErrorResponse
    | UpdateWorkspaceApiKeyResponse400
    | UpdateWorkspaceApiKeyResponse401
    | UpdateWorkspaceApiKeyResponse404
    | UpdateWorkspaceApiKeyResponse422
    | UpdateWorkspaceApiKeyResponse429
    | UpdateWorkspaceApiKeyResponse500
    | None
):
    """Update an API key for a child workspace

     Update an existing API key belonging to a child workspace, using a parent-team credential. Requires
    the workspaces_write scope in addition to api_keys_write.

    Args:
        team_id (int):
        workspace_uuid (UUID):
        api_key_id (str):
        body (UpdateWorkspaceApiKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyResponse | ErrorResponse | UpdateWorkspaceApiKeyResponse400 | UpdateWorkspaceApiKeyResponse401 | UpdateWorkspaceApiKeyResponse404 | UpdateWorkspaceApiKeyResponse422 | UpdateWorkspaceApiKeyResponse429 | UpdateWorkspaceApiKeyResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            workspace_uuid=workspace_uuid,
            api_key_id=api_key_id,
            client=client,
            body=body,
        )
    ).parsed
