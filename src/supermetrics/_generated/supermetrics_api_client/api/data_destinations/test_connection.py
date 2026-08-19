from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.test_connection_request import TestConnectionRequest
from ...models.test_connection_response import TestConnectionResponse
from ...models.test_connection_response_400 import TestConnectionResponse400
from ...models.test_connection_response_401 import TestConnectionResponse401
from ...models.test_connection_response_403 import TestConnectionResponse403
from ...models.test_connection_response_422 import TestConnectionResponse422
from ...models.test_connection_response_429 import TestConnectionResponse429
from ...models.test_connection_response_500 import TestConnectionResponse500
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: TestConnectionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/destinations/test-connection".format(
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
    TestConnectionResponse
    | TestConnectionResponse400
    | TestConnectionResponse401
    | TestConnectionResponse403
    | TestConnectionResponse422
    | TestConnectionResponse429
    | TestConnectionResponse500
    | None
):
    if response.status_code == 200:
        response_200 = TestConnectionResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = TestConnectionResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = TestConnectionResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = TestConnectionResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = TestConnectionResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = TestConnectionResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = TestConnectionResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    TestConnectionResponse
    | TestConnectionResponse400
    | TestConnectionResponse401
    | TestConnectionResponse403
    | TestConnectionResponse422
    | TestConnectionResponse429
    | TestConnectionResponse500
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
    body: TestConnectionRequest,
) -> Response[
    TestConnectionResponse
    | TestConnectionResponse400
    | TestConnectionResponse401
    | TestConnectionResponse403
    | TestConnectionResponse422
    | TestConnectionResponse429
    | TestConnectionResponse500
]:
    """Test destination connection

     Test destination connection using credentials

    Args:
        team_id (int):
        body (TestConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestConnectionResponse | TestConnectionResponse400 | TestConnectionResponse401 | TestConnectionResponse403 | TestConnectionResponse422 | TestConnectionResponse429 | TestConnectionResponse500]
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
    body: TestConnectionRequest,
) -> (
    TestConnectionResponse
    | TestConnectionResponse400
    | TestConnectionResponse401
    | TestConnectionResponse403
    | TestConnectionResponse422
    | TestConnectionResponse429
    | TestConnectionResponse500
    | None
):
    """Test destination connection

     Test destination connection using credentials

    Args:
        team_id (int):
        body (TestConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestConnectionResponse | TestConnectionResponse400 | TestConnectionResponse401 | TestConnectionResponse403 | TestConnectionResponse422 | TestConnectionResponse429 | TestConnectionResponse500
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
    body: TestConnectionRequest,
) -> Response[
    TestConnectionResponse
    | TestConnectionResponse400
    | TestConnectionResponse401
    | TestConnectionResponse403
    | TestConnectionResponse422
    | TestConnectionResponse429
    | TestConnectionResponse500
]:
    """Test destination connection

     Test destination connection using credentials

    Args:
        team_id (int):
        body (TestConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestConnectionResponse | TestConnectionResponse400 | TestConnectionResponse401 | TestConnectionResponse403 | TestConnectionResponse422 | TestConnectionResponse429 | TestConnectionResponse500]
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
    body: TestConnectionRequest,
) -> (
    TestConnectionResponse
    | TestConnectionResponse400
    | TestConnectionResponse401
    | TestConnectionResponse403
    | TestConnectionResponse422
    | TestConnectionResponse429
    | TestConnectionResponse500
    | None
):
    """Test destination connection

     Test destination connection using credentials

    Args:
        team_id (int):
        body (TestConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestConnectionResponse | TestConnectionResponse400 | TestConnectionResponse401 | TestConnectionResponse403 | TestConnectionResponse422 | TestConnectionResponse429 | TestConnectionResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
