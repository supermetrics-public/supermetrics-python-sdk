# Decision Architecture - Supermetrics Python SDK

**Project:** Supermetrics python SDK
**Author:** Aleksei
**Date:** 2025-10-27
**Project Level:** 2 - Greenfield Software Project
**Architecture Type:** Adapter Pattern + Resource-Based + Dual Sync/Async

---

## Executive Summary

The Supermetrics Python SDK architecture leverages modern Python tooling with an adapter pattern wrapping OpenAPI-generated code. This approach enables monthly API regeneration without breaking users while providing a type-safe, resource-based developer experience. The dual sync/async client design supports both notebook-based exploration and production async pipelines. Built on proven technologies (openapi-python-client + httpx + Pydantic v2), the architecture prioritizes stability, maintainability, and rapid POC delivery within 1-2 weeks.

---

## Project Initialization

**First implementation story (Story 1.1) should execute:**

```bash
# Step 1: Initialize project structure using cookiecutter-pypackage
pip install -U cookiecutter
cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage.git

# Answer prompts:
# - project_name: supermetrics-sdk
# - project_slug: supermetrics_sdk
# - author_name: Supermetrics
# - email: support@supermetrics.com
# - project_short_description: Official Python SDK for Supermetrics API
# - version: 0.1.0
# - use_pytest: yes
# - use_pypi_deployment_with_travis: no (we'll use GitHub Actions)
# - command_line_interface: no
# - open_source_license: Apache Software License 2.0

# Step 2: Convert to uv package management
cd supermetrics-sdk
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Step 3: Update pyproject.toml to use hatchling build system
# (Manual edit - see pyproject.toml section below)

# Step 4: Add open source governance files
# Create: CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
# Create: .github/ISSUE_TEMPLATE/, .github/PULL_REQUEST_TEMPLATE.md

# Step 5: Initialize git repository
git init
git add .
git commit -m "Initial project structure from cookiecutter"
```

**This establishes the base architecture with these decisions:**
- Project structure: src-layout (modern best practice)
- Build system: hatchling (pyproject.toml native, fast)
- Package manager: uv (fast, modern dependency management)
- Testing: pytest with fixtures
- License: Apache 2.0
- CI/CD: GitHub Actions foundation
- Open source: Comprehensive governance templates

---

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale | Provided By |
|----------|----------|---------|---------------|-----------|-------------|
| **OpenAPI Generator** | openapi-python-client | latest stable | Epic 1 (Story 1.2) | Built-in dual sync/async, fast POC timeline, excellent type safety, minimal deps | Manual |
| **HTTP Client** | httpx | latest stable | Epic 1 (all stories) | Only library with dual sync/async support, type-safe, modern | openapi-python-client |
| **Data Validation** | Pydantic v2 | latest stable | Epic 1 (all stories) | Industry standard, auto-generated from OpenAPI, excellent type safety | openapi-python-client |
| **Build System** | hatchling | latest stable | Epic 1 (Story 1.1), Epic 2 (Story 2.5) | Modern, pyproject.toml native, fast builds | Manual |
| **Package Manager** | uv | latest stable | Epic 1 (Story 1.1) | Fast dependency resolution, lockfile support, modern Python tooling | Manual |
| **Code Quality** | ruff | latest stable | Epic 1 (all stories) | All-in-one linter/formatter, fast, replaces black+flake8+isort | Manual |
| **Testing Framework** | pytest | latest stable | Epic 1 (Story 1.8), Epic 2 (Story 2.1) | Standard Python testing, extensive plugin ecosystem | Starter template |
| **Async Testing** | pytest-asyncio | latest stable | Epic 1 (Stories 1.4-1.7), Epic 2 (Story 2.1) | Async test support for dual client testing | Manual |
| **Test Coverage** | pytest-cov | latest stable | Epic 2 (Story 2.1) | Coverage measurement, 80%+ target | Starter template |
| **HTTP Mocking** | httpx (built-in MockTransport) | latest stable | Epic 2 (Story 2.1) | Native httpx testing support, no additional deps | httpx |
| **Documentation** | MkDocs | latest stable | Epic 2 (Story 2.2) | Markdown-native, simple, great for SDK docs | Manual |
| **CI/CD** | GitHub Actions | N/A | Epic 2 (Story 2.4, 2.6, 2.7) | Native GitHub integration, free for open source | Starter template |
| **Python Versions** | 3.10, 3.11, 3.12 | N/A | All epics | Modern type hints, active maintenance | Manual |
| **Project Layout** | src-layout | N/A | Epic 1 (Story 1.1) | Prevents import issues, best practice | Manual |
| **Architecture Pattern** | Adapter + Resource-Based + Dual Sync/Async | N/A | Epic 1 (all stories) | Stable API, monthly regeneration, type safety | Technical Research |
| **Logging** | stdlib logging | N/A | All epics | Simple, extensible, no additional deps | Manual |
| **Date Handling** | python-dateutil | latest stable | Epic 1 (Stories 1.4-1.7) | ISO 8601 parsing, timezone support | openapi-python-client |
| **Exception Hierarchy** | 4-level (base + 4 types) | N/A | Epic 1 (Story 1.8) | Clear error semantics, HTTP status mapping | Manual |
| **Version Management** | Manual (semver) | N/A | Epic 2 (Story 2.5-2.6) | Simple, defer automation to Phase 2 | Manual |

---

## Project Structure

