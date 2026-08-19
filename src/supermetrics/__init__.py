"""Official Python SDK for Supermetrics API."""

from supermetrics.__version__ import __version__
from supermetrics._auth import AsyncTokenProvider, TokenProvider
from supermetrics._generated.supermetrics_api_client.models.condition_case import ConditionCase
from supermetrics._generated.supermetrics_api_client.models.condition_case_condition import ConditionCaseCondition
from supermetrics._generated.supermetrics_api_client.models.condition_step import ConditionStep
from supermetrics._generated.supermetrics_api_client.models.custom_field_create_request_data_source_item import (
    CustomFieldCreateRequestDataSourceItem,
)
from supermetrics._generated.supermetrics_api_client.models.definition_value import DefinitionValue
from supermetrics._generated.supermetrics_api_client.models.function_argument import FunctionArgument
from supermetrics._generated.supermetrics_api_client.models.function_step import FunctionStep
from supermetrics._generated.supermetrics_api_client.models.lookup_step import LookupStep
from supermetrics._generated.supermetrics_api_client.models.lookup_step_map import LookupStepMap
from supermetrics._generated.supermetrics_api_client.models.transfer_account import TransferAccount
from supermetrics._generated.supermetrics_api_client.models.transfer_data_source_setting import (
    TransferDataSourceSetting,
)
from supermetrics._generated.supermetrics_api_client.models.transfer_schedule import TransferSchedule
from supermetrics._generated.supermetrics_api_client.models.transfer_segment import TransferSegment
from supermetrics._transport import (
    current_auth_token,
    current_request_headers,
    current_request_timeout,
    request_options,
)
from supermetrics.async_client import SupermetricsAsyncClient
from supermetrics.client import SupermetricsClient
from supermetrics.exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    SupermetricsAPIError,
    SupermetricsAuthError,
    SupermetricsClientError,
    SupermetricsError,
    SupermetricsForbiddenError,
    SupermetricsNotFoundError,
    SupermetricsRateLimitError,
    SupermetricsServerError,
    SupermetricsValidationError,
    ValidationError,
)
from supermetrics.response import ApiResponse

__author__ = "Supermetrics"
__email__ = "opensource@supermetrics.com"

__all__ = [
    # Clients
    "SupermetricsClient",
    "SupermetricsAsyncClient",
    "__version__",
    # Authentication
    "TokenProvider",
    "AsyncTokenProvider",
    # Transport
    "ApiResponse",
    "request_options",
    "current_auth_token",
    "current_request_headers",
    "current_request_timeout",
    # Request models a caller has to construct.
    #
    # The SDK does not otherwise re-export generated models: they are values you get
    # back from a call, so there is nothing to import. These are different —
    # transfers.create / update / validate / validate_update and
    # custom_fields.create / update cannot be called without building them, and a
    # public signature that can only be satisfied by importing from a private,
    # underscore-prefixed package is not a public signature.
    "TransferSchedule",
    "TransferAccount",
    "TransferSegment",
    "TransferDataSourceSetting",
    # Custom field definition steps. A `definition` is a list of these, and each step
    # nests the value/argument types below it.
    "FunctionStep",
    "LookupStep",
    "ConditionStep",
    "DefinitionValue",
    "FunctionArgument",
    "ConditionCase",
    "ConditionCaseCondition",
    "LookupStepMap",
    "CustomFieldCreateRequestDataSourceItem",
    # Exceptions
    "SupermetricsError",
    "SupermetricsClientError",
    "NetworkError",
    "SupermetricsAPIError",
    "SupermetricsAuthError",
    "SupermetricsForbiddenError",
    "SupermetricsNotFoundError",
    "SupermetricsValidationError",
    "SupermetricsRateLimitError",
    "SupermetricsServerError",
    # Backwards-compatible exception aliases
    "AuthenticationError",
    "ValidationError",
    "APIError",
]
