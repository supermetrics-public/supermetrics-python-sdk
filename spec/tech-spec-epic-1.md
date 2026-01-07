# Technical Specification: Project Foundation & Core SDK Generation

Date: 2025-10-28
Author: Aleksei
Epic ID: 1
Status: Approved

---

## Overview

Epic 1 establishes the foundational infrastructure and delivers a working Python SDK that enables the complete customer onboarding journey: from creating login links for data source authentication, through retrieving login credentials and accounts, to executing data queries. This epic implements the adapter pattern architecture that wraps OpenAPI-generated code with a stable public API, enabling monthly regeneration from the OpenAPI specification without breaking existing users. The deliverable is a functional POC SDK sufficient for enterprise customer validation, supporting both synchronous and asynchronous client patterns with full type safety through Pydantic v2 models.

## Objectives and Scope

**In Scope:**
- Python project initialization with modern tooling (uv, hatchling, pyproject.toml, src-layout)
- OpenAPI client code generation using openapi-python-client with sync/async support
- Adapter pattern implementation wrapping generated code with stable public API
- Resource-based API organization (login_links, logins, accounts, queries resources)
- Complete authentication flow: login links creation → login retrieval → accounts discovery → query execution
- Type-safe Pydantic v2 models for all requests and responses
- Custom exception hierarchy with HTTP status code mapping
- Basic error handling with clear, actionable error messages
- POC validation examples demonstrating complete onboarding workflow (sync + async)
- Repository structure, git initialization, and governance files (LICENSE, README skeleton)

**Out of Scope (Deferred to Epic 2 or later):**
- Comprehensive test coverage >80% (Epic 2)
- Full documentation, user guides, and API reference (Epic 2)
- Jupyter notebook examples (Epic 2)
- CI/CD pipelines and GitHub Actions workflows (Epic 2)
- PyPI package preparation and publishing (Epic 2)
- Automated regeneration workflows (Epic 2)
- Advanced retry strategies, rate limiting, caching
- OAuth2 authentication support
- CLI tools or visualization components

## System Architecture Alignment

This epic implements the core architecture decisions documented in `architecture.md`:

**Adapter Pattern + Resource-Based Architecture:**
- Generated code in `_generated/` (internal, regeneratable from OpenAPI)
- Stable public API in `resources/` (hand-written adapters wrapping generated code)
- Resource classes attached to client: `client.login_links`, `client.logins`, `client.accounts`, `client.queries`
- Dual sync/async support via separate client classes: `SupermetricsClient` and `SupermetricsAsyncClient`

**Technology Stack Alignment:**
- **openapi-python-client** (Story 1.2): Generates dual sync/async clients with Pydantic v2 models from OpenAPI spec
- **httpx** (provided by generator): HTTP client with sync/async support, connection pooling, custom headers
- **Pydantic v2** (provided by generator): Type-safe request/response models with validation
- **uv** (Story 1.1): Fast package manager with lockfile support
- **hatchling** (Story 1.1): Modern build system for pyproject.toml-native builds
- **ruff** (Stories 1.3-1.7): All-in-one code quality (linting + formatting)
- **pytest + pytest-asyncio** (Story 1.8): Testing framework with async support

**Project Structure:**
- `src/supermetrics/`: Source code with src-layout pattern
- `src/supermetrics/_generated/`: OpenAPI-generated code (regeneratable)
- `src/supermetrics/resources/`: Hand-written resource adapters (stable API)
- `src/supermetrics/client.py` & `async_client.py`: Client initialization with header injection
- `src/supermetrics/exceptions.py`: Custom exception hierarchy
- `tests/`: Unit and integration tests
- `examples/`: Complete flow demonstrations
- `scripts/regenerate_client.sh`: OpenAPI regeneration script

**Key Constraints:**
- Python 3.10+ only (modern type hints)
- Minimal runtime dependencies (<5 libraries)
- Apache 2.0 license
- No breaking changes on monthly OpenAPI regeneration

## Detailed Design

### Services and Modules

