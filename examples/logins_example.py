"""
Example: Using Supermetrics SDK Logins Resource

This example demonstrates how to use the Logins resource introduced in SDK v1.5
to retrieve login information and verify authentication completion.

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

        # Example 1: Get a login by login ID
        print("\n=== Getting Login by ID ===")
        login_id = "login_abc123"  # Replace with actual login ID
        try:
            login = client.logins.get(login_id)
            print(f"Login ID: {login.login_id}")
            print(f"Username: {login.username}")
            print(f"Data Source: {login.ds_info.ds_name if login.ds_info else 'N/A'}")
            print(f"Login Type: {login.login_type}")
            if login.auth_user_info:
                print(f"Owner: {login.auth_user_info.email}")
        except AuthenticationError as e:
            print(f"Authentication failed: {e.message}")
            print(f"Please check your API key")
        except APIError as e:
            if e.status_code == 404:
                print(f"Login not found: {e.message}")
            else:
                print(f"API error: {e.message} (status: {e.status_code})")
        except NetworkError as e:
            print(f"Network error: {e.message}")

        # Example 2: List all logins
        print("\n=== Listing All Logins ===")
        logins = client.logins.list()
        print(f"Found {len(logins)} logins:")
        for login in logins:
            ds_name = login.ds_info.ds_name if login.ds_info else "Unknown"
            print(f"  - {login.username} ({ds_name}) - ID: {login.login_id}")

        # Example 3: Get login by username
        print("\n=== Getting Login by Username ===")
        if logins:
            # Use the first login's username as an example
            username = logins[0].username
            try:
                login = client.logins.get_by_username(username)
                print(f"Found login: {login.login_id}")
                print(f"Username: {login.username}")
                print(f"Display Name: {login.display_name}")
            except ValueError as e:
                # ValueError is raised when multiple logins have the same username
                print(f"Error: {e}")
            except APIError as e:
                print(f"API error: {e.message}")
            except NetworkError as e:
                print(f"Network error: {e.message}")


def advanced_sync_example():
    """Advanced example with error handling and login verification."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Verifying Login Authentication ===")

        # List all logins and check their status
        logins = client.logins.list()

        for login in logins:
            print(f"\nLogin: {login.username}")
            print(f"  Data Source: {login.ds_info.ds_name if login.ds_info else 'N/A'}")
            print(f"  Login Type: {login.login_type}")

            # Check if login is active
            if login.revoked_time:
                print(f"  Status: ⚠️  REVOKED at {login.revoked_time}")
            elif login.expiry_time:
                print(f"  Status: ✓ Active (expires: {login.expiry_time})")
            else:
                print(f"  Status: ✓ Active")

            # Check if refreshable
            if login.is_refreshable:
                print(f"  Refresh: ✓ Auto-refreshable")

            # Check default scopes
            if login.default_scopes and login.default_scopes != UNSET:
                print(f"  Scopes: {', '.join(login.default_scopes)}")


def search_logins_example():
    """Example showing how to search and filter logins."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Searching Logins ===")

        # Get all logins
        all_logins = client.logins.list()
        print(f"Total logins: {len(all_logins)}")

        # Filter by data source
        target_ds = "GA4"
        ga4_logins = [
            login for login in all_logins
            if login.ds_info and login.ds_info.ds_id == target_ds
        ]
        print(f"\nGoogle Analytics 4 logins: {len(ga4_logins)}")
        for login in ga4_logins:
            print(f"  - {login.username} (ID: {login.login_id})")

        # Filter by login type
        oauth_logins = [
            login for login in all_logins
            if login.login_type == "oauth2"
        ]
        print(f"\nOAuth logins: {len(oauth_logins)}")

        # Find shared logins
        shared_logins = [
            login for login in all_logins
            if login.is_shared
        ]
        print(f"\nShared logins: {len(shared_logins)}")


async def async_example():
    """Asynchronous example for concurrent operations."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    # Use async client for better performance
    async with SupermetricsAsyncClient(api_key=api_key) as client:

        print("\n=== Async: Listing All Logins ===")

        # List all logins asynchronously
        logins = await client.logins.list()
        print(f"Found {len(logins)} logins")

        # Get specific logins concurrently
        if len(logins) >= 2:
            print("\n=== Async: Getting Multiple Logins Concurrently ===")

            # Get first two logins by ID concurrently
            tasks = [
                client.logins.get(logins[0].login_id),
                client.logins.get(logins[1].login_id),
            ]

            results = await asyncio.gather(*tasks)
            for login in results:
                print(f"  - {login.username} ({login.ds_info.ds_name if login.ds_info else 'N/A'})")


