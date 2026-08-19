"""Asynchronous client for Supermetrics API."""

import logging
import sys
from typing import Any

import httpx

from supermetrics.__version__ import __version__
from supermetrics._auth import AsyncTokenProvider, AuthConfig, resolve_auth_config
from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._transport import build_async_event_hooks, build_default_headers, resolve_dts_base_url
from supermetrics.resources._raw import SupermetricsAsyncClientWithRawResponse
from supermetrics.resources.account_tags import AccountTagsAsyncResource
from supermetrics.resources.accounts import AccountsAsyncResource
from supermetrics.resources.backfills import BackfillsAsyncResource
from supermetrics.resources.blends import BlendsAsyncResource
from supermetrics.resources.connector_builder import ConnectorBuilderAsyncResource
from supermetrics.resources.connector_builder_logs import ConnectorBuilderLogsAsyncResource
from supermetrics.resources.connector_builder_secrets import ConnectorBuilderSecretsAsyncResource
from supermetrics.resources.custom_fields import CustomFieldsAsyncResource
from supermetrics.resources.datasource_details import DatasourceDetailsAsyncResource
from supermetrics.resources.destinations import DestinationsAsyncResource
from supermetrics.resources.login_links import LoginLinksAsyncResource
from supermetrics.resources.logins import LoginsAsyncResource
from supermetrics.resources.queries import QueriesAsyncResource
from supermetrics.resources.transfer_runs import TransferRunsAsyncResource
from supermetrics.resources.transfers import TransfersAsyncResource

logger = logging.getLogger(__name__)


