# Story 1.6: Implement Accounts Resource Adapter

Status: Done
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
- [x] Create `src/supermetrics/resources/accounts.py`
- [x] Import Account model from `_generated.models`
- [x] Define `AccountsResource` class
- [x] Implement `list()` method with optional filtering parameters:
  - `login_usernames: str | list[str] | None`
  - `ds_id: str` (required)
  - `cache_minutes: int | None`
- [x] Add error handling and logging
- [x] Add type hints and docstrings
- [x] Format with ruff and type check with mypy

### Task 2: Create AccountsAsyncResource (async) (AC: 3, 5, 6)
- [x] Define `AccountsAsyncResource` class
- [x] Implement async `list()` method with same parameters
- [x] Add error handling and logging

### Task 3: Attach to clients (AC: 4)
- [x] Edit `client.py`: Add `self.accounts = AccountsResource(self._client)`
- [x] Edit `async_client.py`: Add `self.accounts = AccountsAsyncResource(self._client)`

### Task 4: Create unit tests (AC: 7)
- [x] Create `tests/unit/test_accounts.py`
- [x] Test `list()` without filters
- [x] Test `list(login_usernames="...")`
- [x] Test `list(login_usernames=[...])`
- [x] Test `list()` with cache_minutes
- [x] Test error scenarios
- [x] Test async versions
- [x] Run tests: `pytest tests/unit/test_accounts.py -v`

### Task 5: Code quality checks (AC: 6)
- [x] Run mypy and ruff

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

- Story Context XML: `spec/stories/story-context-1.6.xml`
- Generated: 2025-12-05

### Agent Model Used

claude-sonnet-4-5@20250929

### Debug Log References

None - implementation completed without blockers.

### Completion Notes List

**Implementation Summary:**
- Created AccountsResource and AccountsAsyncResource in src/supermetrics/resources/accounts.py
- Implemented list() method with ds_id (required), login_usernames, and cache_minutes parameters
- Implemented automatic response flattening from nested structure: Response.data[].accounts[] → single list
- Attached resources to SupermetricsClient and SupermetricsAsyncClient
- Created comprehensive unit tests with 10 test cases covering all scenarios
- All tests passing (10/10)

**Technical Notes:**
- Used GetAccountsResponse200DataItemAccountsItem model from generated code
- Renamed ds_users parameter to login_usernames for better developer experience
- Supports both single string and list of strings for login_usernames
- Returns empty list (not error) when no accounts found
- Properly flattens nested response structure where each data item can contain multiple accounts
- Added proper logging at DEBUG and INFO levels
- Used Google-style docstrings with Args, Returns, Raises, and Example sections

**Key Implementation Detail:**
The API returns a nested structure: `Response.data[]` contains login items, each with an `accounts[]` list. The adapter automatically flattens this into a single list of all accounts across all logins, making it much easier for developers to work with.

**Code Quality:**
- ruff format: 1 file reformatted ✓
- ruff check: All checks passed! ✓
- pytest: 10 passed in 0.16s ✓

**Files Modified:**
- Created: src/supermetrics/resources/accounts.py (203 lines)
- Modified: src/supermetrics/client.py (+2 lines)
- Modified: src/supermetrics/async_client.py (+2 lines)
- Created: tests/unit/test_accounts.py (418 lines)

### File List

**Created Files:**
- src/supermetrics/resources/accounts.py
- tests/unit/test_accounts.py

**Modified Files:**
- src/supermetrics/client.py
- src/supermetrics/async_client.py
