"""Unit tests for authentication configuration and credential resolution."""

import dataclasses
import gc
import warnings
from collections.abc import Generator
from functools import partial

import pytest

from supermetrics._auth import (
    DEFAULT_AUTH_SCHEME,
    AuthConfig,
    format_authorization,
    resolve_auth_config,
)
from supermetrics.exceptions import SupermetricsClientError

#: Shared tail of the "wrong number of credentials" errors. The distinguishing part of each
#: message (which fields were seen, and in which order) is spelled out literally per test.
CREDENTIAL_CHOICE_HINT = "Provide exactly one of: api_key, bearer_token, or token_provider."

ASYNC_PROVIDER_ON_SYNC_CLIENT_MESSAGE = (
    "An async token_provider cannot be used with SupermetricsClient. "
    "Use SupermetricsAsyncClient, or supply a synchronous callable."
)

AWAITABLE_ON_SYNC_CLIENT_MESSAGE = (
    "token_provider returned an awaitable on a synchronous client. "
    "Use SupermetricsAsyncClient for async token providers."
)


class ImmediateAwaitable:
    """An awaitable that is not a coroutine and resolves immediately to a fixed value."""

    def __init__(self, value: object) -> None:
        self.value = value

    def __await__(self) -> Generator[None, None, object]:
        yield from ()
        return self.value


class AsyncCallableProvider:
    """A callable object whose ``__call__`` is a coroutine function."""

    async def __call__(self) -> str:
        return "otok_123"


class ProviderBoom(RuntimeError):
    """Raised by test providers to check that failures reach the caller unchanged."""


class TestFormatAuthorization:
    """Test suite for format_authorization."""

    def test_plain_token_gets_default_scheme(self) -> None:
        """Test that a bare token is prefixed with the default Bearer scheme."""
        assert format_authorization("otok_123") == "Bearer otok_123"

    def test_default_scheme_constant_is_bearer(self) -> None:
        """Test that the default scheme matches the exported DEFAULT_AUTH_SCHEME constant."""
        assert DEFAULT_AUTH_SCHEME == "Bearer"
        assert format_authorization("otok_123") == format_authorization("otok_123", DEFAULT_AUTH_SCHEME)

    def test_already_prefixed_token_is_unchanged(self) -> None:
        """Test that a token already carrying the scheme prefix is not prefixed twice."""
        assert format_authorization("Bearer otok_123") == "Bearer otok_123"

    def test_lowercase_prefix_is_detected_and_preserved(self) -> None:
        """Test that a lowercase scheme prefix is recognised and left verbatim."""
        assert format_authorization("bearer otok_123") == "bearer otok_123"

    def test_uppercase_prefix_is_detected_and_preserved(self) -> None:
        """Test that an uppercase scheme prefix is recognised and left verbatim."""
        assert format_authorization("BEARER otok_123") == "BEARER otok_123"

    def test_mixed_case_prefix_is_detected_and_preserved(self) -> None:
        """Test that a mixed-case scheme prefix is recognised and left verbatim."""
        assert format_authorization("BeArEr otok_123") == "BeArEr otok_123"

    def test_surrounding_whitespace_is_stripped(self) -> None:
        """Test that leading and trailing whitespace around a bare token is removed."""
        assert format_authorization("  \totok_123\n ") == "Bearer otok_123"

    def test_surrounding_whitespace_is_stripped_from_prefixed_token(self) -> None:
        """Test that whitespace around an already-prefixed token is removed."""
        assert format_authorization("\t Bearer otok_123  ") == "Bearer otok_123"

    def test_whitespace_inside_prefixed_token_is_preserved(self) -> None:
        """Test that whitespace between the scheme and the token is left untouched."""
        assert format_authorization("Bearer  otok_123") == "Bearer  otok_123"

    def test_custom_scheme_is_used_as_prefix(self) -> None:
        """Test that a custom scheme replaces Bearer when prefixing a bare token."""
        assert format_authorization("otok_123", "Token") == "Token otok_123"

    def test_custom_scheme_prefix_is_detected_case_insensitively(self) -> None:
        """Test that an existing custom-scheme prefix is not duplicated."""
        assert format_authorization("token otok_123", "Token") == "token otok_123"

    def test_foreign_scheme_prefix_is_not_treated_as_present(self) -> None:
        """Test that a prefix from a different scheme is treated as part of the token."""
        assert format_authorization("Bearer otok_123", "Token") == "Token Bearer otok_123"

    def test_scheme_without_trailing_space_is_not_a_prefix_match(self) -> None:
        """Test that a token merely starting with the scheme letters is still prefixed."""
        assert format_authorization("Bearertoken") == "Bearer Bearertoken"

    def test_scheme_word_alone_is_prefixed(self) -> None:
        """Test that a token equal to the scheme word is prefixed rather than passed through."""
        assert format_authorization("Bearer") == "Bearer Bearer"

    def test_custom_scheme_casing_is_preserved_in_output(self) -> None:
        """Test that the caller's scheme casing is emitted verbatim, not normalised."""
        assert format_authorization("otok_123", "TOKEN") == "TOKEN otok_123"

    def test_empty_token_yields_scheme_only(self) -> None:
        """Test that an empty token produces a header value with just the scheme."""
        assert format_authorization("") == "Bearer "

    def test_whitespace_only_token_yields_scheme_only(self) -> None:
        """Test that a whitespace-only token collapses to the same value as an empty one."""
        assert format_authorization("  \t\n ") == "Bearer "


