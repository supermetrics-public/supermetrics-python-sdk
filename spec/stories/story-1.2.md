# Story 1.2: Generate Initial SDK from OpenAPI Specification

Status: Done
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want to generate Python client code from the Supermetrics OpenAPI specification,
so that I have type-safe models and API client foundation.

## Acceptance Criteria

1. OpenAPI specification file obtained and stored in project root
2. `openapi-python-client` installed as dev dependency
3. Initial SDK generated into `src/supermetrics/_generated/` directory
4. Generated code includes sync and async clients, Pydantic models, and API endpoints
5. Generated code reviewed for completeness (login_links, logins, accounts, queries endpoints present)
6. Generation script created in `scripts/regenerate_client.sh` for future use

## Tasks / Subtasks

### Task 1: Obtain and filter OpenAPI specifications (AC: 1)
- [x] Contact Supermetrics team or check documentation for OpenAPI spec file locations
- [x] Create `openapi-specs/` directory in project root to store source specification files
- [x] Download all relevant OpenAPI specification files (YAML format) to `openapi-specs/` directory
- [x] Verify all downloaded specs are OpenAPI 3.x format
- [x] Create `sdk-endpoints.txt` configuration file in project root with METHOD|PATH format (one per line):
- [x] Implement `scripts/filter_openapi_spec.py` with the following features:
  - Read all `.yaml` files from `openapi-specs/` directory
  - Parse `sdk-endpoints.txt` for METHOD|PATH inclusion list
  - **Detect duplicates:** Check if same METHOD|PATH exists in multiple spec files
  - **On duplicate found:** Log warning with file locations and fail with error message
  - Filter paths/operations matching the inclusion list (skip duplicates)
  - Collect all referenced schemas/models from matched operations (including transitive dependencies via $ref)
  - Merge filtered paths into single OpenAPI specification
  - Consolidate schemas/components section (deduplicate if same schema name across files)
  - Use custom metadata (title: "Supermetrics API") instead of first spec file
  - Write merged spec to `openapi-spec.yaml` in project root
- [x] Run filter script: `python scripts/filter_openapi_spec.py`
- [x] Verify script output: no duplicate warnings/errors
- [x] Verify generated `openapi-spec.yaml` contains only SDK-supported endpoints
- [x] Verify spec is valid OpenAPI 3.x format and includes all referenced schemas

### Task 2: Install openapi-python-client (AC: 2)
- [x] Verify `openapi-python-client>=0.15.0` is in `pyproject.toml` dev dependencies (should already be there from Story 1.1)
- [x] Install dev dependencies: `pip install -e ".[dev]"` (used venv instead of uv)
- [x] Verify installation: `openapi-python-client --version` (v0.27.1)

### Task 3: Generate initial SDK code (AC: 3, 4)
- [x] Create output directory: `mkdir -p src/supermetrics/_generated`
- [x] Run openapi-python-client generate command (generated into `supermetrics_api_client/` subdirectory - standard behavior)
- [x] Review generated directory structure:
  - `_generated/supermetrics_api_client/client.py` (single Client class with sync/async support)
  - `_generated/supermetrics_api_client/api/` (API endpoint modules)
  - `_generated/supermetrics_api_client/models/` (Pydantic models)
- [x] Verify generated code compiles without errors

### Task 4: Review generated code for completeness (AC: 5)
- [x] Check `_generated/api/` contains endpoint modules for:
  - `data_source_login_links/` - create, get, list, close operations ✓
  - `data_source_logins/` - get, list operations ✓
  - `data_source/` - get_accounts operation ✓
  - `get_data/` - get_data operation ✓
- [x] Check `_generated/models/` contains Pydantic models for:
  - `LoginLink` model ✓
  - `DataSourceLogin` model ✓
  - Account models (get_accounts_json) ✓
  - Data/Query models (data_query, data_response) ✓
- [x] Verify sync and async clients exist:
  - Single `Client` class with both sync and async support (httpx.Client and httpx.AsyncClient) ✓
