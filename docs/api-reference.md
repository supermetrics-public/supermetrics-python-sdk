# API Reference

Complete reference for the supermetrics Python SDK public API.

## Client Classes

### SupermetricsClient

Synchronous client for blocking I/O operations.

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(
    api_key="your_api_key",
    user_agent=None,
    custom_headers=None,
    timeout=30.0,
    base_url="https://api.supermetrics.com"
)
```

**Parameters:**

- `api_key` (str, required): Your Supermetrics API key
- `user_agent` (str, optional): Custom User-Agent header
- `custom_headers` (dict, optional): Additional HTTP headers for all requests
- `timeout` (float, optional): Request timeout in seconds (default: 30.0)
- `base_url` (str, optional): API base URL

**Resource Properties:**

- `login_links`: Access to LoginLinksResource
- `logins`: Access to LoginsResource
- `accounts`: Access to AccountsResource
- `queries`: Access to QueriesResource
- `backfills`: Access to BackfillsResource
- `datasource_details`: Access to DatasourceDetailsResource

**Methods:**

- `close()`: Close client and release resources
- `__enter__()`: Context manager entry
- `__exit__()`: Context manager exit

**Example:**

```python
# Using context manager (recommended)
with SupermetricsClient(api_key="your_key") as client:
    accounts = client.accounts.list(ds_id="GAWA")

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
    user_agent=None,
    custom_headers=None,
    timeout=30.0,
    base_url="https://api.supermetrics.com"
)
```

**Parameters:** Same as SupermetricsClient

**Resource Properties:**

- `login_links`: Access to LoginLinksAsyncResource
- `logins`: Access to LoginsAsyncResource
- `accounts`: Access to AccountsAsyncResource
- `queries`: Access to QueriesAsyncResource
- `backfills`: Access to BackfillsAsyncResource
- `datasource_details`: Access to DatasourceDetailsAsyncResource

**Methods:**

- `async close()`: Close client and release resources
- `async __aenter__()`: Async context manager entry
- `async __aexit__()`: Async context manager exit

**Example:**

```python
import asyncio
from supermetrics import SupermetricsAsyncClient

async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        accounts = await client.accounts.list(ds_id="GAWA")
        print(f"Found {len(accounts)} accounts")

asyncio.run(main())
```

---

## Resources

### LoginLinksResource

Manage data source authentication links.

#### create()

Create a login link for data source authentication.

```python
link = client.login_links.create(
    ds_id="GAWA",
    description="My Analytics Connection",
    expiry_time=None,
    **kwargs
)
```

**Parameters:**

- `ds_id` (str, required): Data source ID (e.g., "GAWA", "google_ads", "facebook_ads")
- `description` (str, optional): Internal description for the link
- `expiry_time` (datetime, optional): Link expiry time (default: 24 hours from creation)
- `**kwargs`: Additional parameters:
  - `require_username` (str): Required username for authentication
  - `redirect_url` (str): Custom redirect URL after authentication

**Returns:** `LoginLink` object

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

**Example:**

```python
link = client.login_links.create(
    ds_id="GAWA",
    description="Analytics Connection for Q1 Report"
)
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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`, `ValueError` (if not found)

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
accounts = client.accounts.list(
    ds_id="GAWA",
    login_usernames=None,
    cache_minutes=None
)
```

**Parameters:**

- `ds_id` (str, required): Data source ID (e.g., "GAWA", "google_ads", "facebook_ads")
- `login_usernames` (str | list[str], optional): Username(s) to filter accounts
- `cache_minutes` (int, optional): Maximum age of cached data in minutes

**Returns:** Flattened list of account objects with `account_id`, `account_name`, `group_name`

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

**Example:**

```python
# List all GAWA accounts
accounts = client.accounts.list(ds_id="GAWA")

# Filter by specific username
accounts = client.accounts.list(
    ds_id="GAWA",
    login_usernames="analytics@company.com"
)

# Filter by multiple usernames
accounts = client.accounts.list(
    ds_id="google_ads",
    login_usernames=["user1@company.com", "user2@company.com"]
)

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
    **kwargs
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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

**Example:**

```python
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users", "Pageviews"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    max_rows=10000,
    filter_="Sessions > 100"
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

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

**Example:**

```python
# Execute query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-12-31"
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
    team_id=12345,
    transfer_id=456789,
    range_start=date(2024, 1, 1),
    range_end=date(2024, 1, 31)
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `transfer_id` (int, required): Unique identifier of the transfer
- `range_start` (date, required): Start date of the backfill range (inclusive)
- `range_end` (date, required): End date of the backfill range (inclusive)

**Returns:** `Backfill` object with status `"CREATED"`

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

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
        team_id=12345,
        transfer_id=456789,
        range_start=date(2024, 1, 1),
        range_end=date(2024, 1, 31)
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

**Raises:** `AuthenticationError`, `APIError` (404 if not found), `NetworkError`

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

**Raises:** `AuthenticationError`, `APIError` (404 if no backfill has ever been created), `NetworkError`

**Example:**

```python
try:
    latest = client.backfills.get_latest(team_id=12345, transfer_id=456789)
    print(f"Latest backfill: {latest.transfer_backfill_id}")
    print(f"Status: {latest.status}")
    print(f"Range: {latest.range_start_date} — {latest.range_end_date}")
except APIError as e:
    if e.status_code == 404:
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

**Raises:** `AuthenticationError`, `APIError`, `NetworkError`

**Example:**

