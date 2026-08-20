"""Smoke tests against the real Supermetrics API.

These are skipped unless ``SUPERMETRICS_API_KEY`` is present in the environment,
so they never block local runs or pull requests from forks. When credentials are
available (for example on a scheduled CI run) they verify that the modernized
transport works against production: authentication, per-request headers, the raw
response envelope, and the error taxonomy.

Set ``SUPERMETRICS_BASE_URL`` to point at a non-production environment.
"""

from __future__ import annotations

import os

import pytest

from supermetrics import SupermetricsAsyncClient, SupermetricsClient
from supermetrics.exceptions import SupermetricsAuthError
from supermetrics.response import ApiResponse

API_KEY = os.environ.get("SUPERMETRICS_API_KEY", "")
BASE_URL = os.environ.get("SUPERMETRICS_BASE_URL", "https://api.supermetrics.com")

#: Team id for the team-scoped read coverage below. There is no "list my teams"
#: endpoint, so it cannot be discovered — it has to be supplied. Team-scoped tests
#: self-skip when it is absent, exactly as the whole file self-skips without a key.
_TEAM_ID_RAW = os.environ.get("SUPERMETRICS_TEAM_ID", "")
TEAM_ID = int(_TEAM_ID_RAW) if _TEAM_ID_RAW.isdigit() else None

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not API_KEY, reason="SUPERMETRICS_API_KEY is not set; skipping live API smoke tests"),
]

#: Applied to team-scoped tests. These verify that the SDK can parse what production
#: really returns — the check that caught four spec/model mismatches (see
#: docs/openapi-spec-fixes.md). They are read-only: nothing is created, changed, or
#: deleted on the real account.
requires_team = pytest.mark.skipif(
    TEAM_ID is None, reason="SUPERMETRICS_TEAM_ID is not set; skipping team-scoped live tests"
)


@pytest.fixture
def live_client() -> SupermetricsClient:
    """A synchronous client pointed at the real API."""
    with SupermetricsClient(api_key=API_KEY, base_url=BASE_URL, timeout=60.0) as client:
        yield client


def test_authenticated_request_succeeds(live_client: SupermetricsClient) -> None:
    """A real authenticated call returns without raising."""
    logins = live_client.logins.list()
    assert isinstance(logins, list)


def test_raw_response_exposes_live_metadata(live_client: SupermetricsClient) -> None:
    """The raw response envelope is populated by the real API."""
    response = live_client.with_raw_response.logins.list()

    assert isinstance(response, ApiResponse)
    assert response.status_code == 200
    assert response.raw_body


def test_per_request_headers_are_accepted(live_client: SupermetricsClient) -> None:
    """Injecting correlation headers does not break a real request."""
    response = live_client.with_raw_response.logins.list(headers={"X-Span-Id": "sdk-live-smoke"})
    assert response.status_code == 200


def test_invalid_token_raises_auth_error() -> None:
    """A deliberately bad credential produces SupermetricsAuthError."""
    with SupermetricsClient(bearer_token="otok_definitely_invalid", base_url=BASE_URL, timeout=30.0) as client:
        with pytest.raises(SupermetricsAuthError) as exc_info:
            client.logins.list()

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_async_client_against_live_api() -> None:
    """The async client works against the real API with a token provider."""
    async with SupermetricsAsyncClient(token_provider=lambda: API_KEY, base_url=BASE_URL, timeout=60.0) as client:
        logins = await client.logins.list()

    assert isinstance(logins, list)