```
supermetrics-sdk/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml              # Story 2.2: Bug report template
│   │   ├── feature_request.yml         # Story 2.2: Feature request template
│   │   └── config.yml                  # Issue template configuration
│   ├── PULL_REQUEST_TEMPLATE.md        # Story 2.2: PR checklist
│   └── workflows/
│       ├── test.yml                    # Story 2.4: Multi-Python testing (3.10, 3.11, 3.12)
│       ├── publish.yml                 # Story 2.6: PyPI publishing on release
│       ├── pr-checks.yml               # Strict PR validation (ruff, mypy, tests)
│       └── regenerate.yml              # Story 2.7: Monthly OpenAPI regeneration
│
├── .gitignore                          # Python, IDE, OS ignores
├── .pre-commit-config.yaml             # ruff, mypy hooks
├── LICENSE                             # Apache 2.0
├── README.md                           # Story 2.2: Quick-start guide
├── CONTRIBUTING.md                     # Story 2.2: Contribution guidelines
├── CODE_OF_CONDUCT.md                  # Story 2.2: Community standards
├── SECURITY.md                         # Story 2.2: Vulnerability reporting
├── CHANGELOG.md                        # Version history
├── pyproject.toml                      # Story 1.1, 2.5: Project metadata, deps, build config
├── uv.lock                             # uv dependency lockfile
├── openapi-spec.yaml                   # Story 1.2: OpenAPI source of truth
│
├── scripts/
│   ├── regenerate_client.sh            # Story 1.2: OpenAPI regeneration script
│   └── setup_dev.sh                    # Development environment setup
│
├── src/
│   └── supermetrics_sdk/
│       ├── __init__.py                 # Public API exports (clients, exceptions)
│       ├── __version__.py              # Version string (e.g., "1.0.0")
│       ├── client.py                   # Story 1.3: SupermetricsClient (sync)
│       ├── async_client.py             # Story 1.3: SupermetricsAsyncClient (async)
│       ├── exceptions.py               # Story 1.8: Custom exception hierarchy
│       ├── _logger.py                  # Internal logging configuration
│       │
│       ├── resources/                  # Stories 1.4-1.7: Resource adapters
│       │   ├── __init__.py
│       │   ├── base.py                 # Base resource class with shared utilities
│       │   ├── login_links.py          # Story 1.4: LoginLinksResource
│       │   ├── logins.py               # Story 1.5: LoginsResource
│       │   ├── accounts.py             # Story 1.6: AccountsResource
│       │   └── queries.py              # Story 1.7: QueriesResource
│       │
│       └── _generated/                 # Story 1.2: Generated code (INTERNAL, never edit)
│           ├── __init__.py
│           ├── client.py               # Generated sync client
│           ├── async_client.py         # Generated async client
│           ├── api/                    # Generated API endpoints
│           │   ├── __init__.py
│           │   ├── login_links/
│           │   ├── logins/
│           │   ├── accounts/
│           │   └── queries/
│           └── models/                 # Generated Pydantic models
│               ├── __init__.py
│               ├── login_link.py
│               ├── login.py
│               ├── account.py
│               └── ...
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # pytest fixtures (mock httpx, test data)
│   ├── fixtures/
│   │   ├── mock_responses.json         # Mock API response data
│   │   └── test_data.py                # Shared test data and factories
│   │
│   ├── unit/                           # Unit tests (80%+ coverage target)
│   │   ├── __init__.py
│   │   ├── test_client_init.py         # Story 1.3: Client initialization tests
│   │   ├── test_login_links.py         # Story 1.4: LoginLinksResource tests
│   │   ├── test_logins.py              # Story 1.5: LoginsResource tests
│   │   ├── test_accounts.py            # Story 1.6: AccountsResource tests
│   │   ├── test_queries.py             # Story 1.7: QueriesResource tests
│   │   └── test_exceptions.py          # Story 1.8: Exception handling tests
│   │
│   └── integration/                    # Integration tests (httpx mock)
│       ├── __init__.py
│       ├── test_complete_flow.py       # Story 1.9: Sync complete flow
│       └── test_async_flow.py          # Story 1.9: Async complete flow
│
├── examples/
│   ├── complete_flow.py                # Story 1.9: Sync example (login → query)
│   ├── async_flow.py                   # Story 1.9: Async example
│   └── notebooks/
│       ├── quickstart.ipynb            # Story 2.3: Quick-start notebook
│       └── complete_workflow.ipynb     # Story 2.3: Complete workflow notebook
│
└── docs/
    ├── index.md                        # Story 2.2: Documentation home
    ├── installation.md                 # Installation guide
    ├── quickstart.md                   # Quick-start tutorial
    ├── authentication.md               # Authentication guide
    ├── user-guide/
    │   ├── sync-client.md              # Synchronous client usage
    │   ├── async-client.md             # Asynchronous client usage
    │   ├── error-handling.md           # Error handling patterns
    │   └── advanced.md                 # Advanced usage
    ├── api-reference/                  # Auto-generated API docs
    │   ├── client.md
    │   ├── resources.md
    │   └── exceptions.md
    └── mkdocs.yml                      # MkDocs configuration
```

---

## Epic to Architecture Mapping

| Epic | Stories | Architecture Components | Purpose |
|------|---------|------------------------|---------|
| **Epic 1: Project Foundation & Core SDK Generation** | Stories 1.1-1.9 | Project structure, generated code, adapter layer, resources, examples | Establish infrastructure and implement POC SDK with complete onboarding flow |
| Story 1.1 | Initialize Python Project Structure | `pyproject.toml`, src-layout, `.github/`, governance docs | Professional project foundation with modern tooling |
| Story 1.2 | Generate Initial SDK from OpenAPI | `_generated/` directory, `openapi-spec.yaml`, `scripts/regenerate_client.sh` | Auto-generated type-safe client code from API specification |
| Story 1.3 | Create Adapter Pattern Foundation | `client.py`, `async_client.py`, header injection, resource attachment | Stable public API wrapping generated code for regeneration safety |
| Story 1.4 | Implement Login Links Resource | `resources/login_links.py`, sync/async resource classes | Clean interface for login link CRUD operations |
| Story 1.5 | Implement Logins Resource | `resources/logins.py` | Retrieve login information after user authentication |
| Story 1.6 | Implement Accounts Resource | `resources/accounts.py` | Discover available data source accounts for queries |
| Story 1.7 | Implement Queries Resource | `resources/queries.py` | Execute data queries with parameter validation |
| Story 1.8 | Create Basic Error Handling | `exceptions.py`, exception hierarchy, HTTP→exception mapping | Clear, actionable error messages for SDK users |
| Story 1.9 | Create POC Example and Validation | `examples/complete_flow.py`, `examples/async_flow.py` | Demonstrate complete onboarding flow for POC validation |
| **Epic 2: Production SDK & Distribution** | Stories 2.1-2.8 | Tests, docs, CI/CD, PyPI, regeneration workflows | Transform POC into production-ready public package |
| Story 2.1 | Expand Test Coverage to 80%+ | `tests/unit/`, `tests/integration/`, fixtures | Comprehensive testing for reliability and regression prevention |
| Story 2.2 | Create Comprehensive Documentation | `docs/`, `README.md`, `CONTRIBUTING.md`, governance | Enable self-service integration with clear guides |
| Story 2.3 | Create Jupyter Notebook Examples | `examples/notebooks/` | Interactive exploration for data scientists |
| Story 2.4 | Setup CI/CD Pipeline | `.github/workflows/test.yml`, multi-Python matrix | Automated quality checks and testing |
| Story 2.5 | Prepare PyPI Package | `pyproject.toml` metadata, build config | Professional package ready for public distribution |
| Story 2.6 | Publish to PyPI and Verify | `.github/workflows/publish.yml`, PyPI automation | Global availability via `pip install supermetrics-sdk` |
| Story 2.7 | Create Regeneration Workflow | `.github/workflows/regenerate.yml`, automation | Keep SDK in sync with API changes via automated regeneration |
| Story 2.8 | Customer Onboarding and Success | POC delivery, feedback collection | Validate SDK meets customer needs and close deal |

---

## Technology Stack Details

### Core Technologies

**Python SDK Generator: openapi-python-client**
- Version: Latest stable
- Purpose: Generate type-safe Python client from OpenAPI 3.x specification
- Key Features:
  - Built-in dual sync/async support via httpx
  - Full Pydantic v2 models for validation
  - Comprehensive type hints throughout
  - Human-readable generated code
- Installation: `uv pip install openapi-python-client`
- Generation Command: `openapi-python-client generate --path openapi-spec.yaml --output-path src/supermetrics/_generated`

**HTTP Client: httpx**
- Version: Latest stable
- Purpose: HTTP client with dual sync/async support
- Key Features:
  - Single library for both sync and async
  - HTTP/1.1 and HTTP/2 support
  - Type hints throughout
  - Built-in test client (MockTransport)
  - Custom headers and User-Agent support
- Usage: Provided by openapi-python-client, users don't interact directly

**Data Validation: Pydantic v2**
- Version: Latest stable
- Purpose: Type-safe request/response models with validation
- Key Features:
  - Automatic validation of all inputs
  - IDE autocomplete support
  - JSON serialization/deserialization
  - Custom validators for complex rules
- Usage: Auto-generated from OpenAPI, exposed in public API

**Package Manager: uv**
- Version: Latest stable
- Purpose: Fast, modern Python package and dependency management
- Key Features:
  - Fast dependency resolution
  - Lockfile support (uv.lock)
  - Compatible with pyproject.toml
  - Virtual environment management
- Installation: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Build System: hatchling**
- Version: Latest stable
- Purpose: Modern Python build backend
- Key Features:
  - pyproject.toml native configuration
  - Fast builds
  - Extensible plugin system
  - Version source integration
- Configuration: Specified in `pyproject.toml` `[build-system]`

**Code Quality: ruff**
- Version: Latest stable
- Purpose: All-in-one Python linter and formatter
- Key Features:
  - Replaces black + flake8 + isort + more
  - Extremely fast (Rust-based)
  - Compatible with existing configs
  - Auto-fix capabilities
