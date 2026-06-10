"""Contains all the data models used in inputs/outputs"""

from .backfill import Backfill
from .backfill_response import BackfillResponse
from .backfill_status import BackfillStatus
from .close_login_link_response_401 import CloseLoginLinkResponse401
from .close_login_link_response_401_meta import CloseLoginLinkResponse401Meta
from .close_login_link_response_404 import CloseLoginLinkResponse404
from .close_login_link_response_404_error import CloseLoginLinkResponse404Error
from .close_login_link_response_429 import CloseLoginLinkResponse429
from .close_login_link_response_429_meta import CloseLoginLinkResponse429Meta
from .close_login_link_response_500 import CloseLoginLinkResponse500
from .close_login_link_response_500_error import CloseLoginLinkResponse500Error
from .connector import Connector
from .connector_configuration import ConnectorConfiguration
from .connector_configuration_configuration_json import ConnectorConfigurationConfigurationJson
from .connector_with_configuration import ConnectorWithConfiguration
from .create_backfill_request import CreateBackfillRequest
from .create_connector_body import CreateConnectorBody
from .create_connector_response_401 import CreateConnectorResponse401
from .create_connector_response_401_meta import CreateConnectorResponse401Meta
from .create_connector_response_404 import CreateConnectorResponse404
from .create_connector_response_404_meta import CreateConnectorResponse404Meta
from .create_connector_response_429 import CreateConnectorResponse429
from .create_connector_response_429_meta import CreateConnectorResponse429Meta
from .create_connector_response_500 import CreateConnectorResponse500
from .create_connector_response_500_meta import CreateConnectorResponse500Meta
from .create_connector_secret_response_201 import CreateConnectorSecretResponse201
from .create_connector_secret_response_400 import CreateConnectorSecretResponse400
from .create_connector_secret_response_400_meta import CreateConnectorSecretResponse400Meta
from .create_connector_secret_response_401 import CreateConnectorSecretResponse401
from .create_connector_secret_response_401_meta import CreateConnectorSecretResponse401Meta
from .create_connector_secret_response_404 import CreateConnectorSecretResponse404
from .create_connector_secret_response_404_meta import CreateConnectorSecretResponse404Meta
from .create_connector_secret_response_409 import CreateConnectorSecretResponse409
from .create_connector_secret_response_409_meta import CreateConnectorSecretResponse409Meta
from .create_connector_secret_response_429 import CreateConnectorSecretResponse429
from .create_connector_secret_response_429_meta import CreateConnectorSecretResponse429Meta
from .create_connector_secret_response_500 import CreateConnectorSecretResponse500
from .create_connector_secret_response_500_meta import CreateConnectorSecretResponse500Meta
from .create_login_link_body import CreateLoginLinkBody
from .create_login_link_response_401 import CreateLoginLinkResponse401
from .create_login_link_response_401_meta import CreateLoginLinkResponse401Meta
from .create_login_link_response_403 import CreateLoginLinkResponse403
from .create_login_link_response_403_error import CreateLoginLinkResponse403Error
from .create_login_link_response_429 import CreateLoginLinkResponse429
from .create_login_link_response_429_meta import CreateLoginLinkResponse429Meta
from .create_login_link_response_500 import CreateLoginLinkResponse500
from .create_login_link_response_500_meta import CreateLoginLinkResponse500Meta
from .create_secret_request import CreateSecretRequest
from .data_query import DataQuery
from .data_query_ds_accounts_type_2 import DataQueryDsAccountsType2
from .data_query_fields_type_2_item import DataQueryFieldsType2Item
from .data_query_settings import DataQuerySettings
from .data_response import DataResponse
from .data_response_meta import DataResponseMeta
from .data_response_meta_paginate import DataResponseMetaPaginate
from .data_response_meta_query import DataResponseMetaQuery
from .data_response_meta_query_fields_item import DataResponseMetaQueryFieldsItem
from .data_response_meta_query_settings import DataResponseMetaQuerySettings
from .data_response_meta_result import DataResponseMetaResult
from .data_source import DataSource
from .data_source_login import DataSourceLogin
from .data_source_login_type import DataSourceLoginType
from .data_source_type import DataSourceType
from .datasource_details import DatasourceDetails
from .datasource_details_account_labels_type_0 import DatasourceDetailsAccountLabelsType0
from .datasource_details_categories_item import DatasourceDetailsCategoriesItem
from .datasource_details_response import DatasourceDetailsResponse
from .datasource_details_status import DatasourceDetailsStatus
from .datasource_option import DatasourceOption
from .datasource_report_type import DatasourceReportType
from .datasource_setting import DatasourceSetting
from .datasource_setting_context import DatasourceSettingContext
from .datasource_setting_type import DatasourceSettingType
from .delete_connector_response_400 import DeleteConnectorResponse400
from .delete_connector_response_400_meta import DeleteConnectorResponse400Meta
from .delete_connector_response_401 import DeleteConnectorResponse401
from .delete_connector_response_401_meta import DeleteConnectorResponse401Meta
from .delete_connector_response_404 import DeleteConnectorResponse404
from .delete_connector_response_404_meta import DeleteConnectorResponse404Meta
from .delete_connector_response_429 import DeleteConnectorResponse429
from .delete_connector_response_429_meta import DeleteConnectorResponse429Meta
from .delete_connector_response_500 import DeleteConnectorResponse500
from .delete_connector_response_500_meta import DeleteConnectorResponse500Meta
from .delete_connector_secret_response_401 import DeleteConnectorSecretResponse401
from .delete_connector_secret_response_401_meta import DeleteConnectorSecretResponse401Meta
from .delete_connector_secret_response_404 import DeleteConnectorSecretResponse404
from .delete_connector_secret_response_404_meta import DeleteConnectorSecretResponse404Meta
from .delete_connector_secret_response_429 import DeleteConnectorSecretResponse429
from .delete_connector_secret_response_429_meta import DeleteConnectorSecretResponse429Meta
from .delete_connector_secret_response_500 import DeleteConnectorSecretResponse500
from .delete_connector_secret_response_500_meta import DeleteConnectorSecretResponse500Meta
from .error import Error
from .error_response import ErrorResponse
from .get_accounts_json import GetAccountsJson
from .get_accounts_response_200 import GetAccountsResponse200
from .get_accounts_response_200_data_item import GetAccountsResponse200DataItem
from .get_accounts_response_200_data_item_accounts_item import GetAccountsResponse200DataItemAccountsItem
from .get_accounts_response_200_meta import GetAccountsResponse200Meta
from .get_accounts_response_200_meta_query import GetAccountsResponse200MetaQuery
from .get_accounts_response_400 import GetAccountsResponse400
from .get_accounts_response_400_meta import GetAccountsResponse400Meta
from .get_accounts_response_401 import GetAccountsResponse401
from .get_accounts_response_401_meta import GetAccountsResponse401Meta
from .get_accounts_response_429 import GetAccountsResponse429
from .get_accounts_response_429_meta import GetAccountsResponse429Meta
from .get_accounts_response_500 import GetAccountsResponse500
from .get_accounts_response_500_meta import GetAccountsResponse500Meta
from .get_connector_log_response_401 import GetConnectorLogResponse401
from .get_connector_log_response_401_meta import GetConnectorLogResponse401Meta
from .get_connector_log_response_404 import GetConnectorLogResponse404
from .get_connector_log_response_404_meta import GetConnectorLogResponse404Meta
from .get_connector_log_response_429 import GetConnectorLogResponse429
from .get_connector_log_response_429_meta import GetConnectorLogResponse429Meta
from .get_connector_log_response_500 import GetConnectorLogResponse500
from .get_connector_log_response_500_meta import GetConnectorLogResponse500Meta
from .get_connector_logo_response_200 import GetConnectorLogoResponse200
from .get_connector_logo_response_401 import GetConnectorLogoResponse401
from .get_connector_logo_response_401_meta import GetConnectorLogoResponse401Meta
from .get_connector_logo_response_404 import GetConnectorLogoResponse404
from .get_connector_logo_response_404_meta import GetConnectorLogoResponse404Meta
from .get_connector_logo_response_429 import GetConnectorLogoResponse429
from .get_connector_logo_response_429_meta import GetConnectorLogoResponse429Meta
from .get_connector_logo_response_500 import GetConnectorLogoResponse500
from .get_connector_logo_response_500_meta import GetConnectorLogoResponse500Meta
from .get_connector_response_400 import GetConnectorResponse400
from .get_connector_response_400_meta import GetConnectorResponse400Meta
from .get_connector_response_401 import GetConnectorResponse401
from .get_connector_response_401_meta import GetConnectorResponse401Meta
from .get_connector_response_404 import GetConnectorResponse404
from .get_connector_response_404_meta import GetConnectorResponse404Meta
from .get_connector_response_429 import GetConnectorResponse429
from .get_connector_response_429_meta import GetConnectorResponse429Meta
from .get_connector_response_500 import GetConnectorResponse500
from .get_connector_response_500_meta import GetConnectorResponse500Meta
from .get_data_response_400 import GetDataResponse400
from .get_data_response_400_meta import GetDataResponse400Meta
from .get_data_response_401 import GetDataResponse401
from .get_data_response_401_meta import GetDataResponse401Meta
from .get_data_response_429 import GetDataResponse429
from .get_data_response_429_meta import GetDataResponse429Meta
from .get_data_response_500 import GetDataResponse500
from .get_data_response_500_meta import GetDataResponse500Meta
from .get_data_source_login_response_200 import GetDataSourceLoginResponse200
from .get_data_source_login_response_401 import GetDataSourceLoginResponse401
from .get_data_source_login_response_401_meta import GetDataSourceLoginResponse401Meta
from .get_data_source_login_response_404 import GetDataSourceLoginResponse404
from .get_data_source_login_response_404_error import GetDataSourceLoginResponse404Error
from .get_data_source_login_response_429 import GetDataSourceLoginResponse429
from .get_data_source_login_response_429_meta import GetDataSourceLoginResponse429Meta
from .get_data_source_login_response_500 import GetDataSourceLoginResponse500
from .get_data_source_login_response_500_error import GetDataSourceLoginResponse500Error
from .get_datasource_details_response_400 import GetDatasourceDetailsResponse400
from .get_datasource_details_response_400_meta import GetDatasourceDetailsResponse400Meta
from .get_datasource_details_response_401 import GetDatasourceDetailsResponse401
from .get_datasource_details_response_401_meta import GetDatasourceDetailsResponse401Meta
from .get_datasource_details_response_404 import GetDatasourceDetailsResponse404
from .get_datasource_details_response_404_meta import GetDatasourceDetailsResponse404Meta
from .get_datasource_details_response_429 import GetDatasourceDetailsResponse429
from .get_datasource_details_response_429_meta import GetDatasourceDetailsResponse429Meta
from .get_datasource_details_response_500 import GetDatasourceDetailsResponse500
from .get_datasource_details_response_500_meta import GetDatasourceDetailsResponse500Meta
from .get_login_link_response_401 import GetLoginLinkResponse401
from .get_login_link_response_401_meta import GetLoginLinkResponse401Meta
from .get_login_link_response_404 import GetLoginLinkResponse404
from .get_login_link_response_404_error import GetLoginLinkResponse404Error
from .get_login_link_response_429 import GetLoginLinkResponse429
from .get_login_link_response_429_meta import GetLoginLinkResponse429Meta
from .get_login_link_response_500 import GetLoginLinkResponse500
from .get_login_link_response_500_meta import GetLoginLinkResponse500Meta
from .list_connector_logs_response_200 import ListConnectorLogsResponse200
from .list_connector_logs_response_400 import ListConnectorLogsResponse400
from .list_connector_logs_response_400_meta import ListConnectorLogsResponse400Meta
from .list_connector_logs_response_401 import ListConnectorLogsResponse401
from .list_connector_logs_response_401_meta import ListConnectorLogsResponse401Meta
from .list_connector_logs_response_429 import ListConnectorLogsResponse429
from .list_connector_logs_response_429_meta import ListConnectorLogsResponse429Meta
from .list_connector_logs_response_500 import ListConnectorLogsResponse500
from .list_connector_logs_response_500_meta import ListConnectorLogsResponse500Meta
from .list_connector_secrets_response_200 import ListConnectorSecretsResponse200
from .list_connector_secrets_response_401 import ListConnectorSecretsResponse401
from .list_connector_secrets_response_401_meta import ListConnectorSecretsResponse401Meta
from .list_connector_secrets_response_404 import ListConnectorSecretsResponse404
from .list_connector_secrets_response_404_meta import ListConnectorSecretsResponse404Meta
from .list_connector_secrets_response_429 import ListConnectorSecretsResponse429
from .list_connector_secrets_response_429_meta import ListConnectorSecretsResponse429Meta
from .list_connector_secrets_response_500 import ListConnectorSecretsResponse500
from .list_connector_secrets_response_500_meta import ListConnectorSecretsResponse500Meta
from .list_connectors_response_200 import ListConnectorsResponse200
from .list_connectors_response_401 import ListConnectorsResponse401
from .list_connectors_response_401_meta import ListConnectorsResponse401Meta
from .list_connectors_response_429 import ListConnectorsResponse429
from .list_connectors_response_429_meta import ListConnectorsResponse429Meta
from .list_connectors_response_500 import ListConnectorsResponse500
from .list_connectors_response_500_meta import ListConnectorsResponse500Meta
from .list_data_source_logins_response_200 import ListDataSourceLoginsResponse200
from .list_data_source_logins_response_401 import ListDataSourceLoginsResponse401
from .list_data_source_logins_response_401_meta import ListDataSourceLoginsResponse401Meta
from .list_data_source_logins_response_429 import ListDataSourceLoginsResponse429
from .list_data_source_logins_response_429_meta import ListDataSourceLoginsResponse429Meta
from .list_data_source_logins_response_500 import ListDataSourceLoginsResponse500
from .list_data_source_logins_response_500_error import ListDataSourceLoginsResponse500Error
from .list_incomplete_backfills_response_200 import ListIncompleteBackfillsResponse200
from .list_login_links_response_200 import ListLoginLinksResponse200
from .list_login_links_response_401 import ListLoginLinksResponse401
from .list_login_links_response_401_meta import ListLoginLinksResponse401Meta
from .list_login_links_response_429 import ListLoginLinksResponse429
from .list_login_links_response_429_meta import ListLoginLinksResponse429Meta
from .list_login_links_response_500 import ListLoginLinksResponse500
from .list_login_links_response_500_meta import ListLoginLinksResponse500Meta
from .log_entry import LogEntry
from .login_link import LoginLink
from .login_link_response import LoginLinkResponse
from .login_link_status_code import LoginLinkStatusCode
from .response_meta import ResponseMeta
from .secret import Secret
from .transfer_backfill_run_error import TransferBackfillRunError
from .update_backfill_status_body import UpdateBackfillStatusBody
from .update_backfill_status_body_status import UpdateBackfillStatusBodyStatus
from .update_connector_request import UpdateConnectorRequest
from .update_connector_request_configuration import UpdateConnectorRequestConfiguration
from .update_connector_request_configuration_configuration_json import (
    UpdateConnectorRequestConfigurationConfigurationJson,
)
from .update_connector_request_connector import UpdateConnectorRequestConnector
from .update_connector_response_400 import UpdateConnectorResponse400
from .update_connector_response_400_meta import UpdateConnectorResponse400Meta
from .update_connector_response_401 import UpdateConnectorResponse401
from .update_connector_response_401_meta import UpdateConnectorResponse401Meta
from .update_connector_response_404 import UpdateConnectorResponse404
from .update_connector_response_404_meta import UpdateConnectorResponse404Meta
from .update_connector_response_429 import UpdateConnectorResponse429
from .update_connector_response_429_meta import UpdateConnectorResponse429Meta
from .update_connector_response_500 import UpdateConnectorResponse500
from .update_connector_response_500_meta import UpdateConnectorResponse500Meta
from .update_connector_secret_response_400 import UpdateConnectorSecretResponse400
from .update_connector_secret_response_400_meta import UpdateConnectorSecretResponse400Meta
from .update_connector_secret_response_401 import UpdateConnectorSecretResponse401
from .update_connector_secret_response_401_meta import UpdateConnectorSecretResponse401Meta
from .update_connector_secret_response_404 import UpdateConnectorSecretResponse404
from .update_connector_secret_response_404_meta import UpdateConnectorSecretResponse404Meta
from .update_connector_secret_response_429 import UpdateConnectorSecretResponse429
from .update_connector_secret_response_429_meta import UpdateConnectorSecretResponse429Meta
from .update_connector_secret_response_500 import UpdateConnectorSecretResponse500
from .update_connector_secret_response_500_meta import UpdateConnectorSecretResponse500Meta
from .update_secret_request import UpdateSecretRequest
from .upload_connector_logo_body import UploadConnectorLogoBody
from .upload_connector_logo_response_201 import UploadConnectorLogoResponse201
from .upload_connector_logo_response_400 import UploadConnectorLogoResponse400
from .upload_connector_logo_response_400_meta import UploadConnectorLogoResponse400Meta
from .upload_connector_logo_response_401 import UploadConnectorLogoResponse401
from .upload_connector_logo_response_401_meta import UploadConnectorLogoResponse401Meta
from .upload_connector_logo_response_404 import UploadConnectorLogoResponse404
from .upload_connector_logo_response_404_meta import UploadConnectorLogoResponse404Meta
from .upload_connector_logo_response_429 import UploadConnectorLogoResponse429
from .upload_connector_logo_response_429_meta import UploadConnectorLogoResponse429Meta
from .upload_connector_logo_response_500 import UploadConnectorLogoResponse500
from .upload_connector_logo_response_500_meta import UploadConnectorLogoResponse500Meta
from .user import User
from .user_type import UserType

