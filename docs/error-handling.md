# Error Handling Guide

Comprehensive guide to handling errors in the supermetrics Python SDK.

## Table of Contents

- [Exception Hierarchy](#exception-hierarchy)
- [Exception Types](#exception-types)
- [Error Handling Patterns](#error-handling-patterns)
- [Common Error Scenarios](#common-error-scenarios)
- [Best Practices](#best-practices)

---

## Exception Hierarchy

All SDK exceptions inherit from the `SupermetricsError` base class:

```
SupermetricsError (Base exception)
├── AuthenticationError (HTTP 401)
├── ValidationError (HTTP 400, 422)
├── APIError (HTTP 403, 404, 429, 5xx)
└── NetworkError (Network-level failures)
```

You can catch specific exceptions for granular error handling, or catch `SupermetricsError` to handle all SDK errors.

---

## Exception Types

### SupermetricsError

**Base exception for all SDK errors.**

```python
from supermetrics import SupermetricsError

try:
    client.accounts.list(ds_id="GAWA")
except SupermetricsError as e:
    print(f"SDK Error: {e.message}")
    print(f"HTTP Status: {e.status_code}")
    print(f"Endpoint: {e.endpoint}")
    print(f"Response: {e.response_body}")
```

**Attributes:**

- `message` (str): Human-readable error description
- `status_code` (int | None): HTTP status code (if applicable)
- `endpoint` (str | None): API endpoint that was called
- `response_body` (str | None): Raw API response for debugging

**When to use:**
- Catch all SDK errors with a single handler
- Generic error logging
- Top-level error boundaries

---

### AuthenticationError

**Raised when API authentication fails (HTTP 401).**

```python
from supermetrics import AuthenticationError

try:
    client = SupermetricsClient(api_key="invalid_key")
    client.login_links.list()
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Log error and prompt user to check API key
```

**Common causes:**

- Invalid API key
- Expired API key
- Revoked API key
- Missing Authorization header

**How to fix:**

1. Verify your API key is correct
2. Check if the API key has expired
3. Ensure the API key hasn't been revoked
4. Verify the API key has the necessary permissions

**Example: Graceful authentication handling**

```python
import os
from supermetrics import SupermetricsClient, AuthenticationError

def get_authenticated_client():
    """Get authenticated client with error handling."""
    api_key = os.getenv("SUPERMETRICS_API_KEY")

    if not api_key:
        raise ValueError("SUPERMETRICS_API_KEY environment variable not set")

    try:
        client = SupermetricsClient(api_key=api_key)
        # Test authentication
        client.login_links.list()
        return client
    except AuthenticationError:
        raise ValueError("Invalid API key. Please check your credentials.")

try:
    client = get_authenticated_client()
except ValueError as e:
    print(f"Setup error: {e}")
    exit(1)
```

---

### ValidationError

**Raised when request validation fails (HTTP 400, 422).**

```python
from supermetrics import ValidationError

try:
    # Missing required parameter
    client.accounts.list(ds_id="")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Response details: {e.response_body}")
```

**Common causes:**

- Missing required parameters
- Invalid parameter values
- Incorrect parameter types
- Parameters violating API constraints
- Malformed request body

**How to fix:**

1. Check that all required parameters are provided
2. Validate parameter values match expected format
3. Ensure parameter types are correct
4. Review API documentation for parameter constraints

**Example: Parameter validation**

```python
from supermetrics import SupermetricsClient, ValidationError
from datetime import datetime

def execute_query_with_validation(
    client,
    ds_id: str,
    account_ids: list[str],
    fields: list[str],
    start_date: str,
    end_date: str
):
    """Execute query with input validation."""
    # Validate inputs
    if not ds_id:
        raise ValueError("ds_id cannot be empty")
    if not account_ids:
        raise ValueError("At least one account ID required")
    if not fields:
        raise ValueError("At least one field required")
    if not start_date or not end_date:
        raise ValueError("Start and end dates are required")

    try:
        return client.queries.execute(
            ds_id=ds_id,
            ds_accounts=account_ids,
            fields=fields,
            start_date=start_date,
            end_date=end_date
        )
    except ValidationError as e:
        print(f"API validation failed: {e.message}")
        # Log the full response for debugging
        if e.response_body:
            print(f"Details: {e.response_body}")
        raise

# Usage
client = SupermetricsClient(api_key="your_key")

try:
    result = execute_query_with_validation(
        client,
        ds_id="GAWA",
        account_ids=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
except ValueError as e:
    print(f"Input error: {e}")
except ValidationError as e:
    print(f"API validation error: {e.message}")
```

---

### APIError

**Raised for API-level errors during request processing (HTTP 403, 404, 429, 5xx).**

```python
from supermetrics import APIError

try:
    client.logins.get("nonexistent_id")
except APIError as e:
    print(f"API error ({e.status_code}): {e.message}")

    # Handle specific status codes
    if e.status_code == 404:
        print("Resource not found")
    elif e.status_code == 429:
        print("Rate limited - retry later")
    elif e.status_code == 403:
        print("Forbidden - insufficient permissions")
    elif e.status_code >= 500:
        print("Server error - try again later")
```

**Common causes:**

- **404 Not Found**: Resource doesn't exist
- **403 Forbidden**: Insufficient permissions or account restrictions
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server-side error
- **503 Service Unavailable**: Service temporarily unavailable
- **504 Gateway Timeout**: Request timeout on server

**How to fix:**

- **404**: Verify resource ID is correct and resource exists
- **403**: Check account permissions and API key access level
- **429**: Implement retry logic with exponential backoff
- **500/503/504**: Retry the request after a delay

**Example: Comprehensive API error handling**

```python
import time
from supermetrics import SupermetricsClient, APIError

def execute_with_retry(client, max_retries=3, **query_params):
    """Execute query with retry logic for transient errors."""
    for attempt in range(max_retries):
        try:
            return client.queries.execute(**query_params)

        except APIError as e:
            # Rate limiting - exponential backoff
            if e.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1s, 2s, 4s
                    print(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise

            # Server errors - retry with delay
            elif e.status_code in [500, 503, 504]:
                if attempt < max_retries - 1:
                    wait_time = 5
                    print(f"Server error. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise

            # Not found or forbidden - don't retry
            elif e.status_code in [403, 404]:
                print(f"Error {e.status_code}: {e.message}")
                raise

            # Other errors - raise immediately
            else:
                raise

# Usage
client = SupermetricsClient(api_key="your_key")

try:
    result = execute_with_retry(
        client,
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
except APIError as e:
    print(f"Query failed after retries: {e.message}")
```

---

### NetworkError

**Raised for network-level failures before/during HTTP request.**

```python
from supermetrics import NetworkError

try:
    client = SupermetricsClient(api_key="key", timeout=1.0)
    client.login_links.list()
except NetworkError as e:
    print(f"Network error: {e.message}")
    # Check network connectivity
    # Verify firewall/proxy settings
```

**Common causes:**

- Connection timeout
- Connection refused (API server unreachable)
- DNS resolution failure
- Network connectivity issues
- Firewall blocking requests
- Proxy configuration issues
- SSL/TLS certificate errors

**How to fix:**

1. Check internet connectivity
2. Verify API endpoint is accessible
3. Check firewall/proxy settings
4. Increase timeout for slow connections
5. Verify SSL certificates are valid

**Example: Network error handling with timeout**

```python
from supermetrics import SupermetricsClient, NetworkError
import time

def create_robust_client(api_key, timeout=30.0, max_retries=3):
    """Create client with network error retry logic."""
    for attempt in range(max_retries):
        try:
            client = SupermetricsClient(api_key=api_key, timeout=timeout)
            # Test connectivity
            client.login_links.list()
            return client

        except NetworkError as e:
            print(f"Network error (attempt {attempt + 1}/{max_retries}): {e.message}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("Failed to establish connection after retries")
                raise

# Usage
try:
    client = create_robust_client(
        api_key="your_key",
        timeout=30.0,
        max_retries=3
    )
    print("Client connected successfully")
except NetworkError:
    print("Unable to connect. Check network connectivity.")
```

---

## Error Handling Patterns

### Pattern 1: Granular Exception Handling

Handle each exception type differently:

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
    # Authentication issues - likely configuration problem
    print(f"Auth error: {e.message}")
    # Action: Check API key configuration

except ValidationError as e:
    # Validation issues - likely code bug
    print(f"Validation error: {e.message}")
    # Action: Fix parameter values

except APIError as e:
    # API issues - handle based on status code
    if e.status_code == 429:
        print("Rate limited - wait and retry")
    elif e.status_code == 404:
        print("Resource not found - check IDs")
    else:
        print(f"API error: {e.message}")

except NetworkError as e:
    # Network issues - likely transient
    print(f"Network error: {e.message}")
    # Action: Retry request
```

### Pattern 2: Catch-All with Base Exception

Handle all SDK errors uniformly:

```python
from supermetrics import SupermetricsClient, SupermetricsError

client = SupermetricsClient(api_key="your_key")

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31"
    )

except SupermetricsError as e:
    # Handle all SDK errors
    print(f"SDK Error: {e.message}")
    print(f"Status Code: {e.status_code}")

    # Log error details
    import logging
    logging.error(
        f"SDK error: {e.message}",
        extra={
            "status_code": e.status_code,
            "endpoint": e.endpoint,
            "response_body": e.response_body
        }
    )
```

### Pattern 3: Contextual Error Handling

Different error handling for different operations:

```python
from supermetrics import SupermetricsClient, APIError

client = SupermetricsClient(api_key="your_key")

# Critical operation - fail fast
try:
    login = client.logins.get(login_id="login_123")
except APIError as e:
    if e.status_code == 404:
        raise ValueError(f"Login not found: {login_id}")
    raise

# Optional operation - continue on error
try:
    client.login_links.close(link_id="link_123")
except APIError as e:
    if e.status_code == 404:
        print("Link already closed or doesn't exist")
    else:
        print(f"Warning: Failed to close link: {e.message}")

# Batch operation - collect errors
errors = []
for account_id in account_ids:
    try:
        result = client.queries.execute(...)
        results.append(result)
    except APIError as e:
        errors.append({"account_id": account_id, "error": e.message})

if errors:
    print(f"Errors occurred for {len(errors)} accounts")
    for error in errors:
        print(f"  {error['account_id']}: {error['error']}")
```

### Pattern 4: Async Error Handling

Error handling in async code:

```python
import asyncio
from supermetrics import SupermetricsAsyncClient, APIError

async def fetch_with_error_handling(client, account_id):
    """Fetch data with error handling."""
    try:
        result = await client.queries.execute(
            ds_id="GAWA",
            ds_accounts=[account_id],
            fields=["Date", "Sessions"],
            start_date="2024-01-01",
            end_date="2024-01-31"
        )
        return {"account_id": account_id, "result": result, "error": None}

    except APIError as e:
        return {"account_id": account_id, "result": None, "error": e.message}

async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        # Fetch data for multiple accounts
        tasks = [
            fetch_with_error_handling(client, account_id)
            for account_id in ["123", "456", "789"]
        ]

        results = await asyncio.gather(*tasks)

        # Process results
        successful = [r for r in results if r["error"] is None]
        failed = [r for r in results if r["error"] is not None]

        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")

        for failure in failed:
            print(f"  {failure['account_id']}: {failure['error']}")

asyncio.run(main())
```

---

## Common Error Scenarios

### Scenario 1: Invalid API Key

```python
from supermetrics import SupermetricsClient, AuthenticationError

try:
    client = SupermetricsClient(api_key="invalid_key")
    client.login_links.list()
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print("Please check your API key in the environment variables")
```

### Scenario 2: Resource Not Found

```python
from supermetrics import SupermetricsClient, APIError

client = SupermetricsClient(api_key="your_key")

try:
    login = client.logins.get(login_id="nonexistent_id")
except APIError as e:
    if e.status_code == 404:
        print("Login not found. Verify the login ID is correct.")
    else:
        raise
```

### Scenario 3: Rate Limiting

```python
import time
from supermetrics import SupermetricsClient, APIError

client = SupermetricsClient(api_key="your_key")

def execute_with_backoff(client, **query_params):
    """Execute query with exponential backoff on rate limits."""
    max_retries = 5
    base_delay = 1

    for attempt in range(max_retries):
        try:
            return client.queries.execute(**query_params)

        except APIError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 1, 2, 4, 8, 16 seconds
                print(f"Rate limited. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

result = execute_with_backoff(
    client,
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### Scenario 4: Network Timeout

```python
from supermetrics import SupermetricsClient, NetworkError

# Increase timeout for slow connections
client = SupermetricsClient(api_key="your_key", timeout=60.0)

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-12-31"  # Large date range
    )
except NetworkError as e:
    print(f"Request timed out: {e.message}")
    print("Try reducing the date range or increasing the timeout")
```

### Scenario 5: Malformed Query Parameters

```python
from supermetrics import SupermetricsClient, ValidationError

client = SupermetricsClient(api_key="your_key")

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=[],  # Empty list - invalid
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print("At least one account ID is required")
```

---

## Best Practices

### 1. Always Handle Exceptions

Never let exceptions go unhandled:

```python
# Bad
result = client.queries.execute(...)

# Good
try:
    result = client.queries.execute(...)
except SupermetricsError as e:
    logger.error(f"Query failed: {e.message}")
    # Handle error appropriately
```

### 2. Log Error Details

Include all available error information:

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = client.queries.execute(...)
except SupermetricsError as e:
    logger.error(
        f"API request failed: {e.message}",
        extra={
            "status_code": e.status_code,
            "endpoint": e.endpoint,
            "response_body": e.response_body,
        }
    )
```

### 3. Implement Retry Logic

Retry transient errors (rate limits, server errors):

```python
import time
from supermetrics import APIError

def retry_on_transient_error(func, max_retries=3):
    """Decorator to retry on transient errors."""
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except APIError as e:
                if e.status_code in [429, 500, 503, 504]:
                    if attempt < max_retries - 1:
                        wait = 2 ** attempt
                        time.sleep(wait)
                        continue
                raise
    return wrapper

@retry_on_transient_error
def fetch_data(client):
    return client.queries.execute(...)
```

### 4. Provide User-Friendly Error Messages

Convert technical errors to user-friendly messages:

```python
from supermetrics import AuthenticationError, ValidationError, APIError

try:
    result = client.queries.execute(...)
except AuthenticationError:
    print("Your API key is invalid. Please check your configuration.")
except ValidationError as e:
    print(f"Invalid input: {e.message}")
    print("Please verify your query parameters.")
except APIError as e:
    if e.status_code == 429:
        print("Too many requests. Please wait a moment and try again.")
    elif e.status_code == 404:
        print("The requested resource was not found.")
    else:
        print(f"An error occurred: {e.message}")
```

### 5. Use Specific Exceptions When Possible

Catch specific exceptions for better control:

```python
# Good - specific handling
try:
    result = client.queries.execute(...)
except ValidationError as e:
    fix_parameters()
except APIError as e:
    if e.status_code == 429:
        retry_later()

# Less ideal - catch-all
try:
    result = client.queries.execute(...)
except SupermetricsError as e:
    # Harder to handle different error types
    pass
```

### 6. Clean Up Resources

Always close clients, even when errors occur:

```python
# Good - context manager handles cleanup
with SupermetricsClient(api_key="key") as client:
    result = client.queries.execute(...)

# Also good - manual cleanup
client = SupermetricsClient(api_key="key")
try:
    result = client.queries.execute(...)
finally:
    client.close()
```

### 7. Monitor and Alert

Set up monitoring for production errors:

```python
import logging
from supermetrics import SupermetricsError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    result = client.queries.execute(...)
except SupermetricsError as e:
    # Log error
    logger.error(f"Query failed: {e.message}", extra={
        "status_code": e.status_code,
        "endpoint": e.endpoint
    })

    # Send alert for critical errors
    if isinstance(e, AuthenticationError):
        send_alert("Critical: API authentication failed")
    elif isinstance(e, APIError) and e.status_code >= 500:
        send_alert(f"Server error: {e.message}")
```

---

## Summary

- **Use specific exceptions** (`AuthenticationError`, `ValidationError`, etc.) for granular control
- **Implement retry logic** for transient errors (rate limits, server errors)
- **Log error details** including status code, endpoint, and response body
- **Provide user-friendly messages** instead of exposing technical errors
- **Always clean up resources** using context managers or try/finally
- **Monitor production errors** and set up alerts for critical failures

For more information, see:
- [API Reference](api-reference.md) - Complete API documentation
- [User Guide](user-guide.md) - Usage examples and tutorials