class TestResolveAuthConfigAccepted:
    """Test suite for resolve_auth_config with a single valid credential."""

    def test_api_key_is_accepted(self) -> None:
        """Test that an api_key alone produces a static configuration."""
        config = resolve_auth_config("api_123", None, None, allow_async_provider=False)

        assert config.static_token == "api_123"
        assert config.token_provider is None
        assert config.is_dynamic is False
        assert config.scheme == DEFAULT_AUTH_SCHEME
        assert config.static_authorization() == "Bearer api_123"

    def test_bearer_token_is_accepted(self) -> None:
        """Test that a bearer_token alone produces a static configuration."""
        config = resolve_auth_config(None, "otok_123", None, allow_async_provider=False)

        assert config.static_token == "otok_123"
        assert config.token_provider is None
        assert config.is_dynamic is False
        assert config.static_authorization() == "Bearer otok_123"

    def test_static_token_is_stored_verbatim_but_header_is_stripped(self) -> None:
        """Test that padding around a static credential survives on the config but not the header."""
        config = resolve_auth_config("  api_123  ", None, None, allow_async_provider=False)

        assert config.static_token == "  api_123  "
        assert config.static_authorization() == "Bearer api_123"

    def test_sync_token_provider_is_accepted_by_sync_client(self) -> None:
        """Test that a synchronous provider is accepted when async providers are disallowed."""

        def provider() -> str:
            return "otok_123"

        config = resolve_auth_config(None, None, provider, allow_async_provider=False)

        assert config.token_provider is provider
        assert config.static_token is None
        assert config.is_dynamic is True
        assert config.scheme == DEFAULT_AUTH_SCHEME
        assert config.static_authorization() is None

    def test_sync_token_provider_is_accepted_by_async_client(self) -> None:
        """Test that a synchronous provider is also accepted when async providers are allowed."""

        def provider() -> str:
            return "otok_123"

        config = resolve_auth_config(None, None, provider, allow_async_provider=True)

        assert config.token_provider is provider
        assert config.is_dynamic is True
        assert config.static_token is None
        assert config.scheme == DEFAULT_AUTH_SCHEME
        assert config.static_authorization() is None

    def test_async_token_provider_is_accepted_when_allowed(self) -> None:
        """Test that an async def provider is accepted when allow_async_provider is True."""

        async def provider() -> str:
            return "otok_123"

        config = resolve_auth_config(None, None, provider, allow_async_provider=True)

        assert config.token_provider is provider
        assert config.is_dynamic is True
        assert config.static_token is None
        assert config.scheme == DEFAULT_AUTH_SCHEME
        assert config.static_authorization() is None

    def test_callable_object_provider_is_accepted(self) -> None:
        """Test that any callable, not just a function, may be used as a provider."""

        class Provider:
            def __call__(self) -> str:
                return "otok_123"

        provider = Provider()
        config = resolve_auth_config(None, None, provider, allow_async_provider=False)

        assert config.token_provider is provider
        assert config.is_dynamic is True
        assert config.static_token is None

    @pytest.mark.parametrize("allow_async_provider", [False, True])
    def test_token_provider_is_not_invoked_while_resolving_config(self, allow_async_provider: bool) -> None:
        """Test that validation only inspects the provider; it must be called per request, not up front."""
        calls: list[None] = []

        def provider() -> str:
            calls.append(None)
            return "otok_123"

        config = resolve_auth_config(None, None, provider, allow_async_provider=allow_async_provider)

        assert calls == []
        assert config.resolve_sync() == "otok_123"
        assert calls == [None]

    def test_async_callable_object_is_rejected_by_the_sync_client(self) -> None:
        """Test that an object with an ``async def __call__`` is rejected up front.

        ``inspect.iscoroutinefunction`` is False for the instance itself, so the guard
        also probes ``__call__``. Without that, the mistake would only surface on the
        first request instead of at construction time.
        """
        provider = AsyncCallableProvider()

        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, None, provider, allow_async_provider=False)

        assert str(excinfo.value) == ASYNC_PROVIDER_ON_SYNC_CLIENT_MESSAGE

    def test_async_callable_object_is_accepted_by_the_async_client(self) -> None:
        """Test that the async client still accepts an object with an ``async def __call__``."""
        provider = AsyncCallableProvider()

        config = resolve_auth_config(None, None, provider, allow_async_provider=True)

        assert config.token_provider is provider