- [x] Check models have proper type hints and Pydantic v2 syntax ✓
- [x] Note any missing endpoints or models for manual addition later (None - all required endpoints present)

### Task 5: Create regeneration script (AC: 6)
- [x] Create `scripts/regenerate_client.sh` with executable permissions
- [x] Make script executable: `chmod +x scripts/regenerate_client.sh`
- [x] Test script: `./scripts/regenerate_client.sh` ✓
- [x] Verify regenerated code is identical to original generation ✓

### Task 6: Add _generated/ to .gitignore with caution note (AC: 3)
- [x] DO NOT add `_generated/` to `.gitignore` - generated code SHOULD be committed ✓
- [x] Comment already exists in `.gitignore` from Story 1.1 explaining why ✓
- [x] Stage generated code for manual commit: `git add src/supermetrics/_generated` ✓

### Task 7: Document generation process (AC: 6)
- [x] Update README.md with comprehensive OpenAPI regeneration section:
  - Source specifications location (openapi-specs/)
  - Merged spec location (openapi-spec.yaml)
  - Filter configuration (sdk-endpoints.txt)
  - How to regenerate (full process with filter script + regeneration script)
  - When to regenerate (monthly, after spec updates, after endpoint changes)
  - How to add/remove endpoints
- [x] Add note about adapter pattern protecting users from regeneration (Story 1.3+)

## Dev Notes

### Architecture Alignment

**OpenAPI Generator:** openapi-python-client (latest stable)
- Built-in dual sync/async support
- Generates Pydantic v2 models
- Minimal dependencies
- Fast POC timeline
- [Source: architecture.md - Decision Summary table, line 72]

**Generated Code Location:** `src/supermetrics/_generated/`
- Internal, regeneratable from OpenAPI
- Never edited manually
- Protected by adapter pattern
- [Source: architecture.md - Project Structure, line 143]

**Regeneration Strategy:**
- On-demand via script
- Monthly automated regeneration (Epic 2 Story 2.7)
- Tests validate adapter compatibility after regeneration
- [Source: architecture.md - OpenAPI Specification → Generated Code, lines 357-376]

### Project Structure Notes

After this story, the structure will include:
```
supermetrics-sdk/
├── openapi-spec.yaml           # NEW: OpenAPI source of truth
├── src/supermetrics/
│   └── _generated/              # NEW: Generated code directory
│       ├── __init__.py
│       ├── client.py            # Generated sync client
│       ├── async_client.py      # Generated async client
│       ├── api/                 # Generated API endpoints
│       │   ├── login_links/
│       │   ├── logins/
│       │   ├── accounts/
│       │   └── queries/
│       └── models/              # Generated Pydantic models
│           ├── login_link.py
│           ├── login.py
│           ├── account.py
│           └── ...
└── scripts/
    └── regenerate_client.sh     # NEW: Regeneration script
```

[Source: architecture.md - Project Structure, lines 143-158]

### Key Integration Points

**OpenAPI Spec → Generated Code Flow:**
1. OpenAPI spec (YAML) contains API definition
2. openapi-python-client CLI reads spec
3. Generates code in `_generated/` directory:
   - Sync/async clients
   - Pydantic models
   - API endpoint modules
4. Generated code provides foundation for adapter layer (Story 1.3+)

[Source: architecture.md - OpenAPI Specification → Generated Code, lines 357-376]

**Expected Endpoints (from PRD/Tech Spec):**
- `/login_links` - POST (create), GET (get, list), DELETE (close)
- `/logins` - GET (get, list)
- `/accounts` - GET (list with filtering)
- `/queries` - POST (execute), GET (get_results)

[Source: tech-spec-epic-1.md - APIs and Interfaces, lines 179-240]

### Testing Standards

