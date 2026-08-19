"""End-to-end tests for the Transfer Runs resource.

Drives the whole stack over a real loopback socket. Every test asserts on what went
*out* — verb, path, credential — not only on what came back, because the request is the
half a mocked transport cannot check.
"""

from __future__ import annotations

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import (
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
)

from .conftest import TRANSFER_RUN_DETAIL_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

ENDPOINT = "/teams/42/transfer_runs/12345"


def _error_envelope(code: str, message: str) -> dict[str, object]:
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


class TestTransferRunsResource:
    """Synchronous transfer run lookup."""

    def test_get_returns_the_unwrapped_run(self, api_server: MockAPIServer) -> None:
        """The response is {meta, data}; the adapter hands back the run itself."""
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            run = client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert run.id == 12345
        assert run.status == "COMPLETED"
        assert run.external_id == "run-ext-12345"
        assert run.total_rows == 4821

    def test_get_sends_a_get_to_the_underscored_path(self, api_server: MockAPIServer) -> None:
        """The path segment is ``transfer_runs``, with an underscore.

        Its sibling collections use hyphens (``available-sources``,
        ``data-source-connections``), so this is worth pinning down on the wire.
        """
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == "/teams/42/transfer_runs/12345"
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_query_details_are_parsed(self, api_server: MockAPIServer) -> None:
        """Per-query execution detail survives the round trip."""
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            run = client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert len(run.query_details) == 1
        assert run.query_details[0].status == "COMPLETED"
        assert run.query_details[0].rows == 4821

    def test_per_request_overrides_reach_the_wire(self, api_server: MockAPIServer) -> None:
        """auth_token and headers are applied by the client event hooks."""
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.transfer_runs.get(
                team_id=42,
                transfer_run_id=12345,
                auth_token="otok_scoped",
                headers={"X-Span-Id": "span-run", "Idempotency-Key": "idem-run"},
            )

        request = api_server.last_request
        assert request.bearer_token == "otok_scoped"
        assert request.headers["x-span-id"] == "span-run"
        assert request.headers["idempotency-key"] == "idem-run"

    def test_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response carries the status, headers and parsed body."""
        api_server.route(
            ENDPOINT,
            ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY, headers={"X-Request-Id": "req-run-1"}),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert response.status_code == 200
        assert response.request_id == "req-run-1"
        assert response.data.id == 12345
        assert response.json_body == TRANSFER_RUN_DETAIL_BODY

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, code: str, expected: type[Exception]
    ) -> None:
        """Every documented failure status maps to its own exception class."""
        api_server.route(ENDPOINT, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code

    def test_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the response, not guessed."""
        api_server.route(
            ENDPOINT,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "42"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert exc_info.value.retry_after == 42


class TestTransferRunsAsyncResource:
    """Asynchronous transfer run lookup — same wire behaviour, own event hooks."""

    @pytest.mark.asyncio
    async def test_get_returns_the_unwrapped_run(self, api_server: MockAPIServer) -> None:
        """The async path unwraps the envelope identically."""
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            run = await client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert run.id == 12345
        assert run.external_id == "run-ext-12345"

    @pytest.mark.asyncio
    async def test_get_sends_a_get_to_the_underscored_path(self, api_server: MockAPIServer) -> None:
        """Same request shape on the async client."""
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == "/teams/42/transfer_runs/12345"
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_per_request_overrides_reach_the_wire(self, api_server: MockAPIServer) -> None:
        """The async hook applies the per-request credential too."""
        api_server.route(ENDPOINT, ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.transfer_runs.get(
                team_id=42,
                transfer_run_id=12345,
                auth_token="otok_async",
                headers={"X-Span-Id": "span-async-run"},
            )

        request = api_server.last_request
        assert request.bearer_token == "otok_async"
        assert request.headers["x-span-id"] == "span-async-run"

    @pytest.mark.asyncio
    async def test_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response works on the async mirror."""
        api_server.route(
            ENDPOINT,
            ScriptedResponse(json_body=TRANSFER_RUN_DETAIL_BODY, headers={"X-Span-Id": "async-run-span"}),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert response.status_code == 200
        assert response.span_id == "async-run-span"
        assert response.data.id == 12345

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    async def test_status_maps_to_exception(
        self, api_server: MockAPIServer, status: int, code: str, expected: type[Exception]
    ) -> None:
        """Error classification is identical on the async path."""
        api_server.route(ENDPOINT, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert exc_info.value.status_code == status

    @pytest.mark.asyncio
    async def test_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """The async client reads Retry-After off the response as well."""
        api_server.route(
            ENDPOINT,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "42"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                await client.transfer_runs.get(team_id=42, transfer_run_id=12345)

        assert exc_info.value.retry_after == 42
