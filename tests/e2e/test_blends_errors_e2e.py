"""End-to-end tests for the data blending error taxonomy.

Every failure here is a real HTTP response with a real status and real headers, driven
through the whole stack over a loopback socket. Error classification, ``Retry-After``
parsing and correlation-header capture only exist on the wire, so a mocked transport
cannot observe any of them.

Three things about this domain make it worth its own module rather than a couple of cases
bolted onto the happy-path tests:

- **400 is the validation failure, not 422.** The spec documents no 422 anywhere in the
  data blending domain; a rejected blend definition comes back as 400.
- **The two collection operations document no 404.** ``list`` and ``create`` document
  400, 401, 403, 429 and 500 only, while the three by-id operations add 404 — so the
  status table is not the same on both routes and is written out twice on purpose.
- **``delete`` returns 204 on success**, and its adapter branches on that status before
  raising. A 404 that slipped past that branch would surface as a successful delete.
"""

from __future__ import annotations

import pytest

from supermetrics import (
    BlendConfig,
    BlendDatasourceFieldRef,
    BlendedDataSourceInput,
    BlendField,
    SupermetricsAsyncClient,
    SupermetricsClient,
)
from supermetrics.exceptions import (
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

from .conftest import (
    BLENDS_COLLECTION,
    BLENDS_ITEM,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e


def _error_envelope(code: str, message: str) -> dict[str, object]:
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


#: A 200 whose body is missing the required ``data`` key. The generated
#: ``BlendResponse.from_dict`` pops ``data`` and raises ``KeyError``; the point of the
#: test that uses this is that the caller must never see that ``KeyError``.
_BLEND_BODY_WITHOUT_DATA: dict[str, object] = {"meta": {"request_id": "req_0123456789ab"}}

#: The create-time alias every field reference in the same request points at.
_BLEND_DATA_SOURCE_KEY = "abcd1234"


#: Every failure status the by-id blend operations document, and the class each becomes.
#: There is deliberately no 422 entry: this domain documents none on any operation, and a
#: rejected blend is reported as 400 instead — see ``TestBlendsWriteErrors``.
DOCUMENTED_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (404, "NOT_FOUND", SupermetricsNotFoundError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]

#: The same table for the *collection* route, which documents one status fewer. ``list``
#: and ``create`` have no 404 in the spec — there is no blend id in the path to miss, and
#: an unknown team is reported as 403 — so a 404 there would be undocumented and would
#: reach the caller through the generic path instead of this table.
COLLECTION_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


def _blended_data_sources() -> list[BlendedDataSourceInput]:
    """One well-formed data source, so writes fail on the scripted status alone.

    All five of ``data_source_id``, ``blend_data_source_id``, ``blend_data_source_key``,
    ``report_type`` and ``report_type_settings`` are required-but-nullable upstream, so
    three of them are passed as ``None``/``[]`` rather than omitted.
    """
    return [
        BlendedDataSourceInput(
            data_source_id="GA4",
            blend_data_source_id=None,
            blend_data_source_key=_BLEND_DATA_SOURCE_KEY,
            report_type=None,
            report_type_settings=[],
        )
    ]


def _config() -> BlendConfig:
    """A minimal union-blend config: one field mapped to one data-source field."""
    return BlendConfig(
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_datasource_fields=[
                    BlendDatasourceFieldRef(
                        datasource_field_name="Impressions",
                        field_source="standard",
                        blend_data_source_key=_BLEND_DATA_SOURCE_KEY,
                    )
                ],
                blend_field_display_name="Impressions",
            )
        ]
    )


class TestBlendsErrorTaxonomy:
    """Status-to-exception mapping and preserved transport metadata, on a read method."""

    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Each documented status raises its own class and keeps the upstream code."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.blends.get(team_id=42, blend_id=569)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == BLENDS_ITEM

    def test_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the 429 response rather than guessed."""
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "42"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.blends.get(team_id=42, blend_id=569)

        assert exc_info.value.retry_after == 42

    def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """X-Request-Id and X-Span-Id on the failing response are reachable on the exception."""
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-blend-500", "X-Span-Id": "span-blend-500"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.blends.get(team_id=42, blend_id=569)

        assert exc_info.value.request_id == "req-blend-500"
        assert exc_info.value.span_id == "span-blend-500"

    @pytest.mark.parametrize(("status", "code"), [(401, "UNAUTHORIZED"), (500, "INTERNAL_SERVER_ERROR")])
    def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer, status: int, code: str) -> None:
        """The credential goes out on the wire and appears in no rendering of the error."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.blends.get(team_id=42, blend_id=569)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)

    def test_malformed_success_body_becomes_an_sdk_error(self, api_server: MockAPIServer) -> None:
        """A 200 that does not match the schema reaches the caller as an SDK error.

        ``BlendResponse.from_dict`` pops the required ``data`` key and raises ``KeyError``
        when it is absent. ``api_error_handler`` catches ``KeyError`` and re-raises it as a
        ``SupermetricsAPIError``; the status is 0 because the transport recorded a 200 and
        there is no failing status to classify by. What must never happen is a bare
        ``KeyError`` escaping the SDK boundary.
        """
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=200, json_body=_BLEND_BODY_WITHOUT_DATA))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.blends.get(team_id=42, blend_id=569)

        assert not isinstance(exc_info.value, KeyError)
        assert exc_info.value.status_code == 0
        assert exc_info.value.endpoint == "/teams/42/data-blending/blends/569"
        assert isinstance(exc_info.value.__cause__, KeyError)


