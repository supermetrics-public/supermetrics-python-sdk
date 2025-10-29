# Supermetrics python SDK - Epic Breakdown

**Author:** Aleksei
**Date:** 2025-10-24
**Project Level:** 2
**Target Scale:** Level 2 - Greenfield Software Project

---

## Overview

This document provides the detailed epic breakdown for Supermetrics python SDK, expanding on the high-level epic list in the [PRD](./PRD.md).

Each epic includes:

- Expanded goal and value proposition
- Complete story breakdown with user stories
- Acceptance criteria for each story
- Story sequencing and dependencies

**Epic Sequencing Principles:**

- Epic 1 establishes foundational infrastructure and initial functionality
- Subsequent epics build progressively, each delivering significant end-to-end value
- Stories within epics are vertically sliced and sequentially ordered
- No forward dependencies - each story builds only on previous work

---

## Epic 1: Project Foundation & Core SDK Generation

### Expanded Goal

Establish the complete project infrastructure and generate a working Python SDK from the OpenAPI specification. Implement the adapter pattern architecture to provide a stable, type-safe public API for core authentication and data query flows. By the end of this epic, we will have a functional POC SDK that supports the complete customer onboarding journey (login links → logins → accounts → queries), sufficient for the enterprise customer POC validation.

This epic delivers immediate value by unblocking the customer POC while establishing the architectural foundation for long-term SDK maintainability through the adapter pattern and monthly regeneration capability.

### Story Breakdown

**Story 1.1: Initialize Python Project Structure**

As a developer,
I want a properly structured Python project with modern tooling,
So that the SDK has a professional foundation and follows Python best practices.

**Acceptance Criteria:**
1. Repository created with `.gitignore`, `LICENSE` (Apache 2.0), and `README.md` skeleton
2. `pyproject.toml` configured with project metadata, dependencies, and build system (hatchling or setuptools)
3. Project structure created: `supermetrics_sdk/` (source), `tests/`, `examples/`, `docs/`, `scripts/`
4. Python 3.10+ compatibility verified
5. Git repository initialized with initial commit

**Prerequisites:** None

---

**Story 1.2: Generate Initial SDK from OpenAPI Specification**

As a developer,
I want to generate Python client code from the Supermetrics OpenAPI specification,
So that I have type-safe models and API client foundation.

**Acceptance Criteria:**
1. OpenAPI specification file obtained and stored in project root
2. `openapi-python-client` installed as dev dependency
3. Initial SDK generated into `supermetrics_sdk/_generated/` directory
4. Generated code includes sync and async clients, Pydantic models, and API endpoints
5. Generated code reviewed for completeness (login_links, logins, accounts, queries endpoints present)
6. Generation script created in `scripts/regenerate_client.sh` for future use

**Prerequisites:** Story 1.1 complete

---

**Story 1.3: Create Adapter Pattern Foundation**

As a developer,
I want a stable public API layer that wraps the generated code,
So that monthly OpenAPI regeneration won't break existing users.

**Acceptance Criteria:**
1. `supermetrics_sdk/client.py` created with `SupermetricsClient` class accepting `api_key`, optional `user_agent`, and `custom_headers`
2. `SupermetricsAsyncClient` class created with same initialization signature
3. Both clients wrap `_generated` client with custom headers injection
4. `supermetrics_sdk/__init__.py` exports public API (both client classes)
5. Complete type hints and docstrings added to public client classes
6. Code passes `mypy` strict type checking
7. Code formatted with `black` or `ruff` formatter
8. Simple initialization test added (`tests/test_client_init.py`)

**Prerequisites:** Story 1.2 complete

---

**Story 1.4: Implement Login Links Resource Adapter**

As a developer,
I want a clean, Pythonic interface for login link operations,
So that users can easily create and manage data source authentication links.

**Acceptance Criteria:**
1. `supermetrics_sdk/resources/login_links.py` created with `LoginLinksResource` class
2. Methods implemented: `create()`, `get()`, `list()`, `close()`
3. Methods wrap `_generated` client calls with proper parameter mapping
4. Both sync and async versions implemented (`LoginLinksResource` and `LoginLinksAsyncResource`)
5. Resources attached to client: `client.login_links` property
6. Complete type hints and docstrings added for all public methods
7. Code passes `mypy` strict type checking and formatted with `black`/`ruff`
8. Unit tests added covering all CRUD operations

**Prerequisites:** Story 1.3 complete

---

**Story 1.5: Implement Logins Resource Adapter**

As a developer,
I want a clean interface for retrieving login information,
So that users can verify authentication completion and obtain login credentials.

