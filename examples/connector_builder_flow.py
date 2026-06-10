"""
Connector Builder - End-to-End Example

Demonstrates creating, configuring, and managing custom connectors
using the Connector Builder API.

Usage:
    python examples/connector_builder_flow.py
    python examples/connector_builder_flow.py --base-url https://api.ismtip.com

Setup:
    export SUPERMETRICS_API_KEY=your_api_key
    export SUPERMETRICS_TEAM_ID=12345
"""

import argparse
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
    parser = argparse.ArgumentParser(description="Connector Builder example")
    parser.add_argument(
        "--base-url",
        default="https://api.supermetrics.com",
        help="API base URL (default: https://api.supermetrics.com, use https://api.ismtip.com for local dev)",
    )
    parser.add_argument("--team-id", type=int, help="Team ID (or set SUPERMETRICS_TEAM_ID env var)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    api_key = getpass("Enter your API key: ")

    import os

    team_id = args.team_id or int(os.getenv("SUPERMETRICS_TEAM_ID", "0"))
    if not team_id:
        team_id = int(input("Enter your team ID: "))

    client = SupermetricsClient(api_key=api_key, base_url=args.base_url)
    print(f"✓ Client initialized (base: {args.base_url})")

    try:
        # 1. List existing connectors
        print("\n--- List Connectors ---")
        connectors_response = client.connector_builder.list(team_id=team_id)
        print(f"✓ Found connectors: {connectors_response}")

        # 2. Create a new connector
        print("\n--- Create Connector ---")
        title = input("Connector title (or press Enter for 'SDK Test Connector'): ").strip()
        if not title:
            title = "SDK Test Connector"

        created = client.connector_builder.create(
            team_id=team_id,
            title=title,
            description="Created via Python SDK example",
        )
        connector_id = created.connector_identifier
        print(f"✓ Connector created: {connector_id}")
        print(f"  Name: {created.name}")

        # 3. Get connector details
        print("\n--- Get Connector ---")
        connector = client.connector_builder.get(team_id=team_id, connector_identifier=connector_id)
        print(f"✓ Connector: {connector.name}")
        print(f"  Created: {connector.created_at}")
        if connector.configuration:
            print(f"  Config version: {connector.configuration.version}")

        # 4. Update connector
        print("\n--- Update Connector ---")
        config = connector.configuration.to_dict() if connector.configuration else {}
        client.connector_builder.update(
            team_id=team_id,
            connector_identifier=connector_id,
            connector={"name": f"{title} (updated)", "description": "Updated via SDK"},
            configuration=config,
        )
        print("✓ Connector updated")

        # 5. Manage secrets
        print("\n--- Connector Secrets ---")
        secrets_response = client.connector_builder_secrets.list(team_id=team_id, connector_identifier=connector_id)
        print(f"✓ Secrets count: {secrets_response.count}")

        secret_created = client.connector_builder_secrets.create(
            team_id=team_id,
            connector_identifier=connector_id,
            secret_name="test_api_key",
            secret_value="sk-test-value-12345",
        )
        print(f"✓ Secret created (count now: {secret_created.count})")

        if secret_created.secrets:
            placeholder = secret_created.secrets[0].secret_placeholder
            print(f"  Placeholder: {placeholder}")

            client.connector_builder_secrets.update(
                team_id=team_id,
                connector_identifier=connector_id,
                secret_placeholder=placeholder,
                secret_value="sk-updated-value-67890",
            )
            print("✓ Secret updated")

            client.connector_builder_secrets.delete(
                team_id=team_id,
                connector_identifier=connector_id,
                secret_placeholder=placeholder,
            )
            print("✓ Secret deleted")

        # 6. View logs
        print("\n--- Connector Logs ---")
        logs_response = client.connector_builder_logs.list(team_id=team_id, connector_identifier=connector_id, limit=5)
        print(f"✓ Logs: {logs_response}")

        # 7. Logo operations
        print("\n--- Connector Logo ---")
        logo = client.connector_builder.get_logo(team_id=team_id, connector_identifier=connector_id)
        print(f"✓ Logo URL: {logo.logo_url}")

        logo_path = input("Upload logo image? Enter path (or press Enter to skip): ").strip()
        if logo_path:
            import os

            if not os.path.isfile(logo_path):
                print(f"  ⚠ File not found: {logo_path}")
            else:
                with open(logo_path, "rb") as f:
                    from supermetrics._generated.supermetrics_api_client.types import File

                    uploaded = client.connector_builder.upload_logo(
                        team_id=team_id,
                        connector_identifier=connector_id,
                        logo=File(payload=f, file_name=os.path.basename(logo_path)),
                    )
                    print(f"✓ Logo uploaded: {uploaded.logo_url}")

                logo_check = client.connector_builder.get_logo(team_id=team_id, connector_identifier=connector_id)
                print(f"✓ Logo verified: {logo_check.logo_url}")
                assert logo_check.logo_url == uploaded.logo_url, "Logo URL mismatch after upload!"

        # 8. Cleanup - delete the test connector
        cleanup = input("\nDelete test connector? (y/N): ").strip().lower()
        if cleanup == "y":
            client.connector_builder.delete(team_id=team_id, connector_identifier=connector_id)
            print(f"✓ Connector {connector_id} deleted")

        print("\n✅ Connector Builder flow complete!")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e.message}")
    except ValidationError as e:
        print(f"❌ Validation error: {e.message}")
        if e.response_body:
            print(f"   Detail: {e.response_body}")
    except APIError as e:
        print(f"❌ API error ({e.status_code}): {e.message}")
        if e.response_body:
            print(f"   Detail: {e.response_body}")
    except NetworkError as e:
        print(f"❌ Network error: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)


if __name__ == "__main__":
    main()
