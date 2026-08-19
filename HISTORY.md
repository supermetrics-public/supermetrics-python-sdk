# History

## 0.5.0 (unreleased)

### Account Tags (Phase 6)

`client.account_tags`, on both clients — `list`, `get`, `create`, `update`, `delete`,
`add_accounts` and `remove_accounts` over a team's account tags, the reusable labels that
group data source accounts from across its connections so a query or a transfer can name
the group instead of listing every account by hand. It appears under
`client.with_raw_response` and takes the same keyword-only `auth_token`, `headers` and
`timeout` overrides as every other resource.

Two names identify a tag and they are not interchangeable. `name` is the slug the server
assigns at creation, `"a1b2c3d"`, and it is what every later call addresses the tag by;
`display_name` is the human label, `"EMEA paid media"`. So `create()` takes no `name` at
all — you read it off the tag that comes back.

Five behaviours of the upstream API are exposed as they actually are, rather than smoothed
over:

* **`delete()` returns a `bool`, not `None`.** Every other delete in the SDK is a 204 and
  returns nothing. This one is a 200 whose entire body answers "did anything actually get
  deleted?", because upstream made deletion idempotent: removing a tag that does not exist
  is a success carrying `result=false` rather than a 404. Returning `None` would have
  discarded the one thing the endpoint exists to say. A `False` is not a failure — a
  genuine failure still raises, as everywhere else.
* **Nothing in this domain answers 404.** Not `get`, not `update`, not `delete`, not the
  two membership calls. An unknown tag arrives as an HTTP 400 and is translated to
  `SupermetricsValidationError`, exactly as a 422 would be elsewhere. There is no 422 here
  either.
* **`create()` answers 200, not 201, and it is the only endpoint in the SDK that can
  answer 409.** A conflict stays a plain `SupermetricsAPIError` with `status_code == 409`
  and `error_code == "CONFLICT_ERROR"`; giving one endpoint its own exception class would
  have meant widening the public error taxonomy for a single status.
* **`update()` renames and recolours; it cannot move accounts.** The PUT body carries
  `display_name` and `color` and nothing else, and both are required, so changing only the
  colour means resending the current label. Membership moves through `add_accounts()` and
  `remove_accounts()`, two PATCH endpoints whose body is `{"data_sources": [...]}`.
* **`list()` and `get()` return different types.** `AccountTagOverview` summarises
  membership as `data_source_count` and `account_count`; `AccountTag` carries the
  membership itself and no counts. They are not two projections of one model and the SDK
  does not pretend otherwise, so reading accounts off a listing means a `get()` per tag.

Membership is a list of plain dicts shaped like
`{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}`, and that example
is the only place the shape is written down. Upstream declares the array elements as a
bare `type: object`, so the generator emits classes holding nothing but an
`additional_properties` dict declared `init=False` — which a caller cannot construct. The
public signature takes `list[dict[str, Any]]` and converts at the call site, and no new
name is re-exported from the top-level package: four unconstructable aliases of one open
shape would be four names nobody could call.

Like custom fields, **account tags are served from the core API host**, with their `/v1`
prefix in the path — `/v1/teams/{team_id}/account_tags`. Nothing is re-hosted for them and
no routing change was needed.

### Custom Fields (Phase 4)

`client.custom_fields`, on both clients — `list`, `get`, `get_metadata`, `create`,
`update` and `delete` over a team's calculated dimensions and metrics, which the API calls
*field transformations*. It appears under `client.with_raw_response` and takes the same
keyword-only `auth_token`, `headers` and `timeout` overrides as every other resource.

A field's `definition` is an ordered pipeline of `FunctionStep`, `LookupStep` and
`ConditionStep`. Those three, and the value types they nest — `DefinitionValue`,
`FunctionArgument`, `ConditionCase`, `ConditionCaseCondition`, `LookupStepMap`,
`CustomFieldCreateRequestDataSourceItem` — are re-exported from the top-level package,
because `create()` and `update()` cannot be called without constructing them.
`get_metadata()` returns the functions, rules and data types a team is actually allowed to
use, which is the only way to find out short of a rejected `create()`.

Four behaviours of the upstream API are exposed as they actually are, rather than smoothed
over:

