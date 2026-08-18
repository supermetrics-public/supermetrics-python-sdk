"""Unit tests for custom exception classes."""

import httpx
import pytest

from supermetrics.exceptions import (
    APIError,
    AuthenticationError,
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
    ValidationError,
)


class TestSupermetricsError:
    """Test suite for SupermetricsError base exception."""

    def test_base_exception_initialization(self) -> None:
        """Test SupermetricsError can be initialized with message only."""
        error = SupermetricsError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.status_code is None
        assert error.endpoint is None
        assert error.response_body is None

    def test_base_exception_with_all_attributes(self) -> None:
        """Test SupermetricsError with all optional attributes."""
        error = SupermetricsError(
            message="Complete error",
            status_code=500,
            endpoint="/api/test",
            response_body='{"error": "details"}',
        )

        assert error.message == "Complete error"
        assert error.status_code == 500
        assert error.endpoint == "/api/test"
        assert error.response_body == '{"error": "details"}'

    def test_base_exception_is_exception(self) -> None:
        """Test that SupermetricsError is a proper Exception."""
        error = SupermetricsError("test")
        assert isinstance(error, Exception)


class TestAuthenticationError:
    """Test suite for AuthenticationError (HTTP 401)."""

    def test_authentication_error_inherits_from_base(self) -> None:
        """Test AuthenticationError inherits from SupermetricsError."""
        error = AuthenticationError("Invalid API key")
        assert isinstance(error, SupermetricsError)
        assert isinstance(error, Exception)

    def test_authentication_error_with_context(self) -> None:
        """Test AuthenticationError with full HTTP context."""
        error = AuthenticationError(
            message="Invalid or expired API key",
            status_code=401,
            endpoint="https://api.supermetrics.com/login_links",
            response_body='{"error": "Unauthorized"}',
        )

        assert error.message == "Invalid or expired API key"
        assert error.status_code == 401
        assert error.endpoint == "https://api.supermetrics.com/login_links"
        assert error.response_body == '{"error": "Unauthorized"}'

    def test_authentication_error_can_be_caught_as_base(self) -> None:
        """Test AuthenticationError can be caught as SupermetricsError."""
        with pytest.raises(SupermetricsError) as exc_info:
            raise AuthenticationError("Test")

        assert isinstance(exc_info.value, AuthenticationError)


class TestValidationError:
    """Test suite for ValidationError (HTTP 400)."""

    def test_validation_error_inherits_from_base(self) -> None:
        """Test ValidationError inherits from SupermetricsError."""
        error = ValidationError("Invalid parameters")
        assert isinstance(error, SupermetricsError)
        assert isinstance(error, Exception)

    def test_validation_error_with_context(self) -> None:
        """Test ValidationError with parameter validation details."""
        error = ValidationError(
            message="Invalid request parameters: ds_id is required",
            status_code=400,
            endpoint="https://api.supermetrics.com/login_links",
            response_body='{"error": "ds_id is required"}',
        )

        assert error.message == "Invalid request parameters: ds_id is required"
        assert error.status_code == 400
        assert "ds_id is required" in error.message

    def test_validation_error_can_be_caught_as_base(self) -> None:
        """Test ValidationError can be caught as SupermetricsError."""
        with pytest.raises(SupermetricsError) as exc_info:
            raise ValidationError("Test")

        assert isinstance(exc_info.value, ValidationError)


class TestAPIError:
    """Test suite for APIError (HTTP 404, 5xx, other errors)."""

    def test_api_error_inherits_from_base(self) -> None:
        """Test APIError inherits from SupermetricsError."""
        error = APIError("Server error")
        assert isinstance(error, SupermetricsError)
        assert isinstance(error, Exception)

    def test_api_error_404_not_found(self) -> None:
        """Test APIError for 404 Not Found responses."""
        error = APIError(
            message="Login link not found",
            status_code=404,
            endpoint="https://api.supermetrics.com/login_links/invalid-id",
            response_body='{"error": "Not found"}',
        )

        assert error.status_code == 404
        assert "not found" in error.message.lower()

    def test_api_error_500_server_error(self) -> None:
        """Test APIError for 500 Internal Server Error responses."""
        error = APIError(
            message="Supermetrics API error: Internal server error",
            status_code=500,
            endpoint="https://api.supermetrics.com/queries",
            response_body='{"error": "Internal server error"}',
        )

        assert error.status_code == 500
        assert "server error" in error.message.lower()

    def test_api_error_503_service_unavailable(self) -> None:
        """Test APIError for 503 Service Unavailable responses."""
        error = APIError(
            message="Supermetrics API error: Service unavailable",
            status_code=503,
            endpoint="https://api.supermetrics.com/accounts",
        )

        assert error.status_code == 503

    def test_api_error_can_be_caught_as_base(self) -> None:
        """Test APIError can be caught as SupermetricsError."""
        with pytest.raises(SupermetricsError) as exc_info:
            raise APIError("Test", status_code=500)

        assert isinstance(exc_info.value, APIError)