class TestLiveReadCoverage:
    """Read-only coverage of every resource against the real API.

    The point of these is not the return value but the *parse*: they push whatever
    production actually returns through the generated models, which is the only way to
    catch a spec/model mismatch that hermetic fixtures are too tidy to expose (four such
    mismatches were found this way — see docs/openapi-spec-fixes.md).

    Nothing here mutates the account. Every call is a list/get. Where a call needs an id
    (a login, a destination, a connector), the id is discovered from a prior list and the
    dependent assertions are skipped when the account has none, so the file stays portable
    across accounts.
    """

    def test_logins_and_accounts_chain(self, live_client: SupermetricsClient) -> None:
        """logins.list -> get / get_accounts / get_by_username, then accounts.list."""
        logins = live_client.logins.list()
        assert isinstance(logins, list)
        if not logins:
            pytest.skip("account has no data source logins")

        first = logins[0]
        assert live_client.logins.get(first.login_id).login_id == first.login_id
        assert isinstance(live_client.logins.get_accounts(first.login_id), list)
        assert live_client.logins.get_by_username(first.username) is not None

        ds_id = first.ds_info.ds_id
        assert isinstance(live_client.accounts.list(ds_id=ds_id), list)

    @requires_team
    def test_datasource_details(self, live_client: SupermetricsClient) -> None:
        """datasource_details.get for a data source the account actually holds."""
        logins = live_client.logins.list()
        if not logins:
            pytest.skip("account has no data source logins")
        ds_id = logins[0].ds_info.ds_id
        assert live_client.datasource_details.get(team_id=TEAM_ID, data_source_id=ds_id) is not None

    @requires_team
    def test_teams(self, live_client: SupermetricsClient) -> None:
        """teams.get and teams.list_users."""
        assert live_client.teams.get(TEAM_ID) is not None
        assert isinstance(live_client.teams.list_users(TEAM_ID), list)

    @requires_team
    def test_custom_fields(self, live_client: SupermetricsClient) -> None:
        """custom_fields.list (pagination bugs #1/#4) and get_metadata."""
        assert isinstance(live_client.custom_fields.list(team_id=TEAM_ID), list)
        assert live_client.custom_fields.get_metadata(team_id=TEAM_ID) is not None

    @requires_team
    def test_blends_list(self, live_client: SupermetricsClient) -> None:
        """blends.list."""
        assert isinstance(live_client.blends.list(team_id=TEAM_ID), list)

    @requires_team
    def test_account_tags_list(self, live_client: SupermetricsClient) -> None:
        """account_tags.list (the data.items double-wrap, bug #3)."""
        assert isinstance(live_client.account_tags.list(team_id=TEAM_ID), list)

    @requires_team
    def test_destinations(self, live_client: SupermetricsClient) -> None:
        """destinations.list -> get / get_usage (auth-method shape, bug #2)."""
        destinations = live_client.destinations.list(team_id=TEAM_ID)
        assert isinstance(destinations, list)
        if not destinations:
            pytest.skip("team has no destinations")
        destination_id = destinations[0].id
        assert live_client.destinations.get(team_id=TEAM_ID, destination_id=destination_id) is not None
        assert live_client.destinations.get_usage(team_id=TEAM_ID, destination_id=destination_id) is not None

    @requires_team
    def test_transfers_reads(self, live_client: SupermetricsClient) -> None:
        """transfers.list and transfers.list_available_sources."""
        assert live_client.transfers.list(team_id=TEAM_ID) is not None
        assert live_client.transfers.list_available_sources(team_id=TEAM_ID) is not None

    @requires_team
    def test_backfills_list_incomplete(self, live_client: SupermetricsClient) -> None:
        """backfills.list_incomplete."""
        assert isinstance(live_client.backfills.list_incomplete(team_id=TEAM_ID), list)

    @requires_team
    def test_connector_builder_reads(self, live_client: SupermetricsClient) -> None:
        """connector_builder.list -> get, and the connector's secrets/logs lists."""
        connectors = live_client.connector_builder.list(team_id=TEAM_ID)
        assert connectors is not None
        identifiers = [c.connector_identifier for c in (connectors.connectors or [])]
        if not identifiers:
            pytest.skip("team has no custom connectors")
        identifier = identifiers[0]
        assert live_client.connector_builder.get(team_id=TEAM_ID, connector_identifier=identifier) is not None
        assert live_client.connector_builder_secrets.list(team_id=TEAM_ID, connector_identifier=identifier) is not None
        assert live_client.connector_builder_logs.list(team_id=TEAM_ID, connector_identifier=identifier) is not None


class TestLiveReadCoverageAsync:
    """A representative async slice — the async client has its own event hooks."""

    @pytest.mark.asyncio
    async def test_logins_chain(self) -> None:
        """The async logins chain parses real responses."""
        async with SupermetricsAsyncClient(api_key=API_KEY, base_url=BASE_URL, timeout=60.0) as client:
            logins = await client.logins.list()
            assert isinstance(logins, list)
            if logins:
                assert (await client.logins.get(logins[0].login_id)).login_id == logins[0].login_id

    @requires_team
    @pytest.mark.asyncio
    async def test_team_scoped_reads(self) -> None:
        """The async client parses the previously-broken team-scoped responses."""
        async with SupermetricsAsyncClient(api_key=API_KEY, base_url=BASE_URL, timeout=60.0) as client:
            assert isinstance(await client.custom_fields.list(team_id=TEAM_ID), list)
            assert isinstance(await client.account_tags.list(team_id=TEAM_ID), list)
            assert isinstance(await client.blends.list(team_id=TEAM_ID), list)
