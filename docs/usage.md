# Usage

This page provides a quick overview of how to use the Supermetrics Python SDK. For detailed documentation, see the [User Guide](user-guide.md).

## Basic Usage

### Import and Initialize

```python
from supermetrics import SupermetricsClient

# Initialize the client with your API key
client = SupermetricsClient(api_key="your_api_key_here")
```

### Create Login Link

```python
# Create a login link for Google Analytics 4
link = client.login_links.create(
    ds_id="GAWA",
    description="My Analytics Connection"
)

print(f"Authentication URL: {link.login_url}")
print(f"Link ID: {link.link_id}")
```

### Get Login Details

```python
# After user authenticates, get the login details
login = client.logins.get(login_id=link.login_id)

print(f"Authenticated as: {login.username}")
print(f"Login ID: {login.login_id}")
```

### List Accounts

```python
# List available accounts for the data source
accounts = client.accounts.list(
    ds_id="GAWA",
    login_usernames=login.username
)

print(f"Found {len(accounts)} accounts")
for account in accounts:
    print(f"  - {account.account_name} ({account.account_id})")
```

### Execute Query

```python
# Execute a query to retrieve marketing data
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=[accounts[0].account_id],
    fields=["Date", "Sessions", "Users", "Pageviews"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)

if result and result.data:
    print(f"Retrieved {len(result.data)} rows")
    for row in result.data:
        print(row)
```

## Complete Example

```python
from supermetrics import SupermetricsClient

# Initialize client
client = SupermetricsClient(api_key="your_api_key")

try:
    # Create login link
    link = client.login_links.create(ds_id="GAWA", description="Q1 Report")
    print(f"Please authenticate at: {link.login_url}")

    # Wait for authentication
    input("Press Enter after authenticating...")

    # Get login
    updated_link = client.login_links.get(link.link_id)
    login = client.logins.get(updated_link.login_id)

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

    # Process results
    if result and result.data:
        print(f"Success! Retrieved {len(result.data)} rows")

finally:
    client.close()
```

## Error Handling

```python
from supermetrics import (
    SupermetricsClient,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError
)

client = SupermetricsClient(api_key="your_key")

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
except AuthenticationError as e:
    print(f"Invalid API key: {e.message}")
except ValidationError as e:
    print(f"Invalid parameters: {e.message}")
except APIError as e:
    print(f"API error: {e.message}")
except NetworkError as e:
    print(f"Network error: {e.message}")
```

## Async Support

```python
import asyncio
from supermetrics import SupermetricsAsyncClient

async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        # All methods are async
        accounts = await client.accounts.list(ds_id="GAWA")
        print(f"Found {len(accounts)} accounts")

        result = await client.queries.execute(
            ds_id="GAWA",
            ds_accounts=[accounts[0].account_id],
            fields=["Date", "Sessions", "Users"],
            start_date="2024-01-01",
            end_date="2024-01-31"
        )

        if result and result.data:
            print(f"Retrieved {len(result.data)} rows")

asyncio.run(main())
```

## Next Steps

- [User Guide](user-guide.md) - Comprehensive tutorials and examples
- [API Reference](api-reference.md) - Complete API documentation
- [Error Handling](error-handling.md) - Error handling patterns and best practices
- [Examples](../examples/) - Working code examples
