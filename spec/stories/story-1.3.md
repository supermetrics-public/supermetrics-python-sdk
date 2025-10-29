# Story 1.3: Create Adapter Pattern Foundation

Status: Draft
Created: 2025-10-28
Epic: 1 - Project Foundation & Core SDK Generation

## Story

As a developer,
I want a stable public API layer that wraps the generated code,
so that monthly OpenAPI regeneration won't break existing users.

## Acceptance Criteria

1. `src/supermetrics/client.py` created with `SupermetricsClient` class accepting `api_key`, optional `user_agent`, and `custom_headers` parameters
2. `src/supermetrics/async_client.py` created with `SupermetricsAsyncClient` class with same initialization signature
3. Both clients wrap `_generated` client with custom headers injection
4. `src/supermetrics/__init__.py` exports public API (both client classes)
5. Complete type hints and docstrings added to public client classes
6. Code passes `mypy` strict type checking
7. Code formatted with `black` or `ruff` formatter
8. Simple initialization test added (`tests/test_client_init.py`)

## Tasks / Subtasks

### Task 1: Create SupermetricsClient (sync) (AC: 1, 3, 5, 6, 7)
- [ ] Create `src/supermetrics/client.py`
- [ ] Import generated client: `from supermetrics_sdk._generated.client import Client as GeneratedClient`
- [ ] Define `SupermetricsClient` class with `__init__` method:
  - Parameters: `api_key: str`, `user_agent: Optional[str] = None`, `custom_headers: Optional[dict[str, str]] = None`, `timeout: float = 30.0`, `base_url: str = "https://api.supermetrics.com"`
- [ ] Build headers dict:
  - `Authorization: Bearer {api_key}`
  - `User-Agent: supermetrics-sdk/{version} python/{py_version}` (default)
  - Merge custom_headers if provided (user headers take precedence)
- [ ] Create internal `_client` instance: `GeneratedClient(base_url=base_url, headers=headers, timeout=timeout)`
- [ ] Add `close()` method for cleanup
- [ ] Add context manager support (`__enter__` and `__exit__`)
- [ ] Add complete type hints to all methods
- [ ] Add Google-style docstrings with parameter descriptions, return types, and usage examples
- [ ] Format code with ruff: `ruff format src/supermetrics/client.py`
- [ ] Type check with mypy: `mypy src/supermetrics/client.py`

### Task 2: Create SupermetricsAsyncClient (async) (AC: 2, 3, 5, 6, 7)
- [ ] Create `src/supermetrics/async_client.py`
- [ ] Import generated async client: `from supermetrics_sdk._generated.async_client import AsyncClient as GeneratedAsyncClient`
- [ ] Define `SupermetricsAsyncClient` class with same `__init__` signature as sync client
- [ ] Build headers dict (identical to sync client)
- [ ] Create internal `_client` instance with `GeneratedAsyncClient`
- [ ] Add async `close()` method: `async def close()`
- [ ] Add async context manager support (`__aenter__` and `__aexit__`)
- [ ] Add complete type hints
- [ ] Add Google-style docstrings
- [ ] Format with ruff: `ruff format src/supermetrics/async_client.py`
- [ ] Type check with mypy: `mypy src/supermetrics/async_client.py`

### Task 3: Update __init__.py to export public API (AC: 4)
- [ ] Edit `src/supermetrics/__init__.py`
- [ ] Import client classes:
  ```python
  from supermetrics_sdk.client import SupermetricsClient
  from supermetrics_sdk.async_client import SupermetricsAsyncClient
  ```
- [ ] Import version:
  ```python
  from supermetrics_sdk.__version__ import __version__
  ```
- [ ] Define `__all__`:
  ```python
  __all__ = [
      "SupermetricsClient",
      "SupermetricsAsyncClient",
      "__version__",
  ]
  ```
- [ ] Verify public API works: `python -c "from supermetrics_sdk import SupermetricsClient, SupermetricsAsyncClient"`

### Task 4: Create tests/conftest.py with shared fixtures (AC: 8)
- [ ] Create `tests/conftest.py`
- [ ] Add pytest fixture for test API key:
  ```python
  @pytest.fixture
  def test_api_key():
      return "test-api-key-12345"
  ```
- [ ] Add fixture for mock headers:
  ```python
  @pytest.fixture
  def expected_headers(test_api_key):
      return {
          "Authorization": f"Bearer {test_api_key}",
          "User-Agent": "supermetrics-sdk/0.1.0 python/3.10",  # Adjust version
      }
  ```

### Task 5: Create unit tests for client initialization (AC: 8)
- [ ] Create `tests/unit/test_client_init.py`
- [ ] Test sync client initialization:
  - Initialize client with API key
  - Verify `_client` instance created
  - Verify headers include Authorization bearer token
  - Verify default User-Agent header
- [ ] Test sync client with custom headers:
  - Initialize with custom_headers dict
  - Verify custom headers merged with defaults
  - Verify user headers override defaults
- [ ] Test sync client context manager:
  - Use `with SupermetricsClient(...)` pattern
  - Verify client initializes and closes properly
- [ ] Test async client initialization (similar tests with async/await):
  - Initialize async client
  - Verify headers
  - Verify custom headers merge
