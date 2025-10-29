# Story 1.4: Implement Login Links Resource Adapter

Status: Draft
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want a clean, Pythonic interface for login link operations,
so that users can easily create and manage data source authentication links.

## Acceptance Criteria

1. `src/supermetrics/resources/login_links.py` created with `LoginLinksResource` class
2. Methods implemented: `create()`, `get()`, `list()`, `close()`
3. Methods wrap `_generated` client calls with proper parameter mapping
4. Both sync and async versions implemented (`LoginLinksResource` and `LoginLinksAsyncResource`)
5. Resources attached to client: `client.login_links` property
6. Complete type hints and docstrings added for all public methods
7. Code passes `mypy` strict type checking and formatted with `ruff`
8. Unit tests added covering all CRUD operations

## Tasks / Subtasks

### Task 1: Create LoginLinksResource (sync) (AC: 1, 2, 3, 6, 7)
- [ ] Create `src/supermetrics/resources/` directory
- [ ] Create `src/supermetrics/resources/__init__.py`
- [ ] Create `src/supermetrics/resources/login_links.py`
- [ ] Import required types:
  ```python
  from typing import Optional
  import logging
  import httpx
  from supermetrics_sdk.exceptions import (
      AuthenticationError, ValidationError, APIError, NetworkError
  )
  from supermetrics_sdk._generated.client import Client as GeneratedClient
  from supermetrics_sdk._generated.models import LoginLink
  ```
- [ ] Define `LoginLinksResource` class with `__init__(self, client: GeneratedClient)`
- [ ] Implement `create(ds_id: str, description: str, **kwargs) -> LoginLink` method
- [ ] Implement `get(link_id: str) -> LoginLink` method
- [ ] Implement `list() -> list[LoginLink]` method
- [ ] Implement `close(link_id: str) -> None` method
- [ ] Add error handling with try/except for httpx exceptions
- [ ] Map HTTP errors to SDK exceptions (401→AuthenticationError, 400→ValidationError, etc.)
- [ ] Add logging (debug for operations, info for success, error for failures)
- [ ] Add complete type hints to all methods
- [ ] Add Google-style docstrings with Args, Returns, Raises, Examples
- [ ] Format code: `ruff format src/supermetrics/resources/login_links.py`
- [ ] Type check: `mypy src/supermetrics/resources/login_links.py`

### Task 2: Create LoginLinksAsyncResource (async) (AC: 4, 6, 7)
- [ ] In same file, define `LoginLinksAsyncResource` class
- [ ] Import async client: `from supermetrics_sdk._generated.async_client import AsyncClient as GeneratedAsyncClient`
- [ ] Implement async versions of all methods:
  - `async def create(...) -> LoginLink`
  - `async def get(...) -> LoginLink`
  - `async def list(...) -> list[LoginLink]`
  - `async def close(...) -> None`
- [ ] Add same error handling and logging as sync version
- [ ] Add complete type hints and docstrings
- [ ] Ensure async methods use `await` for generated client calls

### Task 3: Attach resources to clients (AC: 5)
- [ ] Edit `src/supermetrics/client.py`
- [ ] Import: `from supermetrics_sdk.resources.login_links import LoginLinksResource`
- [ ] In `__init__`, add: `self.login_links = LoginLinksResource(self._client)`
- [ ] Edit `src/supermetrics/async_client.py`
- [ ] Import: `from supermetrics_sdk.resources.login_links import LoginLinksAsyncResource`
- [ ] In `__init__`, add: `self.login_links = LoginLinksAsyncResource(self._client)`

### Task 4: Create unit tests for LoginLinksResource (AC: 8)
- [ ] Create `tests/unit/test_login_links.py`
- [ ] Add fixtures for mock responses in `tests/conftest.py`:
  ```python
  @pytest.fixture
  def mock_login_link_response():
      return {
          "link_id": "link_123",
          "ds_id": "GA4",
          "ds_name": "Test Link",
          "login_url": "https://auth.supermetrics.com/link_123",
          "status_code": "OPEN",
          ...
      }
  ```
- [ ] Test `create()` method:
  - Mock httpx response with successful creation
  - Call `client.login_links.create(ds_id="GA4", description="Test")`
  - Verify returned LoginLink has correct attributes
  - Verify generated client method was called with correct parameters
- [ ] Test `get()` method:
  - Mock httpx response
  - Call `client.login_links.get(link_id="link_123")`
  - Verify LoginLink returned
- [ ] Test `list()` method:
  - Mock httpx response with list of login links
  - Call `client.login_links.list()`
  - Verify list of LoginLink objects returned
- [ ] Test `close()` method:
  - Mock httpx response
  - Call `client.login_links.close(link_id="link_123")`
  - Verify no return value (None)
- [ ] Test error scenarios:
  - 401 error → raises `AuthenticationError`
  - 400 error → raises `ValidationError`
  - 404 error → raises `APIError`
  - Network error → raises `NetworkError`
- [ ] Test async versions of all methods (using `@pytest.mark.asyncio`)
- [ ] Run tests: `pytest tests/unit/test_login_links.py -v`

### Task 5: Update __init__.py exports (AC: 6)
- [ ] Edit `src/supermetrics/__init__.py`
- [ ] Consider whether to export resource classes (likely not - accessed via client.login_links)
- [ ] Verify public API: `from supermetrics_sdk import SupermetricsClient` and `client.login_links` works

