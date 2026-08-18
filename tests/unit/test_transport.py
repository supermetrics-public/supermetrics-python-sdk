"""Unit tests for the per-request transport plumbing in ``supermetrics._transport``.

The event hooks are exercised through real ``httpx`` clients backed by
``httpx.MockTransport``: hooks live on the client rather than the transport, so a
mock transport still runs the full request/response hook pipeline.
"""

import asyncio
import dataclasses
import threading
import warnings
from collections.abc import Callable, Iterator, Mapping
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest

from supermetrics._auth import AuthConfig
from supermetrics._transport import (
    ResponseRecord,
    build_async_event_hooks,
    build_default_headers,
    build_sync_event_hooks,
    capture_last_response,
    current_auth_token,
    current_last_response,
    current_request_headers,
    current_request_timeout,
    request_options,
    reset_last_response,
)
from supermetrics.exceptions import SupermetricsClientError

BASE_URL = "https://api.example.test"

#: Deliberately unusual so that "the client default was kept" is unambiguous.
CLIENT_TIMEOUT = httpx.Timeout(9.5)


@pytest.fixture(autouse=True)
def _isolate_transport_context() -> Iterator[None]:
    """Reset every transport context variable before and after each test."""
    for var in (current_auth_token, current_request_headers, current_request_timeout, current_last_response):
        var.set(None)
    yield
    for var in (current_auth_token, current_request_headers, current_request_timeout, current_last_response):
        var.set(None)


def _recording_handler(
    recorder: list[httpx.Request],
    status_code: int = 200,
    body: bytes = b'{"ok": true}',
) -> Callable[[httpx.Request], httpx.Response]:
    """Build a MockTransport handler that records requests and returns a fixed response."""

    def handler(request: httpx.Request) -> httpx.Response:
        recorder.append(request)
        return httpx.Response(status_code, content=body, headers={"X-Server": "mock"})

    return handler


def _client_headers(auth: AuthConfig, extra: Mapping[str, str] | None = None) -> dict[str, str]:
    """Build the default header set an SDK client would carry for this auth config."""
    headers: dict[str, str] = {}
    static = auth.static_authorization()
    if static is not None:
        headers["Authorization"] = static
    if extra:
        headers.update(extra)
    return headers


def _sync_client(
    auth: AuthConfig,
    recorder: list[httpx.Request],
    *,
    extra_headers: Mapping[str, str] | None = None,
    status_code: int = 200,
    body: bytes = b'{"ok": true}',
) -> httpx.Client:
    """Build a sync httpx client wired with the SDK event hooks and a mock transport."""
    return httpx.Client(
        base_url=BASE_URL,
        headers=_client_headers(auth, extra_headers),
        timeout=CLIENT_TIMEOUT,
        transport=httpx.MockTransport(_recording_handler(recorder, status_code, body)),
        event_hooks=build_sync_event_hooks(auth),
    )


def _async_client(
    auth: AuthConfig,
    recorder: list[httpx.Request],
    *,
    extra_headers: Mapping[str, str] | None = None,
    status_code: int = 200,
    body: bytes = b'{"ok": true}',
) -> httpx.AsyncClient:
    """Build an async httpx client wired with the SDK event hooks and a mock transport."""
    return httpx.AsyncClient(
        base_url=BASE_URL,
        headers=_client_headers(auth, extra_headers),
        timeout=CLIENT_TIMEOUT,
        transport=httpx.MockTransport(_recording_handler(recorder, status_code, body)),
        event_hooks=build_async_event_hooks(auth),
    )


