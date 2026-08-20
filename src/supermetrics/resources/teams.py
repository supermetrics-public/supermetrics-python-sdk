"""Teams resource adapter for the Supermetrics Management API.

This domain is read-only team and user-identity discovery. Both endpoints live on the
**core** API host with ``/v1`` in the path — the same shape as Custom Fields, Account Tags
and Blends, and the opposite of the Data Warehouse families — so nothing here is re-hosted
to ``dts-api``.

Two things about the surface are worth stating plainly, because the original feature
request assumed otherwise:

- There is **no keyless "list my teams" / userinfo endpoint** upstream. Every team call is
  scoped by ``team_id``; :meth:`TeamsResource.get` looks a team up by that id, and
  :meth:`TeamsResource.list_users` lists that team's members. There is deliberately no
  ``client.user`` resource, because nothing backs one.
- Both responses are wrapped in ``{"meta": ..., "data": ...}`` and ``data`` is **required**
  on each schema. The adapter hands back the ``data`` payload — a
  :class:`~supermetrics._generated.supermetrics_api_client.models.team_data.TeamData` for
  ``get`` and a bare ``list`` of
  :class:`~supermetrics._generated.supermetrics_api_client.models.team_user.TeamUser` for
  ``list_users`` — never the envelope. An empty team is an empty list, not an error.
"""

from __future__ import annotations

from typing import cast

import httpx

from supermetrics._generated.supermetrics_api_client import AuthenticatedClient
from supermetrics._generated.supermetrics_api_client import Client as GeneratedClient
from supermetrics._generated.supermetrics_api_client.api.team_users import list_team_users
from supermetrics._generated.supermetrics_api_client.api.teams import get_team
from supermetrics._generated.supermetrics_api_client.models.team_data import TeamData
from supermetrics._generated.supermetrics_api_client.models.team_response import TeamResponse
from supermetrics._generated.supermetrics_api_client.models.team_user import TeamUser
from supermetrics._generated.supermetrics_api_client.models.team_user_list_response import TeamUserListResponse
from supermetrics._transport import request_options
from supermetrics.resources._error_handlers import _raise_for_status, api_error_handler


