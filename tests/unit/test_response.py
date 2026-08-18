"""Unit tests for the raw-response envelope and the ``with_raw_response`` wrappers."""

from __future__ import annotations

import inspect
from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from supermetrics._auth import AuthConfig
from supermetrics._transport import (
    ResponseRecord,
    build_async_event_hooks,
    build_sync_event_hooks,
    current_last_response,
    reset_last_response,
)
from supermetrics.exceptions import SupermetricsClientError
from supermetrics.response import ApiResponse, async_to_raw_response_wrapper, to_raw_response_wrapper


@pytest.fixture(autouse=True)
def _clean_last_response() -> Iterator[None]:
    """Ensure no recorded response leaks between tests."""
    reset_last_response()
    yield
    reset_last_response()


def make_record(
    *,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
    content: bytes = b"",
    request_url: str | None = "https://api.example.test/things",
) -> ResponseRecord:
    """Build a transport record standing in for one captured HTTP response."""
    return ResponseRecord(
        status_code=status_code,
        headers=httpx.Headers(headers or {}),
        content=content,
        request_url=request_url,
    )


class TestApiResponseAttributes:
    """Test suite for the values an ApiResponse stores."""

    def test_stores_every_constructor_argument(self) -> None:
        """Test that data, status, headers, body and URL are exposed as given."""
        data = {"login_id": "login_abc"}
        headers = httpx.Headers({"Content-Type": "application/json"})

        response = ApiResponse(
            data,
            status_code=201,
            headers=headers,
            raw_body=b'{"login_id": "login_abc"}',
            request_url="https://api.example.test/ds/login",
        )

        assert response.data is data
        assert response.status_code == 201
        assert response.headers is headers
        assert response.raw_body == b'{"login_id": "login_abc"}'
        assert response.request_url == "https://api.example.test/ds/login"

    def test_request_url_defaults_to_none(self) -> None:
        """Test that request_url is optional and defaults to None."""
        response = ApiResponse(None, status_code=204, headers=httpx.Headers(), raw_body=b"")

        assert response.request_url is None

    def test_data_may_be_none_for_an_empty_response(self) -> None:
        """Test that a 204-style response with no payload is representable."""
        response = ApiResponse(None, status_code=204, headers=httpx.Headers(), raw_body=b"")

        assert response.data is None
        assert response.status_code == 204
        assert response.json_body is None

    def test_repr_reports_the_status_code_and_the_data(self) -> None:
        """Test the exact repr, so neither field can be dropped, swapped or mislabelled."""
        response = ApiResponse("payload", status_code=418, headers=httpx.Headers(), raw_body=b"")

        assert repr(response) == "ApiResponse(status_code=418, data='payload')"

    def test_header_lookup_is_case_insensitive(self) -> None:
        """Test that headers can be read regardless of the case they arrived in."""
        response = ApiResponse(
            None,
            status_code=200,
            headers=httpx.Headers({"x-span-id": "span-lower"}),
            raw_body=b"",
        )

        assert response.headers["X-SPAN-ID"] == "span-lower"
        assert response.span_id == "span-lower"


