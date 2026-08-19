from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.transfer_configuration_request import TransferConfigurationRequest
from ...models.validate_transfer_response_401 import ValidateTransferResponse401
from ...models.validate_transfer_response_403 import ValidateTransferResponse403
from ...models.validate_transfer_response_429 import ValidateTransferResponse429
from ...models.validate_transfer_response_500 import ValidateTransferResponse500
from ...models.validation_errors_response import ValidationErrorsResponse
from ...types import Response


def _get_kwargs(
    team_id: int,
    *,
    body: TransferConfigurationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/teams/{team_id}/transfers/validations".format(
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
    ValidateTransferResponse401
    | ValidateTransferResponse403
    | ValidateTransferResponse429
    | ValidateTransferResponse500
    | ValidationErrorsResponse
    | None
):
    if response.status_code == 200:
        response_200 = ValidationErrorsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ValidateTransferResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ValidateTransferResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = ValidateTransferResponse429.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ValidateTransferResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ValidateTransferResponse401
    | ValidateTransferResponse403
    | ValidateTransferResponse429
    | ValidateTransferResponse500
    | ValidationErrorsResponse
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
    body: TransferConfigurationRequest,
) -> Response[
    ValidateTransferResponse401
    | ValidateTransferResponse403
    | ValidateTransferResponse429
    | ValidateTransferResponse500
    | ValidationErrorsResponse
]:
    """Validate transfer configuration

     Validates a configuration for a new Hub transfer.

    **Returns:** List of validation errors (empty if valid).

    **Important Notes:**
    - Use this endpoint before creating a transfer to check configuration validity
    - Returns field-level validation errors

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValidateTransferResponse401 | ValidateTransferResponse403 | ValidateTransferResponse429 | ValidateTransferResponse500 | ValidationErrorsResponse]
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
    body: TransferConfigurationRequest,
) -> (
    ValidateTransferResponse401
    | ValidateTransferResponse403
    | ValidateTransferResponse429
    | ValidateTransferResponse500
    | ValidationErrorsResponse
    | None
):
    """Validate transfer configuration

     Validates a configuration for a new Hub transfer.

    **Returns:** List of validation errors (empty if valid).

    **Important Notes:**
    - Use this endpoint before creating a transfer to check configuration validity
    - Returns field-level validation errors

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ValidateTransferResponse401 | ValidateTransferResponse403 | ValidateTransferResponse429 | ValidateTransferResponse500 | ValidationErrorsResponse
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
    body: TransferConfigurationRequest,
) -> Response[
    ValidateTransferResponse401
    | ValidateTransferResponse403
    | ValidateTransferResponse429
    | ValidateTransferResponse500
    | ValidationErrorsResponse
]:
    """Validate transfer configuration

     Validates a configuration for a new Hub transfer.

    **Returns:** List of validation errors (empty if valid).

    **Important Notes:**
    - Use this endpoint before creating a transfer to check configuration validity
    - Returns field-level validation errors

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValidateTransferResponse401 | ValidateTransferResponse403 | ValidateTransferResponse429 | ValidateTransferResponse500 | ValidationErrorsResponse]
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
    body: TransferConfigurationRequest,
) -> (
    ValidateTransferResponse401
    | ValidateTransferResponse403
    | ValidateTransferResponse429
    | ValidateTransferResponse500
    | ValidationErrorsResponse
    | None
):
    """Validate transfer configuration

     Validates a configuration for a new Hub transfer.

    **Returns:** List of validation errors (empty if valid).

    **Important Notes:**
    - Use this endpoint before creating a transfer to check configuration validity
    - Returns field-level validation errors

    Args:
        team_id (int):
        body (TransferConfigurationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ValidateTransferResponse401 | ValidateTransferResponse403 | ValidateTransferResponse429 | ValidateTransferResponse500 | ValidationErrorsResponse
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            body=body,
        )
    ).parsed
