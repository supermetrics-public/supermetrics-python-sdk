"""End-to-end tests for per-request overrides (Phase 1.2).

A single shared client must be able to serve callers that each bring their own
credential, tracing headers, and timeout budget, without losing its connection
pool. These tests assert on what the server received, and on real timeouts
firing against a genuinely slow endpoint.
"""

from __future__ import annotations

import httpx
import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics._transport import current_auth_token, current_request_headers
from supermetrics.exceptions import NetworkError

from .conftest import LOGINS_LIST_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e


class TestPerRequestAuthToken:
    """`auth_token=` overrides the client credential for one call only."""

    def test_auth_token_overrides_client_credential(self, logins_server: MockAPIServer) -> None:
        """The override is used for that call and nothing else changes."""
        with SupermetricsClient(api_key="api_client_level", base_url=logins_server.base_url) as client:
            client.logins.list()
            client.logins.list(auth_token="otok_per_request")
            client.logins.list()

        assert [r.bearer_token for r in logins_server.requests] == [
            "api_client_level",
            "otok_per_request",
            "api_client_level",
        ]

    def test_auth_token_overrides_a_token_provider(self, logins_server: MockAPIServer) -> None:
        """An explicit override wins over the client's dynamic provider."""
        with SupermetricsClient(token_provider=lambda: "otok_from_provider", base_url=logins_server.base_url) as client:
            client.logins.list(auth_token="otok_explicit")
            client.logins.list()

        assert [r.bearer_token for r in logins_server.requests] == ["otok_explicit", "otok_from_provider"]

    @pytest.mark.asyncio
    async def test_auth_token_override_on_async_client(self, logins_server: MockAPIServer) -> None:
        """The async client honours the same override."""
        async with SupermetricsAsyncClient(api_key="api_async", base_url=logins_server.base_url) as client:
            await client.logins.list(auth_token="otok_async_override")
            await client.logins.list()

        assert [r.bearer_token for r in logins_server.requests] == ["otok_async_override", "api_async"]

    def test_override_forwarded_through_a_delegating_method(self, logins_server: MockAPIServer) -> None:
        """`get_by_username` delegates to `list`, and must forward the override."""
        with SupermetricsClient(api_key="api_base", base_url=logins_server.base_url) as client:
            login = client.logins.get_by_username("user@example.com", auth_token="otok_delegated")

        assert login.username == "user@example.com"
        assert logins_server.last_request.bearer_token == "otok_delegated"


