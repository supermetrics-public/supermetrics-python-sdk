# Supermetrics client for Python.

![PyPI version](https://img.shields.io/pypi/v/supermetrics.svg)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://supermetrics-public.github.io/supermetrics-python-sdk/)

Official Python client for Supermetrics

* PyPI package: https://pypi.org/project/supermetrics/
* Free software: Apache License v2

## Features

* Type-safe Python client generated from OpenAPI specification
* Dual sync/async support via separate Client classes
* Fully typed request and response models, generated from the spec as `attrs` classes
* Comprehensive API coverage: login links (including update), logins (including account
  listing and revocation), accounts, queries, DWH transfers and transfer runs, DWH
  destinations, DWH backfills, custom fields, data blending, account tags, Connector Builder
* Custom exception hierarchy with HTTP status code mapping
* Resource-based API organization
* API key, OAuth bearer token, and dynamic token provider authentication
* Per-request authorization, header, and timeout overrides on a shared connection pool
* `with_raw_response` access to HTTP status codes, headers, and raw payloads
* Automatic routing of Data Warehouse calls to their own host, from one pooled client

## Quick Start

### Installation

```bash
pip install supermetrics
```

### Basic Usage

```python
from supermetrics import SupermetricsClient

# Initialize client
client = SupermetricsClient(api_key="your_api_key")

# Create login link for data source authentication
link = client.login_links.create(ds_id="GAWA", description="My Analytics Authentication")

# Get login details after user authenticates
login = client.logins.get(login_id=link.login_id)

# List available accounts
accounts = client.accounts.list(ds_id="GAWA", login_usernames=login.username)

# Execute query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=[accounts[0].account_id],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-07",
)

print(f"Retrieved {len(result.data)} rows")
```

### Logins & Login Links

A login link starts the OAuth flow; once someone completes it a login exists, and that login
can reach a set of data source accounts. Beyond `create`, `get`, `list` and `close`, the SDK
lists a login's accounts, revokes a login, and updates a link's description.

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# The accounts a login can reach. Paginated: offset and limit are always sent (0 and 100 by
# default), and the total rides in meta on the raw response, not in the returned list.
accounts = client.logins.get_accounts("login_abc123", offset=0, limit=100)
for account in accounts:
    print(account.account_id, account.name, account.group)

response = client.with_raw_response.logins.get_accounts("login_abc123")
print(response.json_body["meta"]["paginate"]["total"])

# update() changes only the description — a link's data source, expiry and redirect are
# fixed at creation, so those are set through create(), not here.
link = client.login_links.update("link_123", "Q4 Analytics setup")
print(link.description)  # "Q4 Analytics setup"

# revoke() is a DELETE that answers 200 with a bool, not an empty 204. True means the
# login's OAuth credentials were invalidated; bind a fresh login to restore access.
print(client.logins.revoke("login_abc123"))  # True
```

### Account Tags

An account tag groups data source accounts from across a team's connections under one
reusable label. A tag is addressed by `name`, the slug the server assigns it; the label
you choose is `display_name`.

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# create() takes no name — the server assigns the slug and hands it back.
tag = client.account_tags.create(
    team_id=12345,
    display_name="EMEA paid media",
    color="#112233",
    data_sources=[{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}],
)
print(tag.name)  # "a1b2c3d" — what every later call addresses this tag by

# list() summarises membership as counts; get() returns the membership itself.
for overview in client.account_tags.list(team_id=12345):
    print(overview.display_name, overview.data_source_count, overview.account_count)

detail = client.account_tags.get(team_id=12345, name=tag.name)
print([selection["data_source_id"] for selection in detail.data_sources])

# update() renames and recolours, and does nothing else. Both fields are required, and
# it cannot move accounts — that is what add_accounts() and remove_accounts() are for.
client.account_tags.update(team_id=12345, name=tag.name, display_name="EMEA paid", color="#445566")

client.account_tags.add_accounts(
    team_id=12345,
    name=tag.name,
    data_sources=[{"data_source_id": "FB", "accounts": [{"account_id": "act_99"}]}],
)

# delete() returns a bool, not None: deletion is idempotent upstream, so deleting a tag
# that is already gone is a success answering False rather than a 404. No operation in
# this domain answers 404 at all.
print(client.account_tags.delete(team_id=12345, name=tag.name))  # True
print(client.account_tags.delete(team_id=12345, name=tag.name))  # False
```

### Connector Builder

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# List connectors
connectors = client.connector_builder.list(team_id=12345)

# Create a connector
created = client.connector_builder.create(
    team_id=12345, title="My Custom Connector", description="Fetches data from a custom API"
)
connector_id = created.connector_identifier

# Manage secrets
client.connector_builder_secrets.create(
    team_id=12345, connector_identifier=connector_id, secret_name="api_key", secret_value="sk-secret-value"
)

# View execution logs
logs = client.connector_builder_logs.list(team_id=12345, connector_identifier=connector_id)
```

### Custom Fields

Custom fields are calculated dimensions and metrics defined per team. Each carries a
`definition`: an ordered pipeline of function, lookup, and condition steps.

```python
from supermetrics import DefinitionValue, FunctionArgument, FunctionStep, SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# Discover which functions, rules, and data types the team is allowed to use
metadata = client.custom_fields.get_metadata(team_id=12345)
print([function.name for function in metadata.functions.items])

# Create a one-step field. field_type is "dim" or "met" and is fixed at creation.
field = client.custom_fields.create(
    team_id=12345,
    display_name="Platform (upper)",
    field_type="dim",
    data_type="string.text.value",
    definition=[
        FunctionStep(
            type_="function",
            name="upper_case",
            arguments=[
                FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))
            ],
        )
    ],
)

