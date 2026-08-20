"""End-to-end tests for the Connector Builder resource.

Drives all seven methods over a real loopback socket. Connector Builder lives on the
core API host, so every path keeps its ``/v1`` prefix and there is no re-hosting to the
Data Warehouse host — one server is the whole story. Passing a custom ``base_url`` also
disables DTS host routing, so even if these endpoints were DTS-hosted they would still
land on the single server; here they are genuinely core-host endpoints.

Every method gets two tests: one on the parsed return value, one on the request that
actually went out. The request half is the point of this layer. A mocked transport
cannot see that ``list`` omits the ``include_configs`` query string by default, that
``create`` sends a *form-urlencoded* body rather than JSON, or that ``upload_logo``
streams the raw image bytes inside a multipart part.

Two wire facts worth flagging up front, both verified against the generated endpoints:

* ``create`` posts ``application/x-www-form-urlencoded`` (the generated client uses
  ``data=`` for this body, not ``json=``), so its request body is asserted with
  ``parse_qs`` over the decoded body, never ``request.json()``.
* ``get_logo`` answers a JSON ``{"logo_url": ...}`` object, not a binary blob — the
  logo bytes only travel *up* the wire in ``upload_logo``'s multipart body.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics._generated.supermetrics_api_client.types import File

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

TEAM_ID = 42
CONNECTOR_ID = "T3S70"

#: The four routes exercised here, all under the ``/v1`` core-host prefix.
CONNECTORS_COLLECTION = f"/v1/teams/{TEAM_ID}/connector_builder/connectors"
CONNECTOR_ITEM = f"{CONNECTORS_COLLECTION}/{CONNECTOR_ID}"
CONNECTOR_LOGO = f"{CONNECTOR_ITEM}/logo"

#: One connector as the list endpoint returns it. A ``Connector`` summary has no
#: ``configuration`` — that only comes back from ``get``.
CONNECTOR_LIST_ITEM: dict[str, Any] = {
    "connector_identifier": CONNECTOR_ID,
    "name": "Test Connector",
    "description": "A custom connector for fetching marketing data",
    "logo_url": "https://assets.supermetrics.com/images/dsLogos/Custom_Connector_Default.png",
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-02T00:00:00+00:00",
}

#: GET the collection — bare ``{count, connectors}``, no ``{data}`` envelope.
CONNECTORS_LIST_BODY: dict[str, Any] = {"count": 1, "connectors": [CONNECTOR_LIST_ITEM]}

#: An empty team. ``count`` and ``connectors`` are both required, so empty is ``0`` and
#: ``[]`` — never a body with the keys missing.
CONNECTORS_EMPTY_LIST_BODY: dict[str, Any] = {"count": 0, "connectors": []}

#: A single connector *with* its configuration, as ``get``, ``create`` and ``update``
#: return it. Bare, no envelope. ``configuration_json`` is an open object upstream, so any
#: shape round-trips through the generated model's ``additional_properties``.
CONNECTOR_WITH_CONFIG_BODY: dict[str, Any] = {
    "connector_identifier": CONNECTOR_ID,
    "name": "Test Connector",
    "description": "A custom connector for fetching marketing data",
    "logo_url": "https://assets.supermetrics.com/images/dsLogos/Custom_Connector_Default.png",
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-02T00:00:00+00:00",
    "configuration": {
        "version": "1.0.0",
        "configuration_json": {"base_url": "https://api.example.com", "auth": "oauth2"},
        "created_at": "2026-01-01T00:00:00+00:00",
        "updated_at": "2026-01-02T00:00:00+00:00",
    },
}

#: GET .../logo — a JSON object carrying the URL, not the image itself.
LOGO_BODY: dict[str, Any] = {"logo_url": "https://assets.supermetrics.com/images/dsLogos/T3S70.png"}

#: POST .../logo, 201 — the URL of the freshly uploaded image.
UPLOAD_LOGO_BODY: dict[str, Any] = {"logo_url": "https://assets.supermetrics.com/images/dsLogos/T3S70_new.png"}

#: The raw bytes a caller hands to ``upload_logo``. Asserting these survive onto the wire
#: is the only way to prove the multipart body actually carries the image.
LOGO_BYTES = b"\x89PNG\r\n\x1a\n-fake-png-payload-"

#: A well-formed ``connector`` block for ``update``. Both fields are required upstream.
UPDATE_CONNECTOR: dict[str, Any] = {"name": "Renamed Connector", "description": "Now with a description"}

#: A well-formed ``configuration`` block for ``update``. ``configuration_json`` is required.
UPDATE_CONFIGURATION: dict[str, Any] = {"configuration_json": {"base_url": "https://api.example.com", "auth": "apikey"}}


def _logo_file() -> File:
    """Build the upload payload the way a caller would.

    The generated ``File`` wraps a binary stream plus a filename and MIME type; httpx
    turns ``to_tuple()`` into a multipart part on the wire.
    """
    return File(payload=BytesIO(LOGO_BYTES), file_name="logo.png", mime_type="image/png")


class TestConnectorBuilderResource:
    """Synchronous connector CRUD plus logo read and upload."""

    def test_list_returns_the_connectors(self, api_server: MockAPIServer) -> None:
        """The bare ``{count, connectors}`` body is handed back intact."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder.list(team_id=TEAM_ID)

        assert result.count == 1
        assert len(result.connectors) == 1
        assert result.connectors[0].connector_identifier == CONNECTOR_ID
        assert result.connectors[0].name == "Test Connector"

    def test_list_without_options_still_sends_include_configs_false(self, api_server: MockAPIServer) -> None:
        """A bare ``list`` puts ``include_configs=false`` on the wire.

        The adapter *tries* to drop the default with an ``if include_configs:`` guard, only
        passing the kwarg when it is truthy. But the generated ``list_connectors`` stub
        defaults the parameter to ``False`` (not ``UNSET``), and its param filter drops
        only ``UNSET``/``None`` — so ``include_configs=false`` is serialized regardless of
        the guard. This asserts the behaviour the wire actually shows, not the adapter's
        intent; a mocked transport could never surface the gap between the two.
        """
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.list(team_id=TEAM_ID)

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == CONNECTORS_COLLECTION
        assert parse_qs(urlsplit(request.path).query) == {"include_configs": ["false"]}
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_forwards_include_configs_when_true(self, api_server: MockAPIServer) -> None:
        """Asking for configs puts ``include_configs=true`` on the query string."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.list(team_id=TEAM_ID, include_configs=True)

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {"include_configs": ["true"]}

    def test_list_returns_an_empty_result(self, api_server: MockAPIServer) -> None:
        """An empty team is ``count == 0`` with an empty list, not an error."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder.list(team_id=TEAM_ID)

        assert result.count == 0
        assert result.connectors == []

    def test_get_returns_the_connector_with_configuration(self, api_server: MockAPIServer) -> None:
        """The by-id body is bare; the adapter returns the connector with its config."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(json_body=CONNECTOR_WITH_CONFIG_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            connector = client.connector_builder.get(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        assert connector.connector_identifier == CONNECTOR_ID
        assert connector.name == "Test Connector"
        assert connector.configuration.version == "1.0.0"
        assert connector.configuration.configuration_json["base_url"] == "https://api.example.com"

    def test_get_sends_a_get_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """GET on ``.../connectors/{id}`` with no body."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(json_body=CONNECTOR_WITH_CONFIG_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.get(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == CONNECTOR_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_create_returns_the_connector_from_a_201(self, api_server: MockAPIServer) -> None:
        """Creation answers ``201 Created`` and returns the persisted connector."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(status=201, json_body=CONNECTOR_WITH_CONFIG_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            connector = client.connector_builder.create(team_id=TEAM_ID, title="Test Connector")

        assert connector.connector_identifier == CONNECTOR_ID
        assert connector.name == "Test Connector"

    def test_create_sends_a_form_encoded_body(self, api_server: MockAPIServer) -> None:
        """POST to the collection with a *form-urlencoded* body, not JSON.

        The generated client sends this body via ``data=``, so the wire carries
        ``application/x-www-form-urlencoded`` and the fields are asserted with ``parse_qs``
        over the decoded body rather than ``request.json()``.
        """
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(status=201, json_body=CONNECTOR_WITH_CONFIG_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.create(
                team_id=TEAM_ID,
                title="Test Connector",
                description="A custom connector",
                connector_identifier="SRC42",
            )

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == CONNECTORS_COLLECTION
        assert request.bearer_token == "api_k"
        assert request.headers["content-type"].startswith("application/x-www-form-urlencoded")

        form = parse_qs(request.body.decode())
        assert form == {
            "title": ["Test Connector"],
            "description": ["A custom connector"],
            "connector_identifier": ["SRC42"],
        }

    def test_create_omits_unset_optional_fields(self, api_server: MockAPIServer) -> None:
        """With only ``title`` given, nothing else may leak into the form body.

        ``description`` and ``connector_identifier`` are ``UNSET`` and the generated body
        drops them, so a bare create carries a single field.
        """
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(status=201, json_body=CONNECTOR_WITH_CONFIG_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.create(team_id=TEAM_ID, title="Test Connector")

        form = parse_qs(api_server.last_request.body.decode())
        assert form == {"title": ["Test Connector"]}

    def test_update_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """A successful update answers ``204 No Content`` and the adapter returns ``None``."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder.update(
                team_id=TEAM_ID,
                connector_identifier=CONNECTOR_ID,
                connector=UPDATE_CONNECTOR,
                configuration=UPDATE_CONFIGURATION,
            )

        assert result is None

    def test_update_sends_a_json_put_with_both_blocks(self, api_server: MockAPIServer) -> None:
        """PUT on the by-id path, carrying ``connector`` and ``configuration`` as JSON.

        Unlike ``create``, update sends ``application/json`` — the ``connector`` metadata
        and the nested ``configuration.configuration_json`` both have to reach the wire.
        """
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.update(
                team_id=TEAM_ID,
                connector_identifier=CONNECTOR_ID,
                connector=UPDATE_CONNECTOR,
                configuration=UPDATE_CONFIGURATION,
            )

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == CONNECTOR_ITEM
        assert request.bearer_token == "api_k"
        assert request.headers["content-type"].startswith("application/json")

        body: dict[str, Any] = request.json()
        assert body == {
            "connector": {"name": "Renamed Connector", "description": "Now with a description"},
            "configuration": {"configuration_json": {"base_url": "https://api.example.com", "auth": "apikey"}},
        }

    def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """Deletion answers ``204 No Content`` with a genuinely empty body."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder.delete(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        assert result is None

    def test_delete_sends_a_delete_to_the_by_id_path(self, api_server: MockAPIServer) -> None:
        """DELETE on the by-id path, with no body of its own."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.delete(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == CONNECTOR_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_get_logo_returns_the_url(self, api_server: MockAPIServer) -> None:
        """``get_logo`` answers a JSON object carrying the URL, not the image bytes."""
        api_server.route(CONNECTOR_LOGO, ScriptedResponse(json_body=LOGO_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            logo = client.connector_builder.get_logo(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        assert logo.logo_url == "https://assets.supermetrics.com/images/dsLogos/T3S70.png"

    def test_get_logo_sends_a_get_to_the_logo_path(self, api_server: MockAPIServer) -> None:
        """GET on ``.../connectors/{id}/logo`` with no body."""
        api_server.route(CONNECTOR_LOGO, ScriptedResponse(json_body=LOGO_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.get_logo(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == CONNECTOR_LOGO
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_upload_logo_returns_the_new_url_from_a_201(self, api_server: MockAPIServer) -> None:
        """Upload answers ``201 Created`` and returns the new logo URL."""
        api_server.route(CONNECTOR_LOGO, ScriptedResponse(status=201, json_body=UPLOAD_LOGO_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder.upload_logo(
                team_id=TEAM_ID, connector_identifier=CONNECTOR_ID, logo=_logo_file()
            )

        assert result.logo_url == "https://assets.supermetrics.com/images/dsLogos/T3S70_new.png"

    def test_upload_logo_streams_the_bytes_as_multipart(self, api_server: MockAPIServer) -> None:
        """POST on the logo path, carrying the image inside a ``multipart/form-data`` body.

        The point of this layer: the raw PNG bytes, the ``logo`` part name, the filename
        and the MIME type all have to survive onto the wire, and the content type must be
        multipart rather than the form encoding ``create`` uses.
        """
        api_server.route(CONNECTOR_LOGO, ScriptedResponse(status=201, json_body=UPLOAD_LOGO_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder.upload_logo(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID, logo=_logo_file())

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTOR_LOGO
        assert request.bearer_token == "api_k"
        assert request.headers["content-type"].startswith("multipart/form-data")

        assert LOGO_BYTES in request.body
        assert b'name="logo"' in request.body
        assert b'filename="logo.png"' in request.body
        assert b"image/png" in request.body


class TestConnectorBuilderAsyncResource:
    """Asynchronous connectors — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_the_connectors(self, api_server: MockAPIServer) -> None:
        """The async path returns the same ``{count, connectors}`` and sends the same query.

        Like the sync client, a bare ``list`` serializes ``include_configs=false`` because
        the generated stub's default defeats the adapter's drop-the-default guard.
        """
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder.list(team_id=TEAM_ID)

        assert result.count == 1
        assert result.connectors[0].connector_identifier == CONNECTOR_ID

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == CONNECTORS_COLLECTION
        assert parse_qs(urlsplit(request.path).query) == {"include_configs": ["false"]}
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_list_forwards_include_configs_when_true(self, api_server: MockAPIServer) -> None:
        """The query flag is serialized identically on the async path."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            await client.connector_builder.list(team_id=TEAM_ID, include_configs=True)

        query = parse_qs(urlsplit(api_server.last_request.path).query)
        assert query == {"include_configs": ["true"]}

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_result(self, api_server: MockAPIServer) -> None:
        """An empty team is ``count == 0`` on the async path too."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(json_body=CONNECTORS_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder.list(team_id=TEAM_ID)

        assert result.count == 0
        assert result.connectors == []

    @pytest.mark.asyncio
    async def test_get_returns_the_connector_with_configuration(self, api_server: MockAPIServer) -> None:
        """GET on the by-id path, unwrapped to the connector with its config."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(json_body=CONNECTOR_WITH_CONFIG_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            connector = await client.connector_builder.get(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        assert connector.connector_identifier == CONNECTOR_ID
        assert connector.configuration.configuration_json["base_url"] == "https://api.example.com"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == CONNECTOR_ITEM
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_create_returns_the_connector_and_sends_a_form_body(self, api_server: MockAPIServer) -> None:
        """201 on the async path, with the form-urlencoded body reaching the wire."""
        api_server.route(CONNECTORS_COLLECTION, ScriptedResponse(status=201, json_body=CONNECTOR_WITH_CONFIG_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            connector = await client.connector_builder.create(
                team_id=TEAM_ID, title="Test Connector", description="A custom connector"
            )

        assert connector.connector_identifier == CONNECTOR_ID

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == CONNECTORS_COLLECTION
        assert request.bearer_token == "api_k"
        assert request.headers["content-type"].startswith("application/x-www-form-urlencoded")

        form = parse_qs(request.body.decode())
        assert form == {"title": ["Test Connector"], "description": ["A custom connector"]}

    @pytest.mark.asyncio
    async def test_update_returns_none_and_sends_a_json_put(self, api_server: MockAPIServer) -> None:
        """204 on the async path, with both blocks in the JSON body."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder.update(
                team_id=TEAM_ID,
                connector_identifier=CONNECTOR_ID,
                connector=UPDATE_CONNECTOR,
                configuration=UPDATE_CONFIGURATION,
            )

        assert result is None

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == CONNECTOR_ITEM
        assert request.headers["content-type"].startswith("application/json")

        body: dict[str, Any] = request.json()
        assert body == {
            "connector": {"name": "Renamed Connector", "description": "Now with a description"},
            "configuration": {"configuration_json": {"base_url": "https://api.example.com", "auth": "apikey"}},
        }

    @pytest.mark.asyncio
    async def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """204 with an empty body means ``None`` on the async client as well."""
        api_server.route(CONNECTOR_ITEM, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder.delete(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        assert result is None

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == CONNECTOR_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    @pytest.mark.asyncio
    async def test_get_logo_returns_the_url(self, api_server: MockAPIServer) -> None:
        """``get_logo`` unwraps to the URL on the async path."""
        api_server.route(CONNECTOR_LOGO, ScriptedResponse(json_body=LOGO_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            logo = await client.connector_builder.get_logo(team_id=TEAM_ID, connector_identifier=CONNECTOR_ID)

        assert logo.logo_url == "https://assets.supermetrics.com/images/dsLogos/T3S70.png"

        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == CONNECTOR_LOGO
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_upload_logo_streams_the_bytes_as_multipart(self, api_server: MockAPIServer) -> None:
        """201 on the async path, with the image bytes inside a multipart body."""
        api_server.route(CONNECTOR_LOGO, ScriptedResponse(status=201, json_body=UPLOAD_LOGO_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder.upload_logo(
                team_id=TEAM_ID, connector_identifier=CONNECTOR_ID, logo=_logo_file()
            )

        assert result.logo_url == "https://assets.supermetrics.com/images/dsLogos/T3S70_new.png"

        request = api_server.last_request
        assert request.method == "POST"
        assert request.path == CONNECTOR_LOGO
        assert request.bearer_token == "api_k"
        assert request.headers["content-type"].startswith("multipart/form-data")
        assert LOGO_BYTES in request.body
        assert b'filename="logo.png"' in request.body
        assert b"image/png" in request.body