class TestApiResponseCorrelationHeaders:
    """Test suite for span_id, request_id and retry_after."""

    def test_span_id_and_request_id_read_their_own_headers(self) -> None:
        """Test that each correlation property reads the header it is named for."""
        response = ApiResponse(
            None,
            status_code=200,
            headers=httpx.Headers({"X-Span-Id": "a8f3b2c9e10d", "X-Request-Id": "req-42"}),
            raw_body=b"",
        )

        assert response.span_id == "a8f3b2c9e10d"
        assert response.request_id == "req-42"

    def test_span_id_is_none_when_only_the_request_id_is_present(self) -> None:
        """Test that the two headers are read independently, not as a fallback pair."""
        response = ApiResponse(
            None,
            status_code=200,
            headers=httpx.Headers({"X-Request-Id": "req-42"}),
            raw_body=b"",
        )

        assert response.span_id is None
        assert response.request_id == "req-42"

    def test_span_id_and_request_id_are_none_when_absent(self) -> None:
        """Test that missing correlation headers read as None rather than raising."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=b"")

        assert response.span_id is None
        assert response.request_id is None

    def test_retry_after_parses_a_numeric_value(self) -> None:
        """Test that a numeric Retry-After header is returned as an int, not the raw string."""
        response = ApiResponse(
            None,
            status_code=429,
            headers=httpx.Headers({"Retry-After": "30"}),
            raw_body=b"",
        )

        assert response.retry_after == 30
        assert isinstance(response.retry_after, int)

    def test_retry_after_of_zero_is_reported_as_zero(self) -> None:
        """Test that "retry immediately" is preserved and not flattened to None."""
        response = ApiResponse(
            None,
            status_code=429,
            headers=httpx.Headers({"Retry-After": "0"}),
            raw_body=b"",
        )

        assert response.retry_after == 0

    def test_retry_after_tolerates_surrounding_whitespace(self) -> None:
        """Test that a padded numeric Retry-After header is still parsed."""
        response = ApiResponse(
            None,
            status_code=429,
            headers=httpx.Headers({"Retry-After": " 45 "}),
            raw_body=b"",
        )

        assert response.retry_after == 45

    def test_retry_after_is_none_when_absent(self) -> None:
        """Test that a missing Retry-After header reads as None."""
        response = ApiResponse(None, status_code=429, headers=httpx.Headers(), raw_body=b"")

        assert response.retry_after is None

    @pytest.mark.parametrize("value", ["Wed, 21 Oct 2015 07:28:00 GMT", "soon", "", "-5", "1.5", "30s"])
    def test_retry_after_is_none_for_non_integer_values(self, value: str) -> None:
        """Test that an HTTP-date or otherwise non-integer Retry-After reads as None."""
        response = ApiResponse(
            None,
            status_code=429,
            headers=httpx.Headers({"Retry-After": value}),
            raw_body=b"",
        )

        assert response.retry_after is None

    def test_retry_after_is_none_for_a_digit_int_cannot_parse(self) -> None:
        """Test that a digit-like Retry-After byte sequence reads as None, not ValueError."""
        # Built from wire bytes because that is how httpx parses a real response; the
        # str constructor would reject a non-ASCII header value outright.
        headers = httpx.Headers([(b"retry-after", b"\xc2\xb2")])

        response = ApiResponse(None, status_code=429, headers=headers, raw_body=b"")

        assert response.retry_after is None


class TestApiResponseJsonBody:
    """Test suite for decoding the raw body as JSON."""

    def test_decodes_a_json_object(self) -> None:
        """Test that an object body is decoded into a dict."""
        response = ApiResponse(
            None,
            status_code=200,
            headers=httpx.Headers(),
            raw_body=b'{"data": {"login_id": "login_abc"}}',
        )

        assert response.json_body == {"data": {"login_id": "login_abc"}}

    def test_decodes_a_json_array(self) -> None:
        """Test that a top-level array body is decoded into a list."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=b'[1, "two", null]')

        assert response.json_body == [1, "two", None]

    def test_empty_body_decodes_to_none(self) -> None:
        """Test that an empty body yields None instead of raising."""
        response = ApiResponse(None, status_code=204, headers=httpx.Headers(), raw_body=b"")

        assert response.json_body is None

    def test_non_json_body_decodes_to_none(self) -> None:
        """Test that an HTML error page from a proxy yields None."""
        response = ApiResponse(
            None,
            status_code=502,
            headers=httpx.Headers({"Content-Type": "text/html"}),
            raw_body=b"<html><body>Bad Gateway</body></html>",
        )

        assert response.json_body is None

    def test_whitespace_only_body_decodes_to_none(self) -> None:
        """Test that a body of only whitespace is not mistaken for JSON."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=b"   \n  ")

        assert response.json_body is None

    @pytest.mark.parametrize("raw_body", [b'"just a string"', b"42", b"true", b"null"])
    def test_json_scalars_decode_to_none(self, raw_body: bytes) -> None:
        """Test that a valid but non-object, non-array JSON body yields None."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=raw_body)

        assert response.json_body is None

    def test_undecodable_bytes_decode_to_none(self) -> None:
        """Test that a body which is not valid UTF-8 yields None instead of raising."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=b"\xff\xfe\x00binary")

        assert response.json_body is None

    def test_json_body_is_decoded_once_and_cached(self) -> None:
        """Test that a decoded body is memoized rather than parsed again on each access."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=b'{"a": 1}')

        first = response.json_body
        # Swapping the source body proves the second read never re-parsed it.
        response.raw_body = b'{"replaced": true}'

        assert first == {"a": 1}
        assert response.json_body is first

    @pytest.mark.parametrize(
        ("raw_body", "case"),
        [
            (b"", "empty"),
            (b"not json", "invalid"),
            (b"   \n  ", "whitespace"),
            (b"\xff\xfe\x00binary", "undecodable"),
            (b"42", "scalar"),
        ],
    )
    def test_an_absent_or_unusable_body_is_cached_as_none(self, raw_body: bytes, case: str) -> None:
        """Test that a None result is memoized too, so the body is never decoded twice."""
        response = ApiResponse(None, status_code=200, headers=httpx.Headers(), raw_body=raw_body)

        assert response.json_body is None, case
        # Swapping in a decodable body must not resurrect a second parse attempt.
        response.raw_body = b'{"replaced": true}'

        assert response.json_body is None, case


