"""End-to-end tests for the `with_raw_response` accessor (Phase 1.3.1 / 1.3.2)."""

from __future__ import annotations

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.response import ApiResponse

from .conftest import LOGIN_GET_BODY, LOGINS_LIST_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e


class TestRawResponseSync:
    """The synchronous raw-response view exposes full transport metadata."""

    def test_returns_an_api_response_envelope(self, logins_server: MockAPIServer) -> None:
        """The parsed data is still there, wrapped in an envelope."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            response = client.with_raw_response.logins.list()

        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0].username == "user@example.com"

    def test_exposes_correlation_headers(self, api_server: MockAPIServer) -> None:
        """Span, request id, and Retry-After are read off the response headers."""
        api_server.route(
            "/ds/logins",
            ScriptedResponse(
                json_body=LOGINS_LIST_BODY,
                headers={"X-Span-Id": "a8f3b2c9e10d", "X-Request-Id": "req-1", "Retry-After": "5"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.logins.list()

        assert response.span_id == "a8f3b2c9e10d"
        assert response.request_id == "req-1"
        assert response.retry_after == 5

    def test_exposes_raw_and_json_bodies(self, logins_server: MockAPIServer) -> None:
        """Both the raw bytes and the decoded JSON are available."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            response = client.with_raw_response.logins.get("login_abc123")

        assert response.raw_body.startswith(b"{")
        assert response.json_body == LOGIN_GET_BODY
        assert response.request_url is not None
        assert response.request_url.endswith("/ds/login/login_abc123")

    def test_missing_headers_degrade_gracefully(self, logins_server: MockAPIServer) -> None:
        """Absent correlation headers read as None rather than raising."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            response = client.with_raw_response.logins.list()

        assert response.span_id is None
        assert response.request_id is None
        assert response.retry_after is None

    def test_per_request_overrides_still_apply(self, logins_server: MockAPIServer) -> None:
        """The mirrored methods keep the same signature, overrides included."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            response = client.with_raw_response.logins.list(auth_token="otok_raw", headers={"X-Span-Id": "raw-span"})

        assert response.status_code == 200
        assert logins_server.last_request.bearer_token == "otok_raw"
        assert logins_server.last_request.headers["x-span-id"] == "raw-span"

    def test_plain_calls_are_unaffected(self, logins_server: MockAPIServer) -> None:
        """Using the raw view does not change what the plain methods return."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            client.with_raw_response.logins.list()
            plain = client.logins.list()

        assert plain[0].username == "user@example.com"

    def test_errors_still_raise_through_the_raw_view(self, api_server: MockAPIServer) -> None:
        """Failures raise the normal exception rather than an error envelope."""
        from supermetrics.exceptions import SupermetricsNotFoundError

        api_server.route(
            "/ds/logins", ScriptedResponse(status=404, json_body={"error": {"code": "NOT_FOUND", "message": "x"}})
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError):
                client.with_raw_response.logins.list()

    def test_view_is_cached(self, logins_server: MockAPIServer) -> None:
        """Repeated access returns the same view object."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            assert client.with_raw_response is client.with_raw_response

    def test_every_resource_is_mirrored(self, logins_server: MockAPIServer) -> None:
        """The raw view covers the same resource set as the client."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            resources = {
                name for name, value in vars(client).items() if not name.startswith("_") and hasattr(value, "__class__")
            }
            mirrored = {name for name in vars(client.with_raw_response) if not name.startswith("_")}

        assert resources == mirrored


class TestRawResponseAsync:
    """The asynchronous raw-response view behaves identically."""

    @pytest.mark.asyncio
    async def test_returns_an_api_response_envelope(self, logins_server: MockAPIServer) -> None:
        """Awaiting a mirrored method yields the envelope."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=logins_server.base_url) as client:
            response = await client.with_raw_response.logins.get("login_abc123")

        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert response.data.login_id == "login_abc123"

    @pytest.mark.asyncio
    async def test_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """Headers and raw payload are captured on the async path too."""
        api_server.route(
            "/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, headers={"X-Span-Id": "async-span"})
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.logins.list()

        assert response.span_id == "async-span"
        assert response.json_body == LOGINS_LIST_BODY
