# Story 1.3: Create Adapter Pattern Foundation

Status: Done
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
- [x] Create `src/supermetrics/client.py`
- [x] Import generated client: `from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient`
- [x] Define `SupermetricsClient` class with `__init__` method:
  - Parameters: `api_key: str`, `user_agent: str | None = None`, `custom_headers: dict[str, str] | None = None`, `timeout: float = 30.0`, `base_url: str = "https://api.supermetrics.com"`
- [x] Build headers dict:
  - `Authorization: Bearer {api_key}`
  - `User-Agent: supermetrics-sdk/{version} python/{py_version}` (default)
  - Merge custom_headers if provided (user headers take precedence)
- [x] Create internal `_client` instance: `GeneratedClient(base_url=base_url, headers=headers, timeout=httpx.Timeout(timeout))`
- [x] Add `close()` method for cleanup
- [x] Add context manager support (`__enter__` and `__exit__`)
- [x] Add complete type hints to all methods
- [x] Add Google-style docstrings with parameter descriptions, return types, and usage examples
- [x] Format code with ruff: `ruff format src/supermetrics/client.py`
- [x] Type check with mypy: `mypy src/supermetrics/client.py --strict`

### Task 2: Create SupermetricsAsyncClient (async) (AC: 2, 3, 5, 6, 7)
- [x] Create `src/supermetrics/async_client.py`
- [x] Import generated client: `from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient` (supports both sync and async)
- [x] Define `SupermetricsAsyncClient` class with same `__init__` signature as sync client
- [x] Build headers dict (identical to sync client)
- [x] Create internal `_client` instance with `GeneratedClient`
- [x] Add async `close()` method: `async def close()`
- [x] Add async context manager support (`__aenter__` and `__aexit__`)
- [x] Add complete type hints
- [x] Add Google-style docstrings
- [x] Format with ruff: `ruff format src/supermetrics/async_client.py`
- [x] Type check with mypy: `mypy src/supermetrics/async_client.py --strict`

### Task 3: Update __init__.py to export public API (AC: 4)
- [x] Edit `src/supermetrics/__init__.py`
- [x] Import client classes:
  ```python
  from supermetrics.client import SupermetricsClient
  from supermetrics.async_client import SupermetricsAsyncClient
  ```
- [x] Import version:
  ```python
  from supermetrics.__version__ import __version__
  ```
- [x] Define `__all__`:
  ```python
  __all__ = [
      "SupermetricsClient",
      "SupermetricsAsyncClient",
      "__version__",
  ]
  ```
- [x] Verify public API works: Tests confirm imports work correctly

### Task 4: Create tests/conftest.py with shared fixtures (AC: 8)
- [x] Create `tests/conftest.py`
- [x] Add pytest fixture for test API key:
  ```python
  @pytest.fixture
  def test_api_key():
      return "test-api-key-12345"
  ```
- [x] Add fixture for mock headers:
  ```python
  @pytest.fixture
  def expected_headers(test_api_key):
      return {
          "Authorization": f"Bearer {test_api_key}",
          # User-Agent is dynamic
      }
  ```

### Task 5: Create unit tests for client initialization (AC: 8)
- [x] Create `tests/unit/test_client_init.py`
- [x] Test sync client initialization:
  - Initialize client with API key
  - Verify `_client` instance created
  - Verify headers include Authorization bearer token
  - Verify default User-Agent header
- [x] Test sync client with custom headers:
  - Initialize with custom_headers dict
  - Verify custom headers merged with defaults
  - Verify user headers override defaults
- [x] Test sync client context manager:
  - Use `with SupermetricsClient(...)` pattern
  - Verify client initializes and closes properly
- [x] Test async client initialization (similar tests with async/await):
  - Initialize async client
  - Verify headers
  - Verify custom headers merge
- [x] Test async client context manager:
  - Use `async with SupermetricsAsyncClient(...)` pattern
  - Verify async cleanup
- [x] Run tests: `pytest tests/unit/test_client_init.py -v` (19/19 tests passing)

### Task 6: Run mypy type checking (AC: 6)
- [x] Run mypy on entire src directory: `mypy src/`
- [x] Fix any type errors reported
- [x] Verify all public methods have complete type hints
- [x] Verify no `Any` types in public API (strict mode passing)

### Task 7: Run ruff formatting and linting (AC: 7)
- [x] Format code: `ruff format src/`
- [x] Check linting: `ruff check src/`
- [x] Fix any linting issues (auto-fixed Optional → X | None syntax)
- [x] Verify code follows Python conventions (all checks passed)

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

- Story Context XML: `spec/stories/story-context-1.3.xml`
- Generated: 2025-11-25

### Agent Model Used

<!-- To be filled by dev agent -->

### Debug Log References

<!-- To be filled by dev agent -->

### Completion Notes List

**Implementation Summary:**

Successfully implemented the adapter pattern foundation for the Supermetrics SDK with complete dual sync/async support. Both client classes wrap the generated code and provide a stable public API that shields users from monthly OpenAPI regeneration changes.

**Key Accomplishments:**

1. **SupermetricsClient (sync)** - `src/supermetrics/client.py:1-124`
   - Full initialization with API key, custom headers, user-agent, timeout, and base URL
   - Automatic Authorization header injection (Bearer token)
   - Dynamic User-Agent construction: `supermetrics-sdk/{version} python/{py_version}`
   - Context manager support for proper resource cleanup
   - Complete type hints with strict mypy compliance
   - Comprehensive Google-style docstrings

2. **SupermetricsAsyncClient** - `src/supermetrics/async_client.py:1-121`
   - Identical interface to sync client but with async methods
   - Async context manager (`__aenter__`, `__aexit__`)
   - Properly wraps generated client's async methods

3. **Public API Exports** - `src/supermetrics/__init__.py:1-14`
   - Clean public interface with both clients and version
   - Users can import: `from supermetrics import SupermetricsClient, SupermetricsAsyncClient`

4. **Test Coverage** - 19 comprehensive tests covering:
   - Client initialization with various configurations
   - Header injection and merging (default + custom)
   - Context manager behavior (sync and async)
   - Custom base URL and timeout parameters
   - Public API import verification

**Technical Notes:**

- Generated client uses single `Client` class for both sync/async (not separate classes)
- Timeout parameter converted to `httpx.Timeout` object for compatibility
- Modern Python 3.10+ type syntax used (`X | None` instead of `Optional[X]`)
- All code passes mypy strict mode, ruff formatting, and ruff linting
- No breaking changes on monthly regeneration due to adapter isolation

**Quality Metrics:**

- ✅ 19/19 tests passing
- ✅ 100% mypy strict mode compliance
- ✅ All ruff checks passed
- ✅ All acceptance criteria met

### File List

**Created:**
- `src/supermetrics/client.py` - Synchronous client with adapter pattern implementation
- `src/supermetrics/async_client.py` - Asynchronous client with adapter pattern implementation
- `tests/unit/test_client_init.py` - Comprehensive client initialization tests (19 tests)

**Modified:**
- `src/supermetrics/__init__.py` - Added public API exports for both client classes
- `tests/conftest.py` - Added test fixtures for API key and expected headers
