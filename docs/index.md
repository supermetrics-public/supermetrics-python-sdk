# Supermetrics Python SDK Documentation

Welcome to the official documentation for the Supermetrics Python SDK – the Python client for Supermetrics API.

## What is the Supermetrics Python SDK?

The Supermetrics Python SDK is a type-safe Python client that provides seamless integration with the Supermetrics API. It features:

- Type-safe Python client generated from OpenAPI specification
- Dual sync/async support via separate Client classes
- Pydantic v2 models for request/response validation
- Comprehensive API coverage: login links (including update), logins (including account
  listing and revocation), accounts, queries, DWH transfers and transfer runs, DWH
  backfills, custom fields, account tags, Connector Builder
- Custom exception hierarchy with HTTP status code mapping
- Resource-based API organization
- API key, OAuth bearer token, and dynamic token provider authentication
- Per-request authorization, header, and timeout overrides on a shared connection pool
- `with_raw_response` access to HTTP status codes, headers, and raw payloads

## Quick Start

```python
from supermetrics import SupermetricsClient

# Initialize client
client = SupermetricsClient(api_key="your_api_key")

# Create login link
link = client.login_links.create(ds_id="GAWA", description="My Connection")

# Get login details
login = client.logins.get(login_id=link.login_id)

# List accounts
accounts = client.accounts.list(ds_id="GAWA", login_usernames=login.username)

# Execute query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=[accounts[0].account_id],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

## Documentation Contents

### Getting Started

- [Installation](installation.md) - Installation instructions and requirements
- [Usage](usage.md) - Quick usage overview and basic examples
- [Authentication & Transport](authentication-and-transport.md) - Credentials, dynamic token
  providers, per-request overrides, response metadata, and the error taxonomy

### Guides

- [User Guide](user-guide.md) - Comprehensive tutorials and examples covering:
  - Authentication workflows
  - Querying data
  - Async support
  - Best practices
  - Common data sources

- [API Reference](api-reference.md) - Complete API documentation including:
  - Client classes (sync and async)
  - Resource methods (login links, logins, accounts, queries, transfers, transfer runs,
    backfills, custom fields, account tags)
  - Models and types
  - Exception classes

- [Error Handling](error-handling.md) - Error handling patterns and best practices:
  - Exception hierarchy
  - Common error scenarios
  - Retry strategies
  - Production-ready error handling

- [OpenAPI Code Generation](openapi-generation.md) - Pipeline for generating and updating SDK client code from OpenAPI specs

### Additional Resources

- [Examples](https://github.com/supermetrics-public/SuperPy-SDK/tree/main/examples) - Working code examples
- [Contributing](https://github.com/supermetrics-public/SuperPy-SDK/blob/main/CONTRIBUTING.md) - Contributing guidelines

## Key Features

### Type Safety

All request and response models are fully typed using Pydantic v2:

```python
link = client.login_links.create(ds_id="GAWA")
# link is typed as LoginLink with full IDE autocomplete
print(link.login_url)  # Type-safe access
```

### Dual Sync/Async Support

Choose the right client for your use case:

```python
# Synchronous - for scripts and notebooks
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="key")
accounts = client.accounts.list(ds_id="GAWA")

# Asynchronous - for production apps
from supermetrics import SupermetricsAsyncClient

async with SupermetricsAsyncClient(api_key="key") as client:
    accounts = await client.accounts.list(ds_id="GAWA")
```

### Comprehensive Error Handling

Specific exceptions for different error types:

```python
from supermetrics import (
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError
)

try:
    result = client.queries.execute(...)
except AuthenticationError:
    # Handle auth errors
except ValidationError:
    # Handle validation errors
except APIError as e:
    # Handle API errors with status code
    if e.status_code == 429:
        # Handle rate limiting
```

### Resource-Based Organization

Clean, intuitive API organized by resource type:

```python
client.login_links.create(...)
client.login_links.get(...)
client.login_links.list()
client.login_links.update(...)
client.login_links.close(...)

client.logins.get(...)
client.logins.list()
client.logins.get_accounts(...)
client.logins.revoke(...)
client.logins.get_by_username(...)

client.accounts.list(...)

client.queries.execute(...)
client.queries.get_results(...)

client.account_tags.list(...)
client.account_tags.get(...)
client.account_tags.create(...)
client.account_tags.add_accounts(...)

client.teams.get(team_id=...)
client.teams.list_users(team_id=...)
```

## Supported Data Sources

The SDK supports all Supermetrics data sources including:

- Google Analytics 4 (GAWA)
- Google Ads
- Facebook Ads
- LinkedIn Ads
- Twitter Ads
- And many more...

See the [User Guide](user-guide.md#common-data-sources) for data source-specific examples.

## Getting Help

- Check the [User Guide](user-guide.md) for tutorials and examples
- Review the [API Reference](api-reference.md) for detailed method documentation
- See [Error Handling](error-handling.md) for troubleshooting
- Explore the [examples](https://github.com/supermetrics-public/SuperPy-SDK/tree/main/examples) directory for working code

## License

This project is licensed under the Apache License v2. See the LICENSE file for details.

