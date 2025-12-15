"""
Example: Using Supermetrics SDK Accounts Resource

This example demonstrates how to use the Accounts resource introduced in SDK v1.6
to discover available data source accounts for querying.

Installation:
    pip install supermetrics-sdk

Setup:
    Get your API key from: https://supermetrics.com/account/api
    Set it as an environment variable: export SUPERMETRICS_API_KEY=your_api_key
"""

import os
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
    """Basic synchronous example using context manager."""

    # Get API key from environment variable
    api_key = os.getenv("SUPERMETRICS_API_KEY")
    if not api_key:
        raise ValueError("Please set SUPERMETRICS_API_KEY environment variable")

    # Create client using context manager (recommended)
    with SupermetricsClient(api_key=api_key) as client:

        # Example 1: List all accounts for a data source
        print("\n=== Listing All Accounts for Google Analytics 4 ===")
        accounts = client.accounts.list(ds_id="GA4")

        print(f"Found {len(accounts)} accounts:")
        for account in accounts:
            group = f" ({account.group_name})" if account.group_name else ""
            print(f"  - {account.account_name}{group}")
            print(f"    ID: {account.account_id}")

        # Example 2: List accounts for a specific login
        print("\n=== Listing Accounts for Specific Login ===")
        # First, get a login username
        logins = client.logins.list()
        if logins:
            username = logins[0].username
            print(f"Getting accounts for: {username}")

            accounts = client.accounts.list(
                ds_id="GA4",
                login_usernames=username
            )
            print(f"Found {len(accounts)} accounts for this login:")
            for account in accounts:
                print(f"  - {account.account_name} (ID: {account.account_id})")


def advanced_sync_example():
    """Advanced example with filtering and organization."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Advanced Filtering: Multiple Logins ===")

        # Get accounts for multiple login usernames
        logins = client.logins.list()

        if len(logins) >= 2:
            usernames = [logins[0].username, logins[1].username]
            print(f"Getting accounts for: {', '.join(usernames)}")

            accounts = client.accounts.list(
                ds_id="GA4",
                login_usernames=usernames
            )

            print(f"Found {len(accounts)} accounts across {len(usernames)} logins")


def organize_accounts_by_group():
    """Example: Organize accounts by group name."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Accounts Organized by Group ===")

        # Get all accounts for a data source
        accounts = client.accounts.list(ds_id="GA4")

        # Group accounts by group_name
        by_group = {}
        for account in accounts:
            group = account.group_name if account.group_name else "Ungrouped"
            if group not in by_group:
                by_group[group] = []
            by_group[group].append(account)

        # Display grouped accounts
        for group_name, group_accounts in by_group.items():
            print(f"\n{group_name}:")
            for account in group_accounts:
                print(f"  - {account.account_name} (ID: {account.account_id})")


def find_account_by_name():
    """Example: Search for an account by name."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Finding Account by Name ===")

        # Get all accounts
        accounts = client.accounts.list(ds_id="GA4")

        # Search for account by partial name match
        search_term = "Demo"  # Replace with actual search term
        matching_accounts = [
            acc for acc in accounts
            if search_term.lower() in acc.account_name.lower()
        ]

        if matching_accounts:
            print(f"Found {len(matching_accounts)} accounts matching '{search_term}':")
            for account in matching_accounts:
                print(f"  - {account.account_name}")
                print(f"    ID: {account.account_id}")
        else:
            print(f"No accounts found matching '{search_term}'")


async def async_example():
    """Asynchronous example for concurrent operations."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    # Use async client for better performance
    async with SupermetricsAsyncClient(api_key=api_key) as client:

        print("\n=== Async: Getting Accounts for Multiple Data Sources ===")

        # Get accounts for multiple data sources concurrently
        data_sources = ["GA4", "google_ads", "facebook_ads"]

        # Create tasks for all data sources
        tasks = [
            client.accounts.list(ds_id=ds_id)
            for ds_id in data_sources
        ]

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Display results
        for ds_id, result in zip(data_sources, results):
            if isinstance(result, Exception):
                print(f"\n{ds_id}: Error - {result}")
            else:
                print(f"\n{ds_id}: {len(result)} accounts")
                for account in result[:3]:  # Show first 3
                    print(f"  - {account.account_name}")
                if len(result) > 3:
                    print(f"  ... and {len(result) - 3} more")


