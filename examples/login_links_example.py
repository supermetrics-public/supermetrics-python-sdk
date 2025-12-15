"""
Example: Using Supermetrics SDK Login Links Feature

This example demonstrates how to use the Login Links resource introduced in SDK v1.4
to create and manage OAuth authentication links for data sources.

Installation:
    pip install supermetrics-sdk

Setup:
    Get your API key from: https://supermetrics.com/account/api
    Set it as an environment variable: export SUPERMETRICS_API_KEY=your_api_key
"""

import os
import asyncio
from datetime import datetime, timedelta, UTC

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

        # Example 1: Create a login link for Google Analytics 4
        print("\n=== Creating a Login Link ===")
        link = client.login_links.create(
            ds_id="GA4",
            description="Q4 Marketing Analytics Setup"
        )

        print(f"Login Link Created!")
        print(f"  Link ID: {link.link_id}")
        print(f"  Data Source: {link.ds_name}")
        print(f"  Status: {link.status_code}")
        print(f"  Visit this URL to authenticate: {link.login_url}")
        print(f"  Expires at: {link.expires_at}")

        # Save the link_id to check status later
        link_id = link.link_id

        # Example 2: Get login link details
        print("\n=== Checking Link Status ===")
        link_details = client.login_links.get(link_id)

        if link_details.login_id:
            print(f"✓ Authentication completed!")
            print(f"  Authenticated as: {link_details.login_username}")
            print(f"  Login ID: {link_details.login_id}")
        else:
            print(f"Status: {link_details.status_code}")
            print(f"Waiting for user to authenticate...")

        # Example 3: List all login links
        print("\n=== All Login Links ===")
        all_links = client.login_links.list()

        print(f"Found {len(all_links)} login links:")
        for lnk in all_links:
            print(f"  - {lnk.ds_name} ({lnk.link_id}): {lnk.status_code}")

        # Example 4: Close/expire a login link
        print("\n=== Closing Login Link ===")
        client.login_links.close(link_id)
        print(f"✓ Login link {link_id} has been closed")


def advanced_sync_example():
    """Advanced example with custom configuration and error handling."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    # Create client with custom configuration
    client = SupermetricsClient(
        api_key=api_key,
        timeout=60.0,  # Increase timeout to 60 seconds
        custom_headers={"X-App-Name": "My Analytics Dashboard"}
    )

    try:
        # Create login link with custom expiry time (expires in 1 hour)
        custom_expiry = datetime.now(UTC) + timedelta(hours=1)

        link = client.login_links.create(
            ds_id="google_ads",
            description="Google Ads Campaign Performance",
            expiry_time=custom_expiry,
            # Optional: require specific username
            require_username="user@company.com"
        )

        print(f"Created login link: {link.login_url}")
        print(f"Will expire at: {link.expires_at}")

        # Store the link_id in your database to track authentication status
        # Later, poll this to check if user completed authentication

    except AuthenticationError as e:
        print(f"Authentication failed: {e.message}")
        print(f"Please check your API key (status: {e.status_code})")
    except ValidationError as e:
        print(f"Invalid parameters: {e.message}")
        print(f"Check that ds_id and other parameters are correct (status: {e.status_code})")
    except NetworkError as e:
        print(f"Network error: {e.message}")
        print(f"Check your internet connection or try again later")
    except APIError as e:
        print(f"API error: {e.message}")
        print(f"Status: {e.status_code}, Endpoint: {e.endpoint}")

    finally:
        # Always close the client when done
        client.close()


async def async_example():
    """Asynchronous example for concurrent operations."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    # Use async client for better performance in production
    async with SupermetricsAsyncClient(api_key=api_key) as client:

        # Create multiple login links concurrently
        print("\n=== Creating Multiple Login Links (Async) ===")

        data_sources = [
            ("GA4", "Google Analytics"),
            ("google_ads", "Google Ads"),
            ("facebook_ads", "Facebook Ads"),
        ]

        # Create all links concurrently
        tasks = [
            client.login_links.create(
                ds_id=ds_id,
                description=name
            )
            for ds_id, name in data_sources
        ]

        links = await asyncio.gather(*tasks)

        print(f"Created {len(links)} login links:")
        for link in links:
            print(f"  - {link.ds_name}: {link.login_url}")

        # List all links asynchronously
        all_links = await client.login_links.list()
        print(f"\nTotal login links in account: {len(all_links)}")


def real_world_workflow():
    """Real-world workflow: Create link, wait for auth, use login_id."""

    api_key = os.getenv("SUPERMETRICS_API_KEY")

    with SupermetricsClient(api_key=api_key) as client:

        # Step 1: Create a login link for your user
        print("Step 1: Creating login link...")
        link = client.login_links.create(
            ds_id="GA4",
            description="Customer onboarding - Acme Corp"
        )

        # Step 2: Show the login URL to your user (in your app's UI)
        print(f"\nStep 2: Send this URL to your user:")
        print(f"  {link.login_url}")

        # Store link_id in your database associated with the user
        link_id = link.link_id
        print(f"\nStored link_id in database: {link_id}")

        # Step 3: Poll the link status to detect when auth is complete
        # (In production, you might use webhooks instead)
        print("\nStep 3: Waiting for user to authenticate...")
        print("(In this example, user would visit the URL and complete OAuth)")

        # Check status
        link_status = client.login_links.get(link_id)

        if link_status.login_id:
            # Step 4: Authentication complete! Use login_id for API queries
            print(f"\n✓ Authentication successful!")
            print(f"  Login ID: {link_status.login_id}")
            print(f"  Username: {link_status.login_username}")
            print(f"\nYou can now use this login_id to query data from {link_status.ds_name}")

            # Store login_id in your database - use it for data queries
            # Example: client.queries.create(login_id=link_status.login_id, ...)
        else:
            print(f"\nStatus: {link_status.status_code}")
            print("User hasn't completed authentication yet")


if __name__ == "__main__":
    print("=" * 60)
    print("Supermetrics SDK - Login Links Examples")
    print("=" * 60)

    # Check for API key
    if not os.getenv("SUPERMETRICS_API_KEY"):
        print("\n⚠️  ERROR: SUPERMETRICS_API_KEY environment variable not set")
        print("\nTo run these examples:")
        print("  1. Get your API key from https://supermetrics.com/account/api")
        print("  2. Set it: export SUPERMETRICS_API_KEY=your_api_key")
        print("  3. Run this script again: python login_links_example.py")
        exit(1)

    # Run examples
    try:
        # Basic synchronous example
        basic_sync_example()

        # Advanced configuration
        print("\n" + "=" * 60)
        print("Advanced Example with Custom Configuration")
        print("=" * 60)
        advanced_sync_example()

        # Real-world workflow
        print("\n" + "=" * 60)
        print("Real-World Workflow Example")
        print("=" * 60)
        real_world_workflow()

        # Async example
        print("\n" + "=" * 60)
        print("Asynchronous Example (Concurrent Operations)")
        print("=" * 60)
        asyncio.run(async_example())

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("  1. Installed the SDK: pip install supermetrics-sdk")
        print("  2. Set a valid API key: export SUPERMETRICS_API_KEY=your_key")
