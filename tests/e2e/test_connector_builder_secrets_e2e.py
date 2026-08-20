"""End-to-end tests for the Connector Builder Secrets resource.

Drives all four methods — list, create, update, delete — over a real loopback socket.

Two things about the wire contract are load-bearing here and only observable at this
layer:

* The path carries a ``/v1`` prefix. The resource's internal ``endpoint`` string (used
  only for error context) omits it, but the generated client prepends ``/v1`` to the URL
  it actually sends, so the routes below all start with ``/v1``. A dropped prefix would
  surface as the server's default 404, not as an obvious mistake.
* ``list`` and ``create`` return a bare ``{"count": N, "secrets": [...]}`` body — no
  ``{"data": ...}`` envelope — while ``update`` and ``delete`` answer ``204 No Content``
  with a genuinely empty body and the adapter maps that to ``None``.

Secrets are served from the core API host and are never re-hosted to the Data Warehouse
host, so one server is the whole story. Every method gets a return-value test and an
outgoing-request test; the request half is the point of this layer — a mocked transport
cannot see that ``create`` sends exactly ``secret_name``/``secret_value`` or that
``update`` targets the by-placeholder path with only ``secret_value`` in the body.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote, urlsplit

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

# --- Routes -------------------------------------------------------------------
#
# team 42, connector "my-connector", and a placeholder shaped like the upstream example
# (``sec_a23f23d26``) so the by-id route needs no URL-encoding to match.

SECRETS_COLLECTION = "/v1/teams/42/connector_builder/connectors/my-connector/secrets"
SECRET_PLACEHOLDER = "sec_a23f23d26"
SECRETS_ITEM = f"{SECRETS_COLLECTION}/{SECRET_PLACEHOLDER}"

# --- Response payloads --------------------------------------------------------
#
# A Secret carries only its placeholder and human-readable name; the value is never
# returned by the API, so it never appears in a response body.

SECRET_PAYLOAD: dict[str, Any] = {"secret_placeholder": SECRET_PLACEHOLDER, "secret_name": "client_id"}
SECRET_PAYLOAD_2: dict[str, Any] = {"secret_placeholder": "sec_b91c4470f", "secret_name": "client_secret"}

#: GET .../secrets — bare, with a `count` alongside the `secrets` array.
SECRETS_LIST_BODY: dict[str, Any] = {"count": 2, "secrets": [SECRET_PAYLOAD, SECRET_PAYLOAD_2]}

#: An empty connector. `count` is required, so an empty list is `{"count": 0, "secrets": []}`,
#: never a body with the `secrets` key missing.
SECRETS_EMPTY_LIST_BODY: dict[str, Any] = {"count": 0, "secrets": []}

#: POST .../secrets — 201, returning the updated list (the value just sent is not echoed).
SECRET_CREATED_BODY: dict[str, Any] = {"count": 1, "secrets": [SECRET_PAYLOAD]}


class TestConnectorBuilderSecretsResource:
    """Synchronous connector-secret list, create, update and delete."""

    def test_list_returns_count_and_secrets(self, api_server: MockAPIServer) -> None:
        """The body is bare — the adapter hands back the parsed ``count`` and ``secrets``."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(json_body=SECRETS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_secrets.list(team_id=42, connector_identifier="my-connector")

        assert result.count == 2
        assert [s.secret_placeholder for s in result.secrets] == [SECRET_PLACEHOLDER, "sec_b91c4470f"]
        assert [s.secret_name for s in result.secrets] == ["client_id", "client_secret"]

    def test_list_sends_a_get_to_the_collection(self, api_server: MockAPIServer) -> None:
        """GET on ``/v1/teams/{team}/.../secrets``, no query string, no body."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(json_body=SECRETS_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_secrets.list(team_id=42, connector_identifier="my-connector")

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == SECRETS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_list_returns_an_empty_list_when_the_connector_has_no_secrets(self, api_server: MockAPIServer) -> None:
        """An empty connector answers ``count: 0`` with an empty array, not an error."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(json_body=SECRETS_EMPTY_LIST_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_secrets.list(team_id=42, connector_identifier="my-connector")

        assert result.count == 0
        assert result.secrets == []

    def test_create_returns_the_updated_list_from_a_201(self, api_server: MockAPIServer) -> None:
        """Creation answers ``201 Created`` — not 200 — and returns the updated secret list."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(status=201, json_body=SECRET_CREATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_secrets.create(
                team_id=42,
                connector_identifier="my-connector",
                secret_name="client_id",
                secret_value="sk-abc123",
            )

        assert result.count == 1
        assert result.secrets[0].secret_placeholder == SECRET_PLACEHOLDER
        assert result.secrets[0].secret_name == "client_id"

    def test_create_sends_name_and_value_in_the_body(self, api_server: MockAPIServer) -> None:
        """POST to the collection with exactly ``secret_name`` and ``secret_value``.

        The plaintext value goes out in the request body — the only place it ever travels —
        and nothing else may leak into the payload.
        """
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(status=201, json_body=SECRET_CREATED_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_secrets.create(
                team_id=42,
                connector_identifier="my-connector",
                secret_name="client_id",
                secret_value="sk-abc123",
            )

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == SECRETS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert set(body) == {"secret_name", "secret_value"}
        assert body["secret_name"] == "client_id"
        assert body["secret_value"] == "sk-abc123"

    def test_update_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """A successful update answers ``204 No Content`` and the adapter returns ``None``."""
        api_server.route(SECRETS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_secrets.update(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=SECRET_PLACEHOLDER,
                secret_value="sk-new-value",
            )

        assert result is None

    def test_update_sends_only_the_value_to_the_by_placeholder_path(self, api_server: MockAPIServer) -> None:
        """PUT on the by-placeholder path, with only ``secret_value`` in the body.

        ``secret_name`` cannot be changed on update, so the payload carries the value alone —
        anything else would be rejected upstream.
        """
        api_server.route(SECRETS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_secrets.update(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=SECRET_PLACEHOLDER,
                secret_value="sk-new-value",
            )

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == SECRETS_ITEM
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert set(body) == {"secret_value"}
        assert body["secret_value"] == "sk-new-value"

    def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """Deletion answers ``204 No Content`` with a genuinely empty body."""
        api_server.route(SECRETS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = client.connector_builder_secrets.delete(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=SECRET_PLACEHOLDER,
            )

        assert result is None

    def test_delete_sends_a_delete_to_the_by_placeholder_path(self, api_server: MockAPIServer) -> None:
        """DELETE on the by-placeholder path, with no body of its own."""
        api_server.route(SECRETS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_secrets.delete(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=SECRET_PLACEHOLDER,
            )

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == SECRETS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""

    def test_placeholder_with_special_characters_is_url_encoded(self, api_server: MockAPIServer) -> None:
        """A ``{{API_KEY}}``-style placeholder is percent-encoded into the path.

        The generated client quotes each path segment with ``safe=""``, so the braces of a
        template-style placeholder never travel as literals — proving that with a real
        placeholder means routing the encoded form the server actually sees.
        """
        placeholder = "{{API_KEY}}"
        encoded_path = f"{SECRETS_COLLECTION}/{quote(placeholder, safe='')}"
        api_server.route(encoded_path, ScriptedResponse(status=204, raw_body=b""))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.connector_builder_secrets.delete(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=placeholder,
            )

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == encoded_path
        assert "{{API_KEY}}" not in request.path
        assert request.bearer_token == "api_k"


class TestConnectorBuilderSecretsAsyncResource:
    """Asynchronous connector secrets — same wire behaviour, its own event hooks."""

    @pytest.mark.asyncio
    async def test_list_returns_count_and_secrets(self, api_server: MockAPIServer) -> None:
        """The async path parses the bare body identically."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(json_body=SECRETS_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_secrets.list(team_id=42, connector_identifier="my-connector")

        assert result.count == 2
        assert [s.secret_name for s in result.secrets] == ["client_id", "client_secret"]

        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == SECRETS_COLLECTION
        assert urlsplit(request.path).query == ""
        assert request.bearer_token == "api_k"

    @pytest.mark.asyncio
    async def test_list_returns_an_empty_list_when_the_connector_has_no_secrets(
        self, api_server: MockAPIServer
    ) -> None:
        """An empty connector answers ``count: 0`` on the async path too."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(json_body=SECRETS_EMPTY_LIST_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_secrets.list(team_id=42, connector_identifier="my-connector")

        assert result.count == 0
        assert result.secrets == []

    @pytest.mark.asyncio
    async def test_create_returns_the_list_and_sends_name_and_value(self, api_server: MockAPIServer) -> None:
        """201 on the async path, with exactly ``secret_name``/``secret_value`` on the wire."""
        api_server.route(SECRETS_COLLECTION, ScriptedResponse(status=201, json_body=SECRET_CREATED_BODY))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_secrets.create(
                team_id=42,
                connector_identifier="my-connector",
                secret_name="client_id",
                secret_value="sk-abc123",
            )

        assert result.count == 1
        assert result.secrets[0].secret_placeholder == SECRET_PLACEHOLDER

        request = api_server.last_request
        assert request.method == "POST"
        assert urlsplit(request.path).path == SECRETS_COLLECTION
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert set(body) == {"secret_name", "secret_value"}
        assert body["secret_value"] == "sk-abc123"

    @pytest.mark.asyncio
    async def test_update_returns_none_and_sends_only_the_value(self, api_server: MockAPIServer) -> None:
        """204 maps to ``None``; the PUT body carries only ``secret_value``."""
        api_server.route(SECRETS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_secrets.update(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=SECRET_PLACEHOLDER,
                secret_value="sk-new-value",
            )

        assert result is None

        request = api_server.last_request
        assert request.method == "PUT"
        assert request.path == SECRETS_ITEM
        assert request.bearer_token == "api_k"

        body: dict[str, Any] = request.json()
        assert set(body) == {"secret_value"}
        assert body["secret_value"] == "sk-new-value"

    @pytest.mark.asyncio
    async def test_delete_returns_none_on_a_204(self, api_server: MockAPIServer) -> None:
        """204 with an empty body means ``None`` on the async client as well."""
        api_server.route(SECRETS_ITEM, ScriptedResponse(status=204, raw_body=b""))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            result = await client.connector_builder_secrets.delete(
                team_id=42,
                connector_identifier="my-connector",
                secret_placeholder=SECRET_PLACEHOLDER,
            )

        assert result is None

        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == SECRETS_ITEM
        assert request.bearer_token == "api_k"
        assert request.body == b""
