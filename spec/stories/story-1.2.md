# Story 1.2: Generate Initial SDK from OpenAPI Specification

Status: Draft
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

### Task 1: Obtain OpenAPI specification (AC: 1)
- [ ] Contact Supermetrics team or check documentation for OpenAPI spec location
- [ ] Download OpenAPI specification file (YAML or JSON format)
- [ ] Store as `openapi-spec.yaml` in project root
- [ ] Verify spec is OpenAPI 3.x format
- [ ] Review spec to confirm it includes required endpoints: /login_links, /logins, /accounts, /queries

### Task 2: Install openapi-python-client (AC: 2)
- [ ] Verify `openapi-python-client>=0.15.0` is in `pyproject.toml` dev dependencies (should already be there from Story 1.1)
- [ ] Install dev dependencies: `uv pip install -e ".[dev]"`
- [ ] Verify installation: `openapi-python-client --version`

### Task 3: Generate initial SDK code (AC: 3, 4)
- [ ] Create output directory: `mkdir -p src/supermetrics/_generated`
- [ ] Run openapi-python-client generate command:
  ```bash
  openapi-python-client generate \
    --path openapi-spec.yaml \
    --output-path src/supermetrics/_generated
  ```
- [ ] Review generated directory structure:
  - `_generated/client.py` (sync client)
  - `_generated/async_client.py` (async client)
  - `_generated/api/` (API endpoint modules)
  - `_generated/models/` (Pydantic models)
- [ ] Verify generated code compiles without errors: `python -c "import ._generated"`

### Task 4: Review generated code for completeness (AC: 5)
- [ ] Check `_generated/api/` contains endpoint modules for:
  - `login_links/` - create, get, list, close operations
  - `logins/` - get, list operations
  - `accounts/` - list operations
  - `queries/` - execute, get_results operations
- [ ] Check `_generated/models/` contains Pydantic models for:
  - `LoginLink` model
  - `Login` model
  - `Account` model
  - `QueryResult` model (or equivalent)
- [ ] Verify sync and async clients exist:
  - `_generated/client.py` with `Client` class
  - `_generated/async_client.py` with `AsyncClient` class
- [ ] Check models have proper type hints and Pydantic v2 syntax
- [ ] Note any missing endpoints or models for manual addition later

### Task 5: Create regeneration script (AC: 6)
- [ ] Create `scripts/regenerate_client.sh` with executable permissions:
  ```bash
  #!/bin/bash
  set -e

  echo "Regenerating Supermetrics SDK from OpenAPI specification..."

  # Remove old generated code
  rm -rf src/supermetrics/_generated

  # Generate new code
  openapi-python-client generate \
    --path openapi-spec.yaml \
    --output-path src/supermetrics/_generated

  echo "✓ SDK regenerated successfully"
  echo "Run tests to verify compatibility: pytest tests/"
  ```
- [ ] Make script executable: `chmod +x scripts/regenerate_client.sh`
- [ ] Test script: `./scripts/regenerate_client.sh`
- [ ] Verify regenerated code is identical to original generation

### Task 6: Add _generated/ to .gitignore with caution note (AC: 3)
- [ ] DO NOT add `_generated/` to `.gitignore` - generated code SHOULD be committed
- [ ] Add comment to `.gitignore` explaining why:
  ```
  # Note: _generated/ is NOT ignored - it's committed to version control
  # for transparency and to support offline development
  ```
- [ ] Commit generated code to repository: `git add src/supermetrics/_generated`

### Task 7: Document generation process (AC: 6)
- [ ] Update README.md with OpenAPI regeneration section:
  - Where to find the OpenAPI spec
  - How to regenerate: `./scripts/regenerate_client.sh`
  - When to regenerate (monthly, or when API changes)
- [ ] Add note about adapter pattern protecting users from regeneration

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

<!-- Story context will be generated after story approval -->

### Agent Model Used

<!-- To be filled by dev agent -->

### Debug Log References

<!-- To be filled by dev agent -->

### Completion Notes List

<!-- To be filled by dev agent after story completion -->

### File List

<!-- To be filled by dev agent - list of all files created/modified -->
