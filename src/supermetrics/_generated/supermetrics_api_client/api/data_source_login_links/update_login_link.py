from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.login_link_response import LoginLinkResponse
from ...models.update_login_link_body import UpdateLoginLinkBody
from ...models.update_login_link_response_400 import UpdateLoginLinkResponse400
from ...models.update_login_link_response_401 import UpdateLoginLinkResponse401
from ...models.update_login_link_response_404 import UpdateLoginLinkResponse404
from ...models.update_login_link_response_422 import UpdateLoginLinkResponse422
from ...models.update_login_link_response_429 import UpdateLoginLinkResponse429
from ...models.update_login_link_response_500 import UpdateLoginLinkResponse500
from ...types import Response


def _get_kwargs(
    link_id: str,
    *,
    body: UpdateLoginLinkBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/ds/login/link/{link_id}".format(
            link_id=quote(str(link_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse
    | LoginLinkResponse
    | UpdateLoginLinkResponse400
    | UpdateLoginLinkResponse401
    | UpdateLoginLinkResponse404
    | UpdateLoginLinkResponse422
    | UpdateLoginLinkResponse429
    | UpdateLoginLinkResponse500
    | None
):
    if response.status_code == 200:
        response_200 = LoginLinkResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateLoginLinkResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateLoginLinkResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateLoginLinkResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = UpdateLoginLinkResponse422.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UpdateLoginLinkResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateLoginLinkResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | LoginLinkResponse
    | UpdateLoginLinkResponse400
    | UpdateLoginLinkResponse401
    | UpdateLoginLinkResponse404
    | UpdateLoginLinkResponse422
    | UpdateLoginLinkResponse429
    | UpdateLoginLinkResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    link_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateLoginLinkBody,
) -> Response[
    ErrorResponse
    | LoginLinkResponse
    | UpdateLoginLinkResponse400
    | UpdateLoginLinkResponse401
    | UpdateLoginLinkResponse404
    | UpdateLoginLinkResponse422
    | UpdateLoginLinkResponse429
    | UpdateLoginLinkResponse500
]:
    """Update login link

     Change given properties for specified data source login link

    Args:
        link_id (str):
        body (UpdateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LoginLinkResponse | UpdateLoginLinkResponse400 | UpdateLoginLinkResponse401 | UpdateLoginLinkResponse404 | UpdateLoginLinkResponse422 | UpdateLoginLinkResponse429 | UpdateLoginLinkResponse500]
    """

    kwargs = _get_kwargs(
        link_id=link_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    link_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateLoginLinkBody,
) -> (
    ErrorResponse
    | LoginLinkResponse
    | UpdateLoginLinkResponse400
    | UpdateLoginLinkResponse401
    | UpdateLoginLinkResponse404
    | UpdateLoginLinkResponse422
    | UpdateLoginLinkResponse429
    | UpdateLoginLinkResponse500
    | None
):
    """Update login link

     Change given properties for specified data source login link

    Args:
        link_id (str):
        body (UpdateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LoginLinkResponse | UpdateLoginLinkResponse400 | UpdateLoginLinkResponse401 | UpdateLoginLinkResponse404 | UpdateLoginLinkResponse422 | UpdateLoginLinkResponse429 | UpdateLoginLinkResponse500
    """

    return sync_detailed(
        link_id=link_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    link_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateLoginLinkBody,
) -> Response[
    ErrorResponse
    | LoginLinkResponse
    | UpdateLoginLinkResponse400
    | UpdateLoginLinkResponse401
    | UpdateLoginLinkResponse404
    | UpdateLoginLinkResponse422
    | UpdateLoginLinkResponse429
    | UpdateLoginLinkResponse500
]:
    """Update login link

     Change given properties for specified data source login link

    Args:
        link_id (str):
        body (UpdateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LoginLinkResponse | UpdateLoginLinkResponse400 | UpdateLoginLinkResponse401 | UpdateLoginLinkResponse404 | UpdateLoginLinkResponse422 | UpdateLoginLinkResponse429 | UpdateLoginLinkResponse500]
    """

    kwargs = _get_kwargs(
        link_id=link_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    link_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateLoginLinkBody,
) -> (
    ErrorResponse
    | LoginLinkResponse
    | UpdateLoginLinkResponse400
    | UpdateLoginLinkResponse401
    | UpdateLoginLinkResponse404
    | UpdateLoginLinkResponse422
    | UpdateLoginLinkResponse429
    | UpdateLoginLinkResponse500
    | None
):
    """Update login link

     Change given properties for specified data source login link

    Args:
        link_id (str):
        body (UpdateLoginLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LoginLinkResponse | UpdateLoginLinkResponse400 | UpdateLoginLinkResponse401 | UpdateLoginLinkResponse404 | UpdateLoginLinkResponse422 | UpdateLoginLinkResponse429 | UpdateLoginLinkResponse500
    """

    return (
        await asyncio_detailed(
            link_id=link_id,
            client=client,
            body=body,
        )
    ).parsed
