"""End-to-end tests for credential mechanisms (Phase 1.1).

Every assertion here is made against the ``Authorization`` header as it actually
arrived at a real HTTP server, so these tests cover the client constructor, the
transport event hooks, and the httpx request pipeline together.
"""

from __future__ import annotations

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import SupermetricsClientError

from .conftest import MockAPIServer

pytestmark = pytest.mark.e2e


class TestStaticCredentials:
    """Static API keys and bearer tokens reach the wire unchanged."""

    def test_api_key_is_sent_as_bearer_token(self, logins_server: MockAPIServer) -> None:
        """An api_key is sent as `Authorization: Bearer <key>`."""
        with SupermetricsClient(api_key="api_live_123", base_url=logins_server.base_url) as client:
            client.logins.list()

        assert logins_server.last_request.authorization == "Bearer api_live_123"

    def test_api_key_accepted_positionally(self, logins_server: MockAPIServer) -> None:
        """The api_key stays positional, so existing call sites keep working."""
        with SupermetricsClient("api_positional", base_url=logins_server.base_url) as client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == "api_positional"

    def test_oauth_bearer_token_is_sent(self, logins_server: MockAPIServer) -> None:
        """An OAuth access token supplied as bearer_token is sent verbatim."""
        with SupermetricsClient(bearer_token="otok_xyz789", base_url=logins_server.base_url) as client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == "otok_xyz789"

    def test_token_already_carrying_the_scheme_is_not_double_prefixed(self, logins_server: MockAPIServer) -> None:
        """A credential passed as "Bearer x" is not turned into "Bearer Bearer x"."""
        with SupermetricsClient(bearer_token="Bearer otok_prefixed", base_url=logins_server.base_url) as client:
            client.logins.list()

        assert logins_server.last_request.authorization == "Bearer otok_prefixed"

    def test_exchanged_delegation_token_is_opaque_to_the_sdk(self, logins_server: MockAPIServer) -> None:
        """RFC 8693 style exchanged tokens are forwarded without inspection."""
        exchanged = "eyJhbGciOiJSUzI1NiJ9.eyJhY3QiOnsic3ViIjoic3ZjLW1jcCJ9fQ.sig"
        with SupermetricsClient(bearer_token=exchanged, base_url=logins_server.base_url) as client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == exchanged


class TestCredentialValidation:
    """Exactly one credential mechanism must be supplied."""

    @pytest.mark.parametrize("client_cls", [SupermetricsClient, SupermetricsAsyncClient])
    def test_no_credentials_raises(self, client_cls: type) -> None:
        """Constructing without any credential is rejected locally."""
        with pytest.raises(SupermetricsClientError, match="No credentials supplied"):
            client_cls()

    @pytest.mark.parametrize("client_cls", [SupermetricsClient, SupermetricsAsyncClient])
    def test_multiple_credentials_raise(self, client_cls: type) -> None:
        """Supplying two competing credentials is rejected locally."""
        with pytest.raises(SupermetricsClientError, match="Multiple credentials supplied"):
            client_cls(api_key="api_1", bearer_token="otok_1")

    @pytest.mark.parametrize("client_cls", [SupermetricsClient, SupermetricsAsyncClient])
    def test_credential_errors_are_also_value_errors(self, client_cls: type) -> None:
        """SupermetricsClientError subclasses ValueError, as the spec requires."""
        with pytest.raises(ValueError):
            client_cls()

    def test_async_provider_rejected_by_sync_client(self) -> None:
        """A coroutine provider cannot be used with the synchronous client."""

        async def provider() -> str:
            return "otok_async"

        with pytest.raises(SupermetricsClientError, match="async token_provider"):
            SupermetricsClient(token_provider=provider)


