"""End-to-end tests for per-request overrides and raw responses on data blending.

Blends repeat the Custom Fields shape on the wire — a ``201`` create with a ``Location``
header, a bodyless ``204`` delete, a ``PUT`` whole-object update — so the same three
overrides (``auth_token``, ``headers``, ``timeout``) have to behave identically here, on
every verb rather than only on reads. These tests pin that down over a real socket.

The one place blends genuinely differ is the collection: it is **not** paginated, so
``meta`` carries a request id and nothing else. ``with_raw_response`` therefore earns its
place for a different reason than it does on custom fields — not to recover a pagination
block the ergonomic return type drops, but for the status code, the response headers, and
the request id.
"""

from __future__ import annotations

from typing import Any

import pytest

from supermetrics import (
    BlendConfig,
    BlendDatasourceFieldRef,
    BlendedDataSourceInput,
    BlendField,
    SupermetricsAsyncClient,
    SupermetricsClient,
)
from supermetrics.exceptions import NetworkError
from supermetrics.response import ApiResponse

from .conftest import (
    BLEND_LIST_BODY,
    BLEND_SINGLE_BODY,
    BLENDS_COLLECTION,
    BLENDS_ITEM,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e

#: The request-side alias for a data source that does not exist yet. Exactly eight
#: lowercase alphanumerics, as the spec's ``^[a-z0-9]{8}$`` demands; every field
#: reference in the same body points at it instead of at an id.
_SOURCE_KEY = "abcd1234"


def _sources() -> list[BlendedDataSourceInput]:
    """Build the one blended data source that create and update calls send.

    ``blend_data_source_id``, ``blend_data_source_key``, ``report_type`` and
    ``report_type_settings`` are required-but-nullable upstream, so the generated model
    makes them positional with no defaults: all five arguments have to be passed, and
    three of them are routinely null on a create.
    """
    return [
        BlendedDataSourceInput(
            data_source_id="GA4",
            blend_data_source_id=None,
            blend_data_source_key=_SOURCE_KEY,
            report_type=None,
            report_type_settings=[],
        )
    ]


def _config() -> BlendConfig:
    """Build a minimal union-blend config: one field, mapped to one data-source field."""
    return BlendConfig(
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_datasource_fields=[
                    BlendDatasourceFieldRef(
                        datasource_field_name="Impressions",
                        field_source="standard",
                        blend_data_source_key=_SOURCE_KEY,
                    )
                ],
                blend_field_display_name="Impressions",
            )
        ]
    )


