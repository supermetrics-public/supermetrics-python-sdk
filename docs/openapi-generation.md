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
