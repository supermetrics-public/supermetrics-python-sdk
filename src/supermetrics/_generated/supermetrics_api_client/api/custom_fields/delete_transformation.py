from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_transformation_response_400 import DeleteTransformationResponse400
from ...models.delete_transformation_response_401 import DeleteTransformationResponse401
from ...models.delete_transformation_response_404 import DeleteTransformationResponse404
from ...models.delete_transformation_response_429 import DeleteTransformationResponse429
from ...models.delete_transformation_response_500 import DeleteTransformationResponse500
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    custom_field_id: int,
    *,
    sm_app_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(sm_app_id, Unset):
        headers["Sm-App-Id"] = sm_app_id

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/teams/{team_id}/custom-fields/{custom_field_id}".format(
            team_id=quote(str(team_id), safe=""),
            custom_field_id=quote(str(custom_field_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | DeleteTransformationResponse400
    | DeleteTransformationResponse401
    | DeleteTransformationResponse404
    | DeleteTransformationResponse429
    | DeleteTransformationResponse500
    | ErrorResponse
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = DeleteTransformationResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = DeleteTransformationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = DeleteTransformationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = DeleteTransformationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = DeleteTransformationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | DeleteTransformationResponse400
    | DeleteTransformationResponse401
    | DeleteTransformationResponse404
    | DeleteTransformationResponse429
    | DeleteTransformationResponse500
    | ErrorResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    custom_field_id: int,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    Any
    | DeleteTransformationResponse400
    | DeleteTransformationResponse401
    | DeleteTransformationResponse404
    | DeleteTransformationResponse429
    | DeleteTransformationResponse500
    | ErrorResponse
]:
    """Remove an existing custom field

     Remove an existing custom field. Returns HTTP 204 No Content on success.

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteTransformationResponse400 | DeleteTransformationResponse401 | DeleteTransformationResponse404 | DeleteTransformationResponse429 | DeleteTransformationResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        custom_field_id=custom_field_id,
        sm_app_id=sm_app_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    custom_field_id: int,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> (
    Any
    | DeleteTransformationResponse400
    | DeleteTransformationResponse401
    | DeleteTransformationResponse404
    | DeleteTransformationResponse429
    | DeleteTransformationResponse500
    | ErrorResponse
    | None
):
    """Remove an existing custom field

     Remove an existing custom field. Returns HTTP 204 No Content on success.

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteTransformationResponse400 | DeleteTransformationResponse401 | DeleteTransformationResponse404 | DeleteTransformationResponse429 | DeleteTransformationResponse500 | ErrorResponse
    """

    return sync_detailed(
        team_id=team_id,
        custom_field_id=custom_field_id,
        client=client,
        sm_app_id=sm_app_id,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    custom_field_id: int,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    Any
    | DeleteTransformationResponse400
    | DeleteTransformationResponse401
    | DeleteTransformationResponse404
    | DeleteTransformationResponse429
    | DeleteTransformationResponse500
    | ErrorResponse
]:
    """Remove an existing custom field

     Remove an existing custom field. Returns HTTP 204 No Content on success.

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteTransformationResponse400 | DeleteTransformationResponse401 | DeleteTransformationResponse404 | DeleteTransformationResponse429 | DeleteTransformationResponse500 | ErrorResponse]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        custom_field_id=custom_field_id,
        sm_app_id=sm_app_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    custom_field_id: int,
    *,
    client: AuthenticatedClient,
    sm_app_id: str | Unset = UNSET,
) -> (
    Any
    | DeleteTransformationResponse400
    | DeleteTransformationResponse401
    | DeleteTransformationResponse404
    | DeleteTransformationResponse429
    | DeleteTransformationResponse500
    | ErrorResponse
    | None
):
    """Remove an existing custom field

     Remove an existing custom field. Returns HTTP 204 No Content on success.

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteTransformationResponse400 | DeleteTransformationResponse401 | DeleteTransformationResponse404 | DeleteTransformationResponse429 | DeleteTransformationResponse500 | ErrorResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            custom_field_id=custom_field_id,
            client=client,
            sm_app_id=sm_app_id,
        )
    ).parsed