class TeamsAsyncResource:
    """Asynchronous resource adapter for Teams & user-identity discovery.

    Async version of TeamsResource for use with SupermetricsAsyncClient. Provides the same
    interface but with async/await support.

    Example:
        >>> client = SupermetricsAsyncClient(api_key="your-key")
        >>> team = await client.teams.get(team_id=936506)
        >>> members = await client.teams.list_users(team_id=936506)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the TeamsAsyncResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    async def get(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamData:
        """Fetch a team's identity by its id.

        Async version of TeamsResource.get(). See the sync version for full documentation.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the client
                credential.
            headers: Extra HTTP headers for this request only (for example ``X-Span-Id``,
                ``traceparent``, ``Idempotency-Key``). Takes precedence over client-level
                headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the team is unknown (HTTP 404) or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/v1/teams/{team_id}"
        with (
            api_error_handler(endpoint, context_400="Invalid team request", context_404="Team not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await get_team.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(TeamResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found",
                bad_request_msg="Invalid team request",
                headers=response.headers,
                raw_body=response.content,
            )

    async def list_users(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> list[TeamUser]:
        """List the users belonging to a team.

        Async version of TeamsResource.list_users(). See the sync version for full documentation.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the client
                credential.
            headers: Extra HTTP headers for this request only (for example ``X-Span-Id``,
                ``traceparent``, ``Idempotency-Key``). Takes precedence over client-level
                headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.
        """
        endpoint = f"/v1/teams/{team_id}/users"
        with (
            api_error_handler(endpoint, context_400="Invalid team users request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = await list_team_users.asyncio_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(TeamUserListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid team users request",
                headers=response.headers,
                raw_body=response.content,
            )


class TeamsResource:
    """Synchronous resource adapter for Teams & user-identity discovery.

    A team is the top-level tenant a Supermetrics account belongs to; every other
    team-scoped resource in this SDK addresses it by ``team_id``. This resource is how you
    discover a team's own identity and its membership.

    There is no "list my teams" or "current user" call: the Management API exposes no
    keyless discovery endpoint, so both methods here take a ``team_id`` you already hold.

    This adapter wraps the auto-generated API client to provide:
    - A stable public API that won't break on OpenAPI regeneration
    - Simplified method signatures
    - Proper error handling
    - Complete type safety

    Example:
        >>> client = SupermetricsClient(api_key="your-key")
        >>> team = client.teams.get(team_id=936506)
        >>> print(team.name, team.display_id)
        >>> for user in client.teams.list_users(team_id=936506):
        ...     print(user.email, user.role)
    """

    def __init__(self, client: GeneratedClient) -> None:
        """Initialize the TeamsResource.

        Args:
            client: The generated API client instance.
        """
        self._client = client

    def get(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> TeamData:
        """Fetch a team's identity by its id.

        Returns the team's own attributes — ``team_id``, ``name``, the ``SM_``-prefixed
        ``display_id``, ``status`` and ``created_at`` — unwrapped from the ``data`` envelope.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the client
                credential.
            headers: Extra HTTP headers for this request only (for example ``X-Span-Id``,
                ``traceparent``, ``Idempotency-Key``). Takes precedence over client-level
                headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            TeamData: The team's identity attributes.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the team is unknown (HTTP 404) or the request is rejected
                (HTTP 400, 403, 429, 5xx).
            NetworkError: If a network error occurs during the request.

        Example:
            >>> team = client.teams.get(team_id=936506)
            >>> team.name, team.display_id
            ('My Team', 'SM_ABC123')
        """
        endpoint = f"/v1/teams/{team_id}"
        with (
            api_error_handler(endpoint, context_400="Invalid team request", context_404="Team not found"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = get_team.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(TeamResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                not_found_msg="Team not found",
                bad_request_msg="Invalid team request",
                headers=response.headers,
                raw_body=response.content,
            )

    def list_users(
        self,
        team_id: int,
        *,
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> list[TeamUser]:
        """List the users belonging to a team.

        Returns every member of the team, each a :class:`TeamUser` carrying ``user_id``,
        ``email``, ``first_name``, ``last_name``, ``role`` and ``created_at``. The list is
        not paginated and takes no filters; an empty team returns ``[]``.

        Args:
            team_id: The unique identifier of the team.
            auth_token: Bearer token to use for this request only, overriding the client
                credential.
            headers: Extra HTTP headers for this request only (for example ``X-Span-Id``,
                ``traceparent``, ``Idempotency-Key``). Takes precedence over client-level
                headers.
            timeout: Timeout override for this request only, in seconds or as an
                ``httpx.Timeout``.

        Returns:
            list[TeamUser]: The team's members. Empty when it has none.

        Raises:
            AuthenticationError: If the API key is invalid or expired (HTTP 401).
            APIError: If the request is rejected or the API errors (HTTP 400, 403, 429, 5xx).
                This operation documents no 404.
            NetworkError: If a network error occurs during the request.

        Example:
            >>> for user in client.teams.list_users(team_id=936506):
            ...     print(f"{user.email} ({user.role})")
        """
        endpoint = f"/v1/teams/{team_id}/users"
        with (
            api_error_handler(endpoint, context_400="Invalid team users request"),
            request_options(auth_token=auth_token, headers=headers, timeout=timeout),
        ):
            response = list_team_users.sync_detailed(
                client=cast(AuthenticatedClient, self._client),
                team_id=team_id,
            )
            if response.status_code == 200:
                return cast(TeamUserListResponse, response.parsed).data
            _raise_for_status(
                int(response.status_code),
                response.parsed,
                endpoint,
                bad_request_msg="Invalid team users request",
                headers=response.headers,
                raw_body=response.content,
            )
