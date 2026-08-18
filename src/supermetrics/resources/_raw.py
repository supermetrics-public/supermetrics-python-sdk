"""``with_raw_response`` views over every resource adapter.

Each class here mirrors one resource adapter method-for-method. The wrapped
methods keep the exact signature of their counterparts but return an
:class:`~supermetrics.response.ApiResponse`, which carries the HTTP status code,
response headers, and raw payload alongside the parsed data.

These classes are not instantiated directly — reach them through
``client.with_raw_response`` / ``async_client.with_raw_response``.

Note:
    A handful of resource methods issue more than one HTTP request (for example
    ``queries.execute`` while polling, or ``logins.get_by_username`` which lists
    first). For those, the returned envelope describes the **last** response.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from supermetrics.resources.accounts import AccountsAsyncResource, AccountsResource
from supermetrics.resources.backfills import BackfillsAsyncResource, BackfillsResource
from supermetrics.resources.connector_builder import ConnectorBuilderAsyncResource, ConnectorBuilderResource
from supermetrics.resources.connector_builder_logs import (
    ConnectorBuilderLogsAsyncResource,
    ConnectorBuilderLogsResource,
)
from supermetrics.resources.connector_builder_secrets import (
    ConnectorBuilderSecretsAsyncResource,
    ConnectorBuilderSecretsResource,
)
from supermetrics.resources.datasource_details import DatasourceDetailsAsyncResource, DatasourceDetailsResource
from supermetrics.resources.login_links import LoginLinksAsyncResource, LoginLinksResource
from supermetrics.resources.logins import LoginsAsyncResource, LoginsResource
from supermetrics.resources.queries import QueriesAsyncResource, QueriesResource
from supermetrics.response import async_to_raw_response_wrapper, to_raw_response_wrapper

if TYPE_CHECKING:  # pragma: no cover - typing only
    from supermetrics.async_client import SupermetricsAsyncClient
    from supermetrics.client import SupermetricsClient


class AccountsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.accounts.AccountsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: AccountsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)


class AccountsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.accounts.AccountsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: AccountsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)


class BackfillsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.backfills.BackfillsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: BackfillsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.create = to_raw_response_wrapper(resource.create)
        self.get = to_raw_response_wrapper(resource.get)
        self.get_latest = to_raw_response_wrapper(resource.get_latest)
        self.list_incomplete = to_raw_response_wrapper(resource.list_incomplete)
        self.cancel = to_raw_response_wrapper(resource.cancel)


class BackfillsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.backfills.BackfillsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: BackfillsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.create = async_to_raw_response_wrapper(resource.create)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.get_latest = async_to_raw_response_wrapper(resource.get_latest)
        self.list_incomplete = async_to_raw_response_wrapper(resource.list_incomplete)
        self.cancel = async_to_raw_response_wrapper(resource.cancel)


class ConnectorBuilderResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.connector_builder.ConnectorBuilderResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: ConnectorBuilderResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)
        self.get_logo = to_raw_response_wrapper(resource.get_logo)
        self.upload_logo = to_raw_response_wrapper(resource.upload_logo)


class ConnectorBuilderAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.connector_builder.ConnectorBuilderAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: ConnectorBuilderAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)
        self.get_logo = async_to_raw_response_wrapper(resource.get_logo)
        self.upload_logo = async_to_raw_response_wrapper(resource.upload_logo)


class ConnectorBuilderLogsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.connector_builder_logs.ConnectorBuilderLogsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: ConnectorBuilderLogsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)


class ConnectorBuilderLogsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.connector_builder_logs.ConnectorBuilderLogsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: ConnectorBuilderLogsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)


class ConnectorBuilderSecretsResourceWithRawResponse:
    """Raw-response view over
    :class:`~supermetrics.resources.connector_builder_secrets.ConnectorBuilderSecretsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: ConnectorBuilderSecretsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)


class ConnectorBuilderSecretsAsyncResourceWithRawResponse:
    """Raw-response view over
    :class:`~supermetrics.resources.connector_builder_secrets.ConnectorBuilderSecretsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: ConnectorBuilderSecretsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)


class DatasourceDetailsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.datasource_details.DatasourceDetailsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: DatasourceDetailsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = to_raw_response_wrapper(resource.get)


class DatasourceDetailsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.datasource_details.DatasourceDetailsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: DatasourceDetailsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = async_to_raw_response_wrapper(resource.get)


class LoginLinksResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.login_links.LoginLinksResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: LoginLinksResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.create = to_raw_response_wrapper(resource.create)
        self.get = to_raw_response_wrapper(resource.get)
        self.list = to_raw_response_wrapper(resource.list)
        self.close = to_raw_response_wrapper(resource.close)


class LoginLinksAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.login_links.LoginLinksAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: LoginLinksAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.create = async_to_raw_response_wrapper(resource.create)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.list = async_to_raw_response_wrapper(resource.list)
        self.close = async_to_raw_response_wrapper(resource.close)


class LoginsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.logins.LoginsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: LoginsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = to_raw_response_wrapper(resource.get)
        self.list = to_raw_response_wrapper(resource.list)
        self.get_by_username = to_raw_response_wrapper(resource.get_by_username)


class LoginsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.logins.LoginsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: LoginsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = async_to_raw_response_wrapper(resource.get)
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get_by_username = async_to_raw_response_wrapper(resource.get_by_username)


class QueriesResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.queries.QueriesResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: QueriesResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.execute = to_raw_response_wrapper(resource.execute)
        self.get_results = to_raw_response_wrapper(resource.get_results)


class QueriesAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.queries.QueriesAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: QueriesAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.execute = async_to_raw_response_wrapper(resource.execute)
        self.get_results = async_to_raw_response_wrapper(resource.get_results)


class SupermetricsClientWithRawResponse:
    """Raw-response view over every resource of a synchronous client.

    Reached through :attr:`SupermetricsClient.with_raw_response`.

    Args:
        client: The client whose resources should be mirrored.
    """

    def __init__(self, client: SupermetricsClient) -> None:
        """Build a raw-response view for each resource on ``client``."""
        self.login_links = LoginLinksResourceWithRawResponse(client.login_links)
        self.logins = LoginsResourceWithRawResponse(client.logins)
        self.accounts = AccountsResourceWithRawResponse(client.accounts)
        self.queries = QueriesResourceWithRawResponse(client.queries)
        self.backfills = BackfillsResourceWithRawResponse(client.backfills)
        self.connector_builder = ConnectorBuilderResourceWithRawResponse(client.connector_builder)
        self.connector_builder_secrets = ConnectorBuilderSecretsResourceWithRawResponse(
            client.connector_builder_secrets
        )
        self.connector_builder_logs = ConnectorBuilderLogsResourceWithRawResponse(client.connector_builder_logs)
        self.datasource_details = DatasourceDetailsResourceWithRawResponse(client.datasource_details)


class SupermetricsAsyncClientWithRawResponse:
    """Raw-response view over every resource of a asynchronous client.

    Reached through :attr:`SupermetricsAsyncClient.with_raw_response`.

    Args:
        client: The client whose resources should be mirrored.
    """

    def __init__(self, client: SupermetricsAsyncClient) -> None:
        """Build a raw-response view for each resource on ``client``."""
        self.login_links = LoginLinksAsyncResourceWithRawResponse(client.login_links)
        self.logins = LoginsAsyncResourceWithRawResponse(client.logins)
        self.accounts = AccountsAsyncResourceWithRawResponse(client.accounts)
        self.queries = QueriesAsyncResourceWithRawResponse(client.queries)
        self.backfills = BackfillsAsyncResourceWithRawResponse(client.backfills)
        self.connector_builder = ConnectorBuilderAsyncResourceWithRawResponse(client.connector_builder)
        self.connector_builder_secrets = ConnectorBuilderSecretsAsyncResourceWithRawResponse(
            client.connector_builder_secrets
        )
        self.connector_builder_logs = ConnectorBuilderLogsAsyncResourceWithRawResponse(client.connector_builder_logs)
        self.datasource_details = DatasourceDetailsAsyncResourceWithRawResponse(client.datasource_details)


__all__ = [
    "AccountsAsyncResourceWithRawResponse",
    "AccountsResourceWithRawResponse",
    "BackfillsAsyncResourceWithRawResponse",
    "BackfillsResourceWithRawResponse",
    "ConnectorBuilderAsyncResourceWithRawResponse",
    "ConnectorBuilderLogsAsyncResourceWithRawResponse",
    "ConnectorBuilderLogsResourceWithRawResponse",
    "ConnectorBuilderResourceWithRawResponse",
    "ConnectorBuilderSecretsAsyncResourceWithRawResponse",
    "ConnectorBuilderSecretsResourceWithRawResponse",
    "DatasourceDetailsAsyncResourceWithRawResponse",
    "DatasourceDetailsResourceWithRawResponse",
    "LoginLinksAsyncResourceWithRawResponse",
    "LoginLinksResourceWithRawResponse",
    "LoginsAsyncResourceWithRawResponse",
    "LoginsResourceWithRawResponse",
    "QueriesAsyncResourceWithRawResponse",
    "QueriesResourceWithRawResponse",
    "SupermetricsAsyncClientWithRawResponse",
    "SupermetricsClientWithRawResponse",
]
