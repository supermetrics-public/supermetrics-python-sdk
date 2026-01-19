# Supermetrics client for Python.

![PyPI version](https://img.shields.io/pypi/v/supermetrics.svg)
[![Documentation Status](https://readthedocs.org/projects/supermetrics/badge/?version=latest)](https://supermetrics.readthedocs.io/en/latest/?version=latest)

Official Python client for Supermetrics

* PyPI package: https://pypi.org/project/supermetrics/
* Free software: Apache License v2
* Documentation: https://supermetrics.readthedocs.io.

## Features

* Type-safe Python client generated from OpenAPI specification
* Dual sync/async support via separate Client classes
* Pydantic v2 models for request/response validation
* Comprehensive API coverage: login links, logins, accounts, queries
* Custom exception hierarchy with HTTP status code mapping
* Resource-based API organization

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
link = client.login_links.create(
    ds_id="GAWA",
    description="My Analytics Authentication"
)

# Get login details after user authenticates
login = client.logins.get(login_id=link.login_id)

# List available accounts
accounts = client.accounts.list(
    ds_id="GAWA",
    login_usernames=login.username
)

# Execute query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=[accounts[0].account_id],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-07"
)

print(f"Retrieved {len(result.data)} rows")
```

## Examples

See the [examples/](./examples/) directory for complete working examples:

- `complete_flow.py` - Full sync workflow from authentication to query execution
- `async_flow.py` - Async version of complete workflow

See [examples/README.md](./examples/README.md) for setup and running instructions.

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from supermetrics import (
    SupermetricsClient,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError,
)

client = SupermetricsClient(api_key="your_key")

try:
    link = client.login_links.create(ds_id="GAWA", description="Test")
except AuthenticationError as e:
    print(f"Invalid API key: {e.message}")
except ValidationError as e:
    print(f"Invalid parameters: {e.message}")
except APIError as e:
    print(f"API error: {e.message}")
except NetworkError as e:
    print(f"Network error: {e.message}")
```

## Documentation

- [Examples](./examples/) - Working code examples
- [Scripts](./scripts/README.md) - OpenAPI filtering, patching, and SDK generation

## OpenAPI Client Regeneration

The SDK client is auto-generated from the Supermetrics OpenAPI specification.

### Source Specifications

- **Location:** `openapi-specs/` directory (contains `openapi-data.yaml` and `openapi-management.yaml`)
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

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
