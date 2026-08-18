"""Unit tests for the shared resource error-handling helpers."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from supermetrics._auth import AuthConfig
from supermetrics._transport import ResponseRecord, build_sync_event_hooks, current_last_response
from supermetrics.exceptions import (
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsClientError,
    SupermetricsError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)
from supermetrics.resources._error_handlers import (
    _extract_error_fields,
    _raise_for_error_response,
    _raise_for_status,
    _raise_unexpected_response,
    _raw_response_of,
    _status_to_exception,
    api_error_handler,
)

ENDPOINT = "https://api.supermetrics.com/v1/things"
BASE_URL = "https://api.supermetrics.com"


@pytest.fixture(autouse=True)
def isolate_last_response() -> Iterator[None]:
    """Give every test its own view of the last-response context variable."""
    token = current_last_response.set(None)
    try:
        yield
    finally:
        current_last_response.reset(token)


class _ErrorObject:
    """Stand-in for a generated ``Error`` model, which exposes fields as attributes."""

    def __init__(self, **fields: Any) -> None:
        for name, value in fields.items():
            setattr(self, name, value)


class _ErrorResponseObject:
    """Stand-in for a generated ``ErrorResponse`` model wrapping an ``error`` member."""

    def __init__(self, error: object) -> None:
        self.error = error


def _record(status_code: int, content: bytes, headers: dict[str, str] | None = None) -> ResponseRecord:
    """Build a response record as the transport hooks would have written it."""
    return ResponseRecord(
        status_code=status_code,
        headers=httpx.Headers(headers or {}),
        content=content,
        request_url=ENDPOINT,
    )


class TestStatusToException:
    """Tests for the HTTP status code to exception class mapping."""

    @pytest.mark.parametrize(
        ("status_code", "expected"),
        [
            (400, SupermetricsValidationError),
            (401, SupermetricsAuthError),
            (403, SupermetricsForbiddenError),
            (404, SupermetricsNotFoundError),
            (409, SupermetricsAPIError),
            (418, SupermetricsAPIError),
            (422, SupermetricsValidationError),
            (429, SupermetricsRateLimitError),
            (500, SupermetricsServerError),
            (503, SupermetricsServerError),
        ],
    )
    def test_status_maps_to_expected_class(self, status_code: int, expected: type[SupermetricsAPIError]) -> None:
        """Each HTTP status resolves to the exception class documented for it."""
        assert _status_to_exception(status_code) is expected

    def test_unmapped_client_status_falls_back_to_the_api_error_base(self) -> None:
        """A 4xx status with no dedicated subclass falls back to SupermetricsAPIError itself."""
        assert _status_to_exception(451) is SupermetricsAPIError

    @pytest.mark.parametrize(
        ("status_code", "expected"),
        [
            (399, SupermetricsAPIError),
            (428, SupermetricsAPIError),
            (430, SupermetricsAPIError),
            (499, SupermetricsAPIError),
            (500, SupermetricsServerError),
            (599, SupermetricsServerError),
        ],
    )
    def test_server_error_band_starts_at_500(self, status_code: int, expected: type[SupermetricsAPIError]) -> None:
        """Only 5xx statuses become server errors; the neighbouring codes stay generic."""
        assert _status_to_exception(status_code) is expected


class TestExtractErrorFields:
    """Tests for pulling the upstream error code, message and details out of a payload."""

    def test_none_payload_yields_empty_fields(self) -> None:
        """A missing payload produces no code, an empty message and no details."""
        assert _extract_error_fields(None) == (None, "", None)

    def test_dict_payload_is_unwrapped(self) -> None:
        """A plain dict payload exposes the nested error code, message and details."""
        payload = {"error": {"code": "BAD_REQUEST", "message": "ds_id is required", "details": {"field": "ds_id"}}}

        assert _extract_error_fields(payload) == ("BAD_REQUEST", "ds_id is required", {"field": "ds_id"})

    def test_object_payload_is_unwrapped(self) -> None:
        """An object payload exposing an ``error`` attribute is read via attribute access."""
        payload = _ErrorResponseObject(
            _ErrorObject(
                code="CONNECTOR_NOT_FOUND",
                message="Not found",
                description="No connector with that id",
                details={"connector_id": "abc"},
            )
        )

        code, message, details = _extract_error_fields(payload)

        assert code == "CONNECTOR_NOT_FOUND"
        assert message == "Not found: No connector with that id"
        assert details == {"connector_id": "abc"}

    def test_string_error_member_is_ignored(self) -> None:
        """A payload whose ``error`` is a bare string carries no structured fields."""
        assert _extract_error_fields({"error": "something went wrong"}) == (None, "", None)

    def test_missing_error_key_yields_empty_fields(self) -> None:
        """A dict payload without an ``error`` key produces no structured fields."""
        assert _extract_error_fields({"data": [1, 2, 3]}) == (None, "", None)

    def test_description_duplicating_the_message_is_not_appended(self) -> None:
        """A description identical to the message does not get concatenated onto it."""
        payload = {"error": {"code": "FORBIDDEN", "message": "Access denied", "description": "Access denied"}}

        assert _extract_error_fields(payload) == ("FORBIDDEN", "Access denied", None)

    def test_description_duplicating_the_code_is_not_appended(self) -> None:
        """A description that merely repeats the error code is not concatenated onto the message."""
        payload = {"error": {"code": "FORBIDDEN", "message": "Access denied", "description": "FORBIDDEN"}}

        assert _extract_error_fields(payload) == ("FORBIDDEN", "Access denied", None)

    def test_description_alone_becomes_the_message(self) -> None:
        """When only a description is present it is used as the message."""
        payload = {"error": {"code": "NOT_FOUND", "description": "No such login"}}

        assert _extract_error_fields(payload) == ("NOT_FOUND", "No such login", None)

    def test_empty_code_is_normalised_to_none(self) -> None:
        """An empty upstream code is reported as ``None`` rather than an empty string."""
        code, message, _ = _extract_error_fields({"error": {"code": "", "message": "boom"}})

        assert code is None
        assert message == "boom"

    def test_non_string_fields_are_ignored(self) -> None:
        """Non-string code and message values are treated as absent instead of crashing."""
        assert _extract_error_fields({"error": {"code": 404, "message": None}}) == (None, "", None)

    def test_description_equal_to_the_code_leaves_the_message_empty(self) -> None:
        """With no message and a description that only echoes the code, nothing usable is produced."""
        assert _extract_error_fields({"error": {"code": "NOT_FOUND", "description": "NOT_FOUND"}}) == (
            "NOT_FOUND",
            "",
            None,
        )

    def test_message_and_distinct_description_are_joined(self) -> None:
        """A description that adds information is appended to the message."""
        payload = {"error": {"code": "BAD_REQUEST", "message": "Invalid field", "description": "ds_id must be set"}}

        assert _extract_error_fields(payload) == ("BAD_REQUEST", "Invalid field: ds_id must be set", None)

    def test_list_error_member_yields_empty_fields(self) -> None:
        """An ``error`` member that is a list carries no fields instead of crashing."""
        assert _extract_error_fields({"error": [{"code": "NOT_FOUND"}]}) == (None, "", None)

    def test_non_dict_details_are_dropped(self) -> None:
        """Details that are not a mapping are discarded rather than passed through."""
        code, _, details = _extract_error_fields({"error": {"code": "X", "details": ["a", "b"]}})

        assert code == "X"
        assert details is None


class TestRaiseForStatus:
    """Tests for translating a non-success HTTP status code into an SDK exception."""

    @pytest.mark.parametrize(
        ("status_code", "expected"),
        [
            (400, SupermetricsValidationError),
            (401, SupermetricsAuthError),
            (403, SupermetricsForbiddenError),
            (404, SupermetricsNotFoundError),
            (409, SupermetricsAPIError),
            (418, SupermetricsAPIError),
            (422, SupermetricsValidationError),
            (429, SupermetricsRateLimitError),
            (500, SupermetricsServerError),
            (503, SupermetricsServerError),
        ],
    )
    def test_status_raises_expected_class(self, status_code: int, expected: type[SupermetricsAPIError]) -> None:
        """The raised exception class matches the status matrix and carries the status code."""
        with pytest.raises(expected) as exc_info:
            _raise_for_status(status_code, None, ENDPOINT, raw_body="boom")

        assert type(exc_info.value) is expected
        assert exc_info.value.status_code == status_code
        assert exc_info.value.endpoint == ENDPOINT
        assert exc_info.value.response_body == "boom"

    def test_transport_context_is_preserved(self) -> None:
        """Endpoint, body, headers, upstream code and details all survive the translation."""
        payload = {"error": {"code": "VALIDATION_ERROR", "message": "bad ds_id", "details": {"field": "ds_id"}}}

        with pytest.raises(SupermetricsValidationError) as exc_info:
            _raise_for_status(
                422,
                payload,
                ENDPOINT,
                headers={"X-Request-Id": "req-1", "X-Span-Id": "span-1"},
                raw_body=b'{"error": {"code": "VALIDATION_ERROR"}}',
            )

        error = exc_info.value
        assert error.status_code == 422
        assert error.message == "bad ds_id"
        assert error.endpoint == ENDPOINT
        assert error.response_body == "bad ds_id"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.details == {"field": "ds_id"}
        assert error.headers is not None
        assert error.request_id == "req-1"
        assert error.span_id == "span-1"

    def test_headers_are_matched_case_insensitively(self) -> None:
        """Headers supplied as a plain dict become case-insensitive httpx headers."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_status(409, None, ENDPOINT, headers={"x-request-id": "req-2"})

        assert exc_info.value.headers is not None
        assert exc_info.value.headers["X-Request-Id"] == "req-2"

    def test_missing_headers_leave_the_accessors_empty(self) -> None:
        """Without response headers the derived accessors return ``None`` instead of raising."""
        with pytest.raises(SupermetricsServerError) as exc_info:
            _raise_for_status(500, None, ENDPOINT, raw_body="oops")

        assert exc_info.value.headers is None
        assert exc_info.value.retry_after is None
        assert exc_info.value.request_id is None

    def test_not_found_message_is_honoured(self) -> None:
        """A caller-supplied 404 message replaces the default ``Resource not found``."""
        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_for_status(404, None, ENDPOINT, not_found_msg="Login 'abc' not found", raw_body="ignored body")

        assert exc_info.value.message == "Login 'abc' not found"
        assert exc_info.value.response_body == "ignored body"

    def test_not_found_overrides_the_message_but_keeps_the_upstream_code(self) -> None:
        """A 404 replaces the payload message yet still reports code and details for the caller."""
        payload = {"error": {"code": "LOGIN_NOT_FOUND", "message": "no login abc", "details": {"id": "abc"}}}

        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_for_status(404, payload, ENDPOINT, not_found_msg="Login 'abc' not found")

        error = exc_info.value
        assert error.message == "Login 'abc' not found"
        assert error.error_code == "LOGIN_NOT_FOUND"
        assert error.details == {"id": "abc"}
        assert error.response_body == "no login abc"

    def test_not_found_message_defaults(self) -> None:
        """Without an override a 404 reports the generic not-found message."""
        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_for_status(404, None, ENDPOINT)

        assert exc_info.value.message == "Resource not found"

    def test_bad_request_message_is_honoured(self) -> None:
        """A caller-supplied 400 message takes precedence over the response body."""
        with pytest.raises(SupermetricsValidationError) as exc_info:
            _raise_for_status(400, None, ENDPOINT, bad_request_msg="Invalid query", raw_body="raw detail")

        assert exc_info.value.message == "Invalid query"
        assert exc_info.value.response_body == "raw detail"

    def test_bad_request_falls_back_to_the_body(self) -> None:
        """Without an override a 400 reports the response body as the message."""
        with pytest.raises(SupermetricsValidationError) as exc_info:
            _raise_for_status(400, None, ENDPOINT, raw_body="ds_id is required")

        assert exc_info.value.message == "ds_id is required"

    def test_bad_request_with_no_body_uses_a_generic_message(self) -> None:
        """A 400 with neither override nor body still produces an actionable message."""
        with pytest.raises(SupermetricsValidationError) as exc_info:
            _raise_for_status(400, None, ENDPOINT)

        assert exc_info.value.message == "Invalid request parameters"

    def test_unprocessable_entity_with_no_body_uses_a_generic_message(self) -> None:
        """A 422 with neither payload nor body still produces an actionable message."""
        with pytest.raises(SupermetricsValidationError) as exc_info:
            _raise_for_status(422, None, ENDPOINT)

        assert exc_info.value.message == "Invalid request parameters"

    def test_unprocessable_entity_reports_the_payload_message(self) -> None:
        """A 422 carrying a structured message reports it verbatim, without a status prefix."""
        with pytest.raises(SupermetricsValidationError) as exc_info:
            _raise_for_status(422, {"error": {"code": "UNPROCESSABLE_ENTITY", "message": "field too long"}}, ENDPOINT)

        assert exc_info.value.message == "field too long"

    def test_unauthorized_message_never_echoes_the_body(self) -> None:
        """A 401 reports a fixed message so response contents are not surfaced verbatim."""
        with pytest.raises(SupermetricsAuthError) as exc_info:
            _raise_for_status(401, None, ENDPOINT, raw_body="token otok_secret is invalid")

        assert exc_info.value.message == "Invalid or expired API key"

    def test_forbidden_falls_back_to_a_generic_message(self) -> None:
        """A 403 with no body explains that permissions are insufficient."""
        with pytest.raises(SupermetricsForbiddenError) as exc_info:
            _raise_for_status(403, None, ENDPOINT)

        assert exc_info.value.message == "Forbidden - insufficient permissions"

    def test_raw_body_accepts_bytes(self) -> None:
        """A bytes body is decoded into the message and the preserved response body."""
        with pytest.raises(SupermetricsServerError) as exc_info:
            _raise_for_status(500, None, ENDPOINT, raw_body=b"upstream exploded")

        assert exc_info.value.message == "API error: upstream exploded"
        assert exc_info.value.response_body == "upstream exploded"

    def test_raw_body_accepts_str(self) -> None:
        """A str body is used as-is for both the message and the preserved body."""
        with pytest.raises(SupermetricsServerError) as exc_info:
            _raise_for_status(500, None, ENDPOINT, raw_body="upstream exploded")

        assert exc_info.value.message == "API error: upstream exploded"
        assert exc_info.value.response_body == "upstream exploded"

    def test_undecodable_bytes_do_not_crash_the_translation(self) -> None:
        """Invalid UTF-8 in the body is replaced rather than raising a decode error."""
        with pytest.raises(SupermetricsServerError) as exc_info:
            _raise_for_status(502, None, ENDPOINT, raw_body=b"\xff\xfe")

        assert exc_info.value.response_body == "��"

    def test_parsed_payload_message_wins_over_the_raw_body(self) -> None:
        """A structured error message is preferred over the raw response text."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_status(
                409,
                {"error": {"code": "CONFLICT_ERROR", "message": "Already exists"}},
                ENDPOINT,
                raw_body=b'{"error": {"code": "CONFLICT_ERROR"}}',
            )

        assert exc_info.value.message == "API error (409): Already exists"
        assert exc_info.value.response_body == "Already exists"

    def test_unstructured_payload_is_stringified_when_no_body_is_available(self) -> None:
        """A payload with no usable error fields and no raw body is stringified for context."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_status(409, {"unexpected": "shape"}, ENDPOINT)

        assert exc_info.value.message == "API error (409): {'unexpected': 'shape'}"
        assert exc_info.value.response_body == "{'unexpected': 'shape'}"
        assert exc_info.value.error_code is None

    def test_retry_after_is_readable_on_a_rate_limit_error(self) -> None:
        """A 429 exposes the ``Retry-After`` header as an integer number of seconds."""
        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            _raise_for_status(
                429,
                {"error": {"code": "TOO_MANY_REQUESTS", "message": "slow down"}},
                ENDPOINT,
                headers={"Retry-After": "30"},
            )

        assert exc_info.value.retry_after == 30
        assert exc_info.value.message == "Rate limit exceeded: slow down"
        assert exc_info.value.error_code == "TOO_MANY_REQUESTS"

    def test_headers_fall_back_to_the_recorded_response(self) -> None:
        """Adapters that cannot pass headers still get them from the transport record."""
        current_last_response.set(_record(429, b"", {"Retry-After": "12", "X-Request-Id": "req-ctx"}))

        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            _raise_for_status(429, None, ENDPOINT)

        assert exc_info.value.retry_after == 12
        assert exc_info.value.request_id == "req-ctx"

    def test_explicit_headers_win_over_the_recorded_response(self) -> None:
        """Headers passed by the caller are used instead of the recorded ones."""
        current_last_response.set(_record(429, b"", {"Retry-After": "12"}))

        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            _raise_for_status(429, None, ENDPOINT, headers={"Retry-After": "3"})

        assert exc_info.value.retry_after == 3

    def test_non_numeric_retry_after_is_reported_as_none(self) -> None:
        """A date-formatted ``Retry-After`` is not misreported as a number of seconds."""
        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            _raise_for_status(429, None, ENDPOINT, headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"})

        assert exc_info.value.retry_after is None
        assert exc_info.value.message == "Rate limit exceeded"


class TestRaiseForErrorResponse:
    """Tests for translating an upstream error payload into an SDK exception."""

    #: ``UPSTREAM_MSG`` is the message every payload in the matrix below carries.
    UPSTREAM_MSG = "upstream said no"
    #: The two codes that are answered with a fixed message instead of the upstream one.
    GENERIC_CREDENTIAL_MSG = "Invalid or expired API key"

    @pytest.mark.parametrize(
        ("code", "expected", "expected_status", "expected_message"),
        [
            ("BAD_REQUEST", SupermetricsValidationError, 400, UPSTREAM_MSG),
            ("VALIDATION_ERROR", SupermetricsValidationError, 400, UPSTREAM_MSG),
            ("UNAUTHORIZED", SupermetricsAuthError, 401, GENERIC_CREDENTIAL_MSG),
            ("401", SupermetricsAuthError, 401, GENERIC_CREDENTIAL_MSG),
            ("ACCESS_TOKEN_EXPIRED", SupermetricsAuthError, 401, UPSTREAM_MSG),
            ("INVALID_TOKEN", SupermetricsAuthError, 401, UPSTREAM_MSG),
            ("FORBIDDEN", SupermetricsForbiddenError, 403, UPSTREAM_MSG),
            ("ACCESS_DENIED", SupermetricsForbiddenError, 403, UPSTREAM_MSG),
            ("PERMISSION_ERROR", SupermetricsForbiddenError, 403, UPSTREAM_MSG),
            ("NOT_FOUND", SupermetricsNotFoundError, 404, UPSTREAM_MSG),
            ("CONNECTOR_NOT_FOUND", SupermetricsNotFoundError, 404, UPSTREAM_MSG),
            ("SECRET_NOT_FOUND", SupermetricsNotFoundError, 404, UPSTREAM_MSG),
            ("LOG_NOT_FOUND", SupermetricsNotFoundError, 404, UPSTREAM_MSG),
            ("CONFLICT_ERROR", SupermetricsAPIError, 409, UPSTREAM_MSG),
            ("UNPROCESSABLE_ENTITY", SupermetricsValidationError, 422, UPSTREAM_MSG),
            ("INTERNAL_SERVER_ERROR", SupermetricsServerError, 500, UPSTREAM_MSG),
            # SERVICE_UNAVAILABLE is a 503 upstream but the mapping reports 500; this
            # pins the current behaviour so a deliberate fix shows up as a test change.
            ("SERVICE_UNAVAILABLE", SupermetricsServerError, 500, UPSTREAM_MSG),
            ("TOO_MANY_REQUESTS", SupermetricsRateLimitError, 429, UPSTREAM_MSG),
        ],
    )
    def test_upstream_code_maps_to_expected_class(
        self, code: str, expected: type[SupermetricsAPIError], expected_status: int, expected_message: str
    ) -> None:
        """Each documented upstream error code maps to its exception class, status and message."""
        with pytest.raises(expected) as exc_info:
            _raise_for_error_response({"error": {"code": code, "message": self.UPSTREAM_MSG}}, ENDPOINT)

        error = exc_info.value
        assert type(error) is expected
        assert error.status_code == expected_status
        assert error.error_code == code
        assert error.endpoint == ENDPOINT
        assert error.message == expected_message
        assert error.response_body == expected_message

    def test_codes_are_matched_case_insensitively(self) -> None:
        """A lower-case upstream code is recognised just like its canonical spelling."""
        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_for_error_response({"error": {"code": "not_found", "message": "gone"}}, ENDPOINT)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "not_found"

    def test_access_token_invalid_maps_to_auth_error_preserving_the_code(self) -> None:
        """``ACCESS_TOKEN_INVALID`` becomes an auth error whose code callers can act on."""
        with pytest.raises(SupermetricsAuthError) as exc_info:
            _raise_for_error_response(
                {"error": {"code": "ACCESS_TOKEN_INVALID", "message": "The access token is invalid"}},
                ENDPOINT,
            )

        error = exc_info.value
        assert error.status_code == 401
        assert error.error_code == "ACCESS_TOKEN_INVALID"
        assert error.message == "The access token is invalid"

    @pytest.mark.parametrize("code", ["OAUTH_TOKEN_EXPIRED", "OAUTH_INVALID_GRANT", "oauth_client_unauthorized"])
    def test_oauth_prefixed_codes_map_to_auth_error(self, code: str) -> None:
        """Any ``OAUTH_*`` code is treated as an authentication failure."""
        with pytest.raises(SupermetricsAuthError) as exc_info:
            _raise_for_error_response({"error": {"code": code, "message": "refresh required"}}, ENDPOINT)

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == code
        assert exc_info.value.message == "refresh required"

    @pytest.mark.parametrize("code", ["NOT_OAUTH_TOKEN", "TOKEN_OAUTH_EXPIRED", "OAUTH"])
    def test_codes_that_only_contain_oauth_are_not_auth_errors(self, code: str) -> None:
        """The OAuth rule is a prefix match, so a code merely containing it stays unclassified."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_error_response({"error": {"code": code, "message": "nope"}}, ENDPOINT)

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.status_code == 0

    def test_empty_code_with_a_message_is_unclassified(self) -> None:
        """A payload with a message but no code cannot be classified and keeps status 0."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_error_response({"error": {"code": "", "message": "something broke"}}, ENDPOINT)

        error = exc_info.value
        assert type(error) is SupermetricsAPIError
        assert error.status_code == 0
        assert error.error_code is None
        assert error.message == "API error: something broke"

    def test_unauthorized_code_reports_the_generic_credential_message(self) -> None:
        """A bare ``UNAUTHORIZED`` code reports the generic credential message."""
        with pytest.raises(SupermetricsAuthError) as exc_info:
            _raise_for_error_response({"error": {"code": "UNAUTHORIZED", "message": "token otok_secret"}}, ENDPOINT)

        assert exc_info.value.message == "Invalid or expired API key"
        assert exc_info.value.response_body == "Invalid or expired API key"

    def test_unrecognised_code_yields_an_unclassified_api_error(self) -> None:
        """An unknown upstream code produces a base API error with no HTTP status."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_error_response({"error": {"code": "TEAPOT_OVERFLOW", "message": "brewing"}}, ENDPOINT)

        error = exc_info.value
        assert type(error) is SupermetricsAPIError
        assert error.status_code == 0
        assert error.error_code == "TEAPOT_OVERFLOW"
        assert error.message == "API error: brewing"

    def test_payload_without_an_error_member_yields_an_unclassified_api_error(self) -> None:
        """A payload the helper cannot interpret is surfaced with status 0 and its repr."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_for_error_response("total gibberish", ENDPOINT)

        assert exc_info.value.status_code == 0
        assert exc_info.value.message == "API error: total gibberish"
        assert exc_info.value.error_code is None

    def test_headers_and_details_are_preserved(self) -> None:
        """Response headers and structured details survive the translation."""
        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            _raise_for_error_response(
                {"error": {"code": "TOO_MANY_REQUESTS", "message": "slow", "details": {"limit": 100}}},
                ENDPOINT,
                headers={"Retry-After": "5", "X-Request-Id": "req-9"},
            )

        error = exc_info.value
        assert error.retry_after == 5
        assert error.request_id == "req-9"
        assert error.details == {"limit": 100}

    def test_headers_fall_back_to_the_recorded_response(self) -> None:
        """Without explicit headers the recorded transport metadata is used."""
        current_last_response.set(_record(429, b"", {"Retry-After": "9", "X-Span-Id": "span-ctx"}))

        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            _raise_for_error_response({"error": {"code": "TOO_MANY_REQUESTS", "message": "slow"}}, ENDPOINT)

        assert exc_info.value.retry_after == 9
        assert exc_info.value.span_id == "span-ctx"

    def test_generated_model_style_object_is_accepted(self) -> None:
        """An attribute-based error model is translated the same way as a dict payload."""
        payload = _ErrorResponseObject(_ErrorObject(code="SECRET_NOT_FOUND", message="No such secret"))

        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_for_error_response(payload, ENDPOINT)

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "No such secret"
        assert exc_info.value.error_code == "SECRET_NOT_FOUND"


class TestRaiseUnexpectedResponse:
    """Tests for the fallback used when the generated parser returns nothing usable."""

    def test_without_a_record_the_payload_type_is_reported(self) -> None:
        """With no observed response the error names the type the parser handed back."""
        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_unexpected_response(None, ENDPOINT)

        error = exc_info.value
        assert type(error) is SupermetricsAPIError
        assert error.message == "Unexpected response: NoneType"
        assert error.endpoint == ENDPOINT
        assert error.status_code is None

    def test_a_successful_record_does_not_rescue_the_classification(self) -> None:
        """A 2xx record means the status was fine, so the payload type is still reported."""
        current_last_response.set(_record(200, b'{"unexpected": "shape"}'))

        with pytest.raises(SupermetricsAPIError) as exc_info:
            _raise_unexpected_response({"unexpected": "shape"}, ENDPOINT)

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.message == "Unexpected response: dict"

    def test_a_recorded_failure_is_classified_by_its_status(self) -> None:
        """An undocumented 401 still becomes an auth error carrying the upstream code."""
        body = b'{"error": {"code": "ACCESS_TOKEN_INVALID", "message": "The access token is invalid"}}'
        current_last_response.set(_record(401, body, {"X-Request-Id": "req-unexpected"}))

        with pytest.raises(SupermetricsAuthError) as exc_info:
            _raise_unexpected_response(None, ENDPOINT)

        error = exc_info.value
        assert error.status_code == 401
        assert error.error_code == "ACCESS_TOKEN_INVALID"
        assert error.message == "Invalid or expired API key"
        assert error.request_id == "req-unexpected"

    def test_a_recorded_404_uses_the_supplied_message(self) -> None:
        """The caller's not-found wording is used for a recovered 404."""
        current_last_response.set(_record(404, b""))

        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_unexpected_response(None, ENDPOINT, not_found_msg="Connector 'abc' not found")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Connector 'abc' not found"

    def test_a_recorded_404_defaults_to_the_generic_message(self) -> None:
        """Without a caller message a recovered 404 reports the generic wording."""
        current_last_response.set(_record(404, b""))

        with pytest.raises(SupermetricsNotFoundError) as exc_info:
            _raise_unexpected_response(None, ENDPOINT)

        assert exc_info.value.message == "Resource not found"


class TestApiErrorHandlerPassThrough:
    """Tests for exceptions that ``api_error_handler`` must not rewrite."""

    def test_sdk_api_errors_pass_through_untouched(self) -> None:
        """An SDK error raised inside the block is re-raised as the very same object."""
        original = SupermetricsNotFoundError("gone", status_code=404, endpoint=ENDPOINT)

        with pytest.raises(SupermetricsNotFoundError) as exc_info, api_error_handler(ENDPOINT):
            raise original

        assert exc_info.value is original

    def test_client_errors_pass_through_despite_being_value_errors(self) -> None:
        """A client configuration error is not reclassified even though it is a ValueError."""
        original = SupermetricsClientError("no credentials supplied")

        with pytest.raises(SupermetricsClientError) as exc_info, api_error_handler(ENDPOINT):
            raise original

        assert exc_info.value is original

    def test_unrelated_exceptions_are_not_swallowed(self) -> None:
        """An exception outside the handled taxonomy propagates unchanged."""
        with pytest.raises(RuntimeError, match="unrelated"), api_error_handler(ENDPOINT):
            raise RuntimeError("unrelated")

    def test_successful_block_raises_nothing(self) -> None:
        """The handler is transparent when the wrapped block succeeds."""
        with api_error_handler(ENDPOINT):
            result = 1 + 1

        assert result == 2

    def test_entering_the_handler_clears_a_stale_response_record(self) -> None:
        """The record from an earlier call is dropped on entry, before the block runs."""
        current_last_response.set(_record(500, b"an older failure"))
        seen: list[object] = []

        with api_error_handler(ENDPOINT):
            seen.append(current_last_response.get())

        assert seen == [None]

    def test_unrelated_exception_is_not_swallowed_even_with_a_failed_response_recorded(self) -> None:
        """A recorded 500 does not turn an unrelated exception into an SDK error."""
        with pytest.raises(RuntimeError, match="unrelated"), api_error_handler(ENDPOINT):
            current_last_response.set(_record(500, b"boom"))
            raise RuntimeError("unrelated")


class TestApiErrorHandlerHttpxErrors:
    """Tests for translating low-level httpx failures."""

    def test_request_error_becomes_a_network_error(self) -> None:
        """A transport failure becomes a NetworkError carrying the attempted endpoint."""
        request = httpx.Request("GET", ENDPOINT)

        original = httpx.ConnectTimeout("timed out", request=request)

        with pytest.raises(NetworkError) as exc_info, api_error_handler(ENDPOINT):
            raise original

        error = exc_info.value
        assert type(error) is NetworkError
        assert error.endpoint == ENDPOINT
        assert error.message == "Network error: timed out"
        assert error.status_code is None
        assert error.__cause__ is original

    def test_network_error_is_not_an_api_error(self) -> None:
        """A NetworkError stays outside the HTTP error taxonomy so retries can distinguish it."""
        request = httpx.Request("GET", ENDPOINT)

        with pytest.raises(SupermetricsError) as exc_info, api_error_handler(ENDPOINT):
            raise httpx.ConnectError("refused", request=request)

        assert type(exc_info.value) is NetworkError
        assert not isinstance(exc_info.value, SupermetricsAPIError)

    def test_request_error_without_a_bound_request_still_becomes_a_network_error(self) -> None:
        """A transport failure raised before a request was bound must not mask itself."""
        with pytest.raises(NetworkError) as exc_info, api_error_handler(ENDPOINT):
            raise httpx.ConnectError("name resolution failed")

        assert exc_info.value.message == "Network error: name resolution failed"
        assert exc_info.value.endpoint is None

    def test_network_error_endpoint_comes_from_the_failed_request(self) -> None:
        """The endpoint on a NetworkError is the URL httpx actually tried, not the handler argument."""
        request = httpx.Request("GET", "https://api.supermetrics.com/v1/other")

        with pytest.raises(NetworkError) as exc_info, api_error_handler(ENDPOINT):
            raise httpx.ReadTimeout("read timed out", request=request)

        assert exc_info.value.endpoint == "https://api.supermetrics.com/v1/other"

    @pytest.mark.parametrize(
        ("status_code", "expected"),
        [
            (400, SupermetricsValidationError),
            (401, SupermetricsAuthError),
            (403, SupermetricsForbiddenError),
            (404, SupermetricsNotFoundError),
            (409, SupermetricsAPIError),
            (418, SupermetricsAPIError),
            (422, SupermetricsValidationError),
            (429, SupermetricsRateLimitError),
            (500, SupermetricsServerError),
            (503, SupermetricsServerError),
        ],
    )
    def test_http_status_error_uses_the_status_matrix(
        self, status_code: int, expected: type[SupermetricsAPIError]
    ) -> None:
        """A raised-for-status httpx error is translated with the same status matrix."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(status_code, text="upstream body", request=request)

        with pytest.raises(expected) as exc_info, api_error_handler(ENDPOINT):
            response.raise_for_status()

        error = exc_info.value
        assert type(error) is expected
        assert error.status_code == status_code
        assert error.endpoint == ENDPOINT
        assert error.response_body == "upstream body"
        assert error.raw_response is response

    def test_http_status_error_preserves_response_headers(self) -> None:
        """Headers from the failing response remain readable on the translated error."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(429, text="slow down", headers={"Retry-After": "7"}, request=request)

        with pytest.raises(SupermetricsRateLimitError) as exc_info, api_error_handler(ENDPOINT):
            response.raise_for_status()

        assert exc_info.value.retry_after == 7

    def test_http_status_error_401_message_never_echoes_the_body(self) -> None:
        """A 401 from httpx reports the fixed credential message."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(401, text="token otok_secret rejected", request=request)

        with pytest.raises(SupermetricsAuthError) as exc_info, api_error_handler(ENDPOINT):
            response.raise_for_status()

        assert exc_info.value.message == "Invalid or expired API key"

    def test_http_status_error_uses_the_400_context(self) -> None:
        """The caller's 400 context is prepended to the response body."""
        request = httpx.Request("POST", ENDPOINT)
        response = httpx.Response(400, text="ds_id missing", request=request)

        with (
            pytest.raises(SupermetricsValidationError) as exc_info,
            api_error_handler(ENDPOINT, context_400="Invalid login link request"),
        ):
            response.raise_for_status()

        assert exc_info.value.message == "Invalid login link request: ds_id missing"

    def test_http_status_error_uses_the_404_context(self) -> None:
        """The caller's 404 context is prepended to the response body."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(404, text="no such id", request=request)

        with (
            pytest.raises(SupermetricsNotFoundError) as exc_info,
            api_error_handler(ENDPOINT, context_404="Login 'abc' not found"),
        ):
            response.raise_for_status()

        assert exc_info.value.message == "Login 'abc' not found: no such id"

    @pytest.mark.parametrize("status_code", [400, 404])
    def test_http_status_error_ignores_a_context_for_a_different_status(self, status_code: int) -> None:
        """A 404 context is not applied to a 400 response, and vice versa."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(status_code, text="body text", request=request)
        contexts: dict[str, str] = {"context_400": "ctx 400"} if status_code == 404 else {"context_404": "ctx 404"}

        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT, **contexts):
            response.raise_for_status()

        assert exc_info.value.message == f"API error ({status_code}): body text"

    def test_http_status_error_is_chained_to_the_httpx_error(self) -> None:
        """The original httpx error stays reachable as ``__cause__`` for debugging."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(404, text="no such id", request=request)

        with pytest.raises(SupermetricsNotFoundError) as exc_info, api_error_handler(ENDPOINT):
            response.raise_for_status()

        assert isinstance(exc_info.value.__cause__, httpx.HTTPStatusError)

    def test_http_status_error_without_context_uses_a_generic_message(self) -> None:
        """Without caller context the message still names the status and the body."""
        request = httpx.Request("GET", ENDPOINT)
        response = httpx.Response(409, text="already exists", request=request)

        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            response.raise_for_status()

        assert exc_info.value.message == "API error (409): already exists"

    def test_http_status_error_endpoint_comes_from_the_request(self) -> None:
        """The endpoint recorded on the error is the URL that actually failed."""
        request = httpx.Request("GET", "https://api.supermetrics.com/v1/other")
        response = httpx.Response(500, text="boom", request=request)

        with pytest.raises(SupermetricsServerError) as exc_info, api_error_handler(ENDPOINT):
            response.raise_for_status()

        assert exc_info.value.endpoint == "https://api.supermetrics.com/v1/other"
        assert exc_info.value.message == "Supermetrics API error: boom"


class TestApiErrorHandlerSchemaMismatch:
    """Tests for classifying responses whose body did not match the generated schema."""

    def test_parse_failure_without_a_response_is_unclassified(self) -> None:
        """A parse failure with no observed response yields an API error with status 0."""
        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            raise KeyError("data")

        error = exc_info.value
        assert type(error) is SupermetricsAPIError
        assert error.status_code == 0
        assert error.endpoint == ENDPOINT
        assert error.message == "'data'"

    def test_value_error_without_a_response_is_unclassified(self) -> None:
        """A ValueError from the generated models is handled the same way as a KeyError."""
        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            raise ValueError("not a valid datetime")

        assert exc_info.value.status_code == 0
        assert exc_info.value.message == "not a valid datetime"

    def test_type_error_without_a_response_is_unclassified(self) -> None:
        """A TypeError raised while building a generated model is also translated."""
        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            raise TypeError("expected str, got int")

        error = exc_info.value
        assert type(error) is SupermetricsAPIError
        assert error.status_code == 0
        assert error.endpoint == ENDPOINT
        assert error.message == "expected str, got int"

    def test_unclassified_parse_failure_is_chained_to_the_original(self) -> None:
        """The parsing failure remains reachable as ``__cause__`` so the traceback is not lost."""
        original = KeyError("data")

        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            raise original

        assert exc_info.value.__cause__ is original

    @pytest.mark.parametrize("status_code", [200, 201, 204, 299])
    def test_any_2xx_record_leaves_the_failure_unclassified(self, status_code: int) -> None:
        """Every success status, up to the 299 boundary, is treated as "no error observed"."""
        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(status_code, b'{"error": {"code": "NOT_FOUND"}}'))
            raise KeyError("data")

        assert type(exc_info.value) is SupermetricsAPIError
        assert exc_info.value.status_code == 0

    def test_a_300_record_is_classified_rather_than_ignored(self) -> None:
        """The success window ends at 299, so a redirect status is still surfaced to the caller."""
        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(300, b"multiple choices"))
            raise KeyError("data")

        assert exc_info.value.status_code == 300
        assert exc_info.value.message == "API error (300): multiple choices"

    def test_successful_response_does_not_taint_the_classification(self) -> None:
        """A parse failure after a 2xx response stays unclassified rather than faking a status."""
        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(200, b'{"unexpected": "shape"}'))
            raise KeyError("data")

        assert exc_info.value.status_code == 0
        assert type(exc_info.value) is SupermetricsAPIError

    def test_stale_response_from_before_the_block_is_ignored(self) -> None:
        """A record left over from an earlier call cannot leak into this call's classification."""
        current_last_response.set(_record(500, b"an older failure"))

        with pytest.raises(SupermetricsAPIError) as exc_info, api_error_handler(ENDPOINT):
            raise KeyError("data")

        assert exc_info.value.status_code == 0
        assert type(exc_info.value) is SupermetricsAPIError

    def test_recorded_401_is_classified_as_an_auth_error(self) -> None:
        """A parse failure on a 401 still surfaces as an auth error with the upstream code."""
        body = b'{"error": {"code": "ACCESS_TOKEN_INVALID", "message": "The access token is invalid"}}'

        with pytest.raises(SupermetricsAuthError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(401, body, {"X-Request-Id": "req-401"}))
            raise KeyError("data")

        error = exc_info.value
        assert error.status_code == 401
        assert error.error_code == "ACCESS_TOKEN_INVALID"
        assert error.message == "Invalid or expired API key"
        assert error.request_id == "req-401"

    def test_recorded_404_uses_the_caller_context(self) -> None:
        """The 404 context supplied to the handler is used for the recovered status."""
        with (
            pytest.raises(SupermetricsNotFoundError) as exc_info,
            api_error_handler(ENDPOINT, context_404="Connector 'abc' not found"),
        ):
            current_last_response.set(_record(404, b"{}"))
            raise KeyError("data")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Connector 'abc' not found"
        assert exc_info.value.response_body == "{}"

    def test_recorded_400_uses_the_caller_context(self) -> None:
        """The 400 context supplied to the handler is used for the recovered status."""
        with (
            pytest.raises(SupermetricsValidationError) as exc_info,
            api_error_handler(ENDPOINT, context_400="Invalid backfill request"),
        ):
            current_last_response.set(_record(400, b"whatever"))
            raise KeyError("data")

        assert exc_info.value.status_code == 400
        assert exc_info.value.message == "Invalid backfill request"

    def test_recorded_502_with_an_html_body_becomes_a_server_error(self) -> None:
        """A gateway returning HTML for a 502 is still classified as a server error."""
        with pytest.raises(SupermetricsServerError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(502, b"<html><body>502 Bad Gateway</body></html>"))
            raise KeyError("error")

        error = exc_info.value
        assert error.status_code == 502
        assert error.message == "API error: <html><body>502 Bad Gateway</body></html>"
        assert error.response_body == "<html><body>502 Bad Gateway</body></html>"
        assert error.error_code is None

    def test_recorded_429_preserves_retry_after(self) -> None:
        """A parse failure on a 429 still exposes the ``Retry-After`` hint."""
        body = b'{"error": {"code": "TOO_MANY_REQUESTS", "message": "slow down"}}'

        with pytest.raises(SupermetricsRateLimitError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(429, body, {"Retry-After": "15"}))
            raise ValueError("bad payload")

        assert exc_info.value.retry_after == 15
        assert exc_info.value.error_code == "TOO_MANY_REQUESTS"
        assert exc_info.value.message == "Rate limit exceeded: slow down"

    def test_non_json_body_is_recovered_as_plain_text(self) -> None:
        """A non-JSON error body is preserved verbatim instead of aborting classification."""
        with pytest.raises(SupermetricsForbiddenError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(403, b"access denied by proxy"))
            raise KeyError("error")

        assert exc_info.value.message == "access denied by proxy"

    def test_json_array_body_is_recovered_as_plain_text(self) -> None:
        """A JSON body that is not an object carries no error code but keeps its text."""
        with pytest.raises(SupermetricsServerError) as exc_info, api_error_handler(ENDPOINT):
            current_last_response.set(_record(500, b'["a", "b"]'))
            raise ValueError("expected dict")

        assert exc_info.value.error_code is None
        assert exc_info.value.response_body == '["a", "b"]'
        assert exc_info.value.message == 'API error: ["a", "b"]'


