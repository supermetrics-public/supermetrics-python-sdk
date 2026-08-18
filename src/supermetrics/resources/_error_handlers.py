"""Shared error-handling helpers for resource adapters.

These module-level functions centralise the repetitive error translation logic
that every resource adapter needs:

- _raise_for_status       – translates a non-success HTTP status code
- _raise_for_error_response – translates a generated ErrorResponse model
- _handle_http_error      – translates httpx.HTTPStatusError
- _handle_request_error   – translates httpx.RequestError
- api_error_handler       – context manager wrapping all of the above

Every translated error preserves the full transport context (status code,
response headers, raw body, upstream error code and details) so that callers can
implement retries, token refresh, and structured logging.
"""

from __future__ import annotations

import json
import re
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from typing import Any, NoReturn

import httpx

from supermetrics._transport import current_last_response, reset_last_response
from supermetrics.exceptions import (
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

#: Matches a bearer credential embedded in free-form text, so it can be redacted.
#: Low-level transport errors quote the offending header verbatim - for example h11's
#: ``Illegal header value b'Bearer otok_...'`` - and callers routinely log the message.
_BEARER_IN_TEXT = re.compile('(?i)(bearer[\\s\\\\]+)(.*?)(?=[\'"]\\s*$|[\'"][,)\\]]|$)')


def _redact_credentials(text: str) -> str:
    """Replace any bearer credential embedded in ``text`` with a placeholder.

    Args:
        text: Arbitrary error text that may quote a request header.

    Returns:
        The text with credential values replaced by ``[REDACTED]``.
    """
    return _BEARER_IN_TEXT.sub(lambda match: f"{match.group(1)}[REDACTED]", text)


#: Upstream error codes that always mean "the credential is not usable".
_AUTH_ERROR_CODES = frozenset({"UNAUTHORIZED", "401", "ACCESS_TOKEN_INVALID", "ACCESS_TOKEN_EXPIRED", "INVALID_TOKEN"})

#: Prefix marking upstream OAuth failures, e.g. ``OAUTH_TOKEN_EXPIRED``.
_OAUTH_ERROR_PREFIX = "OAUTH_"


def _status_to_exception(status_code: int) -> type[SupermetricsAPIError]:
    """Map an HTTP status code to the matching SDK exception class.

    Args:
        status_code: The HTTP status code of the response.

    Returns:
        The exception class to raise for that status.
    """
    if status_code == 401:
        return SupermetricsAuthError
    if status_code == 403:
        return SupermetricsForbiddenError
    if status_code == 404:
        return SupermetricsNotFoundError
    if status_code in (400, 422):
        return SupermetricsValidationError
    if status_code == 429:
        return SupermetricsRateLimitError
    if status_code >= 500:
        return SupermetricsServerError
    return SupermetricsAPIError


def _extract_error_fields(parsed: object) -> tuple[str | None, str, dict[str, Any] | None]:
    """Pull the upstream error code, message and details out of a parsed payload.

    Handles both the generated ``ErrorResponse``-style models (an ``error``
    object carrying ``code``/``message``/``description``) and plain dictionaries.

    Args:
        parsed: The parsed response body, or ``None``.

    Returns:
        A ``(error_code, error_message, details)`` triple. ``error_message`` is
        an empty string when nothing usable was found.
    """
    if parsed is None:
        return None, "", None

    error = parsed.get("error") if isinstance(parsed, dict) else getattr(parsed, "error", None)
    if error is None or isinstance(error, str):
        return None, "", None

    def _get(name: str) -> str:
        value = error.get(name) if isinstance(error, dict) else getattr(error, name, None)
        return value if isinstance(value, str) else ""

    code = _get("code") or None
    message = _get("message")
    description = _get("description")
    if description and description != message and description != code:
        message = f"{message}: {description}" if message else description

    details: dict[str, Any] | None = None
    raw_details = error.get("details") if isinstance(error, dict) else getattr(error, "details", None)
    if isinstance(raw_details, dict):
        details = raw_details

    return code, message, details


def _headers_of(headers: Mapping[str, str] | None) -> httpx.Headers | None:
    """Normalise a header mapping into ``httpx.Headers``.

    When no headers are supplied, the transport metadata recorded for the most
    recent response in this context is used instead. Several resource adapters
    call the generated *parsed-only* endpoint wrappers, which hand back a model
    rather than a transport response and therefore cannot pass headers
    explicitly; without this fallback those errors would lose ``Retry-After``,
    ``X-Request-Id``, and the rest.

    Args:
        headers: Headers in any mapping form, or ``None``. The generated client
            types its response headers as a plain ``MutableMapping``.

    Returns:
        ``httpx.Headers``, or ``None`` when nothing is available.
    """
    if headers is None:
        record = current_last_response.get()
        return record.headers if record is not None else None
    return headers if isinstance(headers, httpx.Headers) else httpx.Headers(headers)


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
            response body in the validation error message.
        context_404: Short description of the missing resource, prepended to the
            response body in the not-found error message.

    Raises:
        SupermetricsAPIError: Always, as the subclass matching the status code.
    """
    url = str(e.request.url)
    status = e.response.status_code
    text = e.response.text
    headers = e.response.headers

    if status == 401:
        message = "Invalid or expired API key"
    elif status == 400 and context_400 is not None:
        message = f"{context_400}: {text}"
    elif status == 404 and context_404 is not None:
        message = f"{context_404}: {text}"
    elif status >= 500:
        message = f"Supermetrics API error: {text}"
    else:
        message = f"API error ({status}): {text}"

    raise _status_to_exception(status)(
        message,
        status_code=status,
        endpoint=url,
        response_body=text,
        headers=headers,
        raw_response=e.response,
    ) from e


def _raw_response_of(raw_response: httpx.Response | None) -> httpx.Response | None:
    """Resolve the ``httpx.Response`` to attach to an error.

    Resource adapters work with the generated ``Response`` wrapper, or with a
    parsed model, and so cannot hand over the underlying ``httpx.Response``. It is
    taken from the transport record for the current call instead.

    Args:
        raw_response: An explicitly supplied response, if the caller had one.

    Returns:
        The response to attach, or ``None`` when none was recorded.
    """
    if raw_response is not None:
        return raw_response
    record = current_last_response.get()
    return record.response if record is not None else None


def _handle_request_error(e: httpx.RequestError) -> NoReturn:
    """Translate an httpx request error into a NetworkError.

    Args:
        e: The httpx exception to translate.

    Raises:
        NetworkError: Always.
    """
    # httpx.RequestError.request raises RuntimeError when no request was bound to the
    # exception, which happens for failures raised before or outside the send pipeline.
    # Reading it unguarded would mask the network failure behind an unrelated RuntimeError.
    try:
        endpoint: str | None = str(e.request.url)
    except RuntimeError:
        endpoint = None

    # Transport-layer errors can quote the outgoing headers, so redact the credential
    # before it reaches a message that callers will log.
    raise NetworkError(f"Network error: {_redact_credentials(str(e))}", endpoint=endpoint) from e


def _raise_for_status(
    status_code: int,
    parsed: object,
    endpoint: str,
    *,
    not_found_msg: str = "Resource not found",
    bad_request_msg: str | None = None,
    headers: Mapping[str, str] | None = None,
    raw_body: bytes | str | None = None,
) -> NoReturn:
    """Translate a non-success HTTP status code into the appropriate SDK exception.

    Args:
        status_code: The HTTP status code of the response.
        parsed: The parsed response payload, used to extract the upstream error
            code, message and details.
        endpoint: The endpoint that was called, for error context.
        not_found_msg: Message to use for HTTP 404 responses.
        bad_request_msg: Message to use for HTTP 400 responses, overriding the
            response body.
        headers: Response headers, preserved on the raised exception so callers
            can read ``Retry-After``, ``X-Request-Id`` and friends.
        raw_body: Raw response body, preserved on the raised exception.

    Raises:
        SupermetricsAPIError: Always, as the subclass matching the status code.
    """
    error_code, error_message, details = _extract_error_fields(parsed)
    body_text = raw_body.decode("utf-8", "replace") if isinstance(raw_body, bytes) else raw_body

    if error_code is None and body_text:
        # The generated parser returns None for any status it does not document, so the
        # upstream code would otherwise be lost for exactly the responses a caller most
        # needs to classify. Recover it from the raw body when that body is JSON.
        try:
            decoded = json.loads(body_text)
        except ValueError:
            decoded = None
        if isinstance(decoded, dict):
            error_code, decoded_message, decoded_details = _extract_error_fields(decoded)
            error_message = error_message or decoded_message
            details = details or decoded_details

    error_body = error_message or body_text or (str(parsed) if parsed is not None else "")

    if status_code == 401:
        message = "Invalid or expired API key"
    elif status_code == 400:
        message = bad_request_msg or error_body or "Invalid request parameters"
    elif status_code == 422:
        message = error_body or "Invalid request parameters"
    elif status_code == 403:
        message = error_body or "Forbidden - insufficient permissions"
    elif status_code == 404:
        message = not_found_msg
    elif status_code == 429:
        message = f"Rate limit exceeded: {error_body}" if error_body else "Rate limit exceeded"
    elif status_code >= 500:
        message = f"API error: {error_body}"
    else:
        message = f"API error ({status_code}): {error_body}"

    raise _status_to_exception(status_code)(
        message,
        status_code=status_code,
        endpoint=endpoint,
        response_body=error_body,
        headers=_headers_of(headers),
        error_code=error_code,
        details=details,
        raw_response=_raw_response_of(None),
    )


def _raise_for_error_response(
    response: object,
    endpoint: str,
    *,
    headers: Mapping[str, str] | None = None,
) -> NoReturn:
    """Translate a generated ErrorResponse model into the appropriate SDK exception.

    Args:
        response: The parsed error payload.
        endpoint: The endpoint that was called, for error context.
        headers: Response headers, preserved on the raised exception.

    Raises:
        SupermetricsAPIError: Always, as the subclass matching the upstream code.
    """
    code, message, details = _extract_error_fields(response)
    error_body = message or str(response)
    normalised = (code or "").upper()

    status_code = 0
    if normalised in _AUTH_ERROR_CODES or normalised.startswith(_OAUTH_ERROR_PREFIX):
        status_code = 401
        error_body = "Invalid or expired API key" if normalised in ("UNAUTHORIZED", "401") else error_body
    elif normalised in ("BAD_REQUEST", "VALIDATION_ERROR"):
        status_code = 400
    elif normalised in ("FORBIDDEN", "ACCESS_DENIED", "PERMISSION_ERROR"):
        status_code = 403
    elif normalised in ("NOT_FOUND", "CONNECTOR_NOT_FOUND", "SECRET_NOT_FOUND", "LOG_NOT_FOUND"):
        status_code = 404
    elif normalised == "CONFLICT_ERROR":
        status_code = 409
    elif normalised == "TOO_MANY_REQUESTS":
        status_code = 429
    elif normalised in ("INTERNAL_SERVER_ERROR", "SERVICE_UNAVAILABLE"):
        status_code = 500
    elif normalised == "UNPROCESSABLE_ENTITY":
        status_code = 422

    if status_code == 0:
        raise SupermetricsAPIError(
            f"API error: {error_body}",
            status_code=0,
            endpoint=endpoint,
            response_body=error_body,
            headers=_headers_of(headers),
            error_code=code,
            details=details,
            raw_response=_raw_response_of(None),
        )

    raise _status_to_exception(status_code)(
        error_body,
        status_code=status_code,
        endpoint=endpoint,
        response_body=error_body,
        headers=_headers_of(headers),
        error_code=code,
        details=details,
        raw_response=_raw_response_of(None),
    )


def _try_classify_from_record(
    endpoint: str,
    *,
    not_found_msg: str,
    bad_request_msg: str | None,
) -> None:
    """Raise a properly classified error if the transport saw a failing response.

    Two situations reach here, and both are routine in production:

    1. A response body did not match the schema the generated models expect, so
       parsing raised ``KeyError``/``ValueError`` - a gateway returning HTML for a
       502, or an auth service returning a bare OAuth error object.
    2. The response carried a status the OpenAPI document does not describe for
       that operation, so the generated parser returned ``None`` and the adapter
       reported an unclassified error.

    In both cases the real status code is known, because the transport recorded
    it. Without this, a 401 would surface with no status code at all and a caller
    could never tell that refreshing its token would fix the request.

    Args:
        endpoint: The endpoint being called, for error context.
        not_found_msg: Message to use if the response turns out to be a 404.
        bad_request_msg: Message to use if the response turns out to be a 400.

    Raises:
        SupermetricsAPIError: The subclass matching the recorded status code. If
            no failing response was recorded, this returns normally instead.
    """
    record = current_last_response.get()
    if record is None or 200 <= record.status_code < 300:
        return

    # Recover the upstream error code from the raw body when it is JSON, so that
    # e.g. a 401 still reports ACCESS_TOKEN_INVALID and the caller can refresh.
    payload: object = None
    try:
        decoded = json.loads(record.content)
    except (ValueError, UnicodeDecodeError):
        decoded = None
    if isinstance(decoded, dict):
        payload = decoded

    _raise_for_status(
        record.status_code,
        payload,
        endpoint,
        not_found_msg=not_found_msg,
        bad_request_msg=bad_request_msg,
        headers=record.headers,
        raw_body=record.content,
    )


def _raise_if_failed(endpoint: str, *, not_found_msg: str = "Resource not found") -> None:
    """Raise if the transport recorded a failing response for the current call.

    Some generated endpoints return ``None`` from their parser both for a genuine
    ``204 No Content`` and for any status the OpenAPI document does not describe.
    An adapter that treats ``None`` as success would therefore report a 502 from a
    gateway as a completed delete. Call this before returning on such a path.

    Args:
        endpoint: The endpoint being called, for error context.
        not_found_msg: Message to use if the recorded response turns out to be a 404.

    Raises:
        SupermetricsAPIError: The subclass matching the recorded status, when the
            transport observed a non-2xx response.
    """
    _try_classify_from_record(endpoint, not_found_msg=not_found_msg, bad_request_msg=None)


def _raise_unexpected_response(
    response: object, endpoint: str, *, not_found_msg: str = "Resource not found"
) -> NoReturn:
    """Report a response the adapter could not interpret.

    The generated parsers return ``None`` for any status the OpenAPI document does
    not describe for that operation, which is how a 404 or a gateway 502 reaches an
    adapter with no model attached. Before giving up, classify by the status the
    transport actually recorded, so the caller still learns whether the request was
    unauthorized, throttled, or simply missing.

    Args:
        response: Whatever the generated parser returned, used for the fallback message.
        endpoint: The endpoint being called, for error context.
        not_found_msg: Message to use if the recorded response turns out to be a 404.

    Raises:
        SupermetricsAPIError: The subclass matching the recorded status when one is
            available, otherwise an unclassified error naming the unexpected type.
    """
    _try_classify_from_record(endpoint, not_found_msg=not_found_msg, bad_request_msg=None)
    raise SupermetricsAPIError(f"Unexpected response: {type(response).__name__}", endpoint=endpoint)


def _raise_from_unparseable_response(
    error: Exception,
    endpoint: str,
    *,
    not_found_msg: str,
    bad_request_msg: str | None,
) -> NoReturn:
    """Classify a response whose body could not be parsed into a generated model.

    Args:
        error: The parsing failure.
        endpoint: The endpoint being called, for error context.
        not_found_msg: Message to use if the response turns out to be a 404.
        bad_request_msg: Message to use if the response turns out to be a 400.

    Raises:
        SupermetricsAPIError: Always, classified by the real HTTP status when one
            was observed, or unclassified (status 0) when the failure happened
            without a response.
    """
    try:
        _try_classify_from_record(endpoint, not_found_msg=not_found_msg, bad_request_msg=bad_request_msg)
    except SupermetricsAPIError as classified:
        raise classified from error
    raise SupermetricsAPIError(str(error), status_code=0, endpoint=endpoint) from error


@contextmanager
def api_error_handler(
    endpoint: str,
    *,
    context_400: str | None = None,
    context_404: str | None = None,
) -> Generator[None, None, None]:
    """Context manager that translates low-level exceptions into SDK exceptions.

    Args:
        endpoint: The endpoint being called, for error context.
        context_400: Short description used in HTTP 400 messages.
        context_404: Short description used in HTTP 404 messages.

    Yields:
        ``None``.

    Raises:
        SupermetricsError: Any SDK error raised inside the block passes through
            unchanged; low-level ``httpx`` and value errors are translated. A
            response body that does not match the generated schema is still
            classified by its real HTTP status code.
    """
    reset_last_response()
    try:
        yield
    except SupermetricsAPIError as e:
        # An adapter reported an API error it could not classify (typically because
        # the response carried a status the OpenAPI document does not describe for
        # this operation). Upgrade it using the status the transport actually saw.
        if not e.status_code:
            try:
                _try_classify_from_record(
                    endpoint,
                    not_found_msg=context_404 or "Resource not found",
                    bad_request_msg=context_400,
                )
            except SupermetricsAPIError as classified:
                raise classified from e
        raise
    except SupermetricsError:
        raise
    except (ValueError, TypeError, KeyError) as e:
        _raise_from_unparseable_response(
            e,
            endpoint,
            not_found_msg=context_404 or "Resource not found",
            bad_request_msg=context_400,
        )
    except httpx.HTTPStatusError as e:
        _handle_http_error(e, context_400=context_400, context_404=context_404)
    except httpx.RequestError as e:
        _handle_request_error(e)