* **`list()` returns the page, not the pagination.** The response is double-wrapped: the
  page sits at `data.items` and `total_count` / `limit` / `offset` / next-page links ride
  in `meta`. Returning a page object would have made the common case — iterate the fields
  — go through a wrapper for no reason, and would have been the only resource on the
  client to do so. The metadata is not lost: `client.with_raw_response.custom_fields.list(...)`
  carries it in `.json_body["meta"]["pagination"]`, alongside the same parsed page in
  `.data`. `total_count` appears there only when `include_total_count=True` is passed —
  the API omits it by default because counting costs time, so reading it unconditionally
  raises `KeyError` rather than returning a wrong number.
* **Only the query parameters the caller supplied are sent.** With no optional arguments
  the query string is empty. In particular `limit` is not sent, even though the generated
  layer defaults it to 25; the server applies its own default instead, so the SDK never
  silently pins a page size nobody asked for.
* **`update()` is not `create()` with an id attached.** It takes no `field_type` and no
  `data_source`: upstream states the field kind is fixed at creation, and the request body
  does not carry it. It is also a whole-object replace — there is no PATCH endpoint, so
  every field is resent on every call and anything omitted reverts to unset. The success
  statuses differ too: `create()` answers `201`, `update()` `200`, `delete()` `204`.
* **A rejected definition is an HTTP 400.** This domain documents no 422 at all, so an
  unknown function name or a malformed step arrives as a 400 and is translated to
  `SupermetricsValidationError`, exactly as a 422 would be elsewhere. `list()` and
  `get_metadata()` document no 404 either.

The `definition` is also asymmetric between request and response — sent as a bare list of
steps, returned wrapped in an object with an `items` attribute. That is upstream's shape
and the SDK does not paper over it, so a read-modify-write reads `field.definition.items`
and passes that list straight back to `update()`. Two generated names follow from the wire
format rather than from taste: `ConditionCase`'s field is `return_`, because `return` is a
Python keyword, and `LookupStepMap` holds its mapping in `additional_properties` (declared
`init=False`), so it is built empty and assigned into rather than constructed from a dict.

Unlike transfers and backfills, **custom fields are served from the core API host**, with
their `/v1` prefix in the path — `/v1/teams/{team_id}/custom-fields`. Nothing is re-hosted
for them and no routing change was needed; a plain client reaches them as it does queries
and logins.

### Data Transfers & Transfer Runs (Phase 2)

Two new resources, on both clients, covering the full Data Warehouse transfer surface:

* `client.transfers` — `list`, `get`, `create`, `update`, `delete`, `set_state`,
  `validate`, `validate_update`, `list_available_sources`, `get_available_options`,
  `list_runs`, and `create_datasource_connection`.
* `client.transfer_runs` — `get`, looking a run up by its own id within a team.

Both appear under `client.with_raw_response` and take the same keyword-only `auth_token`,
`headers` and `timeout` overrides as every other resource.

Three behaviours of the upstream API are exposed as they actually are, rather than
smoothed over:

* **`validate()` and `validate_update()` do not raise on an invalid configuration.** The
  API answers `200 OK` with `is_valid: false`, and the SDK returns that result. Raising
  would defeat the purpose of a dry run. A `ValidationError` carries `field_id` and
  `error_code` only — the API sends no human-readable message.
* **`set_state()` takes `"pause"` / `"unpause"`**, the only machine-readable enum in this
  area. The `state` field on the response is a free-form string whose documented example
  is uppercase `"PAUSED"`; request and response do not share a vocabulary.
* **`list()` and `get()` return different shapes.** The list item has `dwh_transfer_id`, a
  `schedule` *string* and an `accounts` *string array*; the detail object has
  `transfer_id`, a `schedule` *array* and an `accounts` *object array*. The list item is
  not a subset of the detail object.

`update()` is a whole-object replace: the request schema forbids extra properties and
there is no PATCH endpoint, so every field has to be resent.

`create_datasource_connection()` deliberately does not expose the request schema's
optional `api_key` field. Upstream describes it as automatically handled, and it
duplicates a credential that already travels in the `Authorization` header.

### Data Warehouse calls are routed automatically

Transfers, transfer runs, backfills and data source connections are served from
`https://dts-api.supermetrics.com/v1`, not from the core API host. The SDK now re-hosts
those requests from its request event hook, so one pooled client reaches everything:

```python
client = SupermetricsClient(api_key="api_...")
client.queries.get(...)  # api.supermetrics.com
client.transfers.list(team_id=1)  # dts-api.supermetrics.com/v1
client.backfills.list_incomplete(team_id=1)  # dts-api.supermetrics.com/v1
```

