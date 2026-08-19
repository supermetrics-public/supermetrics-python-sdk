"""End-to-end tests for the Account Tags resource.

Drives all seven methods over a real loopback socket. Account tags stay on the core API
host — the paths keep their ``/v1`` prefix and nothing is re-hosted to the Data Warehouse
host — so one server is the whole story here.

Every test asserts on both directions: the parsed return value, and the request that
actually went out. The outbound half is the point of this layer, and four things in this
domain exist only on the wire:

* the path carries ``/v1`` and addresses the core host, which no unit test can see;
* ``name`` is percent-encoded into the path with ``safe=""``, so a slash in a tag name
  survives as ``%2F`` rather than splitting the path;
* ``create`` sends ``display_name``/``color``/``data_sources`` and no ``name`` — the
  server assigns the slug — while ``update`` sends only ``display_name``/``color`` and
  must not leak ``data_sources``;
* the two PATCH endpoints send ``{"data_sources": [...]}``, not ``{"accounts": [...]}``.

Error mapping lives in ``test_account_tags_errors_e2e.py`` and per-request overrides in
``test_account_tags_overrides_e2e.py``; neither is repeated here.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.parse import urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: The team and tag these tests address. ``name`` is the server-assigned slug, never the
#: human label — ``display_name`` is that, and it is a body field.
TEAM_ID = 936506
TAG_NAME = "a1b2c3d"

#: A tag name that needs escaping. The generated layer quotes path parameters with
#: ``safe=""``, so both the space and the slash have to come out percent-encoded.
AWKWARD_NAME = "a b/c"

#: The four routes, spelled out as literals. The ``/v1`` is load-bearing: account tags are
#: served from the core API host with the version in the path, while ``base_url`` is a bare
#: ``http://127.0.0.1:<port>``. A dropped prefix or an accidental re-host to the Data
#: Warehouse host would leave these routes unmatched, and the server's default 404 would
#: surface as a ``SupermetricsNotFoundError`` rather than a quiet wrong answer.
ACCOUNT_TAGS_COLLECTION = "/v1/teams/936506/account_tags"
ACCOUNT_TAGS_ITEM = "/v1/teams/936506/account_tags/a1b2c3d"
ACCOUNT_TAGS_ADD = "/v1/teams/936506/account_tags/a1b2c3d/add"
ACCOUNT_TAGS_REMOVE = "/v1/teams/936506/account_tags/a1b2c3d/remove"

#: ``AWKWARD_NAME`` as it must appear on the wire.
ACCOUNT_TAGS_AWKWARD_ITEM = "/v1/teams/936506/account_tags/a%20b%2Fc"

#: One data source selection, in the shape the spec's own example documents. Upstream
#: declares the array items as a bare ``type: object``, so this dict has to survive the
#: round trip untouched — nothing validates or reshapes it at either end.
DATA_SOURCE_SELECTION: dict[str, Any] = {
    "data_source_id": "AW",
    "accounts": [{"account_id": "123-456-7890"}],
}

#: A second selection, used to prove ``add``/``remove`` send what they were given.
OTHER_DATA_SOURCE_SELECTION: dict[str, Any] = {
    "data_source_id": "FB",
    "accounts": [{"account_id": "act_99"}],
}

#: One account tag as the single-object reads return it: membership, no counts.
ACCOUNT_TAG_PAYLOAD: dict[str, Any] = {
    "name": TAG_NAME,
    "display_name": "EMEA paid media",
    "color": "#112233",
    "data_sources": [DATA_SOURCE_SELECTION],
}

#: One account tag as ``list`` returns it: counts, no membership. The two payload models
#: are genuinely different shapes, not one model with optional fields.
ACCOUNT_TAG_OVERVIEW_PAYLOAD: dict[str, Any] = {
    "name": TAG_NAME,
    "display_name": "EMEA paid media",
    "color": "#112233",
    "data_source_count": 3,
    "account_count": 42,
}

#: GET/POST/PUT/PATCH of a single tag. Unlike custom fields there is no ``meta`` — the
#: envelope is a plain ``{"data": ...}`` with nothing else in it.
ACCOUNT_TAG_SINGLE_BODY: dict[str, Any] = {"data": ACCOUNT_TAG_PAYLOAD}

#: GET the collection — a flat ``{"data": [...]}``, not the ``data.items`` double-wrap.
ACCOUNT_TAG_LIST_BODY: dict[str, Any] = {"data": [ACCOUNT_TAG_OVERVIEW_PAYLOAD]}

#: An empty team. ``data`` is optional upstream, so both of these are legal answers and
#: both have to come back as ``[]`` rather than fall over.
ACCOUNT_TAG_EMPTY_LIST_BODY: dict[str, Any] = {"data": []}
ACCOUNT_TAG_NO_DATA_BODY: dict[str, Any] = {}

#: Deletion is idempotent upstream, so all three of these arrive with HTTP 200 and the
#: body is the only place the outcome is recorded. ``result`` is optional in the schema,
#: hence the third case.
DELETED_BODY: dict[str, Any] = {"data": {"result": True}}
NOT_DELETED_BODY: dict[str, Any] = {"data": {"result": False}}
DELETE_WITHOUT_RESULT_BODY: dict[str, Any] = {"data": {}}


class TestAccountTagsResource:
    """Synchronous account tag listing, CRUD and membership changes."""

    def test_list_returns_the_overviews_from_the_data_envelope(self, api_server: MockAPIServer) -> None:
        """The envelope is ``{"data": [...]}``; the adapter hands back the overviews."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = client.account_tags.list(team_id=TEAM_ID)

        assert len(tags) == 1
        assert tags[0].name == TAG_NAME
        assert tags[0].display_name == "EMEA paid media"
        assert tags[0].color == "#112233"
        assert tags[0].data_source_count == 3
        assert tags[0].account_count == 42

        request = api_server.last_request
        assert request.method == "GET"
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_requests_the_v1_collection_path_with_no_query_string(self, api_server: MockAPIServer) -> None:
        """The literal outbound path, spelled out.

        This is the highest-value assertion in the file. Account tags are served from the
        core API host with ``/v1`` in the path; a ``rewrite_path`` slip that dropped the
        prefix, or one that reshaped the path into the ``^/teams/...`` form the transport
        inspects when deciding to re-host to the Data Warehouse host, would be invisible
        to every unit test in the repo. There are also no query parameters anywhere in
        this domain, so an empty query string is part of the contract.
        """
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = client.account_tags.list(team_id=TEAM_ID)

        assert len(tags) == 1

        path = api_server.last_request.path
        assert path.startswith("/v1/teams/936506/account_tags")
        assert urlsplit(path).path == "/v1/teams/936506/account_tags"
        assert urlsplit(path).query == ""

    def test_list_returns_an_empty_list_when_data_is_an_empty_array(self, api_server: MockAPIServer) -> None:
        """No tags is not an error, and not ``None``."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = client.account_tags.list(team_id=TEAM_ID)

        assert tags == []

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == ACCOUNT_TAGS_COLLECTION

    def test_list_returns_an_empty_list_when_the_body_has_no_data_key(self, api_server: MockAPIServer) -> None:
        """``data`` is optional upstream, so a body without it is legal and means empty."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_NO_DATA_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = client.account_tags.list(team_id=TEAM_ID)

        assert tags == []

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == ACCOUNT_TAGS_COLLECTION
        assert request.bearer_token == "api_k"

    def test_get_returns_the_tag_with_its_membership(self, api_server: MockAPIServer) -> None:
        """``get`` returns membership where ``list`` returns counts.

        ``data_sources`` items are free-form upstream, so the generated item class holds
        the whole selection in ``additional_properties`` and reads back by subscript.
        """
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert tag.name == TAG_NAME
        assert tag.display_name == "EMEA paid media"
        assert tag.color == "#112233"
        assert len(tag.data_sources) == 1
        assert tag.data_sources[0]["data_source_id"] == "AW"
        assert tag.data_sources[0]["accounts"] == [{"account_id": "123-456-7890"}]
        assert tag.data_sources[0].to_dict() == DATA_SOURCE_SELECTION

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_get_percent_encodes_the_name_into_the_path(self, api_server: MockAPIServer) -> None:
        """A name needing escaping is quoted with ``safe=""`` — the slash stays encoded.

        ``a b/c`` has to reach the server as ``a%20b%2Fc``. The encoded slash is the whole
        point: with a laxer ``safe`` it would become a real path separator and address
        ``.../account_tags/a b/c``, a different resource entirely. Anyone "simplifying"
        the generated f-string breaks exactly this and nothing else notices.
        """
        api_server.route(ACCOUNT_TAGS_AWKWARD_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.get(team_id=TEAM_ID, name=AWKWARD_NAME)

        assert tag.name == TAG_NAME

        path = api_server.last_request.path
        assert path == "/v1/teams/936506/account_tags/a%20b%2Fc"
        assert "%2F" in path
        # The name is one path segment, not two: the slash inside it never separates.
        assert path.split("/")[1:] == ["v1", "teams", "936506", "account_tags", "a%20b%2Fc"]

    @pytest.mark.parametrize(
        ("method_name", "route", "expected_method", "expected_path", "call"),
        [
            (
                "update",
                ACCOUNT_TAGS_AWKWARD_ITEM,
                "PUT",
                "/v1/teams/936506/account_tags/a%20b%2Fc",
                lambda client: client.account_tags.update(
                    team_id=TEAM_ID, name=AWKWARD_NAME, display_name="EMEA paid", color="#445566"
                ),
            ),
            (
                "delete",
                ACCOUNT_TAGS_AWKWARD_ITEM,
                "DELETE",
                "/v1/teams/936506/account_tags/a%20b%2Fc",
                lambda client: client.account_tags.delete(team_id=TEAM_ID, name=AWKWARD_NAME),
            ),
            (
                "add_accounts",
                ACCOUNT_TAGS_AWKWARD_ITEM + "/add",
                "PATCH",
                "/v1/teams/936506/account_tags/a%20b%2Fc/add",
                lambda client: client.account_tags.add_accounts(
                    team_id=TEAM_ID, name=AWKWARD_NAME, data_sources=[DATA_SOURCE_SELECTION]
                ),
            ),
            (
                "remove_accounts",
                ACCOUNT_TAGS_AWKWARD_ITEM + "/remove",
                "PATCH",
                "/v1/teams/936506/account_tags/a%20b%2Fc/remove",
                lambda client: client.account_tags.remove_accounts(
                    team_id=TEAM_ID, name=AWKWARD_NAME, data_sources=[DATA_SOURCE_SELECTION]
                ),
            ),
        ],
    )
    def test_every_name_bearing_method_percent_encodes_the_name(
        self,
        api_server: MockAPIServer,
        method_name: str,
        route: str,
        expected_method: str,
        expected_path: str,
        call: Callable[[SupermetricsClient], object],
    ) -> None:
        """All five name-bearing methods quote the name the same way ``get`` does.

        ``get`` proves the shared ``quote(str(name), safe="")`` codepath, but ``update``,
        ``delete``, ``add_accounts`` and ``remove_accounts`` each embed ``name`` in their
        own generated URL. A hand-edit to any one of those generated files would slip past
        a ``get``-only check, so each is asserted independently here.
        """
        body = DELETED_BODY if method_name == "delete" else ACCOUNT_TAG_SINGLE_BODY
        api_server.route(route, ScriptedResponse(json_body=body))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            call(client)

        request = api_server.last_request
        assert request.method == expected_method
        assert request.path == expected_path
        assert "%2F" in request.path

    def test_create_returns_the_tag_and_sends_no_name(self, api_server: MockAPIServer) -> None:
        """Creation answers 200 — not 201 — and the slug comes back rather than going out.

        ``name`` is assigned by the server, so a ``name`` key in the POST body would be
        the SDK inventing an identifier for a resource that does not exist yet.
        """
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.create(
                team_id=TEAM_ID,
                display_name="EMEA paid media",
                color="#112233",
                data_sources=[DATA_SOURCE_SELECTION],
            )

        assert tag.name == TAG_NAME
        assert tag.display_name == "EMEA paid media"

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == ACCOUNT_TAGS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "name" not in body
        assert set(body) == {"display_name", "color", "data_sources"}
        assert body["display_name"] == "EMEA paid media"
        assert body["color"] == "#112233"

    def test_create_sends_the_data_source_selection_verbatim(self, api_server: MockAPIServer) -> None:
        """A ``data_sources`` round trip: out as given, back as given.

        The public signature takes plain dicts because the generated item class is
        unconstructable, and the adapter converts them with ``.from_dict``. That
        conversion has to be lossless in both directions — upstream declares no schema
        for the element, so anything the SDK drops is gone silently.
        """
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.create(
                team_id=TEAM_ID,
                display_name="EMEA paid media",
                color="#112233",
                data_sources=[DATA_SOURCE_SELECTION, OTHER_DATA_SOURCE_SELECTION],
            )

        body: dict[str, Any] = api_server.last_request.json()
        assert body["data_sources"] == [DATA_SOURCE_SELECTION, OTHER_DATA_SOURCE_SELECTION]
        assert body["data_sources"][0] == {
            "data_source_id": "AW",
            "accounts": [{"account_id": "123-456-7890"}],
        }

        assert tag.data_sources[0]["data_source_id"] == "AW"

    def test_update_sends_only_display_name_and_color(self, api_server: MockAPIServer) -> None:
        """PUT renames and recolours; it cannot touch membership.

        ``data_sources`` is not part of the update body, and the request schema is
        ``additionalProperties: false``, so leaking it upstream would be rejected. The
        two PATCH endpoints are how membership moves.
        """
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.update(
                team_id=TEAM_ID,
                name=TAG_NAME,
                display_name="EMEA paid",
                color="#445566",
            )

        assert tag.name == TAG_NAME
        assert tag.display_name == "EMEA paid media"

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "data_sources" not in body
        assert "name" not in body
        assert set(body) == {"display_name", "color"}
        assert body["display_name"] == "EMEA paid"
        assert body["color"] == "#445566"

    def test_delete_returns_true_when_a_tag_was_removed(self, api_server: MockAPIServer) -> None:
        """A 200 carrying ``result: true`` means something was actually deleted."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=DELETED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            deleted = client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert deleted is True

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_delete_returns_false_when_no_tag_existed(self, api_server: MockAPIServer) -> None:
        """Deleting an absent tag is a success upstream, reported as ``result: false``.

        This domain documents no 404 anywhere, so the boolean is the only signal there is
        — returning ``None`` here, as every other ``delete`` in the SDK does, would throw
        away the one thing the endpoint exists to say.
        """
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=NOT_DELETED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            deleted = client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert deleted is False

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == ACCOUNT_TAGS_ITEM

    def test_delete_returns_false_when_the_body_omits_result(self, api_server: MockAPIServer) -> None:
        """``result`` is optional in the schema; an absent one is not an implied success."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=DELETE_WITHOUT_RESULT_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            deleted = client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert deleted is False

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"

    def test_add_accounts_patches_the_add_subpath_with_data_sources(self, api_server: MockAPIServer) -> None:
        """PATCH ``/add`` with ``{"data_sources": [...]}``.

        The key is ``data_sources``, not ``accounts``: the feature request says otherwise
        and the spec wins. ``/add`` is also its own path segment, so a call that fell back
        to the bare item path would silently become a replace.
        """
        api_server.route(ACCOUNT_TAGS_ADD, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.add_accounts(
                team_id=TEAM_ID,
                name=TAG_NAME,
                data_sources=[OTHER_DATA_SOURCE_SELECTION],
            )

        assert tag.name == TAG_NAME
        assert tag.data_sources[0]["data_source_id"] == "AW"

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ACCOUNT_TAGS_ADD
        assert request.path.endswith("/add")
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "accounts" not in body
        assert set(body) == {"data_sources"}
        assert body["data_sources"] == [OTHER_DATA_SOURCE_SELECTION]

    def test_remove_accounts_patches_the_remove_subpath_with_data_sources(self, api_server: MockAPIServer) -> None:
        """PATCH ``/remove`` with the same body shape, on its own sibling path."""
        api_server.route(ACCOUNT_TAGS_REMOVE, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = client.account_tags.remove_accounts(
                team_id=TEAM_ID,
                name=TAG_NAME,
                data_sources=[DATA_SOURCE_SELECTION],
            )

        assert tag.name == TAG_NAME

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ACCOUNT_TAGS_REMOVE
        assert request.path.endswith("/remove")
        assert request.path != ACCOUNT_TAGS_ADD
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "accounts" not in body
        assert set(body) == {"data_sources"}
        assert body["data_sources"] == [DATA_SOURCE_SELECTION]


class TestAccountTagsAsyncResource:
    """Asynchronous account tags — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_the_overviews_from_the_data_envelope(self, api_server: MockAPIServer) -> None:
        """The async path unwraps ``data`` and hits the same ``/v1`` core-host path."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = await client.account_tags.list(team_id=TEAM_ID)

        assert len(tags) == 1
        assert tags[0].name == TAG_NAME
        assert tags[0].data_source_count == 3
        assert tags[0].account_count == 42

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path.startswith("/v1/teams/936506/account_tags")
        assert urlsplit(request.path).path == ACCOUNT_TAGS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_list_when_the_body_has_no_data_key(self, api_server: MockAPIServer) -> None:
        """An absent ``data`` is an empty team on the async path too."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_NO_DATA_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = await client.account_tags.list(team_id=TEAM_ID)

        assert tags == []

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == ACCOUNT_TAGS_COLLECTION

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_list_when_data_is_an_empty_array(self, api_server: MockAPIServer) -> None:
        """An explicitly empty ``data`` array behaves the same as an absent one."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tags = await client.account_tags.list(team_id=TEAM_ID)

        assert tags == []
        assert urlsplit(api_server.last_request.path).path == ACCOUNT_TAGS_COLLECTION

    @pytest.mark.asyncio
    async def test_get_returns_the_tag_with_its_membership(self, api_server: MockAPIServer) -> None:
        """GET on the by-name path, unwrapped to the tag and its data sources."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = await client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert tag.name == TAG_NAME
        assert tag.display_name == "EMEA paid media"
        assert tag.data_sources[0]["data_source_id"] == "AW"
        assert tag.data_sources[0].to_dict() == DATA_SOURCE_SELECTION

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_get_percent_encodes_the_name_into_the_path(self, api_server: MockAPIServer) -> None:
        """The async client quotes path parameters identically — encoded slash and all."""
        api_server.route(ACCOUNT_TAGS_AWKWARD_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = await client.account_tags.get(team_id=TEAM_ID, name=AWKWARD_NAME)

        assert tag.name == TAG_NAME

        path = api_server.last_request.path
        assert path == "/v1/teams/936506/account_tags/a%20b%2Fc"
        assert "%2F" in path
        assert path.split("/")[1:] == ["v1", "teams", "936506", "account_tags", "a%20b%2Fc"]

    @pytest.mark.asyncio
    async def test_create_returns_the_tag_and_sends_no_name(self, api_server: MockAPIServer) -> None:
        """200 on the async path, with the selection verbatim and no ``name`` key."""
        api_server.route(ACCOUNT_TAGS_COLLECTION, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = await client.account_tags.create(
                team_id=TEAM_ID,
                display_name="EMEA paid media",
                color="#112233",
                data_sources=[DATA_SOURCE_SELECTION],
            )

        assert tag.name == TAG_NAME
        assert tag.data_sources[0]["data_source_id"] == "AW"

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == ACCOUNT_TAGS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "name" not in body
        assert set(body) == {"display_name", "color", "data_sources"}
        assert body["data_sources"] == [DATA_SOURCE_SELECTION]

    @pytest.mark.asyncio
    async def test_update_sends_only_display_name_and_color(self, api_server: MockAPIServer) -> None:
        """The membership-is-not-updatable rule holds on the async client as well."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = await client.account_tags.update(
                team_id=TEAM_ID,
                name=TAG_NAME,
                display_name="EMEA paid",
                color="#445566",
            )

        assert tag.name == TAG_NAME

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "data_sources" not in body
        assert set(body) == {"display_name", "color"}
        assert body["display_name"] == "EMEA paid"
        assert body["color"] == "#445566"

    @pytest.mark.asyncio
    async def test_delete_returns_true_when_a_tag_was_removed(self, api_server: MockAPIServer) -> None:
        """``result: true`` at 200 is a real deletion, on the async path too."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=DELETED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            deleted = await client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert deleted is True

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == ACCOUNT_TAGS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_no_tag_existed(self, api_server: MockAPIServer) -> None:
        """And ``result: false`` — still a 200 — is an idempotent no-op."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=NOT_DELETED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            deleted = await client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert deleted is False
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_the_body_omits_result(self, api_server: MockAPIServer) -> None:
        """A missing ``result`` is not an implied success on either client."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(json_body=DELETE_WITHOUT_RESULT_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            deleted = await client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert deleted is False
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    @pytest.mark.asyncio
    async def test_add_accounts_patches_the_add_subpath_with_data_sources(self, api_server: MockAPIServer) -> None:
        """PATCH ``/add`` with ``data_sources``, not ``accounts``."""
        api_server.route(ACCOUNT_TAGS_ADD, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = await client.account_tags.add_accounts(
                team_id=TEAM_ID,
                name=TAG_NAME,
                data_sources=[OTHER_DATA_SOURCE_SELECTION],
            )

        assert tag.name == TAG_NAME

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ACCOUNT_TAGS_ADD
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "accounts" not in body
        assert set(body) == {"data_sources"}
        assert body["data_sources"] == [OTHER_DATA_SOURCE_SELECTION]

    @pytest.mark.asyncio
    async def test_remove_accounts_patches_the_remove_subpath_with_data_sources(
        self, api_server: MockAPIServer
    ) -> None:
        """PATCH ``/remove``, its own sibling path, with the same body shape."""
        api_server.route(ACCOUNT_TAGS_REMOVE, ScriptedResponse(json_body=ACCOUNT_TAG_SINGLE_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            tag = await client.account_tags.remove_accounts(
                team_id=TEAM_ID,
                name=TAG_NAME,
                data_sources=[DATA_SOURCE_SELECTION],
            )

        assert tag.name == TAG_NAME

        request = api_server.last_request
        assert request.method == "PATCH"
        assert request.path == ACCOUNT_TAGS_REMOVE
        assert request.path != ACCOUNT_TAGS_ADD
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert "accounts" not in body
        assert set(body) == {"data_sources"}
        assert body["data_sources"] == [DATA_SOURCE_SELECTION]