### Task 6: Run code quality checks (AC: 7)
- [ ] Run mypy: `mypy src/`
- [ ] Fix any type errors
- [ ] Run ruff format: `ruff format src/`
- [ ] Run ruff check: `ruff check src/`
- [ ] Fix any linting issues

## Dev Notes

### Architecture Alignment

**Resource Adapter Pattern:**
- Hand-written resource classes wrap generated API endpoints
- Provide clean, Pythonic method names
- Map exceptions from httpx to SDK exceptions
- Add logging for observability
- [Source: architecture.md - Resource Adapter Pattern, lines 556-679]

**Error Handling Pattern:**
- Catch `httpx.HTTPStatusError` and `httpx.RequestError`
- Map status codes: 401→AuthenticationError, 400→ValidationError, 404/5xx→APIError
- Network errors → NetworkError
- Include context in exceptions (status_code, endpoint, response_body)
- [Source: architecture.md - Exception Mapping Pattern, lines 917-969]

**Logging Pattern:**
- Use `logging.getLogger(__name__)`
- DEBUG: Log method calls with parameters (ds_id, etc.)
- INFO: Log successful operations (link created, id=...)
- ERROR: Log failures with exception info
- NEVER log sensitive data (API keys)
- [Source: architecture.md - Logging Strategy, lines 1186-1251]

### Project Structure Notes

After this story, structure will include:
```
src/supermetrics/
├── client.py                   # UPDATED: Attach login_links resource
├── async_client.py             # UPDATED: Attach login_links async resource
└── resources/                  # NEW: Resource adapters directory
    ├── __init__.py
    └── login_links.py          # NEW: LoginLinks resource (sync + async)

tests/unit/
└── test_login_links.py         # NEW: LoginLinks tests
```

### API Interface Reference

**LoginLinksResource API (from tech spec):**
```python
# Create login link
link: LoginLink = client.login_links.create(
    ds_id: str,                      # Data source ID (e.g., "GA4")
    description: str,                # Human-readable description
    **kwargs                         # Additional API parameters
) -> LoginLink

# Get login link by ID
link: LoginLink = client.login_links.get(link_id: str) -> LoginLink

# List all login links
links: list[LoginLink] = client.login_links.list() -> list[LoginLink]

# Close/expire login link
client.login_links.close(link_id: str) -> None
```

[Source: tech-spec-epic-1.md - LoginLinksResource API, lines 179-196]

### LoginLink Model (from updated tech spec)

Based on actual API schema:
```python
class LoginLink(BaseModel):
    link_id: str                      # Unique login link identifier
    ds_id: str                        # Data source ID
    ds_name: str                      # Human-readable description
    login_url: str                    # Full URL for authentication
    require_username: Optional[str]   # Required username if any
    redirect_url: Optional[str]       # Custom redirect URL
    redirect_verifier: Optional[str]  # Verifier string
    owner_user_id: Optional[str]      # Owner user ID
    owner_user_email: Optional[str]   # Owner email
    login_id: Optional[str]           # Login ID after successful auth
    login_username: Optional[str]     # Username used to authenticate
    created_at: datetime              # Creation timestamp
    expires_at: Optional[datetime]    # Expiration timestamp
    login_at: Optional[datetime]      # Authentication timestamp
    status_code: str                  # "OPEN", "CLOSED", "EXPIRED"
```

[Source: tech-spec-epic-1.md - LoginLink Model, lines 97-115]

### Error Handling Implementation

**HTTP Status Code Mapping:**
```python
def _map_http_exception(self, error: httpx.HTTPStatusError) -> SupermetricsError:
    status_code = error.response.status_code
    endpoint = str(error.request.url)
    response_text = error.response.text

    if status_code == 401:
        return AuthenticationError(
            "Invalid or expired API key",
            status_code=status_code,
            endpoint=endpoint,
            response_body=response_text
        )
    elif status_code == 400:
        return ValidationError(
            f"Invalid request parameters: {response_text}",
            status_code=status_code,
            endpoint=endpoint,
            response_body=response_text
        )
    # ... more mappings
```

[Source: architecture.md - Exception Mapping Pattern, lines 638-678]

### Testing Strategy

**Unit Tests with httpx Mocking:**
- Use httpx MockTransport or mock the generated client methods
- Test each CRUD operation (create, get, list, close)
- Test error scenarios for each status code
- Test both sync and async versions
- No real API calls - all mocked

**Test Structure:**
```python
def test_create_login_link_success(mocker, test_api_key):
    # Arrange: Mock generated client method
    mock_response = LoginLink(link_id="link_123", ...)
    mocker.patch.object(generated_client, 'create_login_link', return_value=mock_response)

    # Act: Call adapter method
    client = SupermetricsClient(api_key=test_api_key)
    link = client.login_links.create(ds_id="GA4", description="Test")

    # Assert: Verify result
    assert link.link_id == "link_123"
    assert link.ds_id == "GA4"
```

[Source: tech-spec-epic-1.md - Test Strategy, lines 708-742]

### References

- [Source: tech-spec-epic-1.md - Acceptance Criteria #4, lines 561-568] - Story AC definition
- [Source: epics.md - Story 1.4, lines 95-113] - Original story specification
- [Source: architecture.md - Resource Adapter Pattern, lines 556-679] - Complete implementation pattern
- [Source: tech-spec-epic-1.md - LoginLinksResource API, lines 179-196] - API interface
- [Source: tech-spec-epic-1.md - LoginLink Model, lines 97-115] - Data model

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