- [ ] Test async client context manager:
  - Use `async with SupermetricsAsyncClient(...)` pattern
  - Verify async cleanup
- [ ] Run tests: `pytest tests/unit/test_client_init.py -v`

### Task 6: Run mypy type checking (AC: 6)
- [ ] Run mypy on entire src directory: `mypy src/`
- [ ] Fix any type errors reported
- [ ] Verify all public methods have complete type hints
- [ ] Verify no `Any` types in public API

### Task 7: Run ruff formatting and linting (AC: 7)
- [ ] Format code: `ruff format src/`
- [ ] Check linting: `ruff check src/`
- [ ] Fix any linting issues
- [ ] Verify code follows Python conventions

## Dev Notes

### Architecture Alignment

**Adapter Pattern:**
- Hand-written stable public API wraps regeneratable generated code
- Protects users from breaking changes during monthly regeneration
- Allows custom logic (error handling, logging) without modifying generated code
- [Source: architecture.md - ADR-001: Use Adapter Pattern, lines 1898-1917]

**Dual Sync/Async Support:**
- Separate client classes: `SupermetricsClient` (sync) and `SupermetricsAsyncClient` (async)
- Identical initialization signatures
- Type safety: clear distinction between sync and async APIs
- [Source: architecture.md - ADR-002: Separate Sync/Async Clients, lines 1922-1944]

**Client Initialization Pattern:**
- Accept `api_key`, `user_agent`, `custom_headers`, `timeout`, `base_url`
- Build headers with Authorization bearer token
- Inject headers into generated client
- Resource adapters will be attached in later stories (1.4-1.7)
- [Source: architecture.md - Client Initialization Pattern, lines 976-1077]

### Project Structure Notes

After this story, structure will include:
```
src/supermetrics/
├── __init__.py                 # UPDATED: Export SupermetricsClient, SupermetricsAsyncClient
├── __version__.py              # Existing from Story 1.1
├── client.py                   # NEW: Sync client
├── async_client.py             # NEW: Async client
└── _generated/                 # Existing from Story 1.2
    ├── client.py               # Generated sync client (wrapped)
    └── async_client.py         # Generated async client (wrapped)

tests/
├── conftest.py                 # NEW: Shared fixtures
└── unit/
    └── test_client_init.py     # NEW: Client initialization tests
```

### Key Implementation Details

**Header Injection Pattern:**
```python
import sys
from supermetrics_sdk.__version__ import __version__

py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "User-Agent": user_agent or default_user_agent,
}

if custom_headers:
    headers.update(custom_headers)  # User headers override defaults
```

[Source: architecture.md - Client Initialization Pattern, lines 1029-1043]

**Context Manager Pattern:**
```python
# Sync client
def __enter__(self):
    return self

def __exit__(self, *args):
    self.close()

# Async client
async def __aenter__(self):
    return self

async def __aexit__(self, *args):
    await self.close()
```

[Source: architecture.md - Client Initialization Pattern, lines 1071-1077, 1177-1183]

### Testing Standards

**Framework:** pytest with pytest-asyncio
- Unit tests for client initialization
- Test both sync and async clients
- Test default and custom headers
- Test context managers
- Use fixtures from conftest.py

**No mocking needed yet** - testing initialization only, not API calls
- Verify `_client` instance created
- Verify headers constructed correctly
- Later stories will add httpx mocking for API calls

[Source: tech-spec-epic-1.md - Test Strategy Summary, lines 708-713]

### Type Checking Requirements

**mypy strict mode:**
- All public methods must have complete type hints
- No `Any` types in public API
- Use `Optional[T]` for optional parameters
- Use `dict[str, str]` for dictionaries (Python 3.10+ syntax)

**Example type hints:**
```python
def __init__(
    self,
    api_key: str,
    *,
    user_agent: Optional[str] = None,
    custom_headers: Optional[dict[str, str]] = None,
    timeout: float = 30.0,
    base_url: str = "https://api.supermetrics.com"
) -> None:
    ...
```

[Source: architecture.md - Type Hints, lines 682-713]

### Docstring Format (Google Style)

**Required for all public APIs:**
```python
def __init__(
    self,
    api_key: str,
    *,
    user_agent: Optional[str] = None,
    ...
) -> None:
    """Initialize Supermetrics client.

    Args:
        api_key: Supermetrics API key (required)
        user_agent: Custom User-Agent header. Defaults to
            "supermetrics-sdk/{version} python/{py_version}"
        custom_headers: Additional HTTP headers for all requests
        timeout: Request timeout in seconds (default: 30.0)
        base_url: API base URL (default: production API)

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Use client for API calls
    """
```

[Source: architecture.md - Docstring Format, lines 750-823]

### References

- [Source: tech-spec-epic-1.md - Acceptance Criteria #3, lines 551-559] - Story AC definition
- [Source: epics.md - Story 1.3, lines 75-93] - Original story specification
- [Source: architecture.md - Client Initialization Pattern, lines 976-1184] - Complete implementation pattern
- [Source: architecture.md - Type Hints, lines 682-747] - Type hint requirements
- [Source: architecture.md - Docstring Format, lines 750-843] - Documentation standards

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