**Acceptance Criteria:**
1. `supermetrics_sdk/resources/logins.py` created with `LoginsResource` class
2. Methods implemented: `get()`, `list()`, `get_by_username()`
3. Both sync and async versions implemented
4. Resources attached to client: `client.logins` property
5. Complete type hints and docstrings added
6. Code passes `mypy` strict type checking and formatted with `black`/`ruff`
7. Unit tests added covering all operations

**Prerequisites:** Story 1.4 complete

---

**Story 1.6: Implement Accounts Resource Adapter**

As a developer,
I want a clean interface for retrieving data source accounts,
So that users can discover available accounts for querying.

**Acceptance Criteria:**
1. `supermetrics_sdk/resources/accounts.py` created with `AccountsResource` class
2. Methods implemented: `list()`, `get_by_login()`, `get_by_datasource()`, with filtering support
3. Both sync and async versions implemented
4. Resources attached to client: `client.accounts` property
5. Complete type hints and docstrings added
6. Code passes `mypy` strict type checking and formatted with `black`/`ruff`
7. Unit tests added covering all operations

**Prerequisites:** Story 1.5 complete

---

**Story 1.7: Implement Queries Resource Adapter**

As a developer,
I want a clean interface for executing data queries,
So that users can fetch marketing data with proper parameter validation.

**Acceptance Criteria:**
1. `supermetrics_sdk/resources/queries.py` created with `QueriesResource` class
2. Methods implemented: `execute()`, `get_results()`, with support for fields, date ranges, accounts, data source parameters
3. Basic async query polling support implemented (check status, retrieve results)
4. Both sync and async versions implemented
5. Resources attached to client: `client.queries` property
6. Complete type hints and docstrings added
7. Code passes `mypy` strict type checking and formatted with `black`/`ruff`
8. Unit tests added covering query execution and result retrieval

**Prerequisites:** Story 1.6 complete

---

**Story 1.8: Create Basic Error Handling**

As a developer,
I want clear exceptions when API calls fail,
So that SDK users can handle errors appropriately.

**Acceptance Criteria:**
1. `supermetrics_sdk/exceptions.py` created with custom exception classes: `SupermetricsError`, `AuthenticationError`, `APIError`, `ValidationError`
2. Adapter methods wrap generated client exceptions and re-raise as custom exceptions with clear messages
3. HTTP error codes mapped to appropriate exception types (401 → AuthenticationError, etc.)
4. Exception messages include relevant context (endpoint, status code, API error details)
5. Unit tests added for error scenarios

**Prerequisites:** Story 1.7 complete

---

**Story 1.9: Create POC Example and Validation**

As a developer,
I want a working example demonstrating the complete onboarding flow,
So that we can validate the POC with the enterprise customer.

**Acceptance Criteria:**
1. `examples/complete_flow.py` created demonstrating: initialize client → create login link → get login → list accounts → execute query
2. `examples/async_flow.py` created with async version of complete flow
3. Example includes comments explaining each step
4. Both examples tested manually against Supermetrics API (or mocked if no test credentials)
5. README updated with quick-start guide referencing examples
6. POC validated: complete flow works end-to-end with type safety and IDE autocomplete

**Prerequisites:** Story 1.8 complete

---

## Epic 2: Production SDK & Distribution

### Expanded Goal

Transform the POC SDK into a production-ready package suitable for public PyPI distribution. Complete comprehensive testing, documentation, examples, and CI/CD automation to ensure SDK quality, maintainability, and ease of adoption. Establish monthly regeneration workflows and monitoring to support ongoing SDK maintenance. By the end of this epic, the SDK will be publicly available on PyPI with full documentation, empowering 100+ API customers to integrate efficiently.

This epic delivers the strategic value of reducing customer integration time by 80% and establishing Supermetrics as having enterprise-grade developer tooling competitive with Fivetran and Airbyte.

### Story Breakdown

**Story 2.1: Expand Test Coverage to 80%+**

As a developer,
I want comprehensive test coverage across all SDK functionality,
So that the SDK is reliable and regressions are caught early.

**Acceptance Criteria:**
1. Unit tests expanded to cover all adapter methods, edge cases, and error scenarios
2. Integration tests added for complete flows (may use mocking or test API credentials)
3. Test coverage measured with `pytest-cov` and reaches 80%+ across all modules
4. Async tests added using `pytest-asyncio`
5. Test fixtures created for reusable test data and mocked responses
6. CI test suite runs successfully

**Prerequisites:** Epic 1 complete

---

**Story 2.2: Create Comprehensive Documentation**

As a developer,
I want clear, comprehensive documentation,
So that SDK users can integrate quickly without extensive support.

