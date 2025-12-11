"""Unit tests for custom exception classes."""

import pytest

from supermetrics.exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsError,
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
        """Test that each exception type is distinct."""
        auth_error = AuthenticationError("test")
        validation_error = ValidationError("test")
        api_error = APIError("test")
        network_error = NetworkError("test")

        # Each type should only match itself
        assert isinstance(auth_error, AuthenticationError)
        assert not isinstance(auth_error, ValidationError)
        assert not isinstance(auth_error, APIError)
        assert not isinstance(auth_error, NetworkError)

        assert isinstance(validation_error, ValidationError)
        assert not isinstance(validation_error, AuthenticationError)

        assert isinstance(api_error, APIError)
        assert not isinstance(api_error, NetworkError)

        assert isinstance(network_error, NetworkError)
        assert not isinstance(network_error, APIError)