def real_world_workflow():
    """Real-world workflow: Check login status after creating login link."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Real-World Workflow: Verify Login After Authentication ===")

        # Step 1: Create a login link (from previous example)
        print("Step 1: Create login link for user to authenticate")
        link = client.login_links.create(
            ds_id="GA4",
            description="Example: Verify Authentication"
        )
        print(f"  Login Link Created: {link.link_id}")
        print(f"  User should visit: {link.login_url}")

        # Step 2: After user authenticates, check the link status
        print("\nStep 2: Check if authentication is complete")
        link_status = client.login_links.get(link.link_id)

        if link_status.login_id:
            print(f"  ✓ Authentication complete!")
            print(f"  Login ID: {link_status.login_id}")

            # Step 3: Get the full login details
            print("\nStep 3: Retrieve full login information")
            login = client.logins.get(link_status.login_id)

            print(f"  Username: {login.username}")
            print(f"  Display Name: {login.display_name}")
            print(f"  Data Source: {login.ds_info.ds_name if login.ds_info else 'N/A'}")

            # Step 4: You can now use this login for data queries
            print(f"\n✓ Ready to query data!")
            print(f"  Use login_id '{login.login_id}' for API queries")
            print(f"  Or use username '{login.username}' to get accounts")

        else:
            print(f"  Status: {link_status.status_code}")
            print("  User hasn't completed authentication yet")

        # Clean up: close the login link
        client.login_links.close(link.link_id)
        print("\nLogin link closed")


def list_logins_by_data_source():
    """Example: Organize logins by data source."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        print("\n=== Logins Organized by Data Source ===")

        logins = client.logins.list()

        # Group logins by data source
        by_ds = {}
        for login in logins:
            ds_name = login.ds_info.ds_name if login.ds_info else "Unknown"
            if ds_name not in by_ds:
                by_ds[ds_name] = []
            by_ds[ds_name].append(login)

        # Display grouped logins
        for ds_name, ds_logins in by_ds.items():
            print(f"\n{ds_name}:")
            for login in ds_logins:
                status = "✓" if not login.revoked_time else "⚠️ "
                print(f"  {status} {login.username} (ID: {login.login_id})")


if __name__ == "__main__":
    print("=" * 60)
    print("Supermetrics SDK - Logins Resource Examples")
    print("=" * 60)

    # Check for API key
    if not os.getenv("SUPERMETRICS_API_KEY"):
        print("\n⚠️  ERROR: SUPERMETRICS_API_KEY environment variable not set")
        print("\nTo run these examples:")
        print("  1. Get your API key from https://supermetrics.com/account/api")
        print("  2. Set it: export SUPERMETRICS_API_KEY=your_api_key")
        print("  3. Run this script again: python logins_example.py")
        exit(1)

    # Run examples
    try:
        # Basic synchronous example
        basic_sync_example()

        # Advanced example with verification
        print("\n" + "=" * 60)
        print("Advanced Example: Login Verification")
        print("=" * 60)
        advanced_sync_example()

        # Search and filter example
        print("\n" + "=" * 60)
        print("Search and Filter Logins")
        print("=" * 60)
        search_logins_example()

        # List by data source
        print("\n" + "=" * 60)
        print("Logins by Data Source")
        print("=" * 60)
        list_logins_by_data_source()

        # Async example
        print("\n" + "=" * 60)
        print("Asynchronous Example")
        print("=" * 60)
        asyncio.run(async_example())

        # Real-world workflow
        # Note: Uncomment to run (requires user interaction)
        # print("\n" + "=" * 60)
        # print("Real-World Workflow")
        # print("=" * 60)
        # real_world_workflow()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("  1. Installed the SDK: pip install supermetrics-sdk")
        print("  2. Set a valid API key: export SUPERMETRICS_API_KEY=your_key")
        print("  3. Created at least one login link and authenticated")
