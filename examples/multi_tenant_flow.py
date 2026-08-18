"""
Multi-Tenant Service - Shared Client with Per-Request Credentials

This example demonstrates the transport features added in Phase 1: a single
long-lived client serving many callers, each with their own OAuth token and
tracing context, without ever rebuilding the client or losing its connection
pool.

This is the pattern to use in a proxy, an MCP server, a background worker pool,
or any service that acts on behalf of multiple end users.

Installation:
    pip install supermetrics-sdk

Setup:
    Get your API key from: https://supermetrics.com/account/api
    Set it as an environment variable: export SUPERMETRICS_API_KEY=your_api_key

Usage:
    python examples/multi_tenant_flow.py

What this shows:
    1. A dynamic token provider, re-evaluated on every request, so short-lived
       OAuth tokens refresh without discarding the connection pool.
    2. Per-request auth_token, headers and timeout overrides on a shared client.
    3. Concurrent callers on one client, each with their own credential.
    4. with_raw_response for HTTP status codes, correlation IDs and rate limits.
    5. Catching SupermetricsAuthError to refresh a token and retry.
"""

import asyncio
import os
import time

from supermetrics import (
    APIError,
    NetworkError,
    SupermetricsAsyncClient,
    SupermetricsAuthError,
    SupermetricsRateLimitError,
)

API_KEY = os.environ.get("SUPERMETRICS_API_KEY", "")
BASE_URL = os.environ.get("SUPERMETRICS_BASE_URL", "https://api.supermetrics.com")


class TokenCache:
    """A stand-in for whatever issues your short-lived access tokens.

    In a real service this would call your OAuth provider, a secrets manager, or
    an internal token-exchange endpoint, and cache the result until it expires.
    """

    def __init__(self, token: str) -> None:
        """Seed the cache with an initial token."""
        self._token = token
        self._expires_at = time.monotonic() + 3600

    async def get_token(self) -> str:
        """Return a valid token, refreshing it first if it is about to expire."""
        if time.monotonic() >= self._expires_at - 60:
            await self.refresh()
        return self._token

    async def refresh(self) -> None:
        """Fetch a new token. Replace this with a real token exchange."""
        await asyncio.sleep(0)  # stand-in for the network round trip
        self._expires_at = time.monotonic() + 3600


async def dynamic_token_provider(cache: TokenCache) -> None:
    """Show a client that follows a rotating token via a provider callable."""
    print("\n1. Dynamic token provider")
    print("-" * 60)

    # The provider is called once per request, so the client always sends a
    # current token. The connection pool is never rebuilt.
    async with SupermetricsAsyncClient(token_provider=cache.get_token, base_url=BASE_URL) as client:
        logins = await client.logins.list()
        print(f"   Retrieved {len(logins)} logins using a provider-issued token")


async def per_request_overrides() -> None:
    """Show one shared client serving callers that each bring their own context."""
    print("\n2. Per-request overrides on a shared client")
    print("-" * 60)

    async with SupermetricsAsyncClient(api_key=API_KEY, base_url=BASE_URL) as client:
        logins = await client.logins.list(
            # Act on behalf of one specific caller for this request only.
            auth_token=API_KEY,
            # Correlation headers your tracing backend can stitch together.
            headers={"X-Span-Id": "example-span-001", "Idempotency-Key": "example-req-001"},
            # This call may be slow; give it more room than the client default.
            timeout=60.0,
        )
        print(f"   Retrieved {len(logins)} logins with per-request auth and tracing headers")


async def concurrent_callers() -> None:
    """Show concurrent tasks on one pooled client, each with its own credential."""
    print("\n3. Concurrent callers, one shared connection pool")
    print("-" * 60)

    async with SupermetricsAsyncClient(api_key=API_KEY, base_url=BASE_URL) as client:

        async def handle_request(caller_id: int) -> int:
            """Serve one inbound request on behalf of one end user."""
            logins = await client.logins.list(
                auth_token=API_KEY,  # in a real service, this caller's own token
                headers={"X-Span-Id": f"span-{caller_id:03d}"},
            )
            return len(logins)

        counts = await asyncio.gather(*(handle_request(i) for i in range(5)))
        print(f"   Served {len(counts)} concurrent callers; login counts: {counts}")


async def response_metadata() -> None:
    """Show reading HTTP status, correlation IDs and rate limits off a response."""
    print("\n4. Transport metadata via with_raw_response")
    print("-" * 60)

    async with SupermetricsAsyncClient(api_key=API_KEY, base_url=BASE_URL) as client:
        response = await client.with_raw_response.logins.list()

        print(f"   HTTP status : {response.status_code}")
        print(f"   Span ID     : {response.span_id}")
        print(f"   Request ID  : {response.request_id}")
        print(f"   Retry-After : {response.retry_after}")
        print(f"   Payload     : {len(response.raw_body)} bytes")
        print(f"   Parsed data : {len(response.data)} logins")


async def refresh_on_auth_error(cache: TokenCache) -> None:
    """Show recovering from an expired token instead of failing the operation."""
    print("\n5. Refresh-and-retry on an expired token")
    print("-" * 60)

    async with SupermetricsAsyncClient(token_provider=cache.get_token, base_url=BASE_URL) as client:
        try:
            logins = await client.logins.list()
        except SupermetricsAuthError as error:
            # The upstream OAuth code tells us whether a refresh would help.
            if error.error_code in ("ACCESS_TOKEN_INVALID", "ACCESS_TOKEN_EXPIRED"):
                print(f"   Token rejected ({error.error_code}); refreshing and retrying")
                await cache.refresh()
                logins = await client.logins.list()
            else:
                raise
        print(f"   Retrieved {len(logins)} logins")


async def main() -> None:
    """Run every demonstration in turn."""
    if not API_KEY:
        print("Set SUPERMETRICS_API_KEY before running this example.")
        return

    print("=" * 60)
    print("Supermetrics SDK - Multi-Tenant Transport Features")
    print("=" * 60)

    cache = TokenCache(API_KEY)

    try:
        await dynamic_token_provider(cache)
        await per_request_overrides()
        await concurrent_callers()
        await response_metadata()
        await refresh_on_auth_error(cache)
    except SupermetricsRateLimitError as error:
        print(f"\nRate limited. Retry after {error.retry_after} seconds.")
    except SupermetricsAuthError as error:
        print(f"\nAuthentication failed ({error.error_code}): {error.message}")
    except APIError as error:
        print(f"\nAPI error {error.status_code}: {error.message}")
    except NetworkError as error:
        print(f"\nNetwork error: {error.message}")
    else:
        print("\n" + "=" * 60)
        print("Done.")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
