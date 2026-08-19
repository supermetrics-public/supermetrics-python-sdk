from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.fetch_transformation_response_400 import FetchTransformationResponse400
from ...models.fetch_transformation_response_401 import FetchTransformationResponse401
from ...models.fetch_transformation_response_404 import FetchTransformationResponse404
from ...models.fetch_transformation_response_429 import FetchTransformationResponse429
from ...models.fetch_transformation_response_500 import FetchTransformationResponse500
from ...models.single_transformation_output import SingleTransformationOutput
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
        "method": "get",
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
    ErrorResponse
    | FetchTransformationResponse400
    | FetchTransformationResponse401
    | FetchTransformationResponse404
    | FetchTransformationResponse429
    | FetchTransformationResponse500
    | SingleTransformationOutput
    | None
):
    if response.status_code == 200:
        response_200 = SingleTransformationOutput.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FetchTransformationResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = FetchTransformationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = FetchTransformationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = FetchTransformationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = FetchTransformationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | FetchTransformationResponse400
    | FetchTransformationResponse401
    | FetchTransformationResponse404
    | FetchTransformationResponse429
    | FetchTransformationResponse500
    | SingleTransformationOutput
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
    ErrorResponse
    | FetchTransformationResponse400
    | FetchTransformationResponse401
    | FetchTransformationResponse404
    | FetchTransformationResponse429
    | FetchTransformationResponse500
    | SingleTransformationOutput
]:
    """Fetch an existing custom field

     Fetch an existing custom field by name

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FetchTransformationResponse400 | FetchTransformationResponse401 | FetchTransformationResponse404 | FetchTransformationResponse429 | FetchTransformationResponse500 | SingleTransformationOutput]
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
    ErrorResponse
    | FetchTransformationResponse400
    | FetchTransformationResponse401
    | FetchTransformationResponse404
    | FetchTransformationResponse429
    | FetchTransformationResponse500
    | SingleTransformationOutput
    | None
):
    """Fetch an existing custom field

     Fetch an existing custom field by name

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FetchTransformationResponse400 | FetchTransformationResponse401 | FetchTransformationResponse404 | FetchTransformationResponse429 | FetchTransformationResponse500 | SingleTransformationOutput
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
    ErrorResponse
    | FetchTransformationResponse400
    | FetchTransformationResponse401
    | FetchTransformationResponse404
    | FetchTransformationResponse429
    | FetchTransformationResponse500
    | SingleTransformationOutput
]:
    """Fetch an existing custom field

     Fetch an existing custom field by name

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FetchTransformationResponse400 | FetchTransformationResponse401 | FetchTransformationResponse404 | FetchTransformationResponse429 | FetchTransformationResponse500 | SingleTransformationOutput]
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
    ErrorResponse
    | FetchTransformationResponse400
    | FetchTransformationResponse401
    | FetchTransformationResponse404
    | FetchTransformationResponse429
    | FetchTransformationResponse500
    | SingleTransformationOutput
    | None
):
    """Fetch an existing custom field

     Fetch an existing custom field by name

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FetchTransformationResponse400 | FetchTransformationResponse401 | FetchTransformationResponse404 | FetchTransformationResponse429 | FetchTransformationResponse500 | SingleTransformationOutput
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            custom_field_id=custom_field_id,
            client=client,
            sm_app_id=sm_app_id,
        )
    ).parsed
