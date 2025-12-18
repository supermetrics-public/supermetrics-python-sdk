"""
Complete Onboarding Flow - Asynchronous Example

This example demonstrates the complete workflow using the async client for
better performance and concurrency in production applications.

Installation:
    pip install supermetrics-sdk

Setup:
    Get your API key from: https://supermetrics.com/account/api
    Set it as an environment variable: export SUPERMETRICS_API_KEY=your_api_key

Usage:
    python examples/async_flow.py

What to expect:
    Same flow as complete_flow.py but using async/await for non-blocking operations.
    This approach is recommended for production applications that need to handle
    multiple concurrent requests or integrate with async frameworks (FastAPI, etc.).

Benefits of async:
    - Non-blocking I/O for better resource utilization
    - Handle multiple operations concurrently
    - Better integration with async frameworks
    - Improved performance for batch operations
"""

import traceback
import asyncio
import os
from datetime import datetime, timedelta

from supermetrics import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsAsyncClient,
    ValidationError,
)


async def main() -> None:
    """Execute complete onboarding workflow asynchronously."""
    # Set your API key as environment variable:
    # export SUPERMETRICS_API_KEY="your_api_key_here"

    api_key = os.getenv("SUPERMETRICS_API_KEY")
    if not api_key:
        raise ValueError("SUPERMETRICS_API_KEY environment variable is required")

    try:
        # Step 1: Initialize async client
        # Using async context manager ensures proper cleanup
        async with SupermetricsAsyncClient(api_key=api_key) as client:
            print("✓ Async client initialized")

            # Step 2: Create login link
            # Same as sync version but with await
            ds_id = input("Enter the data source ID (ds_id): ").strip()
            if not ds_id:
                raise ValueError("ds_id is required")
                
            link = await client.login_links.create(ds_id=ds_id, description="Async Flow POC Example")
            print(f"✓ Login link created: {link.login_url}")
            print(f"  Link ID: {link.link_id}")
            print(f"  Status: {link.status_code}")
            print("\nPlease visit the login URL to authenticate your data source account.")
            print("After authentication, this script will continue automatically.\n")

            # Step 3: Wait for authentication completion
            # Using asyncio.sleep() instead of time.sleep() to avoid blocking
            max_wait = 300  # 5 minutes
            wait_interval = 5  # 5 seconds
            elapsed = 0

            while elapsed < max_wait:
                link = await client.login_links.get(link_id=link.link_id)

                if link.login_id:
                    print(f"✓ Authentication complete! Login ID: {link.login_id}")
                    break

                print(f"  Waiting for authentication... ({elapsed}s elapsed)")
                await asyncio.sleep(wait_interval)  # Non-blocking sleep
                elapsed += wait_interval
            else:
                raise TimeoutError("Authentication did not complete within 5 minutes")

            # Step 4: Retrieve login details
            login = await client.logins.get(login_id=link.login_id)
            print("✓ Login details retrieved:")
            print(f"  Username: {login.username}")
            print(f"  Data Source: {login.ds_info.name if login.ds_info else 'N/A'}")
            print(f"  Login ID: {login.login_id}")

            # Step 5: List available accounts
            accounts = await client.accounts.list(ds_id=ds_id, login_usernames=login.username)
            print(f"\n✓ Found {len(accounts)} accounts:")
            for account in accounts[:3]:  # Show first 3
                print(f"  - {account.account_name} (ID: {account.account_id})")

            if not accounts:
                raise ValueError("No accounts found for this login")

            selected_account = accounts[0]

            # Step 6: Execute query
            # Async queries are particularly useful when querying multiple accounts
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=7)

            result = await client.queries.execute(
                ds_id=ds_id,
                ds_accounts=[selected_account.account_id],
                fields=["Date", "Sessions", "Users"],
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )

            print("\n✓ Query executed:")
            print(f"  Status: {result.meta.status_code if result.meta else 'N/A'}")
            print(f"  Request ID: {result.meta.request_id if result.meta else 'N/A'}")

            # Step 7: Handle async query results
            if result.meta and hasattr(result.meta, "status_code") and result.meta.status_code == "pending":
                print(f"  Query is processing... Request ID: {result.meta.request_id}")

                max_poll = 60  # 1 minute
                poll_interval = 2  # 2 seconds
                elapsed = 0

                while elapsed < max_poll:
                    result = await client.queries.get_results(query_id=result.meta.request_id)

                    if result.meta and result.meta.status_code != "pending":
                        print("✓ Query completed!")
                        break

                    print(f"  Polling... ({elapsed}s)")
                    await asyncio.sleep(poll_interval)  # Non-blocking
                    elapsed += poll_interval
                else:
                    raise TimeoutError("Query did not complete within 1 minute")

            # Step 8: Display results
            print(f"\n{'=' * 60}")
            print("QUERY RESULTS")
            print(f"{'=' * 60}\n")

            if hasattr(result, 'error'):
                raise Exception(result.error.description)
            elif hasattr(result, 'data') and isinstance(result.data, list) and len(result.data) > 0:
                print(f"Retrieved {len(result.data)} rows")
                print("\nSample data (first 5 rows):")
                for i, row in enumerate(result.data[:5]):
                    print(f"  Row {i + 1}: {row}")

                if len(result.data) > 5:
                    print(f"  ... and {len(result.data) - 5} more rows")

                if result.meta:
                    print("\nMetadata:")
                    print(f"  Request ID: {result.meta.request_id}")
                    print(f"  Status: {result.meta.status_code}")
            else:
                print("No data returned")

            print("\n✅ POC complete! All steps executed successfully with async.")
            print("\nAsync benefits demonstrated:")
            print("  - Non-blocking I/O operations (await instead of blocking calls)")
            print("  - Context manager ensures proper resource cleanup")
            print("  - Ready for concurrent operations and async frameworks")

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
    # Run the async main function using asyncio
    asyncio.run(main())
