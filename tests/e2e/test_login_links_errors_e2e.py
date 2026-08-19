"""End-to-end tests for the Login Links error taxonomy.

Every failure here is a real HTTP response with a real status and real headers, driven
through the whole stack over a loopback socket. Error classification, ``Retry-After``
parsing and correlation-header capture only exist on the wire, so a mocked transport
cannot observe any of them.

Two things about this domain make it worth its own module rather than a handful of cases
bolted onto the happy-path tests:

- **``update`` is the one method that documents a 400.** The Login Links spec lists 400,
  401, 403, 404, 422, 429 and 500 on the PATCH, and both 400 and 422 map to
  :class:`SupermetricsValidationError`. The full status ladder is parametrized against it
  so a reclassification of any rung shows up as a failing assertion.
- **``close`` returns ``None`` on success**, so its adapter decides purely from the
  status. A failure that leaked through that branch would look like a link that simply
  closed. Every non-200 on the PUT must raise instead.

The routes are spelled out here rather than in ``conftest.py`` because this module owns
them; ``get`` and ``update`` deliberately share ``/ds/login/link/{link_id}`` and are told
apart by the recorded HTTP method, which is why every case also asserts the verb.
"""

from __future__ import annotations

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import (
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: Login links live on the core API host at bare ``/ds/...`` paths — no ``/v1`` prefix and
#: no re-host to the Data Warehouse host. A regression on either would fall through to the
#: mock server's default 404 rather than reaching the scripted status.
LINK_ID = "link_123"
LINK_CREATE = "/ds/login/link"
LINK_LIST = "/ds/login/links"
LINK_ITEM = f"/ds/login/link/{LINK_ID}"  # GET (get) and PATCH (update) share this path.
LINK_CLOSE = f"{LINK_ITEM}/close"


def _error_envelope(code: str, message: str) -> dict[str, object]:
    return {
        "meta": {"request_id": "req_00000000"},
        "error": {"code": code, "message": message, "description": message},
    }


#: Every failure status the Login Links spec documents on ``update`` (the PATCH), and the
#: class each becomes. Unlike account tags, this domain documents both a 400 and a 422, and
#: both are validation errors — the ladder pins that they do not diverge.
UPDATE_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (404, "NOT_FOUND", SupermetricsNotFoundError),
    (422, "UNPROCESSABLE_ENTITY", SupermetricsValidationError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


class TestLoginLinksUpdateErrorTaxonomy:
    """Status-to-exception mapping and preserved transport metadata, on the PATCH."""

    @pytest.mark.parametrize(("status", "code", "expected"), UPDATE_FAILURES)
    def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Each documented status raises its own class and keeps the upstream code."""
        api_server.route(LINK_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == LINK_ITEM

    def test_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the 429 response rather than guessed."""
        api_server.route(
            LINK_ITEM,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert exc_info.value.status_code == 429
        assert exc_info.value.error_code == "TOO_MANY_REQUESTS"
        assert exc_info.value.retry_after == 30
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == LINK_ITEM

    def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """X-Request-Id and X-Span-Id on the failing response are reachable on the exception."""
        api_server.route(
            LINK_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-ll-500", "X-Span-Id": "span-ll-500"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert exc_info.value.request_id == "req-ll-500"
        assert exc_info.value.span_id == "span-ll-500"

    def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer) -> None:
        """No exception stringifies the credential, whoever ends up logging it."""
        api_server.route(LINK_ITEM, ScriptedResponse(status=401, json_body=_error_envelope("UNAUTHORIZED", "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestLoginLinksErrorsAcrossVerbs:
    """The taxonomy holds on every verb, not only on the PATCH.

    Each test pairs a different documented status with a different HTTP method, so a
    classification regression confined to one adapter cannot hide behind a green
    ``update``. ``create`` is the only POST, ``close`` is the only bodyless PUT, and both
    ``get`` and ``list`` are GETs that must raise rather than degrade to ``None`` or ``[]``.
    """

    def test_create_unauthorized_is_classified(self, api_server: MockAPIServer) -> None:
        """A 401 on the POST is an auth error, and the request still went out."""
        api_server.route(
            LINK_CREATE,
            ScriptedResponse(status=401, json_body=_error_envelope("UNAUTHORIZED", "expired")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                client.login_links.create(ds_id="GAWA", description="Q4 Analytics Setup")

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "UNAUTHORIZED"
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.path == LINK_CREATE

    def test_get_not_found_is_classified(self, api_server: MockAPIServer) -> None:
        """A 404 on the by-id GET is a not-found error, not a missing-data 200."""
        api_server.route(
            LINK_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such link")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.login_links.get(LINK_ID)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == LINK_ITEM

    def test_list_server_error_is_classified(self, api_server: MockAPIServer) -> None:
        """A failing collection GET raises instead of degrading to an empty list."""
        api_server.route(
            LINK_LIST,
            ScriptedResponse(status=500, json_body=_error_envelope("INTERNAL_SERVER_ERROR", "boom")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.login_links.list()

        assert exc_info.value.status_code == 500
        assert exc_info.value.error_code == "INTERNAL_SERVER_ERROR"
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == LINK_LIST

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_close_failures_raise_rather_than_return_none(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """``close`` returns ``None`` at 200, so every non-200 on the PUT must raise."""
        api_server.route(LINK_CLOSE, ScriptedResponse(status=status, json_body=_error_envelope(code, "no")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.login_links.close(LINK_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "PUT"
        assert api_server.last_request.path == LINK_CLOSE


class TestLoginLinksAsyncUpdateErrorTaxonomy:
    """The async surface has its own event hooks and its own error paths."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), UPDATE_FAILURES)
    async def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async adapter classifies a failing PATCH identically to the sync one."""
        api_server.route(LINK_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == LINK_ITEM

    @pytest.mark.asyncio
    async def test_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After survives the async error path with its value intact."""
        api_server.route(
            LINK_ITEM,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                await client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == LINK_ITEM

    @pytest.mark.asyncio
    async def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """Correlation headers reach the exception on the async path too."""
        api_server.route(
            LINK_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-ll-async-500", "X-Span-Id": "span-ll-async-500"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert exc_info.value.request_id == "req-ll-async-500"
        assert exc_info.value.span_id == "span-ll-async-500"

    @pytest.mark.asyncio
    async def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer) -> None:
        """Credential hygiene holds on the async path."""
        api_server.route(LINK_ITEM, ScriptedResponse(status=401, json_body=_error_envelope("UNAUTHORIZED", "bad")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestLoginLinksAsyncErrorsAcrossVerbs:
    """The across-verbs taxonomy holds on the async client as well."""

    @pytest.mark.asyncio
    async def test_create_unauthorized_is_classified(self, api_server: MockAPIServer) -> None:
        """A 401 on the async POST is an auth error."""
        api_server.route(
            LINK_CREATE,
            ScriptedResponse(status=401, json_body=_error_envelope("UNAUTHORIZED", "expired")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.login_links.create(ds_id="GAWA", description="Q4 Analytics Setup")

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "UNAUTHORIZED"
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.path == LINK_CREATE

    @pytest.mark.asyncio
    async def test_get_not_found_is_classified(self, api_server: MockAPIServer) -> None:
        """A 404 on the async by-id GET is a not-found error."""
        api_server.route(
            LINK_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such link")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await client.login_links.get(LINK_ID)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == LINK_ITEM

    @pytest.mark.asyncio
    async def test_list_server_error_is_classified(self, api_server: MockAPIServer) -> None:
        """A failing collection GET raises on the async client too."""
        api_server.route(
            LINK_LIST,
            ScriptedResponse(status=500, json_body=_error_envelope("INTERNAL_SERVER_ERROR", "boom")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.login_links.list()

        assert exc_info.value.status_code == 500
        assert exc_info.value.error_code == "INTERNAL_SERVER_ERROR"
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == LINK_LIST

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    async def test_close_failures_raise_rather_than_return_none(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async ``close`` reads the same status branch, and the same way to get it wrong."""
        api_server.route(LINK_CLOSE, ScriptedResponse(status=status, json_body=_error_envelope(code, "no")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.login_links.close(LINK_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "PUT"
        assert api_server.last_request.path == LINK_CLOSE
