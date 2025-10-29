# Story 1.5: Implement Logins Resource Adapter

Status: Draft
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want a clean interface for retrieving login information,
so that users can verify authentication completion and obtain login credentials.

## Acceptance Criteria

1. `src/supermetrics/resources/logins.py` created with `LoginsResource` class
2. Methods implemented: `get()`, `list()`, `get_by_username()`
3. Both sync and async versions implemented
4. Resources attached to client: `client.logins` property
5. Complete type hints and docstrings added
6. Code passes `mypy` and `ruff`
7. Unit tests covering all operations

## Tasks / Subtasks

### Task 1: Create LoginsResource (sync) (AC: 1, 2, 5, 6)
- [ ] Create `src/supermetrics/resources/logins.py`
- [ ] Import required types and Login model from `_generated.models`
- [ ] Define `LoginsResource` class
- [ ] Implement `get(link_id: str) -> Login` method
- [ ] Implement `list() -> list[Login]` method
- [ ] Implement `get_by_username(login_username: str) -> Login` method
- [ ] Add error handling with httpx exception mapping
- [ ] Add logging (debug/info/error)
- [ ] Add complete type hints and Google-style docstrings
- [ ] Format with ruff and type check with mypy

### Task 2: Create LoginsAsyncResource (async) (AC: 3, 5, 6)
- [ ] In same file, define `LoginsAsyncResource` class
- [ ] Implement async versions of all methods
- [ ] Add error handling and logging
- [ ] Add type hints and docstrings

### Task 3: Attach to clients (AC: 4)
- [ ] Edit `client.py`: Add `self.logins = LoginsResource(self._client)`
- [ ] Edit `async_client.py`: Add `self.logins = LoginsAsyncResource(self._client)`

### Task 4: Create unit tests (AC: 7)
- [ ] Create `tests/unit/test_logins.py`
- [ ] Add mock Login response fixtures
- [ ] Test `get()` method (by link_id)
- [ ] Test `list()` method
- [ ] Test `get_by_username()` method
- [ ] Test error scenarios (401, 400, 404, network errors)
- [ ] Test async versions
- [ ] Run tests: `pytest tests/unit/test_logins.py -v`

### Task 5: Code quality checks (AC: 6)
- [ ] Run mypy: `mypy src/`
- [ ] Run ruff format: `ruff format src/`
- [ ] Run ruff check: `ruff check src/`

## Dev Notes

### Architecture Alignment

**Login Model (from updated tech spec):**
```python
class Login(BaseModel):
    login_id: str                     # Supermetrics login ID
    login_type: str                   # Authentication type
    username: str                     # Authenticated username (used in queries as ds_user)
    display_name: str                 # Visible name in UIs
    ds_id: str                        # Data source ID
    ds_name: str                      # Data source name
    default_scopes: list[str]         # Default API scopes
    additional_scopes: list[str]      # Additional granted scopes
    login_at: datetime                # Last authentication datetime
    owner_user_id: str                # Supermetrics user ID
    owner_user_email: str             # Supermetrics user email
    expires_at: Optional[datetime]    # Expiration datetime if any
    revoked_at: Optional[datetime]    # Revocation datetime if any
    is_refreshable: bool              # Can be auto-refreshed
    is_shared: bool                   # Shared with team users
```

[Source: tech-spec-epic-1.md - Login Model, lines 117-135]

**LoginsResource API (from tech spec):**
```python
# Get login by link ID
login: Login = client.logins.get(link_id: str) -> Login

# Get login by username
login: Login = client.logins.get_by_username(login_username: str) -> Login

# List all logins
logins: list[Login] = client.logins.list() -> list[Login]
```

[Source: tech-spec-epic-1.md - LoginsResource API, lines 199-209]

**Pattern:** Same as Story 1.4 - resource adapter wrapping generated code with error handling and logging.

### References

- [Source: tech-spec-epic-1.md - Acceptance Criteria #5, lines 570-576]
- [Source: epics.md - Story 1.5, lines 115-131]
- [Source: architecture.md - Resource Adapter Pattern, lines 556-679]

## Dev Agent Record

### Context Reference

<!-- Story context will be generated after story approval -->

### Agent Model Used

<!-- To be filled by dev agent -->

### Debug Log References

<!-- To be filled by dev agent -->

### Completion Notes List

<!-- To be filled by dev agent -->

### File List

<!-- To be filled by dev agent -->