class TestToRawResponseWrapper:
    """Test suite for the synchronous with_raw_response wrapper."""

    def test_preserves_name_docstring_and_signature(self) -> None:
        """Test that the wrapper is transparent to introspection."""

        def get_login(login_id: str, *, expand: bool = False) -> str:
            """Fetch one login."""
            return login_id

        wrapped = to_raw_response_wrapper(get_login)

        assert wrapped.__name__ == "get_login"
        assert wrapped.__doc__ == "Fetch one login."
        assert inspect.signature(wrapped) == inspect.signature(get_login)
        assert not inspect.iscoroutinefunction(wrapped)

    def test_passes_positional_and_keyword_arguments_through(self) -> None:
        """Test that every argument reaches the wrapped function untouched."""
        seen: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

        def get_login(login_id: str, *, expand: bool = False, auth_token: str | None = None) -> dict[str, Any]:
            seen.append(((login_id,), {"expand": expand, "auth_token": auth_token}))
            current_last_response.set(make_record())
            return {"login_id": login_id}

        wrapped = to_raw_response_wrapper(get_login)
        result = wrapped("login_abc", expand=True, auth_token="otok_1")

        assert seen == [(("login_abc",), {"expand": True, "auth_token": "otok_1"})]
        assert result.data == {"login_id": "login_abc"}

    def test_wraps_the_return_value_with_the_recorded_transport_metadata(self) -> None:
        """Test that the envelope reports the status, headers, body and URL recorded."""

        @to_raw_response_wrapper
        def create() -> str:
            current_last_response.set(
                make_record(
                    status_code=201,
                    headers={"X-Span-Id": "span-1", "Retry-After": "7"},
                    content=b'{"id": "abc"}',
                    request_url="https://api.example.test/ds/login",
                )
            )
            return "abc"

        result = create()

        assert isinstance(result, ApiResponse)
        assert result.data == "abc"
        assert result.status_code == 201
        assert result.span_id == "span-1"
        assert result.request_id is None
        assert result.retry_after == 7
        assert result.raw_body == b'{"id": "abc"}'
        assert result.json_body == {"id": "abc"}
        assert result.request_url == "https://api.example.test/ds/login"

    def test_wraps_a_none_result_rather_than_reporting_a_missing_request(self) -> None:
        """Test that a 204 delete returning None still yields an envelope."""

        @to_raw_response_wrapper
        def delete() -> None:
            current_last_response.set(make_record(status_code=204, content=b""))
            return None

        result = delete()

        assert result.data is None
        assert result.status_code == 204
        assert result.json_body is None

    def test_describes_the_last_response_when_several_were_recorded(self) -> None:
        """Test that a multi-request method reports the final response."""

        @to_raw_response_wrapper
        def paginate() -> list[int]:
            current_last_response.set(make_record(status_code=200, content=b'{"page": 1}'))
            current_last_response.set(make_record(status_code=206, content=b'{"page": 2}'))
            return [1, 2]

        result = paginate()

        assert result.data == [1, 2]
        assert result.status_code == 206
        assert result.json_body == {"page": 2}

    def test_propagates_exceptions_unchanged(self) -> None:
        """Test that a failure inside the wrapped function is not swallowed or rewrapped."""
        boom = RuntimeError("upstream exploded")

        @to_raw_response_wrapper
        def failing() -> str:
            current_last_response.set(make_record(status_code=500))
            raise boom

        with pytest.raises(RuntimeError) as excinfo:
            failing()

        assert excinfo.value is boom

    def test_restores_the_ambient_record_when_the_call_raises(self) -> None:
        """Test that a failed call leaves none of its own transport state behind."""
        ambient = make_record(status_code=200, content=b'{"ambient": true}')
        current_last_response.set(ambient)

        @to_raw_response_wrapper
        def failing() -> str:
            current_last_response.set(make_record(status_code=500, content=b'{"leaked": true}'))
            raise RuntimeError("upstream exploded")

        with pytest.raises(RuntimeError):
            failing()

        assert current_last_response.get() is ambient

    def test_raises_client_error_when_no_request_was_made(self) -> None:
        """Test that wrapping a method which issues no HTTP call is reported clearly."""

        @to_raw_response_wrapper
        def cached_lookup() -> str:
            return "from-cache"

        with pytest.raises(SupermetricsClientError) as excinfo:
            cached_lookup()

        assert "no HTTP request" in str(excinfo.value)

    def test_ignores_a_record_left_behind_by_an_earlier_call(self) -> None:
        """Test that a stale record is never reported as the metadata of this call."""
        stale = make_record(status_code=500, content=b'{"stale": true}')
        current_last_response.set(stale)

        @to_raw_response_wrapper
        def cached_lookup() -> str:
            return "from-cache"

        with pytest.raises(SupermetricsClientError):
            cached_lookup()

        assert current_last_response.get() is stale

    def test_restores_the_ambient_record_after_a_successful_call(self) -> None:
        """Test that the wrapper's capture does not clobber the surrounding context."""
        ambient = make_record(status_code=200, content=b'{"ambient": true}')
        current_last_response.set(ambient)

        @to_raw_response_wrapper
        def call() -> str:
            current_last_response.set(make_record(status_code=201))
            return "ok"

        result = call()

        assert result.status_code == 201
        assert current_last_response.get() is ambient


