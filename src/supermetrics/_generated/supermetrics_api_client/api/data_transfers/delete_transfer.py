from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_transfer_response_401 import DeleteTransferResponse401
from ...models.delete_transfer_response_403 import DeleteTransferResponse403
from ...models.delete_transfer_response_404 import DeleteTransferResponse404
from ...models.delete_transfer_response_429 import DeleteTransferResponse429
from ...models.delete_transfer_response_500 import DeleteTransferResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    transfer_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/teams/{team_id}/transfers/{transfer_id}".format(
            team_id=quote(str(team_id), safe=""),
            transfer_id=quote(str(transfer_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | DeleteTransferResponse401
    | DeleteTransferResponse403
    | DeleteTransferResponse404
    | DeleteTransferResponse429
    | DeleteTransferResponse500
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 401:
        response_401 = DeleteTransferResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = DeleteTransferResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = DeleteTransferResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = DeleteTransferResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = DeleteTransferResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | DeleteTransferResponse401
    | DeleteTransferResponse403
    | DeleteTransferResponse404
    | DeleteTransferResponse429
    | DeleteTransferResponse500
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
) -> Response[
    Any
    | DeleteTransferResponse401
    | DeleteTransferResponse403
    | DeleteTransferResponse404
    | DeleteTransferResponse429
    | DeleteTransferResponse500
]:
    """Delete transfer

     Delete an existing transfer (soft delete).

    **Returns:** No content on success (HTTP 204).

    **Important Notes:**
    - The transfer must exist and belong to your team
    - This is a soft delete - transfer data is preserved
    - Associated table settings are also cleaned up

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteTransferResponse401 | DeleteTransferResponse403 | DeleteTransferResponse404 | DeleteTransferResponse429 | DeleteTransferResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
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
) -> (
    Any
    | DeleteTransferResponse401
    | DeleteTransferResponse403
    | DeleteTransferResponse404
    | DeleteTransferResponse429
    | DeleteTransferResponse500
    | None
):
    """Delete transfer

     Delete an existing transfer (soft delete).

    **Returns:** No content on success (HTTP 204).

    **Important Notes:**
    - The transfer must exist and belong to your team
    - This is a soft delete - transfer data is preserved
    - Associated table settings are also cleaned up

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteTransferResponse401 | DeleteTransferResponse403 | DeleteTransferResponse404 | DeleteTransferResponse429 | DeleteTransferResponse500
    """

    return sync_detailed(
        team_id=team_id,
        transfer_id=transfer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | DeleteTransferResponse401
    | DeleteTransferResponse403
    | DeleteTransferResponse404
    | DeleteTransferResponse429
    | DeleteTransferResponse500
]:
    """Delete transfer

     Delete an existing transfer (soft delete).

    **Returns:** No content on success (HTTP 204).

    **Important Notes:**
    - The transfer must exist and belong to your team
    - This is a soft delete - transfer data is preserved
    - Associated table settings are also cleaned up

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteTransferResponse401 | DeleteTransferResponse403 | DeleteTransferResponse404 | DeleteTransferResponse429 | DeleteTransferResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        transfer_id=transfer_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    transfer_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | DeleteTransferResponse401
    | DeleteTransferResponse403
    | DeleteTransferResponse404
    | DeleteTransferResponse429
    | DeleteTransferResponse500
    | None
):
    """Delete transfer

     Delete an existing transfer (soft delete).

    **Returns:** No content on success (HTTP 204).

    **Important Notes:**
    - The transfer must exist and belong to your team
    - This is a soft delete - transfer data is preserved
    - Associated table settings are also cleaned up

    Args:
        team_id (int):
        transfer_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteTransferResponse401 | DeleteTransferResponse403 | DeleteTransferResponse404 | DeleteTransferResponse429 | DeleteTransferResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
        )
    ).parsed
