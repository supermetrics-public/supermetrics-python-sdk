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
                         (uvx openapi-python-client, pinned)
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
`https://dts-api.supermetrics.com`, while backfills, data source connections and
destinations are `/teams/...` served from `https://dts-api.supermetrics.com/v1`. Both
resolve to the same URL, but `openapi-python-client` **ignores path-level `servers`**
and simply concatenates `base_url + path` — so under one base URL one of the two groups
is always wrong, by a duplicated or a missing `/v1`. Rewriting normalises them onto a
single convention.

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

Two things it does are load-bearing, and are the reason to use it rather than calling the
generator yourself:

**It generates into a staging directory and swaps only on success.** The committed tree at
`src/supermetrics/_generated/` is replaced *after* the generator has produced a complete
`supermetrics_api_client` package, not before. An earlier version deleted the tree first
and generated second, so any generator failure left the repository with no client at all.
If generation fails now, the script exits non-zero and the committed tree is untouched.
(The redundant `pyproject.toml` the generator emits is removed from the staging directory
before the swap.)

**It runs the generator on a pinned interpreter, outside the project virtualenv.**
`openapi-python-client` 0.29.0 pulls in a pydantic that raises `AssertionError` in
`_typing_extra.eval_type_backport` under Python 3.14 — which is this project's default
interpreter — so running the generator through `uv run` in the project environment fails
before it writes anything. The script instead invokes it with `uvx` on Python 3.12 in a
throwaway environment, at the version read out of the `openapi-python-client==` pin in
`pyproject.toml` so the generator and the dev dependency cannot drift. The interpreter
defaults to `3.12` and is overridable — `GENERATOR_PYTHON=3.13 ./scripts/regenerate_client.sh`
— should a future generator release need a different one.

Running the generator by hand is discouraged for both reasons above. If you must, mirror
what the script does — pin the interpreter and stage the output rather than pointing
`--output-path` at the committed tree:

```bash
# mktemp -d guarantees the parent directory exists. The generator calls
# `mkdir()` without `parents=True`, so pointing --output-path at a path whose
# parent is missing fails with FileNotFoundError before it writes anything.
STAGING="$(mktemp -d)"

uvx --python 3.12 --from "openapi-python-client==0.29.0" \
  openapi-python-client generate \
  --path openapi-spec.yaml \
  --output-path "$STAGING/_generated" \
  --config openapi-python-client-config.yaml

# The generated project scaffolding is not part of the SDK.
rm -f "$STAGING/_generated/pyproject.toml"

# Swap only once the generator has succeeded.
rm -rf src/supermetrics/_generated
mv "$STAGING/_generated" src/supermetrics/_generated
```

