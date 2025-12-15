"""
Example: Using Supermetrics SDK Queries Resource

This example demonstrates how to use the Queries resource introduced in SDK v1.7
to execute data queries and retrieve marketing data from various data sources.

Installation:
    pip install supermetrics-sdk

Setup:
    Get your API key from: https://supermetrics.com/account/api
    Set it as an environment variable: export SUPERMETRICS_API_KEY=your_api_key
"""

import os
import time
import asyncio

from supermetrics import (
    SupermetricsClient,
    SupermetricsAsyncClient,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError,
)


def basic_sync_example():
    """Basic synchronous example of executing a query."""

    # Get API key from environment variable
    api_key = os.getenv("SUPERMETRICS_API_KEY")
    if not api_key:
        raise ValueError("Please set SUPERMETRICS_API_KEY environment variable")

    # Create client using context manager (recommended)
    with SupermetricsClient(api_key=api_key) as client:

        # Example 1: Execute a simple query
        print("\n=== Executing a Simple Query ===")
        result = client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678"],  # Replace with your account ID
            fields=["date", "sessions", "users"],
            start_date="2025-01-01",
            end_date="2025-01-31"
        )

        if result and result.meta:
            print(f"Query Status: {result.meta.status_code}")
            print(f"Request ID: {result.meta.request_id}")

            if result.data:
                print(f"Retrieved {len(result.data)} rows of data")
                # Display first few rows
                for i, row in enumerate(result.data[:3]):
                    print(f"  Row {i+1}: {row}")
                if len(result.data) > 3:
                    print(f"  ... and {len(result.data) - 3} more rows")


def query_with_all_parameters():
    """Example using all available query parameters."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Query with All Parameters ===")

        # Execute query with advanced parameters
        result = client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678", "87654321"],  # Multiple accounts
            fields=[
                "date",
                "sessions",
                "users",
                "pageviews",
                "bounceRate"
            ],
            start_date="2025-01-01",
            end_date="2025-01-31",
            # Additional optional parameters via **kwargs
            max_rows=1000,
            cache_minutes=30,
            sync_timeout=60,
            filter_="sessions>100"  # Filter results
        )

        if result and result.meta:
            print(f"Query executed successfully")
            print(f"Status: {result.meta.status_code}")

            # Display field information
            if hasattr(result.meta, 'query') and result.meta.query:
                print(f"\nQuery Configuration:")
                print(f"  Fields: {result.meta.query.fields if hasattr(result.meta.query, 'fields') else 'N/A'}")
                print(f"  Date Range: {result.meta.query.start_date} to {result.meta.query.end_date if hasattr(result.meta.query, 'start_date') else 'N/A'}")


def async_query_polling():
    """Example: Handle asynchronous queries with polling."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Async Query with Polling ===")

        # Execute query (might return pending status)
        result = client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678"],
            fields=["date", "sessions", "users"],
            start_date="2024-01-01",
            end_date="2024-12-31"  # Large date range may trigger async processing
        )

        if result and result.meta:
            print(f"Initial Status: {result.meta.status_code}")

            # If query is pending, poll for results
            if result.meta.status_code == "pending":
                print(f"Query is being processed asynchronously...")
                print(f"Request ID: {result.meta.request_id}")

                max_attempts = 10
                wait_seconds = 5

                for attempt in range(1, max_attempts + 1):
                    print(f"\nPolling attempt {attempt}/{max_attempts}...")
                    time.sleep(wait_seconds)

                    # Poll for results using the request_id
                    result = client.queries.get_results(
                        query_id=result.meta.request_id
                    )

                    if result and result.meta:
                        print(f"  Status: {result.meta.status_code}")

                        # Check if query is complete
                        if result.meta.status_code != "pending":
                            print(f"\n✓ Query completed!")
                            if result.data:
                                print(f"  Retrieved {len(result.data)} rows")
                                # Display sample data
                                for row in result.data[:3]:
                                    print(f"    {row}")
                            break
                else:
                    print(f"\n⚠️  Query still pending after {max_attempts} attempts")
                    print(f"   You can continue polling with query_id: {result.meta.request_id}")

            else:
                # Query completed immediately
                print(f"✓ Query completed immediately")
                if result.data:
                    print(f"  Retrieved {len(result.data)} rows")


