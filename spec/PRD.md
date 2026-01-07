# Supermetrics python SDK Product Requirements Document (PRD)

**Author:** Aleksei
**Date:** 2025-10-24
**Project Level:** 2
**Target Scale:** Level 2 - Greenfield Software Project

---

## Goals and Background Context

### Goals

- Enable enterprise customer POC and close deal by delivering working Python SDK within 1-2 weeks
- Reduce customer integration time by 80% (from 2-4 weeks to 2-4 days) through type-safe, auto-generated SDK
- Establish official Python SDK as foundation for API ecosystem growth, supporting 50+ active users and enabling internal tooling (MCP server)

### Background Context

Supermetrics API customers currently face significant integration friction, requiring 2-4 weeks of manual HTTP client implementation for each integration. With 100+ API customers and no official Python SDK, developers must hand-code authentication flows, request formatting, and response parsing—work that could be automated. This creates inconsistent implementations, maintenance burden, and lost opportunities as prospects choose competitors like Fivetran and Airbyte who offer mature SDK experiences.

A large enterprise customer is currently blocked from POC without a Python SDK, creating urgency for delivery. The technical research phase validated a proven technology stack (openapi-python-client + httpx + Pydantic v2) using an adapter pattern architecture that enables monthly regeneration from OpenAPI without breaking users. This SDK will serve as the foundation for broader API ecosystem growth, including internal tooling (MCP server) and partner integrations.

---

## Requirements

### Functional Requirements

**Authentication & Client Initialization**
- FR001: SDK shall support API key-based authentication for client initialization
- FR002: SDK shall provide both synchronous (`SupermetricsClient`) and asynchronous (`SupermetricsAsyncClient`) client classes
- FR003: SDK shall support custom User-Agent headers and additional custom headers for all API requests
- FR004: SDK shall support configurable request timeouts

**Login Links Management**
- FR005: SDK shall support creating login links for data source authentication (ds_id, description)
- FR006: SDK shall support retrieving login link details by ID
- FR007: SDK shall support listing all login links and closing/expiring login links

**Logins & Accounts Management**
- FR008: SDK shall support retrieving login details by login link ID or login_username
- FR009: SDK shall support retrieving accounts by login_username or data source ID with filtering

**Data Queries**
- FR010: SDK shall support executing data queries with fields, date ranges, accounts, and data source parameters
- FR011: SDK shall support retrieving query results including handling async query polling patterns

**Type Safety & Developer Experience**
- FR012: SDK shall generate Pydantic v2 models for all request and response objects with full type hints
- FR013: SDK shall provide resource-based organization (client.login_links.create(), client.accounts.list(), etc.)

**Error Handling & Validation**
- FR014: SDK shall raise clear exceptions for HTTP errors and API error responses
- FR015: SDK shall validate input parameters using Pydantic models before API calls

### Non-Functional Requirements

- NFR001: **Performance** - SDK overhead shall be <10ms per API request; async client shall support 100+ concurrent requests
- NFR002: **Distribution & Compatibility** - SDK shall be published to PyPI, installable via `pip install supermetrics-sdk`, supporting Python 3.10+ on Linux, macOS, and Windows with minimal dependencies (httpx, Pydantic, <5 total libraries)
- NFR003: **Maintainability** - SDK shall be regeneratable from OpenAPI specification monthly without breaking existing user code through stable adapter pattern architecture

---

## User Journeys

### Journey 1: Data Engineer - First Integration with Supermetrics API

**Actor:** Sarah, Backend Developer at Enterprise Analytics Company

**Goal:** Integrate Supermetrics data into internal analytics dashboard

**Preconditions:**
- Sarah has a valid Supermetrics API key
- Python 3.10+ environment set up
- SDK installed via `pip install supermetrics-sdk`

**Flow:**

1. **Initialize SDK Client**
   - Sarah imports and initializes the SupermetricsClient with her API key
   - SDK validates credentials and creates authenticated client
   - *Expected outcome:* Client ready for API calls

2. **Create Login Link for Data Source**
   - Sarah creates a login link for Google Analytics 4 (GAWA) data source
   - Provides description: "Company Analytics Dashboard - GAWA Integration"
   - *Expected outcome:* Login link created with unique ID and authentication URL

3. **User Authentication Flow**
   - Sarah shares authentication URL with authorized user (marketing team member)
   - User authenticates with Google via the login link
   - Supermetrics stores authorized credentials
   - *Expected outcome:* Login credentials authorized and stored

