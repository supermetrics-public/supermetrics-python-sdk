# User Guide

Comprehensive guide to using the Supermetrics Python SDK for integrating with the Supermetrics API.

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Workflow](#basic-workflow)
- [Authentication](#authentication)
- [Querying Data](#querying-data)
- [Async Support](#async-support)
- [Best Practices](#best-practices)

---

## Getting Started

### Installation

Install the SDK using pip:

```bash
pip install supermetrics
```

### Quick Start

```python
from supermetrics import SupermetricsClient

# Initialize client with your API key
client = SupermetricsClient(api_key="your_api_key_here")

# Create a login link for Google Analytics 4
link = client.login_links.create(
    ds_id="GAWA",
    description="My Analytics Connection"
)

print(f"Visit this URL to authenticate: {link.login_url}")
```

---

## Basic Workflow

The typical workflow for using the Supermetrics API involves:

1. **Create a login link** - Generate an authentication URL for your data source
2. **User authenticates** - User visits the URL and grants access
3. **Retrieve login credentials** - Get the authenticated login details
4. **List accounts** - Fetch available accounts for the data source
5. **Execute queries** - Retrieve marketing data from the accounts

### Complete Example

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="your_api_key")

# Step 1: Create login link
link = client.login_links.create(
    ds_id="GAWA",
    description="Q1 Analytics Report"
)
print(f"Please authenticate at: {link.login_url}")

# Wait for user to authenticate
input("Press Enter after you've completed authentication...")

# Step 2: Check authentication status
updated_link = client.login_links.get(link.link_id)
if not updated_link.login_id:
    print("Authentication not completed yet")
    exit()

# Step 3: Get login details
login = client.logins.get(updated_link.login_id)
print(f"Authenticated as: {login.username}")

# Step 4: List available accounts
accounts = client.accounts.list(
    ds_id="GAWA",
    login_usernames=login.username
)
print(f"Found {len(accounts)} accounts:")
for account in accounts:
    print(f"  - {account.account_name}")

# Step 5: Execute query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=[accounts[0].account_id],
    fields=["Date", "Sessions", "Users", "Pageviews"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)

if result and result.data:
    print(f"\nRetrieved {len(result.data)} rows")
    # Print first 5 rows
    for row in result.data[:5]:
        print(row)
```

---

## Authentication

### Creating Login Links

Login links are URLs that users visit to authenticate with data sources.

```python
# Basic login link
link = client.login_links.create(ds_id="GAWA")

# With description and custom expiry
from datetime import datetime, timedelta

expiry = datetime.now() + timedelta(hours=2)
link = client.login_links.create(
    ds_id="GAWA",
    description="Analytics for Marketing Dashboard",
    expiry_time=expiry
)

# With required username (force user to authenticate with specific account)
link = client.login_links.create(
    ds_id="google_ads",
    require_username="marketing@company.com"
)

print(f"Link ID: {link.link_id}")
print(f"Authentication URL: {link.login_url}")
print(f"Expires: {link.expiry_time}")
```

### Checking Authentication Status

Poll the link status to see when authentication completes:

```python
import time

link = client.login_links.create(ds_id="GAWA")
print(f"Visit: {link.login_url}")

# Poll every 5 seconds
while True:
    updated_link = client.login_links.get(link.link_id)

    if updated_link.login_id:
        print(f"Authentication successful!")
        print(f"Login ID: {updated_link.login_id}")
        print(f"Username: {updated_link.login_username}")
        break

    print(f"Status: {updated_link.status_code}")
    time.sleep(5)
```

### Managing Logins

```python
# List all logins
logins = client.logins.list()
for login in logins:
    ds_name = login.ds_info.ds_name if login.ds_info else "Unknown"
    print(f"{ds_name}: {login.username}")

# Get specific login
login = client.logins.get(login_id="login_abc123")
print(f"Username: {login.username}")
print(f"Display Name: {login.display_name}")

# Find login by username
try:
    login = client.logins.get_by_username("analytics@company.com")
    print(f"Found: {login.login_id}")
except ValueError:
    print("Login not found")
```

### Closing Login Links

Expire login links to prevent further authentication:

```python
client.login_links.close(link_id="link_abc123")
print("Link closed successfully")
```

---

## Querying Data

### Listing Accounts

Before querying, you need to know which accounts are available:

```python
# List all GAWA accounts
accounts = client.accounts.list(ds_id="GAWA")

# Filter by username
accounts = client.accounts.list(
    ds_id="GAWA",
    login_usernames="analytics@company.com"
)

# Filter by multiple usernames
accounts = client.accounts.list(
    ds_id="google_ads",
    login_usernames=["user1@company.com", "user2@company.com"]
)

# Use cached data (faster)
accounts = client.accounts.list(
    ds_id="GAWA",
    cache_minutes=60  # Use cached data up to 1 hour old
)

# Print account details
for account in accounts:
    print(f"ID: {account.account_id}")
    print(f"Name: {account.account_name}")
    print(f"Group: {account.group_name}")
    print("---")
```

### Executing Queries

Retrieve marketing data from your data sources:

```python
# Basic query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# With filters
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users", "BounceRate"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    filter_="Sessions > 100"
)

# With segments
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    ds_segments=["segment_abc123"]
)

# With row limit
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    max_rows=10000
)

# Use cached results
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    cache_minutes=30  # Use cached results up to 30 minutes old
)
```

### Processing Query Results

```python
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-01-07"
)