**Acceptance Criteria:**
1. README.md completed with: installation, quick-start, authentication, basic usage examples, links to full docs
2. API reference documentation generated using Sphinx or MkDocs from docstrings
3. User guide created covering: installation, authentication, common patterns, error handling, async usage
4. Contributing guide added for community contributions
5. Changelog initialized for version tracking
6. Documentation deployable to GitHub Pages or Read the Docs

**Prerequisites:** Story 2.2 complete

---

**Story 2.3: Create Jupyter Notebook Examples**

As a data scientist,
I want interactive Jupyter notebook examples,
So that I can explore the SDK capabilities in a familiar environment.

**Acceptance Criteria:**
1. `examples/notebooks/quickstart.ipynb` created demonstrating basic authentication and query
2. `examples/notebooks/complete_workflow.ipynb` created with full onboarding flow
3. Notebooks include markdown explanations, code cells, and example outputs
4. Notebooks tested and validated for execution
5. README links to notebook examples

**Prerequisites:** Story 2.2 complete

---

**Story 2.4: Setup CI/CD Pipeline**

As a developer,
I want automated testing and deployment,
So that releases are reliable and deployment is streamlined.

**Acceptance Criteria:**
1. GitHub Actions workflow created for: run tests, type checking, linting on every push/PR
2. Multi-Python version testing matrix configured (3.10, 3.11, 3.12)
3. Multi-OS testing configured (Ubuntu, macOS, Windows)
4. Automated PyPI publishing workflow created (triggered on release tag)
5. Test PyPI publishing tested successfully
6. All CI workflows passing

**Prerequisites:** Story 2.4 complete

---

**Story 2.5: Prepare PyPI Package**

As a developer,
I want the SDK properly packaged for PyPI distribution,
So that users can install it easily with `pip install supermetrics-sdk`.

**Acceptance Criteria:**
1. `pyproject.toml` completed with all metadata: name, version, description, authors, license, classifiers, dependencies
2. Package built successfully using `python -m build`
3. Package tested locally with `pip install dist/supermetrics_sdk-*.whl`
4. Long description pulled from README.md for PyPI page
5. Package includes all necessary files (source, LICENSE, README)
6. Version number follows semantic versioning (1.0.0)

**Prerequisites:** Story 2.4 complete

---

**Story 2.6: Publish to PyPI and Verify Installation**

As a developer,
I want the SDK published to PyPI,
So that users worldwide can install and use the SDK.

**Acceptance Criteria:**
1. SDK published to PyPI using GitHub Actions automated workflow
2. Installation verified: `pip install supermetrics-sdk` works from clean environment
3. PyPI package page displays correctly with description, metadata, and links
4. Quick-start example runs successfully with installed package
5. GitHub release created with changelog and download links
6. Internal stakeholders notified of release

**Prerequisites:** Story 2.6 complete

---

**Story 2.7: Create Regeneration Workflow**

As a developer,
I want automated SDK regeneration from OpenAPI,
So that the SDK stays in sync with API changes without manual effort.

**Acceptance Criteria:**
1. GitHub Actions workflow created to run monthly (or on-demand)
2. Workflow fetches latest OpenAPI spec, regenerates `_generated/` code, runs tests
3. If tests pass, creates PR with regenerated code for review
4. If tests fail, creates GitHub issue with failure details
5. Documentation added explaining regeneration process
6. First regeneration test run successfully

**Prerequisites:** Story 2.6 complete

---

**Story 2.8: Customer Onboarding and Success Validation**

As a product manager,
I want the enterprise customer successfully using the SDK,
So that we validate the SDK meets customer needs and close the deal.

**Acceptance Criteria:**
1. Enterprise customer provided with SDK installation instructions and documentation
2. Customer successfully completes POC integration using the SDK
3. Customer feedback collected and documented
4. Any critical customer-reported issues addressed
5. Customer POC marked as successful
6. Success metrics tracked: integration time, customer satisfaction

**Prerequisites:** Story 2.7 complete

---

## Story Guidelines Reference

**Story Format:**

```
**Story [EPIC.N]: [Story Title]**

As a [user type],
I want [goal/desire],
So that [benefit/value].

**Acceptance Criteria:**
1. [Specific testable criterion]
2. [Another specific criterion]
3. [etc.]

**Prerequisites:** [Dependencies on previous stories, if any]
```

**Story Requirements:**

- **Vertical slices** - Complete, testable functionality delivery
- **Sequential ordering** - Logical progression within epic
- **No forward dependencies** - Only depend on previous work
- **AI-agent sized** - Completable in 2-4 hour focused session
- **Value-focused** - Integrate technical enablers into value-delivering stories

---

**For implementation:** Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown.