class TestBlendsOverridesResource:
    """Per-request auth, headers, and timeout applied to blend calls."""

    def test_auth_token_overrides_the_client_credential_for_one_call(self, blends_server: MockAPIServer) -> None:
        """The scoped token is used for that call only; the next reverts to the client key."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.list(42, auth_token="otok_scoped")
            client.blends.list(42)

        assert [r.bearer_token for r in blends_server.requests] == ["otok_scoped", "api_k"]

    def test_auth_token_override_on_a_by_id_read(self, blends_server: MockAPIServer) -> None:
        """`get` honours the scoped credential the same way `list` does."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.get(42, 569, auth_token="otok_scoped")
            client.blends.get(42, 569)

        assert [r.bearer_token for r in blends_server.requests] == ["otok_scoped", "api_k"]

    def test_headers_reach_the_wire(self, blends_server: MockAPIServer) -> None:
        """Correlation and idempotency headers are sent, recorded lower-cased."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.list(
                42,
                headers={"X-Span-Id": "span-blend-1", "Idempotency-Key": "idem-blend-1"},
            )

        received = blends_server.last_request.headers
        assert received["x-span-id"] == "span-blend-1"
        assert received["idempotency-key"] == "idem-blend-1"

    def test_headers_do_not_leak_into_the_next_call(self, blends_server: MockAPIServer) -> None:
        """Per-request headers are unbound once the call returns."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.list(42, headers={"X-Span-Id": "only-once"})
            client.blends.list(42)

        assert blends_server.requests[0].headers.get("x-span-id") == "only-once"
        assert "x-span-id" not in blends_server.requests[1].headers

    def test_sm_app_id_travels_through_the_headers_argument(self, blends_server: MockAPIServer) -> None:
        """`Sm-App-Id` has no named parameter by design: `headers=` already carries it."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            client.blends.get(42, 569, headers={"Sm-App-Id": "XPLD"})

        assert blends_server.last_request.headers["sm-app-id"] == "XPLD"

    def test_sm_app_id_on_a_write(self, api_server: MockAPIServer) -> None:
        """The same escape hatch works on create, where app attribution matters most."""
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=201, json_body=BLEND_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.create(
                42,
                "GA4 impressions",
                "union",
                _sources(),
                _config(),
                headers={"Sm-App-Id": "XPLD"},
            )

        assert api_server.last_request.method == "POST"
        assert api_server.last_request.headers["sm-app-id"] == "XPLD"

    def test_auth_token_override_on_a_write(self, api_server: MockAPIServer) -> None:
        """The overrides apply to every verb, not only to GETs.

        A blend is replaced with ``PUT`` and removed with ``DELETE``; both go through the
        same request-scoped auth path as a read. This scopes the token to the update and
        then deletes without it, so the assertion catches both an override that fails to
        apply on a write and one that leaks past the call that asked for it.
        """
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(json_body=BLEND_SINGLE_BODY),
            ScriptedResponse(status=204),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            client.blends.update(42, 569, "GA4 impressions", _sources(), _config(), auth_token="otok_scoped")
            client.blends.delete(42, 569)

        assert [r.method for r in api_server.requests] == ["PUT", "DELETE"]
        assert [r.bearer_token for r in api_server.requests] == ["otok_scoped", "api_k"]

    def test_short_timeout_fires_against_a_slow_blend_endpoint(self, api_server: MockAPIServer) -> None:
        """A 0.25s override times out an endpoint that takes 1.5s to answer."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_SINGLE_BODY, delay=1.5))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=30.0) as client:
            with pytest.raises(NetworkError):
                client.blends.get(42, 569, timeout=0.25)

    def test_timeout_override_does_not_leak_to_the_next_call(self, api_server: MockAPIServer) -> None:
        """After a short-timeout failure the client-level budget applies again."""
        api_server.route(
            BLENDS_COLLECTION,
            ScriptedResponse(json_body=BLEND_LIST_BODY, delay=1.5),
            ScriptedResponse(json_body=BLEND_LIST_BODY),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url, timeout=10.0) as client:
            with pytest.raises(NetworkError):
                client.blends.list(42, timeout=0.25)
            assert len(client.blends.list(42)) == 2