class TestDynamicTokenProviderSync:
    """The synchronous client re-evaluates its token provider per request."""

    def test_provider_is_called_for_every_request(self, logins_server: MockAPIServer) -> None:
        """Each request carries the token produced for that request."""
        issued: list[str] = []

        def provider() -> str:
            issued.append(f"otok_rotating_{len(issued) + 1}")
            return issued[-1]

        with SupermetricsClient(token_provider=provider, base_url=logins_server.base_url) as client:
            client.logins.list()
            client.logins.list()
            client.logins.list()

        assert [r.bearer_token for r in logins_server.requests] == [
            "otok_rotating_1",
            "otok_rotating_2",
            "otok_rotating_3",
        ]

    def test_refreshed_token_takes_effect_without_a_new_client(self, logins_server: MockAPIServer) -> None:
        """A token refreshed out of band is picked up on the next request."""
        current = {"token": "otok_before_refresh"}

        with SupermetricsClient(token_provider=lambda: current["token"], base_url=logins_server.base_url) as client:
            client.logins.list()
            current["token"] = "otok_after_refresh"
            client.logins.list()

        assert [r.bearer_token for r in logins_server.requests] == ["otok_before_refresh", "otok_after_refresh"]

    def test_provider_returning_a_non_string_is_reported(self, logins_server: MockAPIServer) -> None:
        """A misbehaving provider produces a clear client-side error."""
        with SupermetricsClient(token_provider=lambda: 42, base_url=logins_server.base_url) as client:  # type: ignore[arg-type,return-value]
            with pytest.raises(SupermetricsClientError, match="must return a string"):
                client.logins.list()


class TestDynamicTokenProviderAsync:
    """The asynchronous client supports both coroutine and plain providers."""

    @pytest.mark.asyncio
    async def test_coroutine_provider_is_awaited_per_request(self, logins_server: MockAPIServer) -> None:
        """An `async def` provider is awaited before every request."""
        calls = {"n": 0}

        async def provider() -> str:
            calls["n"] += 1
            return f"otok_async_{calls['n']}"

        async with SupermetricsAsyncClient(token_provider=provider, base_url=logins_server.base_url) as client:
            await client.logins.list()
            await client.logins.list()

        assert [r.bearer_token for r in logins_server.requests] == ["otok_async_1", "otok_async_2"]
        assert calls["n"] == 2

    @pytest.mark.asyncio
    async def test_plain_callable_provider_is_supported(self, logins_server: MockAPIServer) -> None:
        """A synchronous callable is also accepted by the async client."""
        async with SupermetricsAsyncClient(
            token_provider=lambda: "otok_plain", base_url=logins_server.base_url
        ) as client:
            await client.logins.list()

        assert logins_server.last_request.bearer_token == "otok_plain"

    @pytest.mark.asyncio
    async def test_static_credentials_work_on_the_async_client(self, logins_server: MockAPIServer) -> None:
        """api_key and bearer_token behave identically on the async client."""
        async with SupermetricsAsyncClient(api_key="api_async", base_url=logins_server.base_url) as client:
            await client.logins.list()

        assert logins_server.last_request.bearer_token == "api_async"


