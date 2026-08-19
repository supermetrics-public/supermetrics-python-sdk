"""End-to-end tests for the Login Links resource.

Drives all five methods over a real loopback socket. Login links stay on the core API
host — the paths are bare ``/ds/login/...`` with no ``/v1`` prefix and nothing is
re-hosted to the Data Warehouse host — so one server is the whole story here.

Every test asserts on both directions: the parsed return value, and the request that
actually went out. The outbound half is the point of this layer, and three things in this
domain exist only on the wire:

* ``create`` POSTs to ``/ds/login/link`` (singular) while ``list`` GETs ``/ds/login/links``
  (plural) — one wrong letter addresses a different resource;
* ``create`` always sends ``ds_id`` and an ``expiry_time`` string, defaulting the expiry
  when the caller omits it, and only sends ``description`` when one was given;
* ``update`` PATCHes the item path with a body of exactly ``{"description": ...}`` — the
  API accepts nothing else, so a leaked field would be rejected upstream.

Note:
    The generated ``create_login_link`` parses a body only on HTTP 201, so a successful
    creation is scripted with a 201 here — a 200 would leave the parsed link empty. This
    is a property of the generated layer, not a free choice, so the create tests pin it.
"""

from __future__ import annotations

import datetime
from typing import Any

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: The link these tests address, and the five routes it lives on. ``create`` posts to the
#: singular ``/ds/login/link`` and ``list`` gets the plural ``/ds/login/links``; the two are
#: distinct paths, and the mock server keys routes by path, so both can be wired at once.
LINK_ID = "link_123"
CREATE_PATH = "/ds/login/link"
ITEM_PATH = "/ds/login/link/link_123"
LIST_PATH = "/ds/login/links"
CLOSE_PATH = "/ds/login/link/link_123/close"

#: One login link as the single-object reads return it. ``login_*`` are null until an
#: authentication attempt completes, which is the normal state for an OPEN link.
LOGIN_LINK_PAYLOAD: dict[str, Any] = {
    "link_id": LINK_ID,
    "status_code": "OPEN",
    "description": "desc",
    "ds_id": "GAWA",
    "ds_name": "Google Analytics 4",
    "login_url": "https://app.supermetrics.com/login/link_123",
    "created_time": "2026-01-01T00:00:00Z",
    "expiry_time": "2026-01-02T00:00:00Z",
    "login_id": None,
    "login_time": None,
    "login_username": None,
}

#: The same link after an ``update``: the only editable field, ``description``, has changed.
UPDATED_LINK_PAYLOAD: dict[str, Any] = {**LOGIN_LINK_PAYLOAD, "description": "Q4 Analytics Setup"}

#: GET/POST/PATCH of a single link — a plain ``{"data": ...}`` envelope.
LINK_SINGLE_BODY: dict[str, Any] = {"data": LOGIN_LINK_PAYLOAD}

#: The envelope around the updated link.
LINK_UPDATED_BODY: dict[str, Any] = {"data": UPDATED_LINK_PAYLOAD}

#: GET the collection — a flat ``{"data": [...]}``.
LINK_LIST_BODY: dict[str, Any] = {"data": [LOGIN_LINK_PAYLOAD]}


