from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_update_destinations_body import BatchUpdateDestinationsBody
from ...models.batch_update_destinations_response_200 import BatchUpdateDestinationsResponse200
from ...models.batch_update_destinations_response_400 import BatchUpdateDestinationsResponse400
from ...models.batch_update_destinations_response_401 import BatchUpdateDestinationsResponse401
from ...models.batch_update_destinations_response_403 import BatchUpdateDestinationsResponse403
from ...models.batch_update_destinations_response_500 import BatchUpdateDestinationsResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: BatchUpdateDestinationsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/teams/{team_id}/destinations/batch".format(
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
    BatchUpdateDestinationsResponse200
    | BatchUpdateDestinationsResponse400
    | BatchUpdateDestinationsResponse401
    | BatchUpdateDestinationsResponse403
    | BatchUpdateDestinationsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = BatchUpdateDestinationsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = BatchUpdateDestinationsResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = BatchUpdateDestinationsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = BatchUpdateDestinationsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = BatchUpdateDestinationsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BatchUpdateDestinationsResponse200
    | BatchUpdateDestinationsResponse400
    | BatchUpdateDestinationsResponse401
    | BatchUpdateDestinationsResponse403
    | BatchUpdateDestinationsResponse500
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
    body: BatchUpdateDestinationsBody,
) -> Response[
    BatchUpdateDestinationsResponse200
    | BatchUpdateDestinationsResponse400
    | BatchUpdateDestinationsResponse401
    | BatchUpdateDestinationsResponse403
    | BatchUpdateDestinationsResponse500
]:
    """Batch rotate destination secrets

     Rotate secrets for multiple destinations of the same type in a single request.
    Each update is applied independently — if one fails, the others still succeed.

    Batch-level validations (checked before any processing):
    - The updates array must contain between 1 and 100 items.
    - Each item must include a valid destination_id and a non-empty new_secret.
    - Duplicate destination_id values are not allowed.

    Args:
        team_id (int):
        body (BatchUpdateDestinationsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchUpdateDestinationsResponse200 | BatchUpdateDestinationsResponse400 | BatchUpdateDestinationsResponse401 | BatchUpdateDestinationsResponse403 | BatchUpdateDestinationsResponse500]
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
    body: BatchUpdateDestinationsBody,
) -> (
    BatchUpdateDestinationsResponse200
    | BatchUpdateDestinationsResponse400
    | BatchUpdateDestinationsResponse401
    | BatchUpdateDestinationsResponse403
    | BatchUpdateDestinationsResponse500
    | None
):
    """Batch rotate destination secrets

     Rotate secrets for multiple destinations of the same type in a single request.
    Each update is applied independently — if one fails, the others still succeed.

    Batch-level validations (checked before any processing):
    - The updates array must contain between 1 and 100 items.
    - Each item must include a valid destination_id and a non-empty new_secret.
    - Duplicate destination_id values are not allowed.

    Args:
        team_id (int):
        body (BatchUpdateDestinationsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchUpdateDestinationsResponse200 | BatchUpdateDestinationsResponse400 | BatchUpdateDestinationsResponse401 | BatchUpdateDestinationsResponse403 | BatchUpdateDestinationsResponse500
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
    body: BatchUpdateDestinationsBody,
) -> Response[
    BatchUpdateDestinationsResponse200
    | BatchUpdateDestinationsResponse400
    | BatchUpdateDestinationsResponse401
    | BatchUpdateDestinationsResponse403
    | BatchUpdateDestinationsResponse500
]:
    """Batch rotate destination secrets

     Rotate secrets for multiple destinations of the same type in a single request.
    Each update is applied independently — if one fails, the others still succeed.

    Batch-level validations (checked before any processing):
    - The updates array must contain between 1 and 100 items.
    - Each item must include a valid destination_id and a non-empty new_secret.
    - Duplicate destination_id values are not allowed.

    Args:
        team_id (int):
        body (BatchUpdateDestinationsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchUpdateDestinationsResponse200 | BatchUpdateDestinationsResponse400 | BatchUpdateDestinationsResponse401 | BatchUpdateDestinationsResponse403 | BatchUpdateDestinationsResponse500]
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
    body: BatchUpdateDestinationsBody,
) -> (
    BatchUpdateDestinationsResponse200
    | BatchUpdateDestinationsResponse400
    | BatchUpdateDestinationsResponse401
    | BatchUpdateDestinationsResponse403
    | BatchUpdateDestinationsResponse500
    | None
):
    """Batch rotate destination secrets

     Rotate secrets for multiple destinations of the same type in a single request.
    Each update is applied independently — if one fails, the others still succeed.

    Batch-level validations (checked before any processing):
    - The updates array must contain between 1 and 100 items.
    - Each item must include a valid destination_id and a non-empty new_secret.
    - Duplicate destination_id values are not allowed.

    Args:
        team_id (int):
        body (BatchUpdateDestinationsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchUpdateDestinationsResponse200 | BatchUpdateDestinationsResponse400 | BatchUpdateDestinationsResponse401 | BatchUpdateDestinationsResponse403 | BatchUpdateDestinationsResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
