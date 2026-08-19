"""End-to-end tests for the custom fields error taxonomy.

Every failure here is a real HTTP response with a real status and real headers, driven
through the whole stack over a loopback socket. Error classification, ``Retry-After``
parsing and correlation-header capture only exist on the wire, so a mocked transport
cannot observe any of them.

Two things about this domain make it worth its own module rather than a couple of cases
bolted onto the happy-path tests:

- **400 is the validation failure, not 422.** The spec documents no 422 anywhere in the
  custom fields domain; a rejected ``definition`` comes back as 400.
- **``delete`` returns 204 on success**, and its adapter branches on that status before
  raising. A 404 that slipped past that branch would surface as a successful delete.
"""

from __future__ import annotations

import pytest

from supermetrics import (
    DefinitionValue,
    FunctionArgument,
    FunctionStep,
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
    CUSTOM_FIELDS_COLLECTION,
    CUSTOM_FIELDS_ITEM,
    CUSTOM_FIELDS_METADATA,
    MockAPIServer,
    ScriptedResponse,
)

pytestmark = pytest.mark.e2e


def _error_envelope(code: str, message: str) -> dict[str, object]:
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


#: Every failure status the custom fields spec documents, and the class each becomes.
#: There is deliberately no 422 entry: this domain documents none, and an invalid
#: definition is reported as 400 instead — see ``TestCustomFieldsWriteErrors``.
DOCUMENTED_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (404, "NOT_FOUND", SupermetricsNotFoundError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


def _definition() -> list[FunctionStep]:
    """A minimal well-formed definition, so writes fail on the scripted status alone."""
    return [
        FunctionStep(
            type_="function",
            name="upper_case",
            arguments=[
                FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))
            ],
        )
    ]


class TestCustomFieldsErrorTaxonomy:
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
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.custom_fields.get(team_id=42, custom_field_id=42)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == CUSTOM_FIELDS_ITEM

    def test_rate_limit_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the 429 response rather than guessed."""
        api_server.route(
            CUSTOM_FIELDS_ITEM,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "42"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.custom_fields.get(team_id=42, custom_field_id=42)

        assert exc_info.value.retry_after == 42

    def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """X-Request-Id on the failing response is reachable on the exception."""
        api_server.route(
            CUSTOM_FIELDS_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-cf-500", "X-Span-Id": "span-cf-500"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.custom_fields.get(team_id=42, custom_field_id=42)

        assert exc_info.value.request_id == "req-cf-500"
        assert exc_info.value.span_id == "span-cf-500"

    @pytest.mark.parametrize(("status", "code"), [(401, "UNAUTHORIZED"), (500, "INTERNAL_SERVER_ERROR")])
    def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer, status: int, code: str) -> None:
        """No exception stringifies the credential, whoever ends up logging it."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.custom_fields.get(team_id=42, custom_field_id=42)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestCustomFieldsWriteErrors:
    """The write methods classify failures too — including delete, whose success is 204."""

    def test_create_reports_a_rejected_definition_as_400(self, api_server: MockAPIServer) -> None:
        """An unusable definition is a 400, not a 422.

        The custom fields spec documents no 422 status on any operation, which is why
        this module has no 422 case: 400 is where a rejected definition arrives.
        """
        api_server.route(
            CUSTOM_FIELDS_COLLECTION,
            ScriptedResponse(
                status=400,
                json_body=_error_envelope("VALIDATION_ERROR", "unknown function 'upper_kase'"),
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.custom_fields.create(
                    team_id=42,
                    display_name="Platform (upper)",
                    field_type="dim",
                    data_type="string.text.value",
                    definition=_definition(),
                )

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "VALIDATION_ERROR"
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.path == CUSTOM_FIELDS_COLLECTION

    def test_update_of_a_missing_field_raises_not_found(self, api_server: MockAPIServer) -> None:
        """A 404 on the item path becomes SupermetricsNotFoundError, not a bare API error."""
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "x")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.custom_fields.update(
                    team_id=42,
                    custom_field_id=42,
                    display_name="Platform (upper)",
                    data_type="string.text.value",
                    definition=_definition(),
                )

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "PUT"

    def test_delete_404_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """delete() returns None on 204, so a 404 must still raise rather than return.

        The adapter branches on ``status_code == 204`` and returns ``None``. Any
        regression that widens that branch would turn a missing custom field into a
        silently successful delete, which is exactly the bug this pins down.
        """
        api_server.route(
            CUSTOM_FIELDS_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such custom field")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.custom_fields.delete(team_id=42, custom_field_id=42)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == CUSTOM_FIELDS_ITEM


class TestCustomFieldsCollectionErrors:
    """list() and get_metadata() classify failures like the item endpoints do."""

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_list_failures_are_classified(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """A failing collection GET raises instead of degrading to an empty page."""
        api_server.route(
            CUSTOM_FIELDS_COLLECTION, ScriptedResponse(status=status, json_body=_error_envelope(code, "boom"))
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.custom_fields.list(team_id=42)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (401, "UNAUTHORIZED", SupermetricsAuthError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_get_metadata_failures_are_classified(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The metadata endpoint gets the same taxonomy as the rest of the domain."""
        api_server.route(
            CUSTOM_FIELDS_METADATA, ScriptedResponse(status=status, json_body=_error_envelope(code, "boom"))
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.custom_fields.get_metadata(team_id=42)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.path == CUSTOM_FIELDS_METADATA


class TestCustomFieldsAsyncErrorTaxonomy:
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
        api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.custom_fields.get(team_id=42, custom_field_id=42)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"

    @pytest.mark.asyncio
    async def test_delete_404_is_not_swallowed_by_the_204_check(self, api_server: MockAPIServer) -> None:
        """The async delete has the same 204 branch, and the same way to get it wrong."""
        api_server.route(
            CUSTOM_FIELDS_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such custom field")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await client.custom_fields.delete(team_id=42, custom_field_id=42)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.method == "DELETE"

    @pytest.mark.asyncio
    async def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer) -> None:
        """Credential hygiene holds on the async path too."""
        api_server.route(
            CUSTOM_FIELDS_ITEM,
            ScriptedResponse(status=401, json_body=_error_envelope("ACCESS_TOKEN_INVALID", "expired")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.custom_fields.get(team_id=42, custom_field_id=42)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)
