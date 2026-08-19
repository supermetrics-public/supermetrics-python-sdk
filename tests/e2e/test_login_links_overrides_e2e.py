"""End-to-end tests for per-request overrides on login-link calls.

Login links reach the wire with three distinct request shapes: a bodyless read
(``get``), a POST that carries a body (``create``), and a PATCH (``update``) — a
verb no other login-domain call uses. The override machinery lives in the
client's transport event hooks, not in the adapter, so nothing in the code makes
it obvious that a PATCH is treated the same as a GET; the only place that can be
established is a real socket. These tests pin ``auth_token``, ``headers`` and
``timeout`` down on all three shapes, on both clients, asserting on what the
server actually received rather than on what the client returned. For ``create``
and ``update`` the outbound JSON body is asserted alongside the override, because
a header or token override that quietly mangled the body would otherwise pass.

The route constants and payloads are local to this module rather than shared
through ``conftest``: this file scripts per-route delays that a shared
"everything wired to a 200" fixture would get in the way of.
"""

from __future__ import annotations

import datetime
from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import NetworkError

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: Login links stay on the core API host (``base_url``) — they are not re-hosted to the
#: Data Warehouse host — so the routes here are bare ``/ds/login/...`` paths with no ``/v1``
#: prefix and no query string. ``create`` POSTs to the collection path while ``get`` and
#: ``update`` share the by-id item path, which is a different route, so both coexist.
LINK_ID = "link_123"
DS_ID = "GAWA"
LOGIN_LINK_CREATE = "/ds/login/link"
LOGIN_LINK_ITEM = f"/ds/login/link/{LINK_ID}"

#: A fixed expiry, passed explicitly so the POST body is deterministic. The generated body
#: serializes it with ``datetime.isoformat()``, so a UTC-aware value comes out with a
#: ``+00:00`` offset rather than a trailing ``Z``.
EXPIRY_TIME = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
EXPIRY_TIME_ISO = "2026-01-02T00:00:00+00:00"

#: The description ``create``/``update`` send and that comes back on the link.
DESCRIPTION = "Q4 Analytics Setup"

#: One login link as the single-object reads and writes return it.
LOGIN_LINK_PAYLOAD: dict[str, Any] = {
    "link_id": LINK_ID,
    "status_code": "OPEN",
    "description": "desc",
    "ds_id": DS_ID,
    "ds_name": "Google Analytics 4",
    "login_url": "https://app.supermetrics.com/login/link_123",
    "created_time": "2026-01-01T00:00:00Z",
    "expiry_time": "2026-01-02T00:00:00Z",
    "login_id": None,
    "login_time": None,
    "login_username": None,
}

#: GET/POST/PATCH of a single link — a plain ``{"data": ...}`` envelope.
LOGIN_LINK_SINGLE_BODY: dict[str, Any] = {"data": LOGIN_LINK_PAYLOAD}

#: The exact POST body ``create`` sends for the arguments used throughout this file.
EXPECTED_CREATE_BODY: dict[str, Any] = {
    "ds_id": DS_ID,
    "expiry_time": EXPIRY_TIME_ISO,
    "description": DESCRIPTION,
}

#: The exact PATCH body ``update`` sends: only ``description``, never anything else.
EXPECTED_UPDATE_BODY: dict[str, Any] = {"description": DESCRIPTION}


@pytest.fixture
def login_links_server(api_server: MockAPIServer) -> Iterator[MockAPIServer]:
    """A server with the create, get and update routes wired to 200s.

    ``get`` and ``update`` share the by-id item route, so the one scripted response
    there serves both; the tests that care about the difference assert on
    ``last_request.method``. Creation answers ``201`` — the generated client only
    parses that status as success, so a ``200`` here would leave ``response.parsed``
    unset and the adapter would fall over rather than return the link.
    """
    api_server.route(LOGIN_LINK_CREATE, ScriptedResponse(status=201, json_body=LOGIN_LINK_SINGLE_BODY))
    api_server.route(LOGIN_LINK_ITEM, ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY))
    yield api_server