class TestResolveAuthConfigRejected:
    """Test suite for resolve_auth_config validation failures."""

    def test_no_credentials_is_rejected(self) -> None:
        """Test that supplying no credential at all raises an error naming the alternatives."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, None, None, allow_async_provider=False)

        assert str(excinfo.value) == f"No credentials supplied. {CREDENTIAL_CHOICE_HINT}"

    def test_api_key_and_bearer_token_together_are_rejected(self) -> None:
        """Test that api_key plus bearer_token raises an error naming both fields."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config("api_123", "otok_123", None, allow_async_provider=False)

        assert str(excinfo.value) == f"Multiple credentials supplied (api_key, bearer_token). {CREDENTIAL_CHOICE_HINT}"

    def test_api_key_and_token_provider_together_are_rejected(self) -> None:
        """Test that api_key plus token_provider raises an error naming both fields."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config("api_123", None, lambda: "otok_123", allow_async_provider=False)

        assert (
            str(excinfo.value) == f"Multiple credentials supplied (api_key, token_provider). {CREDENTIAL_CHOICE_HINT}"
        )

    def test_bearer_token_and_token_provider_together_are_rejected(self) -> None:
        """Test that bearer_token plus token_provider raises an error naming both fields."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, "otok_123", lambda: "otok_123", allow_async_provider=False)

        assert (
            str(excinfo.value)
            == f"Multiple credentials supplied (bearer_token, token_provider). {CREDENTIAL_CHOICE_HINT}"
        )

    def test_all_three_credentials_together_are_rejected(self) -> None:
        """Test that supplying all three mechanisms raises an error naming all of them."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config("api_123", "otok_123", lambda: "otok_123", allow_async_provider=True)

        assert (
            str(excinfo.value)
            == f"Multiple credentials supplied (api_key, bearer_token, token_provider). {CREDENTIAL_CHOICE_HINT}"
        )

    def test_empty_second_credential_still_counts_as_supplied(self) -> None:
        """Test that an empty-string credential alongside another one is a conflict, not an empty value."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config("api_123", "", None, allow_async_provider=False)

        assert str(excinfo.value) == f"Multiple credentials supplied (api_key, bearer_token). {CREDENTIAL_CHOICE_HINT}"

    def test_empty_api_key_is_rejected(self) -> None:
        """Test that an empty api_key raises an error naming the api_key field."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config("", None, None, allow_async_provider=False)

        assert str(excinfo.value) == "api_key must be a non-empty string."

    def test_whitespace_only_api_key_is_rejected(self) -> None:
        """Test that a whitespace-only api_key raises an error naming the api_key field."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config("   \t\n", None, None, allow_async_provider=False)

        assert str(excinfo.value) == "api_key must be a non-empty string."

    def test_empty_bearer_token_is_rejected(self) -> None:
        """Test that an empty bearer_token raises an error naming the bearer_token field."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, "", None, allow_async_provider=False)

        assert str(excinfo.value) == "bearer_token must be a non-empty string."

    def test_whitespace_only_bearer_token_is_rejected(self) -> None:
        """Test that a whitespace-only bearer_token raises an error naming the bearer_token field."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, "  ", None, allow_async_provider=False)

        assert str(excinfo.value) == "bearer_token must be a non-empty string."

    def test_non_callable_token_provider_is_rejected(self) -> None:
        """Test that a non-callable token_provider raises an error."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, None, "otok_123", allow_async_provider=False)

        assert str(excinfo.value) == "token_provider must be callable."

    def test_non_callable_token_provider_is_rejected_on_async_client(self) -> None:
        """Test that the non-callable check also applies when async providers are allowed."""
        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, None, object(), allow_async_provider=True)

        assert str(excinfo.value) == "token_provider must be callable."

    def test_async_token_provider_is_rejected_when_not_allowed(self) -> None:
        """Test that an async def provider is refused up front by the synchronous client."""

        async def provider() -> str:
            return "otok_123"

        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, None, provider, allow_async_provider=False)

        assert str(excinfo.value) == ASYNC_PROVIDER_ON_SYNC_CLIENT_MESSAGE

    def test_partially_applied_async_provider_is_rejected_when_not_allowed(self) -> None:
        """Test that an async provider wrapped in functools.partial is still refused."""

        async def provider(prefix: str) -> str:
            return f"{prefix}_123"

        with pytest.raises(SupermetricsClientError) as excinfo:
            resolve_auth_config(None, None, partial(provider, "otok"), allow_async_provider=False)

        assert str(excinfo.value) == ASYNC_PROVIDER_ON_SYNC_CLIENT_MESSAGE


async def _async_provider() -> str:
    """An async provider used to exercise the sync-client rejection path."""
    return "otok_123"


@pytest.mark.parametrize(
    ("api_key", "bearer_token", "token_provider"),
    [
        pytest.param(None, None, None, id="no-credentials"),
        pytest.param("api_123", "otok_123", None, id="multiple-credentials"),
        pytest.param("", None, None, id="empty-api-key"),
        pytest.param(None, "   ", None, id="whitespace-bearer-token"),
        pytest.param(None, None, "not-callable", id="non-callable-provider"),
        pytest.param(None, None, _async_provider, id="async-provider-on-sync-client"),
    ],
)
def test_every_resolve_auth_config_error_is_also_a_value_error(
    api_key: str | None, bearer_token: str | None, token_provider: object
) -> None:
    """Test that every validation failure can be caught as a plain ValueError."""
    with pytest.raises(ValueError) as excinfo:
        resolve_auth_config(api_key, bearer_token, token_provider, allow_async_provider=False)  # type: ignore[arg-type]

    assert isinstance(excinfo.value, SupermetricsClientError)
    assert str(excinfo.value) != ""


class TestAuthConfig:
    """Test suite for the AuthConfig container itself."""

    def test_default_config_has_no_credential(self) -> None:
        """Test that a bare AuthConfig reports no static token and no provider."""
        config = AuthConfig()

        assert config.static_token is None
        assert config.token_provider is None
        assert config.is_dynamic is False
        assert config.scheme == DEFAULT_AUTH_SCHEME
        assert config.static_authorization() is None

    def test_static_config_is_not_dynamic(self) -> None:
        """Test that a config built from a static token is not dynamic."""
        config = AuthConfig(static_token="otok_123")

        assert config.is_dynamic is False
        assert config.static_authorization() == "Bearer otok_123"

    def test_static_authorization_does_not_double_prefix(self) -> None:
        """Test that a static token that already carries the scheme is not prefixed again."""
        config = AuthConfig(static_token="Bearer otok_123")

        assert config.static_authorization() == "Bearer otok_123"

    def test_static_authorization_honours_custom_scheme(self) -> None:
        """Test that a non-default scheme is used when formatting the static header."""
        config = AuthConfig(static_token="otok_123", scheme="Token")

        assert config.static_authorization() == "Token otok_123"

    def test_provider_config_is_dynamic_and_has_no_static_header(self) -> None:
        """Test that a provider-backed config is dynamic and exposes no static header value."""
        config = AuthConfig(token_provider=lambda: "otok_123")

        assert config.is_dynamic is True
        assert config.static_authorization() is None

    def test_config_is_immutable(self) -> None:
        """Test that AuthConfig instances cannot be mutated after creation."""
        config = AuthConfig(static_token="otok_123")

        with pytest.raises(dataclasses.FrozenInstanceError):
            config.static_token = "otok_456"


class TestAuthConfigResolveSync:
    """Test suite for AuthConfig.resolve_sync."""

    def test_returns_none_without_provider(self) -> None:
        """Test that resolve_sync returns None when only a static credential is configured."""
        assert AuthConfig(static_token="otok_123").resolve_sync() is None

    def test_returns_provider_token_unformatted(self) -> None:
        """Test that resolve_sync returns the raw provider token without a scheme prefix."""
        config = AuthConfig(token_provider=lambda: "otok_123")

        assert config.resolve_sync() == "otok_123"

    def test_provider_is_invoked_on_every_call(self) -> None:
        """Test that the provider result is not cached between resolve_sync calls."""
        calls: list[int] = []

        def provider() -> str:
            calls.append(len(calls))
            return f"otok_{len(calls)}"

        config = AuthConfig(token_provider=provider)

        assert config.resolve_sync() == "otok_1"
        assert config.resolve_sync() == "otok_2"
        assert len(calls) == 2

    def test_provider_token_is_returned_without_stripping(self) -> None:
        """Test that resolve_sync hands back the provider's exact string, leaving formatting to the caller."""
        config = AuthConfig(token_provider=lambda: "  otok_123\n")

        assert config.resolve_sync() == "  otok_123\n"

    def test_empty_provider_token_is_returned_as_is(self) -> None:
        """Test that resolve_sync does not reject an empty string from the provider.

        This documents current behaviour: unlike a static ``api_key=""``, an empty token
        from a provider is accepted and would produce a bare ``Authorization: Bearer``.
        """
        config = AuthConfig(token_provider=lambda: "")

        assert config.resolve_sync() == ""

    def test_provider_exception_propagates_unchanged(self) -> None:
        """Test that a failing provider surfaces its own error rather than being swallowed."""

        def provider() -> str:
            raise ProviderBoom("token endpoint unreachable")

        config = AuthConfig(token_provider=provider)

        with pytest.raises(ProviderBoom, match="token endpoint unreachable"):
            config.resolve_sync()

    def test_non_string_provider_result_is_rejected(self) -> None:
        """Test that an integer returned by the provider raises a client error naming the type."""
        config = AuthConfig(token_provider=lambda: 42)

        with pytest.raises(SupermetricsClientError) as excinfo:
            config.resolve_sync()

        assert str(excinfo.value) == "token_provider must return a string, got int."

    def test_none_provider_result_is_rejected(self) -> None:
        """Test that a provider returning None raises a client error naming NoneType."""
        config = AuthConfig(token_provider=lambda: None)

        with pytest.raises(SupermetricsClientError) as excinfo:
            config.resolve_sync()

        assert str(excinfo.value) == "token_provider must return a string, got NoneType."

    def test_bytes_provider_result_is_rejected(self) -> None:
        """Test that a bytes token is rejected rather than silently decoded."""
        config = AuthConfig(token_provider=lambda: b"otok_123")

        with pytest.raises(SupermetricsClientError) as excinfo:
            config.resolve_sync()

        assert str(excinfo.value) == "token_provider must return a string, got bytes."

    def test_non_string_error_is_also_a_value_error(self) -> None:
        """Test that the provider return-type error can be caught as a ValueError."""
        config = AuthConfig(token_provider=lambda: 42)

        with pytest.raises(ValueError) as excinfo:
            config.resolve_sync()

        assert isinstance(excinfo.value, SupermetricsClientError)

    def test_coroutine_provider_is_rejected_with_actionable_message(self) -> None:
        """Test that an async provider reaching resolve_sync raises a message pointing at the async client."""

        async def provider() -> str:
            return "otok_123"

        config = AuthConfig(token_provider=provider)

        with pytest.raises(SupermetricsClientError) as excinfo:
            config.resolve_sync()

        assert str(excinfo.value) == AWAITABLE_ON_SYNC_CLIENT_MESSAGE

    def test_coroutine_provider_does_not_emit_never_awaited_warning(self) -> None:
        """Test that rejecting a coroutine provider closes it instead of leaking a RuntimeWarning."""

        async def provider() -> str:
            return "otok_123"

        config = AuthConfig(token_provider=provider)
        raised = False

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                config.resolve_sync()
            except SupermetricsClientError:
                raised = True
            gc.collect()

        assert raised is True
        assert [str(w.message) for w in caught if "never awaited" in str(w.message)] == []

    def test_non_coroutine_awaitable_provider_is_rejected(self) -> None:
        """Test that any awaitable, not just a coroutine, is refused on the synchronous path."""
        config = AuthConfig(token_provider=lambda: ImmediateAwaitable("otok_123"))

        with pytest.raises(SupermetricsClientError) as excinfo:
            config.resolve_sync()

        assert str(excinfo.value) == AWAITABLE_ON_SYNC_CLIENT_MESSAGE