def relative_date_ranges():
    """Example: Using relative date ranges."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Relative Date Ranges ===")

        # Example 1: Yesterday's data
        print("\nYesterday's data:")
        result = client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678"],
            fields=["sessions", "users"],
            start_date="yesterday",
            end_date="yesterday"
        )

        if result and result.data:
            print(f"  Retrieved {len(result.data)} rows")

        # Example 2: Last 7 days
        print("\nLast 7 days:")
        result = client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678"],
            fields=["date", "sessions"],
            start_date="7daysAgo",
            end_date="today"
        )

        if result and result.data:
            print(f"  Retrieved {len(result.data)} rows")
            for row in result.data[:7]:
                print(f"    {row}")


def multiple_data_sources():
    """Example: Query data from multiple data sources."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Querying Multiple Data Sources ===")

        data_sources = {
            "GA4": {
                "name": "Google Analytics 4",
                "accounts": ["12345678"],
                "fields": ["date", "sessions", "users"]
            },
            "google_ads": {
                "name": "Google Ads",
                "accounts": ["123-456-7890"],
                "fields": ["date", "impressions", "clicks", "cost"]
            },
            "facebook_ads": {
                "name": "Facebook Ads",
                "accounts": ["act_123456789"],
                "fields": ["date", "impressions", "clicks", "spend"]
            }
        }

        for ds_id, config in data_sources.items():
            try:
                print(f"\n{config['name']}:")
                result = client.queries.execute(
                    ds_id=ds_id,
                    ds_accounts=config["accounts"],
                    fields=config["fields"],
                    start_date="yesterday",
                    end_date="yesterday"
                )

                if result and result.meta:
                    print(f"  Status: {result.meta.status_code}")
                    if result.data:
                        print(f"  Rows: {len(result.data)}")
                        print(f"  Sample: {result.data[0] if result.data else 'No data'}")

            except AuthenticationError as e:
                print(f"  Authentication failed: {e.message}")
            except ValidationError as e:
                print(f"  Invalid parameters: {e.message}")
            except APIError as e:
                print(f"  API error: {e.message} (status: {e.status_code})")
            except NetworkError as e:
                print(f"  Network error: {e.message}")


async def async_example():
    """Asynchronous example for concurrent queries."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    # Use async client for better performance
    async with SupermetricsAsyncClient(api_key=api_key) as client:

        print("\n=== Async: Concurrent Queries for Multiple Accounts ===")

        # Query multiple accounts concurrently
        account_ids = ["12345678", "87654321", "11111111"]

        # Create tasks for all accounts
        tasks = [
            client.queries.execute(
                ds_id="GA4",
                ds_accounts=[account_id],
                fields=["sessions", "users"],
                start_date="yesterday",
                end_date="yesterday"
            )
            for account_id in account_ids
        ]

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Display results
        for account_id, result in zip(account_ids, results):
            if isinstance(result, Exception):
                print(f"\nAccount {account_id}: Error - {result}")
            elif result and result.data:
                print(f"\nAccount {account_id}:")
                print(f"  Status: {result.meta.status_code if result.meta else 'unknown'}")
                print(f"  Rows: {len(result.data)}")
                print(f"  Data: {result.data[0] if result.data else 'No data'}")


async def async_polling_workflow():
    """Async example with polling for pending queries."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    async with SupermetricsAsyncClient(api_key=api_key) as client:

        print("\n=== Async Polling Workflow ===")

        # Execute query
        result = await client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678"],
            fields=["date", "sessions", "users"],
            start_date="2024-01-01",
            end_date="2024-12-31"
        )

        if result and result.meta:
            print(f"Initial Status: {result.meta.status_code}")

            # Poll if pending
            if result.meta.status_code == "pending":
                query_id = result.meta.request_id
                print(f"Query pending, polling with ID: {query_id}")

                for attempt in range(1, 11):
                    await asyncio.sleep(5)  # Wait 5 seconds
                    print(f"  Polling attempt {attempt}/10...")

                    result = await client.queries.get_results(query_id=query_id)

                    if result and result.meta and result.meta.status_code != "pending":
                        print(f"✓ Query completed!")
                        if result.data:
                            print(f"  Retrieved {len(result.data)} rows")
                        break
                else:
                    print("Query still pending after 10 attempts")


