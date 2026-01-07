# Story 1.8: Create Basic Error Handling

Status: Done
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want clear exceptions when API calls fail,
So that SDK users can handle errors appropriately and understand what went wrong.

## Acceptance Criteria

1. `src/supermetrics/exceptions.py` created with custom exception hierarchy
2. Base exception `SupermetricsError` defined with common attributes (message, status_code, endpoint, response_body)
3. Specific exceptions implemented: `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`
4. All resource adapters (login_links, logins, accounts, queries) updated to catch httpx exceptions and re-raise as SDK exceptions
5. HTTP status codes mapped appropriately: 401→AuthenticationError, 400→ValidationError, 404/5xx→APIError
6. Network errors (timeout, connection refused) mapped to `NetworkError`
7. Exception messages include relevant context (status code, endpoint, error details from API response)
8. Code passes `mypy` and `ruff`
9. Unit tests covering error scenarios for each resource

## Tasks / Subtasks

### Task 1: Create exception hierarchy (AC: 1, 2, 3, 6)
- [ ] Create `src/supermetrics/exceptions.py`
- [ ] Define base exception `SupermetricsError(Exception)`:
  ```python
  class SupermetricsError(Exception):
      """Base exception for all Supermetrics SDK errors."""
      def __init__(
          self,
          message: str,
          status_code: Optional[int] = None,
          endpoint: Optional[str] = None,
          response_body: Optional[str] = None
      ):
          super().__init__(message)
          self.message = message
          self.status_code = status_code
          self.endpoint = endpoint
          self.response_body = response_body
  ```
- [ ] Define `AuthenticationError(SupermetricsError)`:
  - Raised for 401 Unauthorized responses
  - Indicates invalid or expired API key
- [ ] Define `ValidationError(SupermetricsError)`:
  - Raised for 400 Bad Request responses
  - Indicates invalid request parameters or missing required fields
- [ ] Define `APIError(SupermetricsError)`:
  - Raised for 404, 5xx, and other HTTP errors
  - Indicates server-side errors or resource not found