class TestBlendsWriteErrors:
    """The write methods classify failures too — including delete, whose success is 204."""

    def test_create_reports_a_rejected_blend_as_400(self, api_server: MockAPIServer) -> None:
        """An unusable blend definition is a 400, not a 422.

        The data blending spec documents no 422 status on any operation, which is why this
        module has no 422 case: 400 is where a rejected blend arrives, carrying the
        adapter's own context in the message.
        """
        api_server.route(
            BLENDS_COLLECTION,
            ScriptedResponse(
                status=400,
                json_body=_error_envelope("VALIDATION_ERROR", "joins are not allowed on a union blend"),
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.blends.create(
                    team_id=42,
                    display_name="GA4 impressions",
                    blend_type="union",
                    blended_data_sources=_blended_data_sources(),
                    config=_config(),
                )

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "VALIDATION_ERROR"
        assert "Invalid blend definition" in str(exc_info.value)
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.path == BLENDS_COLLECTION

    def test_update_reports_a_rejected_blend_as_400(self, api_server: MockAPIServer) -> None:
        """A rejected replacement is a 400 on the item path, and it really was a PUT."""
        api_server.route(
            BLENDS_COLLECTION,
            ScriptedResponse(status=400, json_body=_error_envelope("BAD_REQUEST", "unreachable collection route")),
        )
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(
                status=400,
                json_body=_error_envelope("VALIDATION_ERROR", "unknown blend_data_source_key 'zzzzzzzz'"),
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.blends.update(
                    team_id=42,
                    blend_id=569,
                    display_name="GA4 impressions",
                    blended_data_sources=_blended_data_sources(),
                    config=_config(),
                )

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "VALIDATION_ERROR"
        assert "Invalid blend definition" in str(exc_info.value)
        assert api_server.last_request.method == "PUT"
        assert api_server.last_request.path == BLENDS_ITEM

    def test_update_of_a_missing_blend_raises_not_found(self, api_server: MockAPIServer) -> None:
        """A 404 on the item path becomes SupermetricsNotFoundError, not a bare API error."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "gone")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.blends.update(
                    team_id=42,
                    blend_id=569,
                    display_name="GA4 impressions",
                    blended_data_sources=_blended_data_sources(),
                    config=_config(),
                )

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "PUT"

    def test_delete_404_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """delete() returns None on 204, so a 404 must still raise rather than return.

        The adapter branches on ``status_code == 204`` and returns ``None``. Any regression
        that widens that branch — to ``< 300``, or to "no parsed body" — would turn a
        missing blend into a silently successful delete, and the caller would have no way
        to tell. This is the highest-value assertion in the module.
        """
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such blend")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.blends.delete(team_id=42, blend_id=569)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == BLENDS_ITEM


class TestBlendsCollectionErrors:
    """list() classifies failures too, over the shorter status set the collection documents."""

    @pytest.mark.parametrize(("status", "code", "expected"), COLLECTION_FAILURES)
    def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Each status the collection documents raises its own class on the collection path.

        The table this runs over has no 404 entry, unlike ``DOCUMENTED_FAILURES``: the
        collection operations document 400, 401, 403, 429 and 500 and nothing else.
        """
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=status, json_body=_error_envelope(code, "boom")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.blends.list(team_id=42)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == BLENDS_COLLECTION

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_list_failure_does_not_degrade_to_an_empty_list(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """A failing collection GET raises instead of answering [].

        ``list()`` legitimately returns ``[]`` when ``data.items`` is absent from a *200*.
        A failure must not take that same exit, or an expired key would read as "this team
        has no blends".
        """
        api_server.route(BLENDS_COLLECTION, ScriptedResponse(status=status, json_body=_error_envelope(code, "boom")))
        returned: object = "not called"

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                returned = client.blends.list(team_id=42)

        assert returned == "not called"
        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code


class TestBlendsAsyncErrorTaxonomy:
    """The async surface has its own event hooks and its own error paths."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (404, "NOT_FOUND", SupermetricsNotFoundError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    async def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async adapter classifies a failing get identically to the sync one."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.blends.get(team_id=42, blend_id=569)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"

    @pytest.mark.asyncio
    async def test_delete_404_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """The async delete has the same 204 branch, and the same way to get it wrong."""
        api_server.route(
            BLENDS_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such blend")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await client.blends.delete(team_id=42, blend_id=569)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "DELETE"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code"), [(401, "ACCESS_TOKEN_INVALID"), (500, "INTERNAL_SERVER_ERROR")])
    async def test_api_key_never_leaks_into_the_message(
        self, api_server: MockAPIServer, status: int, code: str
    ) -> None:
        """Credential hygiene holds on the async path too."""
        api_server.route(BLENDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "expired")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                await client.blends.get(team_id=42, blend_id=569)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)