# Check if query succeeded
if result and result.data:
    # Get field names
    fields = [field["field_id"] for field in result.meta.fields]
    print(f"Columns: {fields}")

    # Get row count
    print(f"Total rows: {len(result.data)}")

    # Print all rows
    for row in result.data:
        print(row)

    # Convert to dictionary format
    for row in result.data:
        row_dict = dict(zip(fields, row))
        print(row_dict)
        # {'Date': '2024-01-01', 'Sessions': '1250', 'Users': '980'}

    # Convert to pandas DataFrame
    import pandas as pd
    df = pd.DataFrame(result.data, columns=fields)
    print(df.head())
```

### Handling Async Queries

Large queries may process asynchronously:

```python
import time

# Execute query
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions", "Users"],
    start_date="2024-01-01",
    end_date="2024-12-31"  # Large date range
)

# Check if async
if result and result.meta and result.meta.status_code == "pending":
    print(f"Query is processing asynchronously")
    print(f"Request ID: {result.meta.request_id}")

    # Poll for results
    max_attempts = 12  # 1 minute total (5 sec * 12)
    for attempt in range(max_attempts):
        time.sleep(5)

        result = client.queries.get_results(query_id=result.meta.request_id)

        if result and result.meta:
            status = result.meta.status_code
            print(f"Attempt {attempt + 1}: Status = {status}")

            if status == "success":
                print(f"Query completed! Rows: {len(result.data)}")
                break
            elif status == "error":
                print("Query failed")
                break
    else:
        print("Query timeout - still processing")
```

### Relative Dates

Use relative date strings for dynamic queries:

```python
# Today
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="today",
    end_date="today"
)

# Yesterday
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="yesterday",
    end_date="yesterday"
)

# Last 7 days
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="7daysago",
    end_date="today"
)

# Last 30 days
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="30daysago",
    end_date="yesterday"
)

# This month
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="first_day_of_month",
    end_date="today"
)

# Last month
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="first_day_of_last_month",
    end_date="last_day_of_last_month"
)
```

---

## Async Support

For production applications requiring high concurrency, use the async client:

### Basic Async Usage

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

### Concurrent Queries

Execute multiple queries in parallel:

```python
import asyncio
from supermetrics import SupermetricsAsyncClient

async def fetch_data_for_account(client, account_id, start_date, end_date):
    """Fetch data for a single account."""
    result = await client.queries.execute(
        ds_id="GAWA",
        ds_accounts=[account_id],
        fields=["Date", "Sessions", "Users"],
        start_date=start_date,
        end_date=end_date
    )
    return account_id, result

async def main():
    async with SupermetricsAsyncClient(api_key="your_key") as client:
        # Get accounts
        accounts = await client.accounts.list(ds_id="GAWA")
        account_ids = [acc.account_id for acc in accounts[:5]]  # First 5

        # Execute queries concurrently
        tasks = [
            fetch_data_for_account(client, acc_id, "2024-01-01", "2024-01-31")
            for acc_id in account_ids
        ]

        results = await asyncio.gather(*tasks)

        # Process results
        for account_id, result in results:
            if result and result.data:
                print(f"Account {account_id}: {len(result.data)} rows")

asyncio.run(main())
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from supermetrics import SupermetricsAsyncClient, APIError

app = FastAPI()

# Initialize client once at startup
@app.on_event("startup")
async def startup():
    app.state.client = SupermetricsAsyncClient(api_key="your_key")

@app.on_event("shutdown")
async def shutdown():
    await app.state.client.close()

@app.get("/accounts/{ds_id}")
async def get_accounts(ds_id: str):
    """Get accounts for a data source."""
    try:
        accounts = await app.state.client.accounts.list(ds_id=ds_id)
        return {
            "count": len(accounts),
            "accounts": [
                {
                    "id": acc.account_id,
                    "name": acc.account_name,
                    "group": acc.group_name
                }
                for acc in accounts
            ]
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)

