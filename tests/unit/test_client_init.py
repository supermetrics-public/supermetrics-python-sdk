"""Unit tests for client initialization."""

import sys

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.__version__ import __version__


class TestSupermetricsClientInit:
    """Tests for SupermetricsClient initialization."""

    def test_client_initialization_with_api_key(self, test_api_key):
        """Test that client initializes successfully with an API key."""
        client = SupermetricsClient(api_key=test_api_key)

        assert client._api_key == test_api_key
        assert client._client is not None

    def test_client_has_authorization_header(self, test_api_key):
        """Test that client includes Authorization bearer token in headers."""
        client = SupermetricsClient(api_key=test_api_key)

        # Access the httpx client to check headers
        httpx_client = client._client.get_httpx_client()
        assert "Authorization" in httpx_client.headers
        assert httpx_client.headers["Authorization"] == f"Bearer {test_api_key}"

    def test_client_has_default_user_agent(self, test_api_key):
        """Test that client includes default User-Agent header."""
        client = SupermetricsClient(api_key=test_api_key)

        httpx_client = client._client.get_httpx_client()
        assert "User-Agent" in httpx_client.headers

        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        expected_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"
        assert httpx_client.headers["User-Agent"] == expected_user_agent

    def test_client_with_custom_user_agent(self, test_api_key):
        """Test that client accepts custom User-Agent header."""
        custom_ua = "my-custom-client/1.0"
        client = SupermetricsClient(api_key=test_api_key, user_agent=custom_ua)

        httpx_client = client._client.get_httpx_client()
        assert httpx_client.headers["User-Agent"] == custom_ua

    def test_client_with_custom_headers(self, test_api_key):
        """Test that custom headers are merged with defaults."""
        custom_headers = {
            "X-Custom-Header": "custom-value",
            "X-Another-Header": "another-value",
        }
        client = SupermetricsClient(api_key=test_api_key, custom_headers=custom_headers)

        httpx_client = client._client.get_httpx_client()
        assert httpx_client.headers["X-Custom-Header"] == "custom-value"
        assert httpx_client.headers["X-Another-Header"] == "another-value"
        # Default headers should still be present
        assert httpx_client.headers["Authorization"] == f"Bearer {test_api_key}"

    def test_client_custom_headers_override_defaults(self, test_api_key):
        """Test that custom headers override default headers."""
        custom_headers = {
            "User-Agent": "override-agent/1.0",
        }
        client = SupermetricsClient(api_key=test_api_key, custom_headers=custom_headers)

        httpx_client = client._client.get_httpx_client()
        assert httpx_client.headers["User-Agent"] == "override-agent/1.0"

    def test_client_context_manager(self, test_api_key):
        """Test that client works as a context manager."""
        with SupermetricsClient(api_key=test_api_key) as client:
            assert client is not None
            assert client._client is not None
        # Client should be closed after context

    def test_client_close(self, test_api_key):
        """Test that client can be closed properly."""
        client = SupermetricsClient(api_key=test_api_key)
        # Should not raise an exception
        client.close()

    def test_client_with_custom_base_url(self, test_api_key):
        """Test that client accepts custom base URL."""
        custom_base_url = "https://test.example.com"
        client = SupermetricsClient(api_key=test_api_key, base_url=custom_base_url)

        httpx_client = client._client.get_httpx_client()
        assert str(httpx_client.base_url) == custom_base_url

    def test_client_with_custom_timeout(self, test_api_key):
        """Test that client accepts custom timeout."""
        custom_timeout = 60.0
        client = SupermetricsClient(api_key=test_api_key, timeout=custom_timeout)

        httpx_client = client._client.get_httpx_client()
        assert httpx_client.timeout.read == custom_timeout


class TestSupermetricsAsyncClientInit:
    """Tests for SupermetricsAsyncClient initialization."""

    def test_async_client_initialization_with_api_key(self, test_api_key):
        """Test that async client initializes successfully with an API key."""
        client = SupermetricsAsyncClient(api_key=test_api_key)

        assert client._api_key == test_api_key
        assert client._client is not None

    def test_async_client_has_authorization_header(self, test_api_key):
        """Test that async client includes Authorization bearer token in headers."""
        client = SupermetricsAsyncClient(api_key=test_api_key)

        # Access the httpx client to check headers
        httpx_client = client._client.get_async_httpx_client()
        assert "Authorization" in httpx_client.headers
        assert httpx_client.headers["Authorization"] == f"Bearer {test_api_key}"

    def test_async_client_has_default_user_agent(self, test_api_key):
        """Test that async client includes default User-Agent header."""
        client = SupermetricsAsyncClient(api_key=test_api_key)

        httpx_client = client._client.get_async_httpx_client()
        assert "User-Agent" in httpx_client.headers

        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        expected_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"
        assert httpx_client.headers["User-Agent"] == expected_user_agent

    def test_async_client_with_custom_headers(self, test_api_key):
        """Test that custom headers are merged in async client."""
        custom_headers = {
            "X-Custom-Header": "custom-value",
        }
        client = SupermetricsAsyncClient(api_key=test_api_key, custom_headers=custom_headers)

        httpx_client = client._client.get_async_httpx_client()
        assert httpx_client.headers["X-Custom-Header"] == "custom-value"
        assert httpx_client.headers["Authorization"] == f"Bearer {test_api_key}"

    @pytest.mark.asyncio
    async def test_async_client_context_manager(self, test_api_key):
        """Test that async client works as an async context manager."""
        async with SupermetricsAsyncClient(api_key=test_api_key) as client:
            assert client is not None
            assert client._client is not None
        # Client should be closed after context

    @pytest.mark.asyncio
    async def test_async_client_close(self, test_api_key):
        """Test that async client can be closed properly."""
        client = SupermetricsAsyncClient(api_key=test_api_key)
        # Should not raise an exception
        await client.close()


class TestPublicAPIExports:
    """Test that public API exports work correctly."""

    def test_supermetrics_client_import(self):
        """Test that SupermetricsClient is importable from supermetrics."""
        from supermetrics import SupermetricsClient as Client

        assert Client is not None

    def test_supermetrics_async_client_import(self):
        """Test that SupermetricsAsyncClient is importable from supermetrics."""
        from supermetrics import SupermetricsAsyncClient as AsyncClient

        assert AsyncClient is not None

    def test_version_import(self):
        """Test that __version__ is importable from supermetrics."""
        from supermetrics import __version__ as version

        assert version is not None
        assert isinstance(version, str)
