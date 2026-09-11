"""
Destination Setup - End-to-End Example

Demonstrates creating and managing Data Warehouse destinations using the
Supermetrics SDK: listing existing destinations, testing credentials before
committing, creating a new destination, inspecting it, checking usage, and
cleaning up.

Usage:
    python examples/destination_setup_flow.py
    python examples/destination_setup_flow.py --base-url https://{replace-me}

Setup:
    export SUPERMETRICS_API_KEY=your_api_key
    export SUPERMETRICS_TEAM_ID=12345
"""

import argparse
import os
import traceback
from getpass import getpass

from dotenv import load_dotenv

from supermetrics import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsClient,
    ValidationError,
)

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Destination setup example")
    parser.add_argument(
        "--base-url",
        default="https://api.supermetrics.com",
        help="API base URL (default: https://api.supermetrics.com)",
    )
    parser.add_argument("--team-id", type=int, help="Team ID (or set SUPERMETRICS_TEAM_ID env var)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    api_key = getpass("Enter your API key: ")
    team_id = args.team_id or int(os.getenv("SUPERMETRICS_TEAM_ID", "0"))
    if not team_id:
        team_id = int(input("Enter your team ID: "))

    client = SupermetricsClient(api_key=api_key, base_url=args.base_url)
    print(f"Client initialized (base: {args.base_url})")

    try:
        # 1. List existing destinations
        print("\n--- List Destinations ---")
        destinations = client.destinations.list(team_id=team_id)
        print(f"Found {len(destinations)} destination(s)")
        for dest in destinations:
            print(f"  {dest.id}: {dest.display_name} ({dest.type_})")

        # 2. Collect credentials for a new Snowflake destination
        #    Replace with your own destination type and fields as needed.
        print("\n--- Configure New Destination ---")
        dest_type = input("Destination type (default: DWH_SNOWFLAKE): ").strip() or "DWH_SNOWFLAKE"
        display_name = input("Display name (default: SDK Test Destination): ").strip() or "SDK Test Destination"

        fields: dict[str, str] = {}
        print("Enter destination fields (blank name to finish):")
        while True:
            name = input("  Field name: ").strip()
            if not name:
                break
            value = input(f"  {name} value: ").strip()
            fields[name] = value

        if not fields:
            print("No fields entered, using Snowflake defaults for demonstration.")
            fields = {
                "hostname": "example.us-east-1.snowflakecomputing.com",
                "warehouse": "DEMO_WH",
                "database_name": "TEST_DB",
                "schema": "PUBLIC",
                "role": "ACCOUNTADMIN",
                "username": "DEMO_USER",
            }

        # 3. Test connection before committing
        #    A failed test is a return value, not an exception. Branch on result.success.
        print("\n--- Test Connection ---")
        result = client.destinations.test_connection(
            team_id=team_id,
            type=dest_type,
            display_name=display_name,
            fields=fields,
        )
        if result.success:
            print("Connection test passed")
        else:
            print(f"Connection test failed: {result.error}")
            proceed = input("Create the destination anyway? (y/N): ").strip().lower()
            if proceed != "y":
                print("Aborted.")
                return

        # 4. Create the destination
        print("\n--- Create Destination ---")
        destination = client.destinations.create(
            team_id=team_id,
            type=dest_type,
            display_name=display_name,
            fields=fields,
        )
        destination_id = destination.id
        print(f"Destination created: {destination_id}")
        print(f"  Name: {destination.display_name}")
        print(f"  Type: {destination.destination_type.title}")

        # 5. Get destination details
        #    The read shape differs from the write shape: get() returns edit_settings
        #    (a list of form descriptors), not the flat fields dict that create() takes.
        print("\n--- Get Destination Details ---")
        info = client.destinations.get(team_id=team_id, destination_id=destination_id)
        print(f"  Name: {info.display_name}")
        print("  Edit settings:")
        for setting in info.edit_settings:
            print(f"    {setting.id} ({setting.input_type}): {setting.value}")

        # 6. Check usage before cleanup
        #    get_usage reports which transfers depend on a destination. A freshly
        #    created one has none, but always check before deleting in production.
        print("\n--- Check Usage ---")
        usage = client.destinations.get_usage(team_id=team_id, destination_id=destination_id)
        if usage.is_used:
            print(f"  In use by {len(usage.transfers)} transfer(s):")
            for transfer in usage.transfers:
                print(f"    {transfer.transfer_id}: {transfer.transfer_name}")
        else:
            print("  Not used by any transfers")

        # 7. Cleanup
        cleanup = input("\nDelete test destination? (y/N): ").strip().lower()
        if cleanup == "y":
            client.destinations.delete(team_id=team_id, destination_id=destination_id)
            print(f"Destination {destination_id} deleted")

        print("\nDestination setup flow complete!")

    except AuthenticationError as e:
        print(f"Authentication failed: {e.message}")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        if e.response_body:
            print(f"  Detail: {e.response_body}")
    except APIError as e:
        print(f"API error ({e.status_code}): {e.message}")
        if e.response_body:
            print(f"  Detail: {e.response_body}")
    except NetworkError as e:
        print(f"Network error: {e.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)


if __name__ == "__main__":
    main()
