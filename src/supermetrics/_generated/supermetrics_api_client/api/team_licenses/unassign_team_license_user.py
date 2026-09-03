from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_error import BadRequestError
from ...models.internal_server_error import InternalServerError
from ...models.not_found_error import NotFoundError
from ...models.permission_error import PermissionError_
from ...models.too_many_requests_error import TooManyRequestsError
from ...models.unauthorized_error import UnauthorizedError
from ...types import Response


def _get_kwargs(
    team_id: int,
    license_id: int,
    user_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/teams/{team_id}/licenses/{license_id}/users/{user_id}".format(
            team_id=quote(str(team_id), safe=""),
            license_id=quote(str(license_id), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | BadRequestError
    | InternalServerError
    | NotFoundError
    | PermissionError_
    | TooManyRequestsError
    | UnauthorizedError
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UnauthorizedError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = PermissionError_.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = TooManyRequestsError.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = InternalServerError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | BadRequestError
    | InternalServerError
    | NotFoundError
    | PermissionError_
    | TooManyRequestsError
    | UnauthorizedError
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    license_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | BadRequestError
    | InternalServerError
    | NotFoundError
    | PermissionError_
    | TooManyRequestsError
    | UnauthorizedError
]:
    """Unassign a user from a license

     Unassign a user from a license

    Args:
        team_id (int):
        license_id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestError | InternalServerError | NotFoundError | PermissionError_ | TooManyRequestsError | UnauthorizedError]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        license_id=license_id,
        user_id=user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    license_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | BadRequestError
    | InternalServerError
    | NotFoundError
    | PermissionError_
    | TooManyRequestsError
    | UnauthorizedError
    | None
):
    """Unassign a user from a license

     Unassign a user from a license

    Args:
        team_id (int):
        license_id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestError | InternalServerError | NotFoundError | PermissionError_ | TooManyRequestsError | UnauthorizedError
    """

    return sync_detailed(
        team_id=team_id,
        license_id=license_id,
        user_id=user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    license_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Any
    | BadRequestError
    | InternalServerError
    | NotFoundError
    | PermissionError_
    | TooManyRequestsError
    | UnauthorizedError
]:
    """Unassign a user from a license

     Unassign a user from a license

    Args:
        team_id (int):
        license_id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestError | InternalServerError | NotFoundError | PermissionError_ | TooManyRequestsError | UnauthorizedError]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        license_id=license_id,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    license_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> (
    Any
    | BadRequestError
    | InternalServerError
    | NotFoundError
    | PermissionError_
    | TooManyRequestsError
    | UnauthorizedError
    | None
):
    """Unassign a user from a license

     Unassign a user from a license

    Args:
        team_id (int):
        license_id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestError | InternalServerError | NotFoundError | PermissionError_ | TooManyRequestsError | UnauthorizedError
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            license_id=license_id,
            user_id=user_id,
            client=client,
        )
    ).parsed
