# AGENTS.md — AI Coding Guidelines

Guidelines and repository instructions for AI coding agents working on the Supermetrics Python SDK.

---

## 1. Operational Workspace Rules & `docs.local/`

All working plans, investigation notes, design documents, audit logs, scratchpads, and PR/code reviews MUST be kept in `docs.local/`.

- **Plans:** `docs.local/plans/`
- **Reports & Architecture Docs:** `docs.local/reports/`
- **Code Reviews & Audits:** `docs.local/reviews/`
- **Working Notes / Scratchpads:** `docs.local/scratchpads/`

`docs.local/` are ignored in `.gitignore`. Never commit transient planning or review files to the repository root.

---

## 2. Project Architecture & Patterns

- **Project:** Official Python SDK for Supermetrics (`supermetrics`).
- **Architecture Pattern:** Adapter Pattern + Resource-Based API + Dual Sync/Async Client.
- **Generated Code (`src/supermetrics/_generated/`):**
  - Auto-generated via `openapi-python-client` based on the Supermetrics OpenAPI specifications.
  - **Do NOT manually edit** code under `_generated/`. It is committed for transparency and offline development, but regenerated periodically.
- **Public API & Resource Adapters (`src/supermetrics/`):**
  - High-level, user-friendly, type-safe resource wrappers live in `src/supermetrics/resources/`.
  - Client entry points: `SupermetricsClient` (sync in `src/supermetrics/client.py`) and `SupermetricsAsyncClient` (async in `src/supermetrics/async_client.py`).
  - Exceptions & error handling: `src/supermetrics/exceptions.py` and `src/supermetrics/resources/_error_handlers.py`.

---

## 3. OpenAPI Code Generation

Detailed step-by-step documentation for updating specifications, filtering endpoints, and regenerating client code is available in:
📄 **[docs/openapi-generation.md](docs/openapi-generation.md)**

### Quick Regeneration Reference
1. Update upstream specs in `openapi-specs/` (e.g. `openapi-specs/openapi-data.yaml`, `openapi-specs/openapi-management.yaml`).
2. Update filters & component schema patches in `scripts/references/sdk-endpoint-filters.yaml`.
3. Filter and merge specs:
   ```bash
   uv run python scripts/filter_openapi_spec.py
   ```
4. Regenerate low-level client code:
   ```bash
   ./scripts/regenerate_client.sh
   ```
