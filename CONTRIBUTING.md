# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/supermetrics-public/supermetrics-python-sdk/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Supermetrics client for Python could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/supermetrics-public/supermetrics-python-sdk/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `supermetrics-python-sdk` for local development.

1. Fork the `supermetrics-python-sdk` repo on GitHub.
2. Clone your fork locally:

   ```sh
   git clone git@github.com:your_name_here/supermetrics-python-sdk.git
   ```

3. Install dependencies (requires [uv](https://docs.astral.sh/uv/getting-started/installation/)):

   ```sh
   cd supermetrics-python-sdk
   uv sync --extra dev
   ```

4. Create a branch for local development:

   ```sh
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass formatting, linting, and tests:

   ```sh
   just qa
   ```

   `just qa` covers everything the pull-request checks run. See
   [Running the Tests](#running-the-tests) for the individual suites, including the
   end-to-end tests and the optional live smoke tests.

6. Commit your changes and push your branch to GitHub:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

7. Submit a pull request through the GitHub website.

## Development Commands

This project uses [just](https://github.com/casey/just) as a command runner. Install it with:

```sh
# macOS
brew install just

# or via cargo
cargo install just
```

Available commands:

| Command | Description |
|---------|-------------|
| `just format` | Format code with ruff |
| `just lint` | Lint code with ruff (auto-fixes safe issues) |
| `just typecheck` | Run mypy type checking |
| `just test` | Run tests with pytest |
| `just e2e` | Run only the end-to-end transport tests |
| `just parity` | Verify strict sync/async API parity |
| `just live` | Run smoke tests against the real API (needs credentials) |
| `just qa` | Run all of the above (format + lint + typecheck + test) |
| `just testall` | Run tests across Python 3.11, 3.12, 3.13, and 3.14 |
| `just coverage` | Run tests with coverage and generate HTML report |
| `just build` | Build the package |
| `just clean` | Remove all build, test, and Python artifacts |

## Running the Tests

The suite has three layers. `just test` (and `just qa`) runs the first two; the third is
opt-in because it needs credentials.

### 1. Unit tests — `tests/unit/`

Fast and hermetic. They mock at the generated-client boundary and never open a socket.

```sh
just test tests/unit
```

### 2. End-to-end tests — `tests/e2e/`

These exercise the whole stack over a **real TCP socket**: the public client classes, the
resource adapters, the generated client, the `httpx` transport, the event hooks that apply
per-request authentication and header/timeout overrides, and the error translation layer.
Nothing is mocked or patched — the only substitution is the server on the other end, a
local `http.server.ThreadingHTTPServer` that serves scripted responses and records every
request it receives.

They need no credentials and no network access beyond loopback, so they run everywhere:

```sh
just e2e                      # all of them, verbose, with timings
just e2e -k concurrency       # just one area
just test tests/e2e           # quietly, as part of a wider run
```

Everything is marked `e2e`, so `-m e2e` selects them and `-m "not e2e"` skips them.

Writing one: take a fixture from `tests/e2e/conftest.py`. `api_server` gives you a bare
server you script yourself; `logins_server` comes pre-wired with the two login routes.

```python
def test_something(api_server: MockAPIServer) -> None:
    api_server.route("/ds/logins", ScriptedResponse(status=429, headers={"Retry-After": "30"}))

    with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
        with pytest.raises(SupermetricsRateLimitError) as exc_info:
            client.logins.list()

    assert exc_info.value.retry_after == 30
    assert api_server.last_request.bearer_token == "api_k"  # assert on what went out
```

`ScriptedResponse` takes `status`, `json_body`, `raw_body`, `headers` and `delay` — `delay`
is how the timeout tests get a genuinely slow endpoint. Pass several to `route()` to script
a sequence; the last one repeats.

### 3. Live smoke tests — `tests/e2e/test_live_smoke.py`

These call the real Supermetrics API. They **skip themselves** when no credentials are
present, so they never block a normal run or a pull request from a fork.

```sh
cp .env.example .env          # then put a real key in .env
just live
```

`.env` is gitignored — never commit a real credential. A real environment variable wins
over the file, so this works too:

```sh
SUPERMETRICS_API_KEY=api_... just live
```

Set `SUPERMETRICS_BASE_URL` to point them at a non-production environment.

### What CI runs

`.github/workflows/sdk-lint-test.yml` runs `lint`, `typecheck` (mypy strict), the unit and
e2e suites across Python 3.11–3.14, plus dedicated `e2e` and `parity` jobs so a failure in
either is visible on its own. `.github/workflows/sdk-e2e-live.yml` runs the live smoke
tests on a schedule, and self-skips when the repository has no `SUPERMETRICS_API_KEY`
secret configured.

`just qa` reproduces the pull-request checks locally; `just testall` adds the version matrix.

### Test expectations for a contribution

- Cover both the sync and the async path — a reflection test (`tests/test_api_parity.py`)
  fails the build if the two client surfaces drift apart in any way.
- Add an e2e test whenever a change touches authentication, headers, timeouts, retries, or
  error classification. Those behaviours only show up on the wire, and a unit test that
  mocks the transport cannot see them.
- Assert on what the server received (`api_server.last_request`), not only on what the
  client returned.

## OpenAPI Spec Workflow

The SDK wraps auto-generated API client code. The generated code lives in `src/supermetrics/_generated/`
and is committed to version control. Here is how the regeneration pipeline works:

1. **Source specs** (not in repo): Place the raw Supermetrics OpenAPI YAML files in `openapi-specs/`
   (this directory is gitignored — the source specs are internal to Supermetrics).

2. **Filter and merge**: Run `python scripts/filter_openapi_spec.py` to filter the source specs
   using `scripts/references/sdk-endpoint-filters.yaml` and produce a merged `openapi-spec.yaml`.

3. **Regenerate client**: Run `./scripts/regenerate_client.sh` to regenerate
   `src/supermetrics/_generated/` from `openapi-spec.yaml`.

4. **Review and test**: Review the generated diff and run `just qa` to verify nothing broke.

> **Note for external contributors:** You do not need the source specs to contribute.
> The generated code and `openapi-spec.yaml` are committed. Only Supermetrics maintainers
> run the regeneration pipeline when the upstream API changes.

For detailed documentation on the filter script and patch system, see `scripts/README.md`.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python 3.11, 3.12, 3.13 and 3.14. Tests run in GitHub Actions on every pull request to the main branch, make sure that the tests pass for all supported Python versions.

## Deploying

The release process is fully automated via GitHub Actions. To deploy a new version:

1. Create a new release from the GitHub UI:
   - Go to the repository's **Releases** page
   - Click **Draft a new release**
   - Create a new tag (e.g., `v1.2.3`) from the **main** branch - the version number is automatically derived from the tag
   - Add release notes describing the changes
   - Click **Publish release**

   **Important**: The tag must be created from the `main` branch for the release pipeline to succeed.

2. The release pipeline automatically triggers when the tag is pushed:
   - **Build**: Package is built using `uv build`
   - **TestPyPI**: Build artifacts are published to TestPyPI for verification
   - **PyPI**: If TestPyPI publish succeeds, the package is published to production PyPI

All publishing uses OIDC trusted publishing, so no manual token management is required.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