class TestLoginLinksAuthTokenOverrideResource:
    """`auth_token=` beats the client credential, for exactly one call."""

    def test_auth_token_overrides_the_client_credential_on_a_read(self, login_links_server: MockAPIServer) -> None:
        """The scoped token is used for that call only; the next reverts to the client key."""
        with SupermetricsClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            client.login_links.get(LINK_ID, auth_token="otok_scoped")
            client.login_links.get(LINK_ID)

        assert [r.bearer_token for r in login_links_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in login_links_server.requests] == ["GET", "GET"]

    def test_auth_token_override_on_create(self, login_links_server: MockAPIServer) -> None:
        """`create` scopes the credential the same way, and still POSTs its body."""
        with SupermetricsClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            client.login_links.create(
                ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME, auth_token="otok_scoped"
            )
            client.login_links.create(ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME)

        assert [r.bearer_token for r in login_links_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in login_links_server.requests] == ["POST", "POST"]
        assert login_links_server.last_request.path == LOGIN_LINK_CREATE
        assert login_links_server.last_request.json() == EXPECTED_CREATE_BODY

    def test_auth_token_override_on_update(self, login_links_server: MockAPIServer) -> None:
        """PATCH is generated separately from POST, so the override is proven on it too."""
        with SupermetricsClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            client.login_links.update(LINK_ID, DESCRIPTION, auth_token="otok_scoped")
            client.login_links.update(LINK_ID, DESCRIPTION)

        assert [r.bearer_token for r in login_links_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in login_links_server.requests] == ["PATCH", "PATCH"]
        assert login_links_server.last_request.path == LOGIN_LINK_ITEM
        assert login_links_server.last_request.json() == EXPECTED_UPDATE_BODY