class TestNetworkError:
    """Test suite for NetworkError (network-level failures)."""

    def test_network_error_inherits_from_base(self) -> None:
        """Test NetworkError inherits from SupermetricsError."""
        error = NetworkError("Connection timeout")
        assert isinstance(error, SupermetricsError)
        assert isinstance(error, Exception)

    def test_network_error_timeout(self) -> None:
        """Test NetworkError for timeout scenarios."""
        error = NetworkError(
            message="Network error: Connection timeout",
            endpoint="https://api.supermetrics.com/login_links",
        )

        assert error.message == "Network error: Connection timeout"
        assert error.endpoint == "https://api.supermetrics.com/login_links"
        # Network errors don't have HTTP status codes
        assert error.status_code is None

    def test_network_error_connection_refused(self) -> None:
        """Test NetworkError for connection refused scenarios."""
        error = NetworkError(
            message="Network error: Connection refused",
            endpoint="https://api.supermetrics.com",
        )

        assert "Connection refused" in error.message
        assert error.status_code is None

    def test_network_error_dns_failure(self) -> None:
        """Test NetworkError for DNS resolution failures."""
        error = NetworkError(
            message="Network error: Name or service not known",
            endpoint="https://invalid-domain.supermetrics.com",
        )

        assert error.status_code is None
        assert error.endpoint is not None

    def test_network_error_can_be_caught_as_base(self) -> None:
        """Test NetworkError can be caught as SupermetricsError."""
        with pytest.raises(SupermetricsError) as exc_info:
            raise NetworkError("Test")

        assert isinstance(exc_info.value, NetworkError)