- Configuration: `pyproject.toml` `[tool.ruff]`

**Testing: pytest + pytest-asyncio + pytest-cov**
- Versions: Latest stable
- Purpose: Comprehensive testing framework
- pytest: Test runner and framework
- pytest-asyncio: Async test support
- pytest-cov: Coverage measurement
- httpx MockTransport: HTTP mocking without additional dependencies

**Documentation: MkDocs**
- Version: Latest stable
- Purpose: Markdown-based documentation generator
- Key Features:
  - Markdown-native (no RST learning curve)
  - Material theme for modern UI
  - API reference auto-generation
  - Simple deployment (GitHub Pages)
- Plugins: mkdocstrings (API reference from docstrings)

**Date/Time Handling: python-dateutil**
- Version: Latest stable (dependency of openapi-python-client)
- Purpose: ISO 8601 parsing and timezone support
- Usage: Internal date parsing, users receive Python datetime objects

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "openapi-python-client>=0.15.0",
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.4.0",
    "mkdocstrings[python]>=0.24.0",
]
```

### Runtime Dependencies (Minimal - <5 libraries)

```toml
[project]
dependencies = [
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "python-dateutil>=2.8.0",
    "attrs>=23.0.0",
]
```

---

## Integration Points

### OpenAPI Specification → Generated Code

**Flow:**
```
openapi-spec.yaml
    ↓ (openapi-python-client generate)
src/supermetrics/_generated/
    ├── client.py              # Generated sync client
    ├── async_client.py        # Generated async client
    ├── api/                   # Generated endpoint modules
    └── models/                # Generated Pydantic models
```

**Regeneration Process:**
1. Fetch latest `openapi-spec.yaml` from Supermetrics API
2. Run `scripts/regenerate_client.sh`
3. Generated code replaced in `_generated/` directory
4. Run test suite to validate adapter compatibility
5. If tests pass → commit regenerated code
6. If tests fail → update adapters to handle API changes

**Frequency:** On-demand or automated (monthly GitHub Actions workflow)

### Generated Code → Adapter Layer

**Pattern:**
```python
# _generated/client.py (generated, internal)
class Client:
    def create_login_link(self, ds_id: str, description: str) -> LoginLink:
        # Generated implementation
        ...

# resources/login_links.py (hand-written, stable public API)
class LoginLinksResource:
    def __init__(self, client: Client):
        self._client = client

    def create(self, ds_id: str, description: str, **kwargs) -> LoginLink:
        """Stable public method."""
        try:
            return self._client.create_login_link(ds_id, description, **kwargs)
        except GeneratedError as e:
            raise self._map_exception(e)
```

**Key Principle:** Public API (`resources/`) wraps generated code (`_generated/`) to absorb API evolution

### Adapter Layer → User Code

**Export Pattern:**
```python
# src/supermetrics/__init__.py
from supermetrics_sdk.client import SupermetricsClient
from supermetrics_sdk.async_client import SupermetricsAsyncClient
from supermetrics_sdk.exceptions import (
    SupermetricsError,
    AuthenticationError,
    APIError,
    ValidationError,
    NetworkError,
)

__all__ = [
    "SupermetricsClient",
    "SupermetricsAsyncClient",
    "SupermetricsError",
    "AuthenticationError",
    "APIError",
    "ValidationError",
    "NetworkError",
]
```

**User Experience:**
```python
from supermetrics_sdk import SupermetricsClient

client = SupermetricsClient(api_key="your-key")
link = client.login_links.create(ds_id="GAWA", description="Test")
```

### CI/CD → PyPI Distribution

**Automation Flow:**
```
Developer: git tag v1.0.0 + git push --tags
    ↓
GitHub Actions: .github/workflows/publish.yml
    ↓
    1. Checkout code
    2. Install uv
    3. uv build  # Creates wheel and sdist
    4. Publish to PyPI (using PYPI_TOKEN secret)
    ↓
PyPI: Package available at https://pypi.org/project/supermetrics-sdk/
    ↓
Users: pip install supermetrics-sdk
```

---

## Implementation Patterns

### Naming Conventions

**Files & Modules:**
- Python source files: `snake_case.py` (e.g., `login_links.py`, `async_client.py`)
- Test files: `test_<module>.py` (e.g., `test_login_links.py`)
- Private/internal modules: `_<name>.py` (e.g., `_generated/`, `_logger.py`)
- Package names: `snake_case` (e.g., `supermetrics_sdk`)

**Classes:**
- Public classes: `PascalCase` (e.g., `SupermetricsClient`, `LoginLinksResource`)
- Exceptions: `PascalCase` ending in `Error` (e.g., `AuthenticationError`, `APIError`)
- Pydantic models: `PascalCase` (e.g., `LoginLink`, `Account`, `QueryResult`)

**Functions & Methods:**
- Public methods: `snake_case` (e.g., `create()`, `get_by_username()`, `list()`)
- Private methods: `_snake_case` (e.g., `_enrich_error()`, `_build_headers()`, `_map_exception()`)
- Async methods: Same name as sync version (differentiated by class, not name)

**Variables:**
- Local variables: `snake_case` (e.g., `api_key`, `login_link`, `response`)
- Instance variables: `snake_case` (e.g., `self.login_links`, `self.queries`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`, `API_BASE_URL`, `MAX_RETRIES`)
- Private attributes: `_snake_case` (e.g., `self._client`, `self._api_key`, `self._headers`)

**Resource Naming:**
- Resource classes: `<Resource>Resource` or `<Resource>AsyncResource`
  - Examples: `LoginLinksResource`, `QueriesResource`, `LoginLinksAsyncResource`
- Client properties: Plural lowercase with underscores
  - Examples: `client.login_links`, `client.accounts`, `client.queries`

### Code Organization Patterns

**Module Import Order (enforced by ruff):**
```python
# 1. Standard library imports (alphabetical)
import logging
from typing import Optional

# 2. Third-party imports (alphabetical)
import httpx
from pydantic import BaseModel

# 3. Local imports - ALWAYS use absolute imports
from supermetrics_sdk.exceptions import APIError, AuthenticationError
from supermetrics_sdk._generated.client import Client as GeneratedClient
from supermetrics_sdk._generated.models import LoginLink
```

**Class Structure Template:**
```python
class ResourceName:
    """Brief description of the resource.

    Longer description explaining purpose and usage patterns.
    This class manages [specific functionality].
    """

    # Class-level constants (if any)
    DEFAULT_TIMEOUT = 30.0

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the resource.

        Args:
            client: Internal generated client instance
        """
        # Store dependencies
        self._client = client

        # Initialize logger
        self._logger = logging.getLogger(__name__)

    # Public methods (alphabetical order)

    def create(self, ...) -> Model:
        """Create a new resource."""
        ...

    def get(self, ...) -> Model:
        """Retrieve a specific resource."""
        ...

    def list(self, ...) -> list[Model]:
        """List resources."""
        ...

    # Private helper methods (alphabetical order)

    def _build_request(self, ...) -> dict:
        """Build request parameters."""
        ...

    def _map_exception(self, error: Exception) -> SupermetricsError:
        """Map internal exceptions to public API exceptions."""
        ...
```