def real_world_workflow():
    """Real-world workflow: Complete authentication and account discovery flow."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Complete Workflow: From Login to Accounts ===")

        # Step 1: Create login link
        print("\nStep 1: Create login link")
        link = client.login_links.create(
            ds_id="GA4",
            description="Complete workflow example"
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

            print(f"\nFound {len(accounts)} accounts:")
            for account in accounts:
                print(f"  - {account.account_name}")
                print(f"    Account ID: {account.account_id}")
                if account.group_name:
                    print(f"    Group: {account.group_name}")

            # Step 5: Ready to query!
            if accounts:
                print(f"\n✓ Setup complete!")
                print(f"  You can now query data using:")
                print(f"    - Login username: {login.username}")
                print(f"    - Account ID: {accounts[0].account_id}")
                print(f"\n  Example query:")
                print(f"    client.queries.execute(")
                print(f"        ds_user='{login.username}',")
                print(f"        ds_accounts=['{accounts[0].account_id}'],")
                print(f"        fields=['date', 'sessions'],")
                print(f"        date_range_preset='last_30_days'")
                print(f"    )")

        else:
            print(f"  Status: {link_status.status_code}")
            print("  User hasn't completed authentication yet")

        # Cleanup
        client.login_links.close(link.link_id)
        print("\nLogin link closed")


def cache_example():
    """Example: Using cache to speed up account retrieval."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Using Cache for Faster Retrieval ===")

        # First call: Fetches fresh data
        print("First call (fresh data):")
        accounts = client.accounts.list(ds_id="GA4")
        print(f"  Retrieved {len(accounts)} accounts")

        # Second call: Uses cache if available (max 60 minutes old)
        print("\nSecond call (cached data, max 60 min old):")
        accounts = client.accounts.list(
            ds_id="GA4",
            cache_minutes=60
        )
        print(f"  Retrieved {len(accounts)} accounts (from cache)")

        # Force fresh data: Set cache_minutes=0
        print("\nForce fresh data (cache_minutes=0):")
        accounts = client.accounts.list(
            ds_id="GA4",
            cache_minutes=0
        )
        print(f"  Retrieved {len(accounts)} accounts (fresh)")


def multi_data_source_example():
    """Example: Get accounts across multiple data sources."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Accounts Across Multiple Data Sources ===")

        data_sources = {
            "GA4": "Google Analytics 4",
            "google_ads": "Google Ads",
            "facebook_ads": "Facebook Ads",
        }

        for ds_id, ds_name in data_sources.items():
            try:
                accounts = client.accounts.list(ds_id=ds_id)
                print(f"\n{ds_name}:")
                print(f"  Total accounts: {len(accounts)}")

                # Show first few accounts
                for account in accounts[:3]:
                    print(f"  - {account.account_name} (ID: {account.account_id})")

                if len(accounts) > 3:
                    print(f"  ... and {len(accounts) - 3} more")

            except AuthenticationError as e:
                print(f"\n{ds_name}: Authentication failed - {e.message}")
            except ValidationError as e:
                print(f"\n{ds_name}: Invalid parameters - {e.message}")
            except APIError as e:
                print(f"\n{ds_name}: API error - {e.message} (status: {e.status_code})")
            except NetworkError as e:
                print(f"\n{ds_name}: Network error - {e.message}")


if __name__ == "__main__":
    print("=" * 60)
    print("Supermetrics SDK - Accounts Resource Examples")
    print("=" * 60)

    # Check for API key
    if not os.getenv("SUPERMETRICS_API_KEY"):
        print("\n⚠️  ERROR: SUPERMETRICS_API_KEY environment variable not set")
        print("\nTo run these examples:")
        print("  1. Get your API key from https://supermetrics.com/account/api")
        print("  2. Set it: export SUPERMETRICS_API_KEY=your_api_key")
        print("  3. Run this script again: python accounts_example.py")
        exit(1)

    # Run examples
    try:
        # Basic synchronous example
        basic_sync_example()

        # Advanced filtering
        print("\n" + "=" * 60)
        print("Advanced Filtering Example")
        print("=" * 60)
        advanced_sync_example()

        # Organize by group
        print("\n" + "=" * 60)
        print("Organize Accounts by Group")
        print("=" * 60)
        organize_accounts_by_group()

        # Search by name
        print("\n" + "=" * 60)
        print("Find Account by Name")
        print("=" * 60)
        find_account_by_name()

        # Cache example
        print("\n" + "=" * 60)
        print("Cache Example")
        print("=" * 60)
        cache_example()

        # Multi data source
        print("\n" + "=" * 60)
        print("Multi-Data Source Example")
        print("=" * 60)
        multi_data_source_example()

        # Async example
        print("\n" + "=" * 60)
        print("Asynchronous Example (Concurrent)")
        print("=" * 60)
        asyncio.run(async_example())

        # Real-world workflow
        # Note: Uncomment to run (requires user interaction)
        # print("\n" + "=" * 60)
        # print("Complete Real-World Workflow")
        # print("=" * 60)
        # real_world_workflow()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("  1. Installed the SDK: pip install supermetrics-sdk")
        print("  2. Set a valid API key: export SUPERMETRICS_API_KEY=your_key")
        print("  3. Created login links and authenticated with data sources")


