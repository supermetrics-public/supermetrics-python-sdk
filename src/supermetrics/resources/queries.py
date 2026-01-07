"""Queries resource adapter for Supermetrics API."""

import logging
from typing import Any, cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.get_data import get_data
from supermetrics._generated.supermetrics_api_client.models.data_query import DataQuery
from supermetrics._generated.supermetrics_api_client.models.data_response import DataResponse
from supermetrics._generated.supermetrics_api_client.models.get_data_response_400 import GetDataResponse400
from supermetrics._generated.supermetrics_api_client.models.get_data_response_401 import GetDataResponse401
from supermetrics._generated.supermetrics_api_client.models.get_data_response_403 import GetDataResponse403
from supermetrics._generated.supermetrics_api_client.models.get_data_response_422 import GetDataResponse422
from supermetrics._generated.supermetrics_api_client.models.get_data_response_429 import GetDataResponse429
from supermetrics._generated.supermetrics_api_client.models.get_data_response_500 import GetDataResponse500
from supermetrics._generated.supermetrics_api_client.types import UNSET, Unset
from supermetrics.exceptions import APIError, AuthenticationError, NetworkError, ValidationError

logger = logging.getLogger(__name__)


class QueriesResource:
    """Synchronous resource adapter for Query operations.

    Provides a clean, Pythonic interface for executing data queries
    to retrieve marketing data from various data sources.

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures with intuitive parameter names
    - Support for async query polling when queries take longer to complete
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> # Execute a query for Google Analytics data
        >>> result = client.queries.execute(
        ...     ds_id="GAWA",
        ...     ds_accounts=["account_123"],
        ...     fields=["sessions", "users", "pageviews"],
        ...     start_date="2025-01-01",
        ...     end_date="2025-01-31"
        ... )
        >>> # Check if query is pending (for async queries)
        >>> if result.meta.status_code == "pending":
        ...     result = client.queries.get_results(query_id=result.meta.request_id)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the QueriesResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def execute(
        self,
        ds_id: str,
        ds_accounts: list[str],
        fields: list[str],
        start_date: str,
        end_date: str,
        **kwargs: Any,
    ) -> DataResponse | None:
        """Execute a data query to retrieve marketing data.

        Executes a query against the specified data source to retrieve marketing
        data for the given accounts, fields, and date range. The query may complete
        immediately or return a pending status for async processing.

        For queries that complete immediately, the response will contain the data.
        For async queries (status_code="pending"), use get_results() to poll for
        completion.

        Args:
            ds_id: Data source ID (e.g., "GAWA", "google_ads", "facebook_ads").
                See API documentation for full list of supported data sources.
            ds_accounts: List of account IDs to query. These are the account_id
                values obtained from the accounts.list() method.
            fields: List of field IDs to retrieve. Field IDs are data source specific
                (e.g., ["sessions", "users"] for Google Analytics).
            start_date: Start date for the query in ISO 8601 format (YYYY-MM-DD)
                or relative format (e.g., "yesterday", "7daysAgo").
            end_date: End date for the query in ISO 8601 format (YYYY-MM-DD)
                or relative format (e.g., "today", "yesterday").
            **kwargs: Additional query parameters passed directly to the API.
                Common parameters:
                - schedule_id: Custom identifier for this query
                - ds_segments: List of segment IDs to apply
                - filter_: Filter expression to apply to results
                - max_rows: Maximum number of rows to return
                - cache_minutes: Maximum age of cached data in minutes
                - sync_timeout: Seconds to wait for query completion

        Returns:
            DataResponse | None: Query response containing metadata and data rows.
                Returns None if the API returns no response.
                - response.meta: Metadata including request_id, status_code, fields
                - response.data: List of data rows (each row is a list of strings)

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> # Execute a simple query
            >>> result = client.queries.execute(
            ...     ds_id="GAWA",
            ...     ds_accounts=["12345"],
            ...     fields=["sessions", "users"],
            ...     start_date="2025-01-01",
            ...     end_date="2025-01-31"
            ... )
            >>> if result and result.meta and result.meta.status_code != "pending":
            ...     print(f"Retrieved {len(result.data)} rows")
            >>>
            >>> # Execute with additional parameters
            >>> result = client.queries.execute(
            ...     ds_id="GAWA",
            ...     ds_accounts=["12345", "67890"],
            ...     fields=["sessions", "bounceRate", "avgSessionDuration"],
            ...     start_date="yesterday",
            ...     end_date="yesterday",
            ...     max_rows=1000,
            ...     cache_minutes=30
            ... )
            >>>
            >>> # Handle async query polling
            >>> result = client.queries.execute(
            ...     ds_id="GAWA",
            ...     ds_accounts=["12345"],
            ...     fields=["sessions"],
            ...     start_date="2025-01-01",
            ...     end_date="2025-01-31"
            ... )
            >>> if result and result.meta and result.meta.status_code == "pending":
            ...     import time
            ...     time.sleep(5)  # Wait before polling
            ...     result = client.queries.get_results(query_id=result.meta.request_id)
        """
        logger.debug(
            f"Executing query: ds_id={ds_id}, ds_accounts={ds_accounts}, "
            f"fields={fields}, start_date={start_date}, end_date={end_date}, kwargs={kwargs}"
        )

        try:
            # Build request parameters
            request_params = DataQuery(
                ds_id=ds_id,
                ds_accounts=ds_accounts,
                fields=fields,
                start_date=start_date,
                end_date=end_date,
                **kwargs,
            )

            # Call generated API - cast client to AuthenticatedClient (compatible at runtime)
            response = get_data.sync(client=cast(AuthenticatedClient, self._client), json=request_params)

            # Handle response
            if response is None or isinstance(response, Unset):
                logger.info("Query executed but returned no response (empty)")
                return None

            # Check for error responses and raise appropriate exceptions
            if isinstance(response, GetDataResponse400):
                raise ValidationError(
                    f"Invalid request parameters: {response}",
                    status_code=400,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse401):
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse403):
                raise APIError(
                    "Forbidden - insufficient permissions",
                    status_code=403,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse422):
                raise ValidationError(
                    f"Unprocessable entity - validation failed: {response}",
                    status_code=422,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse429):
                raise APIError(
                    "Rate limit exceeded - too many requests",
                    status_code=429,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse500):
                raise APIError(
                    "Supermetrics API internal server error",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, DataResponse):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is DataResponse
            if hasattr(response, "meta") and response.meta and hasattr(response.meta, "status_code"):
                status = response.meta.status_code if response.meta.status_code is not UNSET else "unknown"
                logger.info(
                    f"Query executed: status={status}, request_id={getattr(response.meta, 'request_id', 'N/A')}"
                )
            else:
                logger.info("Query executed successfully")

            return response

        except httpx.HTTPStatusError as e:
            # Map HTTP status codes to SDK exceptions
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 400:
                raise ValidationError(
                    f"Invalid request parameters: {e.response.text}",
                    status_code=400,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 404:
                raise APIError(
                    f"Resource not found: {e.response.text}",
                    status_code=404,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code >= 500:
                raise APIError(
                    f"Supermetrics API error: {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            else:
                raise APIError(
                    f"API error ({e.response.status_code}): {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(
                f"Network error: {str(e)}",
                endpoint=str(e.request.url) if e.request else None,
            ) from e

    def get_results(self, query_id: str) -> DataResponse | None:
        """Retrieve results for a previously executed query.

        Use this method to poll for results when a query was executed with
        status_code="pending". The query_id should be the request_id from
        the original query response metadata.

        This enables async query polling pattern:
        1. Execute query with execute()
        2. Check if status_code == "pending"
        3. Poll with get_results() until status_code != "pending"

        Args:
            query_id: The request ID from the query execution response.
                This is found in response.meta.request_id.

        Returns:
            DataResponse | None: Query results if available.
                Returns None if the API returns no response.
                - Check response.meta.status_code to see if still pending
                - response.data contains the actual data rows when complete

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).

        Example:
            >>> # Execute query and check status
            >>> result = client.queries.execute(
            ...     ds_id="GAWA",
            ...     ds_accounts=["12345"],
            ...     fields=["sessions"],
            ...     start_date="2025-01-01",
            ...     end_date="2025-01-31"
            ... )
            >>> if result and result.meta and result.meta.status_code == "pending":
            ...     query_id = result.meta.request_id
            ...     # Poll for results
            ...     import time
            ...     max_attempts = 10
            ...     for attempt in range(max_attempts):
            ...         time.sleep(5)
            ...         result = client.queries.get_results(query_id=query_id)
            ...         if result and result.meta and result.meta.status_code != "pending":
            ...             print(f"Query completed with {len(result.data)} rows")
            ...             break
        """
        logger.debug(f"Retrieving query results: query_id={query_id}")

        try:
            # Build request parameters with schedule_id set to the query_id
            # This tells the API to return results for this specific query
            request_params = DataQuery(
                ds_id="",  # Required field but not used for result retrieval
                schedule_id=query_id,
            )

            # Call generated API - cast client to AuthenticatedClient (compatible at runtime)
            response = get_data.sync(client=cast(AuthenticatedClient, self._client), json=request_params)

            # Handle response
            if response is None or isinstance(response, Unset):
                logger.info(f"Query results retrieved but returned no response: query_id={query_id}")
                return None

            # Check for error responses and raise appropriate exceptions
            if isinstance(response, GetDataResponse400):
                raise ValidationError(
                    f"Invalid request parameters: {response}",
                    status_code=400,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse401):
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse403):
                raise APIError(
                    "Forbidden - insufficient permissions",
                    status_code=403,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse422):
                raise ValidationError(
                    f"Unprocessable entity - validation failed: {response}",
                    status_code=422,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse429):
                raise APIError(
                    "Rate limit exceeded - too many requests",
                    status_code=429,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse500):
                raise APIError(
                    "Supermetrics API internal server error",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, DataResponse):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is DataResponse
            if hasattr(response, "meta") and response.meta and hasattr(response.meta, "status_code"):
                status = response.meta.status_code if response.meta.status_code is not UNSET else "unknown"
                logger.info(f"Query results retrieved: query_id={query_id}, status={status}")
            else:
                logger.info(f"Query results retrieved: query_id={query_id}")

            return response

        except httpx.HTTPStatusError as e:
            # Map HTTP status codes to SDK exceptions
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 400:
                raise ValidationError(
                    f"Invalid request parameters: {e.response.text}",
                    status_code=400,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 404:
                raise APIError(
                    f"Resource not found: {e.response.text}",
                    status_code=404,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code >= 500:
                raise APIError(
                    f"Supermetrics API error: {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            else:
                raise APIError(
                    f"API error ({e.response.status_code}): {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(
                f"Network error: {str(e)}",
                endpoint=str(e.request.url) if e.request else None,
            ) from e


class QueriesAsyncResource:
    """Asynchronous resource adapter for Query operations.

    Async version of QueriesResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> result = await client.queries.execute(
        ...     ds_id="GAWA",
        ...     ds_accounts=["account_123"],
        ...     fields=["sessions", "users"],
        ...     start_date="2025-01-01",
        ...     end_date="2025-01-31"
        ... )
        >>> if result and result.meta and result.meta.status_code == "pending":
        ...     result = await client.queries.get_results(query_id=result.meta.request_id)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the QueriesAsyncResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    async def execute(
        self,
        ds_id: str,
        ds_accounts: list[str],
        fields: list[str],
        start_date: str,
        end_date: str,
        **kwargs: Any,
    ) -> DataResponse | None:
        """Execute a data query to retrieve marketing data.

        Async version of execute(). See QueriesResource.execute() for full documentation.

        Args:
            ds_id: Data source ID (e.g., "GAWA", "google_ads").
            ds_accounts: List of account IDs to query.
            fields: List of field IDs to retrieve.
            start_date: Start date in ISO 8601 or relative format.
            end_date: End date in ISO 8601 or relative format.
            **kwargs: Additional query parameters.

        Returns:
            DataResponse | None: Query response with metadata and data.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(
            f"Executing query (async): ds_id={ds_id}, ds_accounts={ds_accounts}, "
            f"fields={fields}, start_date={start_date}, end_date={end_date}, kwargs={kwargs}"
        )

        try:
            # Build request parameters
            request_params = DataQuery(
                ds_id=ds_id,
                ds_accounts=ds_accounts,
                fields=fields,
                start_date=start_date,
                end_date=end_date,
                **kwargs,
            )

            # Call generated API - cast client to AuthenticatedClient (compatible at runtime)
            response = await get_data.asyncio(client=cast(AuthenticatedClient, self._client), json=request_params)

            # Handle response
            if response is None or isinstance(response, Unset):
                logger.info("Query executed (async) but returned no response (empty)")
                return None

            # Check for error responses and raise appropriate exceptions
            if isinstance(response, GetDataResponse400):
                raise ValidationError(
                    f"Invalid request parameters: {response}",
                    status_code=400,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse401):
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse403):
                raise APIError(
                    "Forbidden - insufficient permissions",
                    status_code=403,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse422):
                raise ValidationError(
                    f"Unprocessable entity - validation failed: {response}",
                    status_code=422,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse429):
                raise APIError(
                    "Rate limit exceeded - too many requests",
                    status_code=429,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse500):
                raise APIError(
                    "Supermetrics API internal server error",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, DataResponse):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is DataResponse
            if hasattr(response, "meta") and response.meta and hasattr(response.meta, "status_code"):
                status = response.meta.status_code if response.meta.status_code is not UNSET else "unknown"
                request_id = getattr(response.meta, "request_id", "N/A")
                logger.info(f"Query executed (async): status={status}, request_id={request_id}")
            else:
                logger.info("Query executed (async) successfully")

            return response

        except httpx.HTTPStatusError as e:
            # Map HTTP status codes to SDK exceptions
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 400:
                raise ValidationError(
                    f"Invalid request parameters: {e.response.text}",
                    status_code=400,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 404:
                raise APIError(
                    f"Resource not found: {e.response.text}",
                    status_code=404,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code >= 500:
                raise APIError(
                    f"Supermetrics API error: {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            else:
                raise APIError(
                    f"API error ({e.response.status_code}): {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(
                f"Network error: {str(e)}",
                endpoint=str(e.request.url) if e.request else None,
            ) from e

    async def get_results(self, query_id: str) -> DataResponse | None:
        """Retrieve results for a previously executed query.

        Async version of get_results(). See QueriesResource.get_results() for full documentation.

        Args:
            query_id: The request ID from the query execution response.

        Returns:
            DataResponse | None: Query results if available.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            ValidationError: If request parameters are invalid (HTTP 400).
            APIError: If the API returns a server error (HTTP 404, 5xx).
            NetworkError: If a network-level error occurs (timeout, connection refused).
        """
        logger.debug(f"Retrieving query results (async): query_id={query_id}")

        try:
            # Build request parameters with schedule_id set to the query_id
            request_params = DataQuery(
                ds_id="",  # Required field but not used for result retrieval
                schedule_id=query_id,
            )

            # Call generated API - cast client to AuthenticatedClient (compatible at runtime)
            response = await get_data.asyncio(client=cast(AuthenticatedClient, self._client), json=request_params)

            # Handle response
            if response is None or isinstance(response, Unset):
                logger.info(f"Query results retrieved (async) but returned no response: query_id={query_id}")
                return None

            # Check for error responses and raise appropriate exceptions
            if isinstance(response, GetDataResponse400):
                raise ValidationError(
                    f"Invalid request parameters: {response}",
                    status_code=400,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse401):
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse403):
                raise APIError(
                    "Forbidden - insufficient permissions",
                    status_code=403,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse422):
                raise ValidationError(
                    f"Unprocessable entity - validation failed: {response}",
                    status_code=422,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse429):
                raise APIError(
                    "Rate limit exceeded - too many requests",
                    status_code=429,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )
            elif isinstance(response, GetDataResponse500):
                raise APIError(
                    "Supermetrics API internal server error",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # Defensive validation: ensure response is the expected success type
            if not isinstance(response, DataResponse):
                raise APIError(
                    f"Unexpected response type: {type(response).__name__}",
                    status_code=500,
                    endpoint="/query/data/json",
                    response_body=str(response),
                )

            # After isinstance check, mypy knows response is DataResponse
            if hasattr(response, "meta") and response.meta and hasattr(response.meta, "status_code"):
                status = response.meta.status_code if response.meta.status_code is not UNSET else "unknown"
                logger.info(f"Query results retrieved (async): query_id={query_id}, status={status}")
            else:
                logger.info(f"Query results retrieved (async): query_id={query_id}")

            return response

        except httpx.HTTPStatusError as e:
            # Map HTTP status codes to SDK exceptions
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Invalid or expired API key",
                    status_code=401,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 400:
                raise ValidationError(
                    f"Invalid request parameters: {e.response.text}",
                    status_code=400,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code == 404:
                raise APIError(
                    f"Resource not found: {e.response.text}",
                    status_code=404,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            elif e.response.status_code >= 500:
                raise APIError(
                    f"Supermetrics API error: {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
            else:
                raise APIError(
                    f"API error ({e.response.status_code}): {e.response.text}",
                    status_code=e.response.status_code,
                    endpoint=str(e.request.url),
                    response_body=e.response.text,
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(
                f"Network error: {str(e)}",
                endpoint=str(e.request.url) if e.request else None,
            ) from e