4. **Retrieve Login Information**
   - Sarah polls the login endpoint to confirm authentication completed
   - SDK returns login details including login_username
   - *Expected outcome:* Login confirmed with login_username for subsequent calls

5. **Get Available Accounts**
   - Sarah requests accounts list using login_username
   - SDK returns all accessible GAWA properties/accounts
   - *Expected outcome:* List of accounts with IDs and metadata

6. **Execute Data Query**
   - Sarah executes query for sessions and users metrics
   - Specifies date range (last 30 days), selected account, and desired fields
   - SDK handles async query polling if needed
   - *Expected outcome:* Data returned in structured format with Pydantic models

7. **Process and Display Results**
   - Sarah accesses typed response data with IDE autocomplete
   - Transforms data for dashboard display
   - *Expected outcome:* Data successfully integrated into analytics dashboard

**Success Criteria:**
- Complete integration from installation to working data query in under 30 minutes
- Type-safe code with IDE autocomplete throughout
- Clear error messages if authentication or query fails
- No manual HTTP request construction needed

**Alternative Flows:**
- **Authentication timeout:** If user doesn't authenticate within timeout, Sarah receives clear error and can retry with new login link
- **Invalid query parameters:** SDK validates parameters before API call and provides clear Pydantic validation errors

---

## UX Design Principles

1. **Pythonic and Intuitive** - SDK follows Python conventions and idioms; resource-based organization (`client.login_links.create()`) feels natural to Python developers
2. **Type-Safe by Default** - Full type hints with Pydantic models provide IDE autocomplete, catch errors early, and enable confident refactoring
3. **Progressive Disclosure** - Simple use cases require minimal code; advanced features available when needed without cluttering basic workflows
4. **Clear Error Guidance** - Exceptions provide actionable error messages with context; Pydantic validation errors guide developers to correct usage

---

## User Interface Design Goals

**Platform & Interface:**
- **Target Environments:** Python code editors (VS Code, PyCharm, Jupyter notebooks), CLI/terminal, CI/CD pipelines
- **Core Interaction Pattern:** Import SDK → Initialize client → Call resource methods → Process typed responses
- **Developer Interface:** Code API with comprehensive type hints, docstrings, and auto-generated documentation

**Design Constraints:**
- Pure Python SDK - no graphical UI components
- Follow PEP 8 style guide and Python naming conventions
- Minimal dependencies to reduce installation friction
- Cross-platform compatibility (Linux, macOS, Windows)

**Documentation as UI:**
- README with quick-start guide (zero to first API call in 5 minutes)
- API reference documentation (auto-generated from code)
- Example scripts demonstrating common patterns
- Jupyter notebook examples for interactive exploration

---

## Epic List

**Epic 1: Project Foundation & Core SDK Generation**
- **Goal:** Establish project infrastructure, generate working SDK from OpenAPI, and implement adapter pattern foundation for core authentication and query flows
- **Estimated Stories:** 8-10 stories
- **Deliverable:** Working POC SDK with login links, logins, accounts, and queries - sufficient for enterprise customer POC

**Epic 2: Production SDK & Distribution**
- **Goal:** Complete comprehensive testing, documentation, examples, CI/CD automation, and PyPI publication for public release
- **Estimated Stories:** 8 stories
- **Deliverable:** Production-ready SDK published to PyPI with full documentation, examples, CI/CD automation, and regeneration workflows

**Total Estimated Stories:** 17

> **Note:** Detailed epic breakdown with full story specifications is available in [epics.md](./epics.md)

---

## Out of Scope

**Deferred to Phase 2 (Post-MVP):**
- OAuth2 authentication flow support
- Webhook event handling
- Advanced retry strategies with exponential backoff
- Request rate limiting and throttling
- Response caching layer
- Batch operations for multiple queries
- Streaming data support
- CLI tool for command-line operations
- Async context manager patterns
- Metrics and telemetry collection
- Multi-region API support

**Additional Language SDKs:**
- JavaScript/TypeScript SDK
- Go SDK
- Ruby SDK
- Other language implementations

**Explicitly Not Included:**
- Data transformation or processing logic (user's responsibility)
- Storage or caching of API credentials (security best practice)
- UI components or visualization tools
- Python 3.9 or earlier version support
- Alternative authentication methods beyond API key (OAuth2 is Phase 2)
- Integration with specific frameworks (Airflow, Dagster, Prefect) - future opportunities
- Custom fields and blends support (may be included if time permits, but not MVP requirement)