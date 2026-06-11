"""Shared error-handling helpers for resource adapters.

These module-level functions centralise the repetitive error translation logic
that every resource adapter needs:

- _raise_for_status     – translates a non-success HTTP status code
- _handle_http_error    – translates httpx.HTTPStatusError
- _handle_request_error – translates httpx.RequestError
- api_error_handler     – context manager wrapping all of the above
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import NoReturn

import httpx

from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError


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
        raise AuthenticationError(
            "Invalid or expired API key", status_code=401, endpoint=url, response_body=text
        ) from e
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


def _raise_for_status(
    status_code: int,
    parsed: object,
    endpoint: str,
    *,
    not_found_msg: str = "Resource not found",
    bad_request_msg: str | None = None,
) -> NoReturn:
    """Translate a non-success HTTP status code into the appropriate SDK exception."""
    error_body = str(parsed) if parsed is not None else ""
    if status_code == 401:
        raise AuthenticationError("Invalid or expired API key", status_code=401, endpoint=endpoint)
    if status_code == 400:
        msg = bad_request_msg if bad_request_msg else (error_body or "Invalid request parameters")
        raise ValidationError(msg, status_code=400, endpoint=endpoint, response_body=error_body)
    if status_code == 422:
        raise ValidationError(
            error_body or "Invalid request parameters", status_code=422, endpoint=endpoint, response_body=error_body
        )
    if status_code == 403:
        raise APIError(
            error_body or "Forbidden - insufficient permissions",
            status_code=403,
            endpoint=endpoint,
            response_body=error_body,
        )
    if status_code == 404:
        raise APIError(not_found_msg, status_code=404, endpoint=endpoint, response_body=error_body)
    if status_code == 429:
        raise APIError(
            f"Rate limit exceeded: {error_body}" if error_body else "Rate limit exceeded",
            status_code=429,
            endpoint=endpoint,
            response_body=error_body,
        )
    if status_code >= 500:
        raise APIError(f"API error: {error_body}", status_code=status_code, endpoint=endpoint, response_body=error_body)
    raise APIError(
        f"API error ({status_code}): {error_body}", status_code=status_code, endpoint=endpoint, response_body=error_body
    )


def _raise_for_error_response(response: object, endpoint: str) -> NoReturn:
    """Translate a generated ErrorResponse model into the appropriate SDK exception."""
    code = ""
    message = ""

    error = getattr(response, "error", None)
    if error is not None and not isinstance(error, str):
        code = getattr(error, "code", "") or ""
        message = getattr(error, "message", "") or ""
        description = getattr(error, "description", "") or ""
        if description and description != message and description != code:
            message = f"{message}: {description}"

    error_body = message or str(response)

    if code == "UNAUTHORIZED" or code == "401":
        raise AuthenticationError("Invalid or expired API key", status_code=401, endpoint=endpoint)
    if code in ("BAD_REQUEST", "VALIDATION_ERROR"):
        raise ValidationError(error_body, status_code=400, endpoint=endpoint, response_body=error_body)
    if code in ("FORBIDDEN", "ACCESS_DENIED", "PERMISSION_ERROR"):
        raise APIError(error_body, status_code=403, endpoint=endpoint, response_body=error_body)
    if code in ("NOT_FOUND", "CONNECTOR_NOT_FOUND", "SECRET_NOT_FOUND", "LOG_NOT_FOUND"):
        raise APIError(error_body, status_code=404, endpoint=endpoint, response_body=error_body)
    if code == "CONFLICT_ERROR":
        raise APIError(error_body, status_code=409, endpoint=endpoint, response_body=error_body)
    if code == "TOO_MANY_REQUESTS":
        raise APIError(error_body, status_code=429, endpoint=endpoint, response_body=error_body)
    if code in ("INTERNAL_SERVER_ERROR", "SERVICE_UNAVAILABLE"):
        raise APIError(error_body, status_code=500, endpoint=endpoint, response_body=error_body)
    if code == "UNPROCESSABLE_ENTITY":
        raise ValidationError(error_body, status_code=422, endpoint=endpoint, response_body=error_body)
    raise APIError(f"API error: {error_body}", status_code=0, endpoint=endpoint, response_body=error_body)


@contextmanager
def api_error_handler(
    endpoint: str,
    *,
    context_400: str | None = None,
    context_404: str | None = None,
) -> Generator[None, None, None]:
    """Context manager that translates low-level exceptions into SDK exceptions."""
    try:
        yield
    except (AuthenticationError, ValidationError, APIError):
        raise
    except (ValueError, TypeError, KeyError) as e:
        raise APIError(str(e), status_code=0, endpoint=endpoint) from e
    except httpx.HTTPStatusError as e:
        _handle_http_error(e, context_400=context_400, context_404=context_404)
    except httpx.RequestError as e:
        _handle_request_error(e)