class SupermetricsAsyncClient:
    """Asynchronous client for Supermetrics API.

    This client provides the same interface as SupermetricsClient but all
    methods are async and must be awaited. Recommended for production
    applications that need high concurrency or integration with async
    frameworks (FastAPI, asyncio, etc.).

    A single instance is safe to share across concurrent tasks that each carry
    their own credentials and tracing headers: per-request overrides are bound to
    context variables, so the connection pool is reused without any cross-talk
    between callers.

    Example:
        >>> import asyncio
        >>> from supermetrics import SupermetricsAsyncClient
        >>>
        >>> async def main():
        ...     async with SupermetricsAsyncClient(api_key="your-key") as client:
        ...         # Use client for API operations
        ...         pass
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        bearer_token: str | None = None,
        token_provider: AsyncTokenProvider | None = None,
        user_agent: str | None = None,
        custom_headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        base_url: str = "https://api.supermetrics.com",
        dts_base_url: str | None = None,
    ) -> None:
        """Initialize async Supermetrics client.

        Exactly one credential must be supplied: ``api_key``, ``bearer_token``,
        or ``token_provider``.

        Args:
            api_key: Supermetrics API key (e.g. ``"api_..."``). Sent as a Bearer
                token in the Authorization header.
            bearer_token: OAuth 2.0 access token (e.g. ``"otok_..."``) or any
                other bearer credential, including RFC 8693 exchanged tokens.
            token_provider: Callable returning a bearer token, invoked once per
                request. May be a coroutine function or a plain callable. Use
                this for short-lived tokens that must be refreshed without
                discarding the client's connection pool.
            user_agent: Custom User-Agent header. Defaults to
                "supermetrics-sdk/{version} python/{py_version}".
            custom_headers: Additional HTTP headers for all requests. These
                override the SDK defaults if there are conflicts, with one
                exception: ``Authorization`` cannot be set here, because the
                credential comes from ``api_key`` / ``bearer_token`` /
                ``token_provider``. Setting it emits a ``UserWarning`` and is
                ignored; use a method's ``headers`` argument to send a different
                credential for a single call.
            timeout: Request timeout in seconds (default: 30.0). Individual
                calls can override this with their ``timeout`` argument.
            base_url: API base URL (default: production API at
                https://api.supermetrics.com).
            dts_base_url: Base URL for the Data Warehouse API, which serves transfers,
                transfer runs, backfills, data source connections, and destinations
                from a different host. Leave unset to route those calls to
                https://dts-api.supermetrics.com/v1 automatically whenever ``base_url``
                is the production default. If ``base_url`` is anything else, no routing
                is inferred and every request goes to ``base_url``; pass this explicitly
                to point Data Warehouse traffic somewhere specific.

        Raises:
            SupermetricsClientError: If zero or multiple credentials are
                supplied. Also a ``ValueError``.

        Example:
            >>> client = SupermetricsAsyncClient(api_key="api_abc123")
            >>> client = SupermetricsAsyncClient(bearer_token="otok_abc123")
            >>>
            >>> async def get_valid_token() -> str:
            ...     return await oauth_service.get_access_token(team_id=123)
            >>> client = SupermetricsAsyncClient(token_provider=get_valid_token)
        """
        self._auth: AuthConfig = resolve_auth_config(api_key, bearer_token, token_provider, allow_async_provider=True)
        self._api_key = api_key
        self._bearer_token = bearer_token
        self._token_provider = token_provider

        # Build headers (identical to sync client)
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

        headers = build_default_headers(
            auth=self._auth,
            user_agent=user_agent or default_user_agent,
            custom_headers=custom_headers,
        )

        # Data Warehouse endpoints live on a different host; see resolve_dts_base_url.
        self._dts_base_url = resolve_dts_base_url(base_url, dts_base_url)

        logger.debug(f"Initializing SupermetricsAsyncClient with base_url={base_url}")

        # Create internal generated client (supports both sync and async). Event hooks
        # apply per-request authorization, header, and timeout overrides before sending.
        self._client = GeneratedClient(
            base_url=base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout),
            httpx_args={"event_hooks": build_async_event_hooks(self._auth, self._dts_base_url)},
        )

        # Attach resource adapters
        self.login_links = LoginLinksAsyncResource(self._client)
        self.logins = LoginsAsyncResource(self._client)
        self.accounts = AccountsAsyncResource(self._client)
        self.queries = QueriesAsyncResource(self._client)
        self.backfills = BackfillsAsyncResource(self._client)
        self.connector_builder = ConnectorBuilderAsyncResource(self._client)
        self.connector_builder_secrets = ConnectorBuilderSecretsAsyncResource(self._client)
        self.connector_builder_logs = ConnectorBuilderLogsAsyncResource(self._client)
        self.datasource_details = DatasourceDetailsAsyncResource(self._client)
        self.destinations = DestinationsAsyncResource(self._client)
        self.transfers = TransfersAsyncResource(self._client)
        self.transfer_runs = TransferRunsAsyncResource(self._client)
        self.custom_fields = CustomFieldsAsyncResource(self._client)
        self.account_tags = AccountTagsAsyncResource(self._client)
        self.blends = BlendsAsyncResource(self._client)

        self._with_raw_response: SupermetricsAsyncClientWithRawResponse | None = None

        logger.info("SupermetricsAsyncClient initialized successfully")

    @property
    def with_raw_response(self) -> SupermetricsAsyncClientWithRawResponse:
        """Access the same resources, but returning full HTTP response envelopes.

        Every method mirrored here has an identical signature to its counterpart
        on the client, but resolves to an
        :class:`~supermetrics.response.ApiResponse` carrying the status code,
        headers, and raw payload alongside the parsed data.

        Returns:
            The raw-response view of this client.

        Example:
            >>> response = await client.with_raw_response.logins.get("login_abc")
            >>> response.status_code
            200
            >>> response.data.username
            'user@example.com'
        """
        if self._with_raw_response is None:
            self._with_raw_response = SupermetricsAsyncClientWithRawResponse(self)
        return self._with_raw_response

    async def close(self) -> None:
        """Close the client and release resources.

        Important: Always call this when done, or use async context manager.

        Example:
            >>> client = SupermetricsAsyncClient(api_key="your-key")
            >>> try:
            ...     # Use client
            ...     pass
            ... finally:
            ...     await client.close()
        """
        logger.debug("Closing SupermetricsAsyncClient")
        await self._client.get_async_httpx_client().aclose()

    async def __aenter__(self) -> "SupermetricsAsyncClient":
        """Async context manager entry.

        Returns:
            The client instance.
        """
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit.

        Ensures the client is properly closed when exiting the context.
        """
        await self.close()