class TestRequestOptions:
    """Tests for the request_options context manager."""

    def test_binds_all_three_overrides(self) -> None:
        """Test that every supplied override is visible inside the block."""
        with request_options(auth_token="otok_inner", headers={"X-Span": "s1"}, timeout=2.5):
            assert current_auth_token.get() == "otok_inner"
            assert current_request_headers.get() == {"X-Span": "s1"}
            assert current_request_timeout.get() == 2.5

    def test_binds_only_supplied_arguments(self) -> None:
        """Test that arguments left as None do not bind anything."""
        with request_options(auth_token="otok_only"):
            assert current_auth_token.get() == "otok_only"
            assert current_request_headers.get() is None
            assert current_request_timeout.get() is None

    def test_none_arguments_inherit_ambient_values(self) -> None:
        """Test that ambient values survive a block that overrides other arguments."""
        current_request_headers.set({"X-Ambient": "yes"})
        current_request_timeout.set(30.0)

        with request_options(auth_token="otok_inner"):
            assert current_auth_token.get() == "otok_inner"
            assert current_request_headers.get() == {"X-Ambient": "yes"}
            assert current_request_timeout.get() == 30.0

    def test_no_arguments_changes_nothing(self) -> None:
        """Test that an empty request_options block leaves the ambient state alone."""
        current_auth_token.set("otok_ambient")

        with request_options():
            assert current_auth_token.get() == "otok_ambient"

        assert current_auth_token.get() == "otok_ambient"

    def test_restores_every_variable_on_exit(self) -> None:
        """Test that all bound variables return to their previous values on exit."""
        current_auth_token.set("otok_outer")
        current_request_headers.set({"X-Outer": "1"})
        current_request_timeout.set(1.0)

        with request_options(auth_token="otok_inner", headers={"X-Inner": "2"}, timeout=7.0):
            pass

        assert current_auth_token.get() == "otok_outer"
        assert current_request_headers.get() == {"X-Outer": "1"}
        assert current_request_timeout.get() == 1.0

    def test_restores_to_none_when_nothing_was_bound_before(self) -> None:
        """Test that overrides are unbound entirely when there was no ambient value."""
        with request_options(auth_token="otok_inner", headers={"X-Inner": "2"}, timeout=7.0):
            pass

        assert current_auth_token.get() is None
        assert current_request_headers.get() is None
        assert current_request_timeout.get() is None

    def test_restores_when_block_raises(self) -> None:
        """Test that overrides are unwound when the block raises an exception."""
        current_auth_token.set("otok_outer")

        with pytest.raises(RuntimeError, match="boom"), request_options(auth_token="otok_inner", timeout=3.0):
            raise RuntimeError("boom")

        assert current_auth_token.get() == "otok_outer"
        assert current_request_timeout.get() is None

    def test_nested_blocks_layer_and_unwind(self) -> None:
        """Test that nested blocks override the outer block and restore it on exit."""
        with request_options(auth_token="outer", headers={"X-Level": "outer"}):
            assert current_auth_token.get() == "outer"

            with request_options(auth_token="inner"):
                assert current_auth_token.get() == "inner"
                assert current_request_headers.get() == {"X-Level": "outer"}

            assert current_auth_token.get() == "outer"
            assert current_request_headers.get() == {"X-Level": "outer"}

        assert current_auth_token.get() is None
        assert current_request_headers.get() is None

    def test_empty_header_mapping_is_bound(self) -> None:
        """Test that an empty (but not None) header mapping still shadows the ambient value."""
        current_request_headers.set({"X-Ambient": "yes"})

        with request_options(headers={}):
            assert current_request_headers.get() == {}

        assert current_request_headers.get() == {"X-Ambient": "yes"}

    def test_zero_timeout_is_bound(self) -> None:
        """Test that a zero timeout is treated as a real override rather than as unset."""
        with request_options(timeout=0.0):
            assert current_request_timeout.get() == 0.0

    def test_httpx_timeout_instance_is_bound_unchanged(self) -> None:
        """Test that an httpx.Timeout override is stored as-is."""
        timeout = httpx.Timeout(connect=1.0, read=2.0, write=3.0, pool=4.0)

        with request_options(timeout=timeout):
            assert current_request_timeout.get() is timeout