5. Wrap generated APIs with high-level resource adapters in `src/supermetrics/resources/`.
6. See PR references for past examples: [PR #25](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/25), [PR #34](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/34), and [PR #35](https://github.com/supermetrics-public/supermetrics-python-sdk/pull/35).

---

## 4. Toolchain & Environment

- **Python Version:** `>=3.11` (configured for Python 3.11, 3.12, 3.13, 3.14 support).
- **Package Manager:** `uv`
- **Build System:** `hatchling` with `versioningit`
- **Command Runner:** `just` (see `justfile` for command recipes)

### Common Commands

```bash
# Install dependencies
uv sync --extra dev

# Run QA suite (format, lint, typecheck, test)
just qa
# Or with uv directly:
uv run --extra dev ruff format .
uv run --extra dev ruff check . --fix
uv run --extra dev mypy src/supermetrics --ignore-missing-imports
uv run --extra dev pytest -m "not live"

# Run tests
just test
# Or with uv:
uv run --extra dev pytest -m "not live"

# Run test coverage
just coverage
```

> `addopts = "-q"` is set in `pyproject.toml`, and pytest sums verbosity flags, so a bare
> `-v` cancels out to the default. Pass `-o addopts=""` when you need readable output:
> `uv run --extra dev pytest tests/e2e -o addopts="" -v`.

---

## 4a. Running the Tests

The suite has four layers. `uv run --extra dev pytest -m "not live"` runs the first three
and is exactly what CI's matrix job runs; the fourth needs credentials and is opt-in.

| Layer | Location | Marker | Needs | What it proves |
|---|---|---|---|---|
| Unit | `tests/unit/` | — | nothing | Logic in isolation. Mocks at the generated-client boundary; opens no socket. |
| End-to-end | `tests/e2e/` | `e2e` | loopback only | The real stack over a real TCP socket. Nothing mocked. |
| Parity | `tests/test_api_parity.py` | — | nothing | Sync and async client surfaces are identical. |
| Live smoke | `tests/e2e/test_live_smoke.py` | `live` | real API key | The SDK works against production. Self-skips without a key. |

### The commands

```bash
# Everything CI runs on the matrix (unit + e2e + parity), all Python versions' worth
uv run --extra dev pytest -m "not live"
just test                      # same thing
just qa                        # format + lint + typecheck + the above

# One layer at a time
uv run --extra dev pytest tests/unit                       # unit only
just e2e                                                   # e2e only, verbose, with timings
just parity                                                # sync/async parity only
just live                                                  # live smoke (needs credentials)

# By marker
uv run --extra dev pytest -m e2e                           # only end-to-end
uv run --extra dev pytest -m "not e2e and not live"        # only the fast hermetic tests
uv run --extra dev pytest -m live                          # only live (skips without a key)

# Narrowing down
uv run --extra dev pytest -k concurrency                   # by name substring
uv run --extra dev pytest tests/e2e/test_auth_e2e.py       # one file
uv run --extra dev pytest tests/unit/test_auth.py::TestFormatAuthorization -o addopts="" -v

# Coverage and the version matrix
just coverage                                              # HTML report in htmlcov/
uv run --extra dev pytest -m "not live" --cov=supermetrics --cov-report=term-missing
just testall                                               # Python 3.11, 3.12, 3.13, 3.14
uv run --python=3.14 --extra dev pytest -m "not live"      # one specific version
```

> **Verbosity gotcha.** `addopts = "-q"` is set in `pyproject.toml` and pytest *sums*
> verbosity flags, so a bare `-v` cancels out to the default and prints nothing extra.
> Pass `-o addopts=""` whenever you need readable output:
> `uv run --extra dev pytest tests/e2e -o addopts="" -v`.

### End-to-end tests — read this before touching the transport

**Run `just e2e` before claiming any change to authentication, headers, timeouts, retries,
or error handling works.** Those behaviours only exist on the wire; a unit test that mocks
the transport cannot observe them, and the unit suite will happily stay green while the SDK
sends the wrong `Authorization` header.

`tests/e2e/` drives the whole stack over a **real loopback TCP socket** — public clients,
resource adapters, generated client, `httpx` transport, the event hooks that apply
per-request auth and header/timeout overrides, and error translation. Nothing is mocked;
the only substitution is the server, a stdlib `ThreadingHTTPServer` that serves scripted
responses and records every request. No credentials, no external network, no extra
dependencies.

Writing one — fixtures live in `tests/e2e/conftest.py`. `api_server` is a bare server you
script; `logins_server` is pre-wired with the login routes:

```python
def test_something(api_server: MockAPIServer) -> None:
    api_server.route("/ds/logins", ScriptedResponse(status=429, headers={"Retry-After": "30"}))

    with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            client.logins.list()

    assert exc_info.value.retry_after == 30
    assert api_server.last_request.bearer_token == "api_k"  # assert on what went OUT
```

`ScriptedResponse` takes `status`, `json_body`, `raw_body`, `headers`, `delay`. Use `delay`
to make a genuinely slow endpoint for timeout tests. Pass several responses to `route()`
for a sequence; the last repeats. **Always assert on `api_server.last_request` /
`.requests`, not only on the client's return value** — that is the whole point of this
layer.

### Live API tests (opt-in, real credentials)

`tests/e2e/test_live_smoke.py` calls the production API and **skips itself** when no key is
present, so it never blocks a normal run or a fork's pull request.

```bash
cp .env.example .env      # put a real key in .env, which is gitignored
just live
# or, without a file:
SUPERMETRICS_API_KEY=api_... just live
```

`tests/conftest.py` loads `.env` automatically; a real environment variable overrides it.
`SUPERMETRICS_BASE_URL` targets a non-production environment.

**Never commit `.env`, never paste a credential into a file that is not gitignored, and
never echo one into a commit message, a PR body, or test output.**

### What CI runs

`.github/workflows/sdk-lint-test.yml`: `lint`, `typecheck` (mypy strict), `test` (unit +
e2e + parity across Python 3.11–3.14), plus dedicated `e2e` and `parity` jobs so a failure
in either is visible on its own. `.github/workflows/sdk-e2e-live.yml` runs the live smoke
tests on a schedule and self-skips without a configured secret.

### Definition of done

1. `uv run --extra dev ruff format .` and `ruff check .` clean
2. `uv run --extra dev mypy src/supermetrics --ignore-missing-imports` clean
3. `uv run --extra dev pytest -m "not live"` green
4. `just e2e` green, with a new e2e case covering any behaviour you changed on the wire
5. `just parity` green — sync and async surfaces must stay identical

---

## 5. Coding & Agent Standards

1. **Verify First:**
   - Gather context before proposing changes: inspect code with file reading/searching tools.
   - Trace imports, schemas, and resource adapters across `src/supermetrics/`.
2. **Atomic & Clean Edits:**
   - Use targeted find-and-replace edits.
   - Do not reformat unrelated files or introduce drive-by refactorings.
3. **Strict Typing & Type Hints:**
   - All public interfaces, methods, and adapters must have full Python type annotations.
   - Respect Pydantic v2 schemas and models.
4. **Testing Requirements:**
   - Unit tests live under `tests/unit/`; end-to-end tests under `tests/e2e/`. See
     [section 4a](#4a-running-the-end-to-end-tests).
   - Test both sync and async paths when adding or modifying resource methods. The
     reflection test `tests/test_api_parity.py` fails the build if the two surfaces drift.
   - Use `httpx.MockTransport` when a unit test needs a request pipeline. Note that the
     transport event hooks live on the *client*, so `MockTransport` still exercises
     authentication, header merging, and timeout overrides.
   - Anything touching auth, headers, timeouts, retries, or error classification needs an
     e2e test as well: those behaviours only exist on the wire.
5. **Finishing the Job:**
   - Always run the relevant test suite and linters (`pytest`, `ruff`, `mypy`) before considering a task complete.
