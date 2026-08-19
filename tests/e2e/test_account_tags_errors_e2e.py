"""End-to-end tests for the account tags error taxonomy.

Every failure here is a real HTTP response with a real status and real headers, driven
through the whole stack over a loopback socket. Error classification, ``Retry-After``
parsing and correlation-header capture only exist on the wire, so a mocked transport
cannot observe any of them.

Three properties of this domain make it worth its own module rather than a couple of
cases bolted onto the happy-path tests:

- **Nothing 404s.** The spec documents 400, 401, 403, 429 and 500 on every operation and
  a 404 on none of them — not on ``get``, not on ``update``, not on ``delete``, not on
  the two PATCHes. A missing tag arrives as a 400, or as a 200 with ``result=false``.
  There is deliberately no test here asserting ``SupermetricsNotFoundError`` as though
  it were the contract; the one 404 case is labelled as SDK fallback behaviour.
- **409 is unique to ``create``**, and is the only 409 anywhere in the SDK. It stays a
  plain :class:`SupermetricsAPIError` on purpose — see
  ``docs.local/plans/phase6-account-tags.md`` §2.3 — and
  :class:`TestAccountTagsCreateConflict` pins that so a future change to the taxonomy
  shows up as a failing assertion rather than a silent reclassification.
- **``delete`` succeeds with a 200 carrying a boolean**, so its adapter reads the body
  rather than the status. A failure that leaked through that branch would look like a
  tag that simply was not there.

The routes are spelled out here rather than in ``conftest.py`` because this module owns
them; the happy-path module scripts the same paths for successful responses.
"""

from __future__ import annotations

from typing import Any

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import (
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
)

from .conftest import MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e

#: Account tags live on the CORE api host under a "/v1" path prefix, so the routes carry
#: the version. A regression that re-hosted them or dropped the "/v1" would fall through
#: to the mock server's default 404 rather than reaching the scripted status.
TEAM_ID = 42
TAG_NAME = "a1b2c3d"
ACCOUNT_TAGS_COLLECTION = f"/v1/teams/{TEAM_ID}/account_tags"
ACCOUNT_TAGS_ITEM = f"{ACCOUNT_TAGS_COLLECTION}/{TAG_NAME}"
ACCOUNT_TAGS_ADD = f"{ACCOUNT_TAGS_ITEM}/add"
ACCOUNT_TAGS_REMOVE = f"{ACCOUNT_TAGS_ITEM}/remove"

#: The membership selection shape the spec's own example documents. Well-formed, so the
#: write methods below fail on the scripted status alone.
DATA_SOURCES: list[dict[str, Any]] = [{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}]


def _error_envelope(code: str, message: str) -> dict[str, object]:
    return {"meta": {"request_id": "req_0123456789ab"}, "error": {"code": code, "message": message}}


#: Every failure status the account tags spec documents on a read operation, and the
#: class each becomes. There is deliberately no 404 entry — this domain documents none —
#: and no 422 entry either: a rejected request is reported as 400.
DOCUMENTED_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (400, "BAD_REQUEST", SupermetricsValidationError),
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