```python
backfills = client.backfills.list_incomplete(team_id=12345)

if not backfills:
    print("No incomplete backfills")
else:
    for backfill in backfills:
        print(f"[{backfill.status}] Backfill {backfill.transfer_backfill_id} "
              f"(transfer {backfill.transfer_id}): "
              f"{backfill.transfer_runs_completed}/{backfill.transfer_runs_total} runs done")
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

**Raises:** `AuthenticationError`, `ValidationError` (if backfill is already in a final state), `APIError` (404 if not found), `NetworkError`

**Notes:**
- Only backfills with status `CREATED`, `SCHEDULED`, `RUNNING`, or `FAILED` can be cancelled
- Pending/queued transfer runs are cancelled immediately
- Transfer runs already in progress will complete
- The backfill record is retained with status `"CANCELLED"` — it is not deleted

**Example:**

```python
from supermetrics import ValidationError, APIError

try:
    cancelled = client.backfills.cancel(team_id=12345, backfill_id=67890)
    print(f"Status: {cancelled.status}")        # "CANCELLED"
    print(f"Ended at: {cancelled.end_time}")
except ValidationError:
    print("Cannot cancel — backfill is already in a final state")
except APIError as e:
    if e.status_code == 404:
        print("Backfill not found")
```

**Async usage** (all methods above are also available on `BackfillsAsyncResource`):

```python
import asyncio
from datetime import date
from supermetrics import SupermetricsAsyncClient

async def main():
    async with SupermetricsAsyncClient(
        api_key="your_key",
        base_url="https://dts-api.supermetrics.com/v1"
    ) as client:
        backfill = await client.backfills.create(
            team_id=12345,
            transfer_id=456789,
            range_start=date(2024, 1, 1),
            range_end=date(2024, 1, 31)
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
    sm_app_id=None   # optional
)
```

**Parameters:**

- `team_id` (int, required): Unique identifier of the team
- `data_source_id` (str, required): Data source ID (e.g., `"GAWA"`, `"AW"`, `"SA360"`)
- `sm_app_id` (str, optional): Value forwarded as the `Sm-App-Id` request header

**Returns:** `DatasourceDetails` object

**Raises:** `AuthenticationError`, `ValidationError`, `APIError`, `NetworkError`

**Example:**

```python
from supermetrics import SupermetricsClient, APIError

with SupermetricsClient(api_key="your_key") as client:
    details = client.datasource_details.get(team_id=12345, data_source_id="GAWA")

    print(f"Name:    {details.name}")
    print(f"Status:  {details.status}")
    print(f"Premium: {details.is_premium}")

    if details.report_types:
        for rt in details.report_types:
            print(f"  Report type: {rt.id} — {rt.name}")
```

**Async usage:**

```python
import asyncio
from supermetrics import SupermetricsAsyncClient

async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        details = await client.datasource_details.get(
            team_id=12345,
            data_source_id="GAWA"
        )
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
- `categories` (list[DatasourceDetailsCategoriesItem]): Category tags (e.g., `["ANALYTICS"]`)
- `products` (list[str]): Products where this datasource is available (e.g., `["API", "DS", "DWH"]`)
- `status` (DatasourceDetailsStatus): Release status — `Released`, `Beta`, `Deprecated`, etc.
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
- `report_types` (list[DatasourceReportType]): Available report types
- `common_settings` (list[DatasourceSetting]): Settings shared across all report types

**Example:**

```python
details = client.datasource_details.get(team_id=12345, data_source_id="GAWA")

print(f"ID:      {details.id}")
print(f"Name:    {details.name}")
print(f"Status:  {details.status}")
print(f"Premium: {details.is_premium}")
print(f"Auth required: {details.is_authentication_required}")

for rt in (details.report_types or []):
    print(f"  Report type: {rt.id} — {rt.name}")
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
  - `status_code` (str): Query status ("pending", "success", etc.)
  - `fields` (list): Field definitions
  - `query` (dict): Query parameters
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
    headers = [field["field_id"] for field in result.meta.fields]
    print(f"Columns: {headers}")

    for row in result.data:
        print(row)
```

---

## Exceptions

All exceptions inherit from `SupermetricsError` base class.

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

### AuthenticationError

Raised when API authentication fails (HTTP 401).

**Common Causes:**
- Invalid API key
- Expired API key
- Revoked API key

**Example:**

```python
from supermetrics import AuthenticationError

try:
    client = SupermetricsClient(api_key="invalid_key")
    client.login_links.list()
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
```

---

### ValidationError

Raised when request validation fails (HTTP 400, 422).

**Common Causes:**
- Missing required parameters
- Invalid parameter values
- Incorrect parameter types

**Example:**

```python
from supermetrics import ValidationError

try:
    client.accounts.list(ds_id="")  # Invalid empty ds_id
except ValidationError as e:
    print(f"Validation failed: {e.message}")
```

---

### APIError

Raised for API-level errors (HTTP 403, 404, 429, 5xx).

**Common Causes:**
- Resource not found (404)
- Forbidden/insufficient permissions (403)
- Rate limit exceeded (429)
- Server errors (500, 503)

**Example:**

```python
from supermetrics import APIError

try:
    client.logins.get("nonexistent_id")
except APIError as e:
    if e.status_code == 404:
        print("Login not found")
    elif e.status_code == 429:
        print("Rate limited")
```

---

### NetworkError

Raised for network-level failures.

**Common Causes:**
- Connection timeout
- Connection refused
- DNS resolution failure
- Network connectivity issues

**Example:**

```python
from supermetrics import NetworkError

try:
    client = SupermetricsClient(api_key="key", timeout=1.0)
    client.login_links.list()
except NetworkError as e:
    print(f"Network error: {e.message}")
```

---

## Type Utilities

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