| Module | Responsibility | Inputs | Outputs | Owner/Story |
|--------|---------------|--------|---------|-------------|
| `client.py` | Sync client initialization, header injection, resource attachment | `api_key`, `user_agent`, `custom_headers`, `timeout`, `base_url` | `SupermetricsClient` instance with attached resources | Story 1.3 |
| `async_client.py` | Async client initialization, header injection, resource attachment | Same as sync client | `SupermetricsAsyncClient` instance with attached resources | Story 1.3 |
| `resources/login_links.py` | Login link CRUD operations (create, get, list, close) | `ds_id`, `description`, `link_id` | `LoginLink` Pydantic models | Story 1.4 |
| `resources/logins.py` | Login retrieval operations (get by link_id or login_username) | `link_id`, `login_username` | `Login` Pydantic models | Story 1.5 |
| `resources/accounts.py` | Account discovery and filtering (by login_username or ds_id) | `login_username`, `ds_id`, filter params | `list[Account]` Pydantic models | Story 1.6 |
| `resources/queries.py` | Query execution and result retrieval with async polling | `ds_id`, `ds_accounts`, `fields`, `start_date`, `end_date`, `query_id` | `QueryResult` Pydantic models | Story 1.7 |
| `exceptions.py` | Custom exception hierarchy with HTTP status mapping | HTTP errors from httpx | `SupermetricsError` subclasses (`AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`) | Story 1.8 |
| `_generated/` | Auto-generated client code from OpenAPI spec | OpenAPI YAML spec | Sync/async clients, API endpoints, Pydantic models | Story 1.2 |
| `__init__.py` | Public API exports | N/A | Client classes, exception classes | Story 1.3 |
| `__version__.py` | Version string management | N/A | `__version__` string | Story 1.1 |

### Data Models and Contracts

All data models are auto-generated from the OpenAPI specification using Pydantic v2. These models provide type safety, validation, and IDE autocomplete support.

**Core Pydantic Models (generated in `_generated/models/`):**

**LoginLink Model (draft):**
```python
class LoginLink(BaseModel):
    link_id: str                      # Unique login link identifier
    ds_id: str                        # Data source ID (e.g., "GAWA", "google_ads")
    ds_name: str                      # Human-readable description
    login_url: str                    # Full URL to initiate an authentication attempt. Can be accessed multiple times while link is open.
    require_username: Optional[str]   # Data source username that must be used in authentication attempt
    redirect_url: Optional[str]       # Custom URL to redirect to after successful authentication, if any
    redirect_verifier: Optional[str]  # Internal verifier string that is passed to redirect_url
    owner_user_id: Optional[str]            # Supermetrics user ID of the user who will be marked as the primary owner of the login credentials
    owner_user_email: Optional[str]         # Supermetrics user email
    login_id: Optional[str]           # Supermetrics login ID for a successful authentication
    login_username: Optional[str]     # Username used to authenticate to data source
    created_at: datetime              # Creation timestamp
    expires_at: Optional[datetime]    # Expiration timestamp (if applicable)
    login_at: Optional[datetime]      # ISO 8601 datetime for when authentication occurred
    status_code: str                  # Link status ("OPEN", "CLOSED", "EXPIRED" )
```

**Login Model:**
```python
class Login(BaseModel):
    login_id: str # Supermetrics login ID
    login_type: str # Authentication type. Note that some data sources support multiple types, and user can choose between them.
    username: str # Authenticated username, used in queries as ds_user
    display_name: str # Visible name for this authentication in product UIs
    ds_id: str # Data source ID
    ds_name: str # Data source name
    default_scopes: list[str] # List of default source API scopes used in authentication
    additional_scopes: list[str] # List of additional source API scopes user has granted to access more data
    login_at: datetime # ISO 8601 datetime for when last user authentication occurred
    owner_user_id: str # Supermetrics user ID
    owner_user_email: str # Supermetrics user email
    expires_at: Optional[datetime] # ISO 8601 datetime for when authentication expires, if any
    revoked_at: Optional[datetime] # ISO 8601 datetime for when authentication was revoked, if any
    is_refreshable: bool # Whether authentication can be automatically refreshed after expiry time, without user involvement
    is_shared: bool # Whether login is shared with all team users
```

**Account Model:**
```python
class Account(BaseModel):
    account_id: str                   # Account identifier (used in queries)
    account_name: str                 # Account display name
    group_name: str                   # Account group name (empty string when not available)
```

**QueryResult Model:**
```python
class Field(BaseModel):
    id: str                     # Field ID the API uses
    requested_id: str                     # Field ID from the reques
    name: str                       # Field name
    type: str                  # Field type
    split: str                 # Field split by type
    data_type: str                    # Field data type
    data_column: int                    # Field value position in each data row
    visible: bool                    # Whether data for this field is visible

class QueryResult(BaseModel):
    request_id: str                     # API request ID
    schedule_id: str                     # Custom or generated schedule ID for the query
    status_code: str                       # Status code for the query
    data: list[dict]                  # Actual data rows
    fields: list[Field]                 # Field names
    row_count: int                    # Number of rows returned
    data_sampled: bool # If data source has provided sampled data
    cache_used: bool # If cached data was used
    cache_time: datetime # ISO 8601 datetime for the most recent cached data
```