class TestAsyncToRawResponseWrapper:
    """Test suite for the asynchronous with_raw_response wrapper."""

    def test_preserves_name_docstring_and_signature(self) -> None:
        """Test that the async wrapper is transparent to introspection."""

        async def get_login(login_id: str, *, expand: bool = False) -> str:
            """Fetch one login."""
            return login_id

        wrapped = async_to_raw_response_wrapper(get_login)

        assert wrapped.__name__ == "get_login"
        assert wrapped.__doc__ == "Fetch one login."
        assert inspect.signature(wrapped) == inspect.signature(get_login)
        assert inspect.iscoroutinefunction(wrapped)

    @pytest.mark.asyncio
    async def test_passes_positional_and_keyword_arguments_through(self) -> None:
        """Test that every argument reaches the wrapped coroutine untouched."""
        seen: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

        async def get_login(login_id: str, *, expand: bool = False, auth_token: str | None = None) -> dict[str, Any]:
            seen.append(((login_id,), {"expand": expand, "auth_token": auth_token}))
            current_last_response.set(make_record())
            return {"login_id": login_id}

        wrapped = async_to_raw_response_wrapper(get_login)
        result = await wrapped("login_abc", expand=True, auth_token="otok_1")

        assert seen == [(("login_abc",), {"expand": True, "auth_token": "otok_1"})]
        assert result.data == {"login_id": "login_abc"}

    @pytest.mark.asyncio
    async def test_wraps_the_return_value_with_the_recorded_transport_metadata(self) -> None:
        """Test that the awaited envelope reports the recorded transport metadata."""

        @async_to_raw_response_wrapper
        async def create() -> str:
            current_last_response.set(
                make_record(
                    status_code=202,
                    headers={"X-Request-Id": "req-9"},
                    content=b'{"id": "abc"}',
                    request_url="https://api.example.test/ds/login",
                )
            )
            return "abc"

        result = await create()

        assert isinstance(result, ApiResponse)
        assert result.data == "abc"
        assert result.status_code == 202
        assert result.request_id == "req-9"
        assert result.span_id is None
        assert result.json_body == {"id": "abc"}
        assert result.request_url == "https://api.example.test/ds/login"

    @pytest.mark.asyncio
    async def test_describes_the_last_response_when_several_were_recorded(self) -> None:
        """Test that a multi-request coroutine reports the final response."""

        @async_to_raw_response_wrapper
        async def paginate() -> list[int]:
            current_last_response.set(make_record(status_code=200, content=b'{"page": 1}'))
            current_last_response.set(make_record(status_code=206, content=b'{"page": 2}'))
            return [1, 2]

        result = await paginate()

        assert result.data == [1, 2]
        assert result.status_code == 206
        assert result.json_body == {"page": 2}

    @pytest.mark.asyncio
    async def test_propagates_exceptions_unchanged(self) -> None:
        """Test that a failure inside the wrapped coroutine is not swallowed or rewrapped."""
        boom = RuntimeError("upstream exploded")

        @async_to_raw_response_wrapper
        async def failing() -> str:
            current_last_response.set(make_record(status_code=500))
            raise boom

        with pytest.raises(RuntimeError) as excinfo:
            await failing()

        assert excinfo.value is boom

    @pytest.mark.asyncio
    async def test_restores_the_ambient_record_when_the_call_raises(self) -> None:
        """Test that a failed coroutine leaves none of its own transport state behind."""
        ambient = make_record(status_code=200, content=b'{"ambient": true}')
        current_last_response.set(ambient)

        @async_to_raw_response_wrapper
        async def failing() -> str:
            current_last_response.set(make_record(status_code=500, content=b'{"leaked": true}'))
            raise RuntimeError("upstream exploded")

        with pytest.raises(RuntimeError):
            await failing()

        assert current_last_response.get() is ambient

    @pytest.mark.asyncio
    async def test_raises_client_error_when_no_request_was_made(self) -> None:
        """Test that an async method which issues no HTTP call is reported clearly."""

        @async_to_raw_response_wrapper
        async def cached_lookup() -> str:
            return "from-cache"

        with pytest.raises(SupermetricsClientError) as excinfo:
            await cached_lookup()

        assert "no HTTP request" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_ignores_a_record_left_behind_by_an_earlier_call(self) -> None:
        """Test that a stale record is never reported as the metadata of this coroutine."""
        stale = make_record(status_code=500, content=b'{"stale": true}')
        current_last_response.set(stale)

        @async_to_raw_response_wrapper
        async def cached_lookup() -> str:
            return "from-cache"

        with pytest.raises(SupermetricsClientError):
            await cached_lookup()

        assert current_last_response.get() is stale

    @pytest.mark.asyncio
    async def test_restores_the_ambient_record_after_a_successful_call(self) -> None:
        """Test that the async capture does not clobber the surrounding context."""
        ambient = make_record(status_code=200, content=b'{"ambient": true}')
        current_last_response.set(ambient)

        @async_to_raw_response_wrapper
        async def call() -> str:
            current_last_response.set(make_record(status_code=201))
            return "ok"

        result = await call()

        assert result.status_code == 201
        assert current_last_response.get() is ambient