def complete_workflow():
    """Real-world workflow: From authentication to querying data."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Complete Workflow: Authentication to Data Query ===")

        # Step 1: Create login link
        print("\nStep 1: Create login link")
        link = client.login_links.create(
            ds_id="GA4",
            description="Complete query workflow example"
        )
        print(f"  Login link created: {link.link_id}")
        print(f"  User should visit: {link.login_url}")

        # Step 2: Check authentication (in real app, poll or use webhook)
        print("\nStep 2: Check authentication status")
        link_status = client.login_links.get(link.link_id)

        if link_status.login_id:
            print(f"  ✓ User authenticated!")

            # Step 3: Get login details
            print("\nStep 3: Get login information")
            login = client.logins.get(link_status.login_id)
            print(f"  Login username: {login.username}")

            # Step 4: Get available accounts
            print("\nStep 4: Discover available accounts")
            accounts = client.accounts.list(
                ds_id="GA4",
                login_usernames=login.username
            )

            if accounts:
                print(f"  Found {len(accounts)} accounts:")
                for account in accounts[:3]:
                    print(f"    - {account.account_name} (ID: {account.account_id})")

                # Step 5: Execute query!
                print("\nStep 5: Execute data query")
                account_ids = [acc.account_id for acc in accounts[:2]]  # Use first 2 accounts

                result = client.queries.execute(
                    ds_id="GA4",
                    ds_accounts=account_ids,
                    fields=["date", "sessions", "users", "pageviews"],
                    start_date="yesterday",
                    end_date="yesterday"
                )

                if result and result.meta:
                    print(f"  ✓ Query executed successfully!")
                    print(f"  Status: {result.meta.status_code}")
                    print(f"  Request ID: {result.meta.request_id}")

                    if result.data:
                        print(f"  Retrieved {len(result.data)} rows")
                        print(f"\n  Sample data:")
                        for row in result.data[:3]:
                            print(f"    {row}")

                    print(f"\n✓ Complete workflow successful!")

            else:
                print("  No accounts found for this login")

        else:
            print(f"  Status: {link_status.status_code}")
            print("  User hasn't completed authentication yet")

        # Cleanup
        client.login_links.close(link.link_id)
        print("\nLogin link closed")


def data_analysis_example():
    """Example: Simple data analysis on query results."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Data Analysis Example ===")

        # Get last 7 days of data
        result = client.queries.execute(
            ds_id="GA4",
            ds_accounts=["12345678"],
            fields=["date", "sessions", "users"],
            start_date="7daysAgo",
            end_date="yesterday"
        )

        if result and result.data:
            print(f"Analyzing {len(result.data)} days of data...\n")

            # Calculate totals and averages
            # Assuming data structure: [date, sessions, users]
            total_sessions = 0
            total_users = 0

            for row in result.data:
                if len(row) >= 3:
                    # Convert to int, handling potential string values
                    sessions = int(row[1]) if row[1] else 0
                    users = int(row[2]) if row[2] else 0

                    total_sessions += sessions
                    total_users += users

            avg_sessions = total_sessions / len(result.data) if result.data else 0
            avg_users = total_users / len(result.data) if result.data else 0

            print(f"Summary Statistics:")
            print(f"  Total Sessions: {total_sessions:,}")
            print(f"  Total Users: {total_users:,}")
            print(f"  Average Sessions/Day: {avg_sessions:.1f}")
            print(f"  Average Users/Day: {avg_users:.1f}")

            # Find best performing day
            if result.data:
                best_day = max(result.data, key=lambda row: int(row[1]) if len(row) >= 2 and row[1] else 0)
                print(f"\nBest Performing Day:")
                print(f"  Date: {best_day[0]}")
                print(f"  Sessions: {best_day[1]}")
                print(f"  Users: {best_day[2] if len(best_day) >= 3 else 'N/A'}")


if __name__ == "__main__":
    print("=" * 60)
    print("Supermetrics SDK - Queries Resource Examples")
    print("=" * 60)

    # Check for API key
    if not os.getenv("SUPERMETRICS_API_KEY"):
        print("\n⚠️  ERROR: SUPERMETRICS_API_KEY environment variable not set")
        print("\nTo run these examples:")
        print("  1. Get your API key from https://supermetrics.com/account/api")
        print("  2. Set it: export SUPERMETRICS_API_KEY=your_api_key")
        print("  3. Run this script again: python queries_example.py")
        exit(1)

    # Run examples
    try:
        # Basic synchronous example
        basic_sync_example()

        # Query with all parameters
        print("\n" + "=" * 60)
        print("Query with All Parameters")
        print("=" * 60)
        query_with_all_parameters()

        # Async query polling
        print("\n" + "=" * 60)
        print("Async Query with Polling")
        print("=" * 60)
        async_query_polling()

        # Relative date ranges
        print("\n" + "=" * 60)
        print("Relative Date Ranges")
        print("=" * 60)
        relative_date_ranges()

        # Multiple data sources
        print("\n" + "=" * 60)
        print("Multiple Data Sources")
        print("=" * 60)
        multiple_data_sources()

        # Data analysis
        print("\n" + "=" * 60)
        print("Data Analysis Example")
        print("=" * 60)
        data_analysis_example()

        # Async examples
        print("\n" + "=" * 60)
        print("Asynchronous Example (Concurrent Queries)")
        print("=" * 60)
        asyncio.run(async_example())

        print("\n" + "=" * 60)
        print("Async Polling Workflow")
        print("=" * 60)
        asyncio.run(async_polling_workflow())

        # Complete workflow
        # Note: Uncomment to run (requires user interaction)
        # print("\n" + "=" * 60)
        # print("Complete Real-World Workflow")
        # print("=" * 60)
        # complete_workflow()

    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e.message}")
        print("\nMake sure you have:")
        print("  1. Set a valid API key: export SUPERMETRICS_API_KEY=your_key")
        print("  2. Your API key hasn't expired")
    except ValidationError as e:
        print(f"\n❌ Validation Error: {e.message}")
        print(f"Status: {e.status_code}")
        print("\nMake sure you have:")
        print("  1. Valid date ranges and parameters")
        print("  2. Correct field names for the data source")
        print("  3. Valid account IDs")
    except NetworkError as e:
        print(f"\n❌ Network Error: {e.message}")
        print("\nMake sure you have an active internet connection")
    except APIError as e:
        print(f"\n❌ API Error: {e.message}")
        print(f"Status: {e.status_code}")
        print("\nMake sure you have:")
        print("  1. Authenticated accounts with available data")
        print("  2. Created login links and authenticated with data sources")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\nMake sure you have:")
        print("  1. Installed the SDK: pip install supermetrics-sdk")
        print("  2. Configured accounts for querying")
