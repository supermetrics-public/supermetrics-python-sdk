"""End-to-end tests for the Accounts resource.

Drives the single ``list`` method over a real loopback socket. Accounts are served from
the core API host at ``/query/accounts`` — no ``/v1`` prefix and no re-hosting to the Data
Warehouse host — so one server is the whole story here.

The one wire fact worth staring at: this is a ``GET`` and the resource's request model —
``ds_id``, ``ds_users``, ``cache_minutes`` — travels in the *query string*, not a JSON
body, even though the adapter names its argument ``json=``. The generated layer folds
``GetAccountsJson.to_dict()`` into ``params`` and sends no body at all. A mocked transport
cannot see that; asserting on ``last_request.path`` / ``.body`` is the point of this layer.

The second fact is the flattening: the API answers one entry per login, each carrying its
own ``accounts`` array, and the adapter concatenates them into a single flat list. So a
two-login response with 2 + 1 accounts must come back as one list of 3, in order.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: The one route these tests touch. No ``/v1`` prefix: accounts are a query endpoint on the
#: core host, not a versioned management resource.
ACCOUNTS_PATH = "/query/accounts"

#: A two-login response. The first login owns two accounts, the second owns one, so the
#: flattened result has to be 3 long and preserve arrival order. ``group_name`` is an empty
#: string on the middle account — the schema documents that as "not available", and the
#: adapter must surface it verbatim rather than dropping the field. ``cache_time`` is a
#: real ISO timestamp on the first login and ``null`` on the second, exercising both arms
#: of the nullable parse even though ``list`` never returns the login wrapper itself.
ACCOUNTS_LIST_BODY: dict[str, Any] = {
    "meta": {"request_id": "req_0123456789abcdef"},
    "data": [
        {
            "ds_user": "user1@example.com",
            "display_name": "User One",
            "cache_time": "2026-01-01T00:00:00Z",
            "accounts": [
                {"account_id": "111", "account_name": "Acme Corp", "group_name": "Group A"},
                {"account_id": "222", "account_name": "Beta LLC", "group_name": ""},
            ],
        },
        {
            "ds_user": "user2@example.com",
            "display_name": "User Two",
            "cache_time": None,
            "accounts": [
                {"account_id": "333", "account_name": "Gamma Inc", "group_name": "Group B"},
            ],
        },
    ],
}

#: A response whose ``data`` array is present but empty. The adapter iterates it and returns
#: ``[]`` rather than falling over.
ACCOUNTS_EMPTY_DATA_BODY: dict[str, Any] = {"meta": {"request_id": "req_empty"}, "data": []}

#: A response with no ``data`` key at all. ``data`` is optional upstream (``Unset``), and the
#: adapter guards for exactly that before iterating, so a bare envelope is an empty list too,
#: not an ``AttributeError``.
ACCOUNTS_NO_DATA_BODY: dict[str, Any] = {"meta": {"request_id": "req_no_data"}}


class TestAccountsResource:
    """Synchronous account listing."""

    def test_list_flattens_accounts_across_logins(self, api_server: MockAPIServer) -> None:
        """One entry per login, each with its own ``accounts`` — the adapter concatenates.

        Two logins carrying 2 + 1 accounts come back as a single list of 3, in the order the
        API laid them out, with the login wrapper (``ds_user``, ``cache_time``) dropped.
        """
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = client.accounts.list(ds_id="GAWA")

        assert [a.account_id for a in accounts] == ["111", "222", "333"]
        assert accounts[0].account_name == "Acme Corp"
        assert accounts[0].group_name == "Group A"
        # The empty group_name is surfaced verbatim, not coerced away.
        assert accounts[1].group_name == ""
        assert accounts[2].account_name == "Gamma Inc"

    def test_list_sends_a_get_with_ds_id_in_the_query_and_no_body(self, api_server: MockAPIServer) -> None:
        """The request model rides in the query string of a bodyless GET.

        Despite the adapter naming its argument ``json=``, ``ds_id`` lands in the query and
        the body is genuinely empty. Only ``ds_id`` is sent when no optional filter is given —
        ``ds_users`` and ``cache_minutes`` stay off the wire entirely (they are ``UNSET``).
        """
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.accounts.list(ds_id="GAWA")

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == ACCOUNTS_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""

        query = parse_qs(urlsplit(request.path).query)
        assert query == {"ds_id": ["GAWA"]}

    def test_list_serializes_a_single_login_username(self, api_server: MockAPIServer) -> None:
        """A single ``login_usernames`` string becomes one ``ds_users`` query parameter."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.accounts.list(ds_id="GAWA", login_usernames="user@example.com")

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {"ds_id": ["GAWA"], "ds_users": ["user@example.com"]}

    def test_list_serializes_multiple_login_usernames_as_repeated_params(self, api_server: MockAPIServer) -> None:
        """A list of usernames serializes to repeated ``ds_users`` keys, not a joined string."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.accounts.list(
                ds_id="GAWA",
                login_usernames=["user1@example.com", "user2@example.com"],
            )

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {
            "ds_id": ["GAWA"],
            "ds_users": ["user1@example.com", "user2@example.com"],
        }

    def test_list_serializes_cache_minutes_as_a_string(self, api_server: MockAPIServer) -> None:
        """``cache_minutes`` is an int in Python and a decimal string on the wire."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.accounts.list(ds_id="GAWA", cache_minutes=60)

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {"ds_id": ["GAWA"], "cache_minutes": ["60"]}

    def test_list_returns_empty_list_when_data_is_empty(self, api_server: MockAPIServer) -> None:
        """An empty ``data`` array is not an error — it is zero accounts."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_EMPTY_DATA_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = client.accounts.list(ds_id="GAWA")

        assert accounts == []

    def test_list_returns_empty_list_when_data_key_is_absent(self, api_server: MockAPIServer) -> None:
        """``data`` is optional upstream; a bare envelope answers ``[]``, not an error."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_NO_DATA_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = client.accounts.list(ds_id="GAWA")

        assert accounts == []


class TestAccountsAsyncResource:
    """Asynchronous account listing — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_flattens_accounts_across_logins(self, api_server: MockAPIServer) -> None:
        """The async path flattens the per-login arrays identically."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = await client.accounts.list(ds_id="GAWA")

        assert [a.account_id for a in accounts] == ["111", "222", "333"]
        assert accounts[1].group_name == ""

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == ACCOUNTS_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""
        assert parse_qs(urlsplit(request.path).query) == {"ds_id": ["GAWA"]}

    @pytest.mark.asyncio
    async def test_list_serializes_multiple_login_usernames_as_repeated_params(self, api_server: MockAPIServer) -> None:
        """Repeated ``ds_users`` keys are how a username list reaches the wire, async too."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.accounts.list(
                ds_id="GAWA",
                login_usernames=["user1@example.com", "user2@example.com"],
                cache_minutes=30,
            )

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {
            "ds_id": ["GAWA"],
            "ds_users": ["user1@example.com", "user2@example.com"],
            "cache_minutes": ["30"],
        }

    @pytest.mark.asyncio
    async def test_list_returns_empty_list_when_data_key_is_absent(self, api_server: MockAPIServer) -> None:
        """A bare envelope is an empty list on the async client as well."""
        api_server.route(ACCOUNTS_PATH, ScriptedResponse(json_body=ACCOUNTS_NO_DATA_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = await client.accounts.list(ds_id="GAWA")

        assert accounts == []
