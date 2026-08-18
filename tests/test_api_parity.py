"""Reflection tests enforcing strict parity between the sync and async clients.

Spec 1.4 requires that every resource, method, parameter name, type annotation,
and default value is identical across ``SupermetricsClient`` and
``SupermetricsAsyncClient``. These tests fail in CI the moment the two drift, so
parity is maintained by the build rather than by review discipline.
"""

from __future__ import annotations

import inspect
import typing
from typing import Any

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient

#: Per-request override parameters every public resource method must accept.
REQUIRED_OVERRIDES = {"auth_token", "headers", "timeout"}


@pytest.fixture(scope="module")
def sync_client() -> SupermetricsClient:
    """A synchronous client; no requests are made, only introspection."""
    return SupermetricsClient(api_key="parity-test-key")


@pytest.fixture(scope="module")
def async_client() -> SupermetricsAsyncClient:
    """An asynchronous client; no requests are made, only introspection."""
    return SupermetricsAsyncClient(api_key="parity-test-key")


def _resource_names(client: object) -> set[str]:
    """Return the public resource attribute names attached to a client."""
    return {
        name
        for name, value in vars(client).items()
        if not name.startswith("_") and type(value).__name__.endswith(("Resource", "AsyncResource"))
    }


def _public_methods(resource: object) -> dict[str, Any]:
    """Return the public methods declared on a resource's class."""
    return {
        name: member for name, member in vars(type(resource)).items() if not name.startswith("_") and callable(member)
    }


def _signature_shape(func: Any) -> list[tuple[str, str, str, str]]:
    """Reduce a signature to a comparable (name, kind, annotation, default) list."""
    signature = inspect.signature(func)
    return [
        (
            name,
            str(parameter.kind),
            "" if parameter.annotation is inspect.Parameter.empty else str(parameter.annotation),
            "" if parameter.default is inspect.Parameter.empty else repr(parameter.default),
        )
        for name, parameter in signature.parameters.items()
    ]


class TestResourceParity:
    """The two clients expose the same resources."""

    def test_same_resource_names(self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient) -> None:
        """Neither client has a resource the other lacks."""
        assert _resource_names(sync_client) == _resource_names(async_client)

    def test_resource_set_is_not_empty(self, sync_client: SupermetricsClient) -> None:
        """Guard against the reflection helper silently matching nothing."""
        assert len(_resource_names(sync_client)) >= 9

    def test_sync_and_async_classes_are_distinct(
        self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient
    ) -> None:
        """Each resource has its own sync and async implementation class."""
        for name in _resource_names(sync_client):
            sync_type = type(getattr(sync_client, name))
            async_type = type(getattr(async_client, name))
            assert sync_type is not async_type
            assert async_type.__name__ == sync_type.__name__.replace("Resource", "AsyncResource")


class TestMethodParity:
    """Every method matches one-for-one across the two clients."""

    def test_same_method_names(self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient) -> None:
        """No resource gained or lost a method on one side only."""
        for name in sorted(_resource_names(sync_client)):
            sync_methods = set(_public_methods(getattr(sync_client, name)))
            async_methods = set(_public_methods(getattr(async_client, name)))
            assert sync_methods == async_methods, f"method drift on {name}"

    def test_identical_signatures(self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient) -> None:
        """Parameter names, kinds, annotations, and defaults all match."""
        for name in sorted(_resource_names(sync_client)):
            sync_methods = _public_methods(getattr(sync_client, name))
            async_methods = _public_methods(getattr(async_client, name))
            for method_name, sync_method in sorted(sync_methods.items()):
                assert _signature_shape(sync_method) == _signature_shape(async_methods[method_name]), (
                    f"signature drift on {name}.{method_name}"
                )

    def test_identical_return_annotations(
        self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient
    ) -> None:
        """Both sides return the same models; only the awaitability differs."""
        for name in sorted(_resource_names(sync_client)):
            sync_methods = _public_methods(getattr(sync_client, name))
            async_methods = _public_methods(getattr(async_client, name))
            for method_name, sync_method in sorted(sync_methods.items()):
                sync_return = inspect.signature(sync_method).return_annotation
                async_return = inspect.signature(async_methods[method_name]).return_annotation
                assert str(sync_return) == str(async_return), f"return type drift on {name}.{method_name}"

    def test_async_methods_are_coroutines(self, async_client: SupermetricsAsyncClient) -> None:
        """Every async resource method is actually awaitable."""
        for name in sorted(_resource_names(async_client)):
            for method_name, method in sorted(_public_methods(getattr(async_client, name)).items()):
                assert inspect.iscoroutinefunction(method), f"{name}.{method_name} is not a coroutine function"

    def test_sync_methods_are_not_coroutines(self, sync_client: SupermetricsClient) -> None:
        """No sync resource method leaked an `async def`."""
        for name in sorted(_resource_names(sync_client)):
            for method_name, method in sorted(_public_methods(getattr(sync_client, name)).items()):
                assert not inspect.iscoroutinefunction(method), f"{name}.{method_name} is a coroutine function"


