from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.change_transfer_state_request import ChangeTransferStateRequest
from ...models.change_transfer_state_response_400 import ChangeTransferStateResponse400
from ...models.change_transfer_state_response_401 import ChangeTransferStateResponse401
from ...models.change_transfer_state_response_403 import ChangeTransferStateResponse403
from ...models.change_transfer_state_response_404 import ChangeTransferStateResponse404
from ...models.change_transfer_state_response_429 import ChangeTransferStateResponse429
from ...models.change_transfer_state_response_500 import ChangeTransferStateResponse500
from ...models.transfer_state_update_response import TransferStateUpdateResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_id: int,
    *,
    body: ChangeTransferStateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/teams/{team_id}/transfers/{transfer_id}/state".format(
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
    ChangeTransferStateResponse400
    | ChangeTransferStateResponse401
    | ChangeTransferStateResponse403
    | ChangeTransferStateResponse404
    | ChangeTransferStateResponse429
    | ChangeTransferStateResponse500
    | TransferStateUpdateResponse
    | None
):
    if response.status_code == 200:
        response_200 = TransferStateUpdateResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ChangeTransferStateResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ChangeTransferStateResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ChangeTransferStateResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ChangeTransferStateResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ChangeTransferStateResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ChangeTransferStateResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ChangeTransferStateResponse400
    | ChangeTransferStateResponse401
    | ChangeTransferStateResponse403
    | ChangeTransferStateResponse404
    | ChangeTransferStateResponse429
    | ChangeTransferStateResponse500
    | TransferStateUpdateResponse
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
    body: ChangeTransferStateRequest,
) -> Response[
    ChangeTransferStateResponse400
    | ChangeTransferStateResponse401
    | ChangeTransferStateResponse403
    | ChangeTransferStateResponse404
    | ChangeTransferStateResponse429
    | ChangeTransferStateResponse500
    | TransferStateUpdateResponse
]:
    r"""Change transfer state

     Change the state of a transfer (pause or resume).

    **Returns:** Transfer state update result with new state.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Valid actions: \"pause\", \"unpause\"
    - Pausing a transfer stops scheduled runs but preserves configuration
    - Resuming a transfer restarts scheduled runs from next scheduled time

    Args:
        team_id (int):
        transfer_id (int):
        body (ChangeTransferStateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangeTransferStateResponse400 | ChangeTransferStateResponse401 | ChangeTransferStateResponse403 | ChangeTransferStateResponse404 | ChangeTransferStateResponse429 | ChangeTransferStateResponse500 | TransferStateUpdateResponse]
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
    body: ChangeTransferStateRequest,
) -> (
    ChangeTransferStateResponse400
    | ChangeTransferStateResponse401
    | ChangeTransferStateResponse403
    | ChangeTransferStateResponse404
    | ChangeTransferStateResponse429
    | ChangeTransferStateResponse500
    | TransferStateUpdateResponse
    | None
):
    r"""Change transfer state

     Change the state of a transfer (pause or resume).

    **Returns:** Transfer state update result with new state.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Valid actions: \"pause\", \"unpause\"
    - Pausing a transfer stops scheduled runs but preserves configuration
    - Resuming a transfer restarts scheduled runs from next scheduled time

    Args:
        team_id (int):
        transfer_id (int):
        body (ChangeTransferStateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangeTransferStateResponse400 | ChangeTransferStateResponse401 | ChangeTransferStateResponse403 | ChangeTransferStateResponse404 | ChangeTransferStateResponse429 | ChangeTransferStateResponse500 | TransferStateUpdateResponse
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
    body: ChangeTransferStateRequest,
) -> Response[
    ChangeTransferStateResponse400
    | ChangeTransferStateResponse401
    | ChangeTransferStateResponse403
    | ChangeTransferStateResponse404
    | ChangeTransferStateResponse429
    | ChangeTransferStateResponse500
    | TransferStateUpdateResponse
]:
    r"""Change transfer state

     Change the state of a transfer (pause or resume).

    **Returns:** Transfer state update result with new state.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Valid actions: \"pause\", \"unpause\"
    - Pausing a transfer stops scheduled runs but preserves configuration
    - Resuming a transfer restarts scheduled runs from next scheduled time

    Args:
        team_id (int):
        transfer_id (int):
        body (ChangeTransferStateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangeTransferStateResponse400 | ChangeTransferStateResponse401 | ChangeTransferStateResponse403 | ChangeTransferStateResponse404 | ChangeTransferStateResponse429 | ChangeTransferStateResponse500 | TransferStateUpdateResponse]
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
    body: ChangeTransferStateRequest,
) -> (
    ChangeTransferStateResponse400
    | ChangeTransferStateResponse401
    | ChangeTransferStateResponse403
    | ChangeTransferStateResponse404
    | ChangeTransferStateResponse429
    | ChangeTransferStateResponse500
    | TransferStateUpdateResponse
    | None
):
    r"""Change transfer state

     Change the state of a transfer (pause or resume).

    **Returns:** Transfer state update result with new state.

    **Important Notes:**
    - The transfer must exist and belong to your team
    - Valid actions: \"pause\", \"unpause\"
    - Pausing a transfer stops scheduled runs but preserves configuration
    - Resuming a transfer restarts scheduled runs from next scheduled time

    Args:
        team_id (int):
        transfer_id (int):
        body (ChangeTransferStateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangeTransferStateResponse400 | ChangeTransferStateResponse401 | ChangeTransferStateResponse403 | ChangeTransferStateResponse404 | ChangeTransferStateResponse429 | ChangeTransferStateResponse500 | TransferStateUpdateResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
            body=body,
        )
    ).parsed
