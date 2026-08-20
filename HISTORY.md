# History

## 0.5.1 (2026-08-20)

### Packaging

The distribution now ships a PEP 561 `py.typed` marker at the package root
(`supermetrics/py.typed`). Every module in `supermetrics` is fully annotated, but
without this marker a type checker treated the installed package as untyped: `import
supermetrics` raised `import-untyped`, and downstream projects had to silence it with a
per-module `ignore_missing_imports` override. The marker makes the SDK's existing
annotations visible to `mypy`, `pyright` and other PEP 561 consumers, so that workaround
can be removed.

The generated subpackage already carried its own marker; this adds the top-level one that
governs the public `supermetrics.*` API. No code or API changed.

## 0.5.0 (2026-08-20)

### Teams & User Identity (Phase 8)

A new `client.teams` resource with two read methods on both clients:
`client.teams.get(team_id)` returns the team (id, name, `display_id`, status and created
time) and `client.teams.list_users(team_id)` returns its members with their roles. Both
appear under `client.with_raw_response` and take the same keyword-only `auth_token`,
`headers` and `timeout` overrides as every other resource.

Teams live on the **core API host** under the `/v1` prefix — `/v1/teams/{team_id}` and
`/v1/teams/{team_id}/users` — so nothing is re-hosted and both responses arrive wrapped in
`{"meta": ..., "data": ...}`, which the adapters unwrap.

### Logins & Login Links (Phase 7)

Three methods added to resources that already existed: `client.logins.get_accounts` and
`client.logins.revoke`, and `client.login_links.update`, on both clients. Each appears under
`client.with_raw_response` and takes the same keyword-only `auth_token`, `headers` and
`timeout` overrides as every other resource. These close the plan's last read/write gaps in
the Logins & Login Links domain — the one domain in the SDK that had shipped with no
end-to-end coverage at all, and which now has full end-to-end coverage on both clients.

Unlike every domain since Phase 2, these endpoints live on the **core API host** under the
`/ds/...` paths — the same host `logins.get` and `login_links.create` already used — so
nothing is re-hosted and no `team_id` is in play.

Four behaviours of the upstream API are exposed as they actually are, rather than smoothed
over:

* **`revoke()` returns a `bool`, not `None`.** It is a `DELETE`, but upstream answers HTTP
  200 with `{"data": {"result": true}}` rather than the empty 204 a delete usually is, and
  the SDK returns that `result`. (`login_links.close()`, the other teardown in this domain,
  is the ordinary shape and still returns `None`.)
* **`get_accounts()` is paginated.** `offset` and `limit` are always sent as query params —
  defaulting to `0` and `100` — and the total count rides in the response `meta`, not in the
  returned list. Reach it through the raw response:
  `client.with_raw_response.logins.get_accounts(...).json_body["meta"]["paginate"]["total"]`.
* **`update()` accepts only `description`.** The plan expected it to change expiry and
  redirect settings too, but the upstream `PATCH /ds/login/link/{link_id}` body carries a
  single `description` field and nothing else. A link's data source, expiry, redirect and
  username requirements are fixed at creation — those live on `create()`, not here.
* **The `PATCH` had to be filed under `data_source_login_links` by hand.** Upstream leaves
  `PATCH /ds/login/link/{link_id}` untagged, so the generator would have dropped it into a
  default catch-all API module rather than alongside the other login-link operations. A tag
  patch in `scripts/references/sdk-endpoint-filters.yaml` assigns it the
  `data_source_login_links` tag, so `update_login_link` lands in the same generated
  subpackage as `create_login_link`, `get_login_link`, `list_login_links` and
  `close_login_link` (`get_accounts` and `revoke` sit under `data_source_logins` the same
  way).