class TestPerRequestOverrideParity:
    """Spec 1.2: every method accepts the standard override parameters."""

    @pytest.mark.parametrize("client_name", ["sync_client", "async_client"])
    def test_all_methods_accept_the_overrides(self, client_name: str, request: pytest.FixtureRequest) -> None:
        """No public resource method is missing auth_token, headers, or timeout."""
        client = request.getfixturevalue(client_name)
        for name in sorted(_resource_names(client)):
            for method_name, method in sorted(_public_methods(getattr(client, name)).items()):
                parameters = inspect.signature(method).parameters
                missing = REQUIRED_OVERRIDES - set(parameters)
                assert not missing, f"{name}.{method_name} is missing {sorted(missing)}"

    @pytest.mark.parametrize("client_name", ["sync_client", "async_client"])
    def test_overrides_are_keyword_only_and_optional(self, client_name: str, request: pytest.FixtureRequest) -> None:
        """The overrides never change positional call sites and always default to None."""
        client = request.getfixturevalue(client_name)
        for name in sorted(_resource_names(client)):
            for method_name, method in sorted(_public_methods(getattr(client, name)).items()):
                parameters = inspect.signature(method).parameters
                for override in sorted(REQUIRED_OVERRIDES):
                    parameter = parameters[override]
                    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY, f"{name}.{method_name}.{override}"
                    assert parameter.default is None, f"{name}.{method_name}.{override}"

    @pytest.mark.parametrize("client_name", ["sync_client", "async_client"])
    def test_override_annotations_are_consistent(self, client_name: str, request: pytest.FixtureRequest) -> None:
        """Every method annotates the overrides identically."""
        client = request.getfixturevalue(client_name)
        expected = {
            "auth_token": "str | None",
            "headers": "dict[str, str] | None",
            "timeout": "float | httpx.Timeout | None",
        }
        for name in sorted(_resource_names(client)):
            for method_name, method in sorted(_public_methods(getattr(client, name)).items()):
                parameters = inspect.signature(method).parameters
                for override, annotation in expected.items():
                    actual = parameters[override].annotation
                    rendered = actual if isinstance(actual, str) else str(actual)
                    assert rendered.replace("supermetrics._generated.", "") == annotation, (
                        f"{name}.{method_name}.{override} is annotated {rendered!r}"
                    )


class TestRawResponseParity:
    """The `with_raw_response` views mirror the clients exactly."""

    def test_same_resources_are_mirrored(
        self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient
    ) -> None:
        """The raw view covers every resource, on both clients."""
        sync_raw = {name for name in vars(sync_client.with_raw_response) if not name.startswith("_")}
        async_raw = {name for name in vars(async_client.with_raw_response) if not name.startswith("_")}

        assert sync_raw == _resource_names(sync_client)
        assert async_raw == _resource_names(async_client)

    def test_same_methods_are_mirrored(
        self, sync_client: SupermetricsClient, async_client: SupermetricsAsyncClient
    ) -> None:
        """Each mirrored resource wraps exactly the methods of the real resource."""
        for name in sorted(_resource_names(sync_client)):
            expected = set(_public_methods(getattr(sync_client, name)))
            sync_wrapped = {n for n in vars(getattr(sync_client.with_raw_response, name)) if not n.startswith("_")}
            async_wrapped = {n for n in vars(getattr(async_client.with_raw_response, name)) if not n.startswith("_")}

            assert sync_wrapped == expected, f"raw view drift on {name}"
            assert async_wrapped == expected, f"async raw view drift on {name}"

    def test_wrapped_methods_keep_their_signature(self, sync_client: SupermetricsClient) -> None:
        """The mirrored methods stay introspectable as the methods they wrap.

        ``inspect.signature`` follows ``__wrapped__``, so comparing the two
        signatures alone would be a tautology for anything built with
        ``functools.wraps``. What is actually worth pinning is that the wrapping is
        in place at all: a hand-rolled wrapper without ``functools.wraps`` would
        present ``(*args, **kwargs)`` to IDEs and documentation tools.

        Note that ``functools.wraps`` also copies ``__annotations__``, so the runtime
        return annotation reports the wrapped method's type rather than
        ``ApiResponse[...]``. Static type checkers see the correct type through the
        ``ParamSpec`` signature of the wrapper factory.
        """
        for name in sorted(_resource_names(sync_client)):
            resource = getattr(sync_client, name)
            mirrored = getattr(sync_client.with_raw_response, name)
            for method_name in sorted(_public_methods(resource)):
                bound = getattr(resource, method_name)
                wrapped = getattr(mirrored, method_name)

                # Bound methods are created fresh on each attribute access, so compare by
                # equality (same underlying function and instance) rather than identity.
                assert getattr(wrapped, "__wrapped__", None) == bound, f"{name}.{method_name} is not wrapped"
                assert wrapped.__name__ == bound.__name__
                assert wrapped.__doc__ == bound.__doc__
                # What tooling sees, thanks to the wrapping above.
                assert inspect.signature(wrapped).parameters == inspect.signature(bound).parameters
                # And the wrapper really is a wrapper, not a copy of the method. Its own
                # parameters are generic; only following __wrapped__ reveals the real ones.
                own = inspect.signature(wrapped, follow_wrapped=False)
                assert list(own.parameters) == ["args", "kwargs"], f"{name}.{method_name}: {own}"