# Read-modify-write. The definition comes back wrapped and is sent bare, so a round
# trip reads `.definition.items`. update() takes no field_type and replaces the whole
# object — anything you omit reverts to unset.
current = client.custom_fields.get(team_id=12345, custom_field_id=field.id)
client.custom_fields.update(
    team_id=12345,
    custom_field_id=field.id,
    display_name="Platform (upper), revised",
    data_type=current.data_type,
    definition=current.definition.items,
    description=current.description,
)

# list() returns the page only; the pagination rides in `meta` on the raw response,
# and total_count appears only when you ask for it.
response = client.with_raw_response.custom_fields.list(team_id=12345, include_total_count=True)
print(f"{len(response.data)} of {response.json_body['meta']['pagination']['total_count']} fields")

client.custom_fields.delete(team_id=12345, custom_field_id=field.id)
```

### Data Blending

A blend combines several data sources into one queryable table — `"union"` stacks their
rows, `"join"` joins them on shared fields. Sources being created have no id yet, so each
is named by a temporary eight-character `blend_data_source_key` that the field and join
references point at.

```python
from supermetrics import (
    BlendConfig,
    BlendDatasourceFieldRef,
    BlendedDataSourceInput,
    BlendField,
    SupermetricsClient,
)

client = SupermetricsClient(api_key="your_api_key")

# All five of these arguments are required, even though three are usually empty:
# upstream marks them required-but-nullable.
source = BlendedDataSourceInput(
    data_source_id="GA4",
    blend_data_source_id=None,
    blend_data_source_key="abcd1234",
    report_type=None,
    report_type_settings=[],
    display_name="Google Analytics 4",
)

# Collections go out as bare lists. They come back wrapped in `.items` — at every level.
config = BlendConfig(
    fields=[
        BlendField(
            blend_field_name="impressions",
            blend_field_display_name="Impressions",
            blend_datasource_fields=[
                BlendDatasourceFieldRef(
                    blend_data_source_key="abcd1234",
                    datasource_field_name="Impressions",
                    field_source="standard",
                )
            ],
        )
    ],
)

# create() answers 201 and assigns the ids. blend_type is fixed here and forever.
blend = client.blends.create(
    team_id=12345,
    display_name="GA4 impressions",
    blend_type="union",
    blended_data_sources=[source],
    config=config,
)
print(blend.blend_id, blend.type_)

# list() returns summaries: no config, and a reduced source shape. This endpoint is not
# paginated, so one call returns every matching blend.
for summary in client.blends.list(team_id=12345, blend_type="union"):
    print(summary.blend_id, summary.display_name)

# A read-modify-write has to rebuild the request objects: the response wraps its
# collections and drops blend_data_source_key, so it cannot be resent as-is. Existing
# sources are addressed by blend_data_source_id from here on. update() takes no
# blend_type and replaces the whole object: the required fields are resent in full, so a
# source or field you leave out is dropped.
current = client.blends.get(team_id=12345, blend_id=blend.blend_id)
existing = BlendedDataSourceInput(
    data_source_id=current.blended_data_sources.items[0].data_source_id,
    blend_data_source_id=current.blended_data_sources.items[0].blend_data_source_id,
    blend_data_source_key=None,
    report_type=None,
    report_type_settings=[],
)
client.blends.update(
    team_id=12345,
    blend_id=blend.blend_id,
    display_name="GA4 impressions, revised",
    blended_data_sources=[existing],
    config=BlendConfig(
        fields=[
            BlendField(
                blend_field_name="impressions",
                blend_field_display_name="Impressions",
                blend_datasource_fields=[
                    BlendDatasourceFieldRef(
                        blend_data_source_id=existing.blend_data_source_id,
                        datasource_field_name="Impressions",
                        field_source="standard",
                    )
                ],
            )
        ],
    ),
)