**Resource Adapter Pattern (MANDATORY for all resources):**
```python
from typing import Optional
import logging
import httpx
from supermetrics_sdk.exceptions import (
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError,
)
from supermetrics_sdk._generated.client import Client as GeneratedClient
from supermetrics_sdk._generated.models import LoginLink

logger = logging.getLogger(__name__)

class LoginLinksResource:
    """Manages login link operations for data source authentication.

    Login links provide a secure way for users to authorize access to their
    data source accounts. Create a login link, share the auth URL with the
    user, then retrieve the login credentials after authorization.
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize login links resource.

        Args:
            client: Internal generated client instance
        """
        self._client = client

    def create(
        self,
        ds_id: str,
        description: str,
        **kwargs
    ) -> LoginLink:
        """Create a new login link for data source authentication.

        Args:
            ds_id: Data source identifier (e.g., "GAWA", "google_ads")
            description: Human-readable description for this login link
            **kwargs: Additional parameters passed to the API

        Returns:
            LoginLink object with id and authentication URL

        Raises:
            AuthenticationError: API key is invalid or expired
            ValidationError: Invalid ds_id or parameters
            APIError: Supermetrics API returned an error
            NetworkError: Network connectivity issue

        Example:
            >>> client = SupermetricsClient(api_key="your-key")
            >>> link = client.login_links.create(
            ...     ds_id="GAWA",
            ...     description="Analytics Dashboard"
            ... )
            >>> print(link.auth_url)
            https://auth.supermetrics.com/...
        """
        logger.debug(f"Creating login link for ds_id={ds_id}")

        try:
            response = self._client.api.create_login_link(
                ds_id=ds_id,
                description=description,
                **kwargs
            )
            logger.info(f"Created login link id={response.id}")
            return response

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating login link: {e}")
            raise self._map_http_exception(e)

        except httpx.RequestError as e:
            logger.error(f"Network error creating login link: {e}")
            raise NetworkError(f"Network error: {str(e)}")

    def _map_http_exception(self, error: httpx.HTTPStatusError) -> SupermetricsError:
        """Map HTTP exceptions to SDK exceptions.

        Args:
            error: HTTP status error from httpx

        Returns:
            Appropriate SupermetricsError subclass
        """
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
        elif status_code >= 500:
            return APIError(
                f"Supermetrics API error: {response_text}",
                status_code=status_code,
                endpoint=endpoint,
                response_body=response_text
            )
        else:
            return APIError(
                f"API error ({status_code}): {response_text}",
                status_code=status_code,
                endpoint=endpoint,
                response_body=response_text
            )
```

### Type Hints (MANDATORY on all public APIs)

**Function Signatures:**
```python
# Always use type hints on public functions
def create(self, ds_id: str, description: str) -> LoginLink:
    """Type hints are mandatory."""
    ...

# Use Optional for optional parameters
def get(
    self,
    link_id: str,
    *,
    timeout: Optional[float] = None
) -> LoginLink:
    """Optional params use Optional[T]."""
    ...

# Use list[] for lists (Python 3.10+ syntax)
def list(self, *, limit: Optional[int] = None) -> list[LoginLink]:
    """Returns list of LoginLink objects."""
    ...

# Use dict[] for dictionaries
def update(self, data: dict[str, Any]) -> LoginLink:
    """Dict with key/value types."""
    ...

# Private methods also get type hints
def _build_headers(self, custom: Optional[dict[str, str]]) -> dict[str, str]:
    """Even private methods are typed."""
    ...
```

**Complex Types:**
```python
from typing import Optional, Union, Literal, TypeVar, Generic

# Use Literal for specific string values
def create(self, ds_id: Literal["GAWA", "google_ads", "facebook"]) -> LoginLink:
    """Literal restricts to specific values."""
    ...

# Use Union sparingly (prefer overloads)
def get(self, identifier: Union[str, int]) -> LoginLink:
    """Union allows multiple types (use sparingly)."""
    ...

# For methods that accept different parameter combinations, use @overload
from typing import overload

@overload
def list(self, *, limit: int) -> list[LoginLink]: ...

@overload
def list(self, *, ds_id: str) -> list[LoginLink]: ...

def list(
    self,
    *,
    limit: Optional[int] = None,
    ds_id: Optional[str] = None
) -> list[LoginLink]:
    """Implementation accepts both."""
    ...
```

### Docstring Format (Google Style - MANDATORY on public APIs)

**Complete Docstring Template:**
```python
def create(
    self,
    ds_id: str,
    description: str,
    *,
    expires_in: Optional[int] = None,
    **kwargs
) -> LoginLink:
    """Create a new login link for data source authentication.

    This creates a unique authentication URL that users visit to authorize
    access to their data source account. The link can optionally expire
    after a specified duration.

    Login links are the first step in the Supermetrics authentication flow:
    1. Create login link
    2. User authorizes via auth_url
    3. Retrieve login credentials
    4. Access accounts and query data

    Args:
        ds_id: Data source identifier (e.g., "GAWA", "google_ads", "facebook").
            See API documentation for full list of supported data sources.
        description: Human-readable description for this login link. Helps
            identify the purpose when viewing multiple links.
        expires_in: Optional expiration time in seconds. If not specified,
            link never expires. Recommended for security: 3600 (1 hour).
        **kwargs: Additional parameters passed directly to the API. See
            Supermetrics API documentation for advanced options.

    Returns:
        LoginLink object containing:
            - id: Unique identifier for this login link
            - auth_url: URL to share with user for authorization
            - ds_id: Data source identifier
            - description: Link description
            - created_at: Creation timestamp
            - expires_at: Expiration timestamp (if expires_in specified)

    Raises:
        AuthenticationError: API key is invalid, expired, or lacks permissions
            for the specified data source.
        ValidationError: Invalid ds_id, description, or other parameters.
            Check error message for specific validation failures.
        APIError: Supermetrics API returned an unexpected error. This may
            indicate temporary API issues - retry may succeed.
        NetworkError: Network connectivity issue prevented request completion.
            Check internet connection and retry.

    Example:
        Create a login link with expiration:

        >>> client = SupermetricsClient(api_key="your-key")
        >>> link = client.login_links.create(
        ...     ds_id="GAWA",
        ...     description="Analytics Dashboard - Production",
        ...     expires_in=3600  # Expires in 1 hour
        ... )
        >>> print(f"Share this URL: {link.auth_url}")
        Share this URL: https://auth.supermetrics.com/...

    Note:
        Login links do not automatically refresh. If a link expires, create
        a new one. For production use, implement proper expiration handling.

    See Also:
        - get(): Retrieve login link details
        - list(): List all login links
        - Logins.get(): Retrieve login after user authorization
    """
    ...
```

**Minimal Docstring (for simple methods):**
```python
def get(self, link_id: str) -> LoginLink:
    """Retrieve login link details by ID.

    Args:
        link_id: Unique login link identifier

    Returns:
        LoginLink object

    Raises:
        AuthenticationError: Invalid API key
        ValidationError: Invalid link_id format
        APIError: Link not found or API error
    """
    ...
```

### Error Handling Pattern (CONSISTENT across all resources)

**Exception Hierarchy:**
```python
# src/supermetrics/exceptions.py

class SupermetricsError(Exception):
    """Base exception for all SDK errors.

    All SDK exceptions inherit from this base class, allowing users to
    catch all SDK-specific errors with a single except clause.

    Attributes:
        message: Human-readable error message
        status_code: HTTP status code (if applicable)
        endpoint: API endpoint that caused the error (if applicable)
        response_body: Raw API response body (if applicable)
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        response_body: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        self.response_body = response_body

class AuthenticationError(SupermetricsError):
    """API key authentication failed.

    Raised when:
    - API key is invalid or expired
    - API key lacks permissions for requested operation
    - HTTP 401 Unauthorized response
    """

class ValidationError(SupermetricsError):
    """Request parameters failed validation.

    Raised when:
    - Required parameters are missing
    - Parameters have invalid format or values
    - Pydantic validation fails
    - HTTP 400 Bad Request response
    """

class APIError(SupermetricsError):
    """Supermetrics API returned an error.

    Raised when:
    - API returns 5xx server error
    - API returns unexpected error response
    - Resource not found (404)
    """

class NetworkError(SupermetricsError):
    """Network connectivity error.

    Raised when:
    - Request timeout
    - Connection refused
    - DNS resolution failure
    - Other network-level errors
    """
```

