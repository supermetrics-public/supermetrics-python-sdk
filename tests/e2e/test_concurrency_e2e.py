"""End-to-end tests proving a shared client is safe under concurrency.

The whole point of per-request overrides is that one pooled client can serve many
callers at once. These tests deliberately overlap requests on a single client and
assert that no caller ever sees another caller's credential or tracing headers.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import threading

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import LOGINS_LIST_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

CALLERS = 12


class TestAsyncConcurrencyIsolation:
    """Concurrent asyncio tasks on one client never cross-contaminate."""

    @pytest.mark.asyncio
    async def test_each_task_keeps_its_own_credential(self, api_server: MockAPIServer) -> None:
        """Overlapping tasks each send their own token."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.05))

        async with SupermetricsAsyncClient(api_key="api_shared", base_url=api_server.base_url) as client:

            async def caller(index: int) -> None:
                await client.logins.list(
                    auth_token=f"otok_caller_{index}",
                    headers={"X-Span-Id": f"span-{index}", "X-Team-ID": str(index)},
                )

            await asyncio.gather(*(caller(i) for i in range(CALLERS)))

        pairs = {(r.bearer_token, r.headers["x-span-id"], r.headers["x-team-id"]) for r in api_server.requests}
        assert pairs == {(f"otok_caller_{i}", f"span-{i}", str(i)) for i in range(CALLERS)}

    @pytest.mark.asyncio
    async def test_overridden_and_default_callers_coexist(self, api_server: MockAPIServer) -> None:
        """Tasks that override and tasks that do not can run at the same time."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.05))

        async with SupermetricsAsyncClient(api_key="api_default", base_url=api_server.base_url) as client:

            async def overriding(index: int) -> None:
                await client.logins.list(auth_token=f"otok_{index}")

            async def plain() -> None:
                await client.logins.list()

            await asyncio.gather(*(overriding(i) for i in range(6)), *(plain() for _ in range(6)))

        tokens = sorted(r.bearer_token or "" for r in api_server.requests)
        assert tokens == sorted(["api_default"] * 6 + [f"otok_{i}" for i in range(6)])

    @pytest.mark.asyncio
    async def test_token_provider_resolved_independently_per_task(self, api_server: MockAPIServer) -> None:
        """A per-task provider hands each task a distinct token."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.05))
        counter = {"n": 0}
        lock = asyncio.Lock()

        async def provider() -> str:
            async with lock:
                counter["n"] += 1
                return f"otok_issued_{counter['n']}"

        async with SupermetricsAsyncClient(token_provider=provider, base_url=api_server.base_url) as client:
            await asyncio.gather(*(client.logins.list() for _ in range(CALLERS)))

        tokens = {r.bearer_token for r in api_server.requests}
        assert len(tokens) == CALLERS

    @pytest.mark.asyncio
    async def test_connection_pool_is_reused(self, api_server: MockAPIServer) -> None:
        """Per-request overrides do not force a new connection per call."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            for index in range(6):
                await client.logins.list(auth_token=f"otok_{index}")

        # Sequential keep-alive requests should share a single source port.
        assert len({r.client_port for r in api_server.requests}) == 1

    @pytest.mark.asyncio
    async def test_a_timeout_in_one_task_does_not_affect_another(self, api_server: MockAPIServer) -> None:
        """One task timing out leaves concurrent tasks untouched."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.4))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=5.0) as client:
            from supermetrics.exceptions import NetworkError

            async def impatient() -> str:
                try:
                    await client.logins.list(timeout=0.1)
                except NetworkError:
                    return "timed-out"
                return "ok"

            async def patient() -> str:
                await client.logins.list()
                return "ok"

            results = await asyncio.gather(impatient(), patient(), patient())

        assert results == ["timed-out", "ok", "ok"]


class TestThreadConcurrencyIsolation:
    """Concurrent OS threads on one synchronous client never cross-contaminate."""

    def test_each_thread_keeps_its_own_credential(self, api_server: MockAPIServer) -> None:
        """Overlapping threads each send their own token and headers."""
        api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.05))
        barrier = threading.Barrier(CALLERS)

        with SupermetricsClient(api_key="api_shared", base_url=api_server.base_url) as client:

            def caller(index: int) -> None:
                # Force real overlap rather than accidental serialization.
                barrier.wait(timeout=10)
                client.logins.list(auth_token=f"otok_thread_{index}", headers={"X-Span-Id": f"span-{index}"})

            with concurrent.futures.ThreadPoolExecutor(max_workers=CALLERS) as pool:
                list(pool.map(caller, range(CALLERS)))

        pairs = {(r.bearer_token, r.headers["x-span-id"]) for r in api_server.requests}
        assert pairs == {(f"otok_thread_{i}", f"span-{i}") for i in range(CALLERS)}