**Data Flow and Relationships:**
```
API Key (User)
    ↓
LoginLink (create with ds_id, description)
    ├─ id: str
    ├─ auth_url: str  → (User authorizes via this URL)
    └─ ds_id: str
    ↓
Login (retrieve after authorization)
    ├─ login_username: str  ← KEY: Used to retrieve accounts
    └─ ds_id: str
    ↓
Account[] (list by login_username)
    ├─ account_id: str  ← KEY: Used in queries
    └─ account_name: str
    ↓
QueryResult (execute with account_id)
    ├─ data: list[dict]  ← Actual marketing data
    └─ fields: list[str]
```

### APIs and Interfaces

**Public Client API (stable, hand-written):**

**Client Initialization:**
```python
# Sync client
client = SupermetricsClient(
    api_key: str,                    # Required: API key for authentication
    user_agent: Optional[str] = None,  # Custom User-Agent header
    custom_headers: Optional[dict[str, str]] = None,  # Additional headers
    timeout: float = 30.0,           # Request timeout in seconds
    base_url: Optional[str] = "https://api.supermetrics.com"  # API base URL
)

# Async client (identical signature)
async_client = SupermetricsAsyncClient(...)
```

**LoginLinksResource API:**
```python
# Create login link
link: LoginLink = client.login_links.create(
    ds_id: str,                      # Data source ID (e.g., "GAWA")
    description: str,                # Human-readable description
    **kwargs                         # Additional API parameters
) -> LoginLink
# Raises: AuthenticationError, ValidationError, APIError, NetworkError

# Get login link by ID
link: LoginLink = client.login_links.get(link_id: str) -> LoginLink

# List all login links
links: list[LoginLink] = client.login_links.list() -> list[LoginLink]

# Close/expire login link
client.login_links.close(link_id: str) -> None
```

**LoginsResource API:**
```python
# Get login by link ID
login: Login = client.logins.get(link_id: str) -> Login

# Get login by username
login: Login = client.logins.get_by_username(login_username: str) -> Login

# List all logins
logins: list[Login] = client.logins.list() -> list[Login]
```

**AccountsResource API:**
```python
# List accounts by login username
accounts: list[Account] = client.accounts.list(login_username: str) -> list[Account]

# List accounts by data source
accounts: list[Account] = client.accounts.list(ds_id: str) -> list[Account]

# List accounts with filtering
accounts: list[Account] = client.accounts.list(
    login_username: str,
    account_type: Optional[str] = None
) -> list[Account]
```

**QueriesResource API:**
```python
# Execute data query
result: QueryResult = client.queries.execute(
    ds_id: str,                      # Data source ID
    ds_accounts: list[str],          # Account IDs to query
    fields: list[str],               # Data fields to retrieve
    start_date: str,                 # Start date (ISO 8601)
    end_date: str,                   # End date (ISO 8601)
    **kwargs                         # Additional query parameters
) -> QueryResult

# Get query results (for async queries)
result: QueryResult = client.queries.get_results(query_id: str) -> QueryResult
```

**Exception API:**
```python
# Base exception
class SupermetricsError(Exception):
    message: str
    status_code: Optional[int]
    endpoint: Optional[str]
    response_body: Optional[str]

# Specific exceptions
class AuthenticationError(SupermetricsError):  # 401 errors
class ValidationError(SupermetricsError):      # 400 errors
class APIError(SupermetricsError):             # 5xx, 404, other errors
class NetworkError(SupermetricsError):         # Network-level errors
```

**HTTP Status Code Mapping:**
- 401 → `AuthenticationError`: Invalid or expired API key
- 400 → `ValidationError`: Invalid request parameters
- 404 → `APIError`: Resource not found
- 5xx → `APIError`: Supermetrics API error
- Network errors → `NetworkError`: Timeout, connection refused, DNS failure

### Workflows and Sequencing

**Complete Authentication & Query Flow:**

```
1. Initialize Client
   User creates SupermetricsClient(api_key="...")
   ↓
   SDK builds headers: Authorization: Bearer <api_key>
   SDK creates internal generated client with headers
   SDK attaches resource adapters to client instance
   ↓
   Returns ready client

2. Create Login Link (Story 1.4)
   client.login_links.create(ds_id="GAWA", description="...")
   ↓
   Adapter wraps generated client call
   Generated client sends POST /login_links
   API returns login link with auth_url
   ↓
   Returns LoginLink(id="...", auth_url="...")

3. User Authorization (External - User Action)
   User visits auth_url in browser
   User authenticates with data source (Google, Facebook, etc.)
   Supermetrics stores authorized credentials
   ↓
   Authorization complete

4. Retrieve Login (Story 1.5)
   client.logins.get(link_id="...")
   ↓
   Adapter wraps generated client call
   Generated client sends GET /logins/{link_id}
   API returns login details
   ↓
   Returns Login(login_username="...", ds_id="...")

5. Get Accounts (Story 1.6)
   client.accounts.list(login_username="...")
   ↓
   Adapter wraps generated client call
   Generated client sends GET /accounts?login_username=...
   API returns list of accessible accounts
   ↓
   Returns [Account(account_id="...", account_name="..."), ...]

6. Execute Query (Story 1.7)
   client.queries.execute(ds_id="GAWA", ds_accounts=["..."], fields=["sessions"], ...)
   ↓
   Adapter wraps generated client call
   Generated client sends POST /queries
   API processes query (may be async)
   ↓
   Returns QueryResult(data=[...], fields=["sessions"], status="completed")

7. Error Handling (Story 1.8)
   Any HTTP error during steps 2-6
   ↓
   httpx raises HTTPStatusError or RequestError
   Adapter catches exception
   Adapter maps to appropriate SupermetricsError subclass
   ↓
   Raises AuthenticationError | ValidationError | APIError | NetworkError
```