class TestResponseRecord:
    """Tests for ResponseRecord and reset_last_response."""

    def test_of_snapshots_the_response(self) -> None:
        """Test that ResponseRecord.of copies status, headers, body and request URL."""
        request = httpx.Request("GET", f"{BASE_URL}/v1/logins?page=2")
        response = httpx.Response(201, content=b'{"id": 1}', headers={"X-Server": "mock"}, request=request)

        record = ResponseRecord.of(response)

        assert record.status_code == 201
        assert record.content == b'{"id": 1}'
        assert record.headers["X-Server"] == "mock"
        assert record.request_url == f"{BASE_URL}/v1/logins?page=2"

    def test_of_headers_are_case_insensitive(self) -> None:
        """Test that the recorded headers keep httpx case-insensitive lookup semantics."""
        request = httpx.Request("GET", BASE_URL)
        response = httpx.Response(200, content=b"", headers={"Content-Type": "application/json"}, request=request)

        record = ResponseRecord.of(response)

        assert record.headers["content-TYPE"] == "application/json"

    def test_record_is_immutable(self) -> None:
        """Test that a ResponseRecord cannot be mutated after creation."""
        request = httpx.Request("GET", BASE_URL)
        record = ResponseRecord.of(httpx.Response(200, content=b"", request=request))

        with pytest.raises(dataclasses.FrozenInstanceError):
            record.status_code = 500  # type: ignore[misc]

    def test_reset_last_response_clears_the_record(self) -> None:
        """Test that reset_last_response forgets a previously recorded response."""
        request = httpx.Request("GET", BASE_URL)
        current_last_response.set(ResponseRecord.of(httpx.Response(200, content=b"", request=request)))

        reset_last_response()

        assert current_last_response.get() is None

    def test_reset_last_response_is_idempotent(self) -> None:
        """Test that reset_last_response is a no-op when nothing was recorded."""
        reset_last_response()
        reset_last_response()

        assert current_last_response.get() is None


class TestCaptureLastResponse:
    """Tests for the capture_last_response context manager."""

    def test_yields_none_when_no_request_was_made(self) -> None:
        """Test that the holder stays None when the block issues no request."""
        with capture_last_response() as holder:
            pass

        assert holder[0] is None

    def test_hides_the_ambient_record_inside_the_block(self) -> None:
        """Test that a record from before the block is not visible inside it."""
        request = httpx.Request("GET", BASE_URL)
        current_last_response.set(ResponseRecord.of(httpx.Response(200, content=b"outer", request=request)))

        with capture_last_response():
            assert current_last_response.get() is None

    def test_captures_the_last_response_of_the_block(self) -> None:
        """Test that the holder ends up with the record of the final request in the block."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        with _sync_client(auth, recorder, body=b"first") as client, capture_last_response() as holder:
            client.get("/v1/a")
            client.get("/v1/b")

        assert holder[0] is not None
        assert holder[0].status_code == 200
        assert holder[0].content == b"first"
        assert holder[0].request_url == f"{BASE_URL}/v1/b"

    def test_restores_the_previous_record_on_exit(self) -> None:
        """Test that the record present before the block is restored afterwards."""
        request = httpx.Request("GET", f"{BASE_URL}/v1/outer")
        outer = ResponseRecord.of(httpx.Response(200, content=b"outer", request=request))
        current_last_response.set(outer)

        recorder: list[httpx.Request] = []
        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with capture_last_response() as holder:
                client.get("/v1/inner")

        assert holder[0] is not None
        assert holder[0].request_url == f"{BASE_URL}/v1/inner"
        assert current_last_response.get() is outer

    def test_restores_the_previous_record_when_the_block_raises(self) -> None:
        """Test that the ambient record is restored even when the block raises."""
        request = httpx.Request("GET", f"{BASE_URL}/v1/outer")
        outer = ResponseRecord.of(httpx.Response(200, content=b"outer", request=request))
        current_last_response.set(outer)

        with pytest.raises(RuntimeError, match="boom"):
            with capture_last_response():
                raise RuntimeError("boom")

        assert current_last_response.get() is outer

    def test_nested_captures_are_independent(self) -> None:
        """Test that an inner capture block does not steal the outer block's record."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with capture_last_response() as outer_holder:
                client.get("/v1/outer")
                with capture_last_response() as inner_holder:
                    client.get("/v1/inner")

        assert inner_holder[0] is not None
        assert inner_holder[0].request_url == f"{BASE_URL}/v1/inner"
        assert outer_holder[0] is not None
        assert outer_holder[0].request_url == f"{BASE_URL}/v1/outer"


