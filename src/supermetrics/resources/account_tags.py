"""Account Tags resource adapter for the Supermetrics Management API."""

from __future__ import annotations

from typing import Any, TypeVar, cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.account_tags import (
    append_accounts_to_group,
    create_account_group,
    delete_account_group,
    fetch_account_group,
    fetch_available_account_groups,
    remove_accounts_from_group,
    update_account_group,
)
from supermetrics._generated.supermetrics_api_client.models.account_tag import AccountTag
from supermetrics._generated.supermetrics_api_client.models.account_tag_list_response import AccountTagListResponse
from supermetrics._generated.supermetrics_api_client.models.account_tag_overview import AccountTagOverview
from supermetrics._generated.supermetrics_api_client.models.account_tag_response import AccountTagResponse
from supermetrics._generated.supermetrics_api_client.models.append_accounts_to_group_body import (
    AppendAccountsToGroupBody,
)
from supermetrics._generated.supermetrics_api_client.models.append_accounts_to_group_body_data_sources_item import (
    AppendAccountsToGroupBodyDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.create_account_group_body import CreateAccountGroupBody
from supermetrics._generated.supermetrics_api_client.models.create_account_group_body_data_sources_item import (
    CreateAccountGroupBodyDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.delete_account_group_response_200 import (
    DeleteAccountGroupResponse200,
)
from supermetrics._generated.supermetrics_api_client.models.remove_accounts_from_group_body import (
    RemoveAccountsFromGroupBody,
)
from supermetrics._generated.supermetrics_api_client.models.remove_accounts_from_group_body_data_sources_item import (
    RemoveAccountsFromGroupBodyDataSourcesItem,
)
from supermetrics._generated.supermetrics_api_client.models.update_account_group_body import UpdateAccountGroupBody
from supermetrics._generated.supermetrics_api_client.types import Unset
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler

# These classes expose a method named ``list``, which binds ``list`` in the class
# namespace and shadows the builtin for every annotation evaluated in the class body
# after that point. Aliasing the collection types out here, at module scope, is what
# keeps ``list[AccountTagOverview]`` in a later method meaning a list of account tags
# rather than a subscript of ``AccountTagsResource.list``. Do not inline these back.
AccountTagOverviewList = list[AccountTagOverview]
DataSourceDictList = list[dict[str, Any]]

#: The three generated request-body item classes for ``data_sources``. Upstream declares
#: the array items as a bare ``type: object``, so the generator emits one of these per
#: request body, each with nothing but an ``additional_properties`` dict declared
#: ``init=False`` — which makes them unconstructable by a caller. The public signature
#: therefore takes plain dicts and ``_data_source_items`` converts them here.
_DataSourceItemT = TypeVar(
    "_DataSourceItemT",
    AppendAccountsToGroupBodyDataSourcesItem,
    CreateAccountGroupBodyDataSourcesItem,
    RemoveAccountsFromGroupBodyDataSourcesItem,
)


def _data_source_items(
    item_type: type[_DataSourceItemT],
    data_sources: DataSourceDictList,
) -> list[_DataSourceItemT]:
    """Convert caller-supplied ``data_sources`` dicts into the generated item type.

    Args:
        item_type: The generated item class for the request body being built.
        data_sources: The data source selections, each a plain dict shaped like
            ``{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}``.

    Returns:
        list: The same selections as instances of ``item_type``.
    """
    return [item_type.from_dict(entry) for entry in data_sources]


def _tag_of(parsed: AccountTagResponse) -> AccountTag:
    """Unwrap the account tag from a single-object response.

    Upstream marks ``data`` optional on ``AccountTagResponse``, so it can legitimately
    be absent. Returning an empty :class:`AccountTag` rather than ``None`` keeps the
    return type of every single-object method non-optional; a real failure arrives as a
    non-2xx status and is raised before this is reached.

    Args:
        parsed: The deserialized response envelope.

    Returns:
        AccountTag: The tag, or an empty one when the server sent no ``data``.
    """
    data = parsed.data
    return AccountTag() if isinstance(data, Unset) else data


def _overviews_of(parsed: AccountTagListResponse) -> AccountTagOverviewList:
    """Unwrap the list of account tags from a list response.

    Args:
        parsed: The deserialized response envelope.

    Returns:
        list[AccountTagOverview]: The team's account tags, empty when there are none.
    """
    data = parsed.data
    if isinstance(data, Unset):
        return []
    items = data.items
    return [] if isinstance(items, Unset) else items


def _deleted_of(parsed: DeleteAccountGroupResponse200) -> bool:
    """Read the deletion result out of a delete response.

    Deletion is idempotent upstream, so the body — not the status code — says whether
    anything was removed. Both ``data`` and ``result`` are optional in the schema; an
    absent value means the server made no claim, so neither does this.

    Args:
        parsed: The deserialized response envelope.

    Returns:
        bool: True when a tag was deleted, False when none existed.
    """
    data = parsed.data
    if isinstance(data, Unset) or isinstance(data.result, Unset):
        return False
    return data.result


class AccountTagsAsyncResource:
    """Asynchronous resource adapter for Account Tag operations.

    Async version of AccountTagsResource for use with SupermetricsAsyncClient.
    Provides the same interface but with async/await support for concurrent operations.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> tags = await client.account_tags.list(team_id=936506)
    """

    def __init__(self, client: GeneratedClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTagOverviewList:
        """List the account tags defined for a team.

        Async version of AccountTagsResource.list(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag list request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await fetch_available_account_groups.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return _overviews_of(cast(AccountTagListResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag list request",
                headers=response.headers,
                raw_body=response.content,
            )

    async def get(
        self,
        team_id: int,
        name: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Fetch a single account tag by its name.

        Async version of AccountTagsResource.get(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}"
        with (
            api_error_handler(endpoint, context_400="Unknown account tag or invalid request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await fetch_account_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Unknown account tag or invalid request",
                headers=response.headers,
                raw_body=response.content,
            )

    async def create(
        self,
        team_id: int,
        display_name: str,
        color: str,
        data_sources: DataSourceDictList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Create an account tag.

        Async version of AccountTagsResource.create(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag already exists (HTTP 409) or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag definition"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CreateAccountGroupBody(
                display_name=display_name,
                color=color,
                data_sources=_data_source_items(CreateAccountGroupBodyDataSourcesItem, data_sources),
            )
            response = await create_account_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag definition",
                headers=response.headers,
                raw_body=response.content,
            )

    async def update(
        self,
        team_id: int,
        name: str,
        display_name: str,
        color: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Rename or recolour an account tag.

        Async version of AccountTagsResource.update(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag update"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = UpdateAccountGroupBody(display_name=display_name, color=color)
            response = await update_account_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag update",
                headers=response.headers,
                raw_body=response.content,
            )

    async def delete(
        self,
        team_id: int,
        name: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> bool:
        """Delete an account tag.

        Async version of AccountTagsResource.delete(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag deletion request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await delete_account_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
            )
            if response.status_code == 200:
                return _deleted_of(cast(DeleteAccountGroupResponse200, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag deletion request",
                headers=response.headers,
                raw_body=response.content,
            )

    async def add_accounts(
        self,
        team_id: int,
        name: str,
        data_sources: DataSourceDictList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Add data source accounts to an account tag.

        Async version of AccountTagsResource.add_accounts(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}/add"
        with (
            api_error_handler(endpoint, context_400="Invalid accounts to add"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = AppendAccountsToGroupBody(
                data_sources=_data_source_items(AppendAccountsToGroupBodyDataSourcesItem, data_sources),
            )
            response = await append_accounts_to_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid accounts to add",
                headers=response.headers,
                raw_body=response.content,
            )

    async def remove_accounts(
        self,
        team_id: int,
        name: str,
        data_sources: DataSourceDictList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Remove data source accounts from an account tag.

        Async version of AccountTagsResource.remove_accounts(). See sync version for full documentation.

        Args:
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}/remove"
        with (
            api_error_handler(endpoint, context_400="Invalid accounts to remove"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = RemoveAccountsFromGroupBody(
                data_sources=_data_source_items(RemoveAccountsFromGroupBodyDataSourcesItem, data_sources),
            )
            response = await remove_accounts_from_group.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid accounts to remove",
                headers=response.headers,
                raw_body=response.content,
            )


class AccountTagsResource:
    """Synchronous resource adapter for Account Tag operations.

    An account tag groups data source accounts from across a team's connections under
    one reusable label, so a query or transfer can name the group instead of listing
    every account by hand.

    Two names identify a tag and they are not interchangeable:

    - ``name`` is the immutable slug the server assigns at creation, for example
      ``"a1b2c3d"``. It is what every subsequent call addresses the tag by, and it is
      never sent in a request body.
    - ``display_name`` is the human-readable label, for example ``"EMEA paid media"``.
      It is what :meth:`create` and :meth:`update` set, and it can change freely.

    Membership is expressed as ``data_sources``, a list of plain dicts. Upstream
    declares the element schema as an open object, so the SDK does not impose a shape
    on it; the documented form is::

        {"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}

    This adapter wraps the auto-generated API client to provide:
    - Stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Note:
        :meth:`update` cannot change membership. It replaces ``display_name`` and
        ``color`` and nothing else; accounts move through :meth:`add_accounts` and
        :meth:`remove_accounts`. :meth:`delete` returns a ``bool`` rather than ``None``
        because upstream made deletion idempotent — no operation in this domain
        answers 404, and deleting a tag that does not exist is a success carrying
        ``False``.

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> tags = client.account_tags.list(team_id=936506)
        >>> for tag in tags:
        ...     print(tag.name, tag.display_name, tag.account_count)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the AccountTagsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def list(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTagOverviewList:
        """List the account tags defined for a team.

        The list is not paginated and takes no filters; the API returns every tag on
        the team, up to its own cap of 500.

        Each entry is an :class:`AccountTagOverview`, which summarises membership as
        ``data_source_count`` and ``account_count`` rather than listing it. Call
        :meth:`get` for the accounts themselves.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[AccountTagOverview]: The team's account tags. Empty when it has none.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> tags = client.account_tags.list(team_id=936506)
            >>> for tag in tags:
            ...     print(f"{tag.name}: {tag.display_name} ({tag.account_count} accounts)")
        """
        endpoint = f"/teams/{team_id}/account_tags"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag list request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = fetch_available_account_groups.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return _overviews_of(cast(AccountTagListResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag list request",
                headers=response.headers,
                raw_body=response.content,
            )

    def get(
        self,
        team_id: int,
        name: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Fetch a single account tag by its name.

        Unlike :meth:`list`, this returns the tag's membership — ``data_sources`` —
        and not the summary counts.

        Args:
            team_id: The unique identifier of the team.
            name: The tag's server-assigned slug, for example ``"a1b2c3d"``. This is
                :attr:`AccountTagOverview.name`, not the display name.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            AccountTag: The tag, including its data source and account membership.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the API errors (HTTP 400, 403, 429, 5xx).
                This domain documents no 404 — an unknown tag arrives as a 400.
            NetworkError: If a network error occurs during the request.

        Example:
            >>> tag = client.account_tags.get(team_id=936506, name="a1b2c3d")
            >>> for selection in tag.data_sources:
            ...     print(selection["data_source_id"], selection["accounts"])
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}"
        with (
            api_error_handler(endpoint, context_400="Unknown account tag or invalid request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = fetch_account_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Unknown account tag or invalid request",
                headers=response.headers,
                raw_body=response.content,
            )

    def create(
        self,
        team_id: int,
        display_name: str,
        color: str,
        data_sources: DataSourceDictList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Create an account tag.

        The tag's ``name`` is assigned by the server and is not sent in the request.
        Read it off the returned :class:`AccountTag` — every later call addresses the
        tag by that slug.

        Args:
            team_id: The unique identifier of the team.
            display_name: The human-readable label, for example ``"EMEA paid media"``.
                Up to 255 characters.
            color: Display colour for the tag, for example ``"#112233"``. Up to 50
                characters.
            data_sources: The accounts to put in the tag, up to 100 entries. Each is a
                dict shaped like
                ``{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}``.
                Upstream declares no schema for the element, so no shape is enforced
                here.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            AccountTag: The created tag, carrying its server-assigned ``name``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If a tag with that display name already exists the API answers
                HTTP 409 and this raises ``SupermetricsAPIError`` with
                ``status_code == 409`` and ``error_code == "CONFLICT_ERROR"``. Also
                raised for HTTP 400, 403, 429 and 5xx.
            NetworkError: If a network error occurs during the request.

        Example:
            >>> tag = client.account_tags.create(
            ...     team_id=936506,
            ...     display_name="EMEA paid media",
            ...     color="#112233",
            ...     data_sources=[
            ...         {"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}
            ...     ],
            ... )
            >>> tag.name
            'a1b2c3d'
        """
        endpoint = f"/teams/{team_id}/account_tags"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag definition"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = CreateAccountGroupBody(
                display_name=display_name,
                color=color,
                data_sources=_data_source_items(CreateAccountGroupBodyDataSourcesItem, data_sources),
            )
            response = create_account_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag definition",
                headers=response.headers,
                raw_body=response.content,
            )

    def update(
        self,
        team_id: int,
        name: str,
        display_name: str,
        color: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Rename or recolour an account tag.

        This is the whole of what PUT can change. It does **not** touch membership:
        ``data_sources`` is not part of the request body, and accounts are added and
        removed through :meth:`add_accounts` and :meth:`remove_accounts`. Both fields
        are required, so a call that means to change only the colour must resend the
        current display name.

        Args:
            team_id: The unique identifier of the team.
            name: The tag's server-assigned slug, for example ``"a1b2c3d"``.
            display_name: The new human-readable label. Up to 255 characters.
            color: The new display colour, for example ``"#112233"``. Up to 50
                characters.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            AccountTag: The updated tag.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> tag = client.account_tags.update(
            ...     team_id=936506, name="a1b2c3d", display_name="EMEA paid", color="#445566"
            ... )
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag update"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = UpdateAccountGroupBody(display_name=display_name, color=color)
            response = update_account_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag update",
                headers=response.headers,
                raw_body=response.content,
            )

    def delete(
        self,
        team_id: int,
        name: str,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> bool:
        """Delete an account tag.

        Deletion is idempotent upstream: deleting a tag that does not exist is a
        success, answering HTTP 200 with ``result=false`` rather than 404. That is why
        this returns a ``bool`` where every other ``delete`` in the SDK returns
        ``None`` — the boolean is the only place the distinction is recorded.

        A ``False`` return means "nothing was there". A genuine failure — a bad
        request, a permission problem, a server error — raises, as everywhere else.

        Args:
            team_id: The unique identifier of the team.
            name: The tag's server-assigned slug, for example ``"a1b2c3d"``.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            bool: True when a tag was deleted, False when no tag of that name existed.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> client.account_tags.delete(team_id=936506, name="a1b2c3d")
            True
            >>> client.account_tags.delete(team_id=936506, name="a1b2c3d")
            False
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}"
        with (
            api_error_handler(endpoint, context_400="Invalid account tag deletion request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = delete_account_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
            )
            if response.status_code == 200:
                return _deleted_of(cast(DeleteAccountGroupResponse200, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid account tag deletion request",
                headers=response.headers,
                raw_body=response.content,
            )

    def add_accounts(
        self,
        team_id: int,
        name: str,
        data_sources: DataSourceDictList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Add data source accounts to an account tag.

        This is additive: accounts already in the tag stay in it. Use
        :meth:`remove_accounts` to take them out; :meth:`update` cannot.

        Args:
            team_id: The unique identifier of the team.
            name: The tag's server-assigned slug, for example ``"a1b2c3d"``.
            data_sources: The accounts to add, up to 100 entries. Each is a dict shaped
                like
                ``{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}``.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            AccountTag: The tag with its updated membership.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> tag = client.account_tags.add_accounts(
            ...     team_id=936506,
            ...     name="a1b2c3d",
            ...     data_sources=[
            ...         {"data_source_id": "FB", "accounts": [{"account_id": "act_99"}]}
            ...     ],
            ... )
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}/add"
        with (
            api_error_handler(endpoint, context_400="Invalid accounts to add"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = AppendAccountsToGroupBody(
                data_sources=_data_source_items(AppendAccountsToGroupBodyDataSourcesItem, data_sources),
            )
            response = append_accounts_to_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid accounts to add",
                headers=response.headers,
                raw_body=response.content,
            )

    def remove_accounts(
        self,
        team_id: int,
        name: str,
        data_sources: DataSourceDictList,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> AccountTag:
        """Remove data source accounts from an account tag.

        The tag itself survives even when the last account is removed; use
        :meth:`delete` to get rid of it.

        Args:
            team_id: The unique identifier of the team.
            name: The tag's server-assigned slug, for example ``"a1b2c3d"``.
            data_sources: The accounts to remove, up to 100 entries. Each is a dict
                shaped like
                ``{"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}``.
            auth_token: Bearer token to use for this request only, overriding the
                client credential.
            headers: Extra HTTP headers for this request only (for example
                ``X-Span-Id``, ``traceparent``, ``Idempotency-Key``).
                Takes precedence over client-level headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            AccountTag: The tag with its updated membership.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the tag is unknown or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> tag = client.account_tags.remove_accounts(
            ...     team_id=936506,
            ...     name="a1b2c3d",
            ...     data_sources=[
            ...         {"data_source_id": "AW", "accounts": [{"account_id": "123-456-7890"}]}
            ...     ],
            ... )
        """
        endpoint = f"/teams/{team_id}/account_tags/{name}/remove"
        with (
            api_error_handler(endpoint, context_400="Invalid accounts to remove"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            request = RemoveAccountsFromGroupBody(
                data_sources=_data_source_items(RemoveAccountsFromGroupBodyDataSourcesItem, data_sources),
            )
            response = remove_accounts_from_group.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
                name=name,
                body=request,
            )
            if response.status_code == 200:
                return _tag_of(cast(AccountTagResponse, response.parsed))
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid accounts to remove",
                headers=response.headers,
                raw_body=response.content,
            )
