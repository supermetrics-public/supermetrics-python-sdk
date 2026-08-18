# History

## 0.4.0-beta1 (2026-08-18)

### Core client, authentication & transport modernization (Phase 1)

**Authentication**

* `SupermetricsClient` and `SupermetricsAsyncClient` now accept exactly one of `api_key`,
  `bearer_token`, or `token_provider`. Supplying none or more than one raises
  `SupermetricsClientError` (which is also a `ValueError`).
* Added OAuth bearer token support (`bearer_token="otok_..."`). Tokens are treated as
  opaque strings, so API keys, OAuth access tokens, RFC 8693 exchanged/delegated tokens,
  and JWTs are all accepted.
* Added dynamic token providers, re-evaluated on every request, so short-lived tokens can
  be refreshed without discarding the client's connection pool.
  `SupermetricsClient` takes a synchronous `TokenProvider`; `SupermetricsAsyncClient`
  takes an `AsyncTokenProvider` and accepts both coroutine functions and plain callables.

**Per-request overrides**

* Every resource method on both clients now accepts keyword-only `auth_token`, `headers`,
  and `timeout` overrides, so one shared, pooled client can serve concurrent callers that
  each bring their own credential, tracing headers, and timeout budget.
* Header merging is case-insensitive; per-request headers take precedence over client-level
  `custom_headers`, which in turn take precedence over the SDK defaults.
* Added the public context variables `current_auth_token`, `current_request_headers`, and
  `current_request_timeout`, plus the `request_options()` context manager, for ambient
  propagation from web-framework middleware. Values are isolated per thread and per
  asyncio task.

**Response metadata**

* Added `ApiResponse[T]`, carrying `data`, `status_code`, `headers`, `raw_body`,
  `json_body`, and the `span_id` / `request_id` / `retry_after` helper properties.
* Added the `client.with_raw_response` accessor, mirroring every resource method with an
  identical signature but returning `ApiResponse[T]`.

**Error taxonomy**

* Added `SupermetricsAPIError` and its subclasses `SupermetricsAuthError` (401),
  `SupermetricsForbiddenError` (403), `SupermetricsNotFoundError` (404),
  `SupermetricsValidationError` (400/422), `SupermetricsRateLimitError` (429), and
  `SupermetricsServerError` (5xx), plus `SupermetricsClientError` for local configuration
  problems.
* Every HTTP error now preserves `headers`, `error_code`, `error_message`, `details`, and
  `raw_response`, and exposes `retry_after`, `request_id`, and `span_id`.
* 401 responses surface the upstream OAuth code (for example `ACCESS_TOKEN_INVALID`) in
  `error_code`, so callers can refresh a token and retry instead of failing outright.
* **Fixed:** responses whose body did not match the schema in the OpenAPI document, and
  responses carrying a status that document does not describe for the operation, were
  reported as an unclassified error with no status code. A 404, a throttling 429, or a
  gateway 502 could therefore look identical to a parsing bug. Such responses are now
  classified by the status code the transport actually observed.
* **Fixed:** `error_code` and `details` were dropped whenever the generated parser did not
  model the returned status, so the same error payload produced an `error_code` on some
  adapters and `None` on others. They are now recovered from the raw JSON body on every
  route.
* **Fixed:** `retry_after` raised `ValueError` for a `Retry-After` header containing a
  Unicode digit that `int()` cannot parse, such as a superscript two.
* **Fixed:** `connector_builder.update()`, `connector_builder.delete()`,
  `connector_builder_secrets.update()` and `connector_builder_secrets.delete()`, on both
  the sync and async clients, reported success for any HTTP status the OpenAPI
  document does not describe for the operation. A `502` from a gateway returned `None`,
  exactly like a genuine `204 No Content`, so callers believed a delete had succeeded when
  it had not.
* **Fixed:** the connector-builder adapters let raw `json.JSONDecodeError`, `KeyError` and
  `TypeError` escape instead of an SDK exception, because they used a hand-rolled
  `try`/`except` chain rather than the shared handler. A documented error status carrying a
  non-JSON body (an HTML error page, say) surfaced as a `JSONDecodeError`. All 26 of those
  methods now go through `api_error_handler`.
* **Fixed:** a blank `auth_token`, or a token provider returning an empty string, was sent
  as a bare `Authorization: Bearer` and failed with an opaque server-side error. It is now
  rejected as `SupermetricsClientError`.
