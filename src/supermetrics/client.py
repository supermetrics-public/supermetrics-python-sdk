"""Synchronous client for Supermetrics API."""

import logging
import sys
from typing import Any

import httpx

from supermetrics.__version__ import __version__
from supermetrics._auth import AuthConfig, TokenProvider, resolve_auth_config
from supermetrics._generated.supermetrics_api_client.client import Client as GeneratedClient
from supermetrics._transport import build_default_headers, build_sync_event_hooks, resolve_dts_base_url
from supermetrics.resources._raw import SupermetricsClientWithRawResponse
from supermetrics.resources.accounts import AccountsResource
from supermetrics.resources.backfills import BackfillsResource
from supermetrics.resources.connector_builder import ConnectorBuilderResource
from supermetrics.resources.connector_builder_logs import ConnectorBuilderLogsResource
from supermetrics.resources.connector_builder_secrets import ConnectorBuilderSecretsResource
from supermetrics.resources.datasource_details import DatasourceDetailsResource
from supermetrics.resources.login_links import LoginLinksResource
from supermetrics.resources.logins import LoginsResource
from supermetrics.resources.queries import QueriesResource
from supermetrics.resources.transfer_runs import TransferRunsResource
from supermetrics.resources.transfers import TransfersResource

logger = logging.getLogger(__name__)


class SupermetricsClient:
    """Synchronous client for Supermetrics API.

    This client provides a type-safe, Pythonic interface to the Supermetrics
    API with full IDE autocomplete support. All methods are synchronous and
    suitable for scripts, notebooks, and REPL exploration.

    For asynchronous usage (recommended for production applications), use
    SupermetricsAsyncClient instead.

    Example:
        >>> from supermetrics import SupermetricsClient
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Use client for API operations
        >>> client.close()

        Or using context manager (recommended):
        >>> with SupermetricsClient(api_key="your-key") as client:
        ...     # Use client for API operations
        ...     pass
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        bearer_token: str | None = None,
        token_provider: TokenProvider | None = None,
        user_agent: str | None = None,
        custom_headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        base_url: str = "https://api.supermetrics.com",
        dts_base_url: str | None = None,
    ) -> None:
        """Initialize Supermetrics client.

        Exactly one credential must be supplied: ``api_key``, ``bearer_token``,
        or ``token_provider``.

        Args:
            api_key: Supermetrics API key (e.g. ``"api_..."``). Sent as a Bearer
                token in the Authorization header.
            bearer_token: OAuth 2.0 access token (e.g. ``"otok_..."``) or any
                other bearer credential, including RFC 8693 exchanged tokens.
            token_provider: Callable returning a bearer token, invoked once per
                request. Use this for short-lived tokens that must be refreshed
                without discarding the client's connection pool. Must be
                synchronous; use SupermetricsAsyncClient for async providers.
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
                transfer runs, backfills, and data source connections from a different
                host. Leave unset to route those calls to
                https://dts-api.supermetrics.com/v1 automatically whenever ``base_url``
                is the production default. If ``base_url`` is anything else, no routing
                is inferred and every request goes to ``base_url``; pass this explicitly
                to point Data Warehouse traffic somewhere specific.

        Raises:
            SupermetricsClientError: If zero or multiple credentials are supplied,
                or if an async token provider is given. Also a ``ValueError``.

        Example:
            >>> client = SupermetricsClient(api_key="api_abc123")
            >>> client = SupermetricsClient(bearer_token="otok_abc123")
            >>> client = SupermetricsClient(token_provider=lambda: vault.token())
            >>> client = SupermetricsClient(
            ...     api_key="api_abc123",
            ...     timeout=60.0,
            ...     custom_headers={"X-Custom": "value"}
            ... )
        """
        self._auth: AuthConfig = resolve_auth_config(api_key, bearer_token, token_provider, allow_async_provider=False)
        self._api_key = api_key
        self._bearer_token = bearer_token
        self._token_provider = token_provider

        # Build headers with Authorization and User-Agent
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        default_user_agent = f"supermetrics-sdk/{__version__} python/{py_version}"

        headers = build_default_headers(
            auth=self._auth,
            user_agent=user_agent or default_user_agent,
            custom_headers=custom_headers,
        )

        # Data Warehouse endpoints live on a different host; see resolve_dts_base_url.
        self._dts_base_url = resolve_dts_base_url(base_url, dts_base_url)

        logger.debug(f"Initializing SupermetricsClient with base_url={base_url}")

        # Create internal generated client. Event hooks apply per-request
        # authorization, header, and timeout overrides just before the request is sent.
        self._client = GeneratedClient(
            base_url=base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout),
            httpx_args={"event_hooks": build_sync_event_hooks(self._auth, self._dts_base_url)},
        )

        # Attach resource adapters
        self.login_links = LoginLinksResource(self._client)
        self.logins = LoginsResource(self._client)
        self.accounts = AccountsResource(self._client)
        self.queries = QueriesResource(self._client)
        self.backfills = BackfillsResource(self._client)
        self.connector_builder = ConnectorBuilderResource(self._client)
        self.connector_builder_secrets = ConnectorBuilderSecretsResource(self._client)
        self.connector_builder_logs = ConnectorBuilderLogsResource(self._client)
        self.datasource_details = DatasourceDetailsResource(self._client)
        self.transfers = TransfersResource(self._client)
        self.transfer_runs = TransferRunsResource(self._client)

        self._with_raw_response: SupermetricsClientWithRawResponse | None = None

        logger.info("SupermetricsClient initialized successfully")

    @property
    def with_raw_response(self) -> SupermetricsClientWithRawResponse:
        """Access the same resources, but returning full HTTP response envelopes.

        Every method mirrored here has an identical signature to its counterpart
        on the client, but returns an :class:`~supermetrics.response.ApiResponse`
        carrying the status code, headers, and raw payload alongside the parsed
        data.

        Returns:
            The raw-response view of this client.

        Example:
            >>> response = client.with_raw_response.logins.get("login_abc")
            >>> response.status_code
            200
            >>> response.span_id
            'a8f3b2c9e10d'
            >>> response.data.username
            'user@example.com'
        """
        if self._with_raw_response is None:
            self._with_raw_response = SupermetricsClientWithRawResponse(self)
        return self._with_raw_response

    def close(self) -> None:
        """Close the client and release resources.

        Call this when you're done using the client to ensure proper cleanup.
        Alternatively, use the client as a context manager.

        Example:
            >>> client = SupermetricsClient(api_key="your-key")
            >>> try:
            ...     # Use client
            ...     pass
            ... finally:
            ...     client.close()
        """
        logger.debug("Closing SupermetricsClient")
        self._client.get_httpx_client().close()

    def __enter__(self) -> "SupermetricsClient":
        """Context manager entry.

        Returns:
            The client instance.
        """
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit.

        Ensures the client is properly closed when exiting the context.
        """
        self.close()
