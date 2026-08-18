# Error Handling Guide

Comprehensive guide to handling errors in the supermetrics Python SDK.

> **Hierarchy change:** the exception tree is no longer flat. `AuthenticationError` and
> `ValidationError` are now **subclasses** of `APIError`, so an `except APIError` clause
> placed *before* them will match authentication and validation errors first and silently
> swallow them. Order specific exceptions before general ones — see
> [Migrating from the flat hierarchy](#migrating-from-the-flat-hierarchy).

## Table of Contents

- [Exception Hierarchy](#exception-hierarchy)
- [Exception Types](#exception-types)
- [Error Handling Patterns](#error-handling-patterns)
- [Common Error Scenarios](#common-error-scenarios)
- [Best Practices](#best-practices)
- [Summary](#summary)

---

## Exception Hierarchy

All SDK exceptions inherit from the `SupermetricsError` base class:

```
SupermetricsError
├── SupermetricsClientError        local configuration problems; also a ValueError
├── NetworkError                   timeout, connection refused, DNS, TLS
└── SupermetricsAPIError                           [alias: APIError]
    ├── SupermetricsAuthError       401            [alias: AuthenticationError]
    ├── SupermetricsForbiddenError  403
    ├── SupermetricsNotFoundError   404
    ├── SupermetricsValidationError 400 / 422      [alias: ValidationError]
    ├── SupermetricsRateLimitError  429
    └── SupermetricsServerError     5xx
```

You can catch specific exceptions for granular error handling, or catch `SupermetricsError`
to handle all SDK errors.

The three branches answer three different questions:

- `SupermetricsClientError` — the call never left the process. Something about the way the
  SDK was configured is wrong, and retrying will not help.
- `NetworkError` — the request left the process but no HTTP response came back. There is no
  `status_code`. Usually transient.
- `SupermetricsAPIError` — the API answered with a 4xx or 5xx. The subclass tells you which.

### Legacy names

`APIError`, `AuthenticationError`, and `ValidationError` remain importable and are now
aliases of `SupermetricsAPIError`, `SupermetricsAuthError`, and
`SupermetricsValidationError` respectively. Existing imports keep working; the names are
interchangeable with their `Supermetrics*` counterparts, including in `isinstance` checks.

### Migrating from the flat hierarchy

`except SupermetricsError` is unaffected. What changed is that the specific HTTP errors now
descend from `APIError`, so **clause order decides which handler runs**:

```python
from supermetrics import APIError, AuthenticationError, ValidationError

# Broken: APIError now matches 401 and 422 too, so the later clauses are dead code.
try:
    client.logins.list()
except APIError as e:
    print(f"API error: {e.message}")
except AuthenticationError:  # never reached
    refresh_credentials()
except ValidationError:  # never reached
    fix_parameters()

# Correct: specific first, general last.
try:
    client.logins.list()
except AuthenticationError:
    refresh_credentials()
except ValidationError:
    fix_parameters()
except APIError as e:
    print(f"API error: {e.message}")
```

To audit an existing codebase, look for any `except APIError` (or
`except SupermetricsAPIError`) that is followed by another `except` clause naming an HTTP
error. Those later clauses are now unreachable.

For the wider picture — credentials, per-request overrides, and reading response metadata —
see [Authentication & Transport](authentication-and-transport.md).

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
- `status_code` (int | None): HTTP status code (`None` for client and network errors)
- `endpoint` (str | None): API endpoint that was called
- `response_body` (str | None): Raw API response for debugging

**When to use:**
- Catch all SDK errors with a single handler
- Generic error logging
- Top-level error boundaries

---

### SupermetricsClientError

**Raised for client-side configuration and validation errors, before any HTTP request is
made.**

This exception also inherits from `ValueError`, so code that already catches `ValueError`
around client construction keeps working.

```python
from supermetrics import SupermetricsClient, SupermetricsClientError

try:
    client = SupermetricsClient()  # no credentials supplied
except SupermetricsClientError as e:
    print(f"Configuration problem: {e.message}")
    # "No credentials supplied. Provide exactly one of: api_key, bearer_token,
    #  or token_provider."
```

**Common causes:**

- No credential supplied to the constructor
- More than one of `api_key`, `bearer_token`, and `token_provider` supplied
- An `async def` token provider passed to the synchronous `SupermetricsClient`
- A credential the SDK cannot legally send: empty or whitespace-only (including a blank
  per-request `auth_token`, or a token provider that returns `""`), containing a control
  character such as a newline from a line-wrapped file, or containing a non-ASCII
  character such as a smart quote or en dash pasted from a document
- `with_raw_response` used on a call that issued no HTTP request

**How to fix:**

1. Supply exactly one credential: `api_key`, `bearer_token`, or `token_provider`
2. Use `SupermetricsAsyncClient` for coroutine-function token providers
3. Strip interior line breaks out of credentials read from line-wrapped files or YAML
   block scalars — surrounding whitespace is trimmed for you, interior control characters
   are rejected

The message never echoes the credential value, so it is safe to log.

---

### NetworkError

**Raised for network-level failures before/during the HTTP request.**

```python
from supermetrics import SupermetricsClient, NetworkError

try:
    client = SupermetricsClient(api_key="key", timeout=1.0)
    client.login_links.list()
except NetworkError as e:
    print(f"Network error: {e.message}")
    # Check network connectivity
    # Verify firewall/proxy settings
```

`NetworkError` has no `status_code`, because no HTTP response was received. Credentials are
redacted from the message before it is raised.

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
4. Increase the timeout for slow connections, either on the client or for a single call
   with the per-request `timeout` argument
5. Verify SSL certificates are valid

**Example: Network error handling with timeout**

```python
import time
from supermetrics import SupermetricsClient, NetworkError


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
                wait_time = 2**attempt
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("Failed to establish connection after retries")
                raise


# Usage
try:
    client = create_robust_client(api_key="your_key", timeout=30.0, max_retries=3)
    print("Client connected successfully")
except NetworkError:
    print("Unable to connect. Check network connectivity.")
```

---

### SupermetricsAPIError

**Base class for every error the API returns as an HTTP 4xx or 5xx response.**
Also importable as `APIError`.

Catch it to handle any HTTP-level failure uniformly, or catch one of its subclasses for a
specific status. Because the subclasses inherit from it, an `except SupermetricsAPIError`
clause must come **after** the specific ones.

```python
from supermetrics import SupermetricsAPIError

try:
    client.logins.get("nonexistent_id")
except SupermetricsAPIError as e:
    print(f"API error ({e.status_code}): {e.error_message}")
    print(f"Upstream code: {e.error_code}")
    print(f"Request ID: {e.request_id}")  # for support tickets
    print(f"Span ID: {e.span_id}")  # for trace correlation
```

**Attributes:**

- `message` (str): Human-readable error description
- `error_message` (str): Alias of `message`, matching the API's own payload naming
- `status_code` (int | None): HTTP status code of the response
- `endpoint` (str | None): API endpoint that was called
- `response_body` (str | None): Raw response body
- `headers` (`httpx.Headers` | None): Response headers, when available
- `error_code` (str | None): Machine-readable upstream error code, when the API supplies
  one — for example `"ACCESS_TOKEN_INVALID"`
- `details` (dict | None): Structured error details from the response payload
- `raw_response` (`httpx.Response` | None): The underlying response. Its
  `.request.headers` still contains the `Authorization` header, so do not dump it
  wholesale into logs.

**Properties:**

- `retry_after` (int | None): `Retry-After` in seconds, or `None` when the header is absent
  or holds an HTTP-date rather than a delay
- `request_id` (str | None): `X-Request-Id` from the response headers
- `span_id` (str | None): `X-Span-Id` from the response headers

**How to fix:**

- **400 / 422**: Correct the request parameters — see `SupermetricsValidationError`
- **401**: Refresh or replace the credential — see `SupermetricsAuthError`
- **403**: Check the token's scopes and the account's team access
- **404**: Verify the resource ID is correct and the resource exists
- **429**: Back off for `retry_after` seconds
- **5xx**: Retry the request after a delay

---

### SupermetricsAuthError

**Raised when API authentication fails (HTTP 401).**
Also importable as `AuthenticationError`.

```python
from supermetrics import SupermetricsClient, SupermetricsAuthError

try:
    client = SupermetricsClient(api_key="invalid_key")
    client.login_links.list()
except SupermetricsAuthError as e:
    print(f"Authentication failed: {e.message}")
    print(f"Upstream code: {e.error_code}")
    # Log error and prompt user to check the credential
```

**Common causes:**

- Invalid, expired, or revoked API key or bearer token
- An OAuth access token that needs refreshing
- Insufficient credentials for the endpoint being called
- Attempting to override the credential through `custom_headers={"Authorization": ...}`,
  which the SDK ignores with a `UserWarning`. The credential always comes from `api_key`,
  `bearer_token`, or `token_provider`; use a method's per-request `headers` argument to
  send a different credential for a single call.

**How to fix:**

1. Verify your credential is correct and has not expired or been revoked
2. Check that the credential has the necessary permissions
3. If the token is short-lived, refresh it — the upstream OAuth code in `error_code` tells
   you whether that is worth doing

**Example: Graceful authentication handling**

```python
import os
from supermetrics import SupermetricsClient, SupermetricsAuthError


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
    except SupermetricsAuthError:
        raise ValueError("Invalid API key. Please check your credentials.")


try:
    client = get_authenticated_client()
except ValueError as e:
    print(f"Setup error: {e}")
    exit(1)
```

A 401 carries the upstream OAuth code in `error_code`, which lets a caller tell "refresh
and retry" apart from "this credential will never work". See
[Pattern 5](#pattern-5-refresh-an-expired-token).

---

### SupermetricsForbiddenError

**Raised when the caller is authenticated but not permitted (HTTP 403).**

```python
from supermetrics import SupermetricsForbiddenError

try:
    client.accounts.list(ds_id="GAWA")
except SupermetricsForbiddenError as e:
    print(f"Forbidden: {e.message}")
    print(f"Upstream code: {e.error_code}")
```

**Common causes:**

- The token lacks the scope the endpoint requires
- The account has no access to the requested team or resource

**How to fix:**

1. Check the scopes granted to the token
2. Verify the account has access to the team and data source in question

Unlike a 401, retrying with a fresh token will not help unless the new token carries
different scopes.

---

### SupermetricsNotFoundError

**Raised when the requested resource does not exist (HTTP 404).**

```python
from supermetrics import SupermetricsNotFoundError

try:
    login = client.logins.get(login_id="nonexistent_id")
except SupermetricsNotFoundError:
    print("Login not found. Verify the login ID is correct.")
```

**Common causes:**

- A mistyped or stale resource ID
- A resource that has already been deleted or closed
- A resource that belongs to a different team

**How to fix:**

1. Verify the resource ID is correct
2. Treat 404 as "already gone" for idempotent cleanup operations

---

### SupermetricsValidationError

**Raised when request validation fails (HTTP 400, 422).**
Also importable as `ValidationError`.

```python
from supermetrics import SupermetricsValidationError

try:
    # Missing required parameter
    client.accounts.list(ds_id="")
except SupermetricsValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Response details: {e.response_body}")
    print(f"Structured details: {e.details}")
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
from supermetrics import SupermetricsClient, SupermetricsValidationError


def execute_query_with_validation(
    client, ds_id: str, account_ids: list[str], fields: list[str], start_date: str, end_date: str
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
            ds_id=ds_id, ds_accounts=account_ids, fields=fields, start_date=start_date, end_date=end_date
        )
    except SupermetricsValidationError as e:
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
        end_date="2024-01-31",
    )
except SupermetricsValidationError as e:
    print(f"API validation error: {e.message}")
except ValueError as e:
    print(f"Input error: {e}")
```

> `SupermetricsValidationError` is **not** a `ValueError`, so the two clauses above are
> independent and neither can shadow the other. `SupermetricsClientError` *is* a
> `ValueError`, though — a bare `except ValueError` also catches a misconfigured client and
> reports it as an input error, so catch `SupermetricsClientError` explicitly when that
> distinction matters.

---

### SupermetricsRateLimitError

**Raised when the API rate limit is exceeded (HTTP 429).**

```python
import time
from supermetrics import SupermetricsRateLimitError

try:
    logins = client.logins.list()
except SupermetricsRateLimitError as e:
    # The server tells you how long to wait; fall back to a fixed delay.
    time.sleep(e.retry_after or 30)
    logins = client.logins.list()
```

**How to fix:**

1. Sleep for `retry_after` seconds before retrying
2. Fall back to exponential backoff when `retry_after` is `None`
3. Reduce request concurrency, or batch work into fewer, larger queries

See [Pattern 6](#pattern-6-back-off-with-retry-after) for a complete retry loop.

---

### SupermetricsServerError

**Raised when the API reports a server-side failure (HTTP 5xx).**

```python
from supermetrics import SupermetricsServerError

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31",
    )
except SupermetricsServerError as e:
    print(f"Server error ({e.status_code}): {e.message}")
    print(f"Request ID: {e.request_id}")  # quote this in a support ticket
```

**Common causes:**

- **500 Internal Server Error**: Server-side error
- **502 Bad Gateway**: An upstream gateway failure
- **503 Service Unavailable**: Service temporarily unavailable
- **504 Gateway Timeout**: Request timeout on the server

**How to fix:**

1. Retry after a delay, with exponential backoff
2. If the failure persists, quote `request_id` and `span_id` when contacting support

---

## Error Handling Patterns

### Pattern 1: Granular Exception Handling

Handle each exception type differently. **Order the clauses from most specific to least
specific** — every HTTP error below descends from `SupermetricsAPIError`, so a general
clause placed first would swallow all of them:

```python
from supermetrics import (
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsClient,
    SupermetricsClientError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsValidationError,
)

try:
    client = SupermetricsClient(api_key="your_key")
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

except SupermetricsClientError as e:
    # Local configuration problem - the request was never sent
    print(f"Configuration error: {e.message}")
    # Action: Fix the client setup

except SupermetricsAuthError as e:
    # Authentication issues - credential is invalid or expired
    print(f"Auth error ({e.error_code}): {e.message}")
    # Action: Refresh or replace the credential

except SupermetricsValidationError as e:
    # Validation issues - likely code bug
    print(f"Validation error: {e.message}")
    # Action: Fix parameter values

except SupermetricsNotFoundError as e:
    # Resource does not exist
    print(f"Not found: {e.message}")
    # Action: Check the IDs

except SupermetricsRateLimitError as e:
    # Throttled - the server says how long to wait
    print(f"Rate limited, retry after {e.retry_after}s")
    # Action: Back off and retry

except SupermetricsAPIError as e:
    # Anything else at the HTTP layer (403, 5xx, ...)
    print(f"API error ({e.status_code}): {e.message}")

except NetworkError as e:
    # Network issues - likely transient
    print(f"Network error: {e.message}")
    # Action: Retry request
```

`NetworkError` is not a `SupermetricsAPIError`, so its position relative to the HTTP
clauses does not matter.

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
        end_date="2024-01-31",
    )

except SupermetricsError as e:
    # Handle all SDK errors
    print(f"SDK Error: {e.message}")
    print(f"Status Code: {e.status_code}")

    # Log error details
    import logging

    logging.error(
        f"SDK error: {e.message}",
        extra={"status_code": e.status_code, "endpoint": e.endpoint, "response_body": e.response_body},
    )
```

`except SupermetricsError` is unaffected by the hierarchy change: it catches everything,
exactly as it always did.

### Pattern 3: Contextual Error Handling

Different error handling for different operations:

```python
from supermetrics import SupermetricsAPIError, SupermetricsClient, SupermetricsNotFoundError

client = SupermetricsClient(api_key="your_key")
login_id = "login_123"
account_ids = ["123456789", "987654321"]
results = []

# Critical operation - fail fast
try:
    login = client.logins.get(login_id=login_id)
except SupermetricsNotFoundError:
    raise ValueError(f"Login not found: {login_id}")

# Optional operation - continue on error
try:
    client.login_links.close(link_id="link_123")
except SupermetricsNotFoundError:
    print("Link already closed or doesn't exist")
except SupermetricsAPIError as e:
    print(f"Warning: Failed to close link: {e.message}")

# Batch operation - collect errors
errors = []
for account_id in account_ids:
    try:
        result = client.queries.execute(
            ds_id="GAWA",
            ds_accounts=[account_id],
            fields=["Date", "Sessions"],
            start_date="2024-01-01",
            end_date="2024-01-31",
        )
        results.append(result)
    except SupermetricsAPIError as e:
        errors.append({"account_id": account_id, "error": e.message})

if errors:
    print(f"Errors occurred for {len(errors)} accounts")
    for error in errors:
        print(f"  {error['account_id']}: {error['error']}")
```

### Pattern 4: Async Error Handling

Error handling in async code. The exception hierarchy and every attribute are identical on
`SupermetricsAsyncClient`:

```python
import asyncio
from supermetrics import SupermetricsAPIError, SupermetricsAsyncClient


async def fetch_with_error_handling(client, account_id):
    """Fetch data with error handling."""
    try:
        result = await client.queries.execute(
            ds_id="GAWA",
            ds_accounts=[account_id],
            fields=["Date", "Sessions"],
            start_date="2024-01-01",
            end_date="2024-01-31",
        )
        return {"account_id": account_id, "result": result, "error": None}

    except SupermetricsAPIError as e:
        return {"account_id": account_id, "result": None, "error": e.message}


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        # Fetch data for multiple accounts
        tasks = [fetch_with_error_handling(client, account_id) for account_id in ["123", "456", "789"]]

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

### Pattern 5: Refresh an Expired Token

A 401 carries the upstream OAuth code in `error_code`, which distinguishes "this token has
expired, get a new one" from "this credential will never work". Retry with a fresh token
through the per-request `auth_token` override, so the client's connection pool is reused:

```python
from supermetrics import SupermetricsAuthError

#: Upstream codes that mean the credential is stale rather than wrong.
REFRESHABLE = {"ACCESS_TOKEN_INVALID", "ACCESS_TOKEN_EXPIRED"}


def list_logins(client, credentials):
    """List logins, refreshing the access token once if it has expired."""
    try:
        return client.logins.list()
    except SupermetricsAuthError as e:
        if e.error_code not in REFRESHABLE:
            raise  # revoked, wrong audience, missing scope - refreshing will not help
        credentials.refresh()
        return client.logins.list(auth_token=credentials.access_token)
```

For tokens that expire routinely, hand the client a `token_provider` instead and let it
re-evaluate the credential on every request. See
[Authentication & Transport](authentication-and-transport.md#dynamic-token-provider).

### Pattern 6: Back Off with Retry-After

`SupermetricsRateLimitError.retry_after` reports the server's own `Retry-After` hint in
seconds, and is `None` when the header is absent or holds an HTTP-date. Prefer it over a
guessed delay, and fall back to exponential backoff:

```python
import time
from supermetrics import SupermetricsRateLimitError, SupermetricsServerError


def execute_with_backoff(client, max_attempts=5, **query_params):
    """Execute a query, honouring the server's own Retry-After hint."""
    for attempt in range(max_attempts):
        final_attempt = attempt == max_attempts - 1
        try:
            return client.queries.execute(**query_params)

        except SupermetricsRateLimitError as e:
            if final_attempt:
                raise
            delay = e.retry_after if e.retry_after is not None else 2**attempt
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)

        except SupermetricsServerError as e:
            if final_attempt:
                raise
            print(f"Server error ({e.status_code}). Retrying in {2**attempt}s...")
            time.sleep(2**attempt)


result = execute_with_backoff(
    client,
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

The same metadata is reachable on calls that *succeed*: `client.with_raw_response` mirrors
every method and returns an `ApiResponse`, which exposes `retry_after`, `request_id`, and
`span_id` alongside the parsed `data` — see
[Reading response metadata](authentication-and-transport.md#reading-response-metadata).

---

## Common Error Scenarios

### Scenario 1: Invalid API Key

```python
from supermetrics import SupermetricsAuthError, SupermetricsClient

try:
    client = SupermetricsClient(api_key="invalid_key")
    client.login_links.list()
except SupermetricsAuthError as e:
    print(f"Authentication failed: {e.message}")
    print("Please check your API key in the environment variables")
```

### Scenario 2: Resource Not Found

```python
from supermetrics import SupermetricsClient, SupermetricsNotFoundError

client = SupermetricsClient(api_key="your_key")

try:
    login = client.logins.get(login_id="nonexistent_id")
except SupermetricsNotFoundError:
    print("Login not found. Verify the login ID is correct.")
```

### Scenario 3: Rate Limiting

```python
import time
from supermetrics import SupermetricsClient, SupermetricsRateLimitError

client = SupermetricsClient(api_key="your_key")


def execute_with_backoff(client, **query_params):
    """Execute query, waiting as long as the server asks."""
    max_retries = 5

    for attempt in range(max_retries):
        try:
            return client.queries.execute(**query_params)

        except SupermetricsRateLimitError as e:
            if attempt == max_retries - 1:
                raise
            # Retry-After when the server sends it, otherwise 1, 2, 4, 8 seconds
            delay = e.retry_after if e.retry_after is not None else 2**attempt
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)


result = execute_with_backoff(
    client,
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

### Scenario 4: Network Timeout

```python
from supermetrics import NetworkError, SupermetricsClient

# Increase timeout for slow connections
client = SupermetricsClient(api_key="your_key", timeout=60.0)

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-12-31",  # Large date range
        timeout=300.0,  # override just for this call
    )
except NetworkError as e:
    print(f"Request timed out: {e.message}")
    print("Try reducing the date range or increasing the timeout")
```

### Scenario 5: Malformed Query Parameters

```python
from supermetrics import SupermetricsClient, SupermetricsValidationError

client = SupermetricsClient(api_key="your_key")

try:
    result = client.queries.execute(
        ds_id="GAWA",
        ds_accounts=[],  # Empty list - invalid
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31",
    )
except SupermetricsValidationError as e:
    print(f"Validation error: {e.message}")
    print("At least one account ID is required")
```

### Scenario 6: Misconfigured Client

```python
from supermetrics import SupermetricsClient, SupermetricsClientError

try:
    # Exactly one credential is required
    client = SupermetricsClient(api_key="your_key", bearer_token="otok_abc123")
except SupermetricsClientError as e:
    print(f"Configuration error: {e.message}")
    # "Multiple credentials supplied (api_key, bearer_token). Provide exactly one of:
    #  api_key, bearer_token, or token_provider."
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
        },
    )
```

For HTTP errors specifically, `error_code`, `request_id`, and `span_id` are the fields
support and tracing tools actually need:

```python
from supermetrics import SupermetricsAPIError

try:
    result = client.logins.list()
except SupermetricsAPIError as e:
    logger.error(
        "Supermetrics API error",
        extra={
            "status_code": e.status_code,
            "endpoint": e.endpoint,
            "error_code": e.error_code,
            "request_id": e.request_id,
            "span_id": e.span_id,
        },
    )
```

Log those fields rather than `raw_response`: the underlying request headers still contain
the `Authorization` header.

### 3. Implement Retry Logic

Retry transient errors, and let the server set the pace when it offers one:

```python
import functools
import time
from supermetrics import SupermetricsRateLimitError, SupermetricsServerError


def retry_on_transient_error(func=None, *, max_retries=3):
    """Decorator to retry on rate limits and server errors."""

    def decorate(inner):
        @functools.wraps(inner)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                final_attempt = attempt == max_retries - 1
                try:
                    return inner(*args, **kwargs)
                except SupermetricsRateLimitError as e:
                    if final_attempt:
                        raise
                    time.sleep(e.retry_after if e.retry_after is not None else 2**attempt)
                except SupermetricsServerError:
                    if final_attempt:
                        raise
                    time.sleep(2**attempt)

        return wrapper

    return decorate(func) if func is not None else decorate


@retry_on_transient_error
def fetch_data(client):
    return client.queries.execute(
        ds_id="GAWA",
        ds_accounts=["123456789"],
        fields=["Date", "Sessions"],
        start_date="2024-01-01",
        end_date="2024-01-31",
    )
```

Do not retry `SupermetricsForbiddenError`, `SupermetricsNotFoundError`,
`SupermetricsValidationError`, or `SupermetricsClientError` — the same request will fail
the same way.

### 4. Provide User-Friendly Error Messages

Convert technical errors to user-friendly messages. Specific clauses first:

```python
from supermetrics import (
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsValidationError,
)

try:
    result = client.queries.execute(...)
except SupermetricsAuthError:
    print("Your credential is invalid or expired. Please check your configuration.")
except SupermetricsValidationError as e:
    print(f"Invalid input: {e.message}")
    print("Please verify your query parameters.")
except SupermetricsRateLimitError as e:
    wait = e.retry_after or "a few"
    print(f"Too many requests. Please wait {wait} seconds and try again.")
except SupermetricsNotFoundError:
    print("The requested resource was not found.")
except SupermetricsAPIError as e:
    print(f"An error occurred: {e.message}")
```

### 5. Use Specific Exceptions When Possible

Catch specific exceptions for better control, and keep the general ones last:

```python
# Good - specific handling, general clause last
try:
    result = client.queries.execute(...)
except SupermetricsValidationError:
    fix_parameters()
except SupermetricsRateLimitError as e:
    retry_later(after=e.retry_after)
except SupermetricsAPIError as e:
    report(e)

# Broken - the general clause now matches everything below it
try:
    result = client.queries.execute(...)
except SupermetricsAPIError as e:
    report(e)
except SupermetricsValidationError:  # never reached
    fix_parameters()

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

Set up monitoring for production errors. Order the `isinstance` checks the same way you
would order `except` clauses — most specific first:

```python
import logging
from supermetrics import SupermetricsAuthError, SupermetricsError, SupermetricsServerError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    result = client.queries.execute(...)
except SupermetricsError as e:
    # Log error
    logger.error(f"Query failed: {e.message}", extra={"status_code": e.status_code, "endpoint": e.endpoint})

    # Send alert for critical errors
    if isinstance(e, SupermetricsAuthError):
        send_alert("Critical: API authentication failed")
    elif isinstance(e, SupermetricsServerError):
        send_alert(f"Server error: {e.message}")
```

Checking `isinstance(e, SupermetricsServerError)` is both clearer and safer than comparing
`e.status_code >= 500`, which raises a `TypeError` when the error is a `NetworkError` or a
`SupermetricsClientError` and `status_code` is `None`.

---

## Summary

- **Order except clauses from specific to general** — the HTTP errors now descend from
  `SupermetricsAPIError`, so a general clause placed first swallows the specific ones
- **Use specific exceptions** (`SupermetricsAuthError`, `SupermetricsNotFoundError`,
  `SupermetricsRateLimitError`, ...) for granular control
- **Legacy names still work**: `APIError`, `AuthenticationError`, and `ValidationError` are
  aliases of `SupermetricsAPIError`, `SupermetricsAuthError`, and
  `SupermetricsValidationError`
- **Implement retry logic** for transient errors, using `retry_after` when the server sends it
- **Log error details** including `status_code`, `endpoint`, `error_code`, `request_id`, and
  `span_id` — but not `raw_response`, whose request headers carry the credential
- **Refresh tokens on `error_code`**, so an expired credential does not fail the operation
- **Always clean up resources** using context managers or try/finally
- **Monitor production errors** and set up alerts for critical failures

For more information, see:
- [Authentication & Transport](authentication-and-transport.md) - Credentials, per-request overrides, and response metadata
- [API Reference](api-reference.md) - Complete API documentation
- [User Guide](user-guide.md) - Usage examples and tutorials