class TestSyncEventHooks:
    """Tests for build_sync_event_hooks driven through a real httpx.Client."""

    def test_static_credential_is_left_untouched(self) -> None:
        """Test that a static credential header set on the client is not rewritten."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        with _sync_client(auth, recorder) as client:
            client.get("/v1/logins")

        assert recorder[0].headers["Authorization"] == "Bearer api_static"

    def test_dynamic_provider_is_resolved_on_every_request(self) -> None:
        """Test that a token provider is called once per request and its token is used."""
        calls: list[int] = []

        def provider() -> str:
            calls.append(len(calls) + 1)
            return f"otok_{len(calls)}"

        recorder: list[httpx.Request] = []
        with _sync_client(AuthConfig(token_provider=provider), recorder) as client:
            client.get("/v1/a")
            client.get("/v1/b")

        assert len(calls) == 2
        assert recorder[0].headers["Authorization"] == "Bearer otok_1"
        assert recorder[1].headers["Authorization"] == "Bearer otok_2"

    def test_current_auth_token_overrides_static_credential(self) -> None:
        """Test that the ambient auth token wins over the client's static credential."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        with _sync_client(auth, recorder) as client, request_options(auth_token="otok_override"):
            client.get("/v1/logins")

        assert recorder[0].headers["Authorization"] == "Bearer otok_override"

    def test_current_auth_token_overrides_provider_without_calling_it(self) -> None:
        """Test that the ambient auth token short-circuits the token provider."""
        calls: list[int] = []

        def provider() -> str:
            calls.append(1)
            return "otok_from_provider"

        recorder: list[httpx.Request] = []
        with _sync_client(AuthConfig(token_provider=provider), recorder) as client:
            with request_options(auth_token="otok_override"):
                client.get("/v1/a")

        assert calls == []
        assert recorder[0].headers["Authorization"] == "Bearer otok_override"

    def test_auth_token_already_carrying_the_scheme_is_not_doubled(self) -> None:
        """Test that an ambient token that already says 'Bearer' is passed through as-is."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(auth_token="Bearer otok_prefixed"):
                client.get("/v1/a")

        assert recorder[0].headers["Authorization"] == "Bearer otok_prefixed"

    def test_override_applies_only_inside_the_block(self) -> None:
        """Test that the client falls back to its static credential after the block exits."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(auth_token="otok_override"):
                client.get("/v1/a")
            client.get("/v1/b")

        assert recorder[0].headers["Authorization"] == "Bearer otok_override"
        assert recorder[1].headers["Authorization"] == "Bearer api_static"

    def test_per_request_headers_are_merged(self) -> None:
        """Test that ambient extra headers are added to the outgoing request."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(headers={"X-Span-Id": "s1", "X-Tenant": "acme"}):
                client.get("/v1/a")

        assert recorder[0].headers["X-Span-Id"] == "s1"
        assert recorder[0].headers["X-Tenant"] == "acme"
        assert recorder[0].headers["Authorization"] == "Bearer api_static"

    def test_per_request_headers_beat_client_defaults(self) -> None:
        """Test that ambient headers take precedence over the client's default headers."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        with _sync_client(auth, recorder, extra_headers={"X-Trace-Id": "client-default"}) as client:
            with request_options(headers={"X-Trace-Id": "per-request"}):
                client.get("/v1/a")

        assert recorder[0].headers["X-Trace-Id"] == "per-request"
        assert recorder[0].headers.get_list("X-Trace-Id") == ["per-request"]

    def test_per_request_headers_beat_the_resolved_authorization(self) -> None:
        """Test that an Authorization supplied through headers outranks the auth token."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(auth_token="otok_override", headers={"Authorization": "Basic abc123"}):
                client.get("/v1/a")

        assert recorder[0].headers["Authorization"] == "Basic abc123"

    def test_per_request_headers_match_case_insensitively(self) -> None:
        """Test that a lower-cased ambient header replaces a differently-cased default."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        with _sync_client(auth, recorder, extra_headers={"X-Trace-Id": "client-default"}) as client:
            with request_options(headers={"x-trace-id": "per-request"}):
                client.get("/v1/a")

        assert recorder[0].headers.get_list("X-Trace-Id") == ["per-request"]

    def test_float_timeout_override_is_applied(self) -> None:
        """Test that a float timeout override lands in the request timeout extension."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(timeout=2.5):
                client.get("/v1/a")

        assert recorder[0].extensions["timeout"] == httpx.Timeout(2.5).as_dict()

    def test_httpx_timeout_override_is_applied(self) -> None:
        """Test that an httpx.Timeout override preserves its per-phase values."""
        recorder: list[httpx.Request] = []
        timeout = httpx.Timeout(connect=1.0, read=2.0, write=3.0, pool=4.0)

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(timeout=timeout):
                client.get("/v1/a")

        assert recorder[0].extensions["timeout"] == timeout.as_dict()

    def test_client_timeout_is_kept_when_no_override_is_set(self) -> None:
        """Test that the client's own timeout survives when no override is bound."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:
            client.get("/v1/a")

        assert recorder[0].extensions["timeout"] == CLIENT_TIMEOUT.as_dict()

    def test_response_record_is_populated_for_every_request(self) -> None:
        """Test that each response overwrites the ambient response record."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder, status_code=404, body=b"nope") as client:
            client.get("/v1/a")
            first = current_last_response.get()
            client.get("/v1/b")
            second = current_last_response.get()

        assert first is not None
        assert first.status_code == 404
        assert first.content == b"nope"
        assert first.request_url == f"{BASE_URL}/v1/a"
        assert second is not None
        assert second.request_url == f"{BASE_URL}/v1/b"

    def test_provider_returning_a_non_string_fails_the_request(self) -> None:
        """Test that a misbehaving token provider raises before the request is sent."""
        recorder: list[httpx.Request] = []

        def provider() -> str:
            return 12345  # type: ignore[return-value]

        with _sync_client(AuthConfig(token_provider=provider), recorder) as client:
            with pytest.raises(SupermetricsClientError, match="must return a string"):
                client.get("/v1/a")

        assert recorder == []


class TestAsyncEventHooks:
    """Tests for build_async_event_hooks driven through a real httpx.AsyncClient."""

    @pytest.mark.asyncio
    async def test_static_credential_is_left_untouched(self) -> None:
        """Test that a static credential header set on the client is not rewritten."""
        recorder: list[httpx.Request] = []

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:
            await client.get("/v1/logins")

        assert recorder[0].headers["Authorization"] == "Bearer api_static"

    @pytest.mark.asyncio
    async def test_coroutine_provider_is_awaited_per_request(self) -> None:
        """Test that an async token provider is awaited once per request."""
        calls: list[int] = []

        async def provider() -> str:
            calls.append(len(calls) + 1)
            return f"otok_{len(calls)}"

        recorder: list[httpx.Request] = []
        async with _async_client(AuthConfig(token_provider=provider), recorder) as client:
            await client.get("/v1/a")
            await client.get("/v1/b")

        assert len(calls) == 2
        assert recorder[0].headers["Authorization"] == "Bearer otok_1"
        assert recorder[1].headers["Authorization"] == "Bearer otok_2"

    @pytest.mark.asyncio
    async def test_synchronous_provider_also_works_on_the_async_client(self) -> None:
        """Test that a plain callable provider is accepted by the async hooks."""
        recorder: list[httpx.Request] = []

        async with _async_client(AuthConfig(token_provider=lambda: "otok_sync"), recorder) as client:
            await client.get("/v1/a")

        assert recorder[0].headers["Authorization"] == "Bearer otok_sync"

    @pytest.mark.asyncio
    async def test_current_auth_token_overrides_static_credential(self) -> None:
        """Test that the ambient auth token wins over the client's static credential."""
        recorder: list[httpx.Request] = []

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(auth_token="otok_override"):
                await client.get("/v1/a")

        assert recorder[0].headers["Authorization"] == "Bearer otok_override"

    @pytest.mark.asyncio
    async def test_current_auth_token_overrides_provider_without_awaiting_it(self) -> None:
        """Test that the ambient auth token short-circuits an async token provider."""
        calls: list[int] = []

        async def provider() -> str:
            calls.append(1)
            return "otok_from_provider"

        recorder: list[httpx.Request] = []
        async with _async_client(AuthConfig(token_provider=provider), recorder) as client:
            with request_options(auth_token="otok_override"):
                await client.get("/v1/a")

        assert calls == []
        assert recorder[0].headers["Authorization"] == "Bearer otok_override"

    @pytest.mark.asyncio
    async def test_per_request_headers_are_merged_with_highest_precedence(self) -> None:
        """Test that ambient headers outrank both client defaults and the auth token."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        async with _async_client(auth, recorder, extra_headers={"X-Trace-Id": "client-default"}) as client:
            with request_options(auth_token="otok_override", headers={"Authorization": "Basic abc", "X-Span": "s1"}):
                await client.get("/v1/a")

        assert recorder[0].headers["Authorization"] == "Basic abc"
        assert recorder[0].headers["X-Span"] == "s1"
        assert recorder[0].headers["X-Trace-Id"] == "client-default"

    @pytest.mark.asyncio
    async def test_per_request_headers_match_case_insensitively(self) -> None:
        """Test that a lower-cased ambient header replaces a differently-cased default."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        async with _async_client(auth, recorder, extra_headers={"X-Trace-Id": "client-default"}) as client:
            with request_options(headers={"x-trace-id": "per-request"}):
                await client.get("/v1/a")

        assert recorder[0].headers.get_list("X-Trace-Id") == ["per-request"]

    @pytest.mark.asyncio
    async def test_float_timeout_override_is_applied(self) -> None:
        """Test that a float timeout override lands in the request timeout extension."""
        recorder: list[httpx.Request] = []

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(timeout=2.5):
                await client.get("/v1/a")

        assert recorder[0].extensions["timeout"] == httpx.Timeout(2.5).as_dict()

    @pytest.mark.asyncio
    async def test_httpx_timeout_override_is_applied(self) -> None:
        """Test that an httpx.Timeout override preserves its per-phase values."""
        recorder: list[httpx.Request] = []
        timeout = httpx.Timeout(connect=1.0, read=2.0, write=3.0, pool=4.0)

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:
            with request_options(timeout=timeout):
                await client.get("/v1/a")

        assert recorder[0].extensions["timeout"] == timeout.as_dict()

    @pytest.mark.asyncio
    async def test_client_timeout_is_kept_when_no_override_is_set(self) -> None:
        """Test that the client's own timeout survives when no override is bound."""
        recorder: list[httpx.Request] = []

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:
            await client.get("/v1/a")

        assert recorder[0].extensions["timeout"] == CLIENT_TIMEOUT.as_dict()

    @pytest.mark.asyncio
    async def test_response_record_is_populated_for_every_request(self) -> None:
        """Test that each response overwrites the ambient response record."""
        recorder: list[httpx.Request] = []
        auth = AuthConfig(static_token="api_static")

        async with _async_client(auth, recorder, status_code=503, body=b"down") as client:
            await client.get("/v1/a")
            first = current_last_response.get()
            await client.get("/v1/b")
            second = current_last_response.get()

        assert first is not None
        assert first.status_code == 503
        assert first.content == b"down"
        assert first.request_url == f"{BASE_URL}/v1/a"
        assert second is not None
        assert second.request_url == f"{BASE_URL}/v1/b"

    @pytest.mark.asyncio
    async def test_capture_last_response_works_with_the_async_client(self) -> None:
        """Test that capture_last_response collects the record of an awaited request."""
        recorder: list[httpx.Request] = []

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:
            with capture_last_response() as holder:
                await client.get("/v1/a")

        assert holder[0] is not None
        assert holder[0].request_url == f"{BASE_URL}/v1/a"
        assert current_last_response.get() is None


