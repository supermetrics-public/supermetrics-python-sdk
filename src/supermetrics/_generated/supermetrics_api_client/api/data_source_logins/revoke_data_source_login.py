from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.login_revoke_response import LoginRevokeResponse
from ...models.revoke_data_source_login_response_401 import RevokeDataSourceLoginResponse401
from ...models.revoke_data_source_login_response_403 import RevokeDataSourceLoginResponse403
from ...models.revoke_data_source_login_response_404 import RevokeDataSourceLoginResponse404
from ...models.revoke_data_source_login_response_422 import RevokeDataSourceLoginResponse422
from ...models.revoke_data_source_login_response_429 import RevokeDataSourceLoginResponse429
from ...models.revoke_data_source_login_response_500 import RevokeDataSourceLoginResponse500
from ...types import Response


def _get_kwargs(
    login_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/ds/login/{login_id}".format(
            login_id=quote(str(login_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    LoginRevokeResponse
    | RevokeDataSourceLoginResponse401
    | RevokeDataSourceLoginResponse403
    | RevokeDataSourceLoginResponse404
    | RevokeDataSourceLoginResponse422
    | RevokeDataSourceLoginResponse429
    | RevokeDataSourceLoginResponse500
    | None
):
    if response.status_code == 200:
        response_200 = LoginRevokeResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = RevokeDataSourceLoginResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = RevokeDataSourceLoginResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = RevokeDataSourceLoginResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = RevokeDataSourceLoginResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = RevokeDataSourceLoginResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = RevokeDataSourceLoginResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    LoginRevokeResponse
    | RevokeDataSourceLoginResponse401
    | RevokeDataSourceLoginResponse403
    | RevokeDataSourceLoginResponse404
    | RevokeDataSourceLoginResponse422
    | RevokeDataSourceLoginResponse429
    | RevokeDataSourceLoginResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    LoginRevokeResponse
    | RevokeDataSourceLoginResponse401
    | RevokeDataSourceLoginResponse403
    | RevokeDataSourceLoginResponse404
    | RevokeDataSourceLoginResponse422
    | RevokeDataSourceLoginResponse429
    | RevokeDataSourceLoginResponse500
]:
    """Revoke login

     Revoke an existing data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoginRevokeResponse | RevokeDataSourceLoginResponse401 | RevokeDataSourceLoginResponse403 | RevokeDataSourceLoginResponse404 | RevokeDataSourceLoginResponse422 | RevokeDataSourceLoginResponse429 | RevokeDataSourceLoginResponse500]
    """

    kwargs = _get_kwargs(
        login_id=login_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    LoginRevokeResponse
    | RevokeDataSourceLoginResponse401
    | RevokeDataSourceLoginResponse403
    | RevokeDataSourceLoginResponse404
    | RevokeDataSourceLoginResponse422
    | RevokeDataSourceLoginResponse429
    | RevokeDataSourceLoginResponse500
    | None
):
    """Revoke login

     Revoke an existing data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoginRevokeResponse | RevokeDataSourceLoginResponse401 | RevokeDataSourceLoginResponse403 | RevokeDataSourceLoginResponse404 | RevokeDataSourceLoginResponse422 | RevokeDataSourceLoginResponse429 | RevokeDataSourceLoginResponse500
    """

    return sync_detailed(
        login_id=login_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    LoginRevokeResponse
    | RevokeDataSourceLoginResponse401
    | RevokeDataSourceLoginResponse403
    | RevokeDataSourceLoginResponse404
    | RevokeDataSourceLoginResponse422
    | RevokeDataSourceLoginResponse429
    | RevokeDataSourceLoginResponse500
]:
    """Revoke login

     Revoke an existing data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoginRevokeResponse | RevokeDataSourceLoginResponse401 | RevokeDataSourceLoginResponse403 | RevokeDataSourceLoginResponse404 | RevokeDataSourceLoginResponse422 | RevokeDataSourceLoginResponse429 | RevokeDataSourceLoginResponse500]
    """

    kwargs = _get_kwargs(
        login_id=login_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    login_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    LoginRevokeResponse
    | RevokeDataSourceLoginResponse401
    | RevokeDataSourceLoginResponse403
    | RevokeDataSourceLoginResponse404
    | RevokeDataSourceLoginResponse422
    | RevokeDataSourceLoginResponse429
    | RevokeDataSourceLoginResponse500
    | None
):
    """Revoke login

     Revoke an existing data source login

    Args:
        login_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoginRevokeResponse | RevokeDataSourceLoginResponse401 | RevokeDataSourceLoginResponse403 | RevokeDataSourceLoginResponse404 | RevokeDataSourceLoginResponse422 | RevokeDataSourceLoginResponse429 | RevokeDataSourceLoginResponse500
    """

    return (
        await asyncio_detailed(
            login_id=login_id,
            client=client,
        )
    ).parsed
