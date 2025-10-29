# Story 1.7: Implement Queries Resource Adapter

Status: Draft
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
- [ ] Create `src/supermetrics/resources/queries.py`
- [ ] Import QueryResult and Field models from `_generated.models`
- [ ] Define `QueriesResource` class
- [ ] Implement `execute()` method with parameters:
  - `ds_id: str`
  - `ds_accounts: list[str]`
  - `fields: list[str]`
  - `start_date: str`
  - `end_date: str`
  - `**kwargs` for additional query parameters
  - Returns: `QueryResult`
- [ ] Implement `get_results(query_id: str) -> QueryResult` for async query polling
- [ ] Add error handling and logging
- [ ] Add type hints and docstrings with parameter explanations
- [ ] Format with ruff and type check with mypy

### Task 2: Create QueriesAsyncResource (async) (AC: 4, 6, 7)
- [ ] Define `QueriesAsyncResource` class
- [ ] Implement async `execute()` method
- [ ] Implement async `get_results()` method
- [ ] Add error handling and logging

### Task 3: Attach to clients (AC: 5)
- [ ] Edit `client.py`: Add `self.queries = QueriesResource(self._client)`
- [ ] Edit `async_client.py`: Add `self.queries = QueriesAsyncResource(self._client)`

### Task 4: Create unit tests (AC: 8)
- [ ] Create `tests/unit/test_queries.py`
- [ ] Test `execute()` with successful query (status="completed")
- [ ] Test `execute()` with pending query (status="pending")
- [ ] Test `get_results()` for pending query retrieval
- [ ] Test query with various parameters (fields, date ranges, accounts)
- [ ] Test error scenarios
- [ ] Test async versions
- [ ] Run tests: `pytest tests/unit/test_queries.py -v`

### Task 5: Code quality checks (AC: 7)
- [ ] Run mypy and ruff

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

<!-- Story context will be generated after story approval -->

### Agent Model Used

<!-- To be filled by dev agent -->

### Debug Log References

<!-- To be filled by dev agent -->

### Completion Notes List

<!-- To be filled by dev agent -->

### File List

<!-- To be filled by dev agent -->
