# Supermetrics Python SDK Documentation

Welcome to the official documentation for the Supermetrics Python SDK – the Python client for Supermetrics API.

## What is the Supermetrics Python SDK?

The Supermetrics Python SDK is a type-safe Python client that provides seamless integration with the Supermetrics API. It features:

- Type-safe Python client generated from OpenAPI specification
- Dual sync/async support via separate Client classes
- Pydantic v2 models for request/response validation
- Comprehensive API coverage: login links, logins, accounts, queries
- Custom exception hierarchy with HTTP status code mapping
- Resource-based API organization

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
    end_date="2024-01-31"
)
```

## Documentation Contents

### Getting Started

- [Installation](installation.md) - Installation instructions and requirements
- [Usage](usage.md) - Quick usage overview and basic examples

### Guides

- [User Guide](user-guide.md) - Comprehensive tutorials and examples covering:
  - Authentication workflows
  - Querying data
  - Async support
  - Best practices
  - Common data sources

- [API Reference](api-reference.md) - Complete API documentation including:
  - Client classes (sync and async)
  - Resource methods (login links, logins, accounts, queries)
  - Models and types
  - Exception classes

- [Error Handling](error-handling.md) - Error handling patterns and best practices:
  - Exception hierarchy
  - Common error scenarios
  - Retry strategies
  - Production-ready error handling

### Additional Resources

- [Examples](../examples/) - Working code examples
- [Contributing](contributing.md) - Contributing guidelines
- [History](history.md) - Version history and changelog

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
client.login_links.close(...)

client.logins.get(...)
client.logins.list()
client.logins.get_by_username(...)

client.accounts.list(...)

client.queries.execute(...)
client.queries.get_results(...)
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
- Explore the [examples/](../examples/) directory for working code

## License

This project is licensed under the Apache License v2. See the LICENSE file for details.

## Indices and Tables

- [Index](genindex)
- [Module Index](modindex)
- [Search](search)