class TestApiErrorHandlerWithRealTransport:
    """Tests driving the handler through a real httpx pipeline with the SDK event hooks."""

    @staticmethod
    def _client(handler: Any) -> httpx.Client:
        """Build an httpx client that records responses through the SDK event hooks."""
        return httpx.Client(
            base_url=BASE_URL,
            transport=httpx.MockTransport(handler),
            event_hooks=build_sync_event_hooks(AuthConfig(static_token="otok_test")),
        )

    def test_schema_mismatch_is_classified_by_the_real_status(self) -> None:
        """A body the generated model cannot parse is classified from the recorded response."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(403, json={"error": {"code": "ACCESS_DENIED", "message": "No team access"}})

        with (
            self._client(handler) as client,
            pytest.raises(SupermetricsForbiddenError) as exc_info,
            api_error_handler(ENDPOINT),
        ):
            client.get("/v1/things")
            raise KeyError("data")

        error = exc_info.value
        assert error.status_code == 403
        assert error.error_code == "ACCESS_DENIED"
        assert error.message == "No team access"

    def test_successful_call_leaves_a_later_parse_failure_unclassified(self) -> None:
        """A 200 recorded by the hooks does not turn a later parse failure into an HTTP error."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"unexpected": "shape"})

        with (
            self._client(handler) as client,
            pytest.raises(SupermetricsAPIError) as exc_info,
            api_error_handler(ENDPOINT),
        ):
            client.get("/v1/things")
            raise KeyError("data")

        assert exc_info.value.status_code == 0

    def test_raise_for_status_inside_the_block_wins_over_the_record(self) -> None:
        """An explicit raise_for_status is translated directly from the httpx error."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="upstream exploded")

        with (
            self._client(handler) as client,
            pytest.raises(SupermetricsServerError) as exc_info,
            api_error_handler(ENDPOINT),
        ):
            client.get("/v1/things").raise_for_status()

        assert exc_info.value.status_code == 500
        assert exc_info.value.raw_response is not None


class TestRawResponseResolution:
    """`_raw_response_of` prefers an explicit response over the recorded one."""

    def test_explicit_response_is_used(self) -> None:
        """Test that a caller-supplied response wins over the transport record."""
        explicit = httpx.Response(418)
        recorded = httpx.Response(500)
        token = current_last_response.set(ResponseRecord.of(recorded))
        try:
            assert _raw_response_of(explicit) is explicit
        finally:
            current_last_response.reset(token)

    def test_recorded_response_is_used_when_none_supplied(self) -> None:
        """Test that the transport record fills in when the caller has no response."""
        recorded = httpx.Response(503)
        token = current_last_response.set(ResponseRecord.of(recorded))
        try:
            assert _raw_response_of(None) is recorded
        finally:
            current_last_response.reset(token)

    def test_none_when_nothing_was_recorded(self) -> None:
        """Test that no response is reported when the transport recorded nothing."""
        token = current_last_response.set(None)
        try:
            assert _raw_response_of(None) is None
        finally:
            current_last_response.reset(token)