class TestAuthConfigResolveAsync:
    """Test suite for AuthConfig.resolve_async."""

    @pytest.mark.asyncio
    async def test_returns_none_without_provider(self) -> None:
        """Test that resolve_async returns None when only a static credential is configured."""
        assert await AuthConfig(static_token="otok_123").resolve_async() is None

    @pytest.mark.asyncio
    async def test_awaits_coroutine_provider(self) -> None:
        """Test that an async def provider is awaited and its token returned."""

        async def provider() -> str:
            return "otok_123"

        config = AuthConfig(token_provider=provider)

        assert await config.resolve_async() == "otok_123"

    @pytest.mark.asyncio
    async def test_accepts_plain_callable_provider(self) -> None:
        """Test that a synchronous provider works unchanged on the async path."""
        config = AuthConfig(token_provider=lambda: "otok_123")

        assert await config.resolve_async() == "otok_123"

    @pytest.mark.asyncio
    async def test_awaits_non_coroutine_awaitable(self) -> None:
        """Test that a provider returning a custom awaitable is awaited as well."""
        config = AuthConfig(token_provider=lambda: ImmediateAwaitable("otok_123"))

        assert await config.resolve_async() == "otok_123"

    @pytest.mark.asyncio
    async def test_provider_is_invoked_on_every_call(self) -> None:
        """Test that the provider result is not cached between resolve_async calls."""
        calls: list[int] = []

        async def provider() -> str:
            calls.append(len(calls))
            return f"otok_{len(calls)}"

        config = AuthConfig(token_provider=provider)

        assert await config.resolve_async() == "otok_1"
        assert await config.resolve_async() == "otok_2"
        assert len(calls) == 2

    @pytest.mark.asyncio
    async def test_non_string_result_from_sync_provider_is_rejected(self) -> None:
        """Test that a synchronous provider returning a non-string is rejected on the async path."""
        config = AuthConfig(token_provider=lambda: 42)

        with pytest.raises(SupermetricsClientError) as excinfo:
            await config.resolve_async()

        assert str(excinfo.value) == "token_provider must return a string, got int."

    @pytest.mark.asyncio
    async def test_non_string_awaited_result_is_rejected(self) -> None:
        """Test that the awaited value is type-checked, not just the immediate return value."""

        async def provider() -> int:
            return 42

        config = AuthConfig(token_provider=provider)

        with pytest.raises(SupermetricsClientError) as excinfo:
            await config.resolve_async()

        assert str(excinfo.value) == "token_provider must return a string, got int."

    @pytest.mark.asyncio
    async def test_awaited_none_result_is_rejected(self) -> None:
        """Test that a coroutine provider resolving to None raises a client error naming NoneType."""

        async def provider() -> None:
            return None

        config = AuthConfig(token_provider=provider)

        with pytest.raises(SupermetricsClientError) as excinfo:
            await config.resolve_async()

        assert str(excinfo.value) == "token_provider must return a string, got NoneType."

    @pytest.mark.asyncio
    async def test_awaited_token_is_returned_without_stripping(self) -> None:
        """Test that resolve_async hands back the awaited string verbatim, without formatting it."""

        async def provider() -> str:
            return "  otok_123\n"

        config = AuthConfig(token_provider=provider)

        assert await config.resolve_async() == "  otok_123\n"

    @pytest.mark.asyncio
    async def test_empty_awaited_token_is_returned_as_is(self) -> None:
        """Test that resolve_async does not reject an empty string from the provider.

        As on the synchronous path, this documents current behaviour rather than
        endorsing it: an empty token yields a bare ``Authorization: Bearer`` header.
        """

        async def provider() -> str:
            return ""

        config = AuthConfig(token_provider=provider)

        assert await config.resolve_async() == ""

    @pytest.mark.asyncio
    async def test_sync_provider_exception_propagates_unchanged(self) -> None:
        """Test that an error raised while calling the provider is not swallowed."""

        def provider() -> str:
            raise ProviderBoom("token endpoint unreachable")

        config = AuthConfig(token_provider=provider)

        with pytest.raises(ProviderBoom, match="token endpoint unreachable"):
            await config.resolve_async()

    @pytest.mark.asyncio
    async def test_awaited_exception_propagates_unchanged(self) -> None:
        """Test that an error raised inside the awaited coroutine reaches the caller."""

        async def provider() -> str:
            raise ProviderBoom("token refresh rejected")

        config = AuthConfig(token_provider=provider)

        with pytest.raises(ProviderBoom, match="token refresh rejected"):
            await config.resolve_async()
