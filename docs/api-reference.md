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

> **Important:** Backfill endpoints are served from a separate base URL. You must initialize the client with `base_url="https://dts-api.supermetrics.com/v1"` when using any backfill operations:
>
> ```python
> client = SupermetricsClient(
>     api_key="your_api_key",
>     base_url="https://dts-api.supermetrics.com/v1"
> )
> ```

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
    async with SupermetricsAsyncClient(api_key="your_key", base_url="https://dts-api.supermetrics.com/v1") as client:
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