**Exception Mapping Pattern (use in all resources):**
```python
def create(self, ...) -> Model:
    """Create resource."""
    try:
        response = self._client.api.create_resource(...)
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
                f"Invalid request: {e.response.text}",
                status_code=400,
                endpoint=str(e.request.url),
                response_body=e.response.text
            )
        elif e.response.status_code == 404:
            raise APIError(
                f"Resource not found: {e.response.text}",
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
        # Network-level errors (timeout, connection refused, etc.)
        raise NetworkError(
            f"Network error: {str(e)}",
            endpoint=str(e.request.url) if hasattr(e, 'request') else None
        )
```

---

## Consistency Rules

### Client Initialization Pattern (MANDATORY)

**Sync Client:**
```python
# src/supermetrics/client.py

import logging
from typing import Optional
import httpx
from supermetrics_sdk.__version__ import __version__
from supermetrics_sdk._generated.client import Client as GeneratedClient
from supermetrics_sdk.resources.login_links import LoginLinksResource
from supermetrics_sdk.resources.logins import LoginsResource
from supermetrics_sdk.resources.accounts import AccountsResource
from supermetrics_sdk.resources.queries import QueriesResource

logger = logging.getLogger(__name__)

class SupermetricsClient:
    """Synchronous client for Supermetrics API.

    This client provides a type-safe, Pythonic interface to the Supermetrics
    API with full IDE autocomplete support. All methods are synchronous and
    suitable for scripts, notebooks, and REPL exploration.

    For asynchronous usage (recommended for production applications), use
    SupermetricsAsyncClient instead.

    Example:
        >>> from supermetrics_sdk import SupermetricsClient
        >>> client = SupermetricsClient(api_key="your-key")
        >>> link = client.login_links.create(ds_id="GAWA", description="Test")
    """

    def __init__(
        self,
        api_key: str,
        *,
        user_agent: Optional[str] = None,
        custom_headers: Optional[dict[str, str]] = None,
        timeout: float = 30.0,
        base_url: str = "https://api.supermetrics.com"
    ) -> None:
        """Initialize Supermetrics client.

        Args:
            api_key: Supermetrics API key (required)
            user_agent: Custom User-Agent header. Defaults to
                "supermetrics-sdk/{version} python/{py_version}"
            custom_headers: Additional HTTP headers for all requests
            timeout: Request timeout in seconds (default: 30.0)
            base_url: API base URL (default: production API)
        """
        self._api_key = api_key

        # Build headers
        import sys
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Sm-Python-SDK-Version": default_user_agent,
            "User-Agent": user_agent or default_user_agent,
        }

        if custom_headers:
            # User headers take precedence
            headers.update(custom_headers)

        logger.debug(f"Initializing SupermetricsClient with base_url={base_url}")

        # Create internal generated client
        self._client = GeneratedClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout
        )

        # Attach resource adapters
        self.login_links = LoginLinksResource(self._client)
        self.logins = LoginsResource(self._client)
        self.accounts = AccountsResource(self._client)
        self.queries = QueriesResource(self._client)

        logger.info("SupermetricsClient initialized successfully")

    def close(self) -> None:
        """Close the client and release resources.

        Call this when you're done using the client to ensure proper cleanup.
        Alternatively, use the client as a context manager.
        """
        logger.debug("Closing SupermetricsClient")
        self._client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.close()
```

**Async Client:**
```python
# src/supermetrics/async_client.py

import logging
from typing import Optional
import httpx
from supermetrics_sdk.__version__ import __version__
from supermetrics_sdk._generated.async_client import AsyncClient as GeneratedAsyncClient
from supermetrics_sdk.resources.login_links import LoginLinksAsyncResource
from supermetrics_sdk.resources.logins import LoginsAsyncResource
from supermetrics_sdk.resources.accounts import AccountsAsyncResource
from supermetrics_sdk.resources.queries import QueriesAsyncResource

logger = logging.getLogger(__name__)

class SupermetricsAsyncClient:
    """Asynchronous client for Supermetrics API.

    This client provides the same interface as SupermetricsClient but all
    methods are async and must be awaited. Recommended for production
    applications that need high concurrency or integration with async
    frameworks (FastAPI, asyncio, etc.).

    Example:
        >>> import asyncio
        >>> from supermetrics_sdk import SupermetricsAsyncClient
        >>>
        >>> async def main():
        ...     async with SupermetricsAsyncClient(api_key="your-key") as client:
        ...         link = await client.login_links.create(
        ...             ds_id="GAWA",
        ...             description="Test"
        ...         )
        ...         print(link.id)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        *,
        user_agent: Optional[str] = None,
        custom_headers: Optional[dict[str, str]] = None,
        timeout: float = 30.0,
        base_url: str = "https://api.supermetrics.com"
    ) -> None:
        """Initialize async Supermetrics client.

        Args:
            api_key: Supermetrics API key (required)
            user_agent: Custom User-Agent header
            custom_headers: Additional HTTP headers for all requests
            timeout: Request timeout in seconds (default: 30.0)
            base_url: API base URL (default: production API)
        """
        self._api_key = api_key

        # Build headers (identical to sync client)
        import sys
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent or default_user_agent,
        }

        if custom_headers:
            headers.update(custom_headers)

        logger.debug(f"Initializing SupermetricsAsyncClient with base_url={base_url}")

        # Create internal generated async client
        self._client = GeneratedAsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout
        )

        # Attach async resource adapters
        self.login_links = LoginLinksAsyncResource(self._client)
        self.logins = LoginsAsyncResource(self._client)
        self.accounts = AccountsAsyncResource(self._client)
        self.queries = QueriesAsyncResource(self._client)

        logger.info("SupermetricsAsyncClient initialized successfully")

    async def close(self) -> None:
        """Close the client and release resources.

        Important: Always call this when done, or use async context manager.
        """
        logger.debug("Closing SupermetricsAsyncClient")
        await self._client.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args):
        """Async context manager exit."""
        await self.close()
```

### Logging Strategy

**Configuration:**
```python
# src/supermetrics/_logger.py (internal module)

import logging

# Get SDK logger
logger = logging.getLogger("supermetrics_sdk")

# Default to WARNING level (quiet unless user enables)
logger.setLevel(logging.WARNING)

# Don't propagate to root logger by default
logger.propagate = False

# Add null handler to prevent "No handlers" warning
logger.addHandler(logging.NullHandler())
```

**Usage in SDK Code:**
```python
# In each module
import logging

logger = logging.getLogger(__name__)  # e.g., "supermetrics_sdk.resources.login_links"

class LoginLinksResource:
    def create(self, ds_id: str, description: str) -> LoginLink:
        # DEBUG: Verbose internal details
        logger.debug(f"Creating login link: ds_id={ds_id}, description={description}")

        try:
            response = self._client.api.create_login_link(...)

            # INFO: Important state changes
            logger.info(f"Created login link: id={response.id}")

            return response

        except Exception as e:
            # ERROR: Failures
            logger.error(f"Failed to create login link: {e}", exc_info=True)
            raise
```

**User Enablement:**
```python
# Users can enable SDK logging
import logging

# Enable DEBUG logging for entire SDK
logging.basicConfig(level=logging.DEBUG)

# Or enable for specific SDK module
logging.getLogger("supermetrics_sdk.resources.login_links").setLevel(logging.DEBUG)
```

**Log Levels:**
- `DEBUG`: Verbose SDK internals (parameters, intermediate states)
- `INFO`: Important operations (resource created, query executed)
- `WARNING`: Unexpected but recoverable situations (retries, deprecations)
- `ERROR`: Failures and exceptions

