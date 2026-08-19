from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_transformation_response_400 import CreateTransformationResponse400
from ...models.create_transformation_response_401 import CreateTransformationResponse401
from ...models.create_transformation_response_404 import CreateTransformationResponse404
from ...models.create_transformation_response_429 import CreateTransformationResponse429
from ...models.create_transformation_response_500 import CreateTransformationResponse500
from ...models.custom_field_create_request import CustomFieldCreateRequest
from ...models.error_response import ErrorResponse
from ...models.single_transformation_output import SingleTransformationOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    *,
    body: CustomFieldCreateRequest,
    sm_app_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(sm_app_id, Unset):
        headers["Sm-App-Id"] = sm_app_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/teams/{team_id}/custom-fields".format(
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
    CreateTransformationResponse400
    | CreateTransformationResponse401
    | CreateTransformationResponse404
    | CreateTransformationResponse429
    | CreateTransformationResponse500
    | ErrorResponse
    | SingleTransformationOutput
    | None
):
    if response.status_code == 201:
        response_201 = SingleTransformationOutput.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = CreateTransformationResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateTransformationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CreateTransformationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = CreateTransformationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = CreateTransformationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateTransformationResponse400
    | CreateTransformationResponse401
    | CreateTransformationResponse404
    | CreateTransformationResponse429
    | CreateTransformationResponse500
    | ErrorResponse
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
    *,
    client: AuthenticatedClient,
    body: CustomFieldCreateRequest,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    CreateTransformationResponse400
    | CreateTransformationResponse401
    | CreateTransformationResponse404
    | CreateTransformationResponse429
    | CreateTransformationResponse500
    | ErrorResponse
    | SingleTransformationOutput
]:
    """Create a new custom field

     Create a new custom field. Returns HTTP 201 Created with the created resource.

    Args:
        team_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldCreateRequest): Payload for creating a new custom field (field
            transformation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTransformationResponse400 | CreateTransformationResponse401 | CreateTransformationResponse404 | CreateTransformationResponse429 | CreateTransformationResponse500 | ErrorResponse | SingleTransformationOutput]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
        sm_app_id=sm_app_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CustomFieldCreateRequest,
    sm_app_id: str | Unset = UNSET,
) -> (
    CreateTransformationResponse400
    | CreateTransformationResponse401
    | CreateTransformationResponse404
    | CreateTransformationResponse429
    | CreateTransformationResponse500
    | ErrorResponse
    | SingleTransformationOutput
    | None
):
    """Create a new custom field

     Create a new custom field. Returns HTTP 201 Created with the created resource.

    Args:
        team_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldCreateRequest): Payload for creating a new custom field (field
            transformation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTransformationResponse400 | CreateTransformationResponse401 | CreateTransformationResponse404 | CreateTransformationResponse429 | CreateTransformationResponse500 | ErrorResponse | SingleTransformationOutput
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        body=body,
        sm_app_id=sm_app_id,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CustomFieldCreateRequest,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    CreateTransformationResponse400
    | CreateTransformationResponse401
    | CreateTransformationResponse404
    | CreateTransformationResponse429
    | CreateTransformationResponse500
    | ErrorResponse
    | SingleTransformationOutput
]:
    """Create a new custom field

     Create a new custom field. Returns HTTP 201 Created with the created resource.

    Args:
        team_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldCreateRequest): Payload for creating a new custom field (field
            transformation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTransformationResponse400 | CreateTransformationResponse401 | CreateTransformationResponse404 | CreateTransformationResponse429 | CreateTransformationResponse500 | ErrorResponse | SingleTransformationOutput]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        body=body,
        sm_app_id=sm_app_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient,
    body: CustomFieldCreateRequest,
    sm_app_id: str | Unset = UNSET,
) -> (
    CreateTransformationResponse400
    | CreateTransformationResponse401
    | CreateTransformationResponse404
    | CreateTransformationResponse429
    | CreateTransformationResponse500
    | ErrorResponse
    | SingleTransformationOutput
    | None
):
    """Create a new custom field

     Create a new custom field. Returns HTTP 201 Created with the created resource.

    Args:
        team_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldCreateRequest): Payload for creating a new custom field (field
            transformation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTransformationResponse400 | CreateTransformationResponse401 | CreateTransformationResponse404 | CreateTransformationResponse429 | CreateTransformationResponse500 | ErrorResponse | SingleTransformationOutput
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
            sm_app_id=sm_app_id,
        )
    ).parsed
