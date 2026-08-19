"""End-to-end tests for per-request overrides on account-tag calls.

Account tags are the first domain to reach the wire with three distinct request
shapes: a bodyless read, a POST that carries a body, and a PATCH — a verb no
earlier resource used. The override machinery lives in the client's transport
event hooks, not in the adapter, so it is not obvious from the code that a PATCH
gets the same treatment as a GET; the only place that can be established is a
real socket. These tests pin ``auth_token``, ``headers`` and ``timeout`` down on
all three shapes, on both clients, asserting on what the server received rather
than on what the client returned.

The route constants and payloads are local to this module rather than shared
through ``conftest``: this file scripts per-route delays and multi-response
sequences that a shared "everything wired to a 200" fixture would get in the way
of.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import NetworkError

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: Account tags live on the core API host with ``/v1`` in the path, so every route
#: string here carries the prefix. Dropping it would surface as the mock server's
#: default 404 rather than as an obvious mistake.
TEAM_ID = 936506
TAG_NAME = "a1b2c3d"
ACCOUNT_TAGS_COLLECTION = f"/v1/teams/{TEAM_ID}/account_tags"
ACCOUNT_TAGS_ITEM = f"{ACCOUNT_TAGS_COLLECTION}/{TAG_NAME}"
ACCOUNT_TAGS_ADD = f"{ACCOUNT_TAGS_ITEM}/add"

#: Membership, in the only shape the spec documents — as an ``example``, since the
#: element schema itself is an open object.
DATA_SOURCES: list[dict[str, Any]] = [{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}]

#: The list item: counts, no membership.
ACCOUNT_TAG_OVERVIEW: dict[str, Any] = {
    "name": TAG_NAME,
    "display_name": "EMEA paid media",
    "color": "#112233",
    "data_source_count": 1,
    "account_count": 1,
}

#: The single-object model: membership, no counts.
ACCOUNT_TAG_PAYLOAD: dict[str, Any] = {
    "name": TAG_NAME,
    "display_name": "EMEA paid media",
    "color": "#112233",
    "data_sources": DATA_SOURCES,
}

#: Neither envelope carries a ``meta`` block in this domain — ``data`` is the whole body.
ACCOUNT_TAG_LIST_BODY: dict[str, Any] = {"data": [ACCOUNT_TAG_OVERVIEW]}
ACCOUNT_TAG_SINGLE_BODY: dict[str, Any] = {"data": ACCOUNT_TAG_PAYLOAD}


@pytest.fixture
def account_tags_server(api_server: MockAPIServer) -> Iterator[MockAPIServer]:
    """A server with the read, create and add-accounts routes wired to 200s.

    ``GET`` and ``POST`` share the collection route, so the one scripted response
    there serves both; the tests that care about the difference assert on
    ``last_request.method``.
    """
    api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY))
    api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))
    api_server.route(ACCOUNT_TAGS_ADD, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))
    yield api_server


class TestAccountTagsAuthTokenOverrideResource:
    """`auth_token=` beats the client credential, for exactly one call."""

    def test_auth_token_overrides_the_client_credential_on_a_read(self, account_tags_server: MockAPIServer) -> None:
        """The scoped token is used for that call only; the next reverts to the client key."""
        with SupermetricsClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            client.account_tags.list(TEAM_ID, auth_token="otok_scoped")
            client.account_tags.list(TEAM_ID)

        assert [r.bearer_token for r in account_tags_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in account_tags_server.requests] == ["GET", "GET"]

    def test_auth_token_override_on_a_body_carrying_write(self, account_tags_server: MockAPIServer) -> None:
        """`create` scopes the credential the same way, and still sends its body."""
        api_server = account_tags_server
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.account_tags.create(TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES, auth_token="otok_scoped")
            client.account_tags.create(TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES)

        assert [r.bearer_token for r in api_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in api_server.requests] == ["POST", "POST"]
        assert api_server.last_request.json() == {
            "display_name": "EMEA paid media",
            "color": "#112233",
            "data_sources": DATA_SOURCES,
        }

    def test_auth_token_override_on_a_patch(self, account_tags_server: MockAPIServer) -> None:
        """PATCH is generated separately from POST, so the override is proven on it too."""
        with SupermetricsClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES, auth_token="otok_scoped")
            client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES)

        assert [r.bearer_token for r in account_tags_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in account_tags_server.requests] == ["PATCH", "PATCH"]
        assert account_tags_server.last_request.path == ACCOUNT_TAGS_ADD
        assert account_tags_server.last_request.json() == {"data_sources": DATA_SOURCES}


class TestAccountTagsHeaderOverrideResource:
    """`headers=` reaches the wire and outranks the client's own defaults."""

    def test_headers_reach_the_wire_on_a_read(self, account_tags_server: MockAPIServer) -> None:
        """Correlation and idempotency headers are sent, recorded lower-cased."""
        with SupermetricsClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            client.account_tags.list(TEAM_ID, headers={"X-Span-Id": "span-at-1", "Idempotency-Key": "idem-at-1"})

        received = account_tags_server.last_request.headers
        assert received["x-span-id"] == "span-at-1"
        assert received["idempotency-key"] == "idem-at-1"

    def test_headers_merge_over_client_defaults_case_insensitively(self, account_tags_server: MockAPIServer) -> None:
        """A lower-cased per-request header replaces a differently-cased client one."""
        with SupermetricsClient(
            api_key="api_k",
            base_url=account_tags_server.base_url,
            custom_headers={"X-Team-ID": "client-level", "X-Tenant": "acme"},
        ) as client:
            client.account_tags.list(TEAM_ID)
            client.account_tags.list(TEAM_ID, headers={"x-team-id": "request-level"})

        first, second = account_tags_server.requests
        assert first.headers["x-team-id"] == "client-level"
        # The collision is resolved in the request's favour, and only that header moves:
        # the untouched client default and the SDK's own User-Agent both survive.
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-tenant"] == "acme"
        assert second.headers["user-agent"].startswith("supermetrics-sdk/")

    def test_headers_do_not_leak_into_the_next_call(self, account_tags_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            client.account_tags.list(TEAM_ID, headers={"X-Span-Id": "only-once"})
            client.account_tags.list(TEAM_ID)

        assert account_tags_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in account_tags_server.requests[1].headers

    def test_headers_on_a_body_carrying_write(self, account_tags_server: MockAPIServer) -> None:
        """An idempotency key on `create` reaches the wire alongside the JSON body."""
        api_server = account_tags_server
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(
            api_key="api_k", base_url=api_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            client.account_tags.create(
                TEAM_ID,
                "EMEA paid media",
                "#112233",
                DATA_SOURCES,
                headers={"Idempotency-Key": "idem-create-1", "x-team-id": "request-level"},
            )

        request = api_server.last_request
        assert request.method == "POST"
        assert request.headers["idempotency-key"] == "idem-create-1"
        assert request.headers["x-team-id"] == "request-level"
        assert request.json() == {
            "display_name": "EMEA paid media",
            "color": "#112233",
            "data_sources": DATA_SOURCES,
        }

    def test_headers_on_a_patch(self, account_tags_server: MockAPIServer) -> None:
        """The PATCH routes carry per-request headers too, body untouched."""
        with SupermetricsClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES, headers={"X-Span-Id": "span-patch-1"})

        request = account_tags_server.last_request
        assert request.method == "PATCH"
        assert request.headers["x-span-id"] == "span-patch-1"
        assert request.json() == {"data_sources": DATA_SOURCES}


class TestAccountTagsTimeoutOverrideResource:
    """`timeout=` overrides the client budget in both directions, against a real delay."""

    def test_short_override_times_out_a_slow_read(self, api_server: MockAPIServer) -> None:
        """A 0.2s override fails against an endpoint the 30s client budget would tolerate."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.account_tags.list(TEAM_ID, timeout=0.2)

    def test_generous_override_beats_a_tight_client_timeout_on_a_read(self, api_server: MockAPIServer) -> None:
        """Against the same 0.6s endpoint, the client's 0.2s budget fails and 10s succeeds."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=0.2) as client:
            with pytest.raises(NetworkError):
                client.account_tags.list(TEAM_ID)
            tags = client.account_tags.list(TEAM_ID, timeout=10.0)

        assert [tag.name for tag in tags] == [TAG_NAME]

    def test_timeout_override_on_a_body_carrying_write(self, api_server: MockAPIServer) -> None:
        """`create` against one slow route: 0.2s raises, 10s returns the created tag."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.account_tags.create(TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES, timeout=0.2)
            tag = client.account_tags.create(
                TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES, timeout=httpx.Timeout(10.0)
            )

        assert tag.name == TAG_NAME
        assert api_server.last_request.method == "POST"

    def test_timeout_override_on_a_patch(self, api_server: MockAPIServer) -> None:
        """The same two directions on `add_accounts`, which is a PATCH."""
        api_server.route(ACCOUNT_TAGS_ADD, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES, timeout=0.2)
            tag = client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES, timeout=10.0)

        assert tag.name == TAG_NAME
        assert api_server.last_request.method == "PATCH"

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout failure the client-level budget applies again."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY, delay=0.6),
            ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.account_tags.list(TEAM_ID, timeout=0.2)
            assert len(client.account_tags.list(TEAM_ID)) == 1


class TestAccountTagsOverridesAsyncResource:
    """The async surface applies every one of the same overrides."""

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_on_a_read(
        self, account_tags_server: MockAPIServer
    ) -> None:
        """The async client scopes the override to a single awaited call."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            await client.account_tags.list(TEAM_ID, auth_token="otok_scoped")
            await client.account_tags.list(TEAM_ID)

        assert [r.bearer_token for r in account_tags_server.requests] == ["otok_scoped", "api_k"]

    @pytest.mark.asyncio
    async def test_auth_token_override_on_a_body_carrying_write(self, account_tags_server: MockAPIServer) -> None:
        """`create` on the async client scopes the credential and sends the same body."""
        api_server = account_tags_server
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.account_tags.create(
                TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES, auth_token="otok_scoped"
            )
            await client.account_tags.create(TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES)

        assert [r.bearer_token for r in api_server.requests] == ["otok_scoped", "api_k"]
        assert api_server.last_request.json() == {
            "display_name": "EMEA paid media",
            "color": "#112233",
            "data_sources": DATA_SOURCES,
        }

    @pytest.mark.asyncio
    async def test_auth_token_override_on_a_patch(self, account_tags_server: MockAPIServer) -> None:
        """PATCH on the async client reverts to the client credential afterwards."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            await client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES, auth_token="otok_scoped")
            await client.account_tags.add_accounts(TEAM_ID, TAG_NAME, DATA_SOURCES)

        assert [r.bearer_token for r in account_tags_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in account_tags_server.requests] == ["PATCH", "PATCH"]

    @pytest.mark.asyncio
    async def test_headers_merge_over_client_defaults_case_insensitively(
        self, account_tags_server: MockAPIServer
    ) -> None:
        """Async header merging resolves a cased collision in the request's favour."""
        async with SupermetricsAsyncClient(
            api_key="api_k", base_url=account_tags_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            await client.account_tags.list(TEAM_ID)
            await client.account_tags.list(TEAM_ID, headers={"x-team-id": "request-level", "X-Span-Id": "async-span"})

        first, second = account_tags_server.requests
        assert first.headers["x-team-id"] == "client-level"
        assert "x-span-id" not in first.headers
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-span-id"] == "async-span"

    @pytest.mark.asyncio
    async def test_headers_on_a_patch(self, account_tags_server: MockAPIServer) -> None:
        """Per-request headers reach the wire on the async PATCH path."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=account_tags_server.base_url) as client:
            await client.account_tags.add_accounts(
                TEAM_ID, TAG_NAME, DATA_SOURCES, headers={"Idempotency-Key": "idem-async-patch"}
            )

        request = account_tags_server.last_request
        assert request.method == "PATCH"
        assert request.path == ACCOUNT_TAGS_ADD
        assert request.headers["idempotency-key"] == "idem-async-patch"
        assert request.json() == {"data_sources": DATA_SOURCES}

    @pytest.mark.asyncio
    async def test_timeout_override_in_both_directions_on_a_read(self, api_server: MockAPIServer) -> None:
        """Against one 0.6s route the async client fails at 0.2s and succeeds at 10s."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.account_tags.list(TEAM_ID, timeout=0.2)
            tags = await client.account_tags.list(TEAM_ID, timeout=10.0)

        assert [tag.name for tag in tags] == [TAG_NAME]

    @pytest.mark.asyncio
    async def test_timeout_override_on_a_body_carrying_write(self, api_server: MockAPIServer) -> None:
        """`create` on the async client honours both a tight and a generous override."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.account_tags.create(TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES, timeout=0.2)
            tag = await client.account_tags.create(TEAM_ID, "EMEA paid media", "#112233", DATA_SOURCES, timeout=10.0)

        assert tag.name == TAG_NAME
        assert api_server.last_request.method == "POST"