client.blends.delete(team_id=12345, blend_id=blend.blend_id)
```

### Data Warehouse Transfers

Transfers, transfer runs and backfills are served by the Data Warehouse API on a separate
host. The SDK routes them there automatically, so an ordinary client reaches everything.

```python
from datetime import UTC, datetime

from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# List transfers for a team
for transfer in client.transfers.list(team_id=12345):
    print(f"{transfer.dwh_transfer_id}: {transfer.display_name} ({transfer.state})")

# Inspect one transfer's configuration
transfer = client.transfers.get(team_id=12345, transfer_id=36091)
print(f"Schedule: {transfer.schedule}")

# Dry-run a configuration before creating it. An invalid configuration comes back
# as a result, not an exception — that is the point of a validation endpoint.
from supermetrics._generated.supermetrics_api_client.models.transfer_account import TransferAccount
from supermetrics._generated.supermetrics_api_client.models.transfer_schedule import TransferSchedule

schedule = [TransferSchedule(run_interval="daily", run_hour=4)]
accounts = [TransferAccount(data_source_username="ads@example.com", login_id=1, account_id="8733197711")]

result = client.transfers.validate(
    team_id=12345,
    data_source_id="AW",
    schema_id=99999,
    destination_id=8,
    display_name="Google Ads to BigQuery",
    schedule=schedule,
    accounts=accounts,
)
if not result.is_valid:
    for error in result.errors:
        print(f"{error.field_id}: {error.error_code}")

# Pause and resume. The API's vocabulary is "pause" / "unpause".
client.transfers.set_state(team_id=12345, transfer_id=36091, state="pause")

# Run history for a transfer, and the detail of one run
runs = client.transfers.list_runs(
    team_id=12345,
    transfer_id=36091,
    start_date=datetime(2026, 1, 1, tzinfo=UTC),
    end_date=datetime(2026, 1, 31, tzinfo=UTC),
)
for run in runs:
    print(f"Run {run.id}: {run.status} ({run.total_rows} rows)")

run = client.transfer_runs.get(team_id=12345, transfer_run_id=12345)
for query in run.query_details:
    print(f"  query: {query.status}, {query.rows} rows")
```

### Data Warehouse Destinations

Destinations are the warehouses and buckets transfers write into. They live on the same
Data Warehouse host as transfers, and the same client reaches them.

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# What the team already has
for destination in client.destinations.list(team_id=12345):
    print(f"{destination.id}: {destination.display_name} ({destination.type_})")

# Credentials are a plain dict — there is no request model to import, because the
# generated *Fields classes cannot be constructed. Keys depend on the type.
fields = {
    "hostname": "any-domain.my-region.snowflakecomputing.com",
    "warehouse": "DEMO_WH",
    "database_name": "TEST_DB",
    "schema": "PUBLIC",
    "role": "ACCOUNTADMIN",
    "username": "USER",
    "private_key": "not-a-real-key",
}

# Try the credentials before committing to them. A connection that does not work is a
# returned result with success=False, not an exception.
result = client.destinations.test_connection(
    team_id=12345,
    type="DWH_SNOWFLAKE",
    display_name="Snowflake (prod)",
    fields=fields,
    auth_method="AUTH_METHOD_KEY_PAIR",
)
if not result.success:
    raise RuntimeError(f"Connection failed: {result.error}")

destination = client.destinations.create(
    team_id=12345,
    type="DWH_SNOWFLAKE",
    display_name="Snowflake (prod)",
    fields=fields,
    auth_method="AUTH_METHOD_KEY_PAIR",
)
print(f"Created destination {destination.id}")

# get() answers with edit_settings, a list of UI form descriptors — not the flat fields
# dict create() and update() take. The read shape and the write shape differ.
stored = client.destinations.get(team_id=12345, destination_id=8)
for setting in stored.edit_settings:
    print(f"  {setting.id} ({setting.input_type}): {setting.value}")

# Check what still depends on a destination before removing it
usage = client.destinations.get_usage(team_id=12345, destination_id=8)
if usage.is_used:
    for transfer in usage.transfers:
        print(f"still used by {transfer.transfer_id}: {transfer.transfer_name}")
else:
    client.destinations.delete(team_id=12345, destination_id=8)
```

### Data Warehouse Backfills