**Security:** NEVER log sensitive data (API keys, tokens, PII)

### Testing Patterns (MANDATORY for all tests)

**Test File Naming:**
```
tests/
├── unit/
│   ├── test_client_init.py      # Tests for client.py
│   ├── test_login_links.py      # Tests for resources/login_links.py
│   └── test_exceptions.py       # Tests for exceptions.py
└── integration/
    ├── test_complete_flow.py    # End-to-end flow tests
    └── test_async_flow.py       # Async flow tests
```

**Test Structure (AAA Pattern):**
```python
# tests/unit/test_login_links.py

import pytest
from supermetrics_sdk import SupermetricsClient, SupermetricsAsyncClient
from supermetrics_sdk.exceptions import AuthenticationError, ValidationError

def test_create_login_link_success(mock_httpx_response):
    """Test successful login link creation."""
    # Arrange
    client = SupermetricsClient(api_key="test-api-key")
    mock_httpx_response.return_value = {
        "id": "link_123",
        "ds_id": "GAWA",
        "description": "Test Link",
        "auth_url": "https://auth.supermetrics.com/link_123"
    }

    # Act
    link = client.login_links.create(
        ds_id="GAWA",
        description="Test Link"
    )

    # Assert
    assert link.id == "link_123"
    assert link.ds_id == "GAWA"
    assert link.description == "Test Link"
    assert "auth.supermetrics.com" in link.auth_url

def test_create_login_link_invalid_api_key(mock_httpx_401_error):
    """Test login link creation with invalid API key."""
    # Arrange
    client = SupermetricsClient(api_key="invalid-key")

    # Act & Assert
    with pytest.raises(AuthenticationError) as exc_info:
        client.login_links.create(ds_id="GAWA", description="Test")

    assert exc_info.value.status_code == 401
    assert "Invalid or expired API key" in str(exc_info.value)

def test_create_login_link_invalid_ds_id(mock_httpx_400_error):
    """Test login link creation with invalid ds_id."""
    # Arrange
    client = SupermetricsClient(api_key="test-key")

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        client.login_links.create(ds_id="INVALID", description="Test")

    assert exc_info.value.status_code == 400
```

**Async Test Pattern:**
```python
@pytest.mark.asyncio
async def test_create_login_link_async_success(mock_httpx_response):
    """Test async login link creation."""
    # Arrange
    async_client = SupermetricsAsyncClient(api_key="test-key")
    mock_httpx_response.return_value = {"id": "link_123", ...}

    # Act
    link = await async_client.login_links.create(
        ds_id="GAWA",
        description="Test"
    )

    # Assert
    assert link.id == "link_123"

    # Cleanup
    await async_client.close()
```

**Fixtures (tests/conftest.py):**
```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_httpx_response():
    """Mock successful httpx response."""
    mock = Mock()
    return mock

@pytest.fixture
def mock_httpx_401_error():
    """Mock 401 Unauthorized response."""
    import httpx

    request = httpx.Request("POST", "https://api.supermetrics.com/login_links")
    response = httpx.Response(
        status_code=401,
        text='{"error": "Unauthorized"}',
        request=request
    )

    error = httpx.HTTPStatusError(
        message="Unauthorized",
        request=request,
        response=response
    )

    return error

@pytest.fixture
def mock_httpx_400_error():
    """Mock 400 Bad Request response."""
    # Similar to above, but status 400
    ...
```

---

## Data Architecture

### Pydantic Models (Auto-Generated from OpenAPI)

**Generated Models (in `_generated/models/`):**

All data models are auto-generated from the OpenAPI specification and provide:
- Type-safe field validation
- JSON serialization/deserialization
- IDE autocomplete support
- Clear error messages for validation failures

**Example Models:**

```python
# _generated/models/login_link.py (generated)
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LoginLink(BaseModel):
    """Login link for data source authentication."""

    id: str = Field(..., description="Unique login link identifier")
    ds_id: str = Field(..., description="Data source ID")
    description: str = Field(..., description="Human-readable description")
    auth_url: str = Field(..., description="URL for user authorization")
    created_at: datetime = Field(..., description="Creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    status: str = Field(..., description="Link status (active, expired, used)")

# _generated/models/login.py (generated)
class Login(BaseModel):
    """User login credentials after authorization."""

    login_username: str = Field(..., description="Unique login identifier")
    ds_id: str = Field(..., description="Data source ID")
    ds_user: str = Field(..., description="Data source username/email")
    status: str = Field(..., description="Login status")
    created_at: datetime

# _generated/models/account.py (generated)
class Account(BaseModel):
    """Data source account information."""

    account_id: str = Field(..., description="Account identifier")
    account_name: str = Field(..., description="Account display name")
    ds_id: str = Field(..., description="Data source ID")
    type: str = Field(..., description="Account type")

# _generated/models/query_result.py (generated)
class QueryResult(BaseModel):
    """Data query result."""

    query_id: str
    status: str  # "completed", "pending", "failed"
    data: list[dict]  # Actual data rows
    fields: list[str]  # Field names
    row_count: int
```

**Usage in Adapter Layer:**

Adapters import and expose these models in type hints, providing users with type-safe interactions:

```python
from supermetrics_sdk._generated.models import LoginLink

class LoginLinksResource:
    def create(self, ds_id: str, description: str) -> LoginLink:
        """Returns LoginLink model with full type safety."""
        ...
```

### Data Relationships

**Authentication Flow Data Model:**

```
API Key (User)
    ↓
LoginLink
    ├─ id: str
    ├─ ds_id: str
    ├─ auth_url: str
    └─ description: str
    ↓ (User authorizes via auth_url)
Login
    ├─ login_username: str  ← Used to retrieve accounts
    ├─ ds_id: str
    └─ ds_user: str
    ↓ (Retrieve accounts by login_username)
Account[]
    ├─ account_id: str      ← Used in queries
    ├─ account_name: str
    └─ ds_id: str
    ↓ (Execute query with account_id)
QueryResult
    ├─ query_id: str
    ├─ data: list[dict]     ← Actual marketing data
    └─ fields: list[str]
```

**Key Identifiers:**
- `api_key`: Authenticates SDK client
- `link_id`: Identifies a specific login link
- `login_username`: Links login to accounts (primary key for account retrieval)
- `account_id`: Identifies data source account (used in queries)
- `query_id`: Identifies a data query (for polling async queries)

---

## API Contracts

### Request/Response Format

**All API interactions follow this pattern:**

**Sync Client:**
```python
# Request
client = SupermetricsClient(api_key="key")
result = client.resource.method(param1="value", param2="value")

# Response: Pydantic model instance
assert isinstance(result, PydanticModel)
```

**Async Client:**
```python
# Request
async_client = SupermetricsAsyncClient(api_key="key")
result = await async_client.resource.method(param1="value", param2="value")

# Response: Same Pydantic model instance
assert isinstance(result, PydanticModel)
```

**Error Responses:**
SDK never returns error objects. All errors raise exceptions:
```python
try:
    result = client.login_links.create(...)
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Status: {e.status_code}")
except ValidationError as e:
    print(f"Invalid params: {e.message}")
except APIError as e:
    print(f"API error: {e.message}")
```

### Authentication

**API Key Authentication:**
- Method: Bearer token in Authorization header
- Format: `Authorization: Bearer <api_key>`
- Scope: All requests use the same API key (client-level)
- Storage: API key stored in client instance, never logged
- Custom headers: Merged with defaults, user headers take precedence

**User-Agent:**
- Default: `supermetrics-sdk/{version} python/{py_version}`
- Example: `supermetrics-sdk/1.0.0 python/3.11`
- Customizable: Pass `user_agent` parameter to client initialization