**This changes backfills.** `client.backfills.*` previously 404'd on a default client;
callers had to build a second client on the Data Warehouse host, as
`docs/api-reference.md` instructed. That workaround still works untouched — routing is
only inferred when `base_url` is left at its production default, and any `base_url` you
set yourself is taken literally and receives every request. The new keyword-only
`dts_base_url` parameter, on both clients, points Data Warehouse traffic somewhere
specific.

If you currently hold two clients, one of them is now redundant.

### Generation pipeline

`scripts/filter_openapi_spec.py` gained two options, both documented in
`docs/openapi-generation.md`:

* **`pin_baseline`** — endpoints already in the committed `openapi-spec.yaml` are taken
  from it rather than re-read from upstream, so a regeneration is purely additive. The
  upstream specifications had drifted far enough that regenerating for this change would
  otherwise have retagged most operations (moving their generated modules and breaking
  seven adapter imports) and dropped `GET /query/data/json`, which upstream has
  reparameterised to `GET /query/data/{context_type}`. Refreshing those is a separate,
  deliberate change.
* **`rewrite_path`** — writes an endpoint into the merged spec under a different path.
  Upstream splits the `/v1` prefix inconsistently between the path and the path-level
  `servers` entry, and `openapi-python-client` ignores path-level `servers`, so without
  normalisation the transfers and backfills families cannot share a base URL.

Regenerating also picked up the `openapi-python-client` 0.27.1 → 0.29.0 upgrade, which
had been pinned but never applied. It adds percent-encoding of path parameters and drops
some redundant casts across the generated tree. No endpoint or model was removed.

### Testing

`tests/e2e/` covers every new method on both the sync and async clients over a real
loopback socket, asserting on the outgoing request — verb, path, query string, body, and
credential — as well as the response. `tests/e2e/test_dts_routing_e2e.py` runs **two**
local servers, which is the only way to tell "sent to the right host" apart from "sent to
the only host there is".

---

## 0.4.0 (2026-08-18)

### Breaking changes

Verified by diffing the public API surface against the previous release and by running
pre-Phase-1 usage patterns against the new code. **No API shape changed**: nothing was
removed or renamed, no parameter changed position or default, and all 174 new method
parameters are keyword-only with defaults. `api_key` went from required-positional to
optional, which is strictly more permissive. Three behaviours did change.

1. **`except APIError` now catches authentication and validation errors.**
   `AuthenticationError` and `ValidationError` are subclasses of `APIError`, so a handler
   chain that lists `APIError` *first* will swallow them:

   ```python
   try:
       client.logins.list()
   except APIError:  # <- now also catches 401 and 400/422
       ...
   except AuthenticationError:  # <- unreachable
       refresh_token()
   ```

   Fix by ordering the specific clauses first. `except SupermetricsError` is unaffected,
   and a chain that already listed the specific errors first is unaffected.

2. **`custom_headers={"Authorization": ...}` no longer changes the credential.** It is
   ignored with a `UserWarning`; the credential comes from `api_key` / `bearer_token` /
   `token_provider`. Previously it overrode a static `api_key` but lost to a
   `token_provider`, so the same headers sent different credentials depending on the
   mechanism. To send a different credential for one call, use a method's `headers` or
   `auth_token` argument.

3. **Failed writes now raise instead of reporting success.**
   `connector_builder.update/delete` and `connector_builder_secrets.update/delete`
   returned `None` for any HTTP status the API specification does not describe — a gateway
   `502` was indistinguishable from a real `204 No Content`. They now raise
   `SupermetricsServerError`. Code that relied on those calls never raising will now see
   exceptions on failures it was previously silently ignoring.

#### Lower-risk behaviour changes

- HTTP 403, 404, 429 and 5xx now raise a specific subclass rather than a bare `APIError`.
  `except APIError` is unaffected; only an exact `type(e) is APIError` check would notice.
- `status_code` is now accurate on errors that previously reported `0`, and `error_code` /
  `details` are populated on routes that previously dropped them.
- A malformed credential (blank, control characters, non-ASCII) raises
  `SupermetricsClientError` instead of surfacing later as `NetworkError` or an uncaught
  `UnicodeEncodeError`.
- Constructing a client with no credential raises `SupermetricsClientError` (a `ValueError`)
  rather than `TypeError`.
- An error response whose body is not JSON now raises an SDK exception instead of letting
  `json.JSONDecodeError` escape.
- `logins` no longer logs end-user usernames at INFO.

---

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
