"""End-to-end tests for the error taxonomy (Phase 1.3.3).

Each test drives a real HTTP response with a real status code and real headers
through the whole stack, and asserts on the exception class, the preserved
transport metadata, and the backwards-compatible aliases.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
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

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e


def _error_body(code: str, message: str) -> dict[str, object]:
    """Build an upstream error payload in the Supermetrics envelope shape."""
    return {"error": {"code": code, "message": message}}


class TestStatusCodeMapping:
    """Each HTTP status maps to its dedicated exception subclass."""

    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (401, SupermetricsAuthError),
            (403, SupermetricsForbiddenError),
            (404, SupermetricsNotFoundError),
            (422, SupermetricsValidationError),
            (429, SupermetricsRateLimitError),
            (500, SupermetricsServerError),
            (503, SupermetricsServerError),
        ],
    )
    def test_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, expected: type[SupermetricsAPIError]
    ) -> None:
        """The raised type matches the status, and carries it through."""
        api_server.route("/ds/logins", ScriptedResponse(status=status, json_body=_error_body("ERR", "boom")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.logins.list()

        assert exc_info.value.status_code == status
        assert isinstance(exc_info.value, SupermetricsAPIError)
        assert isinstance(exc_info.value, SupermetricsError)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (401, SupermetricsAuthError),
            (403, SupermetricsForbiddenError),
            (404, SupermetricsNotFoundError),
            (429, SupermetricsRateLimitError),
            (500, SupermetricsServerError),
        ],
    )
    async def test_status_maps_to_exception_async(
        self, api_server: MockAPIServer, status: int, expected: type[SupermetricsAPIError]
    ) -> None:
        """The async path produces the identical taxonomy."""
        api_server.route("/ds/logins", ScriptedResponse(status=status, json_body=_error_body("ERR", "boom")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.logins.list()

        assert exc_info.value.status_code == status


class TestTransportMetadataOnErrors:
    """Errors preserve headers, bodies, and upstream codes."""

    def test_rate_limit_exposes_retry_after(self, api_server: MockAPIServer) -> None:
        """A 429 surfaces Retry-After as an integer for backoff logic."""
        api_server.route(
            "/ds/logins",
            ScriptedResponse(
                status=429,
                json_body=_error_body("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "42", "X-RateLimit-Remaining": "0"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.logins.list()

        error = exc_info.value
        assert error.retry_after == 42
        assert error.headers is not None
        assert error.headers["X-RateLimit-Remaining"] == "0"

    def test_error_carries_correlation_headers(self, api_server: MockAPIServer) -> None:
        """Request and span identifiers survive onto the exception."""
        api_server.route(
            "/ds/logins",
            ScriptedResponse(
                status=500,
                json_body=_error_body("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-77", "X-Span-Id": "span-77"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.logins.list()

        assert exc_info.value.request_id == "req-77"
        assert exc_info.value.span_id == "span-77"

    def test_auth_error_carries_oauth_error_code(self, api_server: MockAPIServer) -> None:
        """A 401 exposes the upstream OAuth code so callers can refresh a token."""
        api_server.route(
            "/ds/logins",
            ScriptedResponse(status=401, json_body=_error_body("ACCESS_TOKEN_INVALID", "token expired")),
        )

        with SupermetricsClient(bearer_token="otok_stale", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                client.logins.list()

        assert exc_info.value.error_code == "ACCESS_TOKEN_INVALID"
        assert exc_info.value.status_code == 401

    def test_refresh_and_retry_flow(self, api_server: MockAPIServer) -> None:
        """A caller can catch the auth error, rotate the token, and succeed."""
        from .conftest import LOGINS_LIST_BODY

        api_server.route(
            "/ds/logins",
            ScriptedResponse(status=401, json_body=_error_body("ACCESS_TOKEN_INVALID", "expired")),
            ScriptedResponse(json_body=LOGINS_LIST_BODY),
        )
        tokens = iter(["otok_expired", "otok_fresh"])
        current = {"token": next(tokens)}

        with SupermetricsClient(token_provider=lambda: current["token"], base_url=api_server.base_url) as client:
            try:
                client.logins.list()
            except SupermetricsAuthError as error:
                assert error.error_code == "ACCESS_TOKEN_INVALID"
                current["token"] = next(tokens)
                logins = client.logins.list()

        assert len(logins) == 1
        assert [r.bearer_token for r in api_server.requests] == ["otok_expired", "otok_fresh"]

    def test_endpoint_is_recorded_on_the_error(self, api_server: MockAPIServer) -> None:
        """The failing endpoint is attached for logging."""
        api_server.route("/ds/logins", ScriptedResponse(status=403, json_body=_error_body("FORBIDDEN", "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsForbiddenError) as exc_info:
                client.logins.list()

        assert exc_info.value.endpoint == "/ds/logins"


class TestBackwardsCompatibleAliases:
    """Legacy exception names keep working for existing user code."""

    def test_auth_error_is_catchable_as_authentication_error(self, api_server: MockAPIServer) -> None:
        """`AuthenticationError` still catches a 401."""
        api_server.route("/ds/logins", ScriptedResponse(status=401, json_body=_error_body("UNAUTHORIZED", "no")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(AuthenticationError):
                client.logins.list()

    def test_not_found_is_catchable_as_api_error(self, api_server: MockAPIServer) -> None:
        """`APIError` still catches a 404."""
        api_server.route("/ds/logins", ScriptedResponse(status=404, json_body=_error_body("NOT_FOUND", "gone")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(APIError):
                client.logins.list()

    def test_validation_error_alias(self, api_server: MockAPIServer) -> None:
        """`ValidationError` still catches a 422."""
        api_server.route("/ds/logins", ScriptedResponse(status=422, json_body=_error_body("VALIDATION_ERROR", "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(ValidationError):
                client.logins.list()


class TestNetworkErrors:
    """Transport failures are distinct from HTTP failures."""

    def test_connection_refused_is_a_network_error(self) -> None:
        """An unreachable server produces NetworkError, not an APIError."""
        # Port 1 on loopback is reserved and refuses connections.
        with SupermetricsClient(api_key="api_k", base_url="http://127.0.0.1:1", timeout=2.0) as client:
            with pytest.raises(NetworkError) as exc_info:
                client.logins.list()

        assert exc_info.value.status_code is None
        assert not isinstance(exc_info.value, SupermetricsAPIError)

    def test_timeout_is_a_network_error(self, api_server: MockAPIServer) -> None:
        """A server that never answers in time produces NetworkError."""
        from .conftest import LOGINS_LIST_BODY

        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=1.5))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=0.3) as client:
            with pytest.raises(NetworkError):
                client.logins.list()


class TestParsedOnlyEndpointErrors:
    """Resources that use the parsed-only generated wrappers keep their metadata.

    Several adapters (connector builder, its logs and its secrets) call the
    generated ``sync()``/``asyncio()`` wrappers, which hand back a parsed model
    rather than a transport response. Those call sites cannot pass response
    headers explicitly, so the SDK falls back to the transport metadata recorded
    for the request. Without that fallback these errors would silently lose
    ``Retry-After`` and the correlation identifiers.
    """

    ENDPOINT = "/v1/teams/42/connector_builder/connectors/conn_1/logs"

    def _error_envelope(self, code: str, message: str) -> dict[str, object]:
        """Build the generated ErrorResponse envelope, including its meta block."""
        return {"meta": {"request_id": "req-parsed"}, "error": {"code": code, "message": message}}

    def test_headers_survive_the_parsed_only_path(self, api_server: MockAPIServer) -> None:
        """A 429 from a parsed-only endpoint still exposes Retry-After."""
        api_server.route(
            self.ENDPOINT,
            ScriptedResponse(
                status=429,
                json_body=self._error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "17", "X-Request-Id": "req-parsed"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.connector_builder_logs.list(team_id=42, connector_identifier="conn_1")

        error = exc_info.value
        assert error.retry_after == 17
        assert error.request_id == "req-parsed"
        assert error.error_code == "TOO_MANY_REQUESTS"

    def test_upstream_code_maps_to_the_right_subclass(self, api_server: MockAPIServer) -> None:
        """A NOT_FOUND envelope becomes SupermetricsNotFoundError."""
        api_server.route(
            self.ENDPOINT,
            ScriptedResponse(status=404, json_body=self._error_envelope("NOT_FOUND", "no such connector")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.connector_builder_logs.list(team_id=42, connector_identifier="conn_1")

        assert exc_info.value.error_code == "NOT_FOUND"

    def test_per_request_overrides_reach_a_parsed_only_endpoint(self, api_server: MockAPIServer) -> None:
        """The overrides work on these adapters too, not just the detailed ones."""
        api_server.route(self.ENDPOINT, ScriptedResponse(json_body={"meta": {"request_id": "r"}, "logs": []}))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_logs.list(
                team_id=42,
                connector_identifier="conn_1",
                auth_token="otok_parsed",
                headers={"X-Span-Id": "parsed-span"},
            )

        assert api_server.last_request.bearer_token == "otok_parsed"
        assert api_server.last_request.headers["x-span-id"] == "parsed-span"


class TestCredentialsNeverReachAnErrorMessage:
    """A malformed credential must fail cleanly without echoing the secret.

    The HTTP layer quotes the whole offending header when it refuses to send it,
    so a credential containing an illegal byte would otherwise land verbatim in an
    exception message and from there in the caller's logs. The SDK rejects such a
    credential itself, and redacts any bearer value that still turns up in
    transport error text.
    """

    MALFORMED = [
        pytest.param("otok_SUPER_SECRET\x00x", id="null-byte"),
        pytest.param("otok_SUPER_SECRET\nwrapped", id="newline"),
        pytest.param("otok_SUPER_SECRET\r\nwrapped", id="crlf"),
        pytest.param("otok_SUPER_SECRET\u65e5", id="non-ascii"),
        pytest.param("otok\u2013SUPER_SECRET", id="en-dash"),
    ]

    @pytest.mark.parametrize("credential", MALFORMED)
    def test_malformed_static_credential_is_rejected_without_echoing_it(self, credential: str) -> None:
        """A malformed constructor credential fails locally and is not quoted back."""
        with pytest.raises(SupermetricsClientError) as exc_info:
            SupermetricsClient(bearer_token=credential, base_url="http://127.0.0.1:1")

        assert "SUPER_SECRET" not in str(exc_info.value)

    @pytest.mark.parametrize("credential", MALFORMED)
    def test_malformed_per_request_token_is_rejected_without_echoing_it(
        self, logins_server: MockAPIServer, credential: str
    ) -> None:
        """A malformed per-request override fails the same way, before sending."""
        with SupermetricsClient(api_key="api_ok", base_url=logins_server.base_url) as client:
            with pytest.raises(SupermetricsClientError) as exc_info:
                client.logins.list(auth_token=credential)

        assert "SUPER_SECRET" not in str(exc_info.value)
        assert logins_server.requests == []

    @pytest.mark.asyncio
    async def test_malformed_credential_is_rejected_on_the_async_client(self, logins_server: MockAPIServer) -> None:
        """The async client applies the identical rule."""
        async with SupermetricsAsyncClient(api_key="api_ok", base_url=logins_server.base_url) as client:
            with pytest.raises(SupermetricsClientError) as exc_info:
                await client.logins.list(auth_token="otok_SUPER_SECRET\nwrapped")

        assert "SUPER_SECRET" not in str(exc_info.value)

    def test_a_valid_credential_is_still_sent_unchanged(self, logins_server: MockAPIServer) -> None:
        """The validation does not disturb ordinary tokens."""
        with SupermetricsClient(bearer_token="  otok_perfectly_fine  ", base_url=logins_server.base_url) as client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == "otok_perfectly_fine"

    def test_transport_error_text_still_redacts_a_bearer_value(self) -> None:
        """Defence in depth: any bearer value in transport error text is redacted."""
        from supermetrics.resources._error_handlers import _redact_credentials

        redacted = _redact_credentials("Illegal header value b'Bearer otok_SUPER_SECRET rest'")

        assert "SUPER_SECRET" not in redacted
        assert "[REDACTED]" in redacted


class TestConnectorBuilderFailureReporting:
    """Connector-builder adapters must never mistake a failure for a success.

    Their generated parsers return ``None`` both for a genuine ``204 No Content``
    and for any status the OpenAPI document does not describe for the operation,
    and they call ``response.json()`` on documented error statuses. Both used to
    surface badly: a 502 looked like a completed delete, and an HTML error page
    escaped as a raw ``json.JSONDecodeError``.
    """

    DELETE_URL = "/v1/teams/1/connector_builder/connectors/c1"

    def test_no_content_is_still_a_success(self, api_server: MockAPIServer) -> None:
        """A genuine 204 still completes without raising."""
        api_server.route(self.DELETE_URL, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            assert client.connector_builder.delete(team_id=1, connector_identifier="c1") is None

    @pytest.mark.parametrize("status", [500, 502, 503])
    def test_undocumented_failure_is_not_reported_as_success(self, api_server: MockAPIServer, status: int) -> None:
        """A gateway failure raises instead of returning None like a completed delete."""
        api_server.route(self.DELETE_URL, ScriptedResponse(status=status, raw_body=b"<html>gateway error</html>"))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.connector_builder.delete(team_id=1, connector_identifier="c1")

        assert exc_info.value.status_code == status

    def test_non_json_error_body_does_not_leak_a_decode_error(self, api_server: MockAPIServer) -> None:
        """An HTML body on a documented error status still yields an SDK exception."""
        api_server.route(self.DELETE_URL, ScriptedResponse(status=500, raw_body=b"<html>not json at all</html>"))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.connector_builder.delete(team_id=1, connector_identifier="c1")

        assert exc_info.value.status_code == 500

    def test_unauthorized_is_classified_so_a_token_can_be_refreshed(self, api_server: MockAPIServer) -> None:
        """A 401 carries its status and OAuth code rather than arriving unclassified."""
        api_server.route(
            self.DELETE_URL,
            ScriptedResponse(
                status=401,
                json_body={"meta": {"request_id": "r"}, "error": {"code": "ACCESS_TOKEN_INVALID", "message": "dead"}},
            ),
        )

        with SupermetricsClient(bearer_token="otok_stale", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                client.connector_builder.delete(team_id=1, connector_identifier="c1")

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "ACCESS_TOKEN_INVALID"

    @pytest.mark.asyncio
    async def test_async_adapter_reports_failures_identically(self, api_server: MockAPIServer) -> None:
        """The async connector-builder adapter behaves the same way."""
        api_server.route(self.DELETE_URL, ScriptedResponse(status=502, raw_body=b"<html>bad gateway</html>"))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.connector_builder.delete(team_id=1, connector_identifier="c1")

        assert exc_info.value.status_code == 502

    @pytest.mark.parametrize(
        ("label", "url", "call"),
        [
            (
                "connectors",
                "/v1/teams/1/connector_builder/connectors",
                lambda client: client.connector_builder.list(team_id=1),
            ),
            (
                "logs",
                "/v1/teams/1/connector_builder/connectors/c1/logs",
                lambda client: client.connector_builder_logs.list(team_id=1, connector_identifier="c1"),
            ),
            (
                "secrets",
                "/v1/teams/1/connector_builder/connectors/c1/secrets",
                lambda client: client.connector_builder_secrets.list(team_id=1, connector_identifier="c1"),
            ),
        ],
    )
    def test_unrecognised_error_code_on_a_401_is_still_an_auth_error(
        self, api_server: MockAPIServer, label: str, url: str, call: Callable[[SupermetricsClient], object]
    ) -> None:
        """A 401 carrying an error code the SDK does not know is still classified by status.

        Mapping on the upstream code alone would leave any code outside the known
        set unclassified, so a caller could not tell that refreshing its token
        would fix the request.
        """
        api_server.route(
            url,
            ScriptedResponse(
                status=401,
                json_body={"meta": {"request_id": "r"}, "error": {"code": "TOKEN_REVOKED", "message": "revoked"}},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                call(client)

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "TOKEN_REVOKED"

    def test_errors_carry_the_underlying_httpx_response(self, api_server: MockAPIServer) -> None:
        """`raw_response` is populated so callers can inspect the real exchange."""
        api_server.route(
            self.DELETE_URL,
            ScriptedResponse(status=503, raw_body=b"<html>unavailable</html>", headers={"X-Request-Id": "req-9"}),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.connector_builder.delete(team_id=1, connector_identifier="c1")

        raw = exc_info.value.raw_response
        assert raw is not None
        assert raw.status_code == 503
        assert raw.headers["X-Request-Id"] == "req-9"
        assert raw.request.method == "DELETE"

    def test_secrets_delete_also_reports_gateway_failures(self, api_server: MockAPIServer) -> None:
        """The secrets adapter shares the same None-means-success shape."""
        url = "/v1/teams/1/connector_builder/connectors/c1/secrets/s1"
        api_server.route(url, ScriptedResponse(status=502, raw_body=b"<html>bad gateway</html>"))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.connector_builder_secrets.delete(team_id=1, connector_identifier="c1", secret_placeholder="s1")

        assert exc_info.value.status_code == 502


class TestErrorCodeConsistencyAcrossAdapters:
    """The same error payload must yield the same error_code on every adapter.

    The adapters reach the error handler by different routes — some hand over a
    parsed model, some only the raw body — and the upstream code was previously
    lost on the routes where the generated parser returned nothing.
    """

    PAYLOAD = {"error": {"code": "FORBIDDEN", "message": "no access", "details": {"scope": "read"}}}

    @pytest.mark.parametrize(
        ("label", "url", "call"),
        [
            ("logins", "/ds/logins", lambda client: client.logins.list()),
            ("login_links", "/ds/login/links", lambda client: client.login_links.list()),
            (
                "connector_builder",
                "/v1/teams/1/connector_builder/connectors",
                lambda client: client.connector_builder.list(team_id=1),
            ),
        ],
    )
    def test_upstream_code_and_details_survive_on_every_route(
        self, api_server: MockAPIServer, label: str, url: str, call: Callable[[SupermetricsClient], object]
    ) -> None:
        """Every adapter reports the same code and details for the same 403 body."""
        api_server.route(url, ScriptedResponse(status=403, json_body=self.PAYLOAD))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsForbiddenError) as exc_info:
                call(client)

        assert exc_info.value.status_code == 403
        assert exc_info.value.error_code == "FORBIDDEN"
        assert exc_info.value.details == {"scope": "read"}

    def test_a_non_json_body_degrades_without_raising(self, api_server: MockAPIServer) -> None:
        """A body that is not JSON leaves error_code unset rather than failing."""
        api_server.route("/ds/logins", ScriptedResponse(status=500, raw_body=b"<html>oops</html>"))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.logins.list()

        assert exc_info.value.status_code == 500
        assert exc_info.value.error_code is None
