"""End-to-end tests for per-request overrides on Logins calls.

The Logins domain reaches the wire with three request shapes the override
machinery has to treat identically: bodyless GETs (``get``, ``list``), a GET that
always carries ``offset``/``limit`` query params (``get_accounts``), and a
bodyless DELETE (``revoke``) — a verb no other read-style resource uses. The
override plumbing lives in the client's transport event hooks, not in the
adapter, so nothing in the adapter code proves a DELETE gets the same
``auth_token``/``headers``/``timeout`` treatment as a GET; only a real socket
can. These tests pin all three overrides down on every shape, on both clients,
asserting on what the server received rather than on what the client returned.

The routes and the accounts/revoke bodies are local to this module rather than
shared through ``conftest``: these tests script per-route delays and
multi-response sequences that a shared "everything wired to a 200" fixture would
get in the way of. ``get`` and ``revoke`` share the ``/ds/login/{login_id}``
path and are told apart only by verb, so the revoke tests re-route that path to
the revoke body themselves.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import NetworkError

from .conftest import LOGIN_GET_BODY, LOGINS_LIST_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: Logins live on the core API host at the bare ``/ds/...`` paths — no ``/v1`` prefix and
#: no re-host to the Data Warehouse host. ``get`` (GET) and ``revoke`` (DELETE) share the
#: item path; routing is keyed by path, so one route serves both verbs.
LOGIN_ID = "login_abc123"
LOGIN_ITEM = f"/ds/login/{LOGIN_ID}"
LOGINS_COLLECTION = "/ds/logins"
LOGIN_ACCOUNTS = f"/ds/login/{LOGIN_ID}/accounts"

#: ``get_accounts`` response: ``data`` is a list of ``DataSourceAccount`` (``@type`` maps to
#: ``type_``) and the total rides in ``meta.paginate``.
ACCOUNTS_BODY: dict[str, Any] = {
    "meta": {"request_id": "req_00000000", "paginate": {"offset": 0, "limit": 100, "total": 1}},
    "data": [{"@type": "ds_account", "account_id": "acc_1", "name": "Account One", "group": "Group A"}],
}

#: ``revoke`` response: a wrapped boolean at ``data.result``.
REVOKE_BODY: dict[str, Any] = {"meta": {"request_id": "req_00000000"}, "data": {"result": True}}


@pytest.fixture
def logins_override_server(api_server: MockAPIServer) -> Iterator[MockAPIServer]:
    """A server with the four Logins routes wired to 200s.

    The item route answers ``get``'s login body; revoke tests re-route it to
    ``REVOKE_BODY`` because DELETE and GET share that path.
    """
    api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))
    api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=LOGIN_GET_BODY))
    api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=ACCOUNTS_BODY))
    yield api_server


class TestLoginsAuthTokenOverrideResource:
    """`auth_token=` beats the client credential, for exactly one call."""

    def test_auth_token_overrides_the_client_credential_on_get(self, logins_override_server: MockAPIServer) -> None:
        """The scoped token is used for that GET only; the next reverts to the client key."""
        with SupermetricsClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            client.logins.get(LOGIN_ID, auth_token="otok_scoped")
            client.logins.get(LOGIN_ID)

        assert [r.bearer_token for r in logins_override_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in logins_override_server.requests] == ["GET", "GET"]
        assert logins_override_server.last_request.path == LOGIN_ITEM

    def test_auth_token_override_on_list(self, logins_override_server: MockAPIServer) -> None:
        """`list` scopes the credential the same way, reverting on the following call."""
        with SupermetricsClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            client.logins.list(auth_token="otok_scoped")
            client.logins.list()

        assert [r.bearer_token for r in logins_override_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in logins_override_server.requests] == ["GET", "GET"]

    def test_auth_token_override_on_get_accounts(self, logins_override_server: MockAPIServer) -> None:
        """`get_accounts` is a GET with query params; the override still scopes to one call."""
        with SupermetricsClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            client.logins.get_accounts(LOGIN_ID, auth_token="otok_scoped")
            client.logins.get_accounts(LOGIN_ID)

        assert [r.bearer_token for r in logins_override_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in logins_override_server.requests] == ["GET", "GET"]
        # The pagination query rides along regardless of the credential in play.
        path = logins_override_server.last_request.path
        assert "offset=0" in path
        assert "limit=100" in path

    def test_auth_token_override_on_revoke(self, logins_override_server: MockAPIServer) -> None:
        """DELETE is generated separately from the GETs, so the override is proven on it too."""
        api_server = logins_override_server
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            assert client.logins.revoke(LOGIN_ID, auth_token="otok_scoped") is True
            assert client.logins.revoke(LOGIN_ID) is True

        assert [r.bearer_token for r in api_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in api_server.requests] == ["DELETE", "DELETE"]
        assert api_server.last_request.path == LOGIN_ITEM


class TestLoginsHeaderOverrideResource:
    """`headers=` reaches the wire and outranks the client's own defaults."""

    def test_headers_reach_the_wire_on_get(self, logins_override_server: MockAPIServer) -> None:
        """Correlation and idempotency headers are sent, recorded lower-cased."""
        with SupermetricsClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            client.logins.get(LOGIN_ID, headers={"X-Span-Id": "span-get-1", "Idempotency-Key": "idem-get-1"})

        received = logins_override_server.last_request.headers
        assert received["x-span-id"] == "span-get-1"
        assert received["idempotency-key"] == "idem-get-1"

    def test_headers_merge_over_client_defaults_case_insensitively(self, logins_override_server: MockAPIServer) -> None:
        """A lower-cased per-request header replaces a differently-cased client one."""
        with SupermetricsClient(
            api_key="api_k",
            base_url=logins_override_server.base_url,
            custom_headers={"X-Team-ID": "client-level", "X-Tenant": "acme"},
        ) as client:
            client.logins.list()
            client.logins.list(headers={"x-team-id": "request-level"})

        first, second = logins_override_server.requests
        assert first.headers["x-team-id"] == "client-level"
        # The collision is resolved in the request's favour, and only that header moves:
        # the untouched client default and the SDK's own User-Agent both survive.
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-tenant"] == "acme"
        assert second.headers["user-agent"].startswith("supermetrics-sdk/")

    def test_headers_do_not_leak_into_the_next_call(self, logins_override_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            client.logins.get(LOGIN_ID, headers={"X-Span-Id": "only-once"})
            client.logins.get(LOGIN_ID)

        assert logins_override_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in logins_override_server.requests[1].headers

    def test_headers_on_get_accounts(self, logins_override_server: MockAPIServer) -> None:
        """The query-bearing GET carries per-request headers alongside its pagination params."""
        with SupermetricsClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            client.logins.get_accounts(LOGIN_ID, headers={"X-Span-Id": "span-accounts-1"})

        request = logins_override_server.last_request
        assert request.method == "GET"
        assert request.headers["x-span-id"] == "span-accounts-1"
        assert "offset=0" in request.path
        assert "limit=100" in request.path

    def test_headers_on_revoke(self, logins_override_server: MockAPIServer) -> None:
        """The DELETE path carries per-request headers too, with no body."""
        api_server = logins_override_server
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.logins.revoke(LOGIN_ID, headers={"Idempotency-Key": "idem-revoke-1"})

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.headers["idempotency-key"] == "idem-revoke-1"
        assert request.body == b""


class TestLoginsTimeoutOverrideResource:
    """`timeout=` overrides the client budget in both directions, against a real delay."""

    def test_short_override_times_out_a_slow_read(self, api_server: MockAPIServer) -> None:
        """A 0.2s override fails against an endpoint the 30s client budget would tolerate."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.logins.list(timeout=0.2)

    def test_generous_override_beats_a_tight_client_timeout_on_a_read(self, api_server: MockAPIServer) -> None:
        """Against the same 0.6s endpoint, the client's 0.2s budget fails and 10s succeeds."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=0.2) as client:
            with pytest.raises(NetworkError):
                client.logins.list()
            logins = client.logins.list(timeout=10.0)

        assert [login.login_id for login in logins] == [LOGIN_ID]

    def test_timeout_override_on_get_accounts(self, api_server: MockAPIServer) -> None:
        """`get_accounts` against one slow route: 0.2s raises, 10s returns the accounts."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=ACCOUNTS_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.logins.get_accounts(LOGIN_ID, timeout=0.2)
            accounts = client.logins.get_accounts(LOGIN_ID, timeout=httpx.Timeout(10.0))

        assert [account.account_id for account in accounts] == ["acc_1"]
        assert api_server.last_request.method == "GET"

    def test_timeout_override_on_revoke(self, api_server: MockAPIServer) -> None:
        """The same two directions on `revoke`, which is a DELETE."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_BODY, delay=0.6))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.logins.revoke(LOGIN_ID, timeout=0.2)
            revoked = client.logins.revoke(LOGIN_ID, timeout=10.0)

        assert revoked is True
        assert api_server.last_request.method == "DELETE"

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout failure the client-level budget applies again."""
        api_server.route(
            LOGINS_COLLECTION,
            ScriptedResponse(json_body=LOGINS_LIST_BODY, delay=0.6),
            ScriptedResponse(json_body=LOGINS_LIST_BODY),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.logins.list(timeout=0.2)
            assert len(client.logins.list()) == 1


class TestLoginsOverridesAsyncResource:
    """The async surface applies every one of the same overrides."""

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_on_get(
        self, logins_override_server: MockAPIServer
    ) -> None:
        """The async client scopes the override to a single awaited GET."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            await client.logins.get(LOGIN_ID, auth_token="otok_scoped")
            await client.logins.get(LOGIN_ID)

        assert [r.bearer_token for r in logins_override_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in logins_override_server.requests] == ["GET", "GET"]

    @pytest.mark.asyncio
    async def test_auth_token_override_on_list(self, logins_override_server: MockAPIServer) -> None:
        """`list` on the async client reverts to the client credential afterwards."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            await client.logins.list(auth_token="otok_scoped")
            await client.logins.list()

        assert [r.bearer_token for r in logins_override_server.requests] == ["otok_scoped", "api_k"]

    @pytest.mark.asyncio
    async def test_auth_token_override_on_get_accounts(self, logins_override_server: MockAPIServer) -> None:
        """The query-bearing GET scopes the credential on the async client too."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            await client.logins.get_accounts(LOGIN_ID, auth_token="otok_scoped")
            await client.logins.get_accounts(LOGIN_ID)

        assert [r.bearer_token for r in logins_override_server.requests] == ["otok_scoped", "api_k"]
        assert "offset=0" in logins_override_server.last_request.path
        assert "limit=100" in logins_override_server.last_request.path

    @pytest.mark.asyncio
    async def test_auth_token_override_on_revoke(self, logins_override_server: MockAPIServer) -> None:
        """DELETE on the async client reverts to the client credential afterwards."""
        api_server = logins_override_server
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            assert await client.logins.revoke(LOGIN_ID, auth_token="otok_scoped") is True
            assert await client.logins.revoke(LOGIN_ID) is True

        assert [r.bearer_token for r in api_server.requests] == ["otok_scoped", "api_k"]
        assert [r.method for r in api_server.requests] == ["DELETE", "DELETE"]

    @pytest.mark.asyncio
    async def test_headers_merge_over_client_defaults_case_insensitively(
        self, logins_override_server: MockAPIServer
    ) -> None:
        """Async header merging resolves a cased collision in the request's favour."""
        async with SupermetricsAsyncClient(
            api_key="api_k", base_url=logins_override_server.base_url, custom_headers={"X-Team-ID": "client-level"}
        ) as client:
            await client.logins.list()
            await client.logins.list(headers={"x-team-id": "request-level", "X-Span-Id": "async-span"})

        first, second = logins_override_server.requests
        assert first.headers["x-team-id"] == "client-level"
        assert "x-span-id" not in first.headers
        assert second.headers["x-team-id"] == "request-level"
        assert second.headers["x-span-id"] == "async-span"

    @pytest.mark.asyncio
    async def test_headers_on_get_accounts(self, logins_override_server: MockAPIServer) -> None:
        """Per-request headers reach the wire on the async query-bearing GET."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=logins_override_server.base_url) as client:
            await client.logins.get_accounts(LOGIN_ID, headers={"Idempotency-Key": "idem-async-accounts"})

        request = logins_override_server.last_request
        assert request.method == "GET"
        assert request.headers["idempotency-key"] == "idem-async-accounts"
        assert "offset=0" in request.path
        assert "limit=100" in request.path

    @pytest.mark.asyncio
    async def test_timeout_override_in_both_directions_on_get_accounts(self, api_server: MockAPIServer) -> None:
        """Against one 0.6s route the async client fails at 0.2s and succeeds at 10s."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=ACCOUNTS_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.logins.get_accounts(LOGIN_ID, timeout=0.2)
            accounts = await client.logins.get_accounts(LOGIN_ID, timeout=10.0)

        assert [account.account_id for account in accounts] == ["acc_1"]

    @pytest.mark.asyncio
    async def test_timeout_override_on_revoke(self, api_server: MockAPIServer) -> None:
        """`revoke` on the async client honours both a tight and a generous override."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_BODY, delay=0.6))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                await client.logins.revoke(LOGIN_ID, timeout=0.2)
            revoked = await client.logins.revoke(LOGIN_ID, timeout=10.0)

        assert revoked is True
        assert api_server.last_request.method == "DELETE"
