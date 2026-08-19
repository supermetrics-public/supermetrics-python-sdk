# API Reference

Complete reference for the supermetrics Python SDK public API.

For a narrative walkthrough of credentials, per-request overrides, response metadata, and
the error taxonomy, see [Authentication & Transport](authentication-and-transport.md).

## Client Classes

### SupermetricsClient

Synchronous client for blocking I/O operations.

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(
    api_key="your_api_key",
    bearer_token=None,
    token_provider=None,
    user_agent=None,
    custom_headers=None,
    timeout=30.0,
    base_url="https://api.supermetrics.com",
)
```

**Credentials:** Supply **exactly one** of `api_key`, `bearer_token`, or `token_provider`.
Every parameter except `api_key` is keyword-only.

**Parameters:**

- `api_key` (str, optional): Your Supermetrics API key (e.g. `"api_..."`), sent as a Bearer
  token. No longer required-positional — it defaults to `None`
- `bearer_token` (str, optional): OAuth 2.0 access token (e.g. `"otok_..."`) or any other
  bearer credential, including RFC 8693 exchanged tokens. Tokens are opaque to the SDK
- `token_provider` (TokenProvider, optional): Synchronous callable returning a bearer
  token, invoked once per request. Use this for short-lived tokens that must be refreshed
  without discarding the connection pool
- `user_agent` (str, optional): Custom User-Agent header (default:
  `supermetrics-sdk/{version} python/{py_version}`)
- `custom_headers` (dict, optional): Additional HTTP headers for all requests. These
  override the SDK defaults on conflict, with one exception: `Authorization` cannot be set
  here. Setting it emits a `UserWarning` and is ignored, because the credential always
  comes from `api_key` / `bearer_token` / `token_provider`. Use a method's `headers`
  argument to send a different credential for a single call
- `timeout` (float, optional): Default request timeout in seconds (default: 30.0).
  Individual calls override it with their own `timeout`
- `base_url` (str, optional): API base URL

**Raises:** `SupermetricsClientError` (which is also a `ValueError`) if zero or more than
one credential is supplied, if the supplied credential is empty, if `token_provider` is not
callable, or if an `async def` provider is given — use `SupermetricsAsyncClient` for those.

**Resource Properties:**

- `login_links`: Access to LoginLinksResource
- `logins`: Access to LoginsResource
- `accounts`: Access to AccountsResource
- `queries`: Access to QueriesResource
- `backfills`: Access to BackfillsResource
- `connector_builder`: Access to ConnectorBuilderResource
- `connector_builder_secrets`: Access to ConnectorBuilderSecretsResource
- `connector_builder_logs`: Access to ConnectorBuilderLogsResource
- `datasource_details`: Access to DatasourceDetailsResource

**Other Properties:**

- `with_raw_response`: The same resources, mirrored method-for-method with identical
  signatures, but returning [`ApiResponse`](#apiresponse) envelopes instead of bare parsed
  values

**Methods:**

- `close()`: Close client and release resources
- `__enter__()`: Context manager entry
- `__exit__()`: Context manager exit

**Example:**

```python
import os

# Using context manager (recommended)
with SupermetricsClient(api_key="your_key") as client:
    accounts = client.accounts.list(ds_id="GAWA")

# An OAuth bearer token instead of an API key
client = SupermetricsClient(bearer_token="otok_abc123")

# A short-lived token, re-read on every request
client = SupermetricsClient(token_provider=lambda: os.environ["SUPERMETRICS_TOKEN"])

# Manual lifecycle
client = SupermetricsClient(api_key="your_key")
try:
    accounts = client.accounts.list(ds_id="GAWA")
finally:
    client.close()
```

---

### SupermetricsAsyncClient

Asynchronous client for non-blocking I/O operations.

```python
from supermetrics import SupermetricsAsyncClient

client = SupermetricsAsyncClient(
    api_key="your_api_key",
    bearer_token=None,
    token_provider=None,
    user_agent=None,
    custom_headers=None,
    timeout=30.0,
    base_url="https://api.supermetrics.com",
)
```

**Credentials:** Supply **exactly one** of `api_key`, `bearer_token`, or `token_provider`.
Every parameter except `api_key` is keyword-only.

**Parameters:** Same as SupermetricsClient, with one difference: `token_provider` is an
`AsyncTokenProvider`, so it may be a coroutine function (`async def`) or a plain callable.
A coroutine provider is awaited on every request.

**Raises:** `SupermetricsClientError` (which is also a `ValueError`) if zero or more than
one credential is supplied, if the supplied credential is empty, or if `token_provider` is
not callable.

**Resource Properties:**

- `login_links`: Access to LoginLinksAsyncResource
- `logins`: Access to LoginsAsyncResource
- `accounts`: Access to AccountsAsyncResource
- `queries`: Access to QueriesAsyncResource
- `backfills`: Access to BackfillsAsyncResource
- `connector_builder`: Access to ConnectorBuilderAsyncResource
- `connector_builder_secrets`: Access to ConnectorBuilderSecretsAsyncResource
- `connector_builder_logs`: Access to ConnectorBuilderLogsAsyncResource
- `datasource_details`: Access to DatasourceDetailsAsyncResource

**Other Properties:**

- `with_raw_response`: The same resources, mirrored method-for-method with identical
  signatures, but resolving to [`ApiResponse`](#apiresponse) envelopes instead of bare
  parsed values

**Methods:**

- `async close()`: Close client and release resources
- `async __aenter__()`: Async context manager entry
- `async __aexit__()`: Async context manager exit

**Example:**

```python
import asyncio
import os

from supermetrics import SupermetricsAsyncClient


async def get_valid_token() -> str:
    # Fetch or refresh a short-lived token however your application does it.
    return os.environ["SUPERMETRICS_TOKEN"]


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        accounts = await client.accounts.list(ds_id="GAWA")
        print(f"Found {len(accounts)} accounts")

    # A coroutine token provider, awaited on every request
    async with SupermetricsAsyncClient(token_provider=get_valid_token) as client:
        logins = await client.logins.list()
        print(f"Found {len(logins)} logins")


asyncio.run(main())
```

---

## Per-Request Overrides

Every resource method on both clients — and every method mirrored on `with_raw_response` —
accepts the same three keyword-only overrides. They are documented once here and are not
repeated in the per-method parameter lists below.

- `auth_token` (str, optional): Bearer token to use for this call instead of the client
  credential. Rejected as `SupermetricsClientError` when empty or whitespace-only
- `headers` (dict[str, str], optional): Extra headers merged into the request with the
  highest precedence. Merging is case-insensitive, so `{"x-team-id": ...}` replaces a
  client-level `X-Team-ID`. Unlike `custom_headers`, this may set `Authorization`
- `timeout` (float | httpx.Timeout, optional): Timeout for this call only, in seconds or as
  an `httpx.Timeout`. Does not change the client default

```python
login = client.logins.get(
    "login_abc123",
    auth_token="otok_this_caller",
    headers={"X-Span-Id": "a8f3b2c9", "Idempotency-Key": "req-42"},
    timeout=120.0,
)
```

Overrides are bound to context variables for the duration of the call only, and context
variables are isolated per thread and per asyncio task. One shared, pooled client can
therefore serve concurrent callers that each bring their own credential and tracing
context. See [Authentication & Transport](authentication-and-transport.md) for the full
header precedence rules.

### request_options()

Context manager that binds the same three overrides for a block of code, so calls inside it
inherit them without passing arguments. Only arguments that are not `None` are bound.

```python
from supermetrics import request_options

with request_options(auth_token="otok_abc", headers={"X-Span-Id": "s1"}, timeout=60.0):
    client.logins.list()
    client.accounts.list(ds_id="GAWA")
```

**Parameters:** `auth_token`, `headers`, `timeout` — all keyword-only, all optional

**Raises:** `SupermetricsClientError` if `auth_token` is empty or whitespace-only

### Context Variables

The overrides are backed by three public `ContextVar` objects, which can be set directly —
typically once in web-framework middleware — so that every SDK call made while handling a
request inherits them. An explicit argument on a call still wins over the ambient value.

- `current_auth_token`: `ContextVar[str | None]`
- `current_request_headers`: `ContextVar[Mapping[str, str] | None]`
- `current_request_timeout`: `ContextVar[float | httpx.Timeout | None]`

```python
from supermetrics import current_auth_token

token = current_auth_token.set("otok_caller")
try:
    logins = client.logins.list()
finally:
    current_auth_token.reset(token)
```

---

## Response Envelope

### ApiResponse

`ApiResponse[T]` pairs the parsed result with the transport metadata of the HTTP response.
It is what every method under `client.with_raw_response` returns; the mirrored methods keep
the exact signature of their plain counterparts.

```python
response = client.with_raw_response.logins.get("login_abc123")
```

The async client works the same way:

```python
response = await async_client.with_raw_response.logins.get("login_abc123")
```

**Attributes:**

- `data` (T): The parsed value the plain resource method would have returned
- `status_code` (int): HTTP status code
- `headers` (httpx.Headers): Response headers (case-insensitive)
- `raw_body` (bytes): Raw response body
- `request_url` (str | None): Absolute URL of the request that produced this response

**Properties:**

- `json_body` (dict | list | None): The body decoded as JSON, or `None` if it is absent or
  not JSON
- `span_id` (str | None): `X-Span-Id`, for linking traces
- `request_id` (str | None): `X-Request-Id`, for support tickets and auditing
- `retry_after` (int | None): `Retry-After` in seconds, or `None` when the header is absent
  or holds an HTTP-date rather than a delay

**Raises:** `SupermetricsClientError` if the wrapped call completed without issuing any HTTP
request, so there is no transport metadata to report.

**Notes:**

- Every resource method issues exactly one HTTP request, and the envelope describes that
  request. If a method ever issues several, the envelope describes the **last** response
- `logins.get_by_username` is served by the *list* endpoint and filters in the client, so
  `data` is the matched `DataSourceLogin` while `request_url`, `raw_body` and `json_body`
  describe the list response
- `queries.execute` does not poll. A pending query is polled by calling
  `queries.get_results()` yourself, and each of those calls has its own envelope

**Example:**

```python
response = client.with_raw_response.accounts.list(ds_id="GAWA")

print(f"Status: {response.status_code}")
print(f"Request ID: {response.request_id}")
print(f"Accounts: {len(response.data)}")
```

---

## Resources

Each resource is reachable as a property on both clients; the async client exposes the same
method names on its `*AsyncResource` classes, which must be awaited. Every method also
accepts the keyword-only `auth_token`, `headers`, and `timeout` overrides described in
[Per-Request Overrides](#per-request-overrides), and is mirrored on
`client.with_raw_response`.

The Connector Builder resources (`connector_builder`, `connector_builder_secrets`,
`connector_builder_logs`) follow the same conventions; their individual methods are not yet
covered in this reference.

### LoginLinksResource

Manage data source authentication links.

#### create()

Create a login link for data source authentication.

```python
link = client.login_links.create(ds_id="GAWA", description="My Analytics Connection", expiry_time=None, **kwargs)
```

**Parameters:**

- `ds_id` (str, required): Data source ID (e.g., "GAWA", "google_ads", "facebook_ads")
- `description` (str, optional): Internal description for the link
- `expiry_time` (datetime, optional): Link expiry time (default: 24 hours from creation)
- `**kwargs`: Additional parameters:
  - `require_username` (str): Required username for authentication
  - `redirect_url` (str): Custom redirect URL after authentication

**Returns:** `LoginLink` object

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
link = client.login_links.create(ds_id="GAWA", description="Analytics Connection for Q1 Report")
print(f"Authentication URL: {link.login_url}")
print(f"Link ID: {link.link_id}")
```

#### get()

Retrieve a login link by ID.

```python
link = client.login_links.get(link_id="abc123")
```

**Parameters:**

- `link_id` (str, required): The login link ID

**Returns:** `LoginLink` object with current state

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
link = client.login_links.get(link_id="abc123")
if link.login_id:
    print(f"User authenticated successfully! Login ID: {link.login_id}")
else:
    print(f"Link status: {link.status_code}")
```

#### list()

List all login links for the authenticated user.

```python
links = client.login_links.list()
```

**Returns:** List of `LoginLink` objects

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
links = client.login_links.list()
for link in links:
    print(f"{link.ds_name}: {link.status_code}")
```

#### close()

Close/expire a login link.

```python
client.login_links.close(link_id="abc123")
```

**Parameters:**

- `link_id` (str, required): The login link ID to close

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
client.login_links.close(link_id="abc123")
print("Link closed successfully")
```

---

### LoginsResource

Retrieve login information and credentials.

#### get()

Retrieve a login by login ID.

```python
login = client.logins.get(login_id="login_abc123")
```

**Parameters:**

- `login_id` (str, required): The Supermetrics login ID

**Returns:** `DataSourceLogin` object

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
login = client.logins.get(login_id="login_abc123")
print(f"Username: {login.username}")
print(f"Display Name: {login.display_name}")
print(f"Data Source: {login.ds_info.ds_name}")
```

#### list()

List all logins for the authenticated user.

```python
logins = client.logins.list()
```

**Returns:** List of `DataSourceLogin` objects

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
logins = client.logins.list()
for login in logins:
    print(f"{login.ds_info.ds_name}: {login.username}")
```

#### get_by_username()

Retrieve a login by username (convenience method).

```python
login = client.logins.get_by_username(login_username="user@example.com")
```

**Parameters:**

- `login_username` (str, required): Username to search for (case-sensitive)

**Returns:** `DataSourceLogin` object

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`, `ValueError` (if not found)

**Example:**

```python
try:
    login = client.logins.get_by_username("analytics@company.com")
    print(f"Found login: {login.login_id}")
except ValueError:
    print("Login not found")
```

---

### AccountsResource

Retrieve data source accounts available for querying.

#### list()

List all accounts for a data source.

```python
accounts = client.accounts.list(ds_id="GAWA", login_usernames=None, cache_minutes=None)
```

**Parameters:**

- `ds_id` (str, required): Data source ID (e.g., "GAWA", "google_ads", "facebook_ads")
- `login_usernames` (str | list[str], optional): Username(s) to filter accounts
- `cache_minutes` (int, optional): Maximum age of cached data in minutes

**Returns:** Flattened list of account objects with `account_id`, `account_name`, `group_name`

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
# List all GAWA accounts
accounts = client.accounts.list(ds_id="GAWA")

# Filter by specific username
accounts = client.accounts.list(ds_id="GAWA", login_usernames="analytics@company.com")

# Filter by multiple usernames
accounts = client.accounts.list(ds_id="google_ads", login_usernames=["user1@company.com", "user2@company.com"])

# Print account details
for account in accounts:
    print(f"{account.account_name} ({account.account_id})")
```

---

### QueriesResource

Execute data queries to retrieve marketing data.

#### execute()

Execute a data query.

```python
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-07",
    **kwargs,
)
```

**Parameters:**

- `ds_id` (str, required): Data source ID
- `ds_accounts` (list[str], required): List of account IDs to query
- `fields` (list[str], required): List of field IDs to retrieve (data source specific)
- `start_date` (str, required): Start date (ISO 8601 "YYYY-MM-DD" or relative like "yesterday")
- `end_date` (str, required): End date (ISO 8601 or relative like "today")
- `**kwargs`: Additional parameters:
  - `schedule_id` (str): Custom identifier for query
  - `ds_segments` (list[str]): List of segment IDs
  - `filter_` (str): Filter expression
  - `max_rows` (int): Maximum rows to return
  - `cache_minutes` (int): Maximum cache age in minutes
  - `sync_timeout` (int): Seconds to wait for completion

**Returns:** `DataResponse` object or `None`

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users", "Pageviews"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    max_rows=10000,
    filter_="Sessions > 100",
)

if result and result.data:
    print(f"Retrieved {len(result.data)} rows")
    for row in result.data:
        print(row)
```

#### get_results()

Retrieve results for a previously executed async query.

```python
result = client.queries.get_results(query_id="query_abc123")
```

**Parameters:**

- `query_id` (str, required): Request ID from query execution response (`response.meta.request_id`)

**Returns:** `DataResponse` object or `None`

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
# Execute query
result = client.queries.execute(
    ds_id="GAWA", ds_accounts=["123456789"], fields=["Date", "Sessions"], start_date="2024-01-01", end_date="2024-12-31"
)

# Check if async processing
if result and result.meta and result.meta.status_code == "pending":
    print(f"Query is processing... Request ID: {result.meta.request_id}")

    # Poll for results
    import time

    time.sleep(5)
    result = client.queries.get_results(query_id=result.meta.request_id)

    if result and result.meta.status_code == "success":
        print(f"Query completed! Rows: {len(result.data)}")
```

---

### BackfillsResource

Schedule and manage historical data backfills for Data Warehouse transfers.

> **Base URL:** Backfill endpoints are served by the Data Warehouse API at
> `https://dts-api.supermetrics.com/v1`, not by the core API host. Since 0.5.0 the SDK
> routes them there for you, so an ordinary client works:
>
> ```python
> client = SupermetricsClient(api_key="your_api_key")
> client.backfills.list_incomplete(team_id=12345)   # goes to dts-api automatically
> ```
>
> Routing is only inferred when `base_url` is left at its production default. If you set
> `base_url` yourself, it is taken literally and every request goes there — including the
> pre-0.5.0 workaround of `base_url="https://dts-api.supermetrics.com/v1"`, which still
> works unchanged. To point Data Warehouse traffic somewhere specific while keeping the
> core API elsewhere, pass `dts_base_url`.

**Required API key scopes:**
- `dwh_transfers_write` — for creating and cancelling backfills
- `dwh_transfers_read` — for retrieving backfill information

**Required user permissions:**
- `dwh.transfer.edit` — for creating and cancelling backfills
- `dwh.transfer.view` — for retrieving backfill information

#### create()

Schedule a new backfill for a transfer.

