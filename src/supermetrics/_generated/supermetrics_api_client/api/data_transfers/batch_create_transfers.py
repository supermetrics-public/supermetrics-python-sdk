from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_create_transfers_body import BatchCreateTransfersBody
from ...models.batch_create_transfers_response_200 import BatchCreateTransfersResponse200
from ...models.batch_create_transfers_response_401 import BatchCreateTransfersResponse401
from ...models.batch_create_transfers_response_403 import BatchCreateTransfersResponse403
from ...models.batch_create_transfers_response_500 import BatchCreateTransfersResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: BatchCreateTransfersBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/transfers/batch".format(
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
    Any
    | BatchCreateTransfersResponse200
    | BatchCreateTransfersResponse401
    | BatchCreateTransfersResponse403
    | BatchCreateTransfersResponse500
    | None
):
    if response.status_code == 200:
        response_200 = BatchCreateTransfersResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = BatchCreateTransfersResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = BatchCreateTransfersResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = BatchCreateTransfersResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | BatchCreateTransfersResponse200
    | BatchCreateTransfersResponse401
    | BatchCreateTransfersResponse403
    | BatchCreateTransfersResponse500
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
    body: BatchCreateTransfersBody,
) -> Response[
    Any
    | BatchCreateTransfersResponse200
    | BatchCreateTransfersResponse401
    | BatchCreateTransfersResponse403
    | BatchCreateTransfersResponse500
]:
    """Batch create transfers

     Create multiple transfers in a single request. Each transfer configuration
    is created independently — if one fails, the others still succeed.
    Mixed data source types are allowed within a single batch.

    The batch must contain between 1 and 100 items. Empty batches, batches
    exceeding 100 items, and exact-duplicate configurations within the same
    batch are rejected. To create copies of an existing transfer, use the
    clone endpoint instead.

    Args:
        team_id (int):
        body (BatchCreateTransfersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BatchCreateTransfersResponse200 | BatchCreateTransfersResponse401 | BatchCreateTransfersResponse403 | BatchCreateTransfersResponse500]
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
    body: BatchCreateTransfersBody,
) -> (
    Any
    | BatchCreateTransfersResponse200
    | BatchCreateTransfersResponse401
    | BatchCreateTransfersResponse403
    | BatchCreateTransfersResponse500
    | None
):
    """Batch create transfers

     Create multiple transfers in a single request. Each transfer configuration
    is created independently — if one fails, the others still succeed.
    Mixed data source types are allowed within a single batch.

    The batch must contain between 1 and 100 items. Empty batches, batches
    exceeding 100 items, and exact-duplicate configurations within the same
    batch are rejected. To create copies of an existing transfer, use the
    clone endpoint instead.

    Args:
        team_id (int):
        body (BatchCreateTransfersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BatchCreateTransfersResponse200 | BatchCreateTransfersResponse401 | BatchCreateTransfersResponse403 | BatchCreateTransfersResponse500
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
    body: BatchCreateTransfersBody,
) -> Response[
    Any
    | BatchCreateTransfersResponse200
    | BatchCreateTransfersResponse401
    | BatchCreateTransfersResponse403
    | BatchCreateTransfersResponse500
]:
    """Batch create transfers

     Create multiple transfers in a single request. Each transfer configuration
    is created independently — if one fails, the others still succeed.
    Mixed data source types are allowed within a single batch.

    The batch must contain between 1 and 100 items. Empty batches, batches
    exceeding 100 items, and exact-duplicate configurations within the same
    batch are rejected. To create copies of an existing transfer, use the
    clone endpoint instead.

    Args:
        team_id (int):
        body (BatchCreateTransfersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BatchCreateTransfersResponse200 | BatchCreateTransfersResponse401 | BatchCreateTransfersResponse403 | BatchCreateTransfersResponse500]
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
    body: BatchCreateTransfersBody,
) -> (
    Any
    | BatchCreateTransfersResponse200
    | BatchCreateTransfersResponse401
    | BatchCreateTransfersResponse403
    | BatchCreateTransfersResponse500
    | None
):
    """Batch create transfers

     Create multiple transfers in a single request. Each transfer configuration
    is created independently — if one fails, the others still succeed.
    Mixed data source types are allowed within a single batch.

    The batch must contain between 1 and 100 items. Empty batches, batches
    exceeding 100 items, and exact-duplicate configurations within the same
    batch are rejected. To create copies of an existing transfer, use the
    clone endpoint instead.

    Args:
        team_id (int):
        body (BatchCreateTransfersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BatchCreateTransfersResponse200 | BatchCreateTransfersResponse401 | BatchCreateTransfersResponse403 | BatchCreateTransfersResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
