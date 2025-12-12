# Story 1.7: Implement Queries Resource Adapter

Status: Approved
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want a clean interface for executing data queries,
so that users can fetch marketing data with proper parameter validation.

## Acceptance Criteria

1. `src/supermetrics/resources/queries.py` created with `QueriesResource` class
2. Methods implemented: `execute()`, `get_results()`, with support for fields, date ranges, accounts, data source parameters
3. Basic async query polling support implemented (check status, retrieve results)
4. Both sync and async versions implemented
5. Resources attached to client: `client.queries` property
6. Complete type hints and docstrings added
7. Code passes `mypy` and `ruff`
8. Unit tests covering query execution and result retrieval

## Tasks / Subtasks

### Task 1: Create QueriesResource (sync) (AC: 1, 2, 3, 6, 7)
- [x] Create `src/supermetrics/resources/queries.py`
- [x] Import QueryResult and Field models from `_generated.models`
- [x] Define `QueriesResource` class
- [x] Implement `execute()` method with parameters:
  - `ds_id: str`
  - `ds_accounts: list[str]`
  - `fields: list[str]`
  - `start_date: str`
  - `end_date: str`
  - `**kwargs` for additional query parameters
  - Returns: `DataResponse`
- [x] Implement `get_results(query_id: str) -> DataResponse` for async query polling
- [x] Add error handling and logging
- [x] Add type hints and docstrings with parameter explanations
- [x] Format with ruff and type check with mypy

### Task 2: Create QueriesAsyncResource (async) (AC: 4, 6, 7)
- [x] Define `QueriesAsyncResource` class
- [x] Implement async `execute()` method
- [x] Implement async `get_results()` method
- [x] Add error handling and logging

### Task 3: Attach to clients (AC: 5)
- [x] Edit `client.py`: Add `self.queries = QueriesResource(self._client)`
- [x] Edit `async_client.py`: Add `self.queries = QueriesAsyncResource(self._client)`

### Task 4: Create unit tests (AC: 8)
- [x] Create `tests/unit/test_queries.py`
- [x] Test `execute()` with successful query (status="completed")
- [x] Test `execute()` with pending query (status="pending")
- [x] Test `get_results()` for pending query retrieval
- [x] Test query with various parameters (fields, date ranges, accounts)
- [x] Test error scenarios
- [x] Test async versions
- [x] Run tests: `pytest tests/unit/test_queries.py -v`

### Task 5: Code quality checks (AC: 7)
- [x] Run mypy and ruff

## Dev Notes

### Architecture Alignment

**QueryResult Model (from updated tech spec):**
```python
class Field(BaseModel):
    id: str                     # Field ID the API uses
    requested_id: str           # Field ID from the request
    name: str                   # Field name
    type: str                   # Field type
    split: str                  # Field split by type
    data_type: str              # Field data type
    data_column: int            # Field value position in each data row
    visible: bool               # Whether data for this field is visible

class QueryResult(BaseModel):
    request_id: str             # API request ID
    schedule_id: str            # Custom or generated schedule ID
    status_code: str            # Status code for the query
    data: list[dict]            # Actual data rows
    fields: list[Field]         # Field definitions
    row_count: int              # Number of rows returned
    data_sampled: bool          # If data source provided sampled data
    cache_used: bool            # If cached data was used
    cache_time: datetime        # Most recent cached data timestamp
```

[Source: tech-spec-epic-1.md - QueryResult Model, lines 145-167]

**QueriesResource API:**
```python
# Execute data query
result: QueryResult = client.queries.execute(
    ds_id: str,
    ds_accounts: list[str],
    fields: list[str],
    start_date: str,
    end_date: str,
    **kwargs
) -> QueryResult

# Get query results (for async queries)
result: QueryResult = client.queries.get_results(query_id: str) -> QueryResult
```

[Source: tech-spec-epic-1.md - QueriesResource API, lines 226-240]

**Async Query Polling Pattern:**
```python
# Execute query
result = client.queries.execute(...)

# If query is pending, poll for results
if result.status_code == "pending":
    result = client.queries.get_results(query_id=result.request_id)
```

[Source: tech-spec-epic-1.md - Workflows, line 313-320]

### References

- [Source: tech-spec-epic-1.md - Acceptance Criteria #7, lines 586-593]
- [Source: epics.md - Story 1.7, lines 152-170]

## Dev Agent Record

### Context Reference

- Story Context XML: `spec/stories/story-context-1.7.xml`
- Generated: 2025-12-09

### Agent Model Used

claude-sonnet-4-5@20250929

### Debug Log References

<!-- To be filled by dev agent -->

### Completion Notes List

**Implementation Summary:**
- Implemented QueriesResource and QueriesAsyncResource classes following the adapter pattern
- Created execute() and get_results() methods with full parameter support (ds_id, ds_accounts, fields, dates, **kwargs)
- Implemented async query polling pattern using schedule_id parameter
- Attached resources to SupermetricsClient and SupermetricsAsyncClient
- Created comprehensive unit tests with 15 test cases covering all methods, async versions, and error scenarios
- All tests passing (15/15)

**Technical Notes:**
- Used DataResponse model from generated code for query results
- Implemented type-safe handling with cast(AuthenticatedClient, self._client) for client compatibility
- Used isinstance(response, Unset) for proper UNSET type checking (mypy strict compliant)
- Followed exact resource adapter pattern from accounts.py including response handling
- Added proper logging at DEBUG and INFO levels
- Used Google-style docstrings with Args, Returns, Raises, and Example sections
- Return type: DataResponse | None (error responses handled by generated client via HTTPStatusError)

**Code Quality:**
- ruff format: 1 file reformatted ✓
- ruff check: All checks passed! ✓
- mypy --strict: Success, no issues found ✓ (proper use of cast() and isinstance())
- pytest: 15 passed in 0.18s ✓

**Files Modified:**
- Created: src/supermetrics/resources/queries.py (380 lines)
- Modified: src/supermetrics/client.py (+2 lines)
- Modified: src/supermetrics/async_client.py (+2 lines)
- Created: tests/unit/test_queries.py (592 lines)

### File List

**Created Files:**
- src/supermetrics/resources/queries.py
- tests/unit/test_queries.py

**Modified Files:**
- src/supermetrics/client.py
- src/supermetrics/async_client.py
