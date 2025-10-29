# Story 1.6: Implement Accounts Resource Adapter

Status: Draft
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want a clean interface for retrieving data source accounts,
so that users can discover available accounts for querying.

## Acceptance Criteria

1. `src/supermetrics/resources/accounts.py` created with `AccountsResource` class
2. Methods implemented: `list()`, with support for filtering by `login_username`, `ds_id`, and other parameters
3. Both sync and async versions implemented
4. Resources attached to client: `client.accounts` property
5. Complete type hints and docstrings added
6. Code passes `mypy` and `ruff`
7. Unit tests covering all operations

## Tasks / Subtasks

### Task 1: Create AccountsResource (sync) (AC: 1, 2, 5, 6)
- [ ] Create `src/supermetrics/resources/accounts.py`
- [ ] Import Account model from `_generated.models`
- [ ] Define `AccountsResource` class
- [ ] Implement `list()` method with optional filtering parameters:
  - `login_username: Optional[str] = None`
  - `ds_id: Optional[str] = None`
  - `account_type: Optional[str] = None`
  - `**kwargs` for additional filters
- [ ] Add error handling and logging
- [ ] Add type hints and docstrings
- [ ] Format with ruff and type check with mypy

### Task 2: Create AccountsAsyncResource (async) (AC: 3, 5, 6)
- [ ] Define `AccountsAsyncResource` class
- [ ] Implement async `list()` method with same parameters
- [ ] Add error handling and logging

### Task 3: Attach to clients (AC: 4)
- [ ] Edit `client.py`: Add `self.accounts = AccountsResource(self._client)`
- [ ] Edit `async_client.py`: Add `self.accounts = AccountsAsyncResource(self._client)`

### Task 4: Create unit tests (AC: 7)
- [ ] Create `tests/unit/test_accounts.py`
- [ ] Test `list()` without filters
- [ ] Test `list(login_username="...")`
- [ ] Test `list(ds_id="...")`
- [ ] Test `list()` with multiple filters
- [ ] Test error scenarios
- [ ] Test async versions
- [ ] Run tests: `pytest tests/unit/test_accounts.py -v`

### Task 5: Code quality checks (AC: 6)
- [ ] Run mypy and ruff

## Dev Notes

### Architecture Alignment

**Account Model (from updated tech spec):**
```python
class Account(BaseModel):
    account_id: str        # Account identifier (used in queries)
    account_name: str      # Account display name
    group_name: str        # Account group name (empty when not available)
```

[Source: tech-spec-epic-1.md - Account Model, lines 137-143]

**AccountsResource API:**
```python
# List accounts by login username
accounts: list[Account] = client.accounts.list(login_username: str)

# List accounts by data source
accounts: list[Account] = client.accounts.list(ds_id: str)

# List with filtering
accounts: list[Account] = client.accounts.list(
    login_username: str,
    account_type: Optional[str] = None
)
```

[Source: tech-spec-epic-1.md - AccountsResource API, lines 211-224]

### References

- [Source: tech-spec-epic-1.md - Acceptance Criteria #6, lines 578-584]
- [Source: epics.md - Story 1.6, lines 133-150]

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