* **Fixed:** a credential containing a character that cannot be sent in an HTTP header — a
  newline from a line-wrapped file, or a typographic dash pasted from a document — either
  escaped as a raw `UnicodeEncodeError` or was quoted verbatim by the transport into an
  error message that callers log. Such credentials are now rejected as
  `SupermetricsClientError` with a message that never echoes the value, and any bearer
  value appearing in transport error text is redacted.
* **Changed:** `logins.get()` and `logins.get_by_username()` no longer log the end user's
  username at INFO. The opaque login ID is still logged; the username moved to DEBUG.
* **Fixed:** `ResponseRecord.of` guarded `httpx.Response.request` with a `None` check, but
  that property raises `RuntimeError` when no request is attached.
* **Fixed:** `_handle_request_error` read `httpx.RequestError.request` unguarded. That
  property raises `RuntimeError` when no request is bound to the exception, which masked
  the underlying network failure. Such errors are now reported as `NetworkError` with no
  endpoint.
* **Fixed (Python 3.14):** `inspect.signature()` and `typing.get_type_hints()` raised
  `TypeError: 'function' object is not subscriptable` for `accounts.list`, `logins.list`,
  and `login_links.list`. Under PEP 649 an annotation is evaluated lazily in the scope
  where the function was defined, so a class that defines a method named `list` shadows the
  `list` builtin for every annotation in that class. The resource modules now use
  `from __future__ import annotations`, and `tests/test_api_parity.py` fails if any public
  method ever becomes uninspectable again. This affected IDEs, documentation generators,
  and any framework that introspects the SDK on Python 3.14.

**Security & consistency**

* `custom_headers={"Authorization": ...}` no longer changes which credential is sent. It
  previously won against a static `api_key` but lost to a `token_provider`, so identical
  headers produced a different credential depending on the mechanism. The credential now
  always comes from `api_key` / `bearer_token` / `token_provider`; setting `Authorization`
  in `custom_headers` emits a `UserWarning` and is ignored. Per-request `headers` remain
  the supported way to send a different credential for one call.
* Credentials are redacted from `NetworkError` messages. A token containing a byte the
  HTTP layer rejects was previously echoed verbatim into the exception message, and from
  there into callers' logs.
* The scheduled live-API workflow no longer accepts a free-text `base_url` input. It reads
  the target host from a repository variable instead, so nobody who can dispatch the
  workflow can redirect the production API key to a host of their choosing.

**Compatibility**

* `APIError`, `AuthenticationError`, and `ValidationError` remain importable and are now
  aliases of `SupermetricsAPIError`, `SupermetricsAuthError`, and
  `SupermetricsValidationError`.
* **Behaviour change:** `AuthenticationError` and `ValidationError` are now subclasses of
  `APIError`. `except SupermetricsError` is unaffected, but code that catches `APIError`
  before `AuthenticationError` will now match authentication errors in the first clause.

**Quality**

* Added `tests/test_api_parity.py`, which reflects over both clients and fails the build if
  resource names, method names, parameter names, annotations, or defaults ever drift apart.
* Added `tests/e2e/`, which drives the real client stack over a loopback TCP socket against
  a local HTTP server — no mocking or patching — covering authentication, token providers,
  per-request overrides, real timeouts, the raw-response envelope, the error taxonomy, and
  concurrency isolation on a shared connection pool.
* CI now runs `mypy --strict`, a dedicated end-to-end job, and a parity job. A scheduled
  workflow runs live smoke tests against the real API when credentials are configured.
* Corrected the ruff `target-version` to `py311` to match `requires-python = ">=3.11"`; it
  had been set to `py312` and was proposing syntax that would not run on Python 3.11.

## 0.3.0-beta1 (2026-06-09)

* Add Connector Builder resource with full CRUD support: create, get, list, update, delete connectors
* Add Connector Builder Secrets resource: create, list, update, delete encrypted secrets
* Add Connector Builder Logs resource: list and get connector execution logs
* Add Connector Builder Logo support: get and upload connector logos
* Add `connector_builder_flow.py` example with `--base-url` flag for local dev testing
* Fix OpenAPI filter script: resolve transitive schema dependencies and bare `$ref` rewriting

## 0.2.0-beta1 (2026-03-26)

* Add Backfills resource with full CRUD support: create, get latest, list incomplete, and cancel backfills ([#16](../../pull/16))
* Add public documentation link and fix broken links ([#17](../../pull/17))
* Remove broken documentation link ([#13](../../pull/13))
* Security: bump `actions/download-artifact` from 7 to 8 ([#14](../../pull/14))
* Security: bump `actions/upload-artifact` from 6 to 7 ([#15](../../pull/15))

## 0.1.0 (2025-10-28)

* First release on PyPI.
