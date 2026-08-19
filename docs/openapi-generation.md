# OpenAPI Code Generation Guide

This guide explains how the Supermetrics Python SDK generates, filters, and wraps code from upstream OpenAPI specifications.

---

## 1. Overview of the Generation Pipeline

The SDK uses a multi-stage pipeline to generate type-safe client code from upstream OpenAPI specs:

```
┌─────────────────────────────────┐      ┌──────────────────────────────────────────────┐
│  openapi-specs/                 │      │  scripts/references/                         │
│  - openapi-data.yaml            │  +   │  sdk-endpoint-filters.yaml                   │
│  - openapi-management.yaml      │      │  (endpoint filters & component patches)      │
└────────────────┬────────────────┘      └──────────────────────┬───────────────────────┘
                 │                                              │
                 └──────────────────────┬───────────────────────┘
                                        │
                         python scripts/filter_openapi_spec.py
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │      openapi-spec.yaml       │
                         └──────────────┬───────────────┘
                                        │
                         scripts/regenerate_client.sh
                         (uv run openapi-python-client)
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │ src/supermetrics/_generated/ │
                         └──────────────┬───────────────┘
                                        │  (Adapter Pattern)
                                        ▼
                         ┌──────────────────────────────┐
                         │   src/supermetrics/          │
                         │   - resources/*.py           │
                         │   - client.py / async_client │
                         └──────────────────────────────┘
```

### Why This Architecture?

1. **Selective Inclusion:** The SDK only exposes vetted endpoints instead of the entire upstream API surface.
2. **Component & Endpoint Patching:** Fixes schema inconsistencies (such as nullable fields or customized descriptions) without modifying upstream specs directly.
3. **Adapter Pattern:** Isolates users from breaking changes in monthly OpenAPI regenerations by wrapping raw client calls in clean, high-level Python interfaces.

---

## 2. Step-by-Step Workflow

### Step 1: Place or Update Upstream OpenAPI Specifications

Place the upstream OpenAPI YAML files in the `openapi-specs/` directory (e.g., `openapi-specs/openapi-data.yaml`, `openapi-specs/openapi-management.yaml`).

> **Note:** `openapi-specs/*` is listed in `.gitignore` so local temporary specs can be tested without cluttering git.

### Step 2: Configure Endpoint Filters and Patches

Edit `scripts/references/sdk-endpoint-filters.yaml` to configure the endpoints and schema patches.

#### A. Include Endpoints

```yaml
endpoints:
  - method: GET
    path: /query/data/json
  - method: POST
    path: /management/connectors
```

#### A1. Pin Already-Shipped Endpoints (`pin_baseline`)

```yaml
pin_baseline: openapi-spec.yaml
```

With this set, any filtered endpoint already present in the committed merged spec is taken
**from that file** rather than re-read from `openapi-specs/`. Only genuinely new endpoints
come from upstream, which makes a regeneration purely **additive**.

This is not a nicety. The upstream specifications drift between publications, and the
generator turns some of that drift into breaking changes:

| Upstream drift | What it does to the SDK |
|---|---|
| An operation is retagged | The first tag *is* the generated API subpackage name, so the module moves and every adapter importing it fails |
| A path is reparameterised | `GET /query/data/json` became `GET /query/data/{context_type}`; the old module disappears |
| A shared schema is restructured | Regenerates a model that shipped adapters and their tests are written against |

Absorbing any of that as a side effect of adding one new domain is how a working SDK
becomes a broken one. Pinning makes each of those a deliberate, separately reviewable
change instead.

Components follow the same rule: for a name defined in both places, the baseline
definition wins, so shared schemas such as `ErrorResponse` stay byte-identical.

**To deliberately refresh a pinned endpoint**, delete its entry from `openapi-spec.yaml`,
or drop `pin_baseline` for a full upstream refresh — then expect to update the affected
adapters, and their tests, in the same change.

**The acceptance check** after any regeneration:

```bash
git status --porcelain src/supermetrics/_generated | grep -v '^??'
```

Only new (`??`) files should appear. Anything modified or deleted means drift got in.

#### A2. Rewrite an Endpoint's Path (`rewrite_path`)

```yaml
endpoints:
  - method: GET
    path: /v1/teams/{team_id}/transfers
    rewrite_path: /teams/{team_id}/transfers
```