class TestExceptionHierarchy:
    """Test the overall exception hierarchy and inheritance."""

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test all custom exceptions inherit from SupermetricsError."""
        exceptions = [
            AuthenticationError("test"),
            ValidationError("test"),
            APIError("test"),
            NetworkError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, SupermetricsError)
            assert isinstance(exc, Exception)

    def test_catch_all_sdk_exceptions(self) -> None:
        """Test that all SDK exceptions can be caught with SupermetricsError."""
        exception_types = [
            AuthenticationError,
            ValidationError,
            APIError,
            NetworkError,
        ]

        for exc_type in exception_types:
            with pytest.raises(SupermetricsError):
                raise exc_type("test message")

    def test_exceptions_are_distinct_types(self) -> None:
        """Test that sibling exception types do not match each other."""
        auth_error = AuthenticationError("test")
        validation_error = ValidationError("test")
        api_error = APIError("test")
        network_error = NetworkError("test")

        # Siblings never match each other...
        assert isinstance(auth_error, AuthenticationError)
        assert not isinstance(auth_error, ValidationError)
        assert not isinstance(auth_error, NetworkError)

        assert isinstance(validation_error, ValidationError)
        assert not isinstance(validation_error, AuthenticationError)

        assert isinstance(api_error, APIError)
        assert not isinstance(api_error, NetworkError)

        # ...but NetworkError is not an HTTP error, so it is never an APIError.
        assert isinstance(network_error, NetworkError)
        assert not isinstance(network_error, APIError)

        # A bare APIError is not one of the specific HTTP subclasses.
        assert not isinstance(api_error, AuthenticationError)
        assert not isinstance(api_error, ValidationError)

    def test_http_errors_are_subclasses_of_api_error(self) -> None:
        """Every HTTP-level error can be caught with a single except APIError."""
        http_errors = [
            SupermetricsAuthError("401"),
            SupermetricsForbiddenError("403"),
            SupermetricsNotFoundError("404"),
            SupermetricsValidationError("422"),
            SupermetricsRateLimitError("429"),
            SupermetricsServerError("500"),
        ]

        for error in http_errors:
            assert isinstance(error, SupermetricsAPIError)
            assert isinstance(error, APIError)
            assert isinstance(error, SupermetricsError)

    def test_legacy_names_are_aliases_of_the_new_names(self) -> None:
        """The pre-existing public names still resolve to the same classes."""
        assert APIError is SupermetricsAPIError
        assert AuthenticationError is SupermetricsAuthError
        assert ValidationError is SupermetricsValidationError

    def test_client_error_is_also_a_value_error(self) -> None:
        """Configuration errors stay catchable as ValueError."""
        error = SupermetricsClientError("bad config")

        assert isinstance(error, SupermetricsError)
        assert isinstance(error, ValueError)
        assert not isinstance(error, SupermetricsAPIError)


class TestApiErrorTransportContext:
    """SupermetricsAPIError preserves the full transport context."""

    def test_all_transport_fields_are_stored(self) -> None:
        """Headers, error code, details and raw response are retained."""
        response = httpx.Response(429, headers={"Retry-After": "30"})
        error = SupermetricsRateLimitError(
            "Rate limit exceeded",
            status_code=429,
            endpoint="/v1/teams/1/transfers",
            response_body="throttled",
            headers=response.headers,
            error_code="TOO_MANY_REQUESTS",
            details={"limit": 100},
            raw_response=response,
        )

        assert error.status_code == 429
        assert error.endpoint == "/v1/teams/1/transfers"
        assert error.response_body == "throttled"
        assert error.error_code == "TOO_MANY_REQUESTS"
        assert error.error_message == "Rate limit exceeded"
        assert error.details == {"limit": 100}
        assert error.raw_response is response

    def test_retry_after_is_parsed_as_an_integer(self) -> None:
        """A numeric Retry-After header is exposed as an int."""
        error = SupermetricsRateLimitError("x", headers=httpx.Headers({"Retry-After": "45"}))
        assert error.retry_after == 45

    def test_retry_after_is_none_for_a_http_date(self) -> None:
        """A non-numeric Retry-After is reported as None rather than crashing."""
        error = SupermetricsRateLimitError("x", headers=httpx.Headers({"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}))
        assert error.retry_after is None

    def test_correlation_ids_are_read_from_headers(self) -> None:
        """Request and span identifiers are surfaced as properties."""
        error = SupermetricsServerError("x", headers=httpx.Headers({"X-Request-Id": "r1", "X-Span-Id": "s1"}))

        assert error.request_id == "r1"
        assert error.span_id == "s1"

    def test_properties_degrade_to_none_without_headers(self) -> None:
        """An error raised with no headers reports None rather than raising."""
        error = SupermetricsAPIError("x")

        assert error.headers is None
        assert error.retry_after is None
        assert error.request_id is None
        assert error.span_id is None


class TestRetryAfterEdgeCases:
    """retry_after only reports a value it can actually return as an integer."""

    def test_absent_header_is_none(self) -> None:
        """Test that an error whose response carried no Retry-After reports None."""
        error = SupermetricsRateLimitError("throttled", headers=httpx.Headers({"X-Other": "1"}))
        assert error.retry_after is None

    def test_unicode_digit_int_cannot_parse_is_none(self) -> None:
        """Test that a digit-like character int() rejects reads as None, not ValueError.

        ``str.isdigit()`` is True for characters such as the superscript two that
        ``int()`` then refuses, so the property gates on ``str.isdecimal()``.
        """
        headers = httpx.Headers([(b"retry-after", b"\xc2\xb2")])
        error = SupermetricsRateLimitError("throttled", headers=headers)
        assert error.retry_after is None

    def test_surrounding_whitespace_is_tolerated(self) -> None:
        """Test that a padded numeric value is still parsed."""
        error = SupermetricsRateLimitError("throttled", headers=httpx.Headers({"Retry-After": "  30  "}))
        assert error.retry_after == 30