### Resource Operations

**LoginLinks Resource:**
```python
# Create login link
link: LoginLink = client.login_links.create(
    ds_id="GAWA",
    description="Analytics Dashboard"
)

# Get login link by ID
link: LoginLink = client.login_links.get(link_id="link_123")

# List login links
links: list[LoginLink] = client.login_links.list()

# Close login link (expire)
client.login_links.close(link_id="link_123")
```

**Logins Resource:**
```python
# Get login by login link ID
login: Login = client.logins.get(link_id="link_123")

# Get login by login_username
login: Login = client.logins.get_by_username(login_username="user_abc")

# List all logins
logins: list[Login] = client.logins.list()
```

**Accounts Resource:**
```python
# Get accounts by login_username
accounts: list[Account] = client.accounts.list(login_username="user_abc")

# Get accounts by data source
accounts: list[Account] = client.accounts.list(ds_id="GAWA")

# Filter accounts
accounts: list[Account] = client.accounts.list(
    login_username="user_abc",
    account_type="property"
)
```

**Queries Resource:**
```python
# Execute data query
result: QueryResult = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["account_123"],
    fields=["sessions", "users", "pageviews"],
    start_date="2025-01-01",
    end_date="2025-01-31"
)

# For async queries (query is still processing)
if result.status == "pending":
    # Poll for results
    result = client.queries.get_results(query_id=result.query_id)
```

---

## Security Architecture

### API Key Handling

**Storage:**
- API key passed to client constructor
- Stored in `self._api_key` (private instance variable)
- Included in Authorization header for all requests
- NEVER logged or exposed in error messages

**Transmission:**
- Always sent via HTTPS (enforced by default base_url)
- Included in Authorization header: `Bearer <api_key>`
- Never sent in URL query parameters or request body

**Best Practices for Users:**
```python
# ✅ GOOD: Load from environment variable
import os
api_key = os.environ["SUPERMETRICS_API_KEY"]
client = SupermetricsClient(api_key=api_key)

# ✅ GOOD: Load from secure config file
import json
with open("config.json") as f:
    config = json.load(f)
client = SupermetricsClient(api_key=config["api_key"])

# ❌ BAD: Hardcode in source code
client = SupermetricsClient(api_key="sk_live_abc123...")  # DON'T DO THIS
```

### HTTPS Enforcement

**Default base URL:** `https://api.supermetrics.com`
- All communication over TLS/SSL
- Certificate validation enabled by default (httpx default)
- Users can override base_url for testing, but production API requires HTTPS

### Dependency Security

**Minimal Dependencies:**
- Only 4 runtime dependencies (httpx, Pydantic, python-dateutil, attrs)
- All are well-maintained, popular packages
- Regular security updates via Dependabot

**CI/CD Security:**
- Dependabot enabled for automatic dependency updates
- GitHub Actions scans for known vulnerabilities
- PyPI publishing uses trusted tokens (no password auth)

### Error Message Security

**NO sensitive data in error messages:**
```python
# ✅ GOOD: Generic error message
raise AuthenticationError("Invalid or expired API key")

# ❌ BAD: Exposes API key
raise AuthenticationError(f"API key {api_key} is invalid")
```

**Error messages include:**
- Generic description of what went wrong
- HTTP status code
- API endpoint (safe to expose)
- Response body (from API, doesn't contain user secrets)

**Error messages NEVER include:**
- User's API key
- Authorization headers
- Internal SDK state

---

## Performance Considerations

### SDK Overhead

**Target:** <10ms per API request

**Actual overhead:**
- Pydantic validation: ~1-2ms per request/response
- httpx client: ~0.5ms overhead vs raw sockets
- Adapter layer: ~0.1ms (simple method delegation)
- **Total SDK overhead: ~2-3ms** (well under target)

**Bottleneck:** Network latency and API processing time (100-500ms typical)

### Async Support for High Concurrency

**SupermetricsAsyncClient supports 100+ concurrent requests:**

```python
import asyncio
from supermetrics_sdk import SupermetricsAsyncClient

async def fetch_query(client, account_id):
    """Fetch data for single account."""
    return await client.queries.execute(
        ds_id="GAWA",
        ds_accounts=[account_id],
        fields=["sessions"],
        start_date="2025-01-01",
        end_date="2025-01-31"
    )

async def main():
    async with SupermetricsAsyncClient(api_key=api_key) as client:
        # Fetch data for 100 accounts concurrently
        account_ids = [f"account_{i}" for i in range(100)]
        tasks = [fetch_query(client, acc_id) for acc_id in account_ids]
        results = await asyncio.gather(*tasks)

    print(f"Fetched {len(results)} query results concurrently")

asyncio.run(main())
```

**Performance:**
- Sequential: 100 queries × 200ms = 20 seconds
- Concurrent (async): 100 queries in ~2-3 seconds (limited by API rate limits)

### Connection Pooling

**httpx provides automatic connection pooling:**
- Reuses TCP connections across requests
- Reduces SSL handshake overhead
- Configurable via httpx limits (not exposed in MVP, use defaults)

### Memory Footprint

**Target:** <50MB for typical usage

**Actual usage:**
- SDK code: ~2-3MB
- Dependencies (httpx, Pydantic): ~15-20MB
- Runtime data: Depends on query results (user-controlled)
- **Total: ~20-25MB baseline, +data**

---

## Deployment Architecture

### Distribution Method

**PyPI Package:**
- Package name: `supermetrics-sdk`
- Installation: `pip install supermetrics-sdk`
- Semantic versioning: v1.0.0 (major.minor.patch)
- License: Apache 2.0

**GitHub Repository:**
- Repository: `https://github.com/supermetrics/supermetrics-sdk` (example)
- Public open-source repository
- Issue tracking, discussions, pull requests

### Supported Environments

**Execution Environments:**
- Containers (Docker, Kubernetes)
- Serverless (AWS Lambda, Google Cloud Functions, Azure Functions)
- Jupyter Notebooks / Google Colab
- Traditional servers (Linux, macOS, Windows)
- CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)

**Operating Systems:**
- Linux (Ubuntu, Debian, RHEL, Alpine)
- macOS (11+)
- Windows (10+)

**Python Versions:**
- Minimum: Python 3.10
- Tested: Python 3.10, 3.11, 3.12
- Future: Python 3.13 (add to CI matrix after stable release)

### Installation

**Basic installation:**
```bash
pip install supermetrics-sdk
```

**With uv (recommended):**
```bash
uv pip install supermetrics-sdk
```

**Verify installation:**
```python
import supermetrics_sdk
print(supermetrics_sdk.__version__)
```

---

## Development Environment

### Prerequisites

**Required:**
- Python 3.10 or higher
- Git
- uv (or pip)

**Optional:**
- Docker (for containerized development)
- VSCode with Python extension (recommended IDE)

### Setup Commands

```bash
# Clone repository
git clone https://github.com/supermetrics/supermetrics-sdk.git
cd supermetrics-sdk

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows

# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify installation
pytest tests/
ruff check src/
mypy src/
```

### Development Workflow

**1. Create feature branch:**
```bash
git checkout -b feature/add-new-resource
```

**2. Make changes:**
```bash
# Edit code
vim src/supermetrics/resources/new_resource.py

# Run tests
pytest tests/unit/test_new_resource.py

# Check code quality
ruff check src/
mypy src/
```

**3. Commit changes:**
```bash
git add .
git commit -m "Add NewResource with create/get/list methods"
# Pre-commit hooks run automatically (ruff, mypy)
```

**4. Push and create PR:**
```bash
git push origin feature/add-new-resource
# Create pull request on GitHub
# CI runs tests, checks, builds
```

**5. After PR approval:**
```bash
git checkout main
git pull origin main
```