class TestPerRequestHeaders:
    """`headers=` injects tracing and idempotency headers for one call."""

    def test_headers_reach_the_server(self, logins_server: MockAPIServer) -> None:
        """Arbitrary correlation headers are sent on the wire."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            client.logins.list(
                headers={
                    "X-Span-Id": "span-abc",
                    "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
                    "Idempotency-Key": "idem-42",
                    "X-Team-ID": "9001",
                }
            )

        received = logins_server.last_request.headers
        assert received["x-span-id"] == "span-abc"
        assert received["traceparent"] == "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
        assert received["idempotency-key"] == "idem-42"
        assert received["x-team-id"] == "9001"

    def test_headers_do_not_leak_into_later_requests(self, logins_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            client.logins.list(headers={"X-Span-Id": "only-once"})
            client.logins.list()

        assert logins_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in logins_server.requests[1].headers

    def test_header_merge_is_case_insensitive(self, logins_server: MockAPIServer) -> None:
        """A lower-case override replaces a differently-cased client header."""
        with SupermetricsClient(
            api_key="api_k", base_url=logins_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            client.logins.list()
            client.logins.list(headers={"x-team-id": "request-level"})

        assert logins_server.requests[0].headers["x-team-id"] == "client-level"
        assert logins_server.requests[1].headers["x-team-id"] == "request-level"

    def test_per_request_headers_outrank_client_custom_headers(self, logins_server: MockAPIServer) -> None:
        """Request headers take the highest precedence in the merge order."""
        with SupermetricsClient(
            api_key="api_k", base_url=logins_server.base_url, custom_headers={"X-Custom": "from-client"}
        ) as client:
            client.logins.list(headers={"X-Custom": "from-request"})

        assert logins_server.last_request.headers["x-custom"] == "from-request"

    def test_authorization_can_be_forced_through_headers(self, logins_server: MockAPIServer) -> None:
        """Per-request headers are applied after auth, so they can override it."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            client.logins.list(headers={"Authorization": "Bearer raw_escape_hatch"})

        assert logins_server.last_request.authorization == "Bearer raw_escape_hatch"

    def test_client_defaults_survive_a_per_request_override(self, logins_server: MockAPIServer) -> None:
        """Injecting one header does not drop the SDK's User-Agent."""
        with SupermetricsClient(api_key="api_k", base_url=logins_server.base_url) as client:
            client.logins.list(headers={"X-Span-Id": "s"})

        assert logins_server.last_request.headers["user-agent"].startswith("supermetrics-sdk/")

    @pytest.mark.asyncio
    async def test_headers_on_async_client(self, logins_server: MockAPIServer) -> None:
        """The async client injects per-request headers identically."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=logins_server.base_url) as client:
            await client.logins.list(headers={"X-Span-Id": "async-span"})

        assert logins_server.last_request.headers["x-span-id"] == "async-span"


class TestPerRequestTimeout:
    """`timeout=` overrides the client timeout for one call, for real."""

    def test_short_timeout_fires_against_a_slow_endpoint(self, api_server: MockAPIServer) -> None:
        """A 0.3s override times out an endpoint that takes 1.5s."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=1.5))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.logins.list(timeout=0.3)

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout call, the client default applies again."""
        api_server.route(
            "/ds/logins",
            ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.8),
            ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.8),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.logins.list(timeout=0.2)
            # The client-level 10s timeout is back in force, so this succeeds.
            assert client.logins.list() == client.logins.list()

    def test_httpx_timeout_object_is_accepted(self, api_server: MockAPIServer) -> None:
        """An httpx.Timeout instance works as well as a float."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=1.0))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.logins.list(timeout=httpx.Timeout(0.25))

    def test_generous_override_beats_a_tight_client_timeout(self, api_server: MockAPIServer) -> None:
        """A long-running call can opt out of a tight client-level timeout."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=0.2) as client:
            with pytest.raises(NetworkError):
                client.logins.list()
            assert len(client.logins.list(timeout=10.0)) == 1

    @pytest.mark.asyncio
    async def test_timeout_override_on_async_client(self, api_server: MockAPIServer) -> None:
        """The async client enforces per-request timeouts too."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=1.5))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.logins.list(timeout=0.3)


class TestAmbientContextPropagation:
    """Ambient context variables propagate into calls that do not override them."""

    def test_ambient_auth_token_is_used(self, logins_server: MockAPIServer) -> None:
        """A token set by surrounding middleware is picked up automatically."""
        token = current_auth_token.set("otok_ambient")
        try:
            with SupermetricsClient(api_key="api_client", base_url=logins_server.base_url) as client:
                client.logins.list()
        finally:
            current_auth_token.reset(token)

        assert logins_server.last_request.bearer_token == "otok_ambient"

    def test_explicit_argument_beats_ambient_value(self, logins_server: MockAPIServer) -> None:
        """An explicit auth_token overrides the ambient one."""
        token = current_auth_token.set("otok_ambient")
        try:
            with SupermetricsClient(api_key="api_client", base_url=logins_server.base_url) as client:
                client.logins.list(auth_token="otok_explicit")
        finally:
            current_auth_token.reset(token)

        assert logins_server.last_request.bearer_token == "otok_explicit"

    def test_ambient_headers_are_applied(self, logins_server: MockAPIServer) -> None:
        """Ambient tracing headers reach the wire without being passed explicitly."""
        token = current_request_headers.set({"X-Span-Id": "ambient-span"})
        try:
            with SupermetricsClient(api_key="api_client", base_url=logins_server.base_url) as client:
                client.logins.list()
        finally:
            current_request_headers.reset(token)

        assert logins_server.last_request.headers["x-span-id"] == "ambient-span"
