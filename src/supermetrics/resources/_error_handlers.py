"""Shared error-handling helpers for resource adapters.

These module-level functions centralise the repetitive error translation logic
that every resource adapter needs:

- _raise_for_response   – translates typed generated-client error responses
- _handle_http_error    – translates httpx.HTTPStatusError
- _handle_request_error – translates httpx.RequestError
"""

from typing import Any, NoReturn

import httpx

from supermetrics._generated.supermetrics_api_client.models.error_response import ErrorResponse
from supermetrics._generated.supermetrics_api_client.types import Unset
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError


def _raise_for_response(
    response: Any,
    endpoint: str,
    *,
    type_401: type,
    type_403: type,
    type_429: type,
    type_500: type,
    not_found_msg: str,
    type_400: type | None = None,
    bad_request_msg: str | None = None,
) -> NoReturn:
    """Translate a typed error response into the appropriate SDK exception.

    Checks each known error response type in priority order and raises the
    matching SDK exception.  Always raises; callers after this call are
    unreachable.

    Args:
        response: The raw response object returned by the generated client.
        endpoint: The logical API endpoint path, used to populate exception metadata.
        type_401: Generated response class that signals HTTP 401.
        type_403: Generated response class that signals HTTP 403.
        type_429: Generated response class that signals HTTP 429.
        type_500: Generated response class that signals HTTP 500.
        not_found_msg: Human-readable message used when an ErrorResponse (404) is detected.
        type_400: Generated response class that signals HTTP 400, or None if the
            endpoint does not return 400.
        bad_request_msg: Human-readable message used for 400 responses.  Falls
            back to ``"Invalid request parameters: {response}"`` when omitted.

    Raises:
        ValueError: If response is None or Unset (empty response).
        AuthenticationError: On type_401 match.
        ValidationError: On type_400 match (when type_400 is provided).
        APIError: On type_403, ErrorResponse, type_429/type_500, or unexpected type.
    """
    if response is None or isinstance(response, Unset):
        raise ValueError("API returned empty response")
    if isinstance(response, type_401):
        raise AuthenticationError("Invalid or expired API key", status_code=401, endpoint=endpoint)
    if type_400 is not None and isinstance(response, type_400):
        # Handle two different 400 response formats:
        # 1. New format with meta and error attributes (e.g., CreateBackfillResponse400)
        # 2. RFC 9457 format with type_, title, status, detail (e.g., UpdateBackfillStatusResponse400)
        if hasattr(response, 'error'):
            error_msg = (
                response.error.message
                if (
                    response.error
                    and not isinstance(response.error, Unset)
                    and response.error.message
                    and not isinstance(response.error.message, Unset)
                )
                else "Invalid request parameters"
            )
        elif hasattr(response, 'detail'):
            # RFC 9457 format
            error_msg = (
                response.detail
                if response.detail and not isinstance(response.detail, Unset)
                else (bad_request_msg if bad_request_msg else "Invalid request parameters")
            )
        else:
            error_msg = bad_request_msg if bad_request_msg else "Invalid request parameters"

        raise ValidationError(
            error_msg,
            status_code=400,
            endpoint=endpoint,
            response_body=str(response),
        )
    if isinstance(response, type_403):
        raise APIError(
            "Forbidden - insufficient permissions",
            status_code=403,
            endpoint=endpoint,
            response_body=str(response),
        )
    if isinstance(response, ErrorResponse):
        raise APIError(not_found_msg, status_code=404, endpoint=endpoint, response_body=str(response))
    if isinstance(response, (type_429, type_500)):
        status = 429 if isinstance(response, type_429) else 500
        raise APIError(f"API error: {response}", status_code=status, endpoint=endpoint, response_body=str(response))
    raise APIError(f"Unexpected response type: {type(response).__name__}", status_code=500, endpoint=endpoint)


def _handle_http_error(
    e: httpx.HTTPStatusError,
    *,
    context_400: str | None = None,
    context_404: str | None = None,
) -> NoReturn:
    """Translate an httpx HTTP status error into the appropriate SDK exception.

    Args:
        e: The httpx exception to translate.
        context_400: Short description of the operation, prepended to the
            response body in the ValidationError message (e.g. ``"Invalid
            request parameters"``).  When None, 400 responses fall through to
            the generic APIError handler.
        context_404: Short description of the missing resource, prepended to
            the response body in the APIError message (e.g. ``"Backfill not
            found"``).  When None, 404 responses fall through to the generic
            APIError handler.

    Raises:
        AuthenticationError: On HTTP 401.
        ValidationError: On HTTP 400 when context_400 is provided.
        APIError: On HTTP 404 (when context_404 is provided), HTTP 5xx, or any
            other status code.
    """
    url = str(e.request.url)
    status = e.response.status_code
    text = e.response.text
    if status == 401:
        raise AuthenticationError("Invalid or expired API key", status_code=401, endpoint=url, response_body=text) from e
    if status == 400 and context_400 is not None:
        raise ValidationError(f"{context_400}: {text}", status_code=400, endpoint=url, response_body=text) from e
    if status == 404 and context_404 is not None:
        raise APIError(f"{context_404}: {text}", status_code=404, endpoint=url, response_body=text) from e
    if status >= 500:
        raise APIError(f"Supermetrics API error: {text}", status_code=status, endpoint=url, response_body=text) from e
    raise APIError(f"API error ({status}): {text}", status_code=status, endpoint=url, response_body=text) from e


def _handle_request_error(e: httpx.RequestError) -> NoReturn:
    """Translate an httpx request error into a NetworkError.

    Args:
        e: The httpx exception to translate.

    Raises:
        NetworkError: Always.
    """
    raise NetworkError(
        f"Network error: {str(e)}",
        endpoint=str(e.request.url) if e.request else None,
    ) from e