The version in the `--from` pin has to be kept in step with `pyproject.toml` by hand,
which is the other reason to prefer the script: it reads the pin instead.

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
- **[PR #61](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/61):** Phase 2 — Data Transfers and Transfer Runs. Introduced `pin_baseline` and `rewrite_path` in the filter script so a regeneration stays additive and the Data Warehouse families can share one base URL.
- **Phase 3 — Storage & Warehouse Destinations** (branch `feat/phase3-destinations`): added the seven `/teams/{team_id}/destinations*` endpoints to the filter config, regenerated purely additively on top of the pinned baseline, wrapped them in `src/supermetrics/resources/destinations.py`, and fixed `scripts/regenerate_client.sh` as described in Step 4.

---

## 4. Troubleshooting & Best Practices

| Issue | Cause | Solution |
|---|---|---|
| `Missing endpoint` warning during filter | Endpoint path or HTTP method does not match spec | Check path syntax and casing in `sdk-endpoint-filters.yaml` |
| Unresolved `$ref` error | Schema references external file or missing definition | Ensure referenced spec files are present in `openapi-specs/` |
| Pydantic/typing errors on `None` values | API returns `null` for a non-nullable field in spec | Add a `component_patches` entry to set `nullable: true` |
| `pyproject.toml` generated inside `_generated/` | `openapi-python-client` creates standalone package by default | The script removes it from the staging directory before the swap, so it never reaches `src/supermetrics/_generated/` |
| `AssertionError` in `_typing_extra.eval_type_backport` while generating | The pinned `openapi-python-client` pulls a pydantic that breaks under Python 3.14, the project's default interpreter | Use `./scripts/regenerate_client.sh`, which runs the generator on Python 3.12 through `uvx`; set `GENERATOR_PYTHON` to pick a different one |
| Generation failed and `src/supermetrics/_generated/` is gone | An older version of the script deleted the tree before generating | Restore it with `git checkout -- src/supermetrics/_generated`, then re-run the current script, which stages and swaps |

---

## 5. Downstream: Notifying the CLI

The SDK is the first consumer of the canonical specs; the `supermetrics-cli` chains through
it. The CLI does **not** read the raw canonical spec — it reads *this repo's* filtered,
production-ready `openapi-spec.yaml`, so the CLI and SDK always expose the same endpoint set.

When `openapi-spec.yaml` changes on `main` (i.e. a spec-update PR merges), the
`.github/workflows/notify-cli-on-spec-change.yml` workflow sends a cross-repo
`repository_dispatch` to the CLI:

```yaml
on:
  push:
    branches: [main]
    paths:
      - openapi-spec.yaml
  workflow_dispatch: # manual re-trigger for the initial backlog sync or recovery

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.CLI_DISPATCH_TOKEN }}
          repository: supermetrics-public/supermetrics-cli
          event-type: openapi-spec-updated
```

The CLI's own `spec-sync.yml` handler receives the `openapi-spec-updated` event, fetches
this repo's `openapi-spec.yaml`, regenerates its commands (`make generate`), and **opens a
PR** for human review. The automation never pushes to the CLI's `main` or auto-merges — a
person reviews and merges every CLI change.

A new endpoint appearing here does **not** automatically become a CLI command: the CLI
regenerates only the endpoints already listed in its `scripts/command-mapping.yaml`. Adding
a command is a deliberate, separate change in the CLI repo.

### The `CLI_DISPATCH_TOKEN` secret

The dispatch authenticates to the CLI repo with a repo-scoped GitHub PAT stored as the
`CLI_DISPATCH_TOKEN` secret in this repo's Actions secrets. The workflow's `GITHUB_TOKEN`
cannot reach another repository, so a PAT is required. To (re)create it: generate a
classic PAT with `repo` scope on `supermetrics-public/supermetrics-cli` (org admin needed),
store it in 1Password, then add it under **Settings → Secrets and variables → Actions**.

### Failure is visible

`repository-dispatch` exits non-zero if the dispatch call fails or the token is
missing/invalid, so the workflow run turns red in the Actions tab — no silent failure
leaves the CLI on a stale spec. Use the `workflow_dispatch` trigger to re-fire the dispatch
manually (e.g. the first large backlog sync) without a dummy spec commit.

---

## 6. CI: Spec Validation

`.github/workflows/sdk-spec-validation.yml` guards the generation pipeline. When a PR
touches any generation input — the raw upstream specs (`openapi-specs/`), the merged spec
(`openapi-spec.yaml`), the allowlist (`scripts/references/sdk-endpoint-filters.yaml`), the
pipeline scripts, or the generator config — CI re-runs the pipeline and fails if the
committed artifacts are out of sync — catching a forgotten regeneration, a regeneration from
stale specs, an allowlist edit that wasn't regenerated, or a hand-edited `openapi-spec.yaml`.
This is what spec-update PRs from upstream (the api-style-guide → SDK sync) are validated
against before a human reviews them.

The job does exactly what a developer does locally in **Step 3** and **Step 4**:

```yaml
- run: uv run python scripts/filter_openapi_spec.py   # regenerate openapi-spec.yaml
- run: ./scripts/regenerate_client.sh                 # regenerate src/supermetrics/_generated/
- run: |                                              # fail if either drifted from the commit
    CHANGES="$(git status --porcelain -- openapi-spec.yaml src/supermetrics/_generated/)"
    [ -z "$CHANGES" ] || { echo "$CHANGES"; exit 1; }
```

When it fails, the run prints the out-of-sync paths and the diff. The fix is always the same
— run the two scripts locally and commit the result:

```bash
uv run python scripts/filter_openapi_spec.py
./scripts/regenerate_client.sh
```

Key properties:

- **Validation only.** The job never pushes commits back to the PR. It reads and compares;
  the developer pushes the fix.
- **Safe unattended.** Both scripts are non-interactive and credential-free, and
  `pin_baseline` keeps regeneration additive-only (see **Step 2 → A1**), so a clean PR
  reproduces the committed artifacts byte-for-byte.
- **No duplicate test gate.** Lint, typecheck, and the hermetic test suite already run on
  every PR — including spec PRs — via `sdk-lint-test.yml` (which has no `paths` filter). This
  workflow adds only the drift check and does not re-run `just qa`.
- **Scoped trigger.** The `paths` filter means PRs that don't touch a generation input never
  start this job. (A bump of the `openapi-python-client` pin in `pyproject.toml` is
  deliberately *not* a trigger — it would fire on every unrelated dependency change; such a
  bump is instead caught by the next spec PR.)