The endpoint is *matched* upstream by `path` and *written* into the merged spec under
`rewrite_path`.

This exists because the upstream specs split a shared prefix inconsistently. Data
Warehouse transfers are declared as `/v1/teams/...` served from
`https://dts-api.supermetrics.com`, while backfills and data source connections are
`/teams/...` served from `https://dts-api.supermetrics.com/v1`. Both resolve to the same
URL, but `openapi-python-client` **ignores path-level `servers`** and simply concatenates
`base_url + path` — so under one base URL one of the two groups is always wrong, by a
duplicated or a missing `/v1`. Rewriting normalises them onto a single convention.

Two filter entries that would write to the same merged path is a hard error, so a rewrite
cannot silently shadow another endpoint.

> Rewriting a path changes the URL the generated client requests. Only use it to correct
> where the spec puts a prefix that the server also puts in `servers` — never to invent a
> route the API does not serve.

#### B. Endpoint Patches (Merge & Replace)

```yaml
endpoints:
  - method: POST
    path: /management/connectors
    patches:
      merge:
        description: "Create a custom connector"
        tags:
          - "Connectors"
```

#### C. Component Patches (Surgical Schema Overrides)

Use `component_patches` to modify shared schemas across all endpoints that reference them:

```yaml
component_patches:
  schemas:
    DataResponse:
      merge:
        properties:
          meta:
            properties:
              result:
                properties:
                  cache_time:
                    nullable: true
```

### Step 3: Merge and Filter the Specification

Run the filter script to produce the consolidated `openapi-spec.yaml`:

```bash
uv run python scripts/filter_openapi_spec.py
```

The script will:
- Discover all specs in `openapi-specs/`
- Match configured endpoints and apply patches
- Recursively resolve `$ref` dependencies and external file references
- Validate that all requested endpoints were found
- Write the merged output to `openapi-spec.yaml`

### Step 4: Regenerate the Low-Level Client

Run the regeneration script:

```bash
./scripts/regenerate_client.sh
```

Or run the generator command directly:

```bash
uv run openapi-python-client generate \
  --path openapi-spec.yaml \
  --output-path src/supermetrics/_generated \
  --config openapi-python-client-config.yaml

# Clean up redundant generated pyproject.toml
rm -f src/supermetrics/_generated/pyproject.toml
```

> **Warning:** Never hand-edit files in `src/supermetrics/_generated/`. Any changes will be overwritten on the next regeneration.

### Step 5: Implement or Update Resource Adapters

Create or update high-level resource adapters under `src/supermetrics/resources/`:

1. Import the generated models and API functions from `supermetrics._generated.supermetrics_api_client`.
2. Implement synchronous and asynchronous methods.
3. Map HTTP error responses using `src/supermetrics/resources/_error_handlers.py`.
4. Expose the resource on `SupermetricsClient` (`src/supermetrics/client.py`) and `SupermetricsAsyncClient` (`src/supermetrics/async_client.py`).

### Step 6: Verify and Test

Run tests and quality checks:

```bash
# Run tests
just test

# Run full QA suite (format, lint, typecheck, test)
just qa
```

---

## 3. Pull Request Examples

For real-world reference, see the following PRs in the repository:

- **[PR #25](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/25):** Migrated SDK to upstream OpenAPI specifications, resolved external `$ref` file dependencies in the filter script, and regenerated low-level clients.
- **[PR #34](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/34) & [PR #35](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/35):** Added Connector Builder resources (Connectors, Secrets, Logs), filtered upstream endpoints, regenerated generated models/APIs, and added resource adapters with comprehensive unit tests.

---

## 4. Troubleshooting & Best Practices

| Issue | Cause | Solution |
|---|---|---|
| `Missing endpoint` warning during filter | Endpoint path or HTTP method does not match spec | Check path syntax and casing in `sdk-endpoint-filters.yaml` |
| Unresolved `$ref` error | Schema references external file or missing definition | Ensure referenced spec files are present in `openapi-specs/` |
| Pydantic/typing errors on `None` values | API returns `null` for a non-nullable field in spec | Add a `component_patches` entry to set `nullable: true` |
| `pyproject.toml` generated inside `_generated/` | `openapi-python-client` creates standalone package by default | The script automatically removes it; ensure `rm -f src/supermetrics/_generated/pyproject.toml` runs |