class TestBlendsRawResponseResource:
    """`with_raw_response` keeps the statuses, headers, and envelope the plain methods drop."""

    def test_get_exposes_status_data_and_json_body(self, api_server: MockAPIServer) -> None:
        """The envelope carries the 200, the parsed blend, the JSON, and the correlation ids."""
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(
                json_body=BLEND_SINGLE_BODY,
                headers={"X-Request-Id": "req-blend-1", "X-Span-Id": "span-blend-1"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.blends.get(42, 569)

        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert response.data.blend_id == 569
        assert response.json_body == BLEND_SINGLE_BODY
        assert response.request_id == "req-blend-1"
        assert response.span_id == "span-blend-1"
        assert api_server.last_request.method == "GET"

    def test_create_preserves_the_201_and_the_location_header(self, api_server: MockAPIServer) -> None:
        """Only the raw view can see that create answered 201 and where the blend landed."""
        api_server.route(
            BLENDS_COLLECTION,
            ScriptedResponse(
                status=201,
                json_body=BLEND_SINGLE_BODY,
                headers={"Location": "/v1/teams/42/data-blending/blends/569"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.blends.create(42, "GA4 impressions", "union", _sources(), _config())

        assert response.status_code == 201
        assert response.headers["Location"] == "/v1/teams/42/data-blending/blends/569"
        assert response.data.blend_id == 569
        assert api_server.last_request.method == "POST"

    def test_delete_preserves_the_204_and_carries_no_data(self, api_server: MockAPIServer) -> None:
        """A successful delete is a bodyless 204, so `data` is None but the status survives."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=204))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.blends.delete(42, 569)

        assert response.status_code == 204
        assert response.data is None
        assert response.raw_body == b""
        assert api_server.last_request.method == "DELETE"

    def test_update_preserves_the_200_and_the_parsed_blend(self, api_server: MockAPIServer) -> None:
        """A whole-object replace answers 200 with the persisted blend, parsed into `.data`."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_SINGLE_BODY))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = client.with_raw_response.blends.update(42, 569, "GA4 impressions", _sources(), _config())

        assert response.status_code == 200
        assert response.data.blend_id == 569
        assert response.data.display_name == "GA4 impressions"
        assert api_server.last_request.method == "PUT"

    def test_list_raw_response_returns_the_page_and_an_envelope_with_no_pagination(
        self, blends_server: MockAPIServer
    ) -> None:
        """The raw view returns both the parsed page and the envelope — which has no pagination.

        This is where blends part company with custom fields. There, `list()` returning a
        bare list is only defensible because `with_raw_response` can still reach the
        `meta.pagination` block the ergonomic type throws away. Here the endpoint answers
        with every matching blend in one response and the spec says so outright, so `meta`
        carries a request id and nothing else: there is no pagination block to lose, and
        `list()` returning a bare list loses nothing at all.

        The negative assertion is the point. If a future spec revision starts paginating
        this collection, `meta.pagination` appears, this test fails, and the failure is a
        signal that `list()` has begun dropping data.
        """
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            response = client.with_raw_response.blends.list(42)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert [item.blend_id for item in response.data] == [569, 570]

        body: Any = response.json_body
        assert body["meta"]["request_id"] == "req_0123456789abcdef"
        assert "pagination" not in body["meta"]

    def test_raw_view_still_honours_per_request_overrides(self, blends_server: MockAPIServer) -> None:
        """The mirrored methods keep the full signature, overrides included."""
        with SupermetricsClient(api_key="api_k", base_url=blends_server.base_url) as client:
            response = client.with_raw_response.blends.list(
                42, auth_token="otok_scoped", headers={"X-Span-Id": "raw-span"}
            )

        assert response.status_code == 200
        assert blends_server.last_request.bearer_token == "otok_scoped"
        assert blends_server.last_request.headers["x-span-id"] == "raw-span"


class TestBlendsOverridesAsyncResource:
    """The async surface applies the same overrides and exposes the same envelope."""

    @pytest.mark.asyncio
    async def test_auth_token_overrides_the_client_credential_for_one_call(self, blends_server: MockAPIServer) -> None:
        """The async client scopes the override to a single awaited call."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            await client.blends.list(42, auth_token="otok_scoped")
            await client.blends.list(42)

        assert [r.bearer_token for r in blends_server.requests] == ["otok_scoped", "api_k"]

    @pytest.mark.asyncio
    async def test_headers_reach_the_wire(self, blends_server: MockAPIServer) -> None:
        """Per-request headers, `Sm-App-Id` included, are sent on the async path too."""
        async with SupermetricsAsyncClient(api_key="api_k", base_url=blends_server.base_url) as client:
            await client.blends.get(42, 569, headers={"X-Span-Id": "async-span", "Sm-App-Id": "XPLD"})

        received = blends_server.last_request.headers
        assert received["x-span-id"] == "async-span"
        assert received["sm-app-id"] == "XPLD"

    @pytest.mark.asyncio
    async def test_get_raw_response_carries_the_envelope(self, api_server: MockAPIServer) -> None:
        """The async raw view exposes the same status, data, and correlation ids as the sync one."""
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(json_body=BLEND_SINGLE_BODY, headers={"X-Request-Id": "req-async-blend"}),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.blends.get(42, 569)

        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert response.data.blend_id == 569
        assert response.json_body == BLEND_SINGLE_BODY
        assert response.request_id == "req-async-blend"

    @pytest.mark.asyncio
    async def test_delete_raw_response_preserves_the_204(self, api_server: MockAPIServer) -> None:
        """The bodyless 204 survives the async raw view too, `data` and body both empty."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=204))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            response = await client.with_raw_response.blends.delete(42, 569)

        assert response.status_code == 204
        assert response.data is None
        assert response.raw_body == b""
        assert api_server.last_request.method == "DELETE"