class TestLoginLinksHeaderOverrideResource:
    """`headers=` reaches the wire and outranks the client's own defaults."""

    def test_headers_reach_the_wire_on_a_read(self, login_links_server: MockAPIServer) -> None:
        """Correlation and idempotency headers are sent, recorded lower-cased."""
        with SupermetricsClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            client.login_links.get(LINK_ID, headers={"X-Span-Id": "span-ll-1", "Idempotency-Key": "idem-ll-1"})

        received = login_links_server.last_request.headers
        assert received["x-span-id"] == "span-ll-1"
        assert received["idempotency-key"] == "idem-ll-1"

    def test_headers_merge_over_client_defaults_case_insensitively(self, login_links_server: MockAPIServer) -> None:
        """A lower-cased per-request header replaces a differently-cased client one."""
        with SupermetricsClient(
            api_key="api_k",
            base_url=login_links_server.base_url,
            custom_headers={"X-Team-ID": "client-level", "X-Tenant": "acme"},
        ) as client:
            client.login_links.get(LINK_ID)
            client.login_links.get(LINK_ID, headers={"x-team-id": "request-level"})

        first, second = login_links_server.requests
        assert first.headers["x-team-id"] == "client-level"
        # The collision is resolved in the request's favour, and only that header moves:
        # the untouched client default and the SDK's own User-Agent both survive.
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-tenant"] == "acme"
        assert second.headers["user-agent"].startswith("supermetrics-sdk/")

    def test_headers_do_not_leak_into_the_next_call(self, login_links_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            client.login_links.get(LINK_ID, headers={"X-Span-Id": "only-once"})
            client.login_links.get(LINK_ID)

        assert login_links_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in login_links_server.requests[1].headers

    def test_headers_on_create(self, login_links_server: MockAPIServer) -> None:
        """An idempotency key on `create` reaches the wire alongside the JSON body."""
        with SupermetricsClient(
            api_key="api_k", base_url=login_links_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            client.login_links.create(
                ds_id=DS_ID,
                description=DESCRIPTION,
                expiry_time=EXPIRY_TIME,
                headers={"Idempotency-Key": "idem-create-1", "x-team-id": "request-level"},
            )

        request = login_links_server.last_request
        assert request.method == "POST"
        assert request.path == LOGIN_LINK_CREATE
        assert request.headers["idempotency-key"] == "idem-create-1"
        assert request.headers["x-team-id"] == "request-level"
        assert request.json() == EXPECTED_CREATE_BODY

    def test_headers_on_update(self, login_links_server: MockAPIServer) -> None:
        """The PATCH path carries per-request headers too, body untouched."""
        with SupermetricsClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            client.login_links.update(LINK_ID, DESCRIPTION, headers={"X-Span-Id": "span-update-1"})

        request = login_links_server.last_request
        assert request.method == "PATCH"
        assert request.path == LOGIN_LINK_ITEM
        assert request.headers["x-span-id"] == "span-update-1"
        assert request.json() == EXPECTED_UPDATE_BODY


class TestLoginLinksTimeoutOverrideResource:
    """`timeout=` overrides the client budget in both directions, against a real delay."""

    def test_short_override_times_out_a_slow_read(self, api_server: MockAPIServer) -> None:
        """A 0.2s override fails against an endpoint the 30s client budget would tolerate."""
        api_server.route(LOGIN_LINK_ITEM, ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.login_links.get(LINK_ID, timeout=0.2)

    def test_generous_override_beats_a_tight_client_timeout_on_a_read(self, api_server: MockAPIServer) -> None:
        """Against the same 0.6s endpoint, the client's 0.2s budget fails and 10s succeeds."""
        api_server.route(LOGIN_LINK_ITEM, ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=0.2) as client:
            with pytest.raises(NetworkError):
                client.login_links.get(LINK_ID)
            link = client.login_links.get(LINK_ID, timeout=10.0)

        assert link.link_id == LINK_ID

    def test_timeout_override_on_create(self, api_server: MockAPIServer) -> None:
        """`create` against one slow route: 0.2s raises, 10s returns the created link.

        The generous call passes an ``httpx.Timeout`` rather than a float, so the override
        is proven to accept both spellings and the POST body still lands correctly.
        """
        api_server.route(LOGIN_LINK_CREATE, ScriptedResponse(status=201, json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.login_links.create(ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME, timeout=0.2)
            link = client.login_links.create(
                ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME, timeout=httpx.Timeout(10.0)
            )

        assert link.link_id == LINK_ID
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.json() == EXPECTED_CREATE_BODY

    def test_timeout_override_on_update(self, api_server: MockAPIServer) -> None:
        """The same two directions on `update`, which is a PATCH."""
        api_server.route(LOGIN_LINK_ITEM, ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.login_links.update(LINK_ID, DESCRIPTION, timeout=0.2)
            link = client.login_links.update(LINK_ID, DESCRIPTION, timeout=10.0)

        assert link.link_id == LINK_ID
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.json() == EXPECTED_UPDATE_BODY

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout failure the client-level budget applies again."""
        api_server.route(
            LOGIN_LINK_ITEM,
            ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6),
            ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.login_links.get(LINK_ID, timeout=0.2)
            assert client.login_links.get(LINK_ID).link_id == LINK_ID


class TestLoginLinksOverridesAsyncResource:
    """The async surface applies every one of the same overrides."""

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_on_a_read(
        self, login_links_server: MockAPIServer
    ) -> None:
        """The async client scopes the override to a single awaited call."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            await client.login_links.get(LINK_ID, auth_token="otok_scoped")
            await client.login_links.get(LINK_ID)

        assert [r.bearer_token for r in login_links_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in login_links_server.requests] == ["GET", "GET"]

    @pytest.mark.asyncio
    async def test_auth_token_override_on_create(self, login_links_server: MockAPIServer) -> None:
        """`create` on the async client scopes the credential and sends the same body."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            await client.login_links.create(
                ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME, auth_token="otok_scoped"
            )
            await client.login_links.create(ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME)

        assert [r.bearer_token for r in login_links_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in login_links_server.requests] == ["POST", "POST"]
        assert login_links_server.last_request.json() == EXPECTED_CREATE_BODY

    @pytest.mark.asyncio
    async def test_auth_token_override_on_update(self, login_links_server: MockAPIServer) -> None:
        """PATCH on the async client reverts to the client credential afterwards."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            await client.login_links.update(LINK_ID, DESCRIPTION, auth_token="otok_scoped")
            await client.login_links.update(LINK_ID, DESCRIPTION)

        assert [r.bearer_token for r in login_links_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in login_links_server.requests] == ["PATCH", "PATCH"]
        assert login_links_server.last_request.path == LOGIN_LINK_ITEM
        assert login_links_server.last_request.json() == EXPECTED_UPDATE_BODY

    @pytest.mark.asyncio
    async def test_headers_merge_over_client_defaults_case_insensitively(
        self, login_links_server: MockAPIServer
    ) -> None:
        """Async header merging resolves a cased collision in the request's favour."""
        async with SupermetricsAsyncClient(
            api_key="api_k", base_url=login_links_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            await client.login_links.get(LINK_ID)
            await client.login_links.get(LINK_ID, headers={"x-team-id": "request-level", "X-Span-Id": "async-span"})

        first, second = login_links_server.requests
        assert first.headers["x-team-id"] == "client-level"
        assert "x-span-id" not in first.headers
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-span-id"] == "async-span"

    @pytest.mark.asyncio
    async def test_headers_on_create(self, login_links_server: MockAPIServer) -> None:
        """Per-request headers reach the wire on the async POST path, body intact."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            await client.login_links.create(
                ds_id=DS_ID,
                description=DESCRIPTION,
                expiry_time=EXPIRY_TIME,
                headers={"Idempotency-Key": "idem-async-create"},
            )

        request = login_links_server.last_request
        assert request.method == "POST"
        assert request.path == LOGIN_LINK_CREATE
        assert request.headers["idempotency-key"] == "idem-async-create"
        assert request.json() == EXPECTED_CREATE_BODY

    @pytest.mark.asyncio
    async def test_headers_on_update(self, login_links_server: MockAPIServer) -> None:
        """Per-request headers reach the wire on the async PATCH path, body intact."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=login_links_server.base_url) as client:
            await client.login_links.update(LINK_ID, DESCRIPTION, headers={"X-Span-Id": "async-patch-span"})

        request = login_links_server.last_request
        assert request.method == "PATCH"
        assert request.path == LOGIN_LINK_ITEM
        assert request.headers["x-span-id"] == "async-patch-span"
        assert request.json() == EXPECTED_UPDATE_BODY

    @pytest.mark.asyncio
    async def test_timeout_override_in_both_directions_on_a_read(self, api_server: MockAPIServer) -> None:
        """Against one 0.6s route the async client fails at 0.2s and succeeds at 10s."""
        api_server.route(LOGIN_LINK_ITEM, ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.login_links.get(LINK_ID, timeout=0.2)
            link = await client.login_links.get(LINK_ID, timeout=10.0)

        assert link.link_id == LINK_ID

    @pytest.mark.asyncio
    async def test_timeout_override_on_create(self, api_server: MockAPIServer) -> None:
        """`create` on the async client honours both a tight and a generous override."""
        api_server.route(LOGIN_LINK_CREATE, ScriptedResponse(status=201, json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.login_links.create(
                    ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME, timeout=0.2
                )
            link = await client.login_links.create(
                ds_id=DS_ID, description=DESCRIPTION, expiry_time=EXPIRY_TIME, timeout=10.0
            )

        assert link.link_id == LINK_ID
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.json() == EXPECTED_CREATE_BODY

    @pytest.mark.asyncio
    async def test_timeout_override_on_update(self, api_server: MockAPIServer) -> None:
        """`update` on the async client honours both a tight and a generous override."""
        api_server.route(LOGIN_LINK_ITEM, ScriptedResponse(json_body=LOGIN_LINK_SINGLE_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.login_links.update(LINK_ID, DESCRIPTION, timeout=0.2)
            link = await client.login_links.update(LINK_ID, DESCRIPTION, timeout=10.0)

        assert link.link_id == LINK_ID
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.json() == EXPECTED_UPDATE_BODY