**Adapter Pattern Flow (Applied in Stories 1.4-1.7):**

```
User Code
    ↓
Resource Adapter (stable public API)
    ├─ Validate inputs
    ├─ Log operation (debug level)
    ├─ Call generated client method
    ├─ Catch httpx exceptions
    ├─ Map to SDK exceptions
    └─ Return Pydantic model
    ↓
Generated Client (internal, regeneratable)
    ├─ Build HTTP request
    ├─ Add headers from client init
    ├─ Send request via httpx
    ├─ Parse JSON response
    └─ Return Pydantic model
    ↓
Supermetrics API
```

## Non-Functional Requirements

### Performance

**Target Metrics (from PRD NFR001):**
- SDK overhead: <10ms per API request
- Async client: Support 100+ concurrent requests
- Memory footprint: <50MB baseline (excluding query result data)

**Implementation Strategy:**
- Pydantic v2 validation: ~1-2ms overhead per request/response
- httpx client overhead: ~0.5ms vs raw sockets
- Adapter layer delegation: ~0.1ms (simple method calls)
- **Expected total SDK overhead: ~2-3ms** (well under 10ms target)
- Connection pooling via httpx reduces SSL handshake overhead on repeated requests
- Async client uses asyncio for concurrent request handling without blocking

**Validation:**
- Story 1.9 POC example validates end-to-end performance
- Bottleneck is network latency + API processing (100-500ms typical), not SDK overhead

### Security

**API Key Handling (Story 1.3):**
- API key stored in private instance variable `self._api_key`
- Transmitted via HTTPS only (default base_url: `https://api.supermetrics.com`)
- Included in Authorization header: `Bearer <api_key>`
- NEVER logged or exposed in error messages
- NEVER sent in URL query parameters or request body

**HTTPS Enforcement:**
- Default base_url uses HTTPS
- Certificate validation enabled by default (httpx default)
- All API communication encrypted over TLS/SSL

