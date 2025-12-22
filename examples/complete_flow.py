"""
Complete Onboarding Flow - Synchronous Example

This example demonstrates the complete workflow from client initialization
through authentication, account discovery, and data querying.

Installation:
    pip install supermetrics-sdk

Setup:
    Get your API key from: https://supermetrics.com/account/api
    Set it as an environment variable: export SUPERMETRICS_API_KEY=your_api_key

Usage:
    python examples/complete_flow.py

What to expect:
    1. Client initialized
    2. Login link created (you'll need to visit the URL in a browser)
    3. Script polls for authentication completion
    4. Login details retrieved
    5. Available accounts discovered
    6. Data query executed
    7. Results displayed

Note:
    This example uses polling which is suitable for POC/testing but not
    recommended for production. Use webhooks or redirect URLs for production.
"""

import traceback
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
from getpass import getpass

from supermetrics import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsClient,
    ValidationError,
)
load_dotenv()

def main() -> None:
    """Execute complete onboarding workflow."""
    # Set your API key as environment variable:
    # export SUPERMETRICS_API_KEY="your_api_key_here"

    # api_key = os.getenv("SUPERMETRICS_API_KEY")
    # if not api_key:
    #     raise ValueError("SUPERMETRICS_API_KEY environment variable is required")

    api_key = getpass("Enter your API key: ")
    print("API key received.")

    try:
        # Step 1: Initialize the Supermetrics client
        # The client provides access to all SDK resources with type safety
        client = SupermetricsClient(api_key=api_key)
        print("✓ Client initialized")

        # Step 2: Create a login link for Google Analytics 4
        # This generates a URL that the user visits to authenticate their datasource account
        # The link ID is used to check status and retrieve login credentials

        ds_id = input("Enter the data source ID (ds_id): ").strip()
        if not ds_id:
            raise ValueError("ds_id is required")

        link = client.login_links.create(ds_id=ds_id, description="Complete Flow POC Example")
        print(f"✓ Login link created: {link.login_url}")
        print(f"  Link ID: {link.link_id}")
        print(f"  Status: {link.status_code}")
        print("\nPlease visit the login URL to authenticate your data source account.")
        print("After authentication, this script will continue automatically.\n")

        # Step 3: Wait for user to complete authentication
        # In production, you'd use webhooks or have user return to your app
        # For POC, we poll the login link status every 5 seconds
        max_wait = 300  # 5 minutes
        wait_interval = 5  # 5 seconds
        elapsed = 0

        while elapsed < max_wait:
            link = client.login_links.get(link_id=link.link_id)

            if link.login_id:
                print(f"✓ Authentication complete! Login ID: {link.login_id}")
                break

            print(f"  Waiting for authentication... ({elapsed}s elapsed)")
            time.sleep(wait_interval)
            elapsed += wait_interval
        else:
            raise TimeoutError("Authentication did not complete within 5 minutes")

        # Step 4: Retrieve login details
        # The login contains the username needed to discover accounts
        login = client.logins.get(login_id=link.login_id)
        print("✓ Login details retrieved:")
        print(f"  Username: {login.username}")
        print(f"  Data Source: {login.ds_info.name if login.ds_info else 'N/A'}")
        print(f"  Login ID: {login.login_id}")

        # Step 5: List available accounts for this login
        accounts = client.accounts.list(ds_id=ds_id, login_usernames=login.username)
        print(f"\n✓ Found {len(accounts)} accounts:")
        for account in accounts[:3]:  # Show first 3
            print(f"  - {account.account_name} (ID: {account.account_id})")

        if not accounts:
            raise ValueError("No accounts found for this login")

        # Use the first account for our query
        selected_account = accounts[0]

        # Step 6: Execute a data query
        # Get last 7 days of sessions and users data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)

        # Ask fields interactively until blank
        fields = []
        while True:
            field = input("Enter field name (blank to finish): ").strip()
            if field == "":
                break
            fields.append(field)

        if not fields:
            raise ValueError("At least one field is required")


        result = client.queries.execute(
            ds_id=ds_id,
            ds_accounts=[selected_account.account_id],
            # fields=["Date", "impressions"],
            fields=fields,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )

        print("\n✓ Query executed:")
        print(f"  Status: {getattr(result.meta, 'status_code', 'N/A')}")
        print(f"  Request ID: {getattr(result.meta, 'request_id', 'N/A')}")

        # Step 7: Handle async query results (if query status is "pending")
        # Large date ranges or complex queries may process asynchronously
        if result.meta and hasattr(result.meta, "status_code") and result.meta.status_code == "pending":
            print(f"  Query is processing... Request ID: {result.meta.request_id}")

            # Poll for results every 2 seconds for up to 1 minute
            max_poll = 60  # 1 minute
            poll_interval = 2  # 2 seconds
            elapsed = 0

            while elapsed < max_poll:
                result = client.queries.get_results(query_id=result.meta.request_id)

                if result.meta and result.meta.status_code != "pending":
                    print("✓ Query completed!")
                    break

                print(f"  Polling... ({elapsed}s)")
                time.sleep(poll_interval)
                elapsed += poll_interval
            else:
                raise TimeoutError("Query did not complete within 1 minute")

        # Step 8: Display query results
        # Results contain metadata about the query and the actual data rows
        print(f"\n{'=' * 60}")
        print("QUERY RESULTS")
        print(f"{'=' * 60}\n")

        if hasattr(result, 'data') and isinstance(result.data, list) and len(result.data) > 0:
            print(f"Retrieved {len(result.data)} rows")
            print("\nSample data (first 5 rows):")
            for i, row in enumerate(result.data[:5]):
                print(f"  Row {i + 1}: {row}")

            if len(result.data) > 5:
                print(f"  ... and {len(result.data) - 5} more rows")

            # Show result metadata
            if result.meta:
                print("\nMetadata:")
                print(f"  Request ID: {result.meta.request_id}")
                print(f"  Status: {result.meta.status_code}")
        else:
            print("No data returned")

        print("\n✅ POC complete! All steps executed successfully.")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e.message}")
        print("   Please check your API key is valid")
        print(f"   Status: {e.status_code}")

    except ValidationError as e:
        print(f"❌ Validation error: {e.message}")
        print(f"   Status: {e.status_code}")
        print(f"   Endpoint: {e.endpoint}")
        print("   Please check your parameters (ds_id, account_id, fields, dates)")

    except APIError as e:
        print(f"❌ API error: {e.message}")
        print(f"   Status: {e.status_code}")
        print("   The Supermetrics API returned an error")

    except NetworkError as e:
        print(f"❌ Network error: {e.message}")
        print("   Please check your internet connection")

    except Exception as e:
        print(f"❌ Unexpected error: {e!s}")
        traceback.print_exception(type(e), e, e.__traceback__)


if __name__ == "__main__":
    main()