__all__ = (
    "Backfill",
    "BackfillResponse",
    "BackfillStatus",
    "CloseLoginLinkResponse401",
    "CloseLoginLinkResponse401Meta",
    "CloseLoginLinkResponse404",
    "CloseLoginLinkResponse404Error",
    "CloseLoginLinkResponse429",
    "CloseLoginLinkResponse429Meta",
    "CloseLoginLinkResponse500",
    "CloseLoginLinkResponse500Error",
    "Connector",
    "ConnectorConfiguration",
    "ConnectorConfigurationConfigurationJson",
    "ConnectorWithConfiguration",
    "CreateBackfillRequest",
    "CreateConnectorBody",
    "CreateConnectorResponse401",
    "CreateConnectorResponse401Meta",
    "CreateConnectorResponse404",
    "CreateConnectorResponse404Meta",
    "CreateConnectorResponse429",
    "CreateConnectorResponse429Meta",
    "CreateConnectorResponse500",
    "CreateConnectorResponse500Meta",
    "CreateConnectorSecretResponse201",
    "CreateConnectorSecretResponse400",
    "CreateConnectorSecretResponse400Meta",
    "CreateConnectorSecretResponse401",
    "CreateConnectorSecretResponse401Meta",
    "CreateConnectorSecretResponse404",
    "CreateConnectorSecretResponse404Meta",
    "CreateConnectorSecretResponse409",
    "CreateConnectorSecretResponse409Meta",
    "CreateConnectorSecretResponse429",
    "CreateConnectorSecretResponse429Meta",
    "CreateConnectorSecretResponse500",
    "CreateConnectorSecretResponse500Meta",
    "CreateLoginLinkBody",
    "CreateLoginLinkResponse401",
    "CreateLoginLinkResponse401Meta",
    "CreateLoginLinkResponse403",
    "CreateLoginLinkResponse403Error",
    "CreateLoginLinkResponse429",
    "CreateLoginLinkResponse429Meta",
    "CreateLoginLinkResponse500",
    "CreateLoginLinkResponse500Meta",
    "CreateSecretRequest",
    "DataQuery",
    "DataQueryDsAccountsType2",
    "DataQueryFieldsType2Item",
    "DataQuerySettings",
    "DataResponse",
    "DataResponseMeta",
    "DataResponseMetaPaginate",
    "DataResponseMetaQuery",
    "DataResponseMetaQueryFieldsItem",
    "DataResponseMetaQuerySettings",
    "DataResponseMetaResult",
    "DataSource",
    "DatasourceDetails",
    "DatasourceDetailsAccountLabelsType0",
    "DatasourceDetailsCategoriesItem",
    "DatasourceDetailsResponse",
    "DatasourceDetailsStatus",
    "DataSourceLogin",
    "DataSourceLoginType",
    "DatasourceOption",
    "DatasourceReportType",
    "DatasourceSetting",
    "DatasourceSettingContext",
    "DatasourceSettingType",
    "DataSourceType",
    "DeleteConnectorResponse400",
    "DeleteConnectorResponse400Meta",
    "DeleteConnectorResponse401",
    "DeleteConnectorResponse401Meta",
    "DeleteConnectorResponse404",
    "DeleteConnectorResponse404Meta",
    "DeleteConnectorResponse429",
    "DeleteConnectorResponse429Meta",
    "DeleteConnectorResponse500",
    "DeleteConnectorResponse500Meta",
    "DeleteConnectorSecretResponse401",
    "DeleteConnectorSecretResponse401Meta",
    "DeleteConnectorSecretResponse404",
    "DeleteConnectorSecretResponse404Meta",
    "DeleteConnectorSecretResponse429",
    "DeleteConnectorSecretResponse429Meta",
    "DeleteConnectorSecretResponse500",
    "DeleteConnectorSecretResponse500Meta",
    "Error",
    "ErrorResponse",
    "GetAccountsJson",
    "GetAccountsResponse200",
    "GetAccountsResponse200DataItem",
    "GetAccountsResponse200DataItemAccountsItem",
    "GetAccountsResponse200Meta",
    "GetAccountsResponse200MetaQuery",
    "GetAccountsResponse400",
    "GetAccountsResponse400Meta",
    "GetAccountsResponse401",
    "GetAccountsResponse401Meta",
    "GetAccountsResponse429",
    "GetAccountsResponse429Meta",
    "GetAccountsResponse500",
    "GetAccountsResponse500Meta",
    "GetConnectorLogoResponse200",
    "GetConnectorLogoResponse401",
    "GetConnectorLogoResponse401Meta",
    "GetConnectorLogoResponse404",
    "GetConnectorLogoResponse404Meta",
    "GetConnectorLogoResponse429",
    "GetConnectorLogoResponse429Meta",
    "GetConnectorLogoResponse500",
    "GetConnectorLogoResponse500Meta",
    "GetConnectorLogResponse401",
    "GetConnectorLogResponse401Meta",
    "GetConnectorLogResponse404",
    "GetConnectorLogResponse404Meta",
    "GetConnectorLogResponse429",
    "GetConnectorLogResponse429Meta",
    "GetConnectorLogResponse500",
    "GetConnectorLogResponse500Meta",
    "GetConnectorResponse400",
    "GetConnectorResponse400Meta",
    "GetConnectorResponse401",
    "GetConnectorResponse401Meta",
    "GetConnectorResponse404",
    "GetConnectorResponse404Meta",
    "GetConnectorResponse429",
    "GetConnectorResponse429Meta",
    "GetConnectorResponse500",
    "GetConnectorResponse500Meta",
    "GetDataResponse400",
    "GetDataResponse400Meta",
    "GetDataResponse401",
    "GetDataResponse401Meta",
    "GetDataResponse429",
    "GetDataResponse429Meta",
    "GetDataResponse500",
    "GetDataResponse500Meta",
    "GetDatasourceDetailsResponse400",
    "GetDatasourceDetailsResponse400Meta",
    "GetDatasourceDetailsResponse401",
    "GetDatasourceDetailsResponse401Meta",
    "GetDatasourceDetailsResponse404",
    "GetDatasourceDetailsResponse404Meta",
    "GetDatasourceDetailsResponse429",
    "GetDatasourceDetailsResponse429Meta",
    "GetDatasourceDetailsResponse500",
    "GetDatasourceDetailsResponse500Meta",
    "GetDataSourceLoginResponse200",
    "GetDataSourceLoginResponse401",
    "GetDataSourceLoginResponse401Meta",
    "GetDataSourceLoginResponse404",
    "GetDataSourceLoginResponse404Error",
    "GetDataSourceLoginResponse429",
    "GetDataSourceLoginResponse429Meta",
    "GetDataSourceLoginResponse500",
    "GetDataSourceLoginResponse500Error",
    "GetLoginLinkResponse401",
    "GetLoginLinkResponse401Meta",
    "GetLoginLinkResponse404",
    "GetLoginLinkResponse404Error",
    "GetLoginLinkResponse429",
    "GetLoginLinkResponse429Meta",
    "GetLoginLinkResponse500",
    "GetLoginLinkResponse500Meta",
    "ListConnectorLogsResponse200",
    "ListConnectorLogsResponse400",
    "ListConnectorLogsResponse400Meta",
    "ListConnectorLogsResponse401",
    "ListConnectorLogsResponse401Meta",
    "ListConnectorLogsResponse429",
    "ListConnectorLogsResponse429Meta",
    "ListConnectorLogsResponse500",
    "ListConnectorLogsResponse500Meta",
    "ListConnectorSecretsResponse200",
    "ListConnectorSecretsResponse401",
    "ListConnectorSecretsResponse401Meta",
    "ListConnectorSecretsResponse404",
    "ListConnectorSecretsResponse404Meta",
    "ListConnectorSecretsResponse429",
    "ListConnectorSecretsResponse429Meta",
    "ListConnectorSecretsResponse500",
    "ListConnectorSecretsResponse500Meta",
    "ListConnectorsResponse200",
    "ListConnectorsResponse401",
    "ListConnectorsResponse401Meta",
    "ListConnectorsResponse429",
    "ListConnectorsResponse429Meta",
    "ListConnectorsResponse500",
    "ListConnectorsResponse500Meta",
    "ListDataSourceLoginsResponse200",
    "ListDataSourceLoginsResponse401",
    "ListDataSourceLoginsResponse401Meta",
    "ListDataSourceLoginsResponse429",
    "ListDataSourceLoginsResponse429Meta",
    "ListDataSourceLoginsResponse500",
    "ListDataSourceLoginsResponse500Error",
    "ListIncompleteBackfillsResponse200",
    "ListLoginLinksResponse200",
    "ListLoginLinksResponse401",
    "ListLoginLinksResponse401Meta",
    "ListLoginLinksResponse429",
    "ListLoginLinksResponse429Meta",
    "ListLoginLinksResponse500",
    "ListLoginLinksResponse500Meta",
    "LogEntry",
    "LoginLink",
    "LoginLinkResponse",
    "LoginLinkStatusCode",
    "ResponseMeta",
    "Secret",
    "TransferBackfillRunError",
    "UpdateBackfillStatusBody",
    "UpdateBackfillStatusBodyStatus",
    "UpdateConnectorRequest",
    "UpdateConnectorRequestConfiguration",
    "UpdateConnectorRequestConfigurationConfigurationJson",
    "UpdateConnectorRequestConnector",
    "UpdateConnectorResponse400",
    "UpdateConnectorResponse400Meta",
    "UpdateConnectorResponse401",
    "UpdateConnectorResponse401Meta",
    "UpdateConnectorResponse404",
    "UpdateConnectorResponse404Meta",
    "UpdateConnectorResponse429",
    "UpdateConnectorResponse429Meta",
    "UpdateConnectorResponse500",
    "UpdateConnectorResponse500Meta",
    "UpdateConnectorSecretResponse400",
    "UpdateConnectorSecretResponse400Meta",
    "UpdateConnectorSecretResponse401",
    "UpdateConnectorSecretResponse401Meta",
    "UpdateConnectorSecretResponse404",
    "UpdateConnectorSecretResponse404Meta",
    "UpdateConnectorSecretResponse429",
    "UpdateConnectorSecretResponse429Meta",
    "UpdateConnectorSecretResponse500",
    "UpdateConnectorSecretResponse500Meta",
    "UpdateSecretRequest",
    "UploadConnectorLogoBody",
    "UploadConnectorLogoResponse201",
    "UploadConnectorLogoResponse400",
    "UploadConnectorLogoResponse400Meta",
    "UploadConnectorLogoResponse401",
    "UploadConnectorLogoResponse401Meta",
    "UploadConnectorLogoResponse404",
    "UploadConnectorLogoResponse404Meta",
    "UploadConnectorLogoResponse429",
    "UploadConnectorLogoResponse429Meta",
    "UploadConnectorLogoResponse500",
    "UploadConnectorLogoResponse500Meta",
    "User",
    "UserType",
)