- **No unit tests required** for generated code (it's auto-generated)
- **Manual verification** of generated code completeness (Task 4)
- **Integration tests** will be added in later stories (1.3+) to verify adapter compatibility
- **Regeneration script** should be tested to ensure it works

[Source: tech-spec-epic-1.md - Test Strategy Summary, lines 706-713]

### Known Risks and Mitigations

**Risk:** OpenAPI spec may not accurately reflect actual API behavior
- **Mitigation:** Manual review of generated code (Task 4). POC validation in Story 1.9 will catch discrepancies.

**Risk:** Generated code may have bugs or unexpected behavior
- **Mitigation:** openapi-python-client is mature. Adapter pattern (Story 1.3+) isolates users from issues.

[Source: tech-spec-epic-1.md - Risks, Assumptions, Open Questions, lines 651-658]

### Open Questions

1. **Where to obtain OpenAPI spec?** - Ask Supermetrics team in Task 1
2. **Does spec include all optional parameters?** - Review in Task 4, may need manual additions

[Source: tech-spec-epic-1.md - Open Questions, lines 688-694]

### References

- [Source: architecture.md - Project Initialization, lines 18-65] - Generation commands and workflow
- [Source: tech-spec-epic-1.md - Acceptance Criteria #2, lines 543-549] - Story AC definition
- [Source: epics.md - Story 1.2, lines 57-72] - Original story specification
- [Source: architecture.md - Integration Points, lines 355-376] - OpenAPI → Generated Code flow
- [Source: architecture.md - Technology Stack Details, lines 237-246] - openapi-python-client details

## Dev Agent Record

### Context Reference

- Story Context XML: `spec/stories/story-context-1.2.xml`
- Generated: 2025-11-20

### Agent Model Used

claude-sonnet-4-5@20250929

### Debug Log References

N/A - No debugging required

### Completion Notes List

**Implementation Summary:**

1. **OpenAPI Filtering & Merging (Task 1)**:
   - Created `sdk-endpoints.txt` with 8 filtered endpoints (login_links, logins, accounts, queries)
   - Implemented `scripts/filter_openapi_spec.py` to merge openapi-data.yaml and openapi-management.yaml
   - Filter script detects duplicates, filters by METHOD|PATH, collects transitive dependencies via $ref
   - Used custom metadata (title: "Supermetrics API") for general-purpose SDK
   - Generated merged `openapi-spec.yaml` with 8 endpoints and 25 components (9 schemas, 11 responses, 5 headers)

2. **SDK Generation (Tasks 2-4)**:
   - Added PyYAML>=6.0.0 to dev dependencies (required by filter script)
   - Installed openapi-python-client v0.27.1
   - Generated SDK into `src/supermetrics/_generated/supermetrics_api_client/`
   - Generated client uses single `Client` class with both sync/async support (httpx.Client + httpx.AsyncClient)
   - All required endpoints present: data_source_login_links, data_source_logins, data_source (accounts), get_data (queries)
   - All required models present: LoginLink, DataSourceLogin, Account models, Query/Data models
   - Generated code compiles successfully

3. **Regeneration & Documentation (Tasks 5-7)**:
   - Created `scripts/regenerate_client.sh` with validation and user-friendly output
   - Tested regeneration script - idempotent and successful
   - Enhanced README.md with comprehensive regeneration documentation (filter process, endpoint management, when to regenerate)

**Notes:**
- openapi-python-client creates nested package structure (`supermetrics_api_client/`) - this is standard behavior
- Some $ref responses not parsed (warnings during generation) - acceptable, doesn't affect core functionality
- Story 1.3 will create adapter pattern to wrap this generated code with stable public API

### File List

**Created:**
- `sdk-endpoints.txt` - Endpoint filter configuration (METHOD|PATH format)
- `scripts/filter_openapi_spec.py` - OpenAPI spec merger and filter script
- `scripts/regenerate_client.sh` - SDK regeneration script
- `openapi-spec.yaml` - Merged and filtered OpenAPI specification
- `src/supermetrics/_generated/` - Generated SDK directory (106 files)

**Modified:**
- `pyproject.toml` - Added pyyaml>=6.0.0 to dev dependencies
- `README.md` - Enhanced OpenAPI regeneration documentation section
- `.venv/` - Created virtual environment and installed dependencies
