# Supermetrics client for Python.

![PyPI version](https://img.shields.io/pypi/v/supermetrics.svg)
[![Documentation Status](https://readthedocs.org/projects/supermetrics/badge/?version=latest)](https://supermetrics.readthedocs.io/en/latest/?version=latest)

Official Python client for Supermetrics

* PyPI package: https://pypi.org/project/supermetrics/
* Free software: Apache License v2
* Documentation: https://supermetrics.readthedocs.io.

## Features

* Type-safe Python client generated from OpenAPI specification
* Dual sync/async support via single Client class
* Pydantic v2 models for request/response validation
* Comprehensive API coverage: login links, logins, accounts, queries

## OpenAPI Client Regeneration

The SDK client is auto-generated from the Supermetrics OpenAPI specification.

### Source Specifications

- **Location:** `openapi-specs/` directory (contains `openapi-data.yaml` and `openapi-management.yaml`)
- **Merged Spec:** `openapi-spec.yaml` (project root) - filtered and merged from source specs
- **Endpoint Filter:** `sdk-endpoints.txt` - controls which endpoints are included in the SDK

### SDK Endpoint Filtering

The SDK uses a two-step process to create a focused, maintainable client from multiple OpenAPI specifications:

#### `sdk-endpoints.txt` - Endpoint Inclusion List

This file defines which API endpoints to include in the generated SDK. Use it to create a focused SDK that includes only the endpoints your application needs.

**Format:**
```
METHOD|PATH
```

**Example:**
```
GET|/ds/logins
POST|/ds/login/link
GET|/query/data/json
```

**Rules:**
- One endpoint per line
- Use `METHOD|PATH` format (pipe-separated)
- METHOD must be uppercase (GET, POST, PUT, PATCH, DELETE)
- PATH must match exactly as defined in the OpenAPI specs
- Lines starting with `#` are comments
- Empty lines are ignored

**Purpose:**
- Controls SDK size by including only needed endpoints
- Maintains a clear list of supported operations
- Simplifies SDK updates when API changes

#### `scripts/filter_openapi_spec.py` - Specification Filter and Merger

This Python script processes multiple OpenAPI specifications and creates a single, filtered `openapi-spec.yaml` file.

**What it does:**
1. Reads all `.yaml`/`.yml` files from `openapi-specs/` directory
2. Filters endpoints based on `sdk-endpoints.txt` inclusion list
3. Detects and fails on duplicate `METHOD|PATH` across specs
4. Collects all referenced schemas via `$ref` traversal (dependency resolution)
5. Merges filtered paths and schemas into single specification
6. Validates all requested endpoints were found

**Usage:**
```bash
python scripts/filter_openapi_spec.py
```

**Parameters:**
None. The script uses these hardcoded paths relative to project root:
- Input: `openapi-specs/*.yaml` and `sdk-endpoints.txt`
- Output: `openapi-spec.yaml`

**Exit codes:**
- `0` - Success
- `1` - Error (missing files, duplicates, or validation failure)

**Output:**
The script provides detailed console output showing:
- Endpoints matched from each source spec
- Total components collected (schemas, responses, parameters)
- Warnings for endpoints in filter but not found in specs
- Errors for duplicate endpoints across multiple specs

### How to Regenerate

**Full Regeneration (recommended):**
```bash
# 1. Update source specs in openapi-specs/ if needed
# 2. Update sdk-endpoints.txt to add/remove endpoints
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
- After adding/removing endpoints in `sdk-endpoints.txt`

### Adding/Removing Endpoints

1. Edit `sdk-endpoints.txt` - add or remove endpoints using `METHOD|PATH` format (see [SDK Endpoint Filtering](#sdk-endpoint-filtering) for format details)
2. Run `python scripts/filter_openapi_spec.py` to regenerate the merged spec
3. Run `./scripts/regenerate_client.sh` to regenerate the SDK client

See the detailed [sdk-endpoints.txt documentation](#sdk-endpointstxt---endpoint-inclusion-list) above for format rules and examples.

**Note:** The adapter pattern (implemented in Story 1.3+) protects users from breaking changes during regeneration

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