class TestClientConstructorParity:
    """Both client constructors offer the same configuration surface."""

    def test_constructor_parameters_match(self) -> None:
        """Only the token_provider annotation differs (sync vs async provider)."""
        sync_params = inspect.signature(SupermetricsClient.__init__).parameters
        async_params = inspect.signature(SupermetricsAsyncClient.__init__).parameters

        assert list(sync_params) == list(async_params)
        for name in sync_params:
            assert sync_params[name].kind is async_params[name].kind, name
            assert sync_params[name].default == async_params[name].default, name

    def test_token_provider_types_differ_as_designed(self) -> None:
        """The sync client takes TokenProvider; the async client also accepts awaitables.

        The aliases resolve to their underlying callable types at runtime, so this
        asserts on the resolved shape rather than the alias name.
        """
        sync_annotation = str(inspect.signature(SupermetricsClient.__init__).parameters["token_provider"].annotation)
        async_annotation = str(
            inspect.signature(SupermetricsAsyncClient.__init__).parameters["token_provider"].annotation
        )

        assert sync_annotation == "collections.abc.Callable[[], str] | None"
        assert "Awaitable[str]" in async_annotation
        assert "Callable[[], str]" in async_annotation


class TestSignatureIntrospection:
    """Every public method must be introspectable on every supported Python.

    Python 3.14 evaluates annotations lazily (PEP 649) in the scope where the
    function was defined, which for a method is the class body. A resource class
    that defines a method named ``list`` therefore shadows the ``list`` builtin
    for every annotation in that class, and ``inspect.signature`` raises
    ``TypeError: 'function' object is not subscriptable``. The resource modules
    use ``from __future__ import annotations`` to avoid this; these tests fail if
    that is ever dropped, or if a new class introduces the same shadowing.

    Introspection matters beyond tests: IDEs, documentation generators, and web
    frameworks that bind handlers all call these APIs.
    """

    @pytest.mark.parametrize("client_name", ["sync_client", "async_client"])
    def test_every_method_signature_is_introspectable(self, client_name: str, request: pytest.FixtureRequest) -> None:
        """inspect.signature() works on every public resource method."""
        client = request.getfixturevalue(client_name)
        for name in sorted(_resource_names(client)):
            for method_name, method in sorted(_public_methods(getattr(client, name)).items()):
                try:
                    inspect.signature(method)
                except Exception as error:  # noqa: BLE001 - the failure mode is the assertion
                    pytest.fail(f"inspect.signature({name}.{method_name}) raised {type(error).__name__}: {error}")

    @pytest.mark.parametrize("client_name", ["sync_client", "async_client"])
    def test_every_method_resolves_its_type_hints(self, client_name: str, request: pytest.FixtureRequest) -> None:
        """typing.get_type_hints() resolves on every public resource method."""
        client = request.getfixturevalue(client_name)
        for name in sorted(_resource_names(client)):
            for method_name, method in sorted(_public_methods(getattr(client, name)).items()):
                try:
                    typing.get_type_hints(method)
                except Exception as error:  # noqa: BLE001 - the failure mode is the assertion
                    pytest.fail(f"get_type_hints({name}.{method_name}) raised {type(error).__name__}: {error}")

    def test_client_constructors_are_introspectable(self) -> None:
        """Both client constructors can be introspected and their hints resolved."""
        for client_cls in (SupermetricsClient, SupermetricsAsyncClient):
            inspect.signature(client_cls.__init__)
            typing.get_type_hints(client_cls.__init__)
