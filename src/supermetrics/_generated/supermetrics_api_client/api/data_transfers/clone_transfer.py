from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clone_transfer_body import CloneTransferBody
from ...models.clone_transfer_response_400 import CloneTransferResponse400
from ...models.clone_transfer_response_401 import CloneTransferResponse401
from ...models.clone_transfer_response_403 import CloneTransferResponse403
from ...models.clone_transfer_response_404 import CloneTransferResponse404
from ...models.clone_transfer_response_422 import CloneTransferResponse422
from ...models.clone_transfer_response_429 import CloneTransferResponse429
from ...models.clone_transfer_response_500 import CloneTransferResponse500
from ...models.transfer_created_envelope import TransferCreatedEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    transfer_id: int,
    *,
    body: CloneTransferBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/transfers/{transfer_id}/clone".format(
            team_id=quote(str(team_id), safe=""),
            transfer_id=quote(str(transfer_id), safe=""),
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
    CloneTransferResponse400
    | CloneTransferResponse401
    | CloneTransferResponse403
    | CloneTransferResponse404
    | CloneTransferResponse422
    | CloneTransferResponse429
    | CloneTransferResponse500
    | TransferCreatedEnvelope
    | None
):
    if response.status_code == 201:
        response_201 = TransferCreatedEnvelope.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CloneTransferResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CloneTransferResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CloneTransferResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CloneTransferResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = CloneTransferResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = CloneTransferResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CloneTransferResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CloneTransferResponse400
    | CloneTransferResponse401
    | CloneTransferResponse403
    | CloneTransferResponse404
    | CloneTransferResponse422
    | CloneTransferResponse429
    | CloneTransferResponse500
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
    transfer_id: int,
    *,
    client: AuthenticatedClient,
    body: CloneTransferBody | Unset = UNSET,
) -> Response[
    CloneTransferResponse400
    | CloneTransferResponse401
    | CloneTransferResponse403
    | CloneTransferResponse404
    | CloneTransferResponse422
    | CloneTransferResponse429
    | CloneTransferResponse500
    | TransferCreatedEnvelope
]:
    """Clone transfer

     Clones an existing transfer, optionally overriding selected fields. The clone
    is a fully independent transfer — editing or deleting it never affects the source.

    All override fields use the exact same structure as the Create Transfer endpoint.
    Fields not provided in the request body are copied from the source transfer.
    Notification recipients are deliberately not copied (default to empty) but can
    be overridden explicitly.

    **Restrictions:**
    - The data source is always inherited from the source transfer and cannot be overridden.
      To use a different data source, create a new transfer instead.
    - The destination can be changed to a different destination, but only if the target
      destination is the same type as the source (e.g. Snowflake to Snowflake, not
      Snowflake to BigQuery).

    **Returns:** The cloned transfer object with its new ID and display name.

    Args:
        team_id (int):
        transfer_id (int):
        body (CloneTransferBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloneTransferResponse400 | CloneTransferResponse401 | CloneTransferResponse403 | CloneTransferResponse404 | CloneTransferResponse422 | CloneTransferResponse429 | CloneTransferResponse500 | TransferCreatedEnvelope]
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
    body: CloneTransferBody | Unset = UNSET,
) -> (
    CloneTransferResponse400
    | CloneTransferResponse401
    | CloneTransferResponse403
    | CloneTransferResponse404
    | CloneTransferResponse422
    | CloneTransferResponse429
    | CloneTransferResponse500
    | TransferCreatedEnvelope
    | None
):
    """Clone transfer

     Clones an existing transfer, optionally overriding selected fields. The clone
    is a fully independent transfer — editing or deleting it never affects the source.

    All override fields use the exact same structure as the Create Transfer endpoint.
    Fields not provided in the request body are copied from the source transfer.
    Notification recipients are deliberately not copied (default to empty) but can
    be overridden explicitly.

    **Restrictions:**
    - The data source is always inherited from the source transfer and cannot be overridden.
      To use a different data source, create a new transfer instead.
    - The destination can be changed to a different destination, but only if the target
      destination is the same type as the source (e.g. Snowflake to Snowflake, not
      Snowflake to BigQuery).

    **Returns:** The cloned transfer object with its new ID and display name.

    Args:
        team_id (int):
        transfer_id (int):
        body (CloneTransferBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloneTransferResponse400 | CloneTransferResponse401 | CloneTransferResponse403 | CloneTransferResponse404 | CloneTransferResponse422 | CloneTransferResponse429 | CloneTransferResponse500 | TransferCreatedEnvelope
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
    body: CloneTransferBody | Unset = UNSET,
) -> Response[
    CloneTransferResponse400
    | CloneTransferResponse401
    | CloneTransferResponse403
    | CloneTransferResponse404
    | CloneTransferResponse422
    | CloneTransferResponse429
    | CloneTransferResponse500
    | TransferCreatedEnvelope
]:
    """Clone transfer

     Clones an existing transfer, optionally overriding selected fields. The clone
    is a fully independent transfer — editing or deleting it never affects the source.

    All override fields use the exact same structure as the Create Transfer endpoint.
    Fields not provided in the request body are copied from the source transfer.
    Notification recipients are deliberately not copied (default to empty) but can
    be overridden explicitly.

    **Restrictions:**
    - The data source is always inherited from the source transfer and cannot be overridden.
      To use a different data source, create a new transfer instead.
    - The destination can be changed to a different destination, but only if the target
      destination is the same type as the source (e.g. Snowflake to Snowflake, not
      Snowflake to BigQuery).

    **Returns:** The cloned transfer object with its new ID and display name.

    Args:
        team_id (int):
        transfer_id (int):
        body (CloneTransferBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloneTransferResponse400 | CloneTransferResponse401 | CloneTransferResponse403 | CloneTransferResponse404 | CloneTransferResponse422 | CloneTransferResponse429 | CloneTransferResponse500 | TransferCreatedEnvelope]
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
    body: CloneTransferBody | Unset = UNSET,
) -> (
    CloneTransferResponse400
    | CloneTransferResponse401
    | CloneTransferResponse403
    | CloneTransferResponse404
    | CloneTransferResponse422
    | CloneTransferResponse429
    | CloneTransferResponse500
    | TransferCreatedEnvelope
    | None
):
    """Clone transfer

     Clones an existing transfer, optionally overriding selected fields. The clone
    is a fully independent transfer — editing or deleting it never affects the source.

    All override fields use the exact same structure as the Create Transfer endpoint.
    Fields not provided in the request body are copied from the source transfer.
    Notification recipients are deliberately not copied (default to empty) but can
    be overridden explicitly.

    **Restrictions:**
    - The data source is always inherited from the source transfer and cannot be overridden.
      To use a different data source, create a new transfer instead.
    - The destination can be changed to a different destination, but only if the target
      destination is the same type as the source (e.g. Snowflake to Snowflake, not
      Snowflake to BigQuery).

    **Returns:** The cloned transfer object with its new ID and display name.

    Args:
        team_id (int):
        transfer_id (int):
        body (CloneTransferBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloneTransferResponse400 | CloneTransferResponse401 | CloneTransferResponse403 | CloneTransferResponse404 | CloneTransferResponse422 | CloneTransferResponse429 | CloneTransferResponse500 | TransferCreatedEnvelope
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            transfer_id=transfer_id,
            client=client,
            body=body,
        )
    ).parsed
