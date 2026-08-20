# OpenAPI Spec Fixes

A running log of places where the upstream OpenAPI specification disagreed with what
the **real** Supermetrics API returns, and how we corrected it.

Each entry here was found by running the SDK against the production API (`just live`
with a real key and `SUPERMETRICS_TEAM_ID`). The committed hermetic fixtures were, in
every case, more complete than production — they included fields the API omits — so the
unit and e2e suites stayed green while the same call raised on real data. See
`tests/e2e/test_prod_shape_regressions_e2e.py`, which reproduces each production shape
over a loopback socket and now passes.

## How these fixes are applied

We do **not** hand-edit `src/supermetrics/_generated/`. The fix belongs in the source
spec, and the client is regenerated from it:

1. Correct the schema in the source spec under `openapi-specs/` (for these four,
   `openapi-specs/openap-management.yaml`).
2. Re-filter and re-merge into `openapi-spec.yaml`:
   ```bash
   uv run python scripts/filter_openapi_spec.py
   ```
3. Regenerate the low-level client:
   ```bash
   ./scripts/regenerate_client.sh
   ```
4. Update any hand-written adapter in `src/supermetrics/resources/` whose unwrapping
   assumptions changed, plus the hermetic fixtures that encoded the old (wrong) shape.
5. Run `just qa` and `just live`.

> **`pin_baseline` gotcha.** `scripts/references/sdk-endpoint-filters.yaml` sets
> `pin_baseline: openapi-spec.yaml`, and baseline component schemas **win over the source
> spec** (this is deliberate anti-drift for shipped models). So a source edit to a schema
> that already exists in `openapi-spec.yaml` is silently ignored on the next filter run.
> To adopt a corrected source schema, delete that schema from `openapi-spec.yaml` before
> re-filtering so the filter re-collects it from source, then regenerate.
>
> An interim alternative — used first for the four fixes below, then removed once the
> source spec was corrected — is a `component_patches.schemas.<Name>` entry in the filter
> config (`merge:` deep-merges, lists replace wholesale; `replace:` overwrites named keys),
> which is applied last and so beats the baseline without touching source.

---

## 2026-08-20 — Four production-shape mismatches

Found while adding end-to-end coverage and running the live suite against a production
team. All four are model-vs-reality mismatches, now corrected in the source spec
(`openapi-specs/openap-management.yaml`) and regenerated.

### 1. `Pagination` required fields the API omits

- **Endpoint / call:** `GET /v1/teams/{team_id}/custom-fields` — `client.custom_fields.list()`
- **Symptom:** `SupermetricsAPIError: 'total_count'` (`KeyError` in `Pagination.from_dict`),
  reported with `status_code=0` because the failure was client-side parsing, not an HTTP
  error. The raw-response path raised too.
- **Root cause:** The schema marked `total_count`, `limit`, and `offset` as `required`.
  Production only returns those when the caller passes `include_total_count=true`; on a
  default `list()` call `meta.pagination` carries only `links`.
- **Fix:** Make the three optional.
  ```yaml
  Pagination:
    merge:
      required: []
  ```

### 2. `PaginationLinks` modelled the wrong shape

- **Endpoint / call:** same as #1 — surfaced only after #1 was fixed and parsing reached
  the links.
- **Symptom:** `SupermetricsAPIError: 'NoneType' object is not iterable`
  (`TypeError` in `ResourceUrl.from_dict(None)`).
- **Root cause:** The schema modelled `next`/`previous` as `ResourceUrl` objects
  (`{href: ...}`). Production sends `first`/`prev`/`next`/`last` as bare, nullable URL
  strings, so the `null` `next` blew up `ResourceUrl.from_dict`.
- **Fix:** Redefine the four link fields as nullable URL strings.
  ```yaml
  PaginationLinks:
    replace:
      properties:
        first: {type: string, format: uri, maxLength: 2048, nullable: true}
        prev:  {type: string, format: uri, maxLength: 2048, nullable: true}
        next:  {type: string, format: uri, maxLength: 2048, nullable: true}
        last:  {type: string, format: uri, maxLength: 2048, nullable: true}
  ```

### 3. `AuthMethod` had the wrong shape

- **Endpoint / call:** `GET /teams/{team_id}/destinations/{destination_id}` —
  `client.destinations.get()`
- **Symptom:** `SupermetricsAPIError: 'label'` (`KeyError` in `AuthMethod.from_dict`).
  `destinations.list()` and `destinations.get_usage()` were unaffected because only the
  detail response embeds auth methods.
- **Root cause:** The schema modelled an auth method as `{id, label, is_default}` with
  `label` required. Production returns `{id, title, fields[], new_secret_field}` and never
  sends `label`.
- **Fix:** Redefine to the real shape; `fields` and `new_secret_field` reuse
  `SetupSetting` (the same field shape destination settings use).
  ```yaml
  AuthMethod:
    replace:
      required: [id, title]
      properties:
        id: {type: string, maxLength: 100}
        title: {type: string, maxLength: 255}
        fields:
          type: array
          maxItems: 50
          items: {$ref: '#/components/schemas/SetupSetting'}
        new_secret_field: {$ref: '#/components/schemas/SetupSetting'}
        is_default: {type: boolean, default: false}
  ```

### 4. `AccountTagListResponse` was not double-wrapped

- **Endpoint / call:** `GET /v1/teams/{team_id}/account_tags` — `client.account_tags.list()`
- **Symptom:** `SupermetricsAPIError: dictionary update sequence element #0 has length N; 2
  is required` (`ValueError` — `AccountTagOverview.from_dict` was handed a dict key string).
- **Root cause:** The schema modelled `data` as a bare array of `AccountTagOverview`.
  Production double-wraps the page as `data.items`, the same shape custom fields and blends
  use. `from_dict` iterated the wrapper object's keys instead of a list.
- **Fix (schema):** `data` becomes an object holding `items`, and the response also
  declares `meta` (both `meta`/`data` required, `items` required) to match the real
  `{meta, data: {items: [...]}}` envelope.
  ```yaml
  AccountTagListResponse:
    type: object
    additionalProperties: false
    required: [meta, data]
    properties:
      meta: {$ref: '#/components/schemas/Meta'}
      data:
        type: object
        additionalProperties: false
        required: [items]
        properties:
          items:
            type: array
            maxItems: 500
            items: {$ref: '#/components/schemas/AccountTagOverview'}
  ```
- **Fix (adapter):** `src/supermetrics/resources/account_tags.py::_overviews_of` now reads
  `parsed.data.items` (guarding `Unset` at both levels) instead of `parsed.data`.
- **Fixtures:** the hermetic account-tag list bodies in `tests/e2e/test_account_tags_e2e.py`,
  `tests/e2e/test_account_tags_overrides_e2e.py`, `tests/e2e/test_dts_routing_e2e.py`, and
  the `tests/unit/test_account_tags.py` helper were updated from `{"data": [...]}` to
  `{"meta": {...}, "data": {"items": [...]}}`.
