"""End-to-end tests for the Logins resource.

Drives all five methods over a real loopback socket. Logins stay on the core API host —
the paths carry no ``/v1`` prefix and nothing is re-hosted to the Data Warehouse host — so
one server is the whole story here.

Every test asserts on both directions: the parsed return value, and the request that
actually went out. The outbound half is the point of this layer, and several things in
this domain exist only on the wire:

* ``get`` and ``revoke`` share the ``/ds/login/{id}`` path but differ by verb — GET versus
  DELETE — so the method is asserted on every case;
* ``get_by_username`` has no endpoint of its own: it reaches ``GET /ds/logins`` and filters
  client-side, so the wire proof is that a lookup and a ``list`` hit the same path;
* ``get_accounts`` always sends ``offset`` and ``limit`` as query parameters, defaulting to
  ``0``/``100``, and the total count rides in ``meta.paginate`` where only
  ``with_raw_response`` can reach it.

Error mapping and per-request overrides live in their own modules and are not repeated
here.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import LOGIN_GET_BODY, LOGIN_PAYLOAD, LOGINS_LIST_BODY, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: The login these tests address. It matches the ``login_id`` baked into ``LOGIN_PAYLOAD``,
#: so the by-id routes and the payload agree.
LOGIN_ID = "login_abc123"

#: The four login routes, spelled out as literals. There is no ``/v1`` prefix — logins are
#: served from the core API host with the version elsewhere — and ``get``/``revoke`` share
#: the by-id path, differing only by verb.
LOGINS_COLLECTION = "/ds/logins"
LOGIN_ITEM = f"/ds/login/{LOGIN_ID}"
LOGIN_ACCOUNTS = f"/ds/login/{LOGIN_ID}/accounts"

#: One data source account as ``get_accounts`` returns it. ``@type`` deserializes onto the
#: model's ``type_`` field; ``account_id``/``name``/``group`` are the rest.
ACCOUNT_ONE: dict[str, Any] = {
    "@type": "ds_account",
    "account_id": "acc_1",
    "name": "Account One",
    "group": "Group A",
}

#: A second account, so the list assertion has more than one element to prove.
ACCOUNT_TWO: dict[str, Any] = {
    "@type": "ds_account",
    "account_id": "acc_2",
    "name": "Account Two",
    "group": "Group B",
}

#: GET /ds/login/{id}/accounts — the page rides in ``data`` and the total count rides in
#: ``meta.paginate.total``, which ``list`` drops and ``with_raw_response`` keeps.
LOGIN_ACCOUNTS_BODY: dict[str, Any] = {
    "meta": {"request_id": "req_00000000", "paginate": {"offset": 0, "limit": 100, "total": 137}},
    "data": [ACCOUNT_ONE, ACCOUNT_TWO],
}

#: DELETE /ds/login/{id} — a 200 whose ``data.result`` boolean is the whole outcome.
REVOKE_TRUE_BODY: dict[str, Any] = {"meta": {"request_id": "req_00000000"}, "data": {"result": True}}

#: The same envelope reporting that nothing was revoked.
REVOKE_FALSE_BODY: dict[str, Any] = {"meta": {"request_id": "req_00000000"}, "data": {"result": False}}


class TestLoginsResource:
    """Synchronous login reads, account listing and revocation."""

    def test_get_returns_the_login_from_the_data_envelope(self, api_server: MockAPIServer) -> None:
        """The envelope is ``{"data": <login>}``; the adapter hands back the login itself."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=LOGIN_GET_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            login = client.logins.get(LOGIN_ID)

        assert login.login_id == LOGIN_ID
        assert login.username == LOGIN_PAYLOAD["username"]

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGIN_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_returns_the_logins_from_the_data_envelope(self, api_server: MockAPIServer) -> None:
        """``list`` unwraps ``data`` into a list on the collection path."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            logins = client.logins.list()

        assert len(logins) == 1
        assert logins[0].login_id == LOGIN_ID
        assert logins[0].username == LOGIN_PAYLOAD["username"]

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_get_by_username_returns_the_matching_login_via_the_list_path(self, api_server: MockAPIServer) -> None:
        """``get_by_username`` has no endpoint of its own — it lists and filters.

        The proof that it delegates is the outbound request: a plain ``GET /ds/logins``,
        the same call ``list`` makes, with the matching done client-side.
        """
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            login = client.logins.get_by_username(LOGIN_PAYLOAD["username"])

        assert login.login_id == LOGIN_ID
        assert login.username == LOGIN_PAYLOAD["username"]

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION
        assert request.bearer_token == "api_k"

    def test_get_by_username_raises_value_error_when_no_login_matches(self, api_server: MockAPIServer) -> None:
        """A username absent from the list is a ``ValueError``, not an empty result.

        The lookup still reaches ``GET /ds/logins`` first — the filtering that fails is
        client-side, so the request is recorded even though the call raises.
        """
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(ValueError, match="No login found with username: nobody@example.com"):
                client.logins.get_by_username("nobody@example.com")

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION

    def test_get_accounts_sends_default_pagination(self, api_server: MockAPIServer) -> None:
        """``get_accounts`` always sends ``offset=0&limit=100`` and returns the page.

        The defaults are not omitted: the generated endpoint drops a query parameter only
        when it is ``UNSET`` or ``None``, and ``0``/``100`` are neither, so both ride on
        the wire on every call.
        """
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=LOGIN_ACCOUNTS_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = client.logins.get_accounts(LOGIN_ID)

        assert [a.account_id for a in accounts] == ["acc_1", "acc_2"]
        assert accounts[0].name == "Account One"
        assert accounts[0].group == "Group A"
        assert accounts[1].name == "Account Two"

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS
        query = parse_qs(urlsplit(request.path).query)
        assert query["offset"] == ["0"]
        assert query["limit"] == ["100"]
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_get_accounts_reflects_custom_offset_and_limit(self, api_server: MockAPIServer) -> None:
        """A caller's ``offset``/``limit`` reach the wire verbatim as query parameters."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=LOGIN_ACCOUNTS_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = client.logins.get_accounts(LOGIN_ID, offset=20, limit=5)

        assert [a.account_id for a in accounts] == ["acc_1", "acc_2"]

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS
        query = parse_qs(urlsplit(request.path).query)
        assert query["offset"] == ["20"]
        assert query["limit"] == ["5"]

    def test_get_accounts_raw_response_exposes_the_pagination_total(self, api_server: MockAPIServer) -> None:
        """``list`` drops ``meta``; ``with_raw_response`` keeps the whole body.

        The total count lives in ``meta.paginate.total`` and never rides on a parsed
        ``DataSourceAccount``. A caller paginating has to read it off the raw JSON body,
        which is exactly what ``with_raw_response`` is for.
        """
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=LOGIN_ACCOUNTS_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.logins.get_accounts(LOGIN_ID)

        assert response.status_code == 200
        assert [a.account_id for a in response.data] == ["acc_1", "acc_2"]

        body = response.json_body
        assert isinstance(body, dict)
        assert body["meta"]["paginate"]["total"] == 137

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS

    def test_revoke_returns_true_from_the_result_flag(self, api_server: MockAPIServer) -> None:
        """A DELETE carrying ``data.result: true`` means the login was revoked."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_TRUE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            revoked = client.logins.revoke(LOGIN_ID)

        assert revoked is True

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == LOGIN_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_revoke_returns_false_when_result_is_false(self, api_server: MockAPIServer) -> None:
        """The same 200 shape reporting ``result: false`` comes back as ``False``."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_FALSE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            revoked = client.logins.revoke(LOGIN_ID)

        assert revoked is False

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == LOGIN_ITEM