class TestRawResponseWrapperOverRealTransport:
    """Test suite driving the wrappers through a real httpx request pipeline."""

    def test_sync_envelope_describes_the_actual_http_response(self) -> None:
        """Test that a real request recorded by the sync event hooks fills the envelope."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                201,
                headers={"X-Span-Id": "span-real", "X-Request-Id": "req-real", "Retry-After": "12"},
                json={"data": {"login_id": "login_abc"}},
            )

        client = httpx.Client(
            base_url="https://api.example.test",
            transport=httpx.MockTransport(handler),
            event_hooks=build_sync_event_hooks(AuthConfig(static_token="api_key_1")),
        )

        @to_raw_response_wrapper
        def create() -> str:
            response = client.post("/ds/login", json={"ds_id": "GAWA"})
            return str(response.json()["data"]["login_id"])

        with client:
            result = create()

        assert result.data == "login_abc"
        assert result.status_code == 201
        assert result.span_id == "span-real"
        assert result.request_id == "req-real"
        assert result.retry_after == 12
        assert result.raw_body == b'{"data":{"login_id":"login_abc"}}'
        assert result.json_body == {"data": {"login_id": "login_abc"}}
        assert result.request_url == "https://api.example.test/ds/login"
        assert current_last_response.get() is None

    def test_sync_envelope_describes_the_last_of_several_real_requests(self) -> None:
        """Test that a method issuing two real requests reports the second one throughout."""
        statuses = iter([200, 206])

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(next(statuses), json={"url": str(request.url)})

        client = httpx.Client(
            base_url="https://api.example.test",
            transport=httpx.MockTransport(handler),
            event_hooks=build_sync_event_hooks(AuthConfig(static_token="api_key_1")),
        )

        @to_raw_response_wrapper
        def paginate() -> int:
            client.get("/ds/logins")
            client.get("/ds/logins?page=2")
            return 2

        with client:
            result = paginate()

        assert result.data == 2
        assert result.status_code == 206
        assert result.request_url == "https://api.example.test/ds/logins?page=2"
        # The body must come from the same response as the status, not the first request.
        assert result.json_body == {"url": "https://api.example.test/ds/logins?page=2"}

    def test_sync_envelope_handles_a_non_json_error_body(self) -> None:
        """Test that an HTML gateway error is still described, with json_body None."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(502, headers={"Content-Type": "text/html"}, content=b"<html>Bad Gateway</html>")

        client = httpx.Client(
            base_url="https://api.example.test",
            transport=httpx.MockTransport(handler),
            event_hooks=build_sync_event_hooks(AuthConfig(static_token="api_key_1")),
        )

        @to_raw_response_wrapper
        def call() -> int:
            return client.get("/ds/logins").status_code

        with client:
            result = call()

        assert result.data == 502
        assert result.status_code == 502
        assert result.raw_body == b"<html>Bad Gateway</html>"
        assert result.json_body is None
        assert result.retry_after is None

    @pytest.mark.asyncio
    async def test_async_envelope_describes_the_actual_http_response(self) -> None:
        """Test that a real request recorded by the async event hooks fills the envelope."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, headers={"X-Span-Id": "span-async"}, json={"data": []})

        client = httpx.AsyncClient(
            base_url="https://api.example.test",
            transport=httpx.MockTransport(handler),
            event_hooks=build_async_event_hooks(AuthConfig(static_token="api_key_1")),
        )

        @async_to_raw_response_wrapper
        async def list_logins() -> list[Any]:
            response = await client.get("/ds/logins")
            data: list[Any] = response.json()["data"]
            return data

        async with client:
            result = await list_logins()

        assert result.data == []
        assert result.status_code == 200
        assert result.span_id == "span-async"
        assert result.request_id is None
        assert result.json_body == {"data": []}
        assert result.request_url == "https://api.example.test/ds/logins"
        assert current_last_response.get() is None

    @pytest.mark.asyncio
    async def test_async_envelope_reports_a_real_error_response(self) -> None:
        """Test that an async 429 carries its status and Retry-After from the wire."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(429, headers={"Retry-After": "60"}, json={"error": "rate limited"})

        client = httpx.AsyncClient(
            base_url="https://api.example.test",
            transport=httpx.MockTransport(handler),
            event_hooks=build_async_event_hooks(AuthConfig(static_token="api_key_1")),
        )

        @async_to_raw_response_wrapper
        async def call() -> int:
            return (await client.get("/ds/logins")).status_code

        async with client:
            result = await call()

        assert result.status_code == 429
        assert result.retry_after == 60
        assert result.json_body == {"error": "rate limited"}