`get_accounts()` returns a list of `DataSourceAccount`s — `type_` (from the wire's `@type`),
`account_id`, `name` and `group` name each account the login can reach. Like every other
response-only model it is not re-exported from the top-level package; you read it off the
returned list. `get_accounts()` and `revoke()` document 401, 403, 404, 422, 429 and 500 and
no 400; `update()` documents 400 as well.

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

### Data Blending (Phase 5)

`client.blends`, on both clients — `list`, `get`, `create`, `update` and `delete` over a
team's blends: the combined tables that draw their rows from several data sources at once.
It appears under `client.with_raw_response` and takes the same keyword-only `auth_token`,
`headers` and `timeout` overrides as every other resource.

A blend is one of two kinds. A `union` stacks rows from each source under a shared set of
blend fields; a `join` joins the sources on shared fields, with one primary table and one
join per additional source. Two things describe it: `blended_data_sources`, the sources it
draws on, and `config`, which maps each source's native fields onto the blend's own fields
and — for a join — says how they are joined. `BlendedDataSourceInput`, `BlendConfig`,
`BlendField`, `BlendDatasourceFieldRef`, `BlendJoin`, `BlendJoinCondition` and the small
types they nest are re-exported from the top-level package, because `create()` and
`update()` cannot be called without constructing them.

Five behaviours of the upstream API are exposed as they actually are, rather than smoothed
over:

* **`list()` returns summaries, not blends.** A `BlendListItemOutput` carries no `config`
  at all and a reduced view of each data source, so a caller who wants a blend's fields has
  to `get()` it. Annotating the list as returning whole blends would have been a lie that
  surfaced only as an `Unset` attribute at runtime, on the caller's machine rather than on
  ours.
* **The list endpoint is not paginated.** It answers with every matching blend in one
  array, so there is no page size to choose and no cursor to follow. That is why `list()`
  returning a bare list costs nothing here, where the equivalent decision for custom fields
  had to be justified by `with_raw_response` keeping the pagination reachable.
* **Requests and responses are not the same shape.** Every collection is sent as a bare
  list and comes back wrapped in an object with an `items` attribute — at every level, so a
  read goes through `blend.blended_data_sources.items`, `blend.config.fields.items`,
  `field.blend_datasource_fields.items` and `join.conditions.items`. The response also drops
  `blend_data_source_key` everywhere and adds `blend_field_type` and
  `blend_field_data_type`, which upstream infers and the request has no way to set. A blend
  therefore cannot be read back and resent unchanged; a read-modify-write has to rebuild the
  request objects. The SDK does not paper over this, and the end-to-end suite pins both
  directions rather than assuming either.
* **New data sources are named by a key, existing ones by an id.** A source being created
  has no id yet, so it is given a `blend_data_source_key` — exactly eight lowercase
  alphanumerics — that every field and join reference in the same request points at. On
  update, sources that already exist are addressed by `blend_data_source_id` and newly added
  ones by a fresh key, so one body legitimately carries both. `BlendedDataSourceInput` also
  marks `blend_data_source_id`, `blend_data_source_key`, `report_type` and
  `report_type_settings` required *but nullable*: all four must be passed even though three
  of them are usually empty.
* **`create()` takes the blend type, `update()` does not.** Upstream fixes a blend's kind at
  creation and the update body does not carry it, so this is not `create()` with an id
  attached. It is also a whole-object replace — there is no PATCH endpoint — so the required
  fields are resent in full on every call and a source or field left out is dropped. The
  success statuses differ as well: `create()` answers `201`, `update()` `200`, `delete()`
  `204`. A rejected blend is an
  HTTP **400**; this domain documents no 422 at all, and only the three by-id operations
  document a 404. Nothing in the SDK checks that a `union` blend omits `joins` or that a
  `join` blend supplies `query_table` — upstream is what rejects those, also with a 400.

Like custom fields, **blends are served from the core API host** with their `/v1` prefix in
the path, so nothing is re-hosted and no routing change was needed. That is a claim worth
more than a comment: `tests/e2e/test_dts_routing_e2e.py` now runs a second local server and
asserts the Data Warehouse origin receives nothing when a blend is listed, read or deleted,
on both clients. A rewrite to the `/teams/...` shape transfers use would have dropped the
`/v1` the core API requires *and* sent the call to the wrong host, and one server cannot
tell those apart.

Every method is covered end to end on both clients rather than only in unit tests — 83
tests driving the real stack over a loopback socket, alongside 92 unit tests at the
generated-client boundary. They run in CI in both the version matrix and the dedicated
end-to-end job.
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

### Storage & Warehouse Destinations (Phase 3)

One new resource, on both clients, covering the destinations that transfers write into:

* `client.destinations` — `list`, `get`, `create`, `update`, `delete`, `test_connection`,
  and `get_usage`.

It appears under `client.with_raw_response` and takes the same keyword-only `auth_token`,
`headers` and `timeout` overrides as every other resource. Like transfers, transfer runs
and backfills, these endpoints are served by the Data Warehouse API on its own host, and
the SDK routes them there automatically — an ordinary client reaches them.

Three things about this domain are worth knowing before the first call:

* **`fields` is a plain `dict[str, Any]`, deliberately.** `create()`, `update()` and
  `test_connection()` take the destination-specific configuration as a mapping, and the
  SDK converts it. The generated `CreateDestinationRequestFields`,
  `UpdateDestinationRequestFields` and `TestConnectionRequestFields` classes keep their
  storage in an attrs attribute declared `init=False`, so a caller cannot construct one;
  exporting three unconstructable near-identical types would have been worse than
  exporting none. This phase adds no new names to the package root.
* **A failed connection test is a return value, not an exception.** The API answers
  `200 OK` with `success: false` and an `error` message for credentials that do not work,
  and `test_connection()` returns that result. Branch on `result.success`; only transport,
  authorization and malformed-payload failures raise. Same rule as `transfers.validate()`.
* **The read shape and the write shape differ.** `get()` answers with
  `edit_settings`, a list of `SetupSetting` UI form descriptors, while `create()` and
  `update()` take a flat `fields` mapping. A `DestinationInfo` cannot be handed straight
  back to `update()`; the SDK surfaces the API's own model rather than inventing a
  symmetrical one.

`create()` and `delete()` both document HTTP 409 Conflict. The error taxonomy has no
conflict subclass, so a 409 arrives as a generic `SupermetricsAPIError` with
`status_code == 409` — adding a dedicated subclass is a change to the public taxonomy and
belongs in its own release, not behind a new resource.

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

### Data Warehouse calls are routed automatically

Transfers, transfer runs, destinations, backfills and data source connections are
served from `https://dts-api.supermetrics.com/v1`, not from the core API host. The SDK now re-hosts
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

### Production-shape fixes

Running the SDK against the live API surfaced four places where the OpenAPI spec disagreed
with what production actually returns; each crashed a call while parsing a real response.
All four are fixed at the schema source and regenerated, and are locked in by regression
tests (`tests/e2e/test_prod_shape_regressions_e2e.py`); the details are logged in
`docs/openapi-spec-fixes.md`.

* **`custom_fields.list()`** raised on a normal call. `Pagination` required
  `total_count`/`limit`/`offset`, which production sends only with
  `include_total_count=true`, and `PaginationLinks` modelled `next`/`previous` as objects
  when production sends `first`/`prev`/`next`/`last` as nullable URL strings.
* **`destinations.get()`** raised on any destination carrying an auth method: `AuthMethod`
  required a `label` the API never sends (it sends `title`, plus `fields` and
  `new_secret_field`).
* **`account_tags.list()`** raised because the response is double-wrapped as `data.items`
  (like custom fields and blends), not the bare `data` array the spec declared.

These endpoints now parse real responses correctly on both clients. Every SDK operation is
additionally exercised by a read-only live smoke test (`tests/e2e/test_live_smoke.py`),
team-gated on `SUPERMETRICS_TEAM_ID` so it self-skips without credentials.

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

`scripts/regenerate_client.sh` was fixed as well — Step 4 of the documented regeneration
procedure could not succeed on a stock checkout, and failed destructively:

* It deleted `src/supermetrics/_generated/` **before** running the generator, so any
  generator failure left the repository with no client at all. It now generates into a
  staging directory and replaces the committed tree only once generation has succeeded.
* The generator crashed on this project's default interpreter. `openapi-python-client`
  0.29.0 pulls in a pydantic that raises `AssertionError` in
  `_typing_extra.eval_type_backport` under Python 3.14, which is what the project
  virtualenv runs. The script now runs the generator through `uvx` on a pinned Python 3.12
  (`GENERATOR_PYTHON`, overridable) at the version read out of `pyproject.toml`, so the
  generator and its dev-dependency pin cannot drift, and the project virtualenv is left
  alone.

### Testing

`tests/e2e/` covers every new method on both the sync and async clients over a real
loopback socket, asserting on the outgoing request — verb, path, query string, body, and
credential — as well as the response. `tests/e2e/test_dts_routing_e2e.py` runs **two**
local servers, which is the only way to tell "sent to the right host" apart from "sent to
the only host there is".

### Pydantic is no longer a dependency

`pydantic>=2.0.0` has been dropped from `project.dependencies`. Nothing in the SDK ever
imported it: `openapi-python-client` generates `attrs` classes, not Pydantic models, so
the declaration only forced every installation to pull `pydantic` and its compiled
`pydantic-core` wheel for nothing. The README's "Pydantic v2 models for request/response
validation" line described the same thing that was never true and has been corrected.

Nothing in the public API changes. Code that imported `pydantic` and happened to get it
transitively through this package now has to depend on it directly.

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