```python
backfill = client.backfills.create(
    team_id=12345, transfer_id=456789, range_start=date(2024, 1, 1), range_end=date(2024, 1, 31)
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer
- `range_start` (date, required): Start date of the backfill range (inclusive)
- `range_end` (date, required): End date of the backfill range (inclusive)

**Returns:** `Backfill` object with status `"CREATED"`

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Notes:**
- The date range cannot overlap with an existing active backfill
- Backfills are processed asynchronously
- The transfer must exist and belong to your team

**Example:**

```python
from datetime import date
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    backfill = client.backfills.create(
        team_id=12345, transfer_id=456789, range_start=date(2024, 1, 1), range_end=date(2024, 1, 31)
    )
    print(f"Backfill ID: {backfill.transfer_backfill_id}")
    print(f"Status: {backfill.status}")  # "CREATED"
    print(f"Total runs: {backfill.transfer_runs_total}")
```

#### get()

Retrieve a backfill by its ID.

```python
backfill = client.backfills.get(team_id=12345, backfill_id=67890)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `backfill_id` (int, required): Unique identifier of the backfill

**Returns:** `Backfill` object with current status and progress

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404 if not found), `NetworkError`

**Example:**

```python
backfill = client.backfills.get(team_id=12345, backfill_id=67890)
print(f"Status: {backfill.status}")
print(f"Progress: {backfill.transfer_runs_completed}/{backfill.transfer_runs_total}")

if backfill.error_report:
    for err in backfill.error_report:
        print(f"Error on {err.transfer_run_date}: {err.error}")
```

#### get_latest()

Retrieve the most recent backfill for a transfer.

```python
backfill = client.backfills.get_latest(team_id=12345, transfer_id=456789)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer

**Returns:** `Backfill` object — the latest backfill regardless of status

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404 if no backfill has ever been created), `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsNotFoundError

try:
    latest = client.backfills.get_latest(team_id=12345, transfer_id=456789)
    print(f"Latest backfill: {latest.transfer_backfill_id}")
    print(f"Status: {latest.status}")
    print(f"Range: {latest.range_start_date} — {latest.range_end_date}")
except SupermetricsNotFoundError:
    print("No backfill has been created for this transfer yet")
```

#### list_incomplete()

List all incomplete backfills for a team.

```python
backfills = client.backfills.list_incomplete(team_id=12345)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team

**Returns:** `list[Backfill]` — backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED`, sorted by creation time (newest first). Returns an empty list if none exist.

**Raises:** `SupermetricsAuthError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
backfills = client.backfills.list_incomplete(team_id=12345)

if not backfills:
    print("No incomplete backfills")
else:
    for backfill in backfills:
        print(
            f"[{backfill.status}] Backfill {backfill.transfer_backfill_id} "
            f"(transfer {backfill.transfer_id}): "
            f"{backfill.transfer_runs_completed}/{backfill.transfer_runs_total} runs done"
        )
```

#### cancel()

Cancel a backfill by setting its status to `"CANCELLED"`.

```python
backfill = client.backfills.cancel(team_id=12345, backfill_id=67890)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `backfill_id` (int, required): Unique identifier of the backfill to cancel

**Returns:** `Backfill` object with status `"CANCELLED"` and updated timestamps

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError` (if backfill is already in a final state), `SupermetricsNotFoundError` (404 if not found), `NetworkError`

**Notes:**
- Only backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED` can be cancelled
- Pending/queued transfer runs are cancelled immediately
- Transfer runs already in progress will complete
- The backfill record is retained with status `"CANCELLED"` — it is not deleted

**Example:**

```python
from supermetrics import SupermetricsNotFoundError, SupermetricsValidationError

try:
    cancelled = client.backfills.cancel(team_id=12345, backfill_id=67890)
    print(f"Status: {cancelled.status}")  # "CANCELLED"
    print(f"Ended at: {cancelled.end_time}")
except SupermetricsValidationError:
    print("Cannot cancel — backfill is already in a final state")
except SupermetricsNotFoundError:
    print("Backfill not found")
```

**Async usage** (all methods above are also available on `BackfillsAsyncResource`):

```python
import asyncio
from datetime import date
from supermetrics import SupermetricsAsyncClient


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        backfill = await client.backfills.create(
            team_id=12345, transfer_id=456789, range_start=date(2024, 1, 1), range_end=date(2024, 1, 31)
        )
        print(f"Created backfill: {backfill.transfer_backfill_id}")

        incomplete = await client.backfills.list_incomplete(team_id=12345)
        print(f"Incomplete backfills: {len(incomplete)}")


asyncio.run(main())
```

---

### DatasourceDetailsResource

Retrieve complete configuration details for a Supermetrics data source.

#### get()

Fetch metadata for a data source including report types, settings, and authentication requirements.

```python
details = client.datasource_details.get(
    team_id=12345,
    data_source_id="GAWA",
    sm_app_id=None,  # optional
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `data_source_id` (str, required): Data source ID (e.g., `"GAWA"`, `"AW"`, `"SA360"`)
- `sm_app_id` (str, optional): Value forwarded as the `Sm-App-Id` request header

**Returns:** `DatasourceDetails` object

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    details = client.datasource_details.get(team_id=12345, data_source_id="GAWA")

    print(f"Name:    {details.name}")
    print(f"Status:  {details.status}")
    print(f"Premium: {details.is_premium}")

    if details.report_types:
        for rt in details.report_types:
            print(f"  Report type: {rt.id} — {rt.label}")
```

**Async usage:**

```python
import asyncio
from supermetrics import SupermetricsAsyncClient


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        details = await client.datasource_details.get(team_id=12345, data_source_id="GAWA")
        print(f"Datasource: {details.name} ({details.status})")


asyncio.run(main())
```

---

### TransfersResource

Create, configure, operate, and inspect Data Warehouse transfers — the scheduled jobs that
move data from a source into a warehouse destination.

> **Base URL:** Transfer endpoints are served by the Data Warehouse API at
> `https://dts-api.supermetrics.com/v1`, not by the core API host. The SDK routes them
> there for you, exactly as it does for backfills. See the base-URL note under
> [BackfillsResource](#backfillsresource) for how `base_url` and `dts_base_url` interact —
> in particular, setting `base_url` yourself disables the automatic routing.

**Required API key scopes:** the specification documents a scope for one endpoint in this
resource only — `create_datasource_connection()` requires `dwh_transfers_write`. The others
inherit the Data Warehouse permissions of the credential.

**Request models.** `create()`, `update()`, `validate()`, and `validate_update()` take lists
of `TransferSchedule`, `TransferAccount`, `TransferSegment`, and
`TransferDataSourceSetting`. They are not re-exported from the top-level package; import
them from the generated models package:

```python
from supermetrics._generated.supermetrics_api_client.models import (
    TransferAccount,
    TransferDataSourceSetting,
    TransferSchedule,
    TransferSegment,
)
```

**Response envelope.** The API wraps some of these responses in `{"meta": ..., "data": ...}`
and returns others bare. The SDK hides the difference — every method below returns the
payload itself, unwrapped — but the envelope is still visible through
`client.with_raw_response`, which is also the only way to reach the `meta.request_id` of a
wrapped response.

- **Wrapped** (`.data` is unwrapped for you): `list()`, `create()`, `list_runs()`,
  `create_datasource_connection()`, and `transfer_runs.get()`
- **Bare** (the model *is* the body): `get()`, `update()`, `set_state()`, `validate()`,
  `validate_update()`, `list_available_sources()`, `get_available_options()`

#### list()

List the transfers belonging to a team.

```python
transfers = client.transfers.list(team_id=12345)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team

**Returns:** `list[TransferInfoResponse]` — a summary of every non-deleted transfer owned by
the team, with its state, schedule, data source, destination, and latest backfill
statistics. Empty list if the team has none.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsAPIError`, `NetworkError`

> **The list item is not a subset of the detail object.** `list()` and `get()` return
> structurally different shapes for the same transfer. A `TransferInfoResponse` from
> `list()` identifies it as `dwh_transfer_id`, carries `schedule` as a **string**
> (`"daily"`), and `accounts` as a **list of strings**. The `TransferConfigurationResponse`
> from `get()` identifies it as `transfer_id`, carries `schedule` as a **list of
> `TransferSchedule` objects**, and `accounts` as a **list of `TransferAccount` objects**.
> Code written against one cannot be reused on the other; to get the full configuration of
> a listed transfer, call `get()` with its `dwh_transfer_id`.

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    transfers = client.transfers.list(team_id=12345)

    for transfer in transfers:
        print(f"{transfer.dwh_transfer_id}: {transfer.display_name}")
        print(f"  state={transfer.state} schedule={transfer.schedule}")
        print(f"  accounts={transfer.accounts}")  # list[str] here, objects in get()
```

#### get()

Retrieve the full configuration of a transfer.

```python
configuration = client.transfers.get(team_id=12345, transfer_id=36091)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer

**Returns:** `TransferConfigurationResponse` — schedule, accounts, segments, data source
settings, destination, and license context. Note the shape difference from `list()`
described above.

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
configuration = client.transfers.get(team_id=12345, transfer_id=36091)

print(f"Name: {configuration.display_name}")
print(f"Schema: {configuration.schema_id} -> destination {configuration.destination_id}")

for entry in configuration.schedule or []:
    print(f"  {entry.run_interval} at {entry.run_hour}:00 UTC")

for account in configuration.accounts or []:
    print(f"  account {account.account_id} via login {account.login_id}")
```

#### create()

Create a new transfer. It starts running on the schedule given here.

```python
created = client.transfers.create(
    team_id=12345,
    data_source_id="AW",
    schema_id=2,
    destination_id=8,
    display_name="AW enhanced",
    schedule=[TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)],
    accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
    segments=None,
    data_source_settings=None,
    notification_recipients=None,
    transfer_type=None,
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `data_source_id` (str, required): Data source identifier, e.g. `"AW"`
- `schema_id` (int, required): Data warehouse schema identifier of the table group this
  transfer writes into
- `destination_id` (int, required): Destination identifier
- `display_name` (str, required): Human-readable name for the transfer
- `schedule` (list[TransferSchedule], required): Execution schedule
- `accounts` (list[TransferAccount], required): Data source accounts to include
- `segments` (list[TransferSegment], optional): Data segments to include
- `data_source_settings` (list[TransferDataSourceSetting], optional): Source-specific settings
- `notification_recipients` (list[str], optional): Email addresses to notify on transfer events
- `transfer_type` (int, optional): Transfer type identifier

Everything from `segments` onwards is keyword-only.

**Returns:** `TransferCreatedResponse` with `transfer_id` and `transfer_name`. The API
answers **HTTP 201** on success.

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError` (400 / 422), `SupermetricsAPIError` (including 409 on conflict), `NetworkError`

**Notes:**
- A data source connection for this source and destination pair must already exist — see
  [`create_datasource_connection()`](#create_datasource_connection)
- `validate()` checks exactly this payload without creating anything; call it first
- Use [`get_available_options()`](#get_available_options) to discover the legal
  `schema_id`, schedule, login, account, and segment values for the pair

**Example:**

```python
from supermetrics import SupermetricsClient
from supermetrics._generated.supermetrics_api_client.models import TransferAccount, TransferSchedule

with SupermetricsClient(api_key="your_key") as client:
    created = client.transfers.create(
        team_id=12345,
        data_source_id="AW",
        schema_id=2,
        destination_id=8,
        display_name="AW enhanced",
        schedule=[TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)],
        accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
        notification_recipients=["data-team@company.com"],
    )
    print(f"Created transfer {created.transfer_id}: {created.transfer_name}")
```

#### update()

Replace the configuration of an existing transfer.

```python
updated = client.transfers.update(
    team_id=12345,
    transfer_id=36091,
    data_source_id="AW",
    schema_id=2,
    destination_id=8,
    display_name="AW enhanced (hourly)",
    schedule=[TransferSchedule(run_interval="hourly", refresh_window=1)],
    accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
)
```

**Parameters:** `team_id` and `transfer_id` (both int, required), then exactly the fields
`create()` takes — `data_source_id`, `schema_id`, `destination_id`, `display_name`,
`schedule`, `accounts`, and the keyword-only `segments`, `data_source_settings`,
`notification_recipients`, `transfer_type`.

**Returns:** `TransferUpdatedResponse` with `transfer_id` and `transfer_name`

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError` (400 / 422), `SupermetricsNotFoundError` (404), `SupermetricsAPIError`, `NetworkError`

> **`update()` replaces, it does not patch.** The request schema sets
> `additionalProperties: false` and the API exposes no PATCH endpoint, so the configuration
> is swapped wholesale rather than merged. Every field the transfer should keep must be
> resent on every call — anything omitted is dropped, not retained. The safe pattern is to
> read the current configuration with `get()`, change what you need, and send all of it
> back. Bear in mind that `get()` returns a different shape than the request takes, so the
> fields have to be mapped rather than passed straight through.

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.models import TransferAccount, TransferSchedule

current = client.transfers.get(team_id=12345, transfer_id=36091)

updated = client.transfers.update(
    team_id=12345,
    transfer_id=36091,
    data_source_id=current.data_source.data_source_id,
    schema_id=current.schema_id,
    destination_id=current.destination_id,
    display_name="AW enhanced (hourly)",  # the only change
    schedule=[TransferSchedule(run_interval="hourly", refresh_window=1)],
    accounts=[TransferAccount(login_id=a.login_id, account_id=a.account_id) for a in current.accounts or []],
)
print(f"Updated {updated.transfer_id}")
```

#### delete()

Delete a transfer.

```python
client.transfers.delete(team_id=12345, transfer_id=36091)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer to delete

**Returns:** `None`. The API answers **HTTP 204 No Content** on success.

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404), `SupermetricsAPIError`, `NetworkError`

**Notes:**
- This is a soft delete: the transfer stops running and disappears from `list()`, but the
  data it already wrote to the warehouse is preserved. Its table settings are cleaned up

**Example:**

```python
from supermetrics import SupermetricsNotFoundError

try:
    client.transfers.delete(team_id=12345, transfer_id=36091)
    print("Transfer deleted")
except SupermetricsNotFoundError:
    print("Transfer not found")
```

#### set_state()

Pause or resume a transfer.

```python
result = client.transfers.set_state(team_id=12345, transfer_id=36091, state="pause")
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer
- `state` (str, required): The action to perform — `"pause"` or `"unpause"`

**Returns:** `TransferStateUpdateResponse` with `result` (bool) and `state` (str)

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError` (400), `SupermetricsNotFoundError` (404), `SupermetricsAPIError`, `NetworkError`

> **The verb you send and the state you get back are not the same vocabulary.** The request
> takes the lowercase **verbs** `"pause"` and `"unpause"` — the SDK sends
> `{"transfer_state": "pause"}` — and those are the only two accepted values. The `state`
> field in the response is an unconstrained string that reports the transfer's resulting
> **state**, and the value documented in the specification is the uppercase `"PAUSED"`.
> There is no enum on the response side and no symmetry with the request side, so do not
> feed a returned `state` back into `set_state()`, and do not compare it to the verb you
> sent. (`TransferInfoResponse.state` from `list()` is a third free-form string, whose
> documented example is the lowercase `"active"`.)

**Notes:**
- Pausing stops scheduled runs while preserving the configuration; unpausing restarts them
  from the next scheduled time
- Runs already in progress are unaffected either way

**Example:**

```python
paused = client.transfers.set_state(team_id=12345, transfer_id=36091, state="pause")
print(f"succeeded={paused.result} state={paused.state}")  # e.g. succeeded=True state=PAUSED

# ...and back again
client.transfers.set_state(team_id=12345, transfer_id=36091, state="unpause")
```

#### validate()

Validate a configuration for a new transfer without creating it.

```python
result = client.transfers.validate(
    team_id=12345,
    data_source_id="AW",
    schema_id=2,
    destination_id=8,
    display_name="AW enhanced",
    schedule=[TransferSchedule(run_interval="daily", run_hour=22)],
    accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
)
```

**Parameters:** exactly the parameters of `create()` — this is its dry run.

**Returns:** `ValidationErrorsResponse` with `is_valid` (bool) and `errors`
(`list[ValidationError]`, empty when valid)

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsAPIError`, `NetworkError`. **Not**
`SupermetricsValidationError` — see below.

> **An invalid configuration is a result, not an exception.** The API answers **HTTP 200
> with `is_valid: false`** and a list of field-level errors; the specification documents no
> 400 and no 422 for this endpoint. `validate()` therefore returns that response rather
> than raising, which is the whole point of a dry run — branch on `result.is_valid`, do not
> wrap the call in `try`/`except SupermetricsValidationError`. The exceptions listed above
> are for the call itself failing (bad credential, no access, upstream fault).
>
> A `ValidationError` carries only `field_id` and `error_code` — for example
> `field_id="display_name"`, `error_code="isEmpty"`. There is **no human-readable message**
> in the payload; any text shown to a user has to be produced from the code by the caller.

**Example:**

```python
result = client.transfers.validate(
    team_id=12345,
    data_source_id="AW",
    schema_id=2,
    destination_id=8,
    display_name="",  # invalid on purpose
    schedule=[TransferSchedule(run_interval="daily", run_hour=22)],
    accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
)

if result.is_valid:
    print("Configuration is valid")
else:
    for error in result.errors or []:
        print(f"  {error.field_id}: {error.error_code}")  # e.g. "display_name: isEmpty"
```

#### validate_update()

Validate a configuration change against an existing transfer without applying it.

```python
result = client.transfers.validate_update(
    team_id=12345,
    transfer_id=36091,
    data_source_id="AW",
    schema_id=2,
    destination_id=8,
    display_name="AW enhanced (hourly)",
    schedule=[TransferSchedule(run_interval="hourly")],
    accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
)
```

**Parameters:** exactly the parameters of [`update()`](#update) — this is its dry run.

**Returns:** `ValidationErrorsResponse`

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404 if the transfer does not exist), `SupermetricsAPIError`, `NetworkError`. As with `validate()`, an invalid
configuration is **not** an exception: it comes back as HTTP 200 with `is_valid` set to
`False`.

**Example:**

```python
result = client.transfers.validate_update(
    team_id=12345,
    transfer_id=36091,
    data_source_id="AW",
    schema_id=2,
    destination_id=8,
    display_name="AW enhanced (hourly)",
    schedule=[TransferSchedule(run_interval="hourly")],
    accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
)

if not result.is_valid:
    for error in result.errors or []:
        print(f"{error.field_id}: {error.error_code}")
else:
    client.transfers.update(...)  # same arguments, for real this time
