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

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not API_KEY, reason="SUPERMETRICS_API_KEY is not set; skipping live API smoke tests"),
]


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