class TestContextIsolation:
    """Tests that per-request overrides never leak across tasks or threads."""

    @pytest.mark.asyncio
    async def test_overrides_are_invisible_to_a_concurrent_task(self) -> None:
        """Test that a token bound in one asyncio task is not seen by a sibling task."""
        bound = asyncio.Event()
        observed = asyncio.Event()

        async def setter() -> str | None:
            with request_options(auth_token="task-a"):
                bound.set()
                await observed.wait()
                return current_auth_token.get()

        async def observer() -> str | None:
            await bound.wait()
            seen = current_auth_token.get()
            observed.set()
            return seen

        setter_token, observer_token = await asyncio.gather(setter(), observer())

        assert setter_token == "task-a"
        assert observer_token is None

    @pytest.mark.asyncio
    async def test_concurrent_tasks_send_their_own_credentials(self) -> None:
        """Test that two concurrent tasks each authorize with their own ambient token."""
        recorder: list[httpx.Request] = []
        release = asyncio.Event()

        async with _async_client(AuthConfig(static_token="api_static"), recorder) as client:

            async def call(token: str, wait: bool) -> None:
                with request_options(auth_token=token, headers={"X-Task": token}):
                    if wait:
                        await release.wait()
                    else:
                        release.set()
                    await client.get(f"/v1/{token}")

            await asyncio.gather(call("task-a", wait=True), call("task-b", wait=False))

        by_task = {request.headers["X-Task"]: request.headers["Authorization"] for request in recorder}
        assert by_task == {"task-a": "Bearer task-a", "task-b": "Bearer task-b"}

    def test_overrides_are_invisible_to_another_thread(self) -> None:
        """Test that a token bound in one worker thread is not seen by a second one."""
        barrier = threading.Barrier(2)

        def setter() -> str | None:
            with request_options(auth_token="thread-a"):
                barrier.wait(timeout=10)
                barrier.wait(timeout=10)
                return current_auth_token.get()

        def observer() -> str | None:
            barrier.wait(timeout=10)
            seen = current_auth_token.get()
            barrier.wait(timeout=10)
            return seen

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(setter), pool.submit(observer)]
            results = [future.result(timeout=10) for future in futures]

        assert results == ["thread-a", None]

    def test_main_thread_overrides_do_not_reach_worker_threads(self) -> None:
        """Test that a worker thread starts from a clean context, not the caller's."""
        with request_options(auth_token="main-thread", headers={"X-Main": "1"}, timeout=1.0):
            with ThreadPoolExecutor(max_workers=1) as pool:
                seen = pool.submit(
                    lambda: (
                        current_auth_token.get(),
                        current_request_headers.get(),
                        current_request_timeout.get(),
                    )
                ).result(timeout=10)

        assert seen == (None, None, None)

    def test_response_records_do_not_leak_between_threads(self) -> None:
        """Test that a response recorded in a worker thread is invisible to the caller."""
        recorder: list[httpx.Request] = []

        with _sync_client(AuthConfig(static_token="api_static"), recorder) as client:

            def call() -> ResponseRecord | None:
                client.get("/v1/worker")
                return current_last_response.get()

            with ThreadPoolExecutor(max_workers=1) as pool:
                worker_record = pool.submit(call).result(timeout=10)

        assert worker_record is not None
        assert worker_record.request_url == f"{BASE_URL}/v1/worker"
        assert current_last_response.get() is None


