from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.transfer_configuration_request import TransferConfigurationRequest
from ...models.transfer_updated_response import TransferUpdatedResponse
from ...models.update_transfer_response_400 import UpdateTransferResponse400
from ...models.update_transfer_response_401 import UpdateTransferResponse401
from ...models.update_transfer_response_403 import UpdateTransferResponse403
from ...models.update_transfer_response_404 import UpdateTransferResponse404
from ...models.update_transfer_response_422 import UpdateTransferResponse422
from ...models.update_transfer_response_429 import UpdateTransferResponse429
from ...models.update_transfer_response_500 import UpdateTransferResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_id: int,
    *,
    body: TransferConfigurationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/teams/{team_id}/transfers/{transfer_id}".format(
            team_id=quote(str(team_id), safe=""),
            transfer_id=quote(str(transfer_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    TransferUpdatedResponse
    | UpdateTransferResponse400
    | UpdateTransferResponse401
    | UpdateTransferResponse403
    | UpdateTransferResponse404
    | UpdateTransferResponse422
    | UpdateTransferResponse429
    | UpdateTransferResponse500
    | None
):
    if response.status_code == 200:
        response_200 = TransferUpdatedResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateTransferResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateTransferResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UpdateTransferResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateTransferResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = UpdateTransferResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateTransferResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateTransferResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    TransferUpdatedResponse
    | UpdateTransferResponse400
    | UpdateTransferResponse401
    | UpdateTransferResponse403
    | UpdateTransferResponse404
    | UpdateTransferResponse422
    | UpdateTransferResponse429
    | UpdateTransferResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: TransferConfigurationRequest,
) -> Response[
    TransferUpdatedResponse
    | UpdateTransferResponse400
    | UpdateTransferResponse401
    | UpdateTransferResponse403
    | UpdateTransferResponse404
    | UpdateTransferResponse422
    | UpdateTransferResponse429
    | UpdateTransferResponse500
]:
    """Update transfer configuration

     Updates existing configuration for a Hub transfer.

    **Returns:** Updated transfer object with ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/{transfer_id}/validations` before
    updating
    - The transfer must exist and belong to your team

    Args:
        team_id (int):
        transfer_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferUpdatedResponse | UpdateTransferResponse400 | UpdateTransferResponse401 | UpdateTransferResponse403 | UpdateTransferResponse404 | UpdateTransferResponse422 | UpdateTransferResponse429 | UpdateTransferResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: TransferConfigurationRequest,
) -> (
    TransferUpdatedResponse
    | UpdateTransferResponse400
    | UpdateTransferResponse401
    | UpdateTransferResponse403
    | UpdateTransferResponse404
    | UpdateTransferResponse422
    | UpdateTransferResponse429
    | UpdateTransferResponse500
    | None
):
    """Update transfer configuration

     Updates existing configuration for a Hub transfer.

    **Returns:** Updated transfer object with ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/{transfer_id}/validations` before
    updating
    - The transfer must exist and belong to your team

    Args:
        team_id (int):
        transfer_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferUpdatedResponse | UpdateTransferResponse400 | UpdateTransferResponse401 | UpdateTransferResponse403 | UpdateTransferResponse404 | UpdateTransferResponse422 | UpdateTransferResponse429 | UpdateTransferResponse500
    """

    return sync_detailed(
        team_id=team_id,
        transfer_id=transfer_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: TransferConfigurationRequest,
) -> Response[
    TransferUpdatedResponse
    | UpdateTransferResponse400
    | UpdateTransferResponse401
    | UpdateTransferResponse403
    | UpdateTransferResponse404
    | UpdateTransferResponse422
    | UpdateTransferResponse429
    | UpdateTransferResponse500
]:
    """Update transfer configuration

     Updates existing configuration for a Hub transfer.

    **Returns:** Updated transfer object with ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/{transfer_id}/validations` before
    updating
    - The transfer must exist and belong to your team

    Args:
        team_id (int):
        transfer_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferUpdatedResponse | UpdateTransferResponse400 | UpdateTransferResponse401 | UpdateTransferResponse403 | UpdateTransferResponse404 | UpdateTransferResponse422 | UpdateTransferResponse429 | UpdateTransferResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: TransferConfigurationRequest,
) -> (
    TransferUpdatedResponse
    | UpdateTransferResponse400
    | UpdateTransferResponse401
    | UpdateTransferResponse403
    | UpdateTransferResponse404
    | UpdateTransferResponse422
    | UpdateTransferResponse429
    | UpdateTransferResponse500
    | None
):
    """Update transfer configuration

     Updates existing configuration for a Hub transfer.

    **Returns:** Updated transfer object with ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/{transfer_id}/validations` before
    updating
    - The transfer must exist and belong to your team

    Args:
        team_id (int):
        transfer_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferUpdatedResponse | UpdateTransferResponse400 | UpdateTransferResponse401 | UpdateTransferResponse403 | UpdateTransferResponse404 | UpdateTransferResponse422 | UpdateTransferResponse429 | UpdateTransferResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
            body=body,
        )
    ).parsed
