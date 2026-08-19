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
