"""End-to-end tests for per-request overrides and raw responses on custom fields.

Custom fields are the first resource with a create that answers ``201`` and a delete
that answers ``204``, and the only one whose pagination metadata is unreachable from
the plain method's return value. These tests pin both halves down on the wire: that
``auth_token``/``headers``/``timeout`` behave on custom-field routes exactly as they do
elsewhere, and that ``with_raw_response`` preserves the statuses, headers, and envelope
that the ergonomic return types drop.
"""

from __future__ import annotations

from typing import Any

import pytest

from supermetrics import (
    DefinitionValue,
    FunctionArgument,
    FunctionStep,
    SupermetricsAsyncClient,
    SupermetricsClient,
)
from supermetrics.exceptions import NetworkError
from supermetrics.response import ApiResponse

from .conftest import (
    CUSTOM_FIELD_LIST_BODY,
    CUSTOM_FIELD_SINGLE_BODY,
    CUSTOM_FIELDS_COLLECTION,
    CUSTOM_FIELDS_ITEM,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e


def _definition() -> list[FunctionStep]:
    """Build a minimal one-step definition for create/update calls."""
    return [
        FunctionStep(
            type_="function",
            name="upper_case",
            arguments=[
                FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))
            ],
        )
    ]


class TestCustomFieldsOverridesResource:
    """Per-request auth, headers, and timeout applied to custom-field calls."""

    def test_auth_token_overrides_the_client_credential_for_one_call(self, custom_fields_server: MockAPIServer) -> None:
        """The scoped token is used for that call only; the next reverts to the client key."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.list(42, auth_token="otok_scoped")
            client.custom_fields.list(42)

        assert [r.bearer_token for r in custom_fields_server.requests] == ["otok_scoped", "api_k"]

    def test_auth_token_override_on_a_by_id_read(self, custom_fields_server: MockAPIServer) -> None:
        """`get` honours the scoped credential the same way `list` does."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.get(42, 42, auth_token="otok_scoped")
            client.custom_fields.get(42, 42)

        assert [r.bearer_token for r in custom_fields_server.requests] == ["otok_scoped", "api_k"]

    def test_headers_reach_the_wire(self, custom_fields_server: MockAPIServer) -> None:
        """Correlation and idempotency headers are sent, recorded lower-cased."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.list(
                42,
                headers={"X-Span-Id": "span-cf-1", "Idempotency-Key": "idem-cf-1"},
            )

        received = custom_fields_server.last_request.headers
        assert received["x-span-id"] == "span-cf-1"
        assert received["idempotency-key"] == "idem-cf-1"

    def test_headers_do_not_leak_into_the_next_call(self, custom_fields_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.list(42, headers={"X-Span-Id": "only-once"})
            client.custom_fields.list(42)

        assert custom_fields_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in custom_fields_server.requests[1].headers

    def test_sm_app_id_travels_through_the_headers_argument(self, custom_fields_server: MockAPIServer) -> None:
        """`Sm-App-Id` has no named parameter by design: `headers=` already carries it."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            client.custom_fields.get_metadata(42, headers={"Sm-App-Id": "XPLD"})

        assert custom_fields_server.last_request.headers["sm-app-id"] == "XPLD"

    def test_sm_app_id_on_a_write(self, api_server: MockAPIServer) -> None:
        """The same escape hatch works on create, where app attribution matters most."""
        api_server.route(CUSTOM_FIELDS_COLLECTION, ScriptedResponse(status=201, json_body=CUSTOM_FIELD_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.custom_fields.create(
                42,
                "Platform (upper)",
                "dim",
                "string.text.value",
                _definition(),
                headers={"Sm-App-Id": "XPLD"},
            )

        assert api_server.last_request.method == "POST"
        assert api_server.last_request.headers["sm-app-id"] == "XPLD"

    def test_short_timeout_fires_against_a_slow_custom_field_endpoint(self, api_server: MockAPIServer) -> None:
        """A 0.25s override times out an endpoint that takes 1.5s to answer."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(json_body=CUSTOM_FIELD_SINGLE_BODY, delay=1.5))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.custom_fields.get(42, 42, timeout=0.25)

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout failure the client-level budget applies again."""
        api_server.route(
            CUSTOM_FIELDS_COLLECTION,
            ScriptedResponse(json_body=CUSTOM_FIELD_LIST_BODY, delay=1.5),
            ScriptedResponse(json_body=CUSTOM_FIELD_LIST_BODY),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.custom_fields.list(42, timeout=0.25)
            assert len(client.custom_fields.list(42)) == 1


class TestCustomFieldsRawResponseResource:
    """`with_raw_response` keeps the statuses, headers, and envelope `list`/`create` drop."""

    def test_get_exposes_status_data_and_json_body(self, api_server: MockAPIServer) -> None:
        """The envelope carries the 200, the parsed field, the JSON, and the correlation ids."""
        api_server.route(
            CUSTOM_FIELDS_ITEM,
            ScriptedResponse(
                json_body=CUSTOM_FIELD_SINGLE_BODY,
                headers={"X-Request-Id": "req-cf-1", "X-Span-Id": "span-cf-1"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.custom_fields.get(42, 42)

        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert response.data.id == 42
        assert response.json_body == CUSTOM_FIELD_SINGLE_BODY
        assert response.request_id == "req-cf-1"
        assert response.span_id == "span-cf-1"
        assert api_server.last_request.method == "GET"

    def test_create_preserves_the_201_and_the_location_header(self, api_server: MockAPIServer) -> None:
        """Only the raw view can see that create answered 201 and where the field landed."""
        api_server.route(
            CUSTOM_FIELDS_COLLECTION,
            ScriptedResponse(
                status=201,
                json_body=CUSTOM_FIELD_SINGLE_BODY,
                headers={"Location": "/v1/teams/42/custom-fields/42"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.custom_fields.create(
                42, "Platform (upper)", "dim", "string.text.value", _definition()
            )

        assert response.status_code == 201
        assert response.headers["Location"] == "/v1/teams/42/custom-fields/42"
        assert response.data.id == 42
        assert api_server.last_request.method == "POST"

    def test_delete_preserves_the_204_and_carries_no_data(self, api_server: MockAPIServer) -> None:
        """A successful delete is a bodyless 204, so `data` is None but the status survives."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=204))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.custom_fields.delete(42, 42)

        assert response.status_code == 204
        assert response.data is None
        assert response.raw_body == b""
        assert api_server.last_request.method == "DELETE"

    def test_list_raw_response_is_how_pagination_is_reached(self, custom_fields_server: MockAPIServer) -> None:
        """The raw view returns both the page and the `meta.pagination` block.

        `list()` returns a bare `list[TeamTransformationOutput]` and throws the response
        envelope away. That is only defensible because this path exists: a caller who
        needs `total_count`, `limit`, `offset` or the `links.next` cursor reads them off
        `with_raw_response.custom_fields.list(...).json_body` without giving up the
        parsed models. Delete this test and dropping the envelope becomes data loss.
        """
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            response = client.with_raw_response.custom_fields.list(42)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0].id == 42

        body: Any = response.json_body
        pagination = body["meta"]["pagination"]
        assert pagination["total_count"] == 137
        assert pagination["limit"] == 25
        assert pagination["offset"] == 0
        assert pagination["links"]["next"]["href"].endswith("offset=25&limit=25")

    def test_raw_view_still_honours_per_request_overrides(self, custom_fields_server: MockAPIServer) -> None:
        """The mirrored methods keep the full signature, overrides included."""
        with SupermetricsClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            response = client.with_raw_response.custom_fields.list(
                42, auth_token="otok_scoped", headers={"X-Span-Id": "raw-span"}
            )

        assert response.status_code == 200
        assert custom_fields_server.last_request.bearer_token == "otok_scoped"
        assert custom_fields_server.last_request.headers["x-span-id"] == "raw-span"


class TestCustomFieldsOverridesAsyncResource:
    """The async surface applies the same overrides and exposes the same envelope."""

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_for_one_call(
        self, custom_fields_server: MockAPIServer
    ) -> None:
        """The async client scopes the override to a single awaited call."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            await client.custom_fields.list(42, auth_token="otok_scoped")
            await client.custom_fields.list(42)

        assert [r.bearer_token for r in custom_fields_server.requests] == ["otok_scoped", "api_k"]

    @pytest.mark.asyncio
    async def test_headers_reach_the_wire(self, custom_fields_server: MockAPIServer) -> None:
        """Per-request headers, `Sm-App-Id` included, are sent on the async path too."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            await client.custom_fields.get(42, 42, headers={"X-Span-Id": "async-span", "Sm-App-Id": "XPLD"})

        received = custom_fields_server.last_request.headers
        assert received["x-span-id"] == "async-span"
        assert received["sm-app-id"] == "XPLD"

    @pytest.mark.asyncio
    async def test_list_raw_response_reaches_pagination(self, custom_fields_server: MockAPIServer) -> None:
        """Async callers read `meta.pagination` off the raw envelope, exactly as sync ones do."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=custom_fields_server.base_url) as client:
            response = await client.with_raw_response.custom_fields.list(42)

        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert len(response.data) == 1

        body: Any = response.json_body
        pagination = body["meta"]["pagination"]
        assert pagination["total_count"] == 137
        assert pagination["limit"] == 25
        assert pagination["offset"] == 0
        assert pagination["links"]["next"]["href"].endswith("offset=25&limit=25")
