# PR: Add Connector Builder endpoint to SDK

> **Note:** CI tests will fail — this PR does not include `_generated/` code. Run `python scripts/filter_openapi_spec.py && ./scripts/regenerate_client.sh` after merge to generate the client.

## Summary

Add Connector Builder API support — connectors CRUD, secrets management, execution logs, and logo operations.

## Changes

### OpenAPI specs
- `openapi-specs/openapi-connector-builder.yaml` — new spec with 15 operations
- `openapi-specs/shared/schemas/domains/connector_builder/ConnectorBuilder.yaml` — shared domain schemas
- `scripts/references/sdk-endpoint-filters.yaml` — added 13 CB endpoints

### Filter script (`scripts/filter_openapi_spec.py`)
- Fix: bare `#/Name` refs from shared files rewritten to `#/components/schemas/Name`
- Fix: resolution cache updated after recursive resolution
- Fix: transitive schema dependencies collected via iterative second pass

### Resource adapters
- `connector_builder.py` — list, get, create, update, delete connectors + get/upload logo
- `connector_builder_logs.py` — list logs, get log detail
- `connector_builder_secrets.py` — list, create, update, delete secrets
- Uses `hasattr(response, "error")` instead of `isinstance(ErrorResponse)` to handle per-status error models

### Error handlers (`_error_handlers.py`)
- New `_raise_for_error_response()` — translates error response models into SDK exceptions
- Maps codes: `ACCESS_DENIED`, `INTERNAL_SERVER_ERROR`, `UNPROCESSABLE_ENTITY`, etc.

### Client registration
- `client.py`, `async_client.py`, `resources/__init__.py` — registered CB resources

### Tests
- `test_connector_builder.py` — 30 tests (sync + async)
- `test_connector_builder_logs.py` — 14 tests
- `test_connector_builder_secrets.py` — 18 tests
- `test_queries.py` — fixed `GetDataResponse400` constructor

### Example
- `examples/connector_builder_flow.py` — end-to-end flow with `--base-url` and `--team-id` flags

### Docs
- `README.md` — CB quick start section, updated feature list
- `HISTORY.md` — 0.3.0-beta1 entry
- `examples/README.md` — CB example usage

## Test plan
- [x] `ruff format` + `ruff check` + `mypy` — clean
- [x] 285 unit tests pass (after regeneration)
- [x] Manual test on dev: list, create, get, update, secrets CRUD, logs, logo get/upload, delete — all working
