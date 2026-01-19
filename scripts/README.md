# Scripts

This directory contains utility scripts for managing and generating the SuperPy SDK.

## Table of Contents

- [OpenAPI Specification Filter](#openapi-specification-filter)
  - [Overview](#overview)
  - [Features](#features)
  - [Configuration File](#configuration-file)
  - [Usage](#usage)
  - [How It Works](#how-it-works)
  - [Patch System](#patch-system)
  - [Examples](#examples)
- [Other Scripts](#other-scripts)

---

## OpenAPI Specification Filter

### Overview

**Script:** `filter_openapi_spec.py`

**Configuration:** `references/sdk-endpoint-filters.yaml`

This script filters and merges multiple OpenAPI specification files from the `openapi-specs/` directory into a single, customized `openapi-spec.yaml` file used for SDK generation.

The script allows you to:
1. Select specific endpoints to include in the SDK
2. Apply patches/overrides to customize endpoint definitions
3. Automatically resolve component dependencies
4. Merge multiple spec files while detecting duplicates

### Features

- **Endpoint Filtering**: Only include the endpoints you need in your SDK
- **Endpoint Patch System**: Customize individual endpoints with two patch strategies:
  - `merge`: Deep merge patches into existing definitions
  - `replace`: Completely replace specific sections
- **Component Patch System**: Apply surgical patches to shared components (schemas, responses, parameters, etc.)
  - More efficient than inlining entire schemas in endpoint patches
  - Changes propagate to all endpoints using the component
- **Duplicate Detection**: Fails if the same endpoint appears in multiple spec files
- **Dependency Resolution**: Automatically collects all referenced schemas, responses, and components
- **External Reference Resolution**: Resolves external YAML file references inline
- **Custom Metadata**: Applies SDK-specific metadata (title, version, description, etc.)

### Configuration File

**Location:** `scripts/references/sdk-endpoint-filters.yaml`

**Format:**

```yaml
endpoints:
  # Basic endpoint (no patches)
  - method: GET
    path: /api/resource

  # Endpoint with patches
  - method: POST
    path: /api/resource
    patches:
      merge:
        # Properties to deep merge with existing operation
        description: "Custom description"
        summary: "Custom summary"
        tags:
          - "CustomTag"
        parameters:
          - name: custom_param
            in: query
            schema:
              type: string
      replace:
        # Sections to completely replace
        responses:
          '200':
            description: "Success"
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/CustomResponse'

# Component patches - apply to shared components
component_patches:
  schemas:
    # Patch a shared schema
    DataResponse:
      merge:
        properties:
          meta:
            properties:
              result:
                properties:
                  cache_time:
                    nullable: true
  responses:
    # Patch a shared response
    BadRequest:
      merge:
        description: "Enhanced error description"
```

**Configuration Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `endpoints` | array | Yes | List of endpoint configurations |
| `endpoints[].method` | string | Yes | HTTP method (GET, POST, PUT, PATCH, DELETE, etc.) |
| `endpoints[].path` | string | Yes | API path (e.g., `/api/resource` or `/api/resource/{id}`) |
| `endpoints[].patches` | object | No | Patches to apply to the endpoint definition |
| `endpoints[].patches.merge` | object | No | Properties to deep merge with the existing operation |
| `endpoints[].patches.replace` | object | No | Sections to completely replace in the operation |
| `component_patches` | object | No | Patches to apply to shared components |
| `component_patches.schemas` | object | No | Patches for schema components |
| `component_patches.responses` | object | No | Patches for response components |
| `component_patches.parameters` | object | No | Patches for parameter components |
| `component_patches.{type}.{name}` | object | No | Patch definition with `merge` and/or `replace` keys |

### Usage

**Prerequisites:**

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if not already installed)
pip install PyYAML
```

**Running the script:**

```bash
# From project root
python scripts/filter_openapi_spec.py

# Or with Python 3.13+ specifically
python3.13 scripts/filter_openapi_spec.py
```

**Expected Output:**

```
📋 Loading endpoint configuration from sdk-endpoint-filters.yaml...
   Found 8 endpoints to include
   Found 1 component patch(es)

📂 Scanning openapi-specs/ for OpenAPI specs...
   Found 2 spec file(s): openapi-data.yaml, openapi-management.yaml

🔍 Processing openapi-data.yaml...
   ✓ Matched: GET /query/data/json
   ✓ Matched: GET /query/accounts
   ...

🔗 Collecting referenced schemas and components...
   Collected 25 component(s)

🔧 Resolving external file references...
   ✓ Resolved 2 external reference(s)

🔧 Applying component patches...
   🔧 Applying patches to schemas/DataResponse
   ✓ Applied patches to 1 component(s)

✅ Validation:
   ✓ All 8 filtered endpoints found and included

🎉 Success!
   Input specs: 2
   Filtered endpoints: 8
   Output: /path/to/openapi-spec.yaml
```

### How It Works

1. **Load Configuration**: Reads `scripts/references/sdk-endpoint-filters.yaml` to get the list of endpoints, endpoint patches, and component patches
2. **Scan Specs**: Discovers all `.yaml` and `.yml` files in `openapi-specs/`
3. **Filter & Patch Endpoints**: For each spec file:
   - Matches endpoints against the configuration
   - Applies endpoint patches if defined
   - Detects duplicates across files
4. **Collect Dependencies**: Recursively collects all referenced components (`$ref`)
5. **Resolve External References**: Loads and inlines external YAML file references
6. **Apply Component Patches**: Applies patches to shared components (schemas, responses, etc.)
7. **Merge & Write**: Combines everything into a single `openapi-spec.yaml` file

### Patch System

The patch system supports two strategies that can be used together or separately:

#### 1. Merge Strategy

**Purpose:** Deep merge patches into the existing operation definition

**Use Cases:**
- Add new properties
- Modify existing properties
- Add parameters, tags, or examples
- Enhance descriptions or summaries

**Behavior:**
- Nested dictionaries are merged recursively
- Lists and primitive values are replaced (not concatenated)
- New keys are added
- Existing keys are updated with patch values

**Example:**

```yaml
patches:
  merge:
    description: "Enhanced description"
    tags:
      - "NewTag"
    parameters:
      - name: filter
        in: query
        description: "Filter results"
        schema:
          type: string
```

#### 2. Replace Strategy

**Purpose:** Completely replace specific sections of the operation

**Use Cases:**
- Override entire response definitions
- Replace all parameters
- Change request body schema
- Redefine security requirements

**Behavior:**
- Specified keys are completely replaced with patch values
- Original values are discarded
- Useful when merge is too complex or insufficient

**Example:**

```yaml
patches:
  replace:
    responses:
      '200':
        description: "Successful operation"
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/Item'
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateRequest'
```

#### 3. Combined Strategy

You can use both `merge` and `replace` together. Merge is applied first, then replace:

```yaml
patches:
  merge:
    description: "Updated description"
    tags:
      - "Enhanced"
  replace:
    responses:
      '200':
        description: "Complete custom response"
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomResponse'
```

### Component Patch System

Component patches allow you to apply surgical modifications to shared OpenAPI components (schemas, responses, parameters, headers, etc.) without duplicating entire definitions.

#### Why Use Component Patches?

**Problem:** When an endpoint uses `$ref: '#/components/schemas/DataResponse'`, you can't modify nested properties without inlining the entire schema.

**Solution:** Apply patches directly to the shared component. Changes automatically propagate to all endpoints using that component.

#### Benefits

- **DRY (Don't Repeat Yourself)**: Modify the component once, affect all endpoints using it
- **Surgical Precision**: Change only what you need, using deep merge
- **Maintainability**: Easier to update and understand than large inline schemas
- **Efficiency**: No need to copy entire schemas into endpoint patches

#### Syntax

```yaml
component_patches:
  # Component type (schemas, responses, parameters, headers, etc.)
  schemas:
    # Component name
    ComponentName:
      # Same merge/replace strategies as endpoint patches
      merge:
        # Deep merge into the component
        properties:
          fieldName:
            nullable: true
      replace:
        # Complete replacement of sections
        required:
          - field1
          - field2
```

#### Supported Component Types

- `schemas` - Data models and request/response schemas
- `responses` - Shared response definitions
- `parameters` - Shared parameter definitions
- `headers` - Shared header definitions
- `requestBodies` - Shared request body definitions
- `securitySchemes` - Security scheme definitions

#### Real-World Example: Making cache_time Nullable

**Scenario:** The `DataResponse` schema is used by `/query/data/json`. The `cache_time` field deep inside the schema needs to be nullable.

**Before Component Patches:** You'd need to inline the entire `DataResponse` schema (100+ lines) in the endpoint patch.

**With Component Patches:**

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

**Result:** The `cache_time` field becomes nullable in the `DataResponse` schema, and this change automatically applies to all endpoints using this schema.

#### Component Patches vs Endpoint Patches

| Aspect | Component Patches | Endpoint Patches |
|--------|------------------|------------------|
| **Scope** | Affects all endpoints using the component | Affects only one endpoint |
| **Use Case** | Modify shared schemas, responses, parameters | Customize individual endpoint behavior |
| **Efficiency** | Single patch affects multiple endpoints | Must patch each endpoint separately |
| **When to Use** | Schema modifications, shared response changes | Endpoint-specific customizations |

#### Example: Multiple Component Patches

```yaml
component_patches:
  # Make multiple schema fields nullable
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
                  run_seconds:
                    nullable: true

    LoginResponse:
      merge:
        properties:
          expires_at:
            nullable: true

  # Enhance shared error responses
  responses:
    BadRequest:
      merge:
        description: "Bad Request - The request was malformed or contains invalid parameters"
        content:
          application/json:
            schema:
              properties:
                errorCode:
                  type: string
                  description: "Machine-readable error code"

    Unauthorized:
      replace:
        description: "Unauthorized - Valid authentication credentials are required"
```

### Examples

#### Example 1: Basic Endpoint List

```yaml
endpoints:
  - method: GET
    path: /users

  - method: GET
    path: /users/{id}

  - method: POST
    path: /users

  - method: DELETE
    path: /users/{id}
```

#### Example 2: Making a Schema Field Nullable (Component Patch)

**Use case:** The `DataResponse` schema has a `cache_time` field that should be nullable.

```yaml
endpoints:
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

**Why component patch?** If multiple endpoints use `DataResponse`, this single patch makes `cache_time` nullable everywhere.

#### Example 3: Adding Custom Tags and Description

```yaml
endpoints:
  - method: GET
    path: /api/analytics
    patches:
      merge:
        description: "Retrieve analytics data with custom filters and aggregations"
        summary: "Get Analytics"
        tags:
          - "Analytics"
          - "Reporting"
        parameters:
          - name: aggregation
            in: query
            description: "Type of aggregation to apply"
            schema:
              type: string
              enum: [sum, avg, count, min, max]
```

#### Example 4: Replacing Response Schema

```yaml
endpoints:
  - method: GET
    path: /api/legacy-endpoint
    patches:
      replace:
        responses:
          '200':
            description: "Modernized response format"
            content:
              application/json:
                schema:
                  type: object
                  required:
                    - data
                    - metadata
                  properties:
                    data:
                      type: array
                      items:
                        $ref: '#/components/schemas/ModernItem'
                    metadata:
                      type: object
                      properties:
                        total:
                          type: integer
                        page:
                          type: integer
```

#### Example 5: Adding Request Body Validation

```yaml
endpoints:
  - method: POST
    path: /api/resources
    patches:
      merge:
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - name
                  - type
                properties:
                  name:
                    type: string
                    minLength: 3
                    maxLength: 100
                  type:
                    type: string
                    enum: [type1, type2, type3]
                  description:
                    type: string
```

#### Example 6: Complete Endpoint Override

```yaml
endpoints:
  - method: GET
    path: /api/custom-endpoint
    patches:
      merge:
        description: "Fully customized endpoint with enhanced features"
        summary: "Get Custom Data"
        tags:
          - "Custom"
        operationId: "getCustomData"
        parameters:
          - name: include_metadata
            in: query
            description: "Include metadata in response"
            schema:
              type: boolean
              default: false
          - name: format
            in: query
            schema:
              type: string
              enum: [json, csv, xml]
              default: json
      replace:
        responses:
          '200':
            description: "Successful response with custom format"
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/CustomDataResponse'
          '400':
            description: "Bad request - invalid parameters"
          '401':
            description: "Unauthorized - authentication required"
          '404':
            description: "Resource not found"
```

#### Example 7: Combining Endpoint and Component Patches

**Use case:** Make schema fields nullable globally (component patch) while customizing specific endpoint behavior (endpoint patch).

```yaml
endpoints:
  # Standard endpoint using DataResponse
  - method: GET
    path: /query/data/json

  # Enhanced endpoint with custom description and tags
  - method: GET
    path: /query/accounts
    patches:
      merge:
        description: "Retrieve account information with enhanced metadata"
        tags:
          - "Accounts"
          - "Query"

# Apply schema changes globally
component_patches:
  schemas:
    # Make DataResponse fields nullable
    DataResponse:
      merge:
        properties:
          meta:
            properties:
              result:
                properties:
                  cache_time:
                    nullable: true
                  run_seconds:
                    nullable: true

  # Enhance error responses
  responses:
    BadRequest:
      merge:
        description: "Bad Request - Invalid parameters or malformed request"
        content:
          application/json:
            schema:
              properties:
                error_code:
                  type: string
                  description: "Machine-readable error code"
                details:
                  type: object
                  description: "Additional error details"
```

**Result:**
- `cache_time` and `run_seconds` are nullable in all endpoints using `DataResponse`
- `/query/accounts` has custom description and tags
- All endpoints using `BadRequest` response have enhanced error information

### Troubleshooting

#### Error: `ModuleNotFoundError: No module named 'yaml'`

**Solution:** Install PyYAML:
```bash
source .venv/bin/activate
pip install PyYAML
```

#### Error: `sdk-endpoint-filters.yaml not found`

**Solution:** Ensure you're running the script from the project root and the file exists at `scripts/references/sdk-endpoint-filters.yaml`

#### Warning: `endpoint(s) from filter not found in specs`

**Cause:** An endpoint is listed in `sdk-endpoint-filters.yaml` but doesn't exist in any OpenAPI spec file

**Solution:**
- Verify the method and path are correct
- Check that the endpoint exists in one of the spec files in `openapi-specs/`
- Remove the endpoint from configuration if it's no longer needed

#### Error: `DUPLICATE METHOD|PATH found`

**Cause:** The same endpoint (method + path) appears in multiple spec files

**Solution:** Remove the duplicate from one of the spec files or consolidate them

#### Endpoint Patches Not Applied

**Troubleshooting:**
1. Verify the `patches` key is at the correct level (under the endpoint, not nested)
2. Check YAML syntax and indentation
3. Ensure `merge` or `replace` keys are properly specified
4. Look for the "🔧 Applying endpoint patches to..." message in output to confirm patches are detected

#### Component Patches Not Applied

**Troubleshooting:**
1. Verify `component_patches` is at the root level of the YAML (not nested under `endpoints`)
2. Check that the component type exists (`schemas`, `responses`, `parameters`, etc.)
3. Verify the component name matches exactly (case-sensitive)
4. Ensure the component is actually used by at least one included endpoint
5. Look for the "🔧 Applying patches to {type}/{name}" message in output

**Warning:** If a component is not referenced by any included endpoint, it won't be in the merged spec, so the patch won't be applied.

#### Component Not Found

**Error message:** `⚠️  Component 'ComponentName' not found in schemas`

**Cause:** The component you're trying to patch doesn't exist or isn't being included in the merged spec.

**Solution:**
1. Verify the component name is spelled correctly (case-sensitive)
2. Check that at least one included endpoint references this component
3. Run the script and check the "Collected X component(s)" section to see which components are included

---

## Other Scripts

### `regenerate_client.sh`

Script for regenerating the SDK client code from the OpenAPI specification.

**Usage:**
```bash
./scripts/regenerate_client.sh
```

---

## Contributing

When adding new scripts:

1. Add executable permissions: `chmod +x scripts/your-script.sh`
2. Document the script in this README
3. Include usage examples
4. Add error handling and helpful output messages

---

## Support

For issues or questions about these scripts, please contact the development team or open an issue in the repository.