class TestCredentialOutranksClientHeaders:
    """A client-level Authorization header never silently replaces the credential.

    The event hook rewrites ``Authorization`` for a token provider but has nothing
    to rewrite for a static token. Without an explicit rule, the same
    ``custom_headers`` would therefore send a different credential depending on
    which authentication mechanism the caller chose.
    """

    @pytest.mark.parametrize(
        ("kwargs", "expected"),
        [
            ({"api_key": "from_api_key"}, "from_api_key"),
            ({"bearer_token": "otok_from_bearer"}, "otok_from_bearer"),
        ],
        ids=["api_key", "bearer_token"],
    )
    def test_static_credential_wins_over_custom_headers(
        self, logins_server: MockAPIServer, kwargs: dict[str, str], expected: str
    ) -> None:
        """A static credential is sent even when custom_headers sets Authorization."""
        with pytest.warns(UserWarning, match="custom_headers set 'Authorization'"):
            client = SupermetricsClient(
                base_url=logins_server.base_url,
                custom_headers={"Authorization": "Bearer from_custom_headers"},
                **kwargs,
            )
        with client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == expected

    def test_token_provider_wins_over_custom_headers(self, logins_server: MockAPIServer) -> None:
        """A provider credential behaves identically to a static one."""
        with pytest.warns(UserWarning, match="custom_headers set 'Authorization'"):
            client = SupermetricsClient(
                token_provider=lambda: "otok_from_provider",
                base_url=logins_server.base_url,
                custom_headers={"Authorization": "Bearer from_custom_headers"},
            )
        with client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == "otok_from_provider"

    def test_conflict_is_detected_case_insensitively(self, logins_server: MockAPIServer) -> None:
        """A lower-cased Authorization key is caught too, and leaves no stray header."""
        with pytest.warns(UserWarning, match="custom_headers set 'Authorization'"):
            client = SupermetricsClient(
                api_key="from_api_key",
                base_url=logins_server.base_url,
                custom_headers={"authorization": "Bearer from_custom_headers"},
            )
        with client:
            client.logins.list()

        assert logins_server.last_request.bearer_token == "from_api_key"

    def test_unrelated_custom_headers_are_untouched_and_silent(self, logins_server: MockAPIServer) -> None:
        """Custom headers that do not clash with the credential warn nothing."""
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with SupermetricsClient(
                api_key="from_api_key",
                base_url=logins_server.base_url,
                custom_headers={"X-Team-ID": "9001"},
            ) as client:
                client.logins.list()

        assert logins_server.last_request.headers["x-team-id"] == "9001"
        assert logins_server.last_request.bearer_token == "from_api_key"

    @pytest.mark.asyncio
    async def test_async_client_applies_the_same_rule(self, logins_server: MockAPIServer) -> None:
        """The async client resolves the conflict identically."""
        with pytest.warns(UserWarning, match="custom_headers set 'Authorization'"):
            client = SupermetricsAsyncClient(
                api_key="from_api_key",
                base_url=logins_server.base_url,
                custom_headers={"Authorization": "Bearer from_custom_headers"},
            )
        async with client:
            await client.logins.list()

        assert logins_server.last_request.bearer_token == "from_api_key"

    def test_per_request_headers_remain_the_escape_hatch(self, logins_server: MockAPIServer) -> None:
        """Sending a different credential for one call still works, without a warning."""
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with SupermetricsClient(api_key="from_api_key", base_url=logins_server.base_url) as client:
                client.logins.list(headers={"Authorization": "Bearer per_request_override"})

        assert logins_server.last_request.bearer_token == "per_request_override"


class TestBlankCredentialsAreRejected:
    """A blank credential must fail locally, not as an opaque server error.

    Sending a bare ``Authorization: Bearer`` produces a rejection from the API that
    looks like a server problem rather than the caller's mistake, so the SDK
    catches it first.
    """

    @pytest.mark.parametrize("blank", ["", "   ", "\t\n"], ids=["empty", "spaces", "whitespace"])
    def test_blank_per_request_auth_token_is_rejected(self, logins_server: MockAPIServer, blank: str) -> None:
        """A blank auth_token override raises before any request is made."""
        with SupermetricsClient(api_key="api_ok", base_url=logins_server.base_url) as client:
            with pytest.raises(SupermetricsClientError, match="auth_token must be a non-empty string"):
                client.logins.list(auth_token=blank)

        assert logins_server.requests == []

    def test_provider_returning_a_blank_token_is_rejected(self, logins_server: MockAPIServer) -> None:
        """A provider that hands back an empty string is reported as a client error."""
        with SupermetricsClient(token_provider=lambda: "", base_url=logins_server.base_url) as client:
            with pytest.raises(SupermetricsClientError, match="token_provider must be a non-empty string"):
                client.logins.list()

    @pytest.mark.parametrize("blank", ["", "   "], ids=["empty", "spaces"])
    def test_blank_constructor_credentials_are_rejected(self, blank: str) -> None:
        """A blank api_key or bearer_token is rejected at construction time."""
        with pytest.raises(SupermetricsClientError, match="api_key must be a non-empty string"):
            SupermetricsClient(api_key=blank)
        with pytest.raises(SupermetricsClientError, match="bearer_token must be a non-empty string"):
            SupermetricsClient(bearer_token=blank)

    @pytest.mark.asyncio
    async def test_blank_token_is_rejected_on_the_async_client(self, logins_server: MockAPIServer) -> None:
        """The async client applies the same rule."""
        async with SupermetricsAsyncClient(api_key="api_ok", base_url=logins_server.base_url) as client:
            with pytest.raises(SupermetricsClientError, match="auth_token must be a non-empty string"):
                await client.logins.list(auth_token="  ")

        assert logins_server.requests == []
