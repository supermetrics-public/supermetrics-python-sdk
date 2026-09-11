"""
Data Warehouse Transfers - End-to-End Example

Demonstrates the transfer lifecycle using the Supermetrics SDK: discovering
available sources and destinations, validating a configuration, creating a
transfer, pausing and resuming it, inspecting runs, creating and cancelling
a backfill, and cleaning up.

Usage:
    python examples/data_warehouse_flow.py
    python examples/data_warehouse_flow.py --base-url https://{replace-me}

Setup:
    export SUPERMETRICS_API_KEY=your_api_key
    export SUPERMETRICS_TEAM_ID=12345
"""

import argparse
import os
import traceback
from datetime import UTC, date, datetime, timedelta
from getpass import getpass

from dotenv import load_dotenv

from supermetrics import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsClient,
    TransferAccount,
    TransferSchedule,
    ValidationError,
)

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data Warehouse transfer example")
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
        # 1. Discover available sources and destinations
        #    The response wraps everything in a "data" envelope, so the typed
        #    attributes are Unset and the actual payload lives in
        #    additional_properties["data"].
        print("\n--- Available Sources & Destinations ---")
        available = client.transfers.list_available_sources(team_id=team_id)
        avail_data = available.additional_properties.get("data", {})
        sources = avail_data.get("data_sources", [])
        dests = avail_data.get("destinations", [])

        print(f"Data sources: {len(sources)}")
        for ds in sources[:5]:
            print(f"  {ds['data_source_id']}: {ds['service_name']}")
        if len(sources) > 5:
            print(f"  ... and {len(sources) - 5} more")

        print(f"Destinations: {len(dests)}")
        for dest in dests[:5]:
            print(f"  {dest['destination_id']}: {dest['destination_name']} ({dest['destination_type']})")
        if len(dests) > 5:
            print(f"  ... and {len(dests) - 5} more")

        # 2. Get configuration options for a source/destination pair
        print("\n--- Configuration Options ---")
        source_id = input("Data source ID (e.g. AW, GA4): ").strip()
        dest_id = int(input("Destination ID (numeric): ").strip())

        options = client.transfers.get_available_options(
            team_id=team_id,
            source_id=source_id,
            destination_id=dest_id,
        )
        options_data = options.additional_properties.get("data", {})
        schemas = options_data.get("schemas", [])
        print(f"Schemas: {len(schemas)}")
        for schema in schemas[:5]:
            print(f"  {schema}")

        # 3. Validate before creating
        #    validate() returns a result, not an exception. An invalid config is
        #    a successful call with is_valid=False and field-level errors.
        print("\n--- Validate Transfer Config ---")
        schema_id = int(input("Schema ID (numeric): ").strip())
        display_name = input("Transfer name (default: SDK Test Transfer): ").strip() or "SDK Test Transfer"
        login_id = int(input("Login ID (numeric): ").strip())
        account_id = input("Account ID: ").strip()

        schedule = [TransferSchedule(run_interval="daily", run_hour=22, refresh_window=1)]
        accounts = [TransferAccount(login_id=login_id, account_id=account_id)]

        validation = client.transfers.validate(
            team_id=team_id,
            data_source_id=source_id,
            schema_id=schema_id,
            destination_id=dest_id,
            display_name=display_name,
            schedule=schedule,
            accounts=accounts,
        )
        if validation.is_valid:
            print("Validation passed")
        else:
            print(f"Validation failed: {validation.errors}")
            proceed = input("Create anyway? (y/N): ").strip().lower()
            if proceed != "y":
                print("Aborted.")
                return

        # 4. Create the transfer
        print("\n--- Create Transfer ---")
        created = client.transfers.create(
            team_id=team_id,
            data_source_id=source_id,
            schema_id=schema_id,
            destination_id=dest_id,
            display_name=display_name,
            schedule=schedule,
            accounts=accounts,
        )
        transfer_id = created.transfer_id
        print(f"Transfer created: {transfer_id}")
        print(f"  Name: {created.display_name}")

        # 5. List transfers and inspect the new one
        print("\n--- List & Inspect ---")
        transfers = client.transfers.list(team_id=team_id)
        print(f"Team has {len(transfers)} transfer(s)")

        config = client.transfers.get(team_id=team_id, transfer_id=transfer_id)
        config_data = config.additional_properties.get("data", {})
        print(f"  Name: {config_data.get('display_name')}")
        print(f"  Source: {config_data.get('data_source', {}).get('data_source_id')}")
        print(f"  Destination: {config_data.get('destination_id')}")

        # 6. Create a backfill
        #    Must happen before pausing -- the API rejects backfills on paused transfers.
        print("\n--- Backfill ---")
        do_backfill = input("Create a test backfill? (y/N): ").strip().lower()
        if do_backfill == "y":
            range_end = date.today()
            range_start = range_end - timedelta(days=7)

            backfill = client.backfills.create(
                team_id=team_id,
                transfer_id=transfer_id,
                range_start=range_start,
                range_end=range_end,
            )
            print(f"Backfill created: {backfill.transfer_backfill_id}")
            print(f"  Status: {backfill.status}")
            print(f"  Range: {range_start} to {range_end}")

            # Check latest backfill status
            latest = client.backfills.get_latest(team_id=team_id, transfer_id=transfer_id)
            print(f"  Latest backfill status: {latest.status}")

            # Cancel it
            cancel = input("Cancel the backfill? (y/N): ").strip().lower()
            if cancel == "y":
                cancelled = client.backfills.cancel(team_id=team_id, backfill_id=backfill.transfer_backfill_id)
                print(f"  Backfill cancelled: {cancelled.status}")

        # 7. List recent runs
        #    A freshly created transfer may not have runs yet.
        #    The API requires timezone-aware datetimes without microseconds.
        print("\n--- Transfer Runs ---")
        now = datetime.now(UTC).replace(microsecond=0)
        runs = client.transfers.list_runs(
            team_id=team_id,
            transfer_id=transfer_id,
            start_date=now - timedelta(days=7),
            end_date=now,
        )
        print(f"Runs in the last 7 days: {len(runs)}")
        for run in runs[:5]:
            print(f"  {run.id}: {run.status}")

        if runs:
            run_detail = client.transfer_runs.get(team_id=team_id, transfer_run_id=runs[0].id)
            print(f"  Latest run status: {run_detail.status}")
            print(f"  Rows: {run_detail.total_rows}")

        # 8. Pause and resume
        print("\n--- Pause / Resume ---")
        paused = client.transfers.set_state(team_id=team_id, transfer_id=transfer_id, state="pause")
        paused_state = paused.additional_properties.get("data", {}).get("state")
        print(f"Paused: state={paused_state}")

        resumed = client.transfers.set_state(team_id=team_id, transfer_id=transfer_id, state="unpause")
        resumed_state = resumed.additional_properties.get("data", {}).get("state")
        print(f"Resumed: state={resumed_state}")

        # 9. Cleanup
        cleanup = input("\nDelete test transfer? (y/N): ").strip().lower()
        if cleanup == "y":
            client.transfers.delete(team_id=team_id, transfer_id=transfer_id)
            print(f"Transfer {transfer_id} deleted")

        print("\nData Warehouse flow complete!")

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