```

#### list_available_sources()

List the data sources and destinations available to a team.

```python
available = client.transfers.list_available_sources(team_id=12345)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team

**Returns:** `AvailableSourcesResponse` with `data_sources`, `destinations`, and
`destination_types`

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsAPIError`, `NetworkError`

**Notes:**
- This is the first step in building a transfer configuration. Pick a data source and a
  destination here, then feed the pair into `get_available_options()` for the rest

**Example:**

```python
available = client.transfers.list_available_sources(team_id=12345)

for source in available.data_sources or []:
    print(f"{source.data_source_id}: {source.service_name}")

for destination in available.destinations or []:
    print(f"{destination.destination_id}: {destination.destination_name} ({destination.destination_type})")
```

#### get_available_options()

Get the configuration options for one source and destination combination.

```python
options = client.transfers.get_available_options(team_id=12345, source_id="AW", destination_id=8)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `source_id` (str, required): Data source identifier, e.g. `"AW"` — sent as a query parameter
- `destination_id` (int, required): Destination identifier — sent as a query parameter

Both `source_id` and `destination_id` are required by the API; there is no "all options"
form of this call.

**Returns:** `TransferOptionsResponse` with `data_source`, `schedule_options`, `schemas`,
`logins`, `accounts`, `segments`, and `license_`

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsAPIError`, `NetworkError`

> **This response is almost entirely untyped upstream.** Only `data_source` has described
> properties (`data_source_id`, `service_name`, `settings`). `schedule_options`, `schemas`,
> `logins`, `accounts`, `segments`, the individual data source setting items, and
> `license_` are declared in the specification as bare objects with no properties, so the
> generated models carry no fields at all — every value lands in
> `additional_properties`. Read them as dictionaries, and expect the keys to be whatever
> the API sends rather than something the SDK can type-check.

**Example:**

```python
options = client.transfers.get_available_options(team_id=12345, source_id="AW", destination_id=8)

print(f"Source: {options.data_source.data_source_id} ({options.data_source.service_name})")

# Untyped members: read through additional_properties
for schema in options.schemas or []:
    print(schema.additional_properties)

for login in options.logins or []:
    print(login.additional_properties.get("login_id"))
```

#### list_runs()

List the runs of a transfer within a date range.

```python
runs = client.transfers.list_runs(
    team_id=12345,
    transfer_id=36091,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 31),
    filter_issues_only=None,
    sort_field=None,
    sort_direction=None,
    limit=None,
    offset=None,
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer
- `start_date` (datetime.datetime, required): Start of the range, sent as an ISO 8601
  `start_date` query parameter
- `end_date` (datetime.datetime, required): End of the range, sent as an ISO 8601
  `end_date` query parameter
- `filter_issues_only` (bool, optional): Return only runs that reported an issue
- `sort_field` (str, optional): `"created_time"`, `"data_date"`, or `"ended_time"`
- `sort_direction` (str, optional): `"ASC"` or `"DESC"`
- `limit` (int, optional): Maximum number of runs to return. The API defaults to 100 and
  caps at 10000
- `offset` (int, optional): Number of runs to skip. The API defaults to 0

`start_date` and `end_date` are **required** — there is no "all runs" form of this call —
and are typed `datetime.datetime`. The SDK calls `.isoformat()` on them, so a string will
not do. Everything from `filter_issues_only` onwards is keyword-only.

**Returns:** `list[TransferRunItem]`

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404 if the transfer does not exist), `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
import datetime

runs = client.transfers.list_runs(
    team_id=12345,
    transfer_id=36091,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 31),
    filter_issues_only=True,
    sort_field="data_date",
    sort_direction="DESC",
    limit=50,
)

for run in runs:
    print(f"{run.id} [{run.status}] {run.type_} {run.data_date}: {run.message}")

# Pass a run's id to transfer_runs.get() for the per-query detail
```

#### create_datasource_connection()

Create a data source connection for a transfer.

```python
connection = client.transfers.create_datasource_connection(
    team_id=12345, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
)
```

**Required API key scope:** `dwh_transfers_write`.

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `data_source_id` (str, required): Data source identifier, e.g. `"GA"` or `"ADM"`
- `destination_type` (str, required): Destination type identifier, e.g. `"SQL_BQ"` or
  `"DWH_SNOWFLAKE"`

**Returns:** `DataSourceConnection` with `connection_id` (a `UUID`) and the optional
`login_url` / `connect_url`. The API answers **HTTP 201** on success.

**Raises:** `SupermetricsAuthError`, `SupermetricsValidationError` (400 / 422), `SupermetricsForbiddenError`, `SupermetricsAPIError`, `NetworkError`

**Notes:**
- The connection must exist before a transfer using that source and destination pair can be
  created
- Connection credentials are taken from the client's own authorization, then encrypted and
  stored by the API. The request schema has an optional `api_key` field which the SDK
  deliberately does not expose: the credential already travels in the `Authorization`
  header, and the field is documented upstream as automatically handled
- `login_url` and `connect_url` are always `null` in the current V1 implementation

**Example:**

```python
connection = client.transfers.create_datasource_connection(
    team_id=12345, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
)
print(f"Connection: {connection.connection_id}")

if connection.login_url:
    print(f"Finish authentication at {connection.login_url}")
```

**Async usage** (all twelve methods above are also available on `TransfersAsyncResource`):

```python
import asyncio
import datetime

from supermetrics import SupermetricsAsyncClient
from supermetrics._generated.supermetrics_api_client.models import TransferAccount, TransferSchedule


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        transfers = await client.transfers.list(team_id=12345)
        print(f"{len(transfers)} transfers")

        created = await client.transfers.create(
            team_id=12345,
            data_source_id="AW",
            schema_id=2,
            destination_id=8,
            display_name="AW enhanced",
            schedule=[TransferSchedule(run_interval="daily", run_hour=22)],
            accounts=[TransferAccount(login_id=2682599, account_id="8733197711")],
        )

        runs = await client.transfers.list_runs(
            team_id=12345,
            transfer_id=created.transfer_id,
            start_date=datetime.datetime(2024, 1, 1),
            end_date=datetime.datetime(2024, 1, 31),
        )
        print(f"{len(runs)} runs")


asyncio.run(main())
```

---

### TransferRunsResource

Inspect a single execution of a Data Warehouse transfer.

