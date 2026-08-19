from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_source_account_list_response import DataSourceAccountListResponse
from ...models.list_data_source_login_accounts_response_401 import ListDataSourceLoginAccountsResponse401
from ...models.list_data_source_login_accounts_response_403 import ListDataSourceLoginAccountsResponse403
from ...models.list_data_source_login_accounts_response_404 import ListDataSourceLoginAccountsResponse404
from ...models.list_data_source_login_accounts_response_422 import ListDataSourceLoginAccountsResponse422
from ...models.list_data_source_login_accounts_response_429 import ListDataSourceLoginAccountsResponse429
from ...models.list_data_source_login_accounts_response_500 import ListDataSourceLoginAccountsResponse500
from ...types import UNSET, Response, Unset


def _get_kwargs(
    login_id: str,
    *,
    offset: int | Unset = 0,
    limit: int | Unset = 100,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ds/login/{login_id}/accounts".format(
            login_id=quote(str(login_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DataSourceAccountListResponse
    | ListDataSourceLoginAccountsResponse401
    | ListDataSourceLoginAccountsResponse403
    | ListDataSourceLoginAccountsResponse404
    | ListDataSourceLoginAccountsResponse422
    | ListDataSourceLoginAccountsResponse429
    | ListDataSourceLoginAccountsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = DataSourceAccountListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListDataSourceLoginAccountsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListDataSourceLoginAccountsResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ListDataSourceLoginAccountsResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ListDataSourceLoginAccountsResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ListDataSourceLoginAccountsResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ListDataSourceLoginAccountsResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DataSourceAccountListResponse
    | ListDataSourceLoginAccountsResponse401
    | ListDataSourceLoginAccountsResponse403
    | ListDataSourceLoginAccountsResponse404
    | ListDataSourceLoginAccountsResponse422
    | ListDataSourceLoginAccountsResponse429
    | ListDataSourceLoginAccountsResponse500
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
    offset: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[
    DataSourceAccountListResponse
    | ListDataSourceLoginAccountsResponse401
    | ListDataSourceLoginAccountsResponse403
    | ListDataSourceLoginAccountsResponse404
    | ListDataSourceLoginAccountsResponse422
    | ListDataSourceLoginAccountsResponse429
    | ListDataSourceLoginAccountsResponse500
]:
    """List login accounts

     List stored data source accounts for specified data source login

    Args:
        login_id (str):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSourceAccountListResponse | ListDataSourceLoginAccountsResponse401 | ListDataSourceLoginAccountsResponse403 | ListDataSourceLoginAccountsResponse404 | ListDataSourceLoginAccountsResponse422 | ListDataSourceLoginAccountsResponse429 | ListDataSourceLoginAccountsResponse500]
    """

    kwargs = _get_kwargs(
        login_id=login_id,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    login_id: str,
    *,
    client: AuthenticatedClient,
    offset: int | Unset = 0,
    limit: int | Unset = 100,
) -> (
    DataSourceAccountListResponse
    | ListDataSourceLoginAccountsResponse401
    | ListDataSourceLoginAccountsResponse403
    | ListDataSourceLoginAccountsResponse404
    | ListDataSourceLoginAccountsResponse422
    | ListDataSourceLoginAccountsResponse429
    | ListDataSourceLoginAccountsResponse500
    | None
):
    """List login accounts

     List stored data source accounts for specified data source login

    Args:
        login_id (str):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSourceAccountListResponse | ListDataSourceLoginAccountsResponse401 | ListDataSourceLoginAccountsResponse403 | ListDataSourceLoginAccountsResponse404 | ListDataSourceLoginAccountsResponse422 | ListDataSourceLoginAccountsResponse429 | ListDataSourceLoginAccountsResponse500
    """

    return sync_detailed(
        login_id=login_id,
        client=client,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    login_id: str,
    *,
    client: AuthenticatedClient,
    offset: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[
    DataSourceAccountListResponse
    | ListDataSourceLoginAccountsResponse401
    | ListDataSourceLoginAccountsResponse403
    | ListDataSourceLoginAccountsResponse404
    | ListDataSourceLoginAccountsResponse422
    | ListDataSourceLoginAccountsResponse429
    | ListDataSourceLoginAccountsResponse500
]:
    """List login accounts

     List stored data source accounts for specified data source login

    Args:
        login_id (str):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSourceAccountListResponse | ListDataSourceLoginAccountsResponse401 | ListDataSourceLoginAccountsResponse403 | ListDataSourceLoginAccountsResponse404 | ListDataSourceLoginAccountsResponse422 | ListDataSourceLoginAccountsResponse429 | ListDataSourceLoginAccountsResponse500]
    """

    kwargs = _get_kwargs(
        login_id=login_id,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    login_id: str,
    *,
    client: AuthenticatedClient,
    offset: int | Unset = 0,
    limit: int | Unset = 100,
) -> (
    DataSourceAccountListResponse
    | ListDataSourceLoginAccountsResponse401
    | ListDataSourceLoginAccountsResponse403
    | ListDataSourceLoginAccountsResponse404
    | ListDataSourceLoginAccountsResponse422
    | ListDataSourceLoginAccountsResponse429
    | ListDataSourceLoginAccountsResponse500
    | None
):
    """List login accounts

     List stored data source accounts for specified data source login

    Args:
        login_id (str):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSourceAccountListResponse | ListDataSourceLoginAccountsResponse401 | ListDataSourceLoginAccountsResponse403 | ListDataSourceLoginAccountsResponse404 | ListDataSourceLoginAccountsResponse422 | ListDataSourceLoginAccountsResponse429 | ListDataSourceLoginAccountsResponse500
    """

    return (
        await asyncio_detailed(
            login_id=login_id,
            client=client,
            offset=offset,
            limit=limit,
        )
    ).parsed
