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

from supermetrics.resources.account_tags import AccountTagsAsyncResource, AccountTagsResource
from supermetrics.resources.accounts import AccountsAsyncResource, AccountsResource
from supermetrics.resources.backfills import BackfillsAsyncResource, BackfillsResource
from supermetrics.resources.blends import BlendsAsyncResource, BlendsResource
from supermetrics.resources.connector_builder import ConnectorBuilderAsyncResource, ConnectorBuilderResource
from supermetrics.resources.connector_builder_logs import (
    ConnectorBuilderLogsAsyncResource,
    ConnectorBuilderLogsResource,
)
from supermetrics.resources.connector_builder_secrets import (
    ConnectorBuilderSecretsAsyncResource,
    ConnectorBuilderSecretsResource,
)
from supermetrics.resources.custom_fields import CustomFieldsAsyncResource, CustomFieldsResource
from supermetrics.resources.datasource_details import DatasourceDetailsAsyncResource, DatasourceDetailsResource
from supermetrics.resources.destinations import DestinationsAsyncResource, DestinationsResource
from supermetrics.resources.login_links import LoginLinksAsyncResource, LoginLinksResource
from supermetrics.resources.logins import LoginsAsyncResource, LoginsResource
from supermetrics.resources.queries import QueriesAsyncResource, QueriesResource
from supermetrics.resources.teams import TeamsAsyncResource, TeamsResource
from supermetrics.resources.transfer_runs import TransferRunsAsyncResource, TransferRunsResource
from supermetrics.resources.transfers import TransfersAsyncResource, TransfersResource
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


class DestinationsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.destinations.DestinationsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: DestinationsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)
        self.test_connection = to_raw_response_wrapper(resource.test_connection)
        self.get_usage = to_raw_response_wrapper(resource.get_usage)


class DestinationsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.destinations.DestinationsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: DestinationsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)
        self.test_connection = async_to_raw_response_wrapper(resource.test_connection)
        self.get_usage = async_to_raw_response_wrapper(resource.get_usage)


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
        self.update = to_raw_response_wrapper(resource.update)


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
        self.update = async_to_raw_response_wrapper(resource.update)


class LoginsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.logins.LoginsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: LoginsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = to_raw_response_wrapper(resource.get)
        self.list = to_raw_response_wrapper(resource.list)
        self.get_accounts = to_raw_response_wrapper(resource.get_accounts)
        self.revoke = to_raw_response_wrapper(resource.revoke)
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
        self.get_accounts = async_to_raw_response_wrapper(resource.get_accounts)
        self.revoke = async_to_raw_response_wrapper(resource.revoke)
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


class TransfersResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.transfers.TransfersResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: TransfersResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)
        self.set_state = to_raw_response_wrapper(resource.set_state)
        self.validate = to_raw_response_wrapper(resource.validate)
        self.validate_update = to_raw_response_wrapper(resource.validate_update)
        self.list_available_sources = to_raw_response_wrapper(resource.list_available_sources)
        self.get_available_options = to_raw_response_wrapper(resource.get_available_options)
        self.list_runs = to_raw_response_wrapper(resource.list_runs)
        self.create_datasource_connection = to_raw_response_wrapper(resource.create_datasource_connection)
        self.clone = to_raw_response_wrapper(resource.clone)
        self.batch_create = to_raw_response_wrapper(resource.batch_create)


class TransfersAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.transfers.TransfersAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: TransfersAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)
        self.set_state = async_to_raw_response_wrapper(resource.set_state)
        self.validate = async_to_raw_response_wrapper(resource.validate)
        self.validate_update = async_to_raw_response_wrapper(resource.validate_update)
        self.list_available_sources = async_to_raw_response_wrapper(resource.list_available_sources)
        self.get_available_options = async_to_raw_response_wrapper(resource.get_available_options)
        self.list_runs = async_to_raw_response_wrapper(resource.list_runs)
        self.create_datasource_connection = async_to_raw_response_wrapper(resource.create_datasource_connection)
        self.clone = async_to_raw_response_wrapper(resource.clone)
        self.batch_create = async_to_raw_response_wrapper(resource.batch_create)


class TransferRunsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.transfer_runs.TransferRunsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: TransferRunsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = to_raw_response_wrapper(resource.get)


class TransferRunsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.transfer_runs.TransferRunsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: TransferRunsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = async_to_raw_response_wrapper(resource.get)


class CustomFieldsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.custom_fields.CustomFieldsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: CustomFieldsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)
        self.get_metadata = to_raw_response_wrapper(resource.get_metadata)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)


class CustomFieldsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.custom_fields.CustomFieldsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: CustomFieldsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.get_metadata = async_to_raw_response_wrapper(resource.get_metadata)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)


class AccountTagsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.account_tags.AccountTagsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: AccountTagsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)
        self.add_accounts = to_raw_response_wrapper(resource.add_accounts)
        self.remove_accounts = to_raw_response_wrapper(resource.remove_accounts)


class AccountTagsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.account_tags.AccountTagsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: AccountTagsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)
        self.add_accounts = async_to_raw_response_wrapper(resource.add_accounts)
        self.remove_accounts = async_to_raw_response_wrapper(resource.remove_accounts)


class BlendsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.blends.BlendsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: BlendsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = to_raw_response_wrapper(resource.list)
        self.get = to_raw_response_wrapper(resource.get)
        self.create = to_raw_response_wrapper(resource.create)
        self.update = to_raw_response_wrapper(resource.update)
        self.delete = to_raw_response_wrapper(resource.delete)


class BlendsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.blends.BlendsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: BlendsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.list = async_to_raw_response_wrapper(resource.list)
        self.get = async_to_raw_response_wrapper(resource.get)
        self.create = async_to_raw_response_wrapper(resource.create)
        self.update = async_to_raw_response_wrapper(resource.update)
        self.delete = async_to_raw_response_wrapper(resource.delete)


class TeamsResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.teams.TeamsResource`.

    Args:
        resource: The synchronous resource adapter to mirror.
    """

    def __init__(self, resource: TeamsResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = to_raw_response_wrapper(resource.get)
        self.list_users = to_raw_response_wrapper(resource.list_users)


class TeamsAsyncResourceWithRawResponse:
    """Raw-response view over :class:`~supermetrics.resources.teams.TeamsAsyncResource`.

    Args:
        resource: The asynchronous resource adapter to mirror.
    """

    def __init__(self, resource: TeamsAsyncResource) -> None:
        """Wrap every method of ``resource`` to return an ``ApiResponse``."""
        self.get = async_to_raw_response_wrapper(resource.get)
        self.list_users = async_to_raw_response_wrapper(resource.list_users)


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
        self.destinations = DestinationsResourceWithRawResponse(client.destinations)
        self.transfers = TransfersResourceWithRawResponse(client.transfers)
        self.transfer_runs = TransferRunsResourceWithRawResponse(client.transfer_runs)
        self.custom_fields = CustomFieldsResourceWithRawResponse(client.custom_fields)
        self.account_tags = AccountTagsResourceWithRawResponse(client.account_tags)
        self.blends = BlendsResourceWithRawResponse(client.blends)
        self.teams = TeamsResourceWithRawResponse(client.teams)


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
        self.destinations = DestinationsAsyncResourceWithRawResponse(client.destinations)
        self.transfers = TransfersAsyncResourceWithRawResponse(client.transfers)
        self.transfer_runs = TransferRunsAsyncResourceWithRawResponse(client.transfer_runs)
        self.custom_fields = CustomFieldsAsyncResourceWithRawResponse(client.custom_fields)
        self.account_tags = AccountTagsAsyncResourceWithRawResponse(client.account_tags)
        self.blends = BlendsAsyncResourceWithRawResponse(client.blends)
        self.teams = TeamsAsyncResourceWithRawResponse(client.teams)


__all__ = [
    "AccountTagsAsyncResourceWithRawResponse",
    "AccountTagsResourceWithRawResponse",
    "AccountsAsyncResourceWithRawResponse",
    "AccountsResourceWithRawResponse",
    "BackfillsAsyncResourceWithRawResponse",
    "BackfillsResourceWithRawResponse",
    "BlendsAsyncResourceWithRawResponse",
    "BlendsResourceWithRawResponse",
    "ConnectorBuilderAsyncResourceWithRawResponse",
    "ConnectorBuilderLogsAsyncResourceWithRawResponse",
    "ConnectorBuilderLogsResourceWithRawResponse",
    "ConnectorBuilderResourceWithRawResponse",
    "ConnectorBuilderSecretsAsyncResourceWithRawResponse",
    "ConnectorBuilderSecretsResourceWithRawResponse",
    "CustomFieldsAsyncResourceWithRawResponse",
    "CustomFieldsResourceWithRawResponse",
    "DatasourceDetailsAsyncResourceWithRawResponse",
    "DatasourceDetailsResourceWithRawResponse",
    "DestinationsAsyncResourceWithRawResponse",
    "DestinationsResourceWithRawResponse",
    "LoginLinksAsyncResourceWithRawResponse",
    "LoginLinksResourceWithRawResponse",
    "LoginsAsyncResourceWithRawResponse",
    "LoginsResourceWithRawResponse",
    "QueriesAsyncResourceWithRawResponse",
    "QueriesResourceWithRawResponse",
    "SupermetricsAsyncClientWithRawResponse",
    "SupermetricsClientWithRawResponse",
    "TeamsAsyncResourceWithRawResponse",
    "TeamsResourceWithRawResponse",
    "TransferRunsAsyncResourceWithRawResponse",
    "TransferRunsResourceWithRawResponse",
    "TransfersAsyncResourceWithRawResponse",
    "TransfersResourceWithRawResponse",
]