class TestLoginLinksResource:
    """Synchronous login link creation, lookup, listing, closing and updating."""

    def test_create_returns_the_link_and_sends_ds_id_expiry_and_description(self, api_server: MockAPIServer) -> None:
        """POST ``/ds/login/link`` carries ds_id, an expiry_time string and the description.

        The public signature takes a ``datetime`` for ``expiry_time``; the generated body
        serializes it to an ISO 8601 string, so the assertion is that a string reaches the
        wire, not a datetime. The server answers 201, the one status the generated layer
        parses a body on.
        """
        api_server.route(CREATE_PATH, ScriptedResponse(status=201, json_body=LINK_SINGLE_BODY))

        expiry = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            link = client.login_links.create(ds_id="GAWA", description="desc", expiry_time=expiry)

        assert link.link_id == LINK_ID
        assert link.ds_id == "GAWA"
        assert link.status_code == "OPEN"
        assert link.description == "desc"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CREATE_PATH
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body["ds_id"] == "GAWA"
        assert body["description"] == "desc"
        assert isinstance(body["expiry_time"], str)

    def test_create_defaults_the_expiry_and_omits_description_when_not_given(self, api_server: MockAPIServer) -> None:
        """With no ``expiry_time`` the adapter still sends one; with no description it sends none.

        The default expiry is computed client-side (24 hours out), so the request must still
        carry an ``expiry_time`` string. ``description`` is optional and stays out of the body
        entirely rather than going out as ``null``.
        """
        api_server.route(CREATE_PATH, ScriptedResponse(status=201, json_body=LINK_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.login_links.create(ds_id="GAWA")

        body: dict[str, Any] = api_server.last_request.json()
        assert body["ds_id"] == "GAWA"
        assert isinstance(body["expiry_time"], str)
        assert "description" not in body

    def test_get_returns_the_link(self, api_server: MockAPIServer) -> None:
        """GET ``/ds/login/link/{id}`` unwraps ``data`` to the link."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=LINK_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            link = client.login_links.get(LINK_ID)

        assert link.link_id == LINK_ID
        assert link.status_code == "OPEN"
        assert link.description == "desc"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_returns_the_links(self, api_server: MockAPIServer) -> None:
        """GET ``/ds/login/links`` (plural) hands back the list from ``data``."""
        api_server.route(LIST_PATH, ScriptedResponse(json_body=LINK_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            links = client.login_links.list()

        assert len(links) == 1
        assert links[0].link_id == LINK_ID
        assert links[0].ds_id == "GAWA"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LIST_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_close_returns_none_and_puts_the_close_subpath(self, api_server: MockAPIServer) -> None:
        """PUT ``/ds/login/link/{id}/close`` returns nothing; the body is irrelevant."""
        api_server.route(CLOSE_PATH, ScriptedResponse(json_body={"data": {"result": True}}))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.login_links.close(LINK_ID)

        assert result is None

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == CLOSE_PATH
        assert request.path.endswith("/close")
        assert request.bearer_token == "api_k"

    def test_update_patches_the_item_with_only_a_description(self, api_server: MockAPIServer) -> None:
        """PATCH ``/ds/login/link/{id}`` with a body of exactly ``{"description": ...}``.

        The API accepts only ``description`` on update. Anything else in the body would be
        rejected upstream, so the assertion pins the body down to that single key.
        """
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=LINK_UPDATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            link = client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert link.link_id == LINK_ID
        assert link.description == "Q4 Analytics Setup"

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body == {"description": "Q4 Analytics Setup"}
        assert set(body) == {"description"}

    def test_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response carries the status, parsed body and decoded JSON."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=LINK_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.login_links.get(LINK_ID)

        assert response.status_code == 200
        assert response.data.link_id == LINK_ID
        assert response.json_body == LINK_SINGLE_BODY
        assert api_server.last_request.path == ITEM_PATH


class TestLoginLinksAsyncResource:
    """Asynchronous login links — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_create_returns_the_link_and_sends_ds_id_expiry_and_description(
        self, api_server: MockAPIServer
    ) -> None:
        """The async path sends the same POST body and unwraps the same envelope."""
        api_server.route(CREATE_PATH, ScriptedResponse(status=201, json_body=LINK_SINGLE_BODY))

        expiry = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            link = await client.login_links.create(ds_id="GAWA", description="desc", expiry_time=expiry)

        assert link.link_id == LINK_ID
        assert link.ds_id == "GAWA"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CREATE_PATH
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body["ds_id"] == "GAWA"
        assert body["description"] == "desc"
        assert isinstance(body["expiry_time"], str)

    @pytest.mark.asyncio
    async def test_create_defaults_the_expiry_and_omits_description_when_not_given(
        self, api_server: MockAPIServer
    ) -> None:
        """The client-side expiry default holds on the async path too."""
        api_server.route(CREATE_PATH, ScriptedResponse(status=201, json_body=LINK_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.login_links.create(ds_id="GAWA")

        body: dict[str, Any] = api_server.last_request.json()
        assert body["ds_id"] == "GAWA"
        assert isinstance(body["expiry_time"], str)
        assert "description" not in body

    @pytest.mark.asyncio
    async def test_get_returns_the_link(self, api_server: MockAPIServer) -> None:
        """GET on the item path, unwrapped to the link, on the async client."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=LINK_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            link = await client.login_links.get(LINK_ID)

        assert link.link_id == LINK_ID
        assert link.description == "desc"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_list_returns_the_links(self, api_server: MockAPIServer) -> None:
        """GET the plural collection path unwraps ``data`` to the list."""
        api_server.route(LIST_PATH, ScriptedResponse(json_body=LINK_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            links = await client.login_links.list()

        assert len(links) == 1
        assert links[0].link_id == LINK_ID

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LIST_PATH
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_close_returns_none_and_puts_the_close_subpath(self, api_server: MockAPIServer) -> None:
        """PUT ``/close`` returns None on the async client as well."""
        api_server.route(CLOSE_PATH, ScriptedResponse(json_body={"data": {"result": True}}))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.login_links.close(LINK_ID)

        assert result is None

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == CLOSE_PATH
        assert request.path.endswith("/close")
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_update_patches_the_item_with_only_a_description(self, api_server: MockAPIServer) -> None:
        """The description-only update body holds on the async client too."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=LINK_UPDATED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            link = await client.login_links.update(LINK_ID, "Q4 Analytics Setup")

        assert link.description == "Q4 Analytics Setup"

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ITEM_PATH
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert body == {"description": "Q4 Analytics Setup"}
        assert set(body) == {"description"}

    @pytest.mark.asyncio
    async def test_raw_response_exposes_transport_metadata(self, api_server: MockAPIServer) -> None:
        """with_raw_response works on the async mirror."""
        api_server.route(ITEM_PATH, ScriptedResponse(json_body=LINK_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.login_links.get(LINK_ID)

        assert response.status_code == 200
        assert response.data.link_id == LINK_ID
        assert response.json_body == LINK_SINGLE_BODY