- [ ] Define `NetworkError(SupermetricsError)`:
  - Raised for network-level failures (timeout, connection refused, DNS errors)
  - Does not include status_code (network errors don't have HTTP status)
- [ ] Add complete docstrings explaining when each exception is raised
- [ ] Add type hints to all exception classes
- [ ] Format with ruff and type check with mypy

### Task 2: Update LoginLinksResource error handling (AC: 4, 5, 6, 7)
- [ ] Edit `src/supermetrics/resources/login_links.py`
- [ ] Import exceptions: `from supermetrics_sdk.exceptions import AuthenticationError, ValidationError, APIError, NetworkError`
- [ ] Import httpx: `import httpx`
- [ ] Wrap each method (`create`, `get`, `list`, `close`) with try/except:
  ```python
  try:
      # Existing method implementation
      response = self._client.login_links.create(...)
      return response
  except httpx.HTTPStatusError as e:
      # Map HTTP status codes to SDK exceptions
      if e.response.status_code == 401:
          raise AuthenticationError(
              "Invalid or expired API key",
              status_code=401,
              endpoint=str(e.request.url),
              response_body=e.response.text
          )
      elif e.response.status_code == 400:
          raise ValidationError(
              f"Invalid request parameters: {e.response.text}",
              status_code=400,
              endpoint=str(e.request.url),
              response_body=e.response.text
          )
      elif e.response.status_code == 404:
          raise APIError(
              f"Login link not found: {e.response.text}",
              status_code=404,
              endpoint=str(e.request.url),
              response_body=e.response.text
          )
      elif e.response.status_code >= 500:
          raise APIError(
              f"Supermetrics API error: {e.response.text}",
              status_code=e.response.status_code,
              endpoint=str(e.request.url),
              response_body=e.response.text
          )
      else:
          raise APIError(
              f"API error ({e.response.status_code}): {e.response.text}",
              status_code=e.response.status_code,
              endpoint=str(e.request.url),
              response_body=e.response.text
          )
  except httpx.RequestError as e:
      raise NetworkError(
          f"Network error: {str(e)}",
          endpoint=str(e.request.url) if hasattr(e, 'request') else None
      )
  ```
- [ ] Apply same pattern to async methods in `LoginLinksAsyncResource`
- [ ] Format and type check

### Task 3: Update LoginsResource error handling (AC: 4, 5, 6, 7)
- [ ] Edit `src/supermetrics/resources/logins.py`
- [ ] Import exceptions and httpx
- [ ] Wrap all methods (`get`, `list`, `get_by_username`) with try/except using same pattern
- [ ] Apply to both sync and async versions
- [ ] Format and type check

### Task 4: Update AccountsResource error handling (AC: 4, 5, 6, 7)
- [ ] Edit `src/supermetrics/resources/accounts.py`
- [ ] Import exceptions and httpx
- [ ] Wrap all methods (`list`) with try/except using same pattern
- [ ] Apply to both sync and async versions
- [ ] Format and type check

### Task 5: Update QueriesResource error handling (AC: 4, 5, 6, 7)
- [ ] Edit `src/supermetrics/resources/queries.py`
- [ ] Import exceptions and httpx
- [ ] Wrap all methods (`execute`, `get_results`) with try/except using same pattern
- [ ] Apply to both sync and async versions
- [ ] Format and type check

### Task 6: Export exceptions from __init__.py (AC: 1)
- [ ] Edit `src/supermetrics/__init__.py`
- [ ] Add exception imports and exports:
  ```python
  from supermetrics_sdk.exceptions import (
      SupermetricsError,
      AuthenticationError,
      ValidationError,
      APIError,
      NetworkError,
  )

  __all__ = [
      "SupermetricsClient",
      "SupermetricsAsyncClient",
      "SupermetricsError",
      "AuthenticationError",
      "ValidationError",
      "APIError",
      "NetworkError",
  ]
  ```

### Task 7: Create exception tests (AC: 9)
- [ ] Create `tests/unit/test_exceptions.py`
- [ ] Test base exception `SupermetricsError`:
  - Verify message, status_code, endpoint, response_body attributes
- [ ] Test each specific exception type:
  - `AuthenticationError` with 401 status
  - `ValidationError` with 400 status
  - `APIError` with 404 and 500 statuses
  - `NetworkError` without status_code
- [ ] Test exception inheritance (all inherit from SupermetricsError)

### Task 8: Update existing resource tests with error scenarios (AC: 9)
- [ ] Edit `tests/unit/test_login_links.py`:
  - Add test for 401 → `AuthenticationError`
  - Add test for 400 → `ValidationError`
  - Add test for 404 → `APIError`
  - Add test for 500 → `APIError`
  - Add test for network timeout → `NetworkError`
- [ ] Edit `tests/unit/test_logins.py`:
  - Add same error scenario tests
- [ ] Edit `tests/unit/test_accounts.py`:
  - Add same error scenario tests
- [ ] Edit `tests/unit/test_queries.py`:
  - Add same error scenario tests
- [ ] Run all tests: `pytest tests/unit/ -v`

### Task 9: Code quality checks (AC: 8)
- [ ] Run mypy: `mypy src/`
- [ ] Run ruff format: `ruff format src/`
- [ ] Run ruff check: `ruff check src/`

## Dev Notes

### Architecture Alignment

**Exception Hierarchy Design:**
```python
SupermetricsError (base)
├── AuthenticationError (401 errors)
├── ValidationError (400 errors)
├── APIError (404, 5xx, other HTTP errors)
└── NetworkError (timeout, connection errors)
```

All exceptions include context:
- `message`: Human-readable error description
- `status_code`: HTTP status code (if applicable)
- `endpoint`: API endpoint that failed
- `response_body`: Raw API response for debugging

[Source: architecture.md - Exception Hierarchy, lines 868-915]

**HTTP Status Code Mapping:**
- 401 Unauthorized → `AuthenticationError` (invalid/expired API key)
- 400 Bad Request → `ValidationError` (invalid parameters)
- 404 Not Found → `APIError` (resource not found)
- 5xx Server Error → `APIError` (server-side error)
- Network errors → `NetworkError` (timeout, connection refused, DNS failure)

[Source: architecture.md - Exception Mapping Pattern, lines 917-969]

**Error Handling Pattern:**
All resource methods follow this pattern:
```python
try:
    response = self._client.api_method(...)
    return response
except httpx.HTTPStatusError as e:
    # Map status codes to SDK exceptions
    if e.response.status_code == 401:
        raise AuthenticationError(...)
    elif e.response.status_code == 400:
        raise ValidationError(...)
    # ... etc
except httpx.RequestError as e:
    raise NetworkError(...)
```

[Source: architecture.md - Exception Mapping Pattern, lines 918-969]

### Error Message Best Practices

**Clear, Actionable Messages:**
- ✅ "Invalid or expired API key" (tells user what's wrong and implies solution)
- ✅ "Invalid request parameters: {api_error_details}" (includes API error context)
- ❌ "HTTP 401 error" (too generic, not actionable)

**Include Context:**
- Always include `status_code` for HTTP errors
- Always include `endpoint` to help debug which API call failed
- Include `response_body` with raw API error for detailed debugging

### Testing Strategy

**Exception Tests:**
- Unit tests for exception class creation and attribute access
- Mock httpx exceptions in resource tests
- Verify correct exception type raised for each status code
- Verify exception attributes (message, status_code, endpoint, response_body)

**Example Test:**
```python
def test_authentication_error_on_401(mocker, test_client):
    """Test 401 response raises AuthenticationError."""
    # Mock httpx to raise HTTPStatusError with 401
    mock_response = httpx.Response(401, text="Unauthorized")
    mocker.patch.object(
        test_client._client.login_links,
        'create',
        side_effect=httpx.HTTPStatusError("", request=..., response=mock_response)
    )

    # Verify AuthenticationError is raised
    with pytest.raises(AuthenticationError) as exc_info:
        test_client.login_links.create(ds_id="GAWA", description="Test")

    # Verify exception attributes
    assert exc_info.value.status_code == 401
    assert "Invalid or expired API key" in str(exc_info.value)
    assert exc_info.value.endpoint is not None
```

[Source: tech-spec-epic-1.md - Error Handling Test Strategy, lines 750-785]

### Project Structure Impact

After this story, error handling will be centralized:
```
src/supermetrics/
├── exceptions.py               # NEW: Exception hierarchy
├── client.py                   # UNCHANGED
├── async_client.py             # UNCHANGED
├── __init__.py                 # UPDATED: Export exceptions
└── resources/
    ├── login_links.py          # UPDATED: Add error handling
    ├── logins.py               # UPDATED: Add error handling
    ├── accounts.py             # UPDATED: Add error handling
    └── queries.py              # UPDATED: Add error handling

tests/unit/
├── test_exceptions.py          # NEW: Exception class tests
├── test_login_links.py         # UPDATED: Add error scenario tests
├── test_logins.py              # UPDATED: Add error scenario tests
├── test_accounts.py            # UPDATED: Add error scenario tests
└── test_queries.py             # UPDATED: Add error scenario tests
```

### References

- [Source: tech-spec-epic-1.md - Acceptance Criteria #8, lines 595-603] - Story AC definition
- [Source: epics.md - Story 1.8, lines 173-187] - Original story specification
- [Source: architecture.md - Exception Hierarchy, lines 868-915] - Exception design
- [Source: architecture.md - Exception Mapping Pattern, lines 917-969] - Implementation pattern

## Dev Agent Record

### Context Reference

- Story Context XML: `spec/stories/story-context-1.8.xml`
- Generated: 2025-12-11

### Agent Model Used

claude-sonnet-4-5@20250929

### Debug Log References

<!-- To be filled by dev agent -->

### Completion Notes List

- Created custom exception hierarchy in `src/supermetrics/exceptions.py` with SupermetricsError base class and 4 specific exception types (AuthenticationError, ValidationError, APIError, NetworkError)
- Updated all resource adapters (login_links, logins, accounts, queries) with comprehensive HTTP error mapping - both sync and async versions
- Exported all exceptions from `src/supermetrics/__init__.py` for public API
- Created comprehensive exception tests in `tests/unit/test_exceptions.py` (22 tests)
- Added error scenario tests to all 4 resource test files (20 new tests across resources)
- All code passes mypy strict type checking and ruff linting/formatting
- Total test suite: 68 tests passing (100% pass rate)

### File List

**New Files:**
- src/supermetrics/exceptions.py
- spec/1-8-create-basic-error-handling.context.xml
- tests/unit/test_exceptions.py

**Modified Files:**
- src/supermetrics/__init__.py
- src/supermetrics/resources/login_links.py
- src/supermetrics/resources/logins.py
- src/supermetrics/resources/accounts.py
- src/supermetrics/resources/queries.py
- tests/unit/test_login_links.py
- tests/unit/test_logins.py
- tests/unit/test_accounts.py
- tests/unit/test_queries.py
- spec/stories/story-1.8.md
- spec/sprint-status.yaml