@app.get("/query/{ds_id}")
async def query_data(
    ds_id: str,
    account_id: str,
    start_date: str,
    end_date: str
):
    """Execute a query for an account."""
    try:
        result = await app.state.client.queries.execute(
            ds_id=ds_id,
            ds_accounts=[account_id],
            fields=["Date", "Sessions", "Users"],
            start_date=start_date,
            end_date=end_date
        )

        if result and result.data:
            return {
                "status": result.meta.status_code if result.meta else None,
                "rows": len(result.data),
                "data": result.data
            }
        else:
            return {"status": "no_data", "rows": 0, "data": []}

    except APIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
```

---

## Best Practices

### 1. Use Context Managers

Always use context managers to ensure proper resource cleanup:

```python
# Good
with SupermetricsClient(api_key="your_key") as client:
    accounts = client.accounts.list(ds_id="GAWA")

# Also good for async
async with SupermetricsAsyncClient(api_key="your_key") as client:
    accounts = await client.accounts.list(ds_id="GAWA")
```

### 2. Handle Errors Gracefully

Catch specific exceptions for better error handling:

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
except AuthenticationError:
    print("Invalid API key - check configuration")
except ValidationError as e:
    print(f"Invalid parameters: {e.message}")
except APIError as e:
    if e.status_code == 429:
        print("Rate limited - retry later")
    elif e.status_code == 404:
        print("Resource not found")
    else:
        print(f"API error: {e.message}")
except NetworkError:
    print("Network error - check connectivity")
```

### 3. Cache Results When Possible

Use `cache_minutes` to avoid redundant API calls:

```python
# Cache account list for 1 hour
accounts = client.accounts.list(
    ds_id="GAWA",
    cache_minutes=60
)

# Cache query results for 30 minutes
result = client.queries.execute(
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    cache_minutes=30
)
```

### 4. Use Async for Concurrent Operations

For multiple queries, async is much faster:

```python
# Slow: Sequential sync queries (10 seconds total)
for account_id in account_ids:
    result = client.queries.execute(...)  # 1 second each

# Fast: Concurrent async queries (1 second total)
tasks = [
    client.queries.execute(...)
    for account_id in account_ids
]
results = await asyncio.gather(*tasks)
```

### 5. Store API Keys Securely

Never hardcode API keys. Use environment variables:

```python
import os
from supermetrics import SupermetricsClient

api_key = os.getenv("SUPERMETRICS_API_KEY")
if not api_key:
    raise ValueError("SUPERMETRICS_API_KEY environment variable required")

client = SupermetricsClient(api_key=api_key)
```

### 6. Implement Retry Logic for Rate Limits

```python
import time
from supermetrics import SupermetricsClient, APIError

def query_with_retry(client, max_retries=3, **query_params):
    """Execute query with exponential backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            return client.queries.execute(**query_params)
        except APIError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

client = SupermetricsClient(api_key="your_key")
result = query_with_retry(
    client,
    ds_id="GAWA",
    ds_accounts=["123456789"],
    fields=["Date", "Sessions"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### 7. Validate Data Source Fields

Different data sources support different fields. Check data source documentation:

```python
# GAWA example
ga4_fields = ["Date", "Sessions", "Users", "Pageviews", "BounceRate"]

# Google Ads example
google_ads_fields = ["Date", "Clicks", "Impressions", "Cost", "Conversions"]

# Facebook Ads example
facebook_ads_fields = ["Date", "Impressions", "Clicks", "Spend", "Purchases"]

# Always refer to Supermetrics field documentation for your data source
```

### 8. Close Unused Login Links

Clean up expired or unused login links:

```python
# List all links
links = client.login_links.list()

# Close expired or unused links
for link in links:
    if link.status_code in ["expired", "closed"] or not link.login_id:
        client.login_links.close(link.link_id)
        print(f"Closed link: {link.link_id}")
```

---

## Common Data Sources

### Google Analytics 4 (GAWA)

```python
ds_id = "GAWA"
fields = ["Date", "Sessions", "Users", "Pageviews", "BounceRate"]
```

### Google Ads

```python
ds_id = "google_ads"
fields = ["Date", "Clicks", "Impressions", "Cost", "Conversions"]
```

### Facebook Ads

```python
ds_id = "facebook_ads"
fields = ["Date", "Impressions", "Clicks", "Spend", "Purchases"]
```

### LinkedIn Ads

```python
ds_id = "linkedin_ads"
fields = ["Date", "Impressions", "Clicks", "Spend", "Conversions"]
```

### Twitter Ads

```python
ds_id = "twitter_ads"
fields = ["Date", "Impressions", "Clicks", "Spend"]
```

For complete field lists, refer to the [Supermetrics field documentation](https://supermetrics.com/docs/product-fields/).

---

## Next Steps

- Review the [API Reference](api-reference.md) for detailed method documentation
- Check out [Error Handling](error-handling.md) for robust error management
- Explore the [examples/](../examples/) directory for complete working code