**Error Message Security (Story 1.8):**
- Exception messages NEVER include user's API key or authorization headers
- Error messages include: generic description, HTTP status code, endpoint (safe), API response body (doesn't contain secrets)
- Example safe error: `AuthenticationError("Invalid or expired API key", status_code=401, endpoint="/login_links")`

**Dependency Security:**
- Minimal runtime dependencies (httpx, Pydantic, python-dateutil, attrs) - all well-maintained, popular packages
- No dependency on packages with known vulnerabilities (to be validated in Story 1.1)

**Best Practices Documentation (Story 1.9):**
- Examples demonstrate loading API key from environment variables
- README includes security best practices (never hardcode API keys)

### Reliability/Availability

**Error Handling (Story 1.8):**
- All HTTP errors caught and mapped to appropriate SDK exceptions
- Clear, actionable error messages with context (status code, endpoint, API response)
- Network errors (timeout, connection refused, DNS failure) raise `NetworkError` with diagnostic info
- Pydantic validation errors raise `ValidationError` before API calls (fail fast)

**Timeout Configuration (Story 1.3):**
- Default timeout: 30 seconds (configurable via client initialization)
- User can override: `SupermetricsClient(api_key="...", timeout=60.0)`
- Prevents indefinite hangs on slow/unresponsive API

**Connection Management:**
- httpx provides automatic connection pooling and reuse
- Connections properly closed on client context manager exit
- Both sync and async clients support context manager pattern for resource cleanup

**Graceful Degradation:**
- API errors don't crash user applications - exceptions provide clear recovery path
- Async query polling supported (Story 1.7) for long-running queries
- User responsible for retry logic (advanced retry strategies deferred to Phase 2)

**Out of Scope for Epic 1 (Deferred to Epic 2 or later):**
- Automatic retry with exponential backoff
- Circuit breaker patterns
- Request rate limiting
- Response caching

### Observability

**Logging Strategy (Stories 1.3-1.7):**
- SDK uses Python stdlib `logging` module
- Logger namespace: `supermetrics_sdk` (and submodules like `supermetrics_sdk.resources.login_links`)
- Default log level: WARNING (quiet unless user enables)
- No console output by default (prevents noise in user applications)
- Users can enable logging: `logging.basicConfig(level=logging.DEBUG)`

**Log Levels:**
- DEBUG: Verbose SDK internals (method parameters, API calls, intermediate states)
- INFO: Important operations (login link created, query executed)
- WARNING: Unexpected but recoverable situations (not used in Epic 1)
- ERROR: Failures and exceptions (includes stack traces)

**Logging Implementation Pattern:**
```python
import logging
logger = logging.getLogger(__name__)

def create(self, ds_id: str, description: str) -> LoginLink:
    logger.debug(f"Creating login link: ds_id={ds_id}")
    try:
        response = self._client.api.create_login_link(...)
        logger.info(f"Created login link: id={response.id}")
        return response
    except Exception as e:
        logger.error(f"Failed to create login link: {e}", exc_info=True)
        raise
```

**Security Constraint:**
- NEVER log sensitive data (API keys, tokens, PII)
- Only log non-sensitive operation parameters and identifiers

**Out of Scope for Epic 1:**
- Metrics collection (request counts, latencies)
- Distributed tracing
- Structured logging (JSON format)

## Dependencies and Integrations

**Note:** No dependency manifest exists yet in the repository. Story 1.1 will create `pyproject.toml` with the following dependencies.

**Runtime Dependencies (Story 1.1 - defined in pyproject.toml):**
```toml
[project]
dependencies = [
    "httpx>=0.25.0",           # HTTP client with sync/async support
    "pydantic>=2.0.0",         # Data validation and type-safe models
    "python-dateutil>=2.8.0",  # ISO 8601 date parsing (dependency of openapi-python-client)
    "attrs>=23.0.0",           # Class utilities (dependency of openapi-python-client)
]
```

**Development Dependencies (Story 1.1 - defined in pyproject.toml):**
```toml
[project.optional-dependencies]
dev = [
    "openapi-python-client>=0.15.0",  # Story 1.2: OpenAPI code generator
    "pytest>=7.4.0",                   # Story 1.8: Test framework
    "pytest-asyncio>=0.21.0",          # Story 1.8: Async test support
    "pytest-cov>=4.1.0",               # Epic 2: Coverage measurement
    "ruff>=0.1.0",                     # Stories 1.3-1.7: Linting and formatting
    "mypy>=1.7.0",                     # Stories 1.3-1.7: Type checking
]
```

**Build System (Story 1.1):**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**External Integrations:**

| Integration | Purpose | Stories | Authentication |
|-------------|---------|---------|----------------|
| Supermetrics API | Primary API endpoint for all SDK operations | All stories (1.4-1.7) | API key via Bearer token in Authorization header |
| OpenAPI Specification | Source of truth for code generation | Story 1.2 | None (file-based) |

**Integration Points:**
- **Supermetrics API**: SDK wraps and simplifies API calls
  - Base URL: `https://api.supermetrics.com` (configurable)
  - Protocol: HTTPS only
  - Authentication: Bearer token
  - Endpoints: `/login_links`, `/logins`, `/accounts`, `/queries`

- **OpenAPI Specification**: Used for client code generation
  - Location: `openapi-spec.yaml` in project root (Story 1.2)
  - Format: OpenAPI 3.x YAML
  - Generator: openapi-python-client CLI
  - Output: `src/supermetrics/_generated/`

**No External Service Dependencies:**
- SDK is fully self-contained (no telemetry, analytics, or update checks)
- No database or cache dependencies
- No third-party authentication providers (API key only)

## Acceptance Criteria (Authoritative)

**Epic 1 is complete when ALL of the following criteria are met:**

1. **Project Foundation (Story 1.1):**
   - Repository initialized with git, .gitignore, LICENSE (Apache 2.0), README skeleton
   - Project structure created with src-layout: `src/supermetrics/`, `tests/`, `examples/`, `scripts/`
   - `pyproject.toml` configured with project metadata, dependencies, and hatchling build system
   - Python 3.10+ compatibility verified
   - Initial commit created

2. **OpenAPI Generation (Story 1.2):**
   - OpenAPI specification file obtained and stored in project root as `openapi-spec.yaml`
   - openapi-python-client installed as dev dependency
   - Initial SDK generated into `src/supermetrics/_generated/` directory
   - Generated code includes sync and async clients, Pydantic models, API endpoints
   - All required endpoints present: login_links, logins, accounts, queries
   - Generation script created: `scripts/regenerate_client.sh`

3. **Adapter Pattern Foundation (Story 1.3):**
   - `SupermetricsClient` class created in `client.py` with `api_key`, `user_agent`, `custom_headers`, `timeout`, `base_url` parameters
   - `SupermetricsAsyncClient` class created in `async_client.py` with same signature
   - Both clients wrap `_generated` client with custom header injection
   - `__init__.py` exports public API (client classes)
   - Complete type hints and docstrings on public client classes
   - Code passes mypy strict type checking
   - Code formatted with ruff
   - Simple initialization test added: `tests/test_client_init.py`

4. **Login Links Resource (Story 1.4):**
   - `LoginLinksResource` and `LoginLinksAsyncResource` classes implemented in `resources/login_links.py`
   - Methods implemented: `create()`, `get()`, `list()`, `close()`
   - Methods wrap `_generated` client calls with proper parameter mapping
   - Resources attached to client: `client.login_links` property
   - Complete type hints and docstrings for all public methods
   - Code passes mypy strict type checking and formatted with ruff
   - Unit tests added covering all CRUD operations

5. **Logins Resource (Story 1.5):**
   - `LoginsResource` and `LoginsAsyncResource` classes implemented in `resources/logins.py`
   - Methods implemented: `get()`, `list()`, `get_by_username()`
   - Resources attached to client: `client.logins` property
   - Complete type hints and docstrings
   - Code passes mypy and ruff
   - Unit tests covering all operations

6. **Accounts Resource (Story 1.6):**
   - `AccountsResource` and `AccountsAsyncResource` classes implemented in `resources/accounts.py`
   - Methods implemented: `list()`, with support for filtering by `login_username`, `ds_id`, and other parameters
   - Resources attached to client: `client.accounts` property
   - Complete type hints and docstrings
   - Code passes mypy and ruff
   - Unit tests covering all operations

7. **Queries Resource (Story 1.7):**
   - `QueriesResource` and `QueriesAsyncResource` classes implemented in `resources/queries.py`
   - Methods implemented: `execute()`, `get_results()` with support for fields, date ranges, accounts, data source parameters
   - Basic async query polling support implemented
   - Resources attached to client: `client.queries` property
   - Complete type hints and docstrings
   - Code passes mypy and ruff
   - Unit tests covering query execution and result retrieval

8. **Error Handling (Story 1.8):**
   - Custom exception hierarchy created in `exceptions.py`: `SupermetricsError`, `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`
   - Adapter methods wrap generated client exceptions and re-raise as custom exceptions with clear messages
   - HTTP error codes mapped: 401→AuthenticationError, 400→ValidationError, 404/5xx→APIError, network→NetworkError
   - Exception messages include relevant context (endpoint, status code, API error details)
   - Unit tests for error scenarios

9. **POC Examples (Story 1.9):**
   - `examples/complete_flow.py` created demonstrating: initialize client → create login link → get login → list accounts → execute query
   - `examples/async_flow.py` created with async version of complete flow
   - Examples include comments explaining each step
   - Both examples tested manually (or mocked if no test credentials available)
   - README updated with quick-start guide referencing examples
   - POC validated: complete flow works end-to-end with type safety and IDE autocomplete

**Overall Epic Success Criteria:**
- All 9 stories completed with acceptance criteria met
- Complete authentication flow functional: login links → logins → accounts → queries
- Both sync and async clients working
- Type safety throughout (mypy passes)
- Code quality standards met (ruff passes)
- Basic unit tests passing
- POC demonstrates full customer onboarding journey

## Traceability Mapping

| Acceptance Criterion | Spec Section(s) | Component(s)/Module(s) | Test Approach |
|---------------------|----------------|----------------------|---------------|
| **AC1: Project Foundation** | System Architecture Alignment, Dependencies | `pyproject.toml`, project structure, git repo | Verify file structure exists, pyproject.toml parses, git log shows initial commit |
| **AC2: OpenAPI Generation** | System Architecture Alignment → Technology Stack | `_generated/`, `openapi-spec.yaml`, `scripts/regenerate_client.sh` | Verify generated code exists, includes required endpoints, regeneration script runs |
| **AC3: Adapter Pattern** | System Architecture Alignment → Adapter Pattern, APIs and Interfaces → Client Init | `client.py`, `async_client.py`, `__init__.py` | Unit tests: client initialization, header injection, mypy type check passes |
| **AC4: Login Links** | APIs and Interfaces → LoginLinksResource, Workflows → Step 2 | `resources/login_links.py`, `LoginLinksResource` | Unit tests: create/get/list/close methods, error handling, sync+async versions |
| **AC5: Logins** | APIs and Interfaces → LoginsResource, Workflows → Step 4 | `resources/logins.py`, `LoginsResource` | Unit tests: get by link_id, get by username, list, sync+async versions |
| **AC6: Accounts** | APIs and Interfaces → AccountsResource, Workflows → Step 5 | `resources/accounts.py`, `AccountsResource` | Unit tests: list by login_username, list by ds_id, filtering, sync+async versions |
| **AC7: Queries** | APIs and Interfaces → QueriesResource, Workflows → Step 6 | `resources/queries.py`, `QueriesResource` | Unit tests: execute query, get results, async polling, sync+async versions |
| **AC8: Error Handling** | APIs and Interfaces → Exception API, Workflows → Step 7, NFR Security | `exceptions.py`, exception hierarchy | Unit tests: HTTP status mapping (401→Auth, 400→Validation, 5xx→API, network→Network), error context |
| **AC9: POC Examples** | Workflows and Sequencing → Complete Flow | `examples/complete_flow.py`, `examples/async_flow.py` | Manual testing: run examples, verify end-to-end flow, check type hints work in IDE |
| **FR001: API Key Auth** | System Architecture, NFR Security → API Key Handling | `client.py`, header injection | Unit test: verify Bearer token in headers, API key not logged |
| **FR002: Sync/Async Clients** | System Architecture → Dual Sync/Async | `client.py`, `async_client.py` | Unit tests: both clients initialize, have same API, async requires await |
| **FR003: Custom Headers** | APIs and Interfaces → Client Init | `client.py`, `async_client.py` | Unit test: custom headers merged with defaults, user headers override |
| **FR004: Configurable Timeout** | NFR Reliability → Timeout Configuration | `client.py`, `async_client.py` | Unit test: timeout parameter passed to httpx client |
| **FR005-007: Login Links** | AC4 covers this | `resources/login_links.py` | Covered by AC4 tests |
| **FR008-009: Logins/Accounts** | AC5, AC6 cover this | `resources/logins.py`, `resources/accounts.py` | Covered by AC5, AC6 tests |
| **FR010-011: Queries** | AC7 covers this | `resources/queries.py` | Covered by AC7 tests |
| **FR012: Pydantic Models** | Data Models and Contracts | `_generated/models/` | Verify generated models exist, have type hints, validate data |
| **FR013: Resource-Based Org** | System Architecture → Resource-Based | All resource classes | Verify client.login_links, client.logins, client.accounts, client.queries exist |
| **FR014: Clear Exceptions** | AC8 covers this | `exceptions.py` | Covered by AC8 tests |
| **FR015: Pydantic Validation** | Data Models and Contracts | Pydantic models | Test: invalid data raises ValidationError before API call |
| **NFR001: Performance** | NFR Performance | Entire SDK | Manual measurement: time API calls, verify <10ms SDK overhead |
| **NFR002: Distribution** | Dependencies, Out of Scope (Epic 2) | N/A for Epic 1 | Deferred to Epic 2 (PyPI publishing) |
| **NFR003: Maintainability** | System Architecture → Adapter Pattern | Adapter layer, regeneration script | Verify regeneration script works, tests pass after regeneration |

## Risks, Assumptions, Open Questions

**Risks:**

1. **RISK:** OpenAPI specification may not accurately reflect actual Supermetrics API behavior
   - **Mitigation:** Story 1.2 includes manual review of generated code for completeness. Story 1.9 POC validation will catch discrepancies early.

2. **RISK:** API may change during Epic 1 development, invalidating generated code
   - **Mitigation:** Lock to specific OpenAPI spec version during Epic 1. Regeneration workflow (Epic 2) handles future changes.

3. **RISK:** Generated code from openapi-python-client may have bugs or unexpected behavior
   - **Mitigation:** openapi-python-client is mature (used by many projects). Adapter pattern isolates users from generated code issues.

4. **RISK:** Tight timeline (1-2 weeks) may force scope cuts
   - **Mitigation:** Epic 1 is already minimal POC scope. Stories 1.1-1.7 are hard requirements. Story 1.8-1.9 could be simplified if needed.

5. **RISK:** No access to test Supermetrics API credentials for validation
   - **Mitigation:** Use httpx MockTransport for unit tests. Story 1.9 examples can use mocked responses. Manual validation with real API deferred to customer POC.

**Assumptions:**

1. **ASSUMPTION:** Supermetrics API provides complete OpenAPI 3.x specification
   - **Validation:** Confirm with Supermetrics team in Story 1.2

2. **ASSUMPTION:** OpenAPI spec includes all endpoints needed for POC (login_links, logins, accounts, queries)
   - **Validation:** Manual review in Story 1.2

3. **ASSUMPTION:** API authentication uses Bearer token in Authorization header
   - **Validation:** Verify with API documentation or Supermetrics team

4. **ASSUMPTION:** Python 3.10+ is acceptable for target users (enterprise customer, internal tooling)
   - **Validation:** Confirmed acceptable based on PRD requirements

5. **ASSUMPTION:** httpx and Pydantic v2 are production-ready and stable
   - **Validation:** Both are mature, widely-used libraries with active maintenance

6. **ASSUMPTION:** Basic unit tests in Epic 1 are sufficient for POC validation (80%+ coverage deferred to Epic 2)
   - **Validation:** POC success depends on functional correctness, not coverage metrics

**Open Questions:**

1. **QUESTION:** Do we have access to a test/sandbox Supermetrics API environment for development?
   - **Next Step:** Ask Supermetrics team (Story 1.2)
   - **Impact:** Determines whether Story 1.9 uses real API or mocked responses

2. **QUESTION:** Does the OpenAPI spec include all optional query parameters, or only required ones?
   - **Next Step:** Review spec in Story 1.2
   - **Impact:** May need manual additions to generated code or adapter layer

3. **QUESTION:** Are there rate limits on Supermetrics API that SDK should handle?
   - **Next Step:** Check API documentation
   - **Impact:** Out of scope for Epic 1 (deferred to Epic 2), but good to know for future

4. **QUESTION:** Should SDK support custom base URLs for different API environments (prod, staging)?
   - **Next Step:** Check with stakeholders
   - **Impact:** Already supported via `base_url` parameter (Story 1.3), just needs documentation

## Test Strategy Summary

**Test Levels:**

1. **Unit Tests (Stories 1.3-1.8):**
   - **Framework:** pytest + pytest-asyncio
   - **Coverage Target:** Basic coverage of all public methods (80%+ coverage deferred to Epic 2 Story 2.1)
   - **Scope:** Test each resource adapter method (create, get, list, etc.) with mocked httpx responses
   - **Mocking Strategy:** Use httpx MockTransport to simulate API responses without real API calls
   - **Test Organization:** `tests/unit/test_client_init.py`, `test_login_links.py`, `test_logins.py`, `test_accounts.py`, `test_queries.py`, `test_exceptions.py`

2. **Integration Tests (Story 1.9):**
   - **Scope:** Complete end-to-end flow from client initialization to query execution
   - **Approach:** Test files: `tests/integration/test_complete_flow.py`, `test_async_flow.py`
   - **Mocking:** Use httpx MockTransport to simulate complete API interaction sequence
   - **Validation:** Verify complete customer onboarding journey works end-to-end

3. **Manual Validation (Story 1.9):**
   - **Approach:** Run example scripts (`examples/complete_flow.py`, `examples/async_flow.py`)
   - **Validation:** Verify type hints work in IDE (autocomplete, type checking)
   - **Real API Testing:** If test credentials available, validate against real Supermetrics API

**Test Fixtures (Story 1.8):**
- **Mock Responses:** JSON fixtures in `tests/fixtures/mock_responses.json` with sample API responses
- **Test Data:** Shared test data and factories in `tests/fixtures/test_data.py`
- **httpx Mocking:** Reusable httpx mock fixtures in `tests/conftest.py`

**Edge Cases and Error Scenarios:**

| Scenario | Test Location | Validation |
|----------|--------------|------------|
| Invalid API key (401) | `test_exceptions.py` | Verify `AuthenticationError` raised with clear message |
| Invalid parameters (400) | `test_exceptions.py` | Verify `ValidationError` raised with parameter details |
| Resource not found (404) | `test_exceptions.py` | Verify `APIError` raised with endpoint context |
| API server error (5xx) | `test_exceptions.py` | Verify `APIError` raised with status code |
| Network timeout | `test_exceptions.py` | Verify `NetworkError` raised with timeout context |
| Connection refused | `test_exceptions.py` | Verify `NetworkError` raised |
| Invalid Pydantic data | `test_login_links.py`, etc. | Verify validation before API call |
| Async query polling | `test_queries.py` | Verify `get_results()` retrieves pending query results |

**Type Checking (Stories 1.3-1.7):**
- **Tool:** mypy with strict mode
- **Validation:** All public APIs have complete type hints
- **CI Integration:** Deferred to Epic 2 Story 2.4 (GitHub Actions)
- **Manual Check:** Run `mypy src/` during each story

**Code Quality (Stories 1.3-1.7):**
- **Tool:** ruff (linting + formatting)
- **Validation:** Code passes `ruff check src/` and formatted with `ruff format src/`
- **CI Integration:** Deferred to Epic 2 Story 2.4
- **Manual Check:** Run ruff during each story

**Out of Scope for Epic 1:**
- Performance/load testing (manual performance check in Story 1.9 sufficient)
- Security testing (penetration testing, vulnerability scanning)
- Comprehensive test coverage >80% (Epic 2 Story 2.1)
- Multi-Python version testing (3.10, 3.11, 3.12) - Epic 2 Story 2.4
- Multi-OS testing (Linux, macOS, Windows) - Epic 2 Story 2.4