class TestBuildDefaultHeaders:
    """Tests for the shared client-level header construction."""

    @staticmethod
    def _static(token: str = "api_key_value") -> AuthConfig:
        """Return a configuration backed by a static credential."""
        return AuthConfig(static_token=token)

    @staticmethod
    def _dynamic() -> AuthConfig:
        """Return a configuration backed by a token provider."""
        return AuthConfig(token_provider=lambda: "otok_from_provider")

    def test_user_agent_is_always_present(self) -> None:
        """Test that the supplied User-Agent is advertised."""
        headers = build_default_headers(auth=self._static(), user_agent="ua/1", custom_headers=None)

        assert headers["User-Agent"] == "ua/1"

    def test_static_credential_is_baked_in(self) -> None:
        """Test that a static credential becomes a default Authorization header."""
        headers = build_default_headers(auth=self._static("api_abc"), user_agent="ua/1", custom_headers=None)

        assert headers["Authorization"] == "Bearer api_abc"

    def test_dynamic_credential_is_not_baked_in(self) -> None:
        """Test that a provider leaves Authorization to the per-request event hook."""
        headers = build_default_headers(auth=self._dynamic(), user_agent="ua/1", custom_headers=None)

        assert "Authorization" not in headers

    def test_custom_headers_are_merged(self) -> None:
        """Test that unrelated custom headers survive untouched."""
        headers = build_default_headers(
            auth=self._static(), user_agent="ua/1", custom_headers={"X-Team-ID": "9001", "X-Trace": "t"}
        )

        assert headers["X-Team-ID"] == "9001"
        assert headers["X-Trace"] == "t"

    def test_custom_headers_may_override_the_user_agent(self) -> None:
        """Test that overriding non-credential defaults still works."""
        headers = build_default_headers(auth=self._static(), user_agent="ua/1", custom_headers={"User-Agent": "mine/2"})

        assert headers["User-Agent"] == "mine/2"

    def test_no_warning_without_a_credential_conflict(self) -> None:
        """Test that ordinary custom headers are silent."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            build_default_headers(auth=self._static(), user_agent="ua/1", custom_headers={"X-Team-ID": "1"})

    @pytest.mark.parametrize("key", ["Authorization", "authorization", "AUTHORIZATION", "AuThOrIzAtIoN"])
    def test_static_credential_outranks_a_custom_authorization(self, key: str) -> None:
        """Test that the constructor credential wins, whatever casing was used."""
        with pytest.warns(UserWarning, match="custom_headers set 'Authorization'"):
            headers = build_default_headers(
                auth=self._static("api_real"), user_agent="ua/1", custom_headers={key: "Bearer sneaky"}
            )

        assert headers["Authorization"] == "Bearer api_real"
        assert [name for name in headers if name.lower() == "authorization"] == ["Authorization"]

    @pytest.mark.parametrize("key", ["Authorization", "authorization"])
    def test_dynamic_credential_leaves_no_stale_authorization(self, key: str) -> None:
        """Test that no leftover header survives for the event hook to fight with."""
        with pytest.warns(UserWarning, match="custom_headers set 'Authorization'"):
            headers = build_default_headers(
                auth=self._dynamic(), user_agent="ua/1", custom_headers={key: "Bearer sneaky"}
            )

        assert not [name for name in headers if name.lower() == "authorization"]

    def test_other_custom_headers_survive_a_credential_conflict(self) -> None:
        """Test that rejecting Authorization does not discard the caller's other headers."""
        with pytest.warns(UserWarning):
            headers = build_default_headers(
                auth=self._static(), user_agent="ua/1", custom_headers={"Authorization": "x", "X-Team-ID": "9001"}
            )

        assert headers["X-Team-ID"] == "9001"


class TestResponseRecordDefensivePaths:
    """The record degrades rather than raising when httpx withholds the request."""

    def test_missing_request_yields_no_url(self) -> None:
        """Test that a response with no request attached records request_url as None.

        ``httpx.Response.request`` raises ``RuntimeError`` rather than returning
        ``None``, so a truthiness guard here would raise instead of degrading.
        """
        response = httpx.Response(200, content=b"{}")

        record = ResponseRecord.of(response)

        assert record.request_url is None
        assert record.status_code == 200
        assert record.content == b"{}"
        assert record.response is response

    def test_attached_request_is_recorded(self) -> None:
        """Test that the request URL is captured when one is attached."""
        request = httpx.Request("GET", "https://api.test/v1/thing")
        response = httpx.Response(200, content=b"{}", request=request)

        record = ResponseRecord.of(response)

        assert record.request_url == "https://api.test/v1/thing"
