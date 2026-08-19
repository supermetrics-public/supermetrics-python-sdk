"""End-to-end tests for the Logins error taxonomy.

Every failure here is a real HTTP response with a real status and real headers, driven
through the whole stack over a loopback socket. Error classification, ``Retry-After``
parsing and the recovery of the upstream ``error.code`` from a response body the
generated parser never modelled only exist on the wire, so a mocked transport cannot
observe any of them.

Two properties of this domain make it worth its own module rather than a handful of
cases bolted onto the happy-path tests:

- **``get_accounts`` and ``revoke`` document no 400.** The spec lists 401, 403, 404, 422,
  429 and 500 on both, and a 400 on neither: a rejected request is reported as a 422.
  ``DOCUMENTED_FAILURES`` therefore has no 400 entry, and there is deliberately no test
  asserting ``SupermetricsValidationError`` from a 400 as though it were the contract.
- **``revoke`` succeeds with a 200 carrying a boolean**, so its adapter reads the body
  (``data.result``) rather than the status. A failure that leaked through that branch
  would look like a login that simply was not there — :class:`TestLoginsRevokeErrors`
  pins that a non-2xx raises rather than degrading to ``False``.

The routes are spelled out here rather than in ``conftest.py`` because this module owns
them; the happy-path module scripts the same paths for successful responses.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

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

#: Logins stay on the core API host — ``base_url`` is a bare ``http://127.0.0.1:<port>``
#: and nothing is re-hosted to the Data Warehouse host. A regression that dropped a path
#: segment or re-hosted these calls would fall through to the mock server's default 404
#: rather than reaching the scripted status.
LOGIN_ID = "login_abc123"
LOGINS_COLLECTION = "/ds/logins"
LOGIN_ITEM = f"/ds/login/{LOGIN_ID}"
LOGIN_ACCOUNTS = f"{LOGIN_ITEM}/accounts"


def _error_envelope(code: str, message: str) -> dict[str, Any]:
    """Build the error envelope every 4xx/5xx in this domain carries.

    The upstream ``Error`` schema is exactly ``code``/``message``/``description`` — there
    is no ``details`` object anywhere in it, which is why the exception's ``details`` is
    ``None`` for every status here (see :meth:`TestLoginsErrorTaxonomy.test_error_context_survives_on_a_404`).
    """
    return {
        "meta": {"request_id": "req_00000000"},
        "error": {"code": code, "message": message, "description": f"{code} occurred"},
    }


#: Every failure status the logins spec documents on ``get_accounts`` and ``revoke``, and
#: the class each becomes. There is deliberately no 400 entry — neither method documents
#: one — so a rejected request arrives as a 422 (``SupermetricsValidationError``) instead.
DOCUMENTED_FAILURES: list[tuple[int, str, type[SupermetricsAPIError]]] = [
    (401, "UNAUTHORIZED", SupermetricsAuthError),
    (403, "FORBIDDEN", SupermetricsForbiddenError),
    (404, "NOT_FOUND", SupermetricsNotFoundError),
    (422, "UNPROCESSABLE_ENTITY", SupermetricsValidationError),
    (429, "TOO_MANY_REQUESTS", SupermetricsRateLimitError),
    (500, "INTERNAL_SERVER_ERROR", SupermetricsServerError),
]


class TestLoginsErrorTaxonomy:
    """Status-to-exception mapping across all four read/write methods, sync surface.

    Each method embeds a different verb and a different path, so a classification
    regression confined to one adapter cannot hide behind a green sibling. The upstream
    ``error.code`` is recovered from the raw body even though the generated parser models
    none of these statuses, which is the whole reason to assert on ``error_code`` here.
    """

    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    def test_get_accounts_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Each documented status on the paginated accounts GET raises its own class."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS

    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    def test_revoke_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """Each documented status on the DELETE raises rather than answering a boolean."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.logins.revoke(LOGIN_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        request = api_server.last_request
        assert request.method == "DELETE"
        assert request.path == LOGIN_ITEM

    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    def test_list_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """A failing collection GET raises instead of degrading to an empty list."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.logins.list()

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGINS_COLLECTION

    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    def test_get_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """A failing by-id GET raises rather than returning an empty login."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                client.logins.get(LOGIN_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        request = api_server.last_request
        assert request.method == "GET"
        assert request.path == LOGIN_ITEM

    def test_get_accounts_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After is read off the 429 response rather than guessed."""
        api_server.route(
            LOGIN_ACCOUNTS,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.status_code == 429
        assert exc_info.value.error_code == "TOO_MANY_REQUESTS"
        assert exc_info.value.retry_after == 30
        assert urlsplit(api_server.last_request.path).path == LOGIN_ACCOUNTS

    def test_revoke_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After survives the DELETE error path too, with its value intact."""
        api_server.route(
            LOGIN_ITEM,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                client.logins.revoke(LOGIN_ID)

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30
        assert api_server.last_request.method == "DELETE"

    def test_error_context_survives_on_a_404(self, api_server: MockAPIServer) -> None:
        """A 404 keeps its status, upstream code and human-readable detail on the exception.

        The generated parser *does* model 404 for ``get_accounts``, so the code comes off
        the parsed ``Error`` rather than the raw-body recovery path — either way it must
        reach the caller. The ``description`` text is folded into ``response_body`` so a
        caller still has the occurrence-specific message a 404 exists to carry.

        ``details`` is asserted ``None`` deliberately, not overlooked: the upstream
        ``Error`` schema is ``code``/``message``/``description`` only, with no ``details``
        object, so there is nothing for the SDK to populate. Pinning it here turns a future
        schema change that adds ``details`` into a visible, failing decision.
        """
        api_server.route(
            LOGIN_ACCOUNTS,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such login")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert "no such login" in (exc_info.value.response_body or "")
        assert exc_info.value.details is None
        assert urlsplit(api_server.last_request.path).path == LOGIN_ACCOUNTS

    def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """X-Request-Id and X-Span-Id on the failing response are reachable on the exception."""
        api_server.route(
            LOGIN_ACCOUNTS,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-at-500", "X-Span-Id": "span-at-500"},
            ),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.request_id == "req-at-500"
        assert exc_info.value.span_id == "span-at-500"

    @pytest.mark.parametrize(("status", "code"), [(401, "UNAUTHORIZED"), (500, "INTERNAL_SERVER_ERROR")])
    def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer, status: int, code: str) -> None:
        """No exception stringifies the credential, whoever ends up logging it."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "bad")))

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAPIError) as exc_info:
                client.logins.revoke(LOGIN_ID)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)


class TestLoginsRevokeErrors:
    """revoke() answers a boolean on success, so a failure must not look like ``False``.

    ``revoke`` reads ``data.result`` off a 200 to decide what to return: a 200 carrying
    ``result: false`` is a legitimate "not revoked", not an error. A failing status must
    still raise. Conflating the two would turn a permissions problem or a missing login
    into a quiet "nothing was revoked", which is exactly the bug these tests pin down.
    """

    def test_failure_raises_instead_of_returning_false(self, api_server: MockAPIServer) -> None:
        """The same route serves a false-y 200 and then a 403; only the second raises."""
        api_server.route(
            LOGIN_ITEM,
            ScriptedResponse(status=200, json_body={"meta": {"request_id": "req_00000000"}, "data": {"result": False}}),
            ScriptedResponse(status=403, json_body=_error_envelope("FORBIDDEN", "logins_write required")),
        )

        with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
            # A 200 saying nothing was revoked is a successful call that returns False.
            assert client.logins.revoke(LOGIN_ID) is False

            # A 403 is a failure, and must not be flattened into the same False.
            with pytest.raises(SupermetricsForbiddenError) as exc_info:
                client.logins.revoke(LOGIN_ID)

        assert exc_info.value.status_code == 403
        assert exc_info.value.error_code == "FORBIDDEN"
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == LOGIN_ITEM


class TestLoginsAsyncErrorTaxonomy:
    """The async surface has its own event hooks and its own error paths."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    async def test_get_accounts_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async accounts GET classifies a failing status identically to the sync one."""
        api_server.route(LOGIN_ACCOUNTS, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        request = api_server.last_request
        assert request.method == "GET"
        assert urlsplit(request.path).path == LOGIN_ACCOUNTS

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    async def test_revoke_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """The async DELETE raises rather than answering a boolean on every documented status."""
        api_server.route(LOGIN_ITEM, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.logins.revoke(LOGIN_ID)

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.method == "DELETE"
        assert api_server.last_request.path == LOGIN_ITEM

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("status", "code", "expected"), DOCUMENTED_FAILURES)
    async def test_list_status_maps_to_exception(
        self,
        api_server: MockAPIServer,
        status: int,
        code: str,
        expected: type[SupermetricsAPIError],
    ) -> None:
        """A failing collection GET raises on the async client too."""
        api_server.route(LOGINS_COLLECTION, ScriptedResponse(status=status, json_body=_error_envelope(code, "nope")))

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(expected) as exc_info:
                await client.logins.list()

        assert exc_info.value.status_code == status
        assert exc_info.value.error_code == code
        assert api_server.last_request.path == LOGINS_COLLECTION

    @pytest.mark.asyncio
    async def test_get_accounts_rate_limited_preserves_retry_after(self, api_server: MockAPIServer) -> None:
        """Retry-After survives the async error path with its value intact."""
        api_server.route(
            LOGIN_ACCOUNTS,
            ScriptedResponse(
                status=429,
                json_body=_error_envelope("TOO_MANY_REQUESTS", "slow down"),
                headers={"Retry-After": "30"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsRateLimitError) as exc_info:
                await client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30
        assert urlsplit(api_server.last_request.path).path == LOGIN_ACCOUNTS

    @pytest.mark.asyncio
    async def test_error_context_survives_on_a_404(self, api_server: MockAPIServer) -> None:
        """The async client keeps the same 404 context — code, detail, and a ``None`` details."""
        api_server.route(
            LOGIN_ACCOUNTS,
            ScriptedResponse(status=404, json_body=_error_envelope("NOT_FOUND", "no such login")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsNotFoundError) as exc_info:
                await client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
        assert "no such login" in (exc_info.value.response_body or "")
        assert exc_info.value.details is None

    @pytest.mark.asyncio
    async def test_revoke_failure_raises_instead_of_returning_false(self, api_server: MockAPIServer) -> None:
        """The async revoke has the same body-reading branch, and the same way to get it wrong."""
        api_server.route(
            LOGIN_ITEM,
            ScriptedResponse(status=200, json_body={"meta": {"request_id": "req_00000000"}, "data": {"result": False}}),
            ScriptedResponse(status=403, json_body=_error_envelope("FORBIDDEN", "logins_write required")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            assert await client.logins.revoke(LOGIN_ID) is False

            with pytest.raises(SupermetricsForbiddenError) as exc_info:
                await client.logins.revoke(LOGIN_ID)

        assert exc_info.value.status_code == 403
        assert exc_info.value.error_code == "FORBIDDEN"
        assert api_server.last_request.method == "DELETE"

    @pytest.mark.asyncio
    async def test_error_carries_the_correlation_id(self, api_server: MockAPIServer) -> None:
        """Correlation headers reach the exception on the async path too."""
        api_server.route(
            LOGIN_ACCOUNTS,
            ScriptedResponse(
                status=500,
                json_body=_error_envelope("INTERNAL_SERVER_ERROR", "kaboom"),
                headers={"X-Request-Id": "req-at-async-500", "X-Span-Id": "span-at-async-500"},
            ),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsServerError) as exc_info:
                await client.logins.get_accounts(LOGIN_ID)

        assert exc_info.value.request_id == "req-at-async-500"
        assert exc_info.value.span_id == "span-at-async-500"

    @pytest.mark.asyncio
    async def test_api_key_never_leaks_into_the_message(self, api_server: MockAPIServer) -> None:
        """Credential hygiene holds on the async path."""
        api_server.route(
            LOGIN_ITEM,
            ScriptedResponse(status=401, json_body=_error_envelope("ACCESS_TOKEN_INVALID", "expired")),
        )

        async with SupermetricsAsyncClient(api_key="api_k", base_url=api_server.base_url) as client:
            with pytest.raises(SupermetricsAuthError) as exc_info:
                await client.logins.revoke(LOGIN_ID)

        assert api_server.last_request.bearer_token == "api_k"
        assert "api_k" not in str(exc_info.value)
        assert "api_k" not in repr(exc_info.value)
