from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_field_update_request import CustomFieldUpdateRequest
from ...models.error_response import ErrorResponse
from ...models.single_transformation_output import SingleTransformationOutput
from ...models.update_transformation_response_400 import UpdateTransformationResponse400
from ...models.update_transformation_response_401 import UpdateTransformationResponse401
from ...models.update_transformation_response_404 import UpdateTransformationResponse404
from ...models.update_transformation_response_429 import UpdateTransformationResponse429
from ...models.update_transformation_response_500 import UpdateTransformationResponse500
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    custom_field_id: int,
    *,
    body: CustomFieldUpdateRequest,
    sm_app_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(sm_app_id, Unset):
        headers["Sm-App-Id"] = sm_app_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/teams/{team_id}/custom-fields/{custom_field_id}".format(
            team_id=quote(str(team_id), safe=""),
            custom_field_id=quote(str(custom_field_id), safe=""),
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
    | SingleTransformationOutput
    | UpdateTransformationResponse400
    | UpdateTransformationResponse401
    | UpdateTransformationResponse404
    | UpdateTransformationResponse429
    | UpdateTransformationResponse500
    | None
):
    if response.status_code == 200:
        response_200 = SingleTransformationOutput.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UpdateTransformationResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UpdateTransformationResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateTransformationResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = UpdateTransformationResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UpdateTransformationResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse
    | SingleTransformationOutput
    | UpdateTransformationResponse400
    | UpdateTransformationResponse401
    | UpdateTransformationResponse404
    | UpdateTransformationResponse429
    | UpdateTransformationResponse500
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
    body: CustomFieldUpdateRequest,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    ErrorResponse
    | SingleTransformationOutput
    | UpdateTransformationResponse400
    | UpdateTransformationResponse401
    | UpdateTransformationResponse404
    | UpdateTransformationResponse429
    | UpdateTransformationResponse500
]:
    """Update an existing custom field

     Update an existing custom field

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldUpdateRequest): Payload for updating an existing custom field. The
            `field_type` cannot be changed and is therefore omitted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SingleTransformationOutput | UpdateTransformationResponse400 | UpdateTransformationResponse401 | UpdateTransformationResponse404 | UpdateTransformationResponse429 | UpdateTransformationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        custom_field_id=custom_field_id,
        body=body,
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
    body: CustomFieldUpdateRequest,
    sm_app_id: str | Unset = UNSET,
) -> (
    ErrorResponse
    | SingleTransformationOutput
    | UpdateTransformationResponse400
    | UpdateTransformationResponse401
    | UpdateTransformationResponse404
    | UpdateTransformationResponse429
    | UpdateTransformationResponse500
    | None
):
    """Update an existing custom field

     Update an existing custom field

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldUpdateRequest): Payload for updating an existing custom field. The
            `field_type` cannot be changed and is therefore omitted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SingleTransformationOutput | UpdateTransformationResponse400 | UpdateTransformationResponse401 | UpdateTransformationResponse404 | UpdateTransformationResponse429 | UpdateTransformationResponse500
    """

    return sync_detailed(
        team_id=team_id,
        custom_field_id=custom_field_id,
        client=client,
        body=body,
        sm_app_id=sm_app_id,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    custom_field_id: int,
    *,
    client: AuthenticatedClient,
    body: CustomFieldUpdateRequest,
    sm_app_id: str | Unset = UNSET,
) -> Response[
    ErrorResponse
    | SingleTransformationOutput
    | UpdateTransformationResponse400
    | UpdateTransformationResponse401
    | UpdateTransformationResponse404
    | UpdateTransformationResponse429
    | UpdateTransformationResponse500
]:
    """Update an existing custom field

     Update an existing custom field

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldUpdateRequest): Payload for updating an existing custom field. The
            `field_type` cannot be changed and is therefore omitted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SingleTransformationOutput | UpdateTransformationResponse400 | UpdateTransformationResponse401 | UpdateTransformationResponse404 | UpdateTransformationResponse429 | UpdateTransformationResponse500]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        custom_field_id=custom_field_id,
        body=body,
        sm_app_id=sm_app_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    custom_field_id: int,
    *,
    client: AuthenticatedClient,
    body: CustomFieldUpdateRequest,
    sm_app_id: str | Unset = UNSET,
) -> (
    ErrorResponse
    | SingleTransformationOutput
    | UpdateTransformationResponse400
    | UpdateTransformationResponse401
    | UpdateTransformationResponse404
    | UpdateTransformationResponse429
    | UpdateTransformationResponse500
    | None
):
    """Update an existing custom field

     Update an existing custom field

    Args:
        team_id (int):
        custom_field_id (int):
        sm_app_id (str | Unset):
        body (CustomFieldUpdateRequest): Payload for updating an existing custom field. The
            `field_type` cannot be changed and is therefore omitted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SingleTransformationOutput | UpdateTransformationResponse400 | UpdateTransformationResponse401 | UpdateTransformationResponse404 | UpdateTransformationResponse429 | UpdateTransformationResponse500
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            custom_field_id=custom_field_id,
            client=client,
            body=body,
            sm_app_id=sm_app_id,
        )
    ).parsed