```python
from supermetrics import SupermetricsClient

# Initialize client
client = SupermetricsClient(api_key="your_api_key")

# Create a backfill for historical data
backfill = client.backfills.create(team_id=12345, transfer_id=456789, range_start="2024-01-01", range_end="2024-01-31")

print(f"Backfill created: {backfill.transfer_backfill_id}")
print(f"Status: {backfill.status}")

# Get the latest backfill for a transfer
latest = client.backfills.get_latest(team_id=12345, transfer_id=456789)
print(f"Latest backfill status: {latest.status}")
print(f"Progress: {latest.transfer_runs_completed}/{latest.transfer_runs_total}")

# List all incomplete backfills for a team
backfills = client.backfills.list_incomplete(team_id=12345)
for bf in backfills:
    print(f"Backfill {bf.transfer_backfill_id}: {bf.status}")

# Cancel a backfill
cancelled = client.backfills.cancel(team_id=12345, backfill_id=67890)
print(f"Backfill cancelled: {cancelled.status}")
```

## Authentication

The client accepts exactly one of `api_key`, `bearer_token`, or `token_provider`:

```python
from supermetrics import SupermetricsAsyncClient, SupermetricsClient

# Static API key
client = SupermetricsClient(api_key="api_live_abc123")

# OAuth access token
client = SupermetricsClient(bearer_token="otok_abc123")


# Dynamic provider, re-evaluated on every request so short-lived tokens can be
# refreshed without discarding the connection pool
async def get_valid_token() -> str:
    return await oauth_service.get_access_token(team_id=123)


client = SupermetricsAsyncClient(token_provider=get_valid_token)
```

Every resource method takes per-request `auth_token`, `headers`, and `timeout` overrides,
so one shared client can serve concurrent callers that each bring their own credential and
tracing context:

```python
sync_client = SupermetricsClient(api_key="api_live_abc123")

login = sync_client.logins.get(
    "login_abc123",
    auth_token="otok_this_caller",
    headers={"X-Span-Id": "a8f3b2c9", "Idempotency-Key": "req-42"},
    timeout=120.0,
)
```

Use `with_raw_response` when you need the HTTP status, headers, or raw payload alongside
the parsed model:

```python
response = sync_client.with_raw_response.logins.get("login_abc123")
print(response.status_code, response.span_id, response.retry_after)
print(response.data.username)
```

See [Authentication & Transport](docs/authentication-and-transport.md) for the full guide.

## Examples

See the [examples/](./examples/) directory for complete working examples:

- `complete_flow.py` - Full sync workflow from authentication to query execution
- `async_flow.py` - Async version of complete workflow
- `connector_builder_flow.py` - Connector Builder end-to-end operations (supports `--base-url` for local dev)

See [examples/README.md](./examples/README.md) for setup and running instructions.

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from supermetrics import (
    APIError,
    NetworkError,
    SupermetricsAuthError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsValidationError,
    SupermetricsClient,
)

client = SupermetricsClient(api_key="your_key")

try:
    link = client.login_links.create(ds_id="GAWA", description="Test")
except SupermetricsAuthError as e:
    # e.error_code carries the upstream OAuth code, e.g. ACCESS_TOKEN_INVALID
    print(f"Credential rejected ({e.error_code}): {e.message}")
except SupermetricsValidationError as e:
    print(f"Invalid parameters: {e.message}")
except SupermetricsNotFoundError as e:
    print(f"Not found: {e.message}")
except SupermetricsRateLimitError as e:
    print(f"Throttled; retry after {e.retry_after}s")
except APIError as e:
    # Any other HTTP error. Carries status_code, headers, error_code and details.
    print(f"API error {e.status_code}: {e.message}")
except NetworkError as e:
    print(f"Network error: {e.message}")