> **Base URL:** As with transfers and backfills, this endpoint lives on the Data Warehouse
> API and the SDK routes it there automatically — see the base-URL note under
> [BackfillsResource](#backfillsresource).
>
> Note the path spelling: run lookup is `/teams/{team_id}/transfer_runs/{transfer_run_id}`,
> with an **underscore**, while every other transfer path uses hyphens. That is what the
> API serves; it matters only if you are matching request paths in a proxy or a test.

#### get()

Retrieve a transfer run by ID.

```python
run = client.transfer_runs.get(team_id=12345, transfer_run_id=98765)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_run_id` (int, required): Unique identifier of the transfer run

The run is addressed by its own identifier within the team, so the transfer that produced
it does not have to be known. Run ids come from
[`transfers.list_runs()`](#list_runs).

**Returns:** `TransferRunDetail` — status, queued/started/ended timestamps, total duration,
row counts, and the per-query execution details

**Raises:** `SupermetricsAuthError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsForbiddenError`, `SupermetricsAPIError`, `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    run = client.transfer_runs.get(team_id=12345, transfer_run_id=98765)

    print(f"Status: {run.status}")
    print(f"Rows: {run.total_rows} in {run.total_duration}s")
    print(f"Queries: {run.query_amount} ({run.failed_query_amount} failed)")

    for query in run.query_details:
        print(f"  [{query.status}] {query.rows} rows in {query.duration}s")
        if query.error_description:
            print(f"    {query.error_description}")
```

**Async usage:**

```python
import asyncio

from supermetrics import SupermetricsAsyncClient


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        run = await client.transfer_runs.get(team_id=12345, transfer_run_id=98765)
        print(f"Run {run.id}: {run.status}")


asyncio.run(main())
```

---

### CustomFieldsResource

Define, inspect, and remove a team's custom fields — the calculated dimensions and metrics
that Supermetrics evaluates alongside a data source's native fields. Upstream calls them
*field transformations*, which is why the models are named `TeamTransformationOutput` and
the generated operations `*_transformation`.

> **Base URL:** Custom fields are served by the core API host, not by the Data Warehouse
> API, so nothing is re-hosted for them. The paths keep their `/v1` prefix:
> `/v1/teams/{team_id}/custom-fields`. A plain client reaches them with no
> `dts_base_url` involvement at all.

Each field carries a **definition**: an ordered pipeline of steps evaluated top to bottom.
A step is one of three kinds, discriminated by its `type`:

- [`FunctionStep`](#functionstep) — applies a named function to its arguments
- [`LookupStep`](#lookupstep) — maps input values to output values through a lookup table
- [`ConditionStep`](#conditionstep) — evaluates ordered cases and returns the first match

Call [`get_metadata()`](#get_metadata) to discover which functions, rules, and data types
the team may actually use before building one.

**Request models.** Unlike the transfer models, the definition-step types *are*
re-exported from the top-level package — `create()` and `update()` cannot be called
without constructing them:

```python
from supermetrics import (
    ConditionCase,
    ConditionCaseCondition,
    ConditionStep,
    CustomFieldCreateRequestDataSourceItem,
    DefinitionValue,
    FunctionArgument,
    FunctionStep,
    LookupStep,
    LookupStepMap,
)
```

> **The definition is asymmetric between request and response.** You *send* a bare list of
> steps and you *get back* an object with an `items` attribute. A read-modify-write cycle
> therefore reads `field.definition.items` and passes that list straight to `update()` —
> see the [`update()` example](#update-1). This is upstream's shape, not the SDK's.

**Response envelope.** All five reading and writing methods are wrapped in
`{"meta": ..., "data": ...}` upstream, and the SDK unwraps `.data` for you. `list()` is
double-wrapped — the page sits at `data.items` and the pagination metadata rides in `meta`
— which is why `list()` returns only the page. See the note under
[`list()`](#list-4) for how to read the pagination.

**Errors.** This domain documents 400, 401, 403, 404, 429, and 500. **There is no 422 in
it**: a rejected definition comes back as HTTP 400, which the SDK translates to
`SupermetricsValidationError` exactly as it does a 422 elsewhere. `list()` and
`get_metadata()` document no 404 at all.

#### list()

List the custom fields defined for a team.

```python
fields = client.custom_fields.list(team_id=12345)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `data_source_id` (str, optional): Only return fields belonging to this data source, e.g.
  `"GAWA"`
- `display_name` (str, optional): Only return fields with this user-facing name
- `page` (int, optional): 1-based page number to fetch
- `limit` (int, optional): Maximum number of fields to return, 1 to 100
- `include_total_count` (bool, optional): Ask the API to report the total number of
  matching fields

Everything from `data_source_id` onwards is keyword-only.

**Returns:** `list[TeamTransformationOutput]` — the custom fields on this page. Empty list
when the page has no results, including when the API omits `data` or `data.items`
entirely.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsValidationError` (400 on an invalid query), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

> **Only the parameters you pass are sent.** With no optional arguments the query string
> is empty — `limit` in particular is *not* sent, even though the generated layer has a
> default of 25. The server applies its own default instead, so the SDK never silently
> pins a page size you did not ask for.

> **`list()` returns the page, not the pagination.** The `total_count`, `limit`, `offset`,
> and next/previous links the API sends alongside the page are dropped by the typed
> method. Read them through the raw-response accessor:
>
> ```python
> response = client.with_raw_response.custom_fields.list(team_id=12345, include_total_count=True)
>
> fields = response.data  # list[TeamTransformationOutput], same as list() returns
> pagination = response.json_body["meta"]["pagination"]
>
> print(f"{len(fields)} of {pagination['total_count']} fields")
> print(f"limit={pagination['limit']} offset={pagination['offset']}")
> ```
>
> **`total_count` is only present when `include_total_count=True`.** The API omits it by
> default because counting costs time, so reading it unconditionally will `KeyError` on a
> plain call.

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    fields = client.custom_fields.list(team_id=12345, data_source_id="GAWA", limit=50)

    for field in fields:
        print(f"{field.id}: {field.display_name} ({field.field_type}, {field.data_type})")
        print(f"  last modified {field.modified_time_utc} by {field.modified_user.email}")
```

Paging through everything, using the total to know when to stop:

```python
page = 1
seen = 0

while True:
    response = client.with_raw_response.custom_fields.list(
        team_id=12345, page=page, limit=100, include_total_count=True
    )
    if not response.data:
        break

    for field in response.data:
        print(field.display_name)

    seen += len(response.data)
    if seen >= response.json_body["meta"]["pagination"]["total_count"]:
        break
    page += 1
```

#### get()

Retrieve a single custom field by ID.

```python
field = client.custom_fields.get(team_id=12345, custom_field_id=42)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `custom_field_id` (int, required): Unique identifier of the custom field

**Returns:** `TeamTransformationOutput` — the field with its definition, data type, and
last-modified metadata

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsValidationError` (400), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    field = client.custom_fields.get(team_id=12345, custom_field_id=42)

    print(f"{field.display_name} [{field.name}] -> {field.data_type}")
    print(f"Applies to {field.data_source_id}, report types {field.report_types}")

    # Note `.definition.items`, not `.definition` — the read shape wraps the list
    for step in field.definition.items:
        print(f"  {step.type_}: {type(step).__name__}")
```

#### get_metadata()

Retrieve the building blocks available for custom field definitions.

```python
metadata = client.custom_fields.get_metadata(team_id=12345)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team

**Returns:** `MetadataOutputData` — the functions the team may call, the rules available to
condition and lookup steps, the field data types that can be referenced, the output data
types a field may declare, and the team's cap on steps per definition

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsValidationError` (400), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

Call this before constructing a `definition` rather than guessing at function and rule
names — an unknown name is rejected on `create()` as a 400.

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    metadata = client.custom_fields.get_metadata(team_id=12345)

    print(f"Up to {metadata.data_transformation_steps_limit} steps per definition")

    for function in metadata.functions.items:
        args = ", ".join(argument["name"] for argument in function.arguments)
        print(f"  [{function.group_name}] {function.name}({args}) -> {function.return_types}")

    print(f"Condition rules: {[rule.name for rule in metadata.rules.condition.items]}")
    print(f"Lookup rules:    {[rule.name for rule in metadata.rules.lookup.items]}")
    print(f"Output types:    {[t.output_type for t in metadata.output_data_types.items]}")
```

Every attribute on `MetadataOutputData` is optional upstream, so guard the ones you read
if you cannot rely on the team having them.

#### create()

Create a custom field.

```python
field = client.custom_fields.create(
    team_id=12345,
    display_name="Platform (normalised)",
    field_type="dim",
    data_type="string.text.value",
    definition=[step],
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `display_name` (str, required): User-facing name shown in the UI
- `field_type` (`"dim"` | `"met"`, required): `"dim"` for a dimension, `"met"` for a
  metric. **This cannot be changed later** — `update()` does not accept it
- `data_type` (str, required): Data type of the field, e.g. `"string.text.value"`,
  `"float.number.value"`, `"int.number.value"`, or `"bool"`. The legal values come from
  `get_metadata().output_data_types.items`
- `definition` (list[FunctionStep | LookupStep | ConditionStep], required): The ordered
  pipeline, sent as a **bare list**
- `description` (str, optional): Free-text description of the field
- `data_source` (list[CustomFieldCreateRequestDataSourceItem], optional): Data sources the
  field applies to, each pairing a `data_source_id` with an optional `report_type`

`description` and `data_source` are keyword-only.

**Returns:** `TeamTransformationOutput` — the persisted field, including the `id` and
machine `name` the API assigned. The API answers **HTTP 201** on success.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsValidationError` (**400** — an invalid definition is a 400, not a 422), `SupermetricsNotFoundError`, `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

**Example** — a three-step pipeline using all three step kinds: upper-case the platform
field, map the result to a friendly name, then classify what came out.

```python
from supermetrics import (
    ConditionCase,
    ConditionCaseCondition,
    ConditionStep,
    CustomFieldCreateRequestDataSourceItem,
    DefinitionValue,
    FunctionArgument,
    FunctionStep,
    LookupStep,
    LookupStepMap,
    SupermetricsClient,
)

upper = FunctionStep(
    type_="function",
    name="upper_case",
    arguments=[FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))],
)

# LookupStepMap takes no mapping in its constructor: `additional_properties` is
# declared init=False, so build it empty and assign the entries.
mapping = LookupStepMap()
mapping["GOOGLE"] = "Google Ads"
mapping["FACEBOOK"] = "Meta Ads"

rename = LookupStep(
    type_="lookup",
    rule="equals",
    map_=mapping,
    source=DefinitionValue(type_="output_from_previous"),
    default=DefinitionValue(type_="static", value="Other"),
)

# ConditionCase's field is `return_` in Python; it serialises to "return", which is a
# Python keyword and so cannot be an attribute name.
classify = ConditionStep(
    type_="condition",
    default=DefinitionValue(type_="static", value="Unclassified"),
    cases=[
        ConditionCase(
            return_=DefinitionValue(type_="static", value="Search"),
            condition=ConditionCaseCondition(
                type_="rule",
                rule="equals",
                source=DefinitionValue(type_="output_from_previous"),
                target=DefinitionValue(type_="static", value="Google Ads"),
            ),
        )
    ],
)

with SupermetricsClient(api_key="your_key") as client:
    field = client.custom_fields.create(
        team_id=12345,
        display_name="Platform (normalised)",
        field_type="dim",
        data_type="string.text.value",
        definition=[upper, rename, classify],
        description="Upper-cases the platform, maps it to a friendly name, then classifies it",
        data_source=[CustomFieldCreateRequestDataSourceItem(data_source_id="GAWA")],
    )
    print(f"Created {field.id} ({field.name})")
```

#### update()

Replace an existing custom field.

```python
field = client.custom_fields.update(
    team_id=12345,
    custom_field_id=42,
    display_name="Platform (normalised, v2)",
    data_type="string.text.value",
    definition=[step],
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `custom_field_id` (int, required): Unique identifier of the custom field to replace
- `display_name` (str, required): User-facing name shown in the UI
- `data_type` (str, required): Data type of the field
- `definition` (list[FunctionStep | LookupStep | ConditionStep], required): The ordered
  pipeline, sent as a **bare list**
- `description` (str, optional, keyword-only): Free-text description of the field

**Returns:** `TeamTransformationOutput` — the updated field

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsValidationError` (**400** on an invalid definition), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

> **`update()` is not `create()` with an id attached.** Two differences, both upstream's:
>
> 1. **There is no `field_type` parameter.** The field kind cannot be changed after
>    creation, so the request body does not carry it at all. `data_source` is absent for
>    the same reason.
> 2. **It is a whole-object replace.** There is no PATCH endpoint, so every field listed
>    above is resent on every call and anything you omit reverts to unset — passing no
>    `description` clears the existing one.

**Example** — the read-modify-write cycle, which is where the definition asymmetry bites:

```python
from supermetrics import DefinitionValue, FunctionArgument, FunctionStep, SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    current = client.custom_fields.get(team_id=12345, custom_field_id=42)

    # Read: the response wraps the pipeline, so unwrap `.items` to get the list.
    steps = list(current.definition.items)

    # Modify: append a step.
    steps.append(
        FunctionStep(
            type_="function",
            name="trim",
            arguments=[FunctionArgument(name="value", value=DefinitionValue(type_="output_from_previous"))],
        )
    )

    # Write: send the bare list back, and resend everything you want to keep.
    updated = client.custom_fields.update(
        team_id=12345,
        custom_field_id=42,
        display_name=current.display_name,
        data_type=current.data_type,
        definition=steps,
        description=current.description,
    )
    print(f"{updated.display_name} now has {len(updated.definition.items)} steps")
```

#### delete()

Delete a custom field.

```python
client.custom_fields.delete(team_id=12345, custom_field_id=42)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `custom_field_id` (int, required): Unique identifier of the custom field to delete

**Returns:** `None`. The API answers **HTTP 204 No Content** on success, so there is no
body to return and nothing to inspect.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsValidationError` (400), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsClient
from supermetrics.exceptions import SupermetricsNotFoundError

with SupermetricsClient(api_key="your_key") as client:
    try:
        client.custom_fields.delete(team_id=12345, custom_field_id=42)
    except SupermetricsNotFoundError:
        print("Already gone")
```

Deletion is not idempotent from the caller's point of view: a second call 404s. Use
`with_raw_response` if you want to assert on the 204 itself.

```python
response = client.with_raw_response.custom_fields.delete(team_id=12345, custom_field_id=42)
assert response.status_code == 204
assert response.data is None
```

**Async usage** (all six methods above are also available on `CustomFieldsAsyncResource`):

```python
import asyncio

from supermetrics import DefinitionValue, FunctionArgument, FunctionStep, SupermetricsAsyncClient


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        metadata, fields = await asyncio.gather(
            client.custom_fields.get_metadata(team_id=12345),
            client.custom_fields.list(team_id=12345, data_source_id="GAWA"),
        )
        print(f"{len(fields)} fields, step limit {metadata.data_transformation_steps_limit}")

        created = await client.custom_fields.create(
            team_id=12345,
            display_name="Platform (upper)",
            field_type="dim",
            data_type="string.text.value",
            definition=[
                FunctionStep(
                    type_="function",
                    name="upper_case",
                    arguments=[
                        FunctionArgument(
                            name="value", value=DefinitionValue(type_="data_source_field", value="platform")
                        )
                    ],
                )
            ],
        )
        await client.custom_fields.delete(team_id=12345, custom_field_id=created.id)


asyncio.run(main())
```

---

### BlendsResource

Define, inspect, and remove a team's blends — the combined tables that draw their rows from
several data sources at once. A blend has one of two kinds, fixed at creation and named by
`blend_type`:

- `"union"` stacks rows from each source under a shared set of blend fields
- `"join"` joins the sources on shared fields, with one primary table
  (`config.query_table`) and one [`BlendJoin`](#blendjoin) per additional source

> **Base URL:** Blends are served by the core API host, not by the Data Warehouse API, so
> nothing is re-hosted for them. The paths keep their `/v1` prefix:
> `/v1/teams/{team_id}/data-blending/blends`. A plain client reaches them with no
> `dts_base_url` involvement at all.

Two things describe a blend. [`blended_data_sources`](#blendeddatasourceinput) lists the
sources it draws on, and [`config`](#blendconfig) maps each source's native fields onto the
blend's own fields — and, for a join blend, says how the sources are joined.

**Request models.** As with custom fields, the request types *are* re-exported from the
top-level package — `create()` and `update()` cannot be called without constructing them:

```python
from supermetrics import (
    BlendConfig,
    BlendConfigQueryTable,
    BlendDatasourceFieldRef,
    BlendDatasourceFieldRefMetaType0,
    BlendField,
    BlendJoin,
    BlendJoinCondition,
    BlendJoinJoinTable,
    BlendedDataSourceInput,
    BlendedDataSourceInputAccountsItem,
    BlendedDataSourceInputDataSourceSettingsItem,
    BlendedDataSourceInputReportTypeSettingsItem,
    BlendedDataSourceInputSegmentsItem,
)
```

> **`BlendedDataSourceInput` takes five required arguments, three of which are routinely
> empty.** `data_source_id`, `blend_data_source_id`, `blend_data_source_key`,
> `report_type`, and `report_type_settings` are all *required but nullable* upstream: they
> have to be present in the JSON even when there is nothing to say. On a create that means
> `blend_data_source_id=None`, and usually `report_type=None` and
> `report_type_settings=[]`. Leaving any of the five out is a `TypeError` before a request
> is ever built.

> **Requests and responses are not the same shape.** Every collection is sent as a bare
> list and comes back wrapped in an object with an `items` attribute — at every level, so a
> read goes through `blend.blended_data_sources.items`, `blend.config.fields.items`,
> `field.blend_datasource_fields.items`, and `join.conditions.items`. The response also
> drops `blend_data_source_key` everywhere, and adds `blend_field_type` and
> `blend_field_data_type`, which upstream infers from the mapped fields and the request has
> no way to set. **A blend cannot be read back and resent unchanged**; a read-modify-write
> has to rebuild the request objects from the response. This is upstream's shape, not the
> SDK's.

> **`blend_data_source_key` is a create-time alias for a source that has no id yet.** It is
> exactly eight lowercase alphanumerics (`^[a-z0-9]{8}$`), and every field and join
> reference in the same request points at it instead of at an id. On
> [`update()`](#update-2), sources that already exist are addressed by
> `blend_data_source_id` and sources being added in the same call by a fresh key, so one
> body legitimately carries both.

> **`list()` returns summaries, `get()` returns whole blends.** A
> [`BlendListItemOutput`](#blendlistitemoutput) has no `config` at all, and a reduced view
> of each data source. Call [`get()`](#get-7) for a blend's fields and joins.

**Response envelope.** The four methods that return a body are wrapped in
`{"meta": ..., "data": ...}` upstream, and the SDK unwraps `.data` for you. `list()` is
double-wrapped — the blends sit at `data.items` — but unlike custom fields there is no
pagination to lose here: **this endpoint is not paginated**, so one call returns every
matching blend and returning a bare list drops nothing. `with_raw_response` still earns its
place for the status code, the headers, and `meta.request_id`.

**Errors.** This domain documents 400, 401, 403, 429, and 500 on every operation, plus 404
on the three by-id operations — `get()`, `update()`, and `delete()`. `list()` and `create()`
document no 404 at all; one that arrives anyway is still translated to
`SupermetricsNotFoundError` through the generic path. **There is no 422 anywhere in this
domain**: a rejected blend definition comes back as HTTP 400, which the SDK turns into
`SupermetricsValidationError` exactly as it does a 422 elsewhere. Nothing in the SDK checks
that a `union` blend omits `joins` or that a `join` blend supplies `query_table` — upstream
is what rejects those, and it does so with a 400.

#### list()

List the blends defined for a team.

```python
blends = client.blends.list(team_id=12345)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `blend_type` (`"join"` | `"union"`, optional): Only return blends of this kind. Sent as
  the `type` query parameter, and omitted entirely when not given, which returns both kinds

`blend_type` is keyword-only.

**Returns:** `list[BlendListItemOutput]` — the team's blends. Empty list when the team has
none, including when the API omits `data` or `data.items` entirely.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsValidationError` (400 on an invalid query), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

> **There is no pagination here.** Upstream returns every matching blend in a single
> `data.items` array and documents no page, limit, or cursor — the response uses the plain
> envelope, whose `meta` carries only a request id. So there is nothing to page through and
> nothing for `with_raw_response` to recover, unlike
> [`custom_fields.list()`](#list-4).

> **The summaries carry no `config`.** A list item has `blend_id`, `blend_uuid`, `type_`,
> `display_name`, `description`, `modified_time_utc`, `last_modify_user_email`, and a
> four-attribute view of each data source. Fields and joins exist only on
> [`get()`](#get-7).

**Example:**

```python
from supermetrics import SupermetricsClient

with SupermetricsClient(api_key="your_key") as client:
    for summary in client.blends.list(team_id=12345, blend_type="join"):
        sources = summary.blended_data_sources.items
        print(f"{summary.blend_id} [{summary.blend_uuid}] {summary.display_name} ({summary.type_})")
        print(f"  {len(sources)} sources: {', '.join(source.data_source_id for source in sources)}")
        print(f"  modified {summary.modified_time_utc} by {summary.last_modify_user_email}")
```

#### get()

Retrieve a single blend, including its full configuration.

```python
blend = client.blends.get(team_id=12345, blend_id=569)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `blend_id` (int, required): Unique identifier of the blend

**Returns:** `BlendOutput` — the blend, with its data sources and its field and join
configuration

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsValidationError` (400), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

> **Everything nested here is wrapped.** The sources are at
> `blend.blended_data_sources.items`, the fields at `blend.config.fields.items`, a field's
> mappings at `field.blend_datasource_fields.items`, and a join's conditions at
> `join.conditions.items`.

> **On a union blend, `config.query_table` and `config.joins` are `Unset`, not `None`.**
> Test them with `isinstance(value, Unset)`. `value is None` is false for the sentinel, so
> that check passes silently and the attribute access after it raises.

**Example:**

```python
from supermetrics import SupermetricsClient
from supermetrics._generated.supermetrics_api_client.types import Unset

with SupermetricsClient(api_key="your_key") as client:
    blend = client.blends.get(team_id=12345, blend_id=569)

    print(f"{blend.display_name} [{blend.blend_uuid}] is a {blend.type_} blend")

    for source in blend.blended_data_sources.items:
        print(f"  source {source.blend_data_source_id}: {source.data_source_id} ({source.display_name})")

    for field in blend.config.fields.items:
        # blend_field_type and blend_field_data_type are response-only — upstream infers
        # them from the mapped fields, and the request has no way to set them.
        print(f"  {field.blend_field_name} ({field.blend_field_type}, {field.blend_field_data_type})")
        for ref in field.blend_datasource_fields.items:
            print(f"    <- {ref.blend_data_source_id}.{ref.datasource_field_name}")

    # A union blend has no joins at all, and the attribute is Unset rather than None.
    if not isinstance(blend.config.joins, Unset):
        for join in blend.config.joins.items:
            print(f"  {join.type_} join on {len(join.conditions.items)} condition(s)")
```

#### create()

Create a blend.

```python
blend = client.blends.create(
    team_id=12345,
    display_name="GA4 + Google Ads",
    blend_type="join",
    blended_data_sources=[ga4, ads],
    config=config,
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `display_name` (str, required): User-facing name shown in the UI
- `blend_type` (`"join"` | `"union"`, required): `"union"` to stack rows, `"join"` to join
  the sources on shared fields. Sent as `type` and returned as `.type_`. **This cannot be
  changed later** — `update()` does not accept it
- `blended_data_sources` (list[BlendedDataSourceInput], required): The data sources the
  blend draws on, sent as a **bare list**
- `config` (BlendConfig, required): Field mappings, and for a join blend the primary table
  and the joins. A union blend sets `fields` only
- `description` (str, optional): Free-text description of the blend. Left out of the request
  body entirely when not passed, rather than sent as `null`

`description` is keyword-only.

**Returns:** `BlendOutput` — the persisted blend, including the `blend_id` and `blend_uuid`
the API assigned and the `blend_data_source_id` it gave each source. The API answers
**HTTP 201** on success.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsValidationError` (**400** — a rejected blend is a 400, not a 422), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

> **Every source is new here, so every source needs a `blend_data_source_key`.** Nothing has
> an id yet. Pick eight lowercase alphanumerics per source, pass
> `blend_data_source_id=None`, and point each
> [`BlendDatasourceFieldRef`](#blenddatasourcefieldref),
> [`BlendConfigQueryTable`](#blendconfigquerytable), and
> [`BlendJoinJoinTable`](#blendjoinjointable) at that key. The API assigns real ids and
> answers in those; the keys never appear in a response.

**Example** — a join blend over two sources, joined on the date:

```python
from supermetrics import (
    BlendConfig,
    BlendConfigQueryTable,
    BlendDatasourceFieldRef,
    BlendField,
    BlendJoin,
    BlendJoinCondition,
    BlendJoinJoinTable,
    BlendedDataSourceInput,
    BlendedDataSourceInputAccountsItem,
    BlendedDataSourceInputDataSourceSettingsItem,
    SupermetricsClient,
)

# One key per new source: exactly eight lowercase alphanumerics, unique in the request.
GA4_KEY = "ga4a0001"
ADS_KEY = "gawa0001"

ga4 = BlendedDataSourceInput(
    data_source_id="GA4",
    blend_data_source_id=None,  # new source: no id yet, so it is named by the key below
    blend_data_source_key=GA4_KEY,
    report_type=None,  # required but nullable, like the two above
    report_type_settings=[],  # required but nullable
    display_name="Google Analytics 4",
    accounts=[BlendedDataSourceInputAccountsItem(account_id="1234567890", account_name="Acme Corp")],
    data_source_settings=[BlendedDataSourceInputDataSourceSettingsItem(id="currency", value="EUR")],
)

ads = BlendedDataSourceInput(
    data_source_id="GAWA",
    blend_data_source_id=None,
    blend_data_source_key=ADS_KEY,
    report_type=None,
    report_type_settings=[],
    display_name="Google Ads",
)

date = BlendField(
    blend_field_name="date",
    blend_field_display_name="Date",
    blend_datasource_fields=[
        BlendDatasourceFieldRef(
            datasource_field_name="Date",
            field_source="standard",
            blend_data_source_key=GA4_KEY,
            datasource_field_type="dim",
            datasource_field_data_type="string.time.date",
        ),
        BlendDatasourceFieldRef(
            datasource_field_name="Date",
            field_source="standard",
            blend_data_source_key=ADS_KEY,
            datasource_field_type="dim",
            datasource_field_data_type="string.time.date",
        ),
    ],
)

impressions = BlendField(
    blend_field_name="impressions",
    blend_field_display_name="Impressions",
    blend_datasource_fields=[
        BlendDatasourceFieldRef(
            datasource_field_name="Impressions",
            field_source="standard",
            blend_data_source_key=ADS_KEY,
            datasource_field_type="met",
            datasource_field_data_type="int.number.value",
        )
    ],
)

config = BlendConfig(
    # A join blend names its primary (left-hand) table and one join per other source.
    query_table=BlendConfigQueryTable(blend_data_source_key=GA4_KEY),
    joins=[
        BlendJoin(
            join_table=BlendJoinJoinTable(blend_data_source_key=ADS_KEY),
            type_="left",
            conditions=[
                BlendJoinCondition(
                    operator="=",
                    left=BlendDatasourceFieldRef(
                        datasource_field_name="Date", field_source="standard", blend_data_source_key=GA4_KEY
                    ),
                    right=BlendDatasourceFieldRef(
                        datasource_field_name="Date", field_source="standard", blend_data_source_key=ADS_KEY
                    ),
                )
            ],
        )
    ],
    fields=[date, impressions],
)

with SupermetricsClient(api_key="your_key") as client:
    blend = client.blends.create(
        team_id=12345,
        display_name="GA4 + Google Ads",
        blend_type="join",
        blended_data_sources=[ga4, ads],
        config=config,
        description="GA4 joined to Google Ads impressions on the date",
    )

    print(f"Created blend {blend.blend_id} ({blend.blend_uuid})")
    for source in blend.blended_data_sources.items:
        # The keys are gone from the response; the API answers in ids from here on.
        print(f"  {source.data_source_id} -> blend_data_source_id={source.blend_data_source_id}")
```

A union blend is the same call with less in it — no `query_table`, no `joins`, and one
`BlendField` per column of the stacked table:

```python
from supermetrics import (
    BlendConfig,
    BlendDatasourceFieldRef,
    BlendField,
    BlendedDataSourceInput,
    SupermetricsClient,
)

GA4_KEY = "ga4a0001"
ADS_KEY = "gawa0001"

sources = [
    BlendedDataSourceInput(
        data_source_id=data_source_id,
        blend_data_source_id=None,
        blend_data_source_key=key,
        report_type=None,
        report_type_settings=[],
    )
    for data_source_id, key in (("GA4", GA4_KEY), ("GAWA", ADS_KEY))
]

config = BlendConfig(
    fields=[
        BlendField(
            blend_field_name="clicks",
            blend_field_display_name="Clicks",
            blend_datasource_fields=[
                BlendDatasourceFieldRef(
                    datasource_field_name="Clicks", field_source="standard", blend_data_source_key=GA4_KEY
                ),
                BlendDatasourceFieldRef(
                    datasource_field_name="Clicks", field_source="standard", blend_data_source_key=ADS_KEY
                ),
            ],
        )
    ]
)

with SupermetricsClient(api_key="your_key") as client:
    blend = client.blends.create(
        team_id=12345,
        display_name="Clicks, everywhere",
        blend_type="union",
        blended_data_sources=sources,
        config=config,
    )
    print(blend.blend_id)
```

#### update()

Replace an existing blend.

```python
blend = client.blends.update(
    team_id=12345,
    blend_id=569,
    display_name="GA4 + Google Ads, revised",
    blended_data_sources=[ga4, ads],
    config=config,
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `blend_id` (int, required): Unique identifier of the blend to replace
- `display_name` (str, required): User-facing name shown in the UI
- `blended_data_sources` (list[BlendedDataSourceInput], required): The complete set of
  sources the blend draws on, sent as a **bare list**. A source left out of it is removed
  from the blend
- `config` (BlendConfig, required): Field mappings, and for a join blend the primary table
  and the joins
- `description` (str, optional): Free-text description of the blend

`description` is keyword-only.

**Returns:** `BlendOutput` — the updated blend. The API answers **HTTP 200** on success.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsValidationError` (**400** on a rejected definition), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

> **`update()` is not `create()` with an id attached.** Two differences, both upstream's:
>
> 1. **There is no `blend_type` parameter.** A blend's kind is fixed at creation, so the
>    request body does not carry it at all.
> 2. **It is a whole-object replace.** There is no PATCH endpoint. `display_name`,
>    `blended_data_sources` and `config` are required and resent in full on every call, so
>    a source left out of `blended_data_sources` or a field left out of `config` is dropped
>    from the blend. `description` is the only optional parameter; omit it and no
>    `description` key is sent.

> **One update body may carry both ids and keys.** A source that already exists is addressed
> by `blend_data_source_id`, with `blend_data_source_key=None`; a source being added in the
> same call has no id yet and takes a fresh eight-character key. Field and join references
> follow the same rule, one attribute or the other per reference.

**Example** — the read-modify-write cycle, which is where the request/response asymmetry
bites: the response objects are a different type from the request objects, so they have to
be rebuilt rather than handed back.

```python
from supermetrics import (
    BlendConfig,
    BlendDatasourceFieldRef,
    BlendField,
    BlendedDataSourceInput,
    SupermetricsClient,
)
from supermetrics._generated.supermetrics_api_client.types import Unset

with SupermetricsClient(api_key="your_key") as client:
    current = client.blends.get(team_id=12345, blend_id=569)

    # Read: rebuild the request objects out of the wrapped response. These sources all
    # exist already, so each is addressed by its id and its key is None.
    sources = [
        BlendedDataSourceInput(
            data_source_id=source.data_source_id,
            blend_data_source_id=source.blend_data_source_id,
            blend_data_source_key=None,
            report_type=None if isinstance(source.report_type, Unset) else source.report_type,
            report_type_settings=[],
            display_name=source.display_name,
        )
        for source in current.blended_data_sources.items
    ]

    # blend_field_type and blend_field_data_type come back on every field but have no
    # place in the request, so they are dropped here and re-inferred upstream.
    fields = [
        BlendField(
            blend_field_name=field.blend_field_name,
            blend_field_display_name=field.blend_field_display_name,
            blend_datasource_fields=[
                BlendDatasourceFieldRef(
                    datasource_field_name=ref.datasource_field_name,
                    field_source=ref.field_source,
                    blend_data_source_id=ref.blend_data_source_id,
                    datasource_field_type=ref.datasource_field_type,
                    datasource_field_data_type=ref.datasource_field_data_type,
                )
                for ref in field.blend_datasource_fields.items
            ],
        )
        for field in current.config.fields.items
    ]

    # Modify: rename the blend and keep everything else.
    updated = client.blends.update(
        team_id=12345,
        blend_id=569,
        display_name=f"{current.display_name} (revised)",
        blended_data_sources=sources,
        config=BlendConfig(fields=fields),
        description=current.description,
    )
    print(f"{updated.display_name} now has {len(updated.config.fields.items)} field(s)")
```

The rebuild above assumes a union blend. A join blend also needs `query_table` and `joins`
reconstructed, from `current.config.query_table` and `current.config.joins.items`, again by
id rather than by key.

#### delete()

Delete a blend.

```python
client.blends.delete(team_id=12345, blend_id=569)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `blend_id` (int, required): Unique identifier of the blend to delete

**Returns:** `None`. The API answers **HTTP 204 No Content** on success, so there is no body
to return and nothing to inspect.

**Raises:** `SupermetricsAuthError`, `SupermetricsForbiddenError`, `SupermetricsNotFoundError` (404 if not found), `SupermetricsValidationError` (400), `SupermetricsRateLimitError`, `SupermetricsServerError`, `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsClient
from supermetrics.exceptions import SupermetricsNotFoundError

with SupermetricsClient(api_key="your_key") as client:
    try:
        client.blends.delete(team_id=12345, blend_id=569)
    except SupermetricsNotFoundError:
        print("Already gone")
```

Deletion is not idempotent from the caller's point of view: a second call 404s. Use
`with_raw_response` if you want to assert on the 204 itself.

```python
response = client.with_raw_response.blends.delete(team_id=12345, blend_id=569)
assert response.status_code == 204
assert response.data is None
```

**Async usage** (all five methods above are also available on `BlendsAsyncResource`):

```python
import asyncio

from supermetrics import (
    BlendConfig,
    BlendDatasourceFieldRef,
    BlendField,
    BlendedDataSourceInput,
    SupermetricsAsyncClient,
)


async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        joins, unions = await asyncio.gather(
            client.blends.list(team_id=12345, blend_type="join"),
            client.blends.list(team_id=12345, blend_type="union"),
        )
        print(f"{len(joins)} join blends, {len(unions)} union blends")

        created = await client.blends.create(
            team_id=12345,
            display_name="Clicks, everywhere",
            blend_type="union",
            blended_data_sources=[
                BlendedDataSourceInput(
                    data_source_id="GA4",
                    blend_data_source_id=None,
                    blend_data_source_key="ga4a0001",
                    report_type=None,
                    report_type_settings=[],
                )
            ],
            config=BlendConfig(
                fields=[
                    BlendField(
                        blend_field_name="clicks",
                        blend_field_display_name="Clicks",
                        blend_datasource_fields=[
                            BlendDatasourceFieldRef(
                                datasource_field_name="Clicks",
                                field_source="standard",
                                blend_data_source_key="ga4a0001",
                            )
                        ],
                    )
                ]
            ),
        )
        await client.blends.delete(team_id=12345, blend_id=created.blend_id)


asyncio.run(main())
```

---

## Models

### Backfill

Represents a Data Warehouse backfill job.

**Attributes:**

- `transfer_backfill_id` (int): Unique identifier of the backfill
- `transfer_id` (int): ID of the transfer this backfill belongs to
- `range_start_date` (str): Start date of the backfill range (`YYYY-MM-DD`)
- `range_end_date` (str): End date of the backfill range (`YYYY-MM-DD`)
- `status` (str): Current status — one of `CREATED`, `SCHEDULED`, `RUNNING`, `FAILED`, `COMPLETED`, `CANCELLED`
- `created_time` (str): ISO 8601 timestamp when the backfill was created
- `created_user_id` (int): ID of the user who created the backfill
- `start_time` (str | None): ISO 8601 timestamp when processing started
- `end_time` (str | None): ISO 8601 timestamp when processing completed or was cancelled
- `removed_time` (str | None): ISO 8601 timestamp when the backfill was cancelled
- `removed_user_id` (int | None): ID of the user who cancelled the backfill
- `transfer_runs_total` (int): Total number of transfer runs for this backfill
- `transfer_runs_created` (int): Number of transfer runs that have been created
- `transfer_runs_completed` (int): Number of transfer runs that completed successfully
- `transfer_runs_failed` (int): Number of transfer runs that failed
- `error_report` (list[TransferBackfillRunError]): Errors from failed transfer runs (empty if none)

**Example:**

```python
backfill = client.backfills.get(team_id=12345, backfill_id=67890)

# Check status
print(f"Status: {backfill.status}")

# Track progress
total = backfill.transfer_runs_total
done = backfill.transfer_runs_completed
failed = backfill.transfer_runs_failed
print(f"Progress: {done}/{total} completed, {failed} failed")

# Check for errors
for err in backfill.error_report:
    print(f"  {err.transfer_run_date}: {err.error}")
```

---

### TransferBackfillRunError

Represents an error that occurred during a single transfer run within a backfill.

**Attributes:**

- `transfer_run_date` (str): The date (`YYYY-MM-DD`) of the transfer run that failed
- `error` (str): Error message describing what went wrong

**Example:**

```python
backfill = client.backfills.get(team_id=12345, backfill_id=67890)
for err in backfill.error_report:
    print(f"Run on {err.transfer_run_date} failed: {err.error}")
```

---

### DatasourceDetails

Represents complete configuration metadata for a Supermetrics data source.

**Key Attributes:**

- `id` (str): Unique data source identifier (e.g., `"GAWA"`, `"AW"`)
- `name` (str): Human-readable name (e.g., `"Google Analytics 4"`)
- `description` (str): Detailed description of the data source
- `marketing_name` (str | None): Connector marketing name
- `logo_url` (str): URL to the connector logo image
- `categories` (list[DatasourceDetailsCategoriesItem]): Category tags (e.g., `["Analytics"]`,
  `["Paid Media"]`)
- `products` (list[str]): Products where this datasource is available (e.g., `["API", "DS", "DWH"]`)
- `status` (DatasourceDetailsStatus): Release status — `"Released"` or `"Early access"`
- `is_premium` (bool): Whether this is a premium connector
- `tags` (list[str]): Tags such as `["popular"]`
- `is_authentication_required` (bool): Whether the datasource requires OAuth/credentials
- `has_account_list` (bool): Whether account-level selection is supported
- `has_fields` (bool): Whether field selection is supported
- `has_segments` (bool): Whether segments are supported
- `has_report_type_selection` (bool): Whether report type selection UI should be shown
- `is_date_range_required` (bool): Whether a date range is required
- `min_metrics` (int | None): Minimum metrics required per query
- `max_metrics` (int | None): Maximum metrics allowed per query
- `min_dimensions` (int | None): Minimum dimensions required per query
- `max_dimensions` (int | None): Maximum dimensions allowed per query
- `report_type_header_label` (str): UI label for the report type selector
- `report_types` (list[DatasourceReportType]): Available report types. Each item exposes
  `id` and `label` (there is no `name`), plus `is_date_range_required`,
  `is_free_text_account_required` and `settings`
- `common_settings` (list[DatasourceSetting]): Settings shared across all report types

**Example:**

```python
details = client.datasource_details.get(team_id=12345, data_source_id="GAWA")

print(f"ID:      {details.id}")
print(f"Name:    {details.name}")
print(f"Status:  {details.status}")
print(f"Premium: {details.is_premium}")
print(f"Auth required: {details.is_authentication_required}")

for rt in details.report_types or []:
    print(f"  Report type: {rt.id} — {rt.label}")
```

---

### LoginLink

Represents a data source login link for OAuth authentication.

**Key Attributes:**

- `link_id` (str): Supermetrics login link ID
- `status_code` (str): Current link status
- `description` (str): Internal link description
- `ds_id` (str): Data source ID
- `ds_name` (str): Data source name
- `login_url` (str): Full URL to initiate authentication
- `created_time` (datetime): Link creation time
- `expiry_time` (datetime): Link expiry time
- `login_id` (str | None): Login ID after successful authentication
- `login_time` (datetime | None): Authentication time
- `login_username` (str | None): Username used for authentication

**Example:**

```python
link = client.login_links.create(ds_id="GAWA")
print(f"Visit: {link.login_url}")
print(f"Expires: {link.expiry_time}")
```

---

### DataSourceLogin

Represents an authenticated data source login with credentials.

**Key Attributes:**

- `login_id` (str): Supermetrics login ID
- `username` (str): Authenticated username (use as `ds_user` in queries)
- `display_name` (str): Visible name in UIs
- `ds_info` (DataSource): Data source information
- `auth_time` (datetime): Last authentication time
- `expiry_time` (datetime | None): Authentication expiry time
- `is_refreshable` (bool): Whether auth can be auto-refreshed
- `is_shared` (bool): Whether login is shared with team

**Example:**

```python
login = client.logins.get(login_id="login_abc123")
print(f"Authenticated as: {login.username}")
print(f"Data Source: {login.ds_info.ds_name}")
print(f"Expires: {login.expiry_time}")
```

---

### Account

Represents a data source account.

**Attributes:**

- `account_id` (str): Account ID (use in queries)
- `account_name` (str): Account display name
- `group_name` (str): Account group name

**Example:**

```python
accounts = client.accounts.list(ds_id="GAWA")
for account in accounts:
    print(f"ID: {account.account_id}")
    print(f"Name: {account.account_name}")
    print(f"Group: {account.group_name}")
```

---

### DataResponse

Represents a query execution response.

**Key Attributes:**

- `meta` (DataResponseMeta): Query metadata
  - `request_id` (str): Query request ID
  - `schedule_id` (str): Schedule identifier echoed back by the API
  - `status_code` (str): Query status ("pending", "success", etc.)
  - `query` (DataResponseMetaQuery): The query as the API resolved it, including
    `fields` — a list of field objects with `.field_id`, `.field_name`, `.data_type` and
    `.data_column`. Note that the field definitions live here, not on `meta` itself
  - `result` (DataResponseMetaResult): Result summary
  - `paginate` (DataResponseMetaPaginate): Pagination state
- `data` (list[list[str]]): Query result rows (2D array)

**Example:**

```python
result = client.queries.execute(...)

# Check metadata
if result and result.meta:
    print(f"Status: {result.meta.status_code}")
    print(f"Request ID: {result.meta.request_id}")

# Process data
if result and result.data:
    columns = [field.field_id for field in result.meta.query.fields]
    print(f"Columns: {columns}")

    for row in result.data:
        print(row)
```

---

### TransferInfoResponse

Summary of one transfer, as returned by `transfers.list()`. **Not** the same shape as
`TransferConfigurationResponse` — see the note under `transfers.list()` above.

Every field of every transfer model below is optional in the response schema unless marked
required, so the generated model defaults it to `UNSET`. Guard on it rather than assuming
presence — see [UNSET and Unset](#unset-and-unset).

**Attributes:**

- `dwh_transfer_id` (int | Unset): The transfer ID (e.g. `36091`). Pass this as
  `transfer_id` to the other methods
- `display_name` (str | Unset): Display name of the transfer
- `external_transfer_id` (str | Unset): External identifier for the transfer
- `status` (str | Unset): Transfer status, free-form (example: `"active"`)
- `state` (str | Unset): Transfer state, free-form (example: `"active"`; the API also uses
  `"paused"`). No enum is generated
- `schedule` (str | Unset): Schedule as a **description string** (example: `"daily"`), not a
  list of objects
- `run_date` (str | Unset): Last run date (`YYYY-MM-DD`)
- `data_source` (TransferInfoResponseDataSourceType0 | None | Unset): Data source
  information. Untyped upstream — read `additional_properties`
- `destination` (TransferInfoResponseDestinationType0 | None | Unset): Destination
  information. Untyped upstream — read `additional_properties`
- `accounts` (list[str] | Unset): Account identifiers, as **strings**
- `backfill` (TransferInfoResponseBackfillType0 | None | Unset): Backfill statistics.
  Untyped upstream — read `additional_properties`

**Example:**

```python
for transfer in client.transfers.list(team_id=12345):
    print(f"{transfer.dwh_transfer_id}: {transfer.display_name}")
    print(f"  {transfer.state} / {transfer.schedule} / last run {transfer.run_date}")
    print(f"  accounts: {', '.join(transfer.accounts or [])}")
```

---

### TransferConfigurationResponse

Full configuration of one transfer, as returned by `transfers.get()`. The API sends this one
bare, without a `{"meta": ..., "data": ...}` envelope.

**Attributes:**

- `transfer_id` (int | Unset): The transfer ID (note: `dwh_transfer_id` in the list item)
- `display_name` (str | Unset): Display name of the transfer
- `schema_id` (int | Unset): Data warehouse schema identifier of the table group
- `destination_id` (int | None | Unset): Destination identifier
- `accounts` (list[TransferAccount] | Unset): Data source accounts included in the transfer,
  as **objects** (strings in the list item)
- `segments` (list[TransferSegment] | Unset): Data segments included in the transfer
- `license_` (TransferConfigurationResponseLicense | Unset): License information — `id`,
  `product_title`, `license_title`, `is_expired`, `is_trial`, `end_date`, `features`. Note
  the trailing underscore, which avoids the Python keyword
- `schedule` (list[TransferSchedule] | Unset): Transfer schedule, as a **list of objects**
  (a single string in the list item)
- `data_source` (TransferConfigurationResponseDataSource | Unset): `data_source_id`,
  `service_name`, `service_provider`, and `settings` (list[TransferDataSourceSetting])
- `notification_recipients` (list | None | Unset): Email recipients for transfer
  notifications
- `external_url` (str | None | Unset): External URL, for DTS BigQuery transfers

**Example:**

```python
configuration = client.transfers.get(team_id=12345, transfer_id=36091)

print(configuration.display_name)
print(configuration.data_source.data_source_id, configuration.data_source.service_name)

for entry in configuration.schedule or []:
    print(f"{entry.run_interval} @ {entry.run_hour}:00 UTC, window {entry.refresh_window}d")

if configuration.license_ and configuration.license_.is_expired:
    print("License has expired")
```

---

### TransferCreatedResponse

What `transfers.create()` returns, unwrapped from its `{"meta": ..., "data": ...}` envelope.

**Attributes:**

- `transfer_id` (int | Unset): The ID of the created transfer
- `transfer_name` (str | Unset): The display name of the created transfer

---

### TransferUpdatedResponse

What `transfers.update()` returns. The API sends this one bare.

**Attributes:**

- `transfer_id` (int | Unset): The ID of the updated transfer
- `transfer_name` (str | Unset): The display name of the updated transfer

---

### TransferStateUpdateResponse

What `transfers.set_state()` returns.

**Attributes:**

- `result` (bool | Unset): Whether the state change succeeded
- `state` (str | Unset): The transfer's state after the action. A free-form string with no
  enum; the documented example is the uppercase `"PAUSED"`, while the verbs accepted by
  `set_state()` are the lowercase `"pause"` and `"unpause"`. The two vocabularies do not
  match

**Example:**

```python
response = client.transfers.set_state(team_id=12345, transfer_id=36091, state="pause")
print(response.result, response.state)  # True PAUSED
```

---

### ValidationErrorsResponse

What `transfers.validate()` and `transfers.validate_update()` return — **including when the
configuration is invalid**, which the API reports as HTTP 200 with `is_valid` set to
`False` rather than as an error.

**Attributes:**

- `is_valid` (bool | Unset): Whether the configuration is valid
- `errors` (list[ValidationError] | Unset): Field-level errors; empty when valid

**Example:**

```python
result = client.transfers.validate(...)

if not result.is_valid:
    for error in result.errors or []:
        print(f"{error.field_id}: {error.error_code}")
```

---

### ValidationError

A single field validation error inside a `ValidationErrorsResponse`. Unrelated to the
`ValidationError` **exception** alias exported from `supermetrics` — this one is a data
model and is never raised.

**Attributes:**

- `field_id` (str | Unset): The field that failed validation (example: `"display_name"`)
- `error_code` (str | Unset): The validation error code (example: `"isEmpty"`)

There is **no human-readable message** in this payload. `error_code` is all the API gives
you, so any text shown to a user has to be mapped from the code by the caller.

---

### AvailableSourcesResponse

What `transfers.list_available_sources()` returns.

**Attributes:**

- `data_sources` (list[DataSourceInfo] | Unset): Available data sources, sorted
  alphabetically by service name. Each item carries `data_source_id`, `service_name`,
  `service_provider`, `logo_url`, `has_custom_fields`, `is_custom_connector`,
  `is_public_beta`, `is_released`, `is_internal`, and `applicable_destinations`
- `destinations` (list[TransferDestination] | Unset): Available destination instances. Each
  item carries `destination_id`, `destination_name`, `destination_type`,
  `destination_label`, `destination_icon_url`, `is_internal`, and `details`
- `destination_types` (list[DestinationTypeSettings] | Unset): Destination type
  configurations. Each item carries `title`, `type_`, `connection_check_url`, `create_url`,
  `update_url_template`, `icon_url`, `app_id`, `is_internal`, `settings`, and `auth_methods`

**Example:**

```python
available = client.transfers.list_available_sources(team_id=12345)

released = [s for s in available.data_sources or [] if s.is_released]
print(f"{len(released)} released data sources")

for destination_type in available.destination_types or []:
    print(f"{destination_type.type_}: {destination_type.title}")
```

---

### TransferOptionsResponse

What `transfers.get_available_options()` returns. Almost every member is untyped upstream —
see the note under [`get_available_options()`](#get_available_options).

**Attributes:**

- `data_source` (TransferOptionsResponseDataSource | Unset): `data_source_id`,
  `service_name`, and `settings`. The only member with described properties
- `schedule_options` (list | Unset): Available schedule options. Untyped — read
  `additional_properties`
- `schemas` (list | Unset): Available schemas. Untyped
- `logins` (list | Unset): Available logins for the data source. Untyped
- `accounts` (list | Unset): Available accounts for the data source. Untyped
- `segments` (list | Unset): Available segments for the data source. Untyped
- `license_` (TransferOptionsResponseLicense | Unset): License information for the team.
  Untyped

**Example:**

```python
options = client.transfers.get_available_options(team_id=12345, source_id="AW", destination_id=8)

print(options.data_source.service_name)
for schema in options.schemas or []:
    print(schema.additional_properties)  # keys are whatever the API sent
```

---

### TransferRunItem

One run in the list returned by `transfers.list_runs()`. Leaner than `TransferRunDetail`:
no per-query breakdown, no queued/started timestamps.

**Attributes:**

- `id` (int, required): Unique identifier of the transfer run. Pass this to
  `transfer_runs.get()`
- `status` (str, required): Current status, free-form (example: `"COMPLETED"`). No enum is
  generated
- `type_` (str, required): Type of the run — `"Recurring"` or `"Backfill"`. Note the
  trailing underscore
- `message` (str, required): Status message or error description
- `created_time` (datetime | None | Unset): When the run was created
- `ended_time` (datetime | None | Unset): When the run finished processing
- `total_duration` (float | None | Unset): Sum of all query durations, in seconds
- `total_rows` (int | None | Unset): Total rows processed
- `data_date` (date | None | Unset): The data date this run covers

**Example:**

```python
import datetime

runs = client.transfers.list_runs(
    team_id=12345,
    transfer_id=36091,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 31),
)

for run in runs:
    print(f"{run.data_date} [{run.type_}] {run.status}: {run.total_rows} rows")
```

---

### TransferRunDetail

One run in full, as returned by `transfer_runs.get()`.

**Attributes:**

- `id` (int, required): Unique identifier of the transfer run
- `status` (str, required): Current status, free-form (example: `"COMPLETED"`)
- `query_details` (list[QueryDetails], required): Per-query execution details
- `external_id` (str, required): External identifier of the run
- `message` (str, required): Status message or error description
- `started_time` (datetime | None | Unset): When the run started processing
- `ended_time` (datetime | None | Unset): When the run finished processing
- `created_time` (datetime | None | Unset): When the run was created
- `queued_time` (datetime | None | Unset): When the run was queued
- `failed_query_amount` (int | None | Unset): Number of queries that failed
- `total_duration` (float | None | Unset): Sum of all query durations, in seconds
- `total_rows` (int | None | Unset): Total rows processed
- `query_amount` (int | None | Unset): Total queries executed
- `data_date` (date | None | Unset): The data date this run covers

**Example:**

```python
run = client.transfer_runs.get(team_id=12345, transfer_run_id=98765)

print(f"{run.status}: {run.total_rows} rows across {run.query_amount} queries")
print(f"Queued {run.queued_time}, started {run.started_time}, ended {run.ended_time}")

failed = [q for q in run.query_details if q.error_description]
for query in failed:
    print(f"  failed: {query.error_description}")
```

---

### QueryDetails

Per-query execution details inside a `TransferRunDetail`.

**Attributes:**

- `status` (str, required): Status of this query execution (example: `"COMPLETED"`)
- `rows` (int, required): Number of rows returned by this query
- `duration` (float | None | Unset): Duration of this query, in seconds
- `error_description` (str | None | Unset): Error description if the query failed

---

### DataSourceConnection

What `transfers.create_datasource_connection()` returns, unwrapped from its envelope.

**Attributes:**

- `connection_id` (UUID, required): Unique identifier of the created connection. A
  `uuid.UUID`, not a string
- `login_url` (str | None | Unset): URL for the OAuth login flow, when the data source
  requires user authentication. Always `null` in the current V1 implementation
- `connect_url` (str | None | Unset): URL for the connection flow, when additional
  authentication steps are required. Always `null` in the current V1 implementation

**Example:**

```python
connection = client.transfers.create_datasource_connection(
    team_id=12345, data_source_id="ADM", destination_type="DWH_SNOWFLAKE"
)
print(str(connection.connection_id))
```

---

### TransferSchedule

Request-side model. One entry in the `schedule` list of `transfers.create()`,
`update()`, `validate()`, and `validate_update()`, and also what
`TransferConfigurationResponse.schedule` contains. Every field is optional.

**Attributes:**

- `run_interval` (str | Unset): Frequency — `"hourly"`, `"daily"`, `"weekly"`, or
  `"monthly"`
- `run_hour` (int | Unset): Hour of day to run, in UTC
- `refresh_window` (int | Unset): Number of days to refresh
- `run_weekday` (int | Unset): Day of week to run (1 = Monday, 7 = Sunday). Required by the
  API for the `"weekly"` interval
- `run_day` (int | Unset): Day of month to run. Required by the API for the `"monthly"`
  interval

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.models import TransferSchedule

daily = TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)
weekly = TransferSchedule(run_interval="weekly", run_hour=3, run_weekday=1)
monthly = TransferSchedule(run_interval="monthly", run_hour=3, run_day=1)
```

---

### TransferAccount

Request-side model. One entry in the `accounts` list, and what
`TransferConfigurationResponse.accounts` contains. Every field is optional.

**Attributes:**

- `data_source_username` (str | Unset): Username for data source authentication
- `login_id` (int | Unset): Login identifier
- `account_id` (str | Unset): Account identifier in the data source

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.models import TransferAccount

account = TransferAccount(data_source_username="user.name@company.com", login_id=2682599, account_id="8733197711")
```

---

### TransferSegment

Request-side model. One entry in the optional `segments` list, and what
`TransferConfigurationResponse.segments` contains. Every field is optional.

**Attributes:**

- `data_source_username` (str | Unset): Username for data source authentication
- `login_id` (int | Unset): Login identifier
- `segment_id` (str | Unset): Segment identifier
- `segment_name` (str | Unset): Human-readable segment name

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.models import TransferSegment

segment = TransferSegment(login_id=2830506, segment_id="-1", segment_name="All users")
```

---

### TransferDataSourceSetting

Request-side model. One entry in the optional `data_source_settings` list, and what
`TransferConfigurationResponse.data_source.settings` contains. Every field is optional.

**Attributes:**

- `field_id` (str | Unset): Setting field identifier (example: `"BRAND_KEYWORDS"`)
- `value` (bool | int | str | None | Unset): Setting value. The type varies by field
- `group` (str | Unset): Setting group identifier (example: `"Default"`)

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.models import TransferDataSourceSetting

setting = TransferDataSourceSetting(field_id="BRAND_KEYWORDS", value="", group="Default")
```

---

### TeamTransformationOutput

A persisted custom field, as every read and write on `client.custom_fields` returns it.
Named after the upstream term: a custom field is a *field transformation*.

Every attribute is optional upstream, so each is typed `... | Unset`.

**Attributes:**

- `id` (int | Unset): Unique identifier of the custom field. Pass this to `get()`,
  `update()`, and `delete()`
- `name` (str | Unset): Machine name the API assigned (example: `"spec_example_field"`).
  This is what appears in a query's field list; `display_name` is what appears in the UI
- `data_source_id` (str | Unset): ID of the data source the field belongs to (example:
  `"GAWA"`)
- `display_name` (str | Unset): User-facing name shown in the UI
- `description` (str | Unset): Free-text description
- `field_type` (`"dim"` | `"met"` | Unset): Field kind — dimension or metric. Fixed at
  creation
- `data_type` (str | Unset): Data type of the transformed field (example:
  `"string.text.value"`)
- `modified_time_utc` (datetime | Unset): Timestamp of the last modification. Serialized
  with a numeric offset (`"+0000"`) rather than a trailing `"Z"`, and parsed into a
  **timezone-aware** `datetime`
- `modified_user` (TransformationUserOutput | Unset): Who last modified it — `email`,
  `first_name`, `last_name`
- `definition` (TeamTransformationOutputDefinition | Unset): Wrapper holding the ordered
  pipeline. **The steps are at `.definition.items`**, not at `.definition`
- `report_types` (list[str] | Unset): Report types associated with the field (example:
  `["Default"]`)

**Example:**

```python
import datetime

field = client.custom_fields.get(team_id=12345, custom_field_id=42)

print(f"{field.display_name} ({field.name}) -> {field.data_type}")
print(f"{'Dimension' if field.field_type == 'dim' else 'Metric'} on {field.data_source_id}")

# modified_time_utc is tz-aware, so it compares directly against an aware datetime
age = datetime.datetime.now(datetime.UTC) - field.modified_time_utc
print(f"Last touched {age.days} days ago by {field.modified_user.email}")

for step in field.definition.items:
    print(f"  {step.type_}")
```

---

### TeamTransformationOutputDefinition

The read-side wrapper around a definition. Its only reason to exist is that the response
nests the pipeline in an object while the request takes a bare list — which is why a
read-modify-write reads `.items` and passes that straight back to `update()`.

**Attributes:**

- `items` (list[FunctionStep | LookupStep | ConditionStep] | Unset): The ordered pipeline

The union is a `oneOf` upstream and is discriminated correctly on parse: a definition
holding all three kinds comes back as `[FunctionStep, LookupStep, ConditionStep]`, in the
order the API sent them. Branch on `type(step)` or on `step.type_`.

**Example:**

```python
from supermetrics import ConditionStep, FunctionStep, LookupStep

field = client.custom_fields.get(team_id=12345, custom_field_id=42)

for step in field.definition.items:
    if isinstance(step, FunctionStep):
        print(f"call {step.name} with {len(step.arguments)} argument(s)")
    elif isinstance(step, LookupStep):
        print(f"lookup by {step.rule} over {len(step.map_.additional_properties)} entries")
    elif isinstance(step, ConditionStep):
        print(f"{len(step.cases)} case(s), default {step.default}")
```

---

### MetadataOutputData

What `custom_fields.get_metadata()` returns: the building blocks a team is allowed to use
in a definition. Every attribute is optional upstream.

**Attributes:**

- `rules` (MetadataOutputDataRules | Unset): Matching rules, split into
  `rules.condition.items` and `rules.lookup.items` — each a `list[RuleOutput]` with `name`
  and `display_name`
- `functions` (MetadataOutputDataFunctions | Unset): Available functions at
  `functions.items`, a `list[FunctionSpecificationOutput]` with `name`, `display_name`,
  `description`, `group_name`, `arguments`, and `return_types`
- `field_data_types` (list[str] | Unset): Field data types that can be referenced in a
  definition (example: `["string.text.value"]`)
- `output_data_types` (MetadataOutputDataOutputDataTypes | Unset): Legal `data_type` values
  at `output_data_types.items`, a `list[OutputDataTypeOutput]` with `output_type` and
  `label`
- `data_transformation_steps_limit` (int | Unset): Maximum number of steps the team may put
  in one definition

Note the repeated `.items` indirection — `functions`, `output_data_types`,
`rules.condition`, and `rules.lookup` are each a wrapper object, not a list. Only
`field_data_types` is a bare list.

An argument inside `FunctionSpecificationOutput.arguments` is an open-ended object with no
declared fields, so read it by key (`argument["name"]`), not by attribute.

**Example:**

```python
metadata = client.custom_fields.get_metadata(team_id=12345)

by_group: dict[str, list[str]] = {}
for function in metadata.functions.items:
    by_group.setdefault(function.group_name, []).append(function.name)

for group, names in sorted(by_group.items()):
    print(f"{group}: {', '.join(sorted(names))}")

print(f"Legal data_type values: {[t.output_type for t in metadata.output_data_types.items]}")
print(f"Lookup rules: {[rule.name for rule in metadata.rules.lookup.items]}")
print(f"At most {metadata.data_transformation_steps_limit} steps per definition")
```

---

### FunctionStep

A definition step that applies a named function to its arguments. Importable from
`supermetrics`.

**Attributes:**

- `type_` (str, required): Always `"function"`. Serializes to `"type"`
- `name` (str, required): Name of the function to apply. Must be one of the names in
  `get_metadata().functions.items`
- `arguments` (list[FunctionArgument], required): Arguments passed to the function
- `description` (str | None | Unset): Optional free-text description of the step

**Example:**

```python
from supermetrics import DefinitionValue, FunctionArgument, FunctionStep

step = FunctionStep(
    type_="function",
    name="upper_case",
    arguments=[FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))],
    description="Normalise casing before the lookup",
)
```

---

### LookupStep

A definition step that maps input values to output values through a lookup table and a
matching rule. Importable from `supermetrics`.

**Attributes:**

- `type_` (str, required): Always `"lookup"`. Serializes to `"type"`
- `rule` (str, required): The matching rule applied when looking a value up (example:
  `"equals"`). Legal values come from `get_metadata().rules.lookup.items`
- `map_` (LookupStepMap, required): The key/value table. Serializes to `"map"`
- `source` (DefinitionValue | Unset): Where the input value comes from
- `default` (DefinitionValue | Unset): Value produced when nothing matches
- `description` (str | None | Unset): Optional free-text description of the step

**Example:**

```python
from supermetrics import DefinitionValue, LookupStep, LookupStepMap

mapping = LookupStepMap()
mapping["GOOGLE"] = "Google Ads"
mapping["FACEBOOK"] = "Meta Ads"

step = LookupStep(
    type_="lookup",
    rule="equals",
    map_=mapping,
    source=DefinitionValue(type_="output_from_previous"),
    default=DefinitionValue(type_="static", value="Other"),
)
```

---

### LookupStepMap

The key/value table inside a [`LookupStep`](#lookupstep). Importable from `supermetrics`.

Upstream declares it as an open-ended object with no fixed properties, so the generated
model has **no declared attributes at all** — the mapping lives in
`additional_properties`, which is declared `init=False`.

> **The constructor takes no mapping.** `LookupStepMap({"a": "b"})` is a `TypeError`.
> Build it empty and assign the entries, either through the item accessors or by replacing
> `additional_properties` wholesale.

**Example:**

```python
from supermetrics import LookupStepMap

# Item assignment
mapping = LookupStepMap()
mapping["GOOGLE"] = "Google Ads"
mapping["FACEBOOK"] = "Meta Ads"

# Or assign the whole dict at once
bulk = LookupStepMap()
bulk.additional_properties = {"GOOGLE": "Google Ads", "FACEBOOK": "Meta Ads"}

# Reading one back
print(mapping["GOOGLE"])  # "Google Ads"
print("TIKTOK" in mapping)  # False
print(mapping.additional_properties)  # {'GOOGLE': 'Google Ads', 'FACEBOOK': 'Meta Ads'}
```

---

### ConditionStep

A definition step that evaluates an ordered list of cases and produces the result of the
first match, falling back to `default` when none match. Importable from `supermetrics`.

**Attributes:**

- `type_` (str, required): Always `"condition"`. Serializes to `"type"`
- `default` (DefinitionValue | FunctionStep, required): Value produced when no case
  matches. This is itself a `oneOf` — a plain value *or* a whole nested function step
- `cases` (list[ConditionCase], required): Cases evaluated in order; the first match wins
- `description` (str | None | Unset): Optional free-text description of the step

**Example:**

```python
from supermetrics import ConditionCase, ConditionCaseCondition, ConditionStep, DefinitionValue

step = ConditionStep(
    type_="condition",
    default=DefinitionValue(type_="static", value="Unclassified"),
    cases=[
        ConditionCase(
            return_=DefinitionValue(type_="static", value="Search"),
            condition=ConditionCaseCondition(
                type_="rule",
                rule="equals",
                source=DefinitionValue(type_="output_from_previous"),
                target=DefinitionValue(type_="static", value="Google Ads"),
            ),
        )
    ],
)
```

---

### ConditionCase

One case inside a [`ConditionStep`](#conditionstep): when `condition` evaluates true, the
return value is produced. Importable from `supermetrics`.

**Attributes:**

- `return_` (DefinitionValue, required): The value produced when this case matches
- `condition` (ConditionCaseCondition, required): The rule evaluated for this case

> **The field is `return_`, with a trailing underscore.** It serializes to `"return"` on
> the wire, which cannot be a Python attribute name because `return` is a keyword. This is
> the same convention as `type_` and `map_` elsewhere in these models.

**Example:**

```python
from supermetrics import ConditionCase, ConditionCaseCondition, DefinitionValue

case = ConditionCase(
    return_=DefinitionValue(type_="static", value="Paid"),
    condition=ConditionCaseCondition(
        type_="rule",
        rule="equals",
        source=DefinitionValue(type_="data_source_field", value="medium"),
        target=DefinitionValue(type_="static", value="cpc"),
    ),
)
```

---

### ConditionCaseCondition

The rule-based comparison inside a [`ConditionCase`](#conditioncase). Importable from
`supermetrics`.

**Attributes:**

- `type_` (str, required): Always `"rule"`. Serializes to `"type"`
- `rule` (str, required): The comparison operator applied between `source` and `target`
  (example: `"equals"`). Legal values come from `get_metadata().rules.condition.items`
- `source` (DefinitionValue, required): Left-hand side of the comparison
- `target` (DefinitionValue, required): Right-hand side of the comparison

**Example:**

```python
from supermetrics import ConditionCaseCondition, DefinitionValue

condition = ConditionCaseCondition(
    type_="rule",
    rule="equals",
    source=DefinitionValue(type_="output_from_previous"),
    target=DefinitionValue(type_="static", value="1"),
)
```

---

### DefinitionValue

A value reference used throughout a definition — as a function argument, a lookup source
or default, and both sides of a condition. Importable from `supermetrics`.

**Attributes:**

- `type_` (str, required): Where the value comes from. Serializes to `"type"`:
  - `"data_source_field"` — a named field on the data source
  - `"output_from_previous"` — the result of the preceding step
  - `"static"` — a literal value
- `value` (str | Unset): The value itself — the field name for `"data_source_field"`, the
  literal for `"static"`, and **omitted** for `"output_from_previous"`

**Example:**

```python
from supermetrics import DefinitionValue

from_field = DefinitionValue(type_="data_source_field", value="platform")
from_previous = DefinitionValue(type_="output_from_previous")  # no value
literal = DefinitionValue(type_="static", value="cpc")
```

---

### FunctionArgument

A named argument supplied to a [`FunctionStep`](#functionstep). Importable from
`supermetrics`.

**Attributes:**

- `name` (str, required): Argument name as the function expects it. The names a given
  function takes are listed in `get_metadata().functions.items[*].arguments`
- `value` (DefinitionValue, required): The argument's value reference

**Example:**

```python
from supermetrics import DefinitionValue, FunctionArgument

argument = FunctionArgument(name="value", value=DefinitionValue(type_="data_source_field", value="platform"))
```

---

### CustomFieldCreateRequestDataSourceItem

One entry in the optional `data_source` list on `custom_fields.create()`, scoping the field
to a data source and optionally to a report type within it. Importable from
`supermetrics`. Both attributes are optional.

**Attributes:**

- `data_source_id` (str | Unset): ID of the data source (example: `"GAWA"`)
- `report_type` (str | None | Unset): Report type within that data source, if any

`update()` does not accept this — the data sources a field applies to are fixed at
creation, like `field_type`.

**Example:**

```python
from supermetrics import CustomFieldCreateRequestDataSourceItem

sources = [
    CustomFieldCreateRequestDataSourceItem(data_source_id="GAWA"),
    CustomFieldCreateRequestDataSourceItem(data_source_id="AW", report_type="Default"),
]
```

---

### BlendOutput

A whole blend, as `blends.get()`, `blends.create()`, and `blends.update()` return it. Every
attribute is optional upstream, so each is typed `... | Unset`.

**Attributes:**

- `blend_id` (int | Unset): Unique identifier of the blend. Pass this to `get()`,
  `update()`, and `delete()`
- `blend_uuid` (UUID | Unset): Stable UUID of the blend, parsed into a **`uuid.UUID`** and
  not left as a string
- `type_` (`"join"` | `"union"` | Unset): Blend kind, fixed at creation. Serialized as
  `"type"`
- `display_name` (str | Unset): User-facing name shown in the UI
- `description` (str | None | Unset): Free-text description
- `modified_time_utc` (datetime | Unset): Timestamp of the last modification. Serialized
  with a numeric offset (`"+0000"`) rather than a trailing `"Z"`, and parsed into a
  **timezone-aware** `datetime`
- `last_modify_user_email` (str | Unset): Email of the user who last modified the blend
- `blended_data_sources` (BlendOutputBlendedDataSources | Unset): Wrapper holding the
  sources. **They are at `.blended_data_sources.items`**, a
  `list[`[`BlendedDataSourceOutput`](#blendeddatasourceoutput)`]`
- `config` (BlendConfigOutput | Unset): The field mappings and, on a join blend, the primary
  table and joins. See [`BlendConfigOutput`](#blendconfigoutput)

> **This object cannot be handed back to `update()`.** It is a different type from the
> request models at every level: collections are wrapped instead of bare,
> `blend_data_source_key` is gone, and `blend_field_type` / `blend_field_data_type` have
> been added. A read-modify-write rebuilds
> [`BlendedDataSourceInput`](#blendeddatasourceinput) and [`BlendConfig`](#blendconfig)
> objects from it — see the [`update()` example](#update-2).

**Example:**

```python
import datetime

blend = client.blends.get(team_id=12345, blend_id=569)

print(f"{blend.display_name} ({blend.type_}) — {blend.blend_uuid}")

# modified_time_utc is tz-aware, so it compares directly against an aware datetime
age = datetime.datetime.now(datetime.UTC) - blend.modified_time_utc
print(f"Last touched {age.days} days ago by {blend.last_modify_user_email}")

for source in blend.blended_data_sources.items:
    print(f"  {source.data_source_id} (blend_data_source_id={source.blend_data_source_id})")
```

---

### BlendListItemOutput

A blend summary, as `blends.list()` returns them. Every attribute is optional upstream.

**Attributes:**

- `blend_id` (int | Unset): Unique identifier of the blend
- `blend_uuid` (UUID | Unset): Stable UUID of the blend, parsed into a `uuid.UUID`
- `type_` (`"join"` | `"union"` | Unset): Blend kind. Serialized as `"type"`
- `display_name` (str | Unset): User-facing name shown in the UI
- `description` (str | None | Unset): Free-text description
- `modified_time_utc` (datetime | Unset): Timestamp of the last modification, timezone-aware
- `last_modify_user_email` (str | Unset): Email of the user who last modified the blend
- `blended_data_sources` (BlendListItemOutputBlendedDataSources | Unset): Wrapper holding
  the sources at `.items`, a `list[`[`BlendListDataSourceOutput`](#blendlistdatasourceoutput)`]`

> **A summary is not a small `BlendOutput`.** It has **no `config`** — no fields, no joins,
> no query table — and its data sources carry four attributes rather than ten. Anything
> beyond the list above requires a [`get()`](#get-7) per blend.

**Example:**

```python
summaries = client.blends.list(team_id=12345)

# The summary is enough to pick one; the fields need a second call.
for summary in summaries:
    print(f"{summary.blend_id}: {summary.display_name} ({summary.type_})")

blend = client.blends.get(team_id=12345, blend_id=summaries[0].blend_id)
print([field.blend_field_name for field in blend.config.fields.items])
```

---

### BlendListDataSourceOutput

The reduced view of a data source that appears inside a
[`BlendListItemOutput`](#blendlistitemoutput). Every attribute is optional upstream.

**Attributes:**

- `blend_data_source_id` (int | Unset): Internal ID of the source within the blend
- `data_source_id` (str | Unset): Data source identifier (example: `"GA4"`)
- `display_name` (str | Unset): Display name of the data source
- `logo_url` (str | Unset): URL of the data source's logo

Settings, accounts, segments, and report type are absent here; they are on
[`BlendedDataSourceOutput`](#blendeddatasourceoutput), which only `get()`, `create()`, and
`update()` return.

**Example:**

```python
for summary in client.blends.list(team_id=12345):
    names = [source.display_name for source in summary.blended_data_sources.items]
    print(f"{summary.display_name}: {', '.join(names)}")
```

---

### BlendConfigOutput

The read side of a blend's configuration. Every attribute is optional upstream.

**Attributes:**

- `fields` (BlendConfigOutputFields | Unset): Wrapper holding the blend's fields at
  `.fields.items`, a `list[`[`BlendFieldOutput`](#blendfieldoutput)`]`
- `query_table` (BlendConfigOutputQueryTable | Unset): The primary (left-hand) source of a
  join blend, carrying only `blend_data_source_id`
- `joins` (BlendConfigOutputJoins | Unset): Wrapper holding the joins at `.joins.items`, a
  `list[`[`BlendJoinOutput`](#blendjoinoutput)`]`

> **On a union blend, `query_table` and `joins` are `Unset`, not `None`.** They are absent
> from the JSON rather than null, so the generated model leaves the sentinel in place. Guard
> them with `isinstance(config.joins, Unset)`; `config.joins is None` is false and the
> `.items` access after it raises `AttributeError`.

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.types import Unset

config = client.blends.get(team_id=12345, blend_id=569).config

for field in config.fields.items:
    print(field.blend_field_name)

if isinstance(config.joins, Unset):
    print("union blend: no joins, no query table")
else:
    print(f"join blend on source {config.query_table.blend_data_source_id}")
    for join in config.joins.items:
        print(f"  {join.type_} join with {join.join_table.blend_data_source_id}")
```

---

### BlendFieldOutput

One field of a blend, on the read side: the blend's own column plus the per-source fields
that feed it. Every attribute is optional upstream.

**Attributes:**

- `blend_field_name` (str | Unset): Machine name of the blend field (example:
  `"impressions"`). Fixed once created
- `blend_field_display_name` (str | Unset): User-facing name shown in the UI
- `blend_field_type` (`"dim"` | `"met"` | Unset): Dimension or metric. **Response-only** —
  upstream infers it from the mapped fields
- `blend_field_data_type` (str | Unset): Data type of the field (example:
  `"int.number.value"`). **Response-only**, inferred the same way
- `blend_datasource_fields` (BlendFieldOutputBlendDatasourceFields | Unset): Wrapper holding
  the per-source mappings at `.items`, a
  `list[`[`BlendDatasourceFieldRefOutput`](#blenddatasourcefieldrefoutput)`]`

> **Two of these five attributes have no request counterpart.** [`BlendField`](#blendfield)
> has `blend_field_name`, `blend_field_display_name`, and `blend_datasource_fields` and
> nothing else, so `blend_field_type` and `blend_field_data_type` are dropped when rebuilding
> a field for `update()` and re-inferred upstream.

**Example:**

```python
blend = client.blends.get(team_id=12345, blend_id=569)

for field in blend.config.fields.items:
    kind = "dimension" if field.blend_field_type == "dim" else "metric"
    print(f"{field.blend_field_display_name} — {kind}, {field.blend_field_data_type}")
    for ref in field.blend_datasource_fields.items:
        print(f"  source {ref.blend_data_source_id}: {ref.datasource_field_name}")
```

---

### BlendDatasourceFieldRefOutput

The read side of a per-source field reference. Every attribute is optional upstream.

**Attributes:**

- `blend_data_source_id` (int | None | Unset): The source this field comes from
- `datasource_field_name` (str | Unset): Field name as the data source defines it
- `datasource_field_display_name` (str | Unset): Display name of that field
- `datasource_field_type` (`"dim"` | `"met"` | Unset): Dimension or metric
- `datasource_field_data_type` (str | Unset): Data type of the field
- `field_source` (`"standard"` | `"transformation"` | `"data_source_account_custom"` | Unset):
  Where the field comes from — the data source itself, a custom field, or an account-level
  custom field
- `meta` (BlendDatasourceFieldRefOutputMetaType0 | None | Unset): Free-form metadata, whose
  contents live in `.additional_properties`

> **There is no `blend_data_source_key` here.** The key is a request-scoped alias, so the
> response only ever speaks in `blend_data_source_id`. This is the read counterpart of
> [`BlendDatasourceFieldRef`](#blenddatasourcefieldref), which has both.

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.types import Unset

field = client.blends.get(team_id=12345, blend_id=569).config.fields.items[0]

for ref in field.blend_datasource_fields.items:
    print(f"{ref.datasource_field_name} ({ref.field_source}) from {ref.blend_data_source_id}")
    if ref.meta is not None and not isinstance(ref.meta, Unset):
        print(f"  meta: {ref.meta.additional_properties}")
```

---

### BlendJoinOutput

The read side of one join between the primary table and another source. Every attribute is
optional upstream.

**Attributes:**

- `join_table` (BlendJoinOutputJoinTable | Unset): The joined source, carrying only
  `blend_data_source_id`
- `type_` (`"inner"` | `"left"` | `"right"` | `"full outer"` | Unset): Join type. Serialized
  as `"type"`
- `conditions` (BlendJoinOutputConditions | Unset): Wrapper holding the conditions at
  `.conditions.items`, a `list[BlendJoinConditionOutput]` — each with `operator`, `left`,
  and `right`, the last two being
  [`BlendDatasourceFieldRefOutput`](#blenddatasourcefieldrefoutput)

**Example:**

```python
config = client.blends.get(team_id=12345, blend_id=569).config

for join in config.joins.items:
    print(f"{join.type_} join with source {join.join_table.blend_data_source_id}")
    for condition in join.conditions.items:
        left, right = condition.left, condition.right
        print(
            f"  {left.blend_data_source_id}.{left.datasource_field_name}"
            f" {condition.operator} "
            f"{right.blend_data_source_id}.{right.datasource_field_name}"
        )
```

---

### BlendedDataSourceOutput

The read side of one data source in a blend, as it appears at
`blend.blended_data_sources.items`. Every attribute is optional upstream.

**Attributes:**

- `blend_data_source_id` (int | Unset): Internal ID of the source within the blend. This is
  what field and join references point at on the read side
- `blend_id` (int | Unset): ID of the blend this source belongs to
- `data_source_id` (str | Unset): Data source identifier (example: `"GA4"`)
- `display_name` (str | Unset): Display name of the data source
- `data_source_settings` (BlendedDataSourceOutputDataSourceSettings | Unset): Wrapper whose
  `.items` are **untyped** objects
- `accounts` (BlendedDataSourceOutputAccounts | Unset): Wrapper whose `.items` are
  **untyped** objects
- `segments` (BlendedDataSourceOutputSegments | Unset): Wrapper whose `.items` are
  **untyped** objects
- `report_type` (str | None | Unset): Report type ID, if the source has one
- `report_type_settings` (BlendedDataSourceOutputReportTypeSettings | Unset): Wrapper whose
  `.items` are **untyped** objects
- `logo_url` (str | Unset): URL of the data source's logo

> **The settings, accounts, and segments items have no declared attributes.** Upstream
> models them as free-form objects on the response side only, so the generated classes
> expose nothing but `additional_properties` — read them by key, not by attribute:
> `source.accounts.items[0].additional_properties["account_id"]`. The *request* side is
> typed: [`BlendedDataSourceInput`](#blendeddatasourceinput) takes real
> `BlendedDataSourceInputAccountsItem` objects with `.account_id` and `.account_name`.

**Example:**

```python
blend = client.blends.get(team_id=12345, blend_id=569)

for source in blend.blended_data_sources.items:
    print(f"{source.display_name} ({source.data_source_id}), report type {source.report_type}")

    for setting in source.data_source_settings.items:
        # Untyped on the way out: everything is in additional_properties.
        properties = setting.additional_properties
        print(f"  {properties['id']} = {properties['value']!r}")

    for account in source.accounts.items:
        print(f"  account {account.additional_properties['account_id']}")
```

---

### BlendedDataSourceInput

One data source in a `create()` or `update()` request. Importable from `supermetrics`.

**Attributes:**

- `data_source_id` (str, required): Data source identifier, i.e. the connector ID (example:
  `"GA4"`)
- `blend_data_source_id` (int | None, required): Internal ID of an **existing** source in
  the blend. `None` when creating a new one
- `blend_data_source_key` (None | str, required): Temporary alias for a **new** source,
  exactly eight lowercase alphanumerics. `None` when addressing an existing one by id
- `report_type` (None | str, required): Report type ID, if the source supports report types
- `report_type_settings` (list[BlendedDataSourceInputReportTypeSettingsItem], required):
  Settings for the selected report type, each an `id` and a `value` that may be a string,
  an integer, a boolean, or `None`
- `display_name` (str | Unset): Display name of the source. Defaults upstream to the data
  source's own name
- `data_source_settings` (list[BlendedDataSourceInputDataSourceSettingsItem] | Unset):
  Settings applied when querying the source, same `id`/`value` shape
- `accounts` (list[BlendedDataSourceInputAccountsItem] | Unset): Accounts to query, each
  with `account_id`, `account_name`, `group_name`, `data_source_username`, and
  `data_source_display_username`
- `segments` (list[BlendedDataSourceInputSegmentsItem] | Unset): Segments to apply, each
  with `id` and `name`

> **The first five arguments are required but nullable, and three of them are usually
> empty.** Upstream marks them `required` *and* `nullable`: they must appear in the JSON
> even when there is nothing to say. So a create typically reads
> `blend_data_source_id=None, blend_data_source_key="abcd1234", report_type=None,
> report_type_settings=[]`. They have no defaults in the generated model, so omitting one is
> a `TypeError`, not a silently absent key.

> **Exactly one of the id and the key identifies the source.** A new source has a key and a
> `None` id; an existing one has an id and a `None` key. Field and join references in the
> same request must point at whichever of the two the source was given.

**Example:**

```python
from supermetrics import (
    BlendedDataSourceInput,
    BlendedDataSourceInputAccountsItem,
    BlendedDataSourceInputDataSourceSettingsItem,
    BlendedDataSourceInputSegmentsItem,
)

# New source, named by a key for the rest of the request
new_source = BlendedDataSourceInput(
    data_source_id="GA4",
    blend_data_source_id=None,
    blend_data_source_key="abcd1234",
    report_type=None,
    report_type_settings=[],
    display_name="Google Analytics 4",
    data_source_settings=[
        BlendedDataSourceInputDataSourceSettingsItem(id="currency", value="EUR"),
        BlendedDataSourceInputDataSourceSettingsItem(id="row_limit", value=1000),
        BlendedDataSourceInputDataSourceSettingsItem(id="include_empty", value=False),
        BlendedDataSourceInputDataSourceSettingsItem(id="timezone", value=None),
    ],
    accounts=[BlendedDataSourceInputAccountsItem(account_id="1234567890", account_name="Acme Corp")],
    segments=[BlendedDataSourceInputSegmentsItem(id="organic_traffic", name="Organic Traffic")],
)

# Existing source on an update, addressed by its id
existing_source = BlendedDataSourceInput(
    data_source_id="GAWA",
    blend_data_source_id=146715,
    blend_data_source_key=None,
    report_type=None,
    report_type_settings=[],
)
```

---

### BlendConfig

The write side of a blend's configuration, passed to `create()` and `update()`. Importable
from `supermetrics`. Every attribute is optional.

**Attributes:**

- `fields` (list[BlendField] | Unset): The blend's fields, sent as a **bare list**
- `query_table` (BlendConfigQueryTable | Unset): The primary (left-hand) source. Join blends
  only
- `joins` (list[BlendJoin] | Unset): The joins, sent as a **bare list**. Join blends only

> **Nothing here enforces the union/join distinction.** Upstream models this as one loose
> object with all three attributes optional rather than as a discriminated union, so the
> generated layer will happily send `joins` on a union blend or a `join` blend with no
> `query_table`. The API is what rejects those, with an HTTP 400.

**Example:**

```python
from supermetrics import BlendConfig, BlendConfigQueryTable, BlendField

# Union blend: fields only
union_config = BlendConfig(fields=[BlendField(blend_field_name="clicks", blend_datasource_fields=[])])

# Join blend: fields, plus a primary table and one join per other source
join_config = BlendConfig(
    fields=[BlendField(blend_field_name="clicks", blend_datasource_fields=[])],
    query_table=BlendConfigQueryTable(blend_data_source_key="abcd1234"),
    joins=[],
)
```

---

### BlendField

The write side of one blend field: the blend's own column and the per-source fields that
feed it. Importable from `supermetrics`.

**Attributes:**

- `blend_field_name` (str, required): Machine name of the field (example: `"impressions"`).
  Cannot be changed once created
- `blend_datasource_fields` (list[BlendDatasourceFieldRef], required): The per-source
  mappings, sent as a **bare list**
- `blend_field_display_name` (str | Unset): User-facing name shown in the UI

There is no way to set the field's type or data type. Upstream infers both from the mapped
source fields and returns them on [`BlendFieldOutput`](#blendfieldoutput).

**Example:**

```python
from supermetrics import BlendDatasourceFieldRef, BlendField

# A union blend maps the same logical column across every source
clicks = BlendField(
    blend_field_name="clicks",
    blend_field_display_name="Clicks",
    blend_datasource_fields=[
        BlendDatasourceFieldRef(
            datasource_field_name="Clicks", field_source="standard", blend_data_source_key="abcd1234"
        ),
        BlendDatasourceFieldRef(
            datasource_field_name="Clicks", field_source="standard", blend_data_source_key="efgh5678"
        ),
    ],
)
```

---

### BlendDatasourceFieldRef

A reference to one field inside one data source, used both in a [`BlendField`](#blendfield)
mapping and on each side of a [`BlendJoinCondition`](#blendjoincondition). Importable from
`supermetrics`.

**Attributes:**

- `datasource_field_name` (str, required): Field name as the data source defines it
  (example: `"Date"`)
- `field_source` (`"standard"` | `"transformation"` | `"data_source_account_custom"`, required):
  Where the field comes from — `"standard"` for a native field, `"transformation"` for a
  custom field, `"data_source_account_custom"` for an account-level custom field
- `blend_data_source_id` (int | None | Unset): The existing source this field comes from
- `blend_data_source_key` (None | str | Unset): The new source this field comes from, by its
  eight-character request key
- `datasource_field_display_name` (str | Unset): Display name of the field
- `datasource_field_type` (`"dim"` | `"met"` | Unset): Dimension or metric
- `datasource_field_data_type` (str | Unset): Data type of the field (example:
  `"string.time.date"`)
- `meta` (BlendDatasourceFieldRefMetaType0 | None | Unset): Free-form metadata, e.g.
  account-level overrides

> **Set the id or the key, never neither.** At least one of `blend_data_source_id` and
> `blend_data_source_key` must be non-null, and it has to match how the source itself was
> identified in `blended_data_sources`. Both default to `UNSET`, so a reference that names
> no source is constructible and is rejected upstream with a 400.

**Example:**

```python
from supermetrics import BlendDatasourceFieldRef

# On create, every source is new, so references point at keys
by_key = BlendDatasourceFieldRef(
    datasource_field_name="Date",
    field_source="standard",
    blend_data_source_key="abcd1234",
    datasource_field_type="dim",
    datasource_field_data_type="string.time.date",
)

# On update, a source that already exists is pointed at by id
by_id = BlendDatasourceFieldRef(
    datasource_field_name="Date",
    field_source="standard",
    blend_data_source_id=146715,
)
```

---

### BlendDatasourceFieldRefMetaType0

The optional `meta` object on a [`BlendDatasourceFieldRef`](#blenddatasourcefieldref).
Importable from `supermetrics`.

Upstream declares it as an open-ended object with no fixed properties, so the generated
model has **no declared attributes at all** — the contents live in `additional_properties`,
which is declared `init=False`.

> **The constructor takes no mapping.** `BlendDatasourceFieldRefMetaType0({"a": "b"})` is a
> `TypeError`. Build it empty and assign the entries, either through the item accessors or
> by replacing `additional_properties` wholesale — the same shape as
> [`LookupStepMap`](#lookupstepmap).

On the read side, `meta` is parsed by a try/except cascade: a JSON `null` becomes `None` and
an object becomes a `BlendDatasourceFieldRefOutputMetaType0`, again with everything in
`.additional_properties`.

**Example:**

```python
from supermetrics import BlendDatasourceFieldRef, BlendDatasourceFieldRefMetaType0

meta = BlendDatasourceFieldRefMetaType0()
meta["account_id"] = "1234567890"

ref = BlendDatasourceFieldRef(
    datasource_field_name="Custom Conversion",
    field_source="data_source_account_custom",
    blend_data_source_key="abcd1234",
    meta=meta,
)
```

---

### BlendJoin

One join between the primary table and another source, in a join blend's
[`BlendConfig`](#blendconfig). Importable from `supermetrics`. All three attributes are
required.

**Attributes:**

- `join_table` (BlendJoinJoinTable, required): The source being joined in
- `type_` (`"inner"` | `"left"` | `"right"` | `"full outer"`, required): Join type.
  Serializes to `"type"`
- `conditions` (list[BlendJoinCondition], required): How the two sources are matched, sent
  as a **bare list**

A join blend needs one `BlendJoin` per source beyond the primary table. Union blends have
none, and sending one is an upstream 400.

**Example:**

```python
from supermetrics import BlendDatasourceFieldRef, BlendJoin, BlendJoinCondition, BlendJoinJoinTable

join = BlendJoin(
    join_table=BlendJoinJoinTable(blend_data_source_key="efgh5678"),
    type_="left",
    conditions=[
        BlendJoinCondition(
            operator="=",
            left=BlendDatasourceFieldRef(
                datasource_field_name="Date", field_source="standard", blend_data_source_key="abcd1234"
            ),
            right=BlendDatasourceFieldRef(
                datasource_field_name="Date", field_source="standard", blend_data_source_key="efgh5678"
            ),
        )
    ],
)
```

---

### BlendJoinCondition

One equality between a field on each side of a [`BlendJoin`](#blendjoin). Importable from
`supermetrics`. All three attributes are required.

**Attributes:**

- `operator` (`"="`, required): Comparison operator. `"="` is the only value upstream
  accepts
- `left` (BlendDatasourceFieldRef, required): The field on the primary table
- `right` (BlendDatasourceFieldRef, required): The field on the joined table

Both sides are full [`BlendDatasourceFieldRef`](#blenddatasourcefieldref) objects, so each
names its own source by id or by key.

**Example:**

```python
from supermetrics import BlendDatasourceFieldRef, BlendJoinCondition

condition = BlendJoinCondition(
    operator="=",
    left=BlendDatasourceFieldRef(
        datasource_field_name="Campaign ID", field_source="standard", blend_data_source_key="abcd1234"
    ),
    right=BlendDatasourceFieldRef(
        datasource_field_name="Campaign ID", field_source="standard", blend_data_source_key="efgh5678"
    ),
)
```

---

### BlendJoinJoinTable

Names the source on the right-hand side of a [`BlendJoin`](#blendjoin). Importable from
`supermetrics`. Both attributes are optional, but one of them has to be set.

**Attributes:**

- `blend_data_source_id` (int | None | Unset): The existing source being joined in
- `blend_data_source_key` (None | str | Unset): The new source being joined in, by its
  eight-character request key

**Example:**

```python
from supermetrics import BlendJoinJoinTable

on_create = BlendJoinJoinTable(blend_data_source_key="efgh5678")
on_update = BlendJoinJoinTable(blend_data_source_id=146715)
```

---

### BlendConfigQueryTable

Names the primary (left-hand) source of a join blend, at `config.query_table`. Importable
from `supermetrics`. Both attributes are optional, but one of them has to be set.

**Attributes:**

- `blend_data_source_id` (int | None | Unset): The existing source used as the primary table
- `blend_data_source_key` (None | str | Unset): The new source used as the primary table, by
  its eight-character request key

Union blends leave `config.query_table` out entirely, and it comes back `Unset` on the read
side rather than `None`.

**Example:**

```python
from supermetrics import BlendConfig, BlendConfigQueryTable, BlendField

config = BlendConfig(
    query_table=BlendConfigQueryTable(blend_data_source_key="abcd1234"),
    joins=[],
    fields=[BlendField(blend_field_name="clicks", blend_datasource_fields=[])],
)
```

---

## Exceptions

All exceptions inherit from `SupermetricsError`.

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

> **Behaviour change:** `AuthenticationError` and `ValidationError` are still importable and
> are now aliases of `SupermetricsAuthError` and `SupermetricsValidationError` — which are
> **subclasses** of `APIError`. An `except APIError` clause placed **before**
> `except AuthenticationError` now matches authentication errors first and leaves the later
> clause unreachable. Order the specific classes before `APIError`.
> `except SupermetricsError` is unaffected.
>
> ```python
> from supermetrics import APIError, SupermetricsAuthError, SupermetricsRateLimitError
>
> try:
>     logins = client.logins.list()
> except SupermetricsAuthError:
>     ...  # 401 only
> except SupermetricsRateLimitError:
>     ...  # 429 only
> except APIError:
>     ...  # everything else at the HTTP layer
> ```

---

### SupermetricsError

Base exception for all SDK errors.

**Attributes:**

- `message` (str): Human-readable error description
- `status_code` (int | None): HTTP status code
- `endpoint` (str | None): API endpoint that was called
- `response_body` (str | None): Raw response body

**Example:**

```python
from supermetrics import SupermetricsError

try:
    client.accounts.list(ds_id="GAWA")
except SupermetricsError as e:
    print(f"Error: {e.message}")
    print(f"Status: {e.status_code}")
    print(f"Endpoint: {e.endpoint}")
```

---

### SupermetricsClientError

Raised for client-side configuration and validation errors, detected locally before any HTTP
request is made. Also inherits from `ValueError`, so existing code that catches `ValueError`
around client construction keeps working.

**Common Causes:**
- No credential, or more than one credential, passed to a client constructor
- An empty credential, or one containing a newline or non-ASCII character
- An `async def` token provider passed to the synchronous client
- A token provider that returns something other than a string
- `with_raw_response` used on a call that issued no HTTP request

**Example:**

```python
from supermetrics import SupermetricsClient, SupermetricsClientError

try:
    client = SupermetricsClient()  # no credential supplied
except SupermetricsClientError as e:
    print(f"Configuration problem: {e.message}")
```

---

### NetworkError

Raised for network-level failures, before any HTTP response is received. Has no
`status_code` for that reason.

**Common Causes:**
- Connection timeout
- Connection refused
- DNS resolution failure
- SSL/TLS errors

**Example:**

```python
from supermetrics import NetworkError, SupermetricsClient

try:
    client = SupermetricsClient(api_key="key", timeout=1.0)
    client.login_links.list()
except NetworkError as e:
    print(f"Network error: {e.message}")
```

---

### SupermetricsAPIError

Alias: `APIError`. Base class for every HTTP-level error (4xx and 5xx). Catching it also
catches all of the status-specific subclasses below.

**Attributes:**

- `message` (str): Human-readable error description
- `status_code` (int | None): HTTP status code
- `endpoint` (str | None): API endpoint that was called
- `response_body` (str | None): Raw response body
- `headers` (httpx.Headers | None): Response headers, when available
- `error_code` (str | None): Machine-readable upstream error code, e.g.
  `"ACCESS_TOKEN_INVALID"` or `"TRANSFER_NOT_FOUND"`
- `details` (dict | None): Structured error details from the response payload
- `raw_response` (httpx.Response | None): The underlying response. Its `.request.headers`
  still contains `Authorization`, so avoid dumping it wholesale into logs

**Properties:**

- `error_message` (str): Alias of `message`, matching the Supermetrics error payload naming
- `retry_after` (int | None): `Retry-After` in seconds, or `None` when the header is absent
  or holds an HTTP-date
- `request_id` (str | None): `X-Request-Id` from the response headers
- `span_id` (str | None): `X-Span-Id` from the response headers

**Example:**

```python
from supermetrics import APIError

try:
    client.logins.get("nonexistent_id")
except APIError as e:
    print(f"{e.status_code} {e.error_code}: {e.error_message}")
    print(f"Request ID: {e.request_id}")
```

---

### SupermetricsAuthError

Alias: `AuthenticationError`. Raised when authentication fails (HTTP 401).

**Common Causes:**
- Invalid, expired, or revoked credential
- A token that lacks the required audience

A 401 carries the upstream OAuth code in `error_code`, so a caller can tell "refresh and
retry" apart from "this credential will never work".

**Example:**

```python
from supermetrics import SupermetricsAuthError

try:
    logins = client.logins.list()
except SupermetricsAuthError as e:
    if e.error_code in ("ACCESS_TOKEN_INVALID", "ACCESS_TOKEN_EXPIRED"):
        credentials.refresh()
        logins = client.logins.list()
    else:
        raise
```

---

### SupermetricsForbiddenError

Raised when the caller is authenticated but not permitted (HTTP 403). Typically the token
lacks the required scope, or the account has no access to the requested team or resource.

**Example:**

```python
from supermetrics import SupermetricsForbiddenError

try:
    client.datasource_details.get(team_id=12345, data_source_id="GAWA")
except SupermetricsForbiddenError as e:
    print(f"Missing permission: {e.error_message}")
```

---

### SupermetricsNotFoundError

Raised when the requested resource does not exist (HTTP 404).

**Example:**

```python
from supermetrics import SupermetricsNotFoundError

try:
    client.logins.get("nonexistent_id")
except SupermetricsNotFoundError:
    print("Login not found")
```

---

### SupermetricsValidationError

Alias: `ValidationError`. Raised when request validation fails (HTTP 400 or 422).

**Common Causes:**
- Missing required parameters
- Invalid parameter values
- Incorrect parameter types

**Example:**

```python
from supermetrics import SupermetricsValidationError

try:
    client.accounts.list(ds_id="")  # Invalid empty ds_id
except SupermetricsValidationError as e:
    print(f"Validation failed: {e.error_message}")
    print(f"Details: {e.details}")
```

---

### SupermetricsRateLimitError

Raised when the API rate limit is exceeded (HTTP 429). Use `retry_after` to find out how
long to wait.

**Example:**

```python
import time

from supermetrics import SupermetricsRateLimitError

try:
    accounts = client.accounts.list(ds_id="GAWA")
except SupermetricsRateLimitError as e:
    time.sleep(e.retry_after or 30)
    accounts = client.accounts.list(ds_id="GAWA")
```

---

### SupermetricsServerError

Raised when the API reports a server-side failure (HTTP 5xx).

**Example:**

```python
from supermetrics import SupermetricsServerError

try:
    client.queries.get_results(query_id="query_abc123")
except SupermetricsServerError as e:
    print(f"Upstream failure {e.status_code}, span {e.span_id}")
```

---

## Type Utilities

### TokenProvider

Type alias for the credential callable accepted by `SupermetricsClient`:
`Callable[[], str]`. It is invoked once per request, so a long-lived client can follow a
short-lived token without discarding its connection pool.

**Example:**

```python
import os

from supermetrics import SupermetricsClient, TokenProvider


def read_token() -> str:
    return os.environ["SUPERMETRICS_TOKEN"]


provider: TokenProvider = read_token
client = SupermetricsClient(token_provider=provider)
```

---

### AsyncTokenProvider

Type alias for the credential callable accepted by `SupermetricsAsyncClient`:
`Callable[[], Awaitable[str]] | Callable[[], str]`. A coroutine function is awaited; a plain
callable is used as-is. An `async def` provider passed to the **synchronous** client is
rejected at construction time rather than failing on the first request.

**Example:**

```python
import os

from supermetrics import AsyncTokenProvider, SupermetricsAsyncClient


async def fetch_token() -> str:
    return os.environ["SUPERMETRICS_TOKEN"]


provider: AsyncTokenProvider = fetch_token
client = SupermetricsAsyncClient(token_provider=provider)
```

---

### UNSET and Unset

Sentinel value to distinguish between `None` and unset optional fields.

**Example:**

```python
from supermetrics._generated.supermetrics_api_client.types import UNSET

link = client.login_links.get(link_id="abc123")

# Check if field is set
if link.description is not UNSET:
    print(f"Description: {link.description}")
else:
    print("No description provided")
```