class TestAccountTagsErrorTaxonomy:
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
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """X-Request-Id and X-Span-Id on the failing response are reachable on the exception."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-at-500", "X-Span-Id": "span-at-500"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.request_id == "req-at-500"
        assert exc_info.value.span_id == "span-at-500"

    @pytest.mark.parametrize(("status", "code"), [(401, "UNAUTHORIZED"), (500, "INTERNAL_SERVER_ERROR")])
    def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer, status: int, code: str) -> None:
        """No exception stringifies the credential, whoever ends up logging it."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestAccountTagsErrorsAcrossVerbs:
    """The taxonomy holds on every verb, not only on the one read method.

    Each test below pairs a different documented status with a different HTTP method, so
    a classification regression confined to one adapter — the PATCHes in particular,
    which are the first of their kind in the SDK — cannot hide behind a green ``get``.
    """

    def test_list_server_error_is_classified(self, api_server: MockAPIServer) -> None:
        """A failing collection GET raises instead of degrading to an empty list."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(status=500, json_body=_error_envelope("INTERNAL_SERVER_ERROR", "boom")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.account_tags.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == 500
        assert exc_info.value.error_code == "INTERNAL_SERVER_ERROR"
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == ACCOUNT_TAGS_COLLECTION

    def test_create_unauthorized_is_classified(self, api_server: MockAPIServer) -> None:
        """A 401 on the POST is an auth error, and the body still went out."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(status=401, json_body=_error_envelope("UNAUTHORIZED", "expired")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                client.account_tags.create(
                    team_id=TEAM_ID,
                    display_name="EMEA paid media",
                    color="#112233",
                    data_sources=DATA_SOURCES,
                )

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "UNAUTHORIZED"
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.path == ACCOUNT_TAGS_COLLECTION

    def test_update_bad_request_is_classified(self, api_server: MockAPIServer) -> None:
        """A rejected rename is a 400, which is where this domain reports validation failures.

        The spec documents no 422 on any account tags operation, so there is no 422 case
        in this module: a colour the API will not accept comes back as a 400.
        """
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=400, json_body=_error_envelope("BAD_REQUEST", "color must be a hex triplet")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.account_tags.update(
                    team_id=TEAM_ID,
                    name=TAG_NAME,
                    display_name="EMEA paid media",
                    color="chartreuse",
                )

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "BAD_REQUEST"
        assert api_server.last_request.method == "PUT"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    def test_add_accounts_forbidden_is_classified(self, api_server: MockAPIServer) -> None:
        """The membership PATCH needs a write scope, and a 403 says so distinctly."""
        api_server.route(
            ACCOUNT_TAGS_ADD,
            ScriptedResponse(status=403, json_body=_error_envelope("FORBIDDEN", "account_tags_write required")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsForbiddenError) as exc_info:
                client.account_tags.add_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert exc_info.value.status_code == 403
        assert exc_info.value.error_code == "FORBIDDEN"
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == ACCOUNT_TAGS_ADD

    def test_remove_accounts_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the 429 response rather than guessed."""
        api_server.route(
            ACCOUNT_TAGS_REMOVE,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.account_tags.remove_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert exc_info.value.status_code == 429
        assert exc_info.value.error_code == "TOO_MANY_REQUESTS"
        assert exc_info.value.retry_after == 30
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == ACCOUNT_TAGS_REMOVE


class TestAccountTagsCreateConflict:
    """409 CONFLICT_ERROR on create — the only 409 the SDK wraps anywhere.

    ``_status_to_exception`` has no 409 branch, so the error surfaces as the base
    :class:`SupermetricsAPIError` carrying ``status_code == 409``. That is a deliberate
    decision, not an oversight: adding a ``SupermetricsConflictError`` would change the
    public error taxonomy on behalf of one endpoint (plan §2.3). These tests exist so
    that changing it later is a visible, failing decision rather than a silent one.
    """

    def test_conflict_is_a_plain_api_error(self, api_server: MockAPIServer) -> None:
        """A duplicate tag raises the base class, with the upstream code intact."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(
                status=409,
                json_body=_error_envelope("CONFLICT_ERROR", "an account tag with that display name exists"),
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.account_tags.create(
                    team_id=TEAM_ID,
                    display_name="EMEA paid media",
                    color="#112233",
                    data_sources=DATA_SOURCES,
                )

        assert exc_info.value.status_code == 409
        assert exc_info.value.error_code == "CONFLICT_ERROR"
        # Not merely "an instance of" - exactly the base class. A 409 that started
        # arriving as SupermetricsValidationError or a new SupermetricsConflictError
        # would still satisfy `pytest.raises(SupermetricsAPIError)`, so assert the type.
        assert type(exc_info.value) is SupermetricsAPIError
        assert api_server.last_request.method == "POST"
        assert api_server.last_request.path == ACCOUNT_TAGS_COLLECTION

    @pytest.mark.asyncio
    async def test_conflict_is_a_plain_api_error_async(self, api_server: MockAPIServer) -> None:
        """The async create classifies the conflict identically."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(
                status=409,
                json_body=_error_envelope("CONFLICT_ERROR", "an account tag with that display name exists"),
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                await client.account_tags.create(
                    team_id=TEAM_ID,
                    display_name="EMEA paid media",
                    color="#112233",
                    data_sources=DATA_SOURCES,
                )

        assert exc_info.value.status_code == 409
        assert exc_info.value.error_code == "CONFLICT_ERROR"
        assert type(exc_info.value) is SupermetricsAPIError
        assert api_server.last_request.method == "POST"


class TestAccountTagsDeleteErrors:
    """delete() answers a boolean on success, so a failure must not look like ``False``.

    ``delete`` is the one method in this domain whose adapter reads the *body* to decide
    what to return: a 200 with ``result=false`` legitimately means "no such tag", because
    deletion is idempotent upstream. A failing status must still raise. Conflating the
    two would turn a permissions problem or a malformed request into a quiet "nothing to
    delete", which is exactly the bug these tests pin down.
    """

    def test_400_raises_instead_of_returning_false(self, api_server: MockAPIServer) -> None:
        """The same route serves a false-y 200 and then a 400; only the second raises."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=200, json_body={"data": {"result": False}}),
            ScriptedResponse(status=400, json_body=_error_envelope("BAD_REQUEST", "malformed tag name")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            # A 200 saying nothing was deleted is a successful call that returns False.
            assert client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME) is False

            # A 400 is a failure, and must not be flattened into the same False.
            with pytest.raises(SupermetricsValidationError) as exc_info:
                client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "BAD_REQUEST"
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    @pytest.mark.parametrize(
        ("status", "code", "expected"),
        [
            (403, "FORBIDDEN", SupermetricsForbiddenError),
            (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
        ],
    )
    def test_other_failures_raise_too(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Every non-200 on the DELETE raises; none of them returns a boolean."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "no")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "DELETE"

    @pytest.mark.asyncio
    async def test_400_raises_instead_of_returning_false_async(self, api_server: MockAPIServer) -> None:
        """The async delete has the same body-reading branch, and the same way to get it wrong."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=200, json_body={"data": {"result": False}}),
            ScriptedResponse(status=400, json_body=_error_envelope("BAD_REQUEST", "malformed tag name")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            assert await client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME) is False

            with pytest.raises(SupermetricsValidationError) as exc_info:
                await client.account_tags.delete(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "BAD_REQUEST"
        assert api_server.last_request.method == "DELETE"


class TestAccountTagsAsyncErrorTaxonomy:
    """The async surface has its own event hooks and its own error paths."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    async def test_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async adapter classifies a failing get identically to the sync one."""
        api_server.route(ACCOUNT_TAGS_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "GET"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    @pytest.mark.asyncio
    async def test_list_server_error_is_classified(self, api_server: MockAPIServer) -> None:
        """A failing collection GET raises on the async client too."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(status=500, json_body=_error_envelope("INTERNAL_SERVER_ERROR", "boom")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.account_tags.list(team_id=TEAM_ID)

        assert exc_info.value.status_code == 500
        assert exc_info.value.error_code == "INTERNAL_SERVER_ERROR"
        assert api_server.last_request.path == ACCOUNT_TAGS_COLLECTION

    @pytest.mark.asyncio
    async def test_create_unauthorized_is_classified(self, api_server: MockAPIServer) -> None:
        """A 401 on the async POST is an auth error."""
        api_server.route(
            ACCOUNT_TAGS_COLLECTION,
            ScriptedResponse(status=401, json_body=_error_envelope("UNAUTHORIZED", "expired")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.account_tags.create(
                    team_id=TEAM_ID,
                    display_name="EMEA paid media",
                    color="#112233",
                    data_sources=DATA_SOURCES,
                )

        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "UNAUTHORIZED"
        assert api_server.last_request.method == "POST"

    @pytest.mark.asyncio
    async def test_update_bad_request_is_classified(self, api_server: MockAPIServer) -> None:
        """A rejected async rename is a 400, not a 422."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=400, json_body=_error_envelope("BAD_REQUEST", "color must be a hex triplet")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsValidationError) as exc_info:
                await client.account_tags.update(
                    team_id=TEAM_ID,
                    name=TAG_NAME,
                    display_name="EMEA paid media",
                    color="chartreuse",
                )

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "BAD_REQUEST"
        assert api_server.last_request.method == "PUT"

    @pytest.mark.asyncio
    async def test_add_accounts_forbidden_is_classified(self, api_server: MockAPIServer) -> None:
        """The async membership PATCH classifies a scope failure as a 403."""
        api_server.route(
            ACCOUNT_TAGS_ADD,
            ScriptedResponse(status=403, json_body=_error_envelope("FORBIDDEN", "account_tags_write required")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsForbiddenError) as exc_info:
                await client.account_tags.add_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert exc_info.value.status_code == 403
        assert exc_info.value.error_code == "FORBIDDEN"
        assert api_server.last_request.method == "PATCH"
        assert api_server.last_request.path == ACCOUNT_TAGS_ADD

    @pytest.mark.asyncio
    async def test_remove_accounts_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After survives the async error path with its value intact."""
        api_server.route(
            ACCOUNT_TAGS_REMOVE,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                await client.account_tags.remove_accounts(team_id=TEAM_ID, name=TAG_NAME, data_sources=DATA_SOURCES)

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30
        assert api_server.last_request.path == ACCOUNT_TAGS_REMOVE

    @pytest.mark.asyncio
    async def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """Correlation headers reach the exception on the async path too."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-at-async-500", "X-Span-Id": "span-at-async-500"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.request_id == "req-at-async-500"
        assert exc_info.value.span_id == "span-at-async-500"

    @pytest.mark.asyncio
    async def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer) -> None:
        """Credential hygiene holds on the async path."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=401, json_body=_error_envelope("ACCESS_TOKEN_INVALID", "expired")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestAccountTagsUndocumented404:
    """What the SDK does with a 404 — which this domain's API contract does not define.

    No account tags operation documents a 404. These two tests are **not** a statement
    about the API; they record the SDK's fallback behaviour if one ever arrives anyway,
    for instance from a gateway or a proxy in front of the service. The generated parser
    has no 404 branch here, so it returns ``None`` and the adapter classifies from the
    transport's recorded status. A caller must not have to distinguish "the API said
    404" from "something between us and the API did".
    """

    def test_an_undocumented_404_still_classifies_by_status(self, api_server: MockAPIServer) -> None:
        """An unmodelled 404 becomes SupermetricsNotFoundError rather than losing its status."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such account tag")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert api_server.last_request.path == ACCOUNT_TAGS_ITEM

    @pytest.mark.asyncio
    async def test_an_undocumented_404_still_classifies_by_status_async(self, api_server: MockAPIServer) -> None:
        """The async client recovers the status from the same place."""
        api_server.route(
            ACCOUNT_TAGS_ITEM,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such account tag")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await client.account_tags.get(team_id=TEAM_ID, name=TAG_NAME)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
