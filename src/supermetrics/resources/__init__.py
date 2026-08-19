"""Resource adapters for Supermetrics API.

This package contains hand-written resource adapters that provide a stable,
Pythonic interface to the Supermetrics API. These adapters wrap the
auto-generated code in _generated/ to provide:

- Stable public API that won't break on OpenAPI regeneration
- Clean, intuitive method signatures
- Comprehensive error handling
- Complete type safety with IDE autocomplete support
"""

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
from supermetrics.resources.transfer_runs import TransferRunsAsyncResource, TransferRunsResource
from supermetrics.resources.transfers import TransfersAsyncResource, TransfersResource

__all__ = [
    "AccountTagsResource",
    "AccountTagsAsyncResource",
    "AccountsResource",
    "AccountsAsyncResource",
    "BackfillsResource",
    "BackfillsAsyncResource",
    "BlendsResource",
    "BlendsAsyncResource",
    "ConnectorBuilderResource",
    "ConnectorBuilderAsyncResource",
    "ConnectorBuilderSecretsResource",
    "ConnectorBuilderSecretsAsyncResource",
    "ConnectorBuilderLogsResource",
    "ConnectorBuilderLogsAsyncResource",
    "CustomFieldsResource",
    "CustomFieldsAsyncResource",
    "DatasourceDetailsResource",
    "DatasourceDetailsAsyncResource",
    "DestinationsResource",
    "DestinationsAsyncResource",
    "LoginLinksResource",
    "LoginLinksAsyncResource",
    "LoginsResource",
    "LoginsAsyncResource",
    "QueriesResource",
    "QueriesAsyncResource",
    "TransfersResource",
    "TransfersAsyncResource",
    "TransferRunsResource",
    "TransferRunsAsyncResource",
]