---

## Architecture Decision Records (ADRs)

### ADR-001: Use Adapter Pattern Over Direct Generated Code

**Status:** Accepted

**Context:**
OpenAPI-generated code will be regenerated monthly to stay in sync with API changes. Direct use of generated code would expose users to breaking changes with each regeneration.

**Decision:**
Implement adapter pattern where hand-written stable public API (`resources/`) wraps regeneratable generated code (`_generated/`).

**Rationale:**
- Monthly regeneration without breaking users
- Absorb API evolution at adapter boundary
- Custom logic (error handling, logging) without modifying generated code
- Proven pattern (AWS SDK, Google Cloud SDK)

**Consequences:**
- Positive: API stability, regeneration safety, custom error messages
- Negative: Additional maintenance overhead, dual code layers
- Mitigation: Clear patterns reduce maintenance burden

---

### ADR-002: Use Separate Sync/Async Client Classes

**Status:** Accepted

**Context:**
SDK must support both synchronous (notebooks, scripts) and asynchronous (production pipelines) use cases.

**Decision:**
Provide two separate client classes: `SupermetricsClient` (sync) and `SupermetricsAsyncClient` (async), with identical APIs.

**Rationale:**
- Type safety: No confusion about when to use `await`
- Clear separation: Users choose based on use case
- Native httpx pattern: Matches underlying library design
- IDE support: Better autocomplete and type checking

**Alternatives Rejected:**
- Single client with sync/async detection: Complex, error-prone
- Parameter-based selection: `client.create(..., async=True)`: Poor type safety

**Consequences:**
- Positive: Clear, type-safe, Pythonic API
- Negative: Duplicate resource classes (sync + async versions)
- Mitigation: openapi-python-client generates both, minimal duplication

---

### ADR-003: Use uv for Package Management

**Status:** Accepted

**Context:**
Project needs fast, reliable dependency management with lockfile support and modern Python tooling.

**Decision:**
Use uv as the primary package manager, replacing pip/poetry.

**Rationale:**
- Fast: 10-100x faster than pip
- Modern: Designed for Python 3.10+ and pyproject.toml
- Lockfile: `uv.lock` ensures reproducible builds
- Compatible: Works with existing pyproject.toml
- Simple: Single tool for venv + dependencies

**Alternatives Rejected:**
- pip: Slower, no lockfile
- poetry: Slower, more complex configuration

**Consequences:**
- Positive: Fast installs, reproducible builds, simple workflow
- Negative: Newer tool (less familiar to some developers)
- Mitigation: Excellent documentation, simple migration from pip

---

### ADR-004: Use ruff for All Code Quality Checks

**Status:** Accepted

**Context:**
Need consistent code formatting, linting, and style enforcement across all contributors.

**Decision:**
Use ruff as the all-in-one code quality tool, replacing black + flake8 + isort + pyupgrade.

**Rationale:**
- Fast: 10-100x faster than existing tools (Rust-based)
- Comprehensive: Replaces 5+ tools with one
- Compatible: Supports existing configurations
- Auto-fix: Automatically fixes many issues
- Modern: Actively maintained, growing ecosystem

**Alternatives Rejected:**
- black + flake8 + isort: Multiple tools, slower
- pylint: Slower, more opinionated

**Consequences:**
- Positive: Fast checks, single tool, auto-fix
- Negative: Newer tool (less familiar)
- Mitigation: Drop-in replacement for existing tools

---

### ADR-005: Use MkDocs for Documentation

**Status:** Accepted

**Context:**
SDK needs comprehensive user-facing documentation that's easy to write, maintain, and deploy.

**Decision:**
Use MkDocs with Material theme for all SDK documentation.

**Rationale:**
- Markdown-native: Easy to write, familiar format
- Simple: Minimal learning curve vs Sphinx/RST
- Modern UI: Material theme provides excellent UX
- API reference: mkdocstrings generates from docstrings
- Deployment: Easy GitHub Pages integration

**Alternatives Rejected:**
- Sphinx: Steeper learning curve (RST), more complex
- Custom: Too much work for minimal benefit

**Consequences:**
- Positive: Easy authoring, beautiful output, simple deployment
- Negative: Less extensible than Sphinx
- Mitigation: MkDocs + plugins cover 95% of SDK doc needs

---

### ADR-006: Support Python 3.10+ Only

**Status:** Accepted

**Context:**
Need to balance broad compatibility with modern Python features and reduced maintenance burden.

**Decision:**
Support Python 3.10, 3.11, 3.12 only. No support for Python 3.9 or earlier.

**Rationale:**
- Python 3.9: End-of-life (EOL) soon
- Python 3.10+: Modern type hints (PEP 604, 612, 613)
- Reduced testing: 3 versions vs 5-6
- Dependencies: All major dependencies support 3.10+
- Aggressive timeline: Can't support old versions

**Alternatives Rejected:**
- Python 3.8+: EOL, missing modern features
- Python 3.11+: Too restrictive, limits adoption

**Consequences:**
- Positive: Modern features, reduced maintenance
- Negative: Users on Python 3.9 must upgrade
- Mitigation: Clear documentation, upgrade guide

---

## Appendices

### Appendix A: pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "supermetrics-sdk"
version = "1.0.0"
description = "Official Python SDK for Supermetrics API"
readme = "README.md"
license = {text = "Apache-2.0"}
authors = [
    {name = "Supermetrics", email = "support@supermetrics.com"}
]
maintainers = [
    {name = "Supermetrics", email = "support@supermetrics.com"}
]
keywords = [
    "supermetrics",
    "api",
    "sdk",
    "analytics",
    "marketing",
    "data",
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "python-dateutil>=2.8.0",
    "attrs>=23.0.0",
]

[project.optional-dependencies]
dev = [
    "openapi-python-client>=0.15.0",
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.4.0",
    "mkdocstrings[python]>=0.24.0",
    "pre-commit>=3.5.0",
]

[project.urls]
Homepage = "https://github.com/supermetrics/supermetrics-sdk"
Documentation = "https://supermetrics.github.io/supermetrics-sdk/"
Repository = "https://github.com/supermetrics/supermetrics-sdk.git"
Issues = "https://github.com/supermetrics/supermetrics-sdk/issues"
Changelog = "https://github.com/supermetrics/supermetrics-sdk/blob/main/CHANGELOG.md"

[tool.hatch.build.targets.wheel]
packages = ["src/supermetrics_sdk"]

[tool.ruff]
line-length = 100
target-version = "py310"
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "SIM", # flake8-simplify
    "C4",  # flake8-comprehensions
]
ignore = [
    "E501",  # Line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true

[[tool.mypy.overrides]]
module = "supermetrics_sdk._generated.*"
ignore_errors = true  # Don't check generated code

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=supermetrics_sdk",
    "--cov-report=term-missing",
    "--cov-report=html",
]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src/supermetrics_sdk"]
omit = [
    "src/supermetrics/_generated/*",  # Don't measure generated code
    "tests/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### Appendix B: GitHub Actions Workflow Examples

**Test Workflow (.github/workflows/test.yml):**
```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test Python ${{ matrix.python-version }} on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1
        with:
          version: "latest"

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          uv pip install -e ".[dev]"

      - name: Run ruff
        run: |
          uv run ruff check src/ tests/

      - name: Run mypy
        run: |
          uv run mypy src/

      - name: Run tests
        run: |
          uv run pytest tests/ --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
        with:
          files: ./coverage.xml
```

**Publish Workflow (.github/workflows/publish.yml):**
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Build package
        run: |
          uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

---

**Generated by:** BMad Decision Architecture Workflow v1.3.2
**Date:** 2025-10-27
**For:** Aleksei
**Project:** Supermetrics python SDK (Level 2 - Greenfield)