```

`AuthenticationError` and `ValidationError` remain available as aliases of
`SupermetricsAuthError` and `SupermetricsValidationError`, and every HTTP error is a
subclass of `APIError`.

## Documentation

- [Authentication & Transport](docs/authentication-and-transport.md) - Credentials, per-request overrides, response metadata, error taxonomy
- [Examples](./examples/) - Working code examples
- [Scripts](./scripts/README.md) - OpenAPI filtering, patching, and SDK generation

## OpenAPI Client Regeneration

The SDK client is auto-generated from the Supermetrics OpenAPI specification.

### Source Specifications

- **Location:** `openapi-specs/` directory (contains `openapi-data.yaml`, `openapi-managment.yaml`, `openapi-team.yaml`, `openapi-connector-builder.yaml`)
- **Merged Spec:** `openapi-spec.yaml` (project root) - filtered, patched, and merged from source specs
- **Configuration:** `scripts/references/sdk-endpoint-filters.yaml` - controls which endpoints are included and applies patches/customizations
- **Documentation:** See [scripts/README.md](./scripts/README.md) for detailed patch system documentation

### SDK Endpoint Filtering and Customization

The SDK uses a configuration-driven process to create a focused, customizable client from multiple OpenAPI specifications.

#### `scripts/references/sdk-endpoint-filters.yaml` - Endpoint Configuration

This YAML file defines which API endpoints to include in the SDK and allows you to apply patches/customizations to both endpoints and shared components.

**Key Features:**
- **Endpoint Filtering:** Include only the endpoints your application needs
- **Endpoint Patches:** Customize individual endpoint definitions (descriptions, parameters, responses, etc.)
- **Component Patches:** Apply surgical modifications to shared schemas, responses, and other components
- **Merge & Replace Strategies:** Deep merge or complete replacement of OpenAPI sections

**Basic Example:**
```yaml
endpoints:
  - method: GET
    path: /ds/logins

  - method: GET
    path: /query/data/json

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

**For detailed documentation** on the configuration format, patch strategies, and comprehensive examples, see [scripts/README.md](./scripts/README.md).

#### `scripts/filter_openapi_spec.py` - Specification Filter, Patcher, and Merger

This Python script processes multiple OpenAPI specifications, applies customizations, and creates a single `openapi-spec.yaml` file.

**What it does:**
1. Reads configuration from `scripts/references/sdk-endpoint-filters.yaml`
2. Scans and loads all `.yaml`/`.yml` files from `openapi-specs/` directory
3. Filters endpoints based on configuration
4. Applies endpoint patches (merge/replace operations)
5. Collects all referenced components via `$ref` traversal (dependency resolution)
6. Resolves external file references
7. Applies component patches to shared schemas, responses, etc.
8. Detects and fails on duplicate `METHOD|PATH` across specs
9. Merges everything into single specification
10. Validates all requested endpoints were found

**Usage:**
```bash
python scripts/filter_openapi_spec.py
```

**Configuration:**
- Input: `openapi-specs/*.yaml` and `scripts/references/sdk-endpoint-filters.yaml`
- Output: `openapi-spec.yaml`

**Exit codes:**
- `0` - Success
- `1` - Error (missing files, duplicates, or validation failure)

**For detailed documentation** on patch strategies, troubleshooting, and examples, see [scripts/README.md](./scripts/README.md).

### How to Regenerate

**Full Regeneration (recommended):**
```bash
# 1. Update source specs in openapi-specs/ if needed
# 2. Update scripts/references/sdk-endpoint-filters.yaml to add/remove endpoints or apply patches
# 3. Run filter script to regenerate merged spec
python scripts/filter_openapi_spec.py

# 4. Regenerate SDK from merged spec
./scripts/regenerate_client.sh
```

**Quick Regeneration (if openapi-spec.yaml unchanged):**
```bash
./scripts/regenerate_client.sh
```

`regenerate_client.sh` generates into a staging directory and replaces
`src/supermetrics/_generated/` only once generation has succeeded, so a failed run leaves
the committed client untouched. It runs the generator through `uvx` on a pinned Python
3.12 — `openapi-python-client` cannot run on this project's default 3.14 interpreter —
at the version read out of `pyproject.toml`. Set `GENERATOR_PYTHON` to override. See
[docs/openapi-generation.md](docs/openapi-generation.md#step-4-regenerate-the-low-level-client).

### When to Regenerate

- Monthly (or when Supermetrics API changes)
- After updating source specs in `openapi-specs/`
- After modifying `scripts/references/sdk-endpoint-filters.yaml` (adding/removing endpoints or changing patches)

### Adding/Removing Endpoints or Applying Patches

1. Edit `scripts/references/sdk-endpoint-filters.yaml`:
   - Add/remove endpoints in the `endpoints` list
   - Add/modify patches in `component_patches` or endpoint-level `patches`
2. Run `python scripts/filter_openapi_spec.py` to regenerate the merged spec
3. Run `./scripts/regenerate_client.sh` to regenerate the SDK client

**See [scripts/README.md](./scripts/README.md)** for detailed documentation on:
- Configuration file format
- Endpoint and component patch strategies
- Comprehensive examples
- Troubleshooting guide

**Note:** The adapter pattern (implemented in Story 1.3+) protects users from breaking changes during regeneration

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to contribute, run tests, and deploy releases.

> **Note:** Every pull request must include an update to [HISTORY.md](./HISTORY.md) describing the change under the relevant version section.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
