from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_transfer_response_400 import CreateTransferResponse400
from ...models.create_transfer_response_401 import CreateTransferResponse401
from ...models.create_transfer_response_403 import CreateTransferResponse403
from ...models.create_transfer_response_409 import CreateTransferResponse409
from ...models.create_transfer_response_422 import CreateTransferResponse422
from ...models.create_transfer_response_429 import CreateTransferResponse429
from ...models.create_transfer_response_500 import CreateTransferResponse500
from ...models.transfer_configuration_request import TransferConfigurationRequest
from ...models.transfer_created_envelope import TransferCreatedEnvelope
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: TransferConfigurationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/transfers".format(
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
    CreateTransferResponse400
    | CreateTransferResponse401
    | CreateTransferResponse403
    | CreateTransferResponse409
    | CreateTransferResponse422
    | CreateTransferResponse429
    | CreateTransferResponse500
    | TransferCreatedEnvelope
    | None
):
    if response.status_code == 201:
        response_201 = TransferCreatedEnvelope.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateTransferResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateTransferResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CreateTransferResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = CreateTransferResponse409.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = CreateTransferResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CreateTransferResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateTransferResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateTransferResponse400
    | CreateTransferResponse401
    | CreateTransferResponse403
    | CreateTransferResponse409
    | CreateTransferResponse422
    | CreateTransferResponse429
    | CreateTransferResponse500
    | TransferCreatedEnvelope
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
    body: TransferConfigurationRequest,
) -> Response[
    CreateTransferResponse400
    | CreateTransferResponse401
    | CreateTransferResponse403
    | CreateTransferResponse409
    | CreateTransferResponse422
    | CreateTransferResponse429
    | CreateTransferResponse500
    | TransferCreatedEnvelope
]:
    """Create transfer

     Create a new data transfer from a source to a destination.

    **Returns:** The created transfer object with its ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/validations` before creation
    - Transfer begins processing according to configured schedule
    - Connection to data source must be established first

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTransferResponse400 | CreateTransferResponse401 | CreateTransferResponse403 | CreateTransferResponse409 | CreateTransferResponse422 | CreateTransferResponse429 | CreateTransferResponse500 | TransferCreatedEnvelope]
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
    body: TransferConfigurationRequest,
) -> (
    CreateTransferResponse400
    | CreateTransferResponse401
    | CreateTransferResponse403
    | CreateTransferResponse409
    | CreateTransferResponse422
    | CreateTransferResponse429
    | CreateTransferResponse500
    | TransferCreatedEnvelope
    | None
):
    """Create transfer

     Create a new data transfer from a source to a destination.

    **Returns:** The created transfer object with its ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/validations` before creation
    - Transfer begins processing according to configured schedule
    - Connection to data source must be established first

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTransferResponse400 | CreateTransferResponse401 | CreateTransferResponse403 | CreateTransferResponse409 | CreateTransferResponse422 | CreateTransferResponse429 | CreateTransferResponse500 | TransferCreatedEnvelope
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
    body: TransferConfigurationRequest,
) -> Response[
    CreateTransferResponse400
    | CreateTransferResponse401
    | CreateTransferResponse403
    | CreateTransferResponse409
    | CreateTransferResponse422
    | CreateTransferResponse429
    | CreateTransferResponse500
    | TransferCreatedEnvelope
]:
    """Create transfer

     Create a new data transfer from a source to a destination.

    **Returns:** The created transfer object with its ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/validations` before creation
    - Transfer begins processing according to configured schedule
    - Connection to data source must be established first

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTransferResponse400 | CreateTransferResponse401 | CreateTransferResponse403 | CreateTransferResponse409 | CreateTransferResponse422 | CreateTransferResponse429 | CreateTransferResponse500 | TransferCreatedEnvelope]
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
    body: TransferConfigurationRequest,
) -> (
    CreateTransferResponse400
    | CreateTransferResponse401
    | CreateTransferResponse403
    | CreateTransferResponse409
    | CreateTransferResponse422
    | CreateTransferResponse429
    | CreateTransferResponse500
    | TransferCreatedEnvelope
    | None
):
    """Create transfer

     Create a new data transfer from a source to a destination.

    **Returns:** The created transfer object with its ID and display name.

    **Important Notes:**
    - Validate configuration using `/v1/teams/{team_id}/transfers/validations` before creation
    - Transfer begins processing according to configured schedule
    - Connection to data source must be established first

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTransferResponse400 | CreateTransferResponse401 | CreateTransferResponse403 | CreateTransferResponse409 | CreateTransferResponse422 | CreateTransferResponse429 | CreateTransferResponse500 | TransferCreatedEnvelope
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