class TestLoginsAsyncResource:
    """Asynchronous logins — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_get_returns_the_login_from_the_data_envelope(self, api_server: MockAPIServer) -> None:
        """The async path unwraps ``data`` and hits the same by-id path."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=LOGIN_GET_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            login = await client.logins.get(LOGIN_ID)

        assert login.login_id == LOGIN_ID
        assert login.username == LOGIN_PAYLOAD["username"]

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGIN_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_list_returns_the_logins_from_the_data_envelope(self, api_server: MockAPIServer) -> None:
        """``list`` unwraps the collection identically on the async client."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            logins = await client.logins.list()

        assert len(logins) == 1
        assert logins[0].login_id == LOGIN_ID

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_get_by_username_returns_the_matching_login_via_the_list_path(
        self, api_server: MockAPIServer
    ) -> None:
        """The async lookup delegates to ``GET /ds/logins`` and filters client-side too."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            login = await client.logins.get_by_username(LOGIN_PAYLOAD["username"])

        assert login.login_id == LOGIN_ID
        assert login.username == LOGIN_PAYLOAD["username"]

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION

    @pytest.mark.asyncio
    async def test_get_by_username_raises_value_error_when_no_login_matches(self, api_server: MockAPIServer) -> None:
        """A missing username raises on the async path, after the same list request."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(json_body=LOGINS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(ValueError, match="No login found with username: nobody@example.com"):
                await client.logins.get_by_username("nobody@example.com")

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION

    @pytest.mark.asyncio
    async def test_get_accounts_sends_default_pagination(self, api_server: MockAPIServer) -> None:
        """The async client sends ``offset=0&limit=100`` and returns the same page."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=LOGIN_ACCOUNTS_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = await client.logins.get_accounts(LOGIN_ID)

        assert [a.account_id for a in accounts] == ["acc_1", "acc_2"]
        assert accounts[0].name == "Account One"
        assert accounts[0].group == "Group A"

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS
        query = parse_qs(urlsplit(request.path).query)
        assert query["offset"] == ["0"]
        assert query["limit"] == ["100"]

    @pytest.mark.asyncio
    async def test_get_accounts_reflects_custom_offset_and_limit(self, api_server: MockAPIServer) -> None:
        """Custom pagination reaches the wire on the async path as well."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=LOGIN_ACCOUNTS_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            accounts = await client.logins.get_accounts(LOGIN_ID, offset=20, limit=5)

        assert [a.account_id for a in accounts] == ["acc_1", "acc_2"]

        request = api_server.last_request
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS
        query = parse_qs(urlsplit(request.path).query)
        assert query["offset"] == ["20"]
        assert query["limit"] == ["5"]

    @pytest.mark.asyncio
    async def test_get_accounts_raw_response_exposes_the_pagination_total(self, api_server: MockAPIServer) -> None:
        """``with_raw_response`` reaches ``meta.paginate.total`` on the async client too."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(json_body=LOGIN_ACCOUNTS_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.logins.get_accounts(LOGIN_ID)

        assert response.status_code == 200
        assert [a.account_id for a in response.data] == ["acc_1", "acc_2"]

        body = response.json_body
        assert isinstance(body, dict)
        assert body["meta"]["paginate"]["total"] == 137

        assert urlsplit(api_server.last_request.path).path == LOGIN_ACCOUNTS

    @pytest.mark.asyncio
    async def test_revoke_returns_true_from_the_result_flag(self, api_server: MockAPIServer) -> None:
        """``result: true`` at 200 is a real revocation on the async path."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_TRUE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            revoked = await client.logins.revoke(LOGIN_ID)

        assert revoked is True

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == LOGIN_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_revoke_returns_false_when_result_is_false(self, api_server: MockAPIServer) -> None:
        """And ``result: false`` — still a 200 — comes back as ``False``."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(json_body=REVOKE_FALSE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            revoked = await client.logins.revoke(LOGIN_ID)

        assert revoked is False
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == LOGIN_ITEM
