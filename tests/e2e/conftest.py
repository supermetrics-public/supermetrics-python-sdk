"""Fixtures for end-to-end tests.

These tests exercise the *whole* SDK stack over a real TCP socket: the public
client classes, the resource adapters, the generated low-level client, the
``httpx`` transport, the event hooks that implement per-request authentication
and header/timeout overrides, and the error translation layer.

Nothing is mocked or patched. The only substitution is the server on the other
end of the socket: a stdlib :class:`http.server.ThreadingHTTPServer` that serves
scripted responses and records every request it receives, so assertions can be
made about exactly what went out on the wire.
"""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

# A minimal but complete DataSourceLogin payload accepted by the generated models.
LOGIN_PAYLOAD: dict[str, Any] = {
    "type": "ds_login",
    "login_id": "login_abc123",
    "login_type": "oauth2",
    "username": "user@example.com",
    "display_name": "Example User",
    "ds_info": {"ds_id": "GAWA", "name": "Google Analytics 4"},
    "default_scopes": ["read_data"],
    "additional_scopes": [],
    "auth_time": "2026-01-01T00:00:00Z",
    "auth_user_info": {"user_id": "user_1", "email": "user@example.com"},
    "expiry_time": "2026-12-01T00:00:00Z",
    "revoked_time": None,
    "is_refreshable": True,
}

#: Response body for ``GET /ds/logins``.
LOGINS_LIST_BODY: dict[str, Any] = {"data": [LOGIN_PAYLOAD]}

#: Response body for ``GET /ds/login/{login_id}``.
LOGIN_GET_BODY: dict[str, Any] = {"data": LOGIN_PAYLOAD}

# --- Data Warehouse transfers -------------------------------------------------
#
# The Management API wraps some transfer responses in {"meta": ..., "data": ...} and
# returns others bare. That split is real, not an oversight in these fixtures: see
# docs.local/plans/phase2-transfers-and-runs.md §4.

#: Every wrapped response carries this envelope metadata.
META: dict[str, Any] = {"request_id": "req_0123456789abcdef"}

#: One item of GET /teams/{team_id}/transfers. Note `dwh_transfer_id`, a `schedule`
#: string and an `accounts` string array — the list item is shaped differently from
#: the detail object below, which is how the API actually behaves.
TRANSFER_LIST_ITEM: dict[str, Any] = {
    "dwh_transfer_id": 36091,
    "display_name": "Google Ads to BigQuery",
    "external_transfer_id": "ext-36091",
    "status": "active",
    "state": "active",
    "schedule": "daily",
    "run_date": "2026-01-01",
    "accounts": ["8733197711"],
}
TRANSFERS_LIST_BODY: dict[str, Any] = {"meta": META, "data": [TRANSFER_LIST_ITEM]}

#: GET /teams/{team_id}/transfers/{transfer_id} — bare, no envelope.
TRANSFER_DETAIL_BODY: dict[str, Any] = {
    "transfer_id": 36091,
    "display_name": "Google Ads to BigQuery",
    "schema_id": 99999,
    "destination_id": 8,
    "accounts": [{"data_source_username": "ads@example.com", "login_id": 1, "account_id": "8733197711"}],
    "segments": [],
    "schedule": [{"run_interval": "daily", "run_hour": 4, "refresh_window": 30}],
    "notification_recipients": [{"email": "ops@example.com"}],
    "external_url": None,
}

#: POST /teams/{team_id}/transfers — wrapped, 201.
TRANSFER_CREATED_BODY: dict[str, Any] = {
    "meta": META,
    "data": {"transfer_id": 36091, "transfer_name": "Google Ads to BigQuery"},
}

#: PUT /teams/{team_id}/transfers/{transfer_id} — bare, despite create being wrapped.
TRANSFER_UPDATED_BODY: dict[str, Any] = {"transfer_id": 36091, "transfer_name": "Google Ads to BigQuery"}

#: PUT .../state — bare. `state` is a free string upstream; the example is uppercase
#: while the request enum is lowercase (`pause` / `unpause`).
TRANSFER_STATE_BODY: dict[str, Any] = {"result": True, "state": "PAUSED"}

#: POST .../validations — returned with HTTP 200 even when the config is invalid.
VALIDATION_OK_BODY: dict[str, Any] = {"is_valid": True, "errors": []}
VALIDATION_FAILED_BODY: dict[str, Any] = {
    "is_valid": False,
    "errors": [{"field_id": "display_name", "error_code": "isEmpty"}],
}

#: GET .../available-sources — bare.
AVAILABLE_SOURCES_BODY: dict[str, Any] = {
    "data_sources": [
        {
            "data_source_id": "AW",
            "service_name": "Google Ads",
            "service_provider": "Google",
            "logo_url": None,
            "has_custom_fields": True,
            "is_custom_connector": False,
            "is_public_beta": False,
            "is_released": True,
            "is_internal": None,
            "applicable_destinations": ["SQL_BQ"],
        }
    ],
    "destinations": [
        {
            "destination_id": 8,
            "destination_name": "Analytics warehouse",
            "destination_type": "SQL_BQ",
            "destination_label": "BigQuery",
            "is_internal": False,
            "details": [],
        }
    ],
    "destination_types": [{"title": "BigQuery", "type": "SQL_BQ", "is_internal": False}],
}

#: GET .../available-options — bare, and almost entirely untyped upstream.
TRANSFER_OPTIONS_BODY: dict[str, Any] = {
    "data_source": {"data_source_id": "AW", "service_name": "Google Ads", "settings": []},
    "schedule_options": [],
    "schemas": [],
    "logins": [],
    "accounts": [],
    "segments": [],
}

#: GET .../{transfer_id}/runs — wrapped. `type` is one of Recurring / Backfill.
TRANSFER_RUN_ITEM: dict[str, Any] = {
    "id": 12345,
    "status": "COMPLETED",
    "type": "Recurring",
    "message": "",
    "created_time": "2026-01-01T04:00:00Z",
    "ended_time": "2026-01-01T04:03:20Z",
    "total_duration": 200.0,
    "total_rows": 4821,
    "data_date": "2026-01-01",
}
TRANSFER_RUNS_LIST_BODY: dict[str, Any] = {"meta": META, "data": [TRANSFER_RUN_ITEM]}

#: GET /teams/{team_id}/transfer_runs/{transfer_run_id} — wrapped. The detail object
#: adds query_details / external_id / timing fields and drops `type`.
TRANSFER_RUN_DETAIL_BODY: dict[str, Any] = {
    "meta": META,
    "data": {
        "id": 12345,
        "status": "COMPLETED",
        "external_id": "run-ext-12345",
        "message": "",
        "query_details": [{"status": "COMPLETED", "rows": 4821, "duration": 12.5, "error_description": None}],
        "started_time": "2026-01-01T04:00:10Z",
        "queued_time": "2026-01-01T04:00:00Z",
        "ended_time": "2026-01-01T04:03:20Z",
        "created_time": "2026-01-01T04:00:00Z",
        "failed_query_amount": 0,
        "total_duration": 200.0,
        "total_rows": 4821,
        "query_amount": 1,
        "data_date": "2026-01-01",
    },
}

#: POST /teams/{team_id}/data-source-connections — wrapped, 201. The connection_id
#: pattern upstream is uppercase hex only.
DATA_SOURCE_CONNECTION_BODY: dict[str, Any] = {
    "meta": META,
    "data": {
        "connection_id": "019461A0-0000-7000-8000-000000000001",
        "login_url": None,
        "connect_url": None,
    },
}

# --- Custom fields ------------------------------------------------------------
#
# Custom fields live on the CORE api host under a "/v1" path prefix, unlike transfers.
# Route strings for these tests therefore include the "/v1" — see
# docs.local/scratchpads/phase4-contract.md.

#: The three custom-field routes, for team 42 and custom field 42.
CUSTOM_FIELDS_COLLECTION = "/v1/teams/42/custom-fields"
CUSTOM_FIELDS_ITEM = "/v1/teams/42/custom-fields/42"
CUSTOM_FIELDS_METADATA = "/v1/teams/42/custom-fields/metadata"

#: A "function" definition step: apply a named function to its arguments.
FUNCTION_STEP: dict[str, Any] = {
    "type": "function",
    "name": "upper_case",
    "arguments": [{"name": "value", "value": {"type": "data_source_field", "value": "platform"}}],
    "description": None,
}

#: A "lookup" definition step. `map` is an open-ended object upstream, so the generated
#: model holds it in `additional_properties` rather than as a declared field.
LOOKUP_STEP: dict[str, Any] = {
    "type": "lookup",
    "rule": "equals",
    "map": {"1": "2", "a": "b"},
    "source": {"type": "output_from_previous"},
    "default": {"type": "static", "value": "other"},
    "description": None,
}

#: A "condition" definition step. Note `default` is itself a oneOf — a DefinitionValue
#: here, but it is equally allowed to be a whole nested FunctionStep.
CONDITION_STEP: dict[str, Any] = {
    "type": "condition",
    "default": {"type": "static", "value": "none"},
    "cases": [
        {
            "return": {"type": "output_from_previous"},
            "condition": {
                "type": "rule",
                "rule": "equals",
                "source": {"type": "output_from_previous"},
                "target": {"type": "static", "value": "1"},
            },
        }
    ],
    "description": None,
}

#: All three step kinds in one definition. The generated layer discriminates the
#: `oneOf` with a try/except cascade rather than by reading the `type` discriminator,
#: so every kind has to be round-tripped rather than assumed to work.
ALL_STEP_KINDS: list[dict[str, Any]] = [FUNCTION_STEP, LOOKUP_STEP, CONDITION_STEP]

#: One custom field as read operations return it. `definition` is an object with an
#: `items` array here, while requests send a bare array — the asymmetry is upstream's.
#: `modified_time_utc` uses a numeric "+0000" offset rather than a trailing "Z".
CUSTOM_FIELD_PAYLOAD: dict[str, Any] = {
    "id": 42,
    "name": "spec_example_field",
    "data_source_id": "GAWA",
    "display_name": "Spec Example Field",
    "description": "Temporary transformation for spec examples",
    "field_type": "dim",
    "data_type": "string.text.value",
    "modified_time_utc": "2026-04-06T10:59:04+0000",
    "modified_user": {"email": "user@supermetrics.com", "first_name": "John", "last_name": "Doe"},
    "definition": {"items": ALL_STEP_KINDS},
    "report_types": ["Default"],
}

#: GET/PUT/POST of a single custom field — wrapped in {meta, data}.
CUSTOM_FIELD_SINGLE_BODY: dict[str, Any] = {"meta": META, "data": CUSTOM_FIELD_PAYLOAD}

#: GET the collection — double-wrapped: the page is at data.items and the pagination
#: metadata rides in meta, which is why list() drops it and with_raw_response keeps it.
CUSTOM_FIELD_LIST_BODY: dict[str, Any] = {
    "meta": {
        "request_id": META["request_id"],
        "pagination": {
            "total_count": 137,
            "limit": 25,
            "offset": 0,
            "links": {"next": {"href": "https://api.supermetrics.com/v1/teams/42/custom-fields?offset=25&limit=25"}},
        },
    },
    "data": {"items": [CUSTOM_FIELD_PAYLOAD]},
}

#: An empty page. Upstream marks `data` and `data.items` optional, so both can be
#: missing outright — list() has to answer [] rather than fall over.
CUSTOM_FIELD_EMPTY_LIST_BODY: dict[str, Any] = {
    "meta": {
        "request_id": META["request_id"],
        "pagination": {"total_count": 0, "limit": 25, "offset": 0},
    },
    "data": {},
}

#: GET .../custom-fields/metadata — wrapped, and every field inside `data` is optional.
CUSTOM_FIELD_METADATA_BODY: dict[str, Any] = {
    "meta": META,
    "data": {
        "rules": {
            "condition": {"items": [{"name": "equals", "display_name": "EQUALS"}]},
            "lookup": {"items": [{"name": "equals", "display_name": "EQUALS"}]},
        },
        "functions": {
            "items": [
                {
                    "name": "upper_case",
                    "display_name": "Upper Case",
                    "description": "Converts text to upper case",
                    "group_name": "String",
                    "arguments": [{"name": "value"}],
                    "return_types": ["string.text.value"],
                }
            ]
        },
        "field_data_types": ["string.text.value"],
        "output_data_types": {"items": [{"output_type": "string.text.value", "label": "STRING"}]},
        "data_transformation_steps_limit": 10,
    },
}


# --- Data blending ------------------------------------------------------------
#
# Blends live on the CORE api host under a "/v1" path prefix, the same shape as custom
# fields and the opposite of transfers. Route strings here therefore include the "/v1" —
# see docs.local/scratchpads/phase5-contract.md.
#
# Every collection in these bodies is wrapped in an {"items": [...]} object. Requests send
# the same collections as bare arrays. That asymmetry is upstream's and the SDK does not
# hide it, so the payloads below are written the way the API really answers.

#: The two blend routes, for team 42 and blend 569.
BLENDS_COLLECTION = "/v1/teams/42/data-blending/blends"
BLENDS_ITEM = "/v1/teams/42/data-blending/blends/569"

#: A field reference as a *response* carries it: addressed by `blend_data_source_id`, with
#: no `blend_data_source_key` — the key is a request-scoped alias and never comes back.
GA4_IMPRESSIONS_REF: dict[str, Any] = {
    "blend_data_source_id": 1,
    "datasource_field_name": "Impressions",
    "datasource_field_display_name": "Impressions",
    "datasource_field_type": "met",
    "datasource_field_data_type": "int.number.value",
    "field_source": "standard",
    "meta": None,
}

#: The same shape for the second source in a join, and with a non-null `meta`. The
#: generated model parses `meta` with a try/except cascade, so both the null and the
#: object form need exercising.
GADS_IMPRESSIONS_REF: dict[str, Any] = {
    "blend_data_source_id": 2,
    "datasource_field_name": "Impressions",
    "datasource_field_display_name": "Impressions",
    "datasource_field_type": "met",
    "datasource_field_data_type": "int.number.value",
    "field_source": "standard",
    "meta": {"account_override": "1234567890"},
}

#: A dimension reference, used as a join key.
GA4_DATE_REF: dict[str, Any] = {
    "blend_data_source_id": 1,
    "datasource_field_name": "Date",
    "datasource_field_display_name": "Date",
    "datasource_field_type": "dim",
    "datasource_field_data_type": "string.time.date",
    "field_source": "standard",
    "meta": None,
}

#: The same dimension on the joined source.
GADS_DATE_REF: dict[str, Any] = {
    "blend_data_source_id": 2,
    "datasource_field_name": "Date",
    "datasource_field_display_name": "Date",
    "datasource_field_type": "dim",
    "datasource_field_data_type": "string.time.date",
    "field_source": "standard",
    "meta": None,
}

#: A data source as a response carries it. `data_source_settings` exercises all four value
#: kinds the upstream anyOf allows — string, integer, boolean and null — because the
#: generated layer types them as one union and nothing else would catch a regression there.
GA4_SOURCE_OUTPUT: dict[str, Any] = {
    "blend_data_source_id": 1,
    "blend_id": 569,
    "data_source_id": "GA4",
    "display_name": "Google Analytics 4",
    "data_source_settings": {
        "items": [
            {"id": "currency", "value": "EUR"},
            {"id": "row_limit", "value": 1000},
            {"id": "include_empty_rows", "value": True},
            {"id": "sampling_level", "value": None},
        ]
    },
    "accounts": {"items": [{"account_id": "1234567890", "account_name": "Acme Corp"}]},
    "segments": {"items": [{"id": "organic_traffic", "name": "Organic Traffic"}]},
    "report_type": None,
    "report_type_settings": {"items": []},
    "logo_url": "https://cdn.supermetrics.com/images/datasource-logos/GA4.png",
}

#: The second source, present only in the join blend.
GADS_SOURCE_OUTPUT: dict[str, Any] = {
    "blend_data_source_id": 2,
    "blend_id": 569,
    "data_source_id": "GADS",
    "display_name": "Google Ads",
    "data_source_settings": {"items": []},
    "accounts": {"items": []},
    "segments": {"items": []},
    "report_type": "organic_search",
    "report_type_settings": {"items": [{"id": "date_range", "value": "last_30_days"}]},
    "logo_url": "https://cdn.supermetrics.com/images/datasource-logos/GADS.png",
}

#: A union blend: `config` carries `fields` and nothing else. Note `blend_field_type` and
#: `blend_field_data_type`, which the response adds — a request has no way to set them.
#: `modified_time_utc` uses a numeric "+0000" offset rather than a trailing "Z".
UNION_BLEND_PAYLOAD: dict[str, Any] = {
    "blend_id": 569,
    "blend_uuid": "71bc0582-31b5-11f1-a55c-4201ac182030",
    "type": "union",
    "display_name": "GA4 impressions",
    "description": "Example blend description",
    "modified_time_utc": "2026-04-07T10:00:00+0000",
    "last_modify_user_email": "user@supermetrics.com",
    "blended_data_sources": {"items": [GA4_SOURCE_OUTPUT]},
    "config": {
        "fields": {
            "items": [
                {
                    "blend_field_name": "impressions",
                    "blend_field_display_name": "Impressions",
                    "blend_field_type": "met",
                    "blend_field_data_type": "int.number.value",
                    "blend_datasource_fields": {"items": [GA4_IMPRESSIONS_REF]},
                }
            ]
        }
    },
}

#: A join blend: `config` additionally carries `query_table` and `joins`. Nothing in the
#: spec discriminates the two kinds, so both shapes have to be round-tripped for real.
JOIN_BLEND_PAYLOAD: dict[str, Any] = {
    "blend_id": 569,
    "blend_uuid": "71bc0582-31b5-11f1-a55c-4201ac182030",
    "type": "join",
    "display_name": "GA4 joined to Google Ads",
    "description": None,
    "modified_time_utc": "2026-04-07T10:00:00+0000",
    "last_modify_user_email": "user@supermetrics.com",
    "blended_data_sources": {"items": [GA4_SOURCE_OUTPUT, GADS_SOURCE_OUTPUT]},
    "config": {
        "query_table": {"blend_data_source_id": 1},
        "joins": {
            "items": [
                {
                    "join_table": {"blend_data_source_id": 2},
                    "type": "left",
                    "conditions": {"items": [{"operator": "=", "left": GA4_DATE_REF, "right": GADS_DATE_REF}]},
                }
            ]
        },
        "fields": {
            "items": [
                {
                    "blend_field_name": "impressions",
                    "blend_field_display_name": "Impressions",
                    "blend_field_type": "met",
                    "blend_field_data_type": "int.number.value",
                    "blend_datasource_fields": {"items": [GA4_IMPRESSIONS_REF, GADS_IMPRESSIONS_REF]},
                }
            ]
        },
    },
}

#: GET/POST/PUT of a single blend — wrapped in {meta, data}.
BLEND_SINGLE_BODY: dict[str, Any] = {"meta": META, "data": UNION_BLEND_PAYLOAD}

#: The same envelope around the join blend.
BLEND_JOIN_SINGLE_BODY: dict[str, Any] = {"meta": META, "data": JOIN_BLEND_PAYLOAD}

#: One item of the list response. A summary has no `config` at all and a reduced data
#: source shape, so a caller who wants a blend's fields has to GET it by id.
BLEND_SUMMARY_PAYLOAD: dict[str, Any] = {
    "blend_id": 569,
    "blend_uuid": "71bc0582-31b5-11f1-a55c-4201ac182030",
    "type": "union",
    "display_name": "GA4 impressions",
    "description": "Example blend description",
    "modified_time_utc": "2026-04-07T10:00:00+0000",
    "last_modify_user_email": "user@supermetrics.com",
    "blended_data_sources": {
        "items": [
            {
                "blend_data_source_id": 1,
                "data_source_id": "GA4",
                "display_name": "Google Analytics 4",
                "logo_url": "https://cdn.supermetrics.com/images/datasource-logos/GA4.png",
            }
        ]
    },
}

#: A second summary, of the other kind, so a `?type=` filter has something to filter.
BLEND_JOIN_SUMMARY_PAYLOAD: dict[str, Any] = {
    "blend_id": 570,
    "blend_uuid": "8a2f1e64-31b5-11f1-a55c-4201ac182031",
    "type": "join",
    "display_name": "GA4 joined to Google Ads",
    "description": None,
    "modified_time_utc": "2026-04-08T09:30:00+0000",
    "last_modify_user_email": "user@supermetrics.com",
    "blended_data_sources": {"items": []},
}

#: GET the collection. Single-wrapped, unlike custom fields: this endpoint is not
#: paginated, so `meta` carries a request id and nothing else.
BLEND_LIST_BODY: dict[str, Any] = {
    "meta": META,
    "data": {"items": [BLEND_SUMMARY_PAYLOAD, BLEND_JOIN_SUMMARY_PAYLOAD]},
}

#: An empty collection. `data.items` is optional upstream and can be missing outright,
#: so list() has to answer [] rather than fall over.
BLEND_EMPTY_LIST_BODY: dict[str, Any] = {"meta": META, "data": {}}


# --- Teams & user identity ----------------------------------------------------
#
# Teams live on the CORE api host under a "/v1" path prefix — the same shape as custom
# fields, account tags and blends, and the opposite of transfers. Route strings here
# therefore include the "/v1"; a dropped prefix or an accidental re-host to the Data
# Warehouse host would leave them unmatched and surface as the server's default 404.
#
# Both responses are wrapped in {"meta": ..., "data": ...}. Unlike account tags, `data`
# is required on these two schemas, so an empty team is `{"data": []}`, never a body with
# no `data` key at all.

#: The two team routes, for team 42.
TEAM_ITEM = "/v1/teams/42"
TEAM_USERS = "/v1/teams/42/users"

#: One team as GET /v1/teams/{team_id} returns it, under `data`. `created_at` is an ISO
#: 8601 timestamp with a numeric "+00:00" offset, and `display_id` is the SM_-prefixed
#: human-readable identifier.
TEAM_PAYLOAD: dict[str, Any] = {
    "team_id": 42,
    "name": "My Team",
    "display_id": "SM_ABC123",
    "status": 1,
    "created_at": "2026-01-01T00:00:00+00:00",
}

#: GET a single team — wrapped in {meta, data}.
TEAM_GET_BODY: dict[str, Any] = {"meta": META, "data": TEAM_PAYLOAD}

#: The first member of a team, an administrator.
TEAM_USER_PAYLOAD: dict[str, Any] = {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "ADMIN",
    "created_at": "2026-01-01T00:00:00+00:00",
}

#: A second member, a plain user, so a list assertion has more than one row to check.
TEAM_MEMBER_PAYLOAD: dict[str, Any] = {
    "user_id": 2,
    "email": "member@example.com",
    "first_name": "Jane",
    "last_name": "Roe",
    "role": "MEMBER",
    "created_at": "2026-02-01T00:00:00+00:00",
}

#: GET /v1/teams/{team_id}/users — wrapped, with `data` a bare array. This endpoint is not
#: paginated, so `meta` carries a request id and nothing else.
TEAM_USERS_BODY: dict[str, Any] = {"meta": META, "data": [TEAM_USER_PAYLOAD, TEAM_MEMBER_PAYLOAD]}

#: An empty team. `data` is a required array on this schema, so empty is `[]`, not absent.
TEAM_USERS_EMPTY_BODY: dict[str, Any] = {"meta": META, "data": []}


@dataclass(frozen=True)
class RecordedRequest:
    """A request as the server actually received it.

    Attributes:
        method: HTTP method, upper-case.
        path: Request path including the query string.
        headers: Request headers with lower-cased names.
        body: Raw request body bytes.
        client_port: Source port of the connection, used to prove pool reuse.
    """

    method: str
    path: str
    headers: dict[str, str]
    body: bytes
    client_port: int

    @property
    def authorization(self) -> str | None:
        """The ``Authorization`` header value, if the request carried one."""
        return self.headers.get("authorization")

    @property
    def bearer_token(self) -> str | None:
        """The bare bearer token, with the ``Bearer`` scheme stripped."""
        value = self.authorization
        if value is None or not value.lower().startswith("bearer "):
            return value
        return value[len("bearer ") :]

    def json(self) -> Any:
        """Decode the request body as JSON.

        Returns:
            The decoded payload, or ``None`` when the body is empty.
        """
        return json.loads(self.body) if self.body else None


@dataclass
class ScriptedResponse:
    """A response the mock server should return.

    Attributes:
        status: HTTP status code to send.
        json_body: Payload to serialize as JSON. Ignored when ``raw_body`` is set.
        headers: Extra response headers.
        delay: Seconds to sleep before responding, used to trigger real timeouts.
        raw_body: Exact body bytes, bypassing JSON serialization.
    """

    status: int = 200
    json_body: Any = None
    headers: dict[str, str] = field(default_factory=dict)
    delay: float = 0.0
    raw_body: bytes | None = None

    def body_bytes(self) -> bytes:
        """Return the response body as bytes."""
        if self.raw_body is not None:
            return self.raw_body
        if self.json_body is None:
            return b""
        return json.dumps(self.json_body).encode()


class MockAPIServer:
    """A real HTTP server that serves scripted responses and records requests.

    Routes are keyed by path (query strings are ignored when matching). Each route
    holds a queue of responses; once the queue is down to its final entry, that
    entry is served for every subsequent request, which keeps repeat-call tests
    simple.

    Example:
        ```python
        server.route("/ds/logins", ScriptedResponse(json_body={"data": []}))
        client = SupermetricsClient(api_key="k", base_url=server.base_url)
        client.logins.list()
        assert server.last_request.bearer_token == "k"
        ```
    """

    def __init__(self) -> None:
        """Start the server on an ephemeral loopback port."""
        self._routes: dict[str, list[ScriptedResponse]] = {}
        self._requests: list[RecordedRequest] = []
        self._lock = threading.Lock()
        self._default = ScriptedResponse(status=404, json_body={"error": {"code": "NOT_FOUND", "message": "no route"}})

        server = self

        class _Handler(BaseHTTPRequestHandler):
            # HTTP/1.1 keeps connections alive, so tests can prove pool reuse.
            protocol_version = "HTTP/1.1"

            def _handle(self) -> None:
                try:
                    self._respond()
                except (BrokenPipeError, ConnectionResetError):
                    # Expected when a timeout test abandons the request mid-flight.
                    self.close_connection = True

            def _respond(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                server._record(
                    RecordedRequest(
                        method=self.command,
                        path=self.path,
                        headers={k.lower(): v for k, v in self.headers.items()},
                        body=body,
                        client_port=self.client_address[1],
                    )
                )
                scripted = server._next_response(self.path)
                if scripted.delay:
                    time.sleep(scripted.delay)
                payload = scripted.body_bytes()
                self.send_response(scripted.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                for key, value in scripted.headers.items():
                    self.send_header(key, value)
                self.end_headers()
                if payload:
                    self.wfile.write(payload)

            do_GET = _handle
            do_POST = _handle
            do_PUT = _handle
            do_PATCH = _handle
            do_DELETE = _handle

            def log_message(self, format: str, *args: Any) -> None:
                """Silence the default stderr access log."""

            def handle_one_request(self) -> None:
                """Handle one request, swallowing disconnects from abandoned calls."""
                try:
                    super().handle_one_request()
                except (BrokenPipeError, ConnectionResetError):
                    self.close_connection = True

        class _Server(ThreadingHTTPServer):
            def handle_error(self, request: Any, client_address: Any) -> None:
                """Swallow the traceback a client disconnect would otherwise print."""

        self._httpd = _Server(("127.0.0.1", 0), _Handler)
        self._httpd.daemon_threads = True
        # A short poll interval keeps shutdown() from blocking for the default 0.5s,
        # which across ~90 tests and six CI legs is most of the suite's wall clock.
        self._thread = threading.Thread(target=self._httpd.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        self._thread.start()

    @property
    def base_url(self) -> str:
        """Base URL to hand to a Supermetrics client."""
        host, port = self._httpd.server_address[:2]
        return f"http://{host}:{port}"

    @property
    def requests(self) -> list[RecordedRequest]:
        """A snapshot of every request received so far, in arrival order."""
        with self._lock:
            return list(self._requests)

    @property
    def last_request(self) -> RecordedRequest:
        """The most recently received request.

        Raises:
            AssertionError: If no request has been received.
        """
        received = self.requests
        assert received, "no request was received by the mock server"
        return received[-1]

    def route(self, path: str, *responses: ScriptedResponse) -> None:
        """Register the responses to serve for ``path``.

        Args:
            path: Request path to match, without a query string.
            responses: Responses to serve in order. The last one repeats.
        """
        with self._lock:
            self._routes[path] = list(responses) or [ScriptedResponse()]

    def set_default(self, response: ScriptedResponse) -> None:
        """Set the response served for paths with no registered route.

        Args:
            response: The fallback response.
        """
        self._default = response

    def clear(self) -> None:
        """Forget all recorded requests."""
        with self._lock:
            self._requests.clear()

    def stop(self) -> None:
        """Shut the server down and join its thread."""
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)

    def _record(self, request: RecordedRequest) -> None:
        with self._lock:
            self._requests.append(request)

    def _next_response(self, path: str) -> ScriptedResponse:
        key = path.split("?", 1)[0]
        with self._lock:
            queue = self._routes.get(key)
            if not queue:
                return self._default
            return queue.pop(0) if len(queue) > 1 else queue[0]


@pytest.fixture
def api_server() -> Iterator[MockAPIServer]:
    """Provide a running :class:`MockAPIServer` for one test."""
    server = MockAPIServer()
    try:
        yield server
    finally:
        server.stop()


@pytest.fixture
def logins_server(api_server: MockAPIServer) -> MockAPIServer:
    """A server with the two login routes wired to successful responses."""
    api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY))
    api_server.route("/ds/login/login_abc123", ScriptedResponse(json_body=LOGIN_GET_BODY))
    return api_server


@pytest.fixture
def dts_server() -> Iterator[MockAPIServer]:
    """A second server, standing in for the Data Warehouse host.

    Transfers, transfer runs, backfills, data source connections and destinations
    are served from ``dts-api.supermetrics.com`` rather than the core API host. Two
    servers is the only way to prove the SDK actually re-hosts those requests instead
    of merely building the right path.
    """
    server = MockAPIServer()
    try:
        yield server
    finally:
        server.stop()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Mark every test collected from ``tests/e2e`` with the ``e2e`` marker.

    CI runs a dedicated job as ``pytest tests/e2e -m e2e``. When membership of that
    job depends on each module remembering ``pytestmark = pytest.mark.e2e``, a file
    that forgets the line — or misspells it — is silently deselected there while
    still passing in the matrix ``test`` job, so the e2e job stays green while
    covering less. Deriving the marker from the file's location instead makes the
    job's contents a property of where a test lives, which cannot be forgotten.

    ``--strict-markers`` (see ``addopts`` in ``pyproject.toml``) closes the other
    half: a misspelt marker is now a collection error rather than a warning.

    Live smoke tests are left alone. They live in this directory but talk to the
    real API, are opt-in behind ``-m live`` and a credential check, and must stay
    out of the hermetic e2e job.

    Args:
        config: The active pytest configuration. Unused; part of the hook signature.
        items: The collected items, modified in place.
    """
    e2e_dir = Path(__file__).parent
    for item in items:
        path = getattr(item, "path", None)
        if path is None or not path.is_relative_to(e2e_dir):
            continue
        if item.get_closest_marker("live") is not None:
            continue
        item.add_marker(pytest.mark.e2e)


@pytest.fixture
def custom_fields_server(api_server: MockAPIServer) -> MockAPIServer:
    """A server with the three custom-field routes wired to successful responses.

    The paths carry the ``/v1`` prefix because custom fields are served from the core
    API host, where the version lives in the path. Getting this wrong surfaces as a
    ``SupermetricsNotFoundError`` from the server's default 404 route rather than as an
    obvious fixture mistake.

    Note:
        ``/metadata`` and ``/{custom_field_id}`` are distinct routes here, so a
        ``get_metadata`` call that wrongly hit the by-id path would 404 rather than
        silently return a custom field.
    """
    api_server.route(CUSTOM_FIELDS_COLLECTION, ScriptedResponse(json_body=CUSTOM_FIELD_LIST_BODY))
    api_server.route(CUSTOM_FIELDS_ITEM, ScriptedResponse(json_body=CUSTOM_FIELD_SINGLE_BODY))
    api_server.route(CUSTOM_FIELDS_METADATA, ScriptedResponse(json_body=CUSTOM_FIELD_METADATA_BODY))
    return api_server


@pytest.fixture
def blends_server(api_server: MockAPIServer) -> MockAPIServer:
    """A server with both blend routes wired to successful responses.

    The paths carry the ``/v1`` prefix because blends are served from the core API host,
    where the version lives in the path. Getting this wrong surfaces as a
    ``SupermetricsNotFoundError`` from the server's default 404 route rather than as an
    obvious fixture mistake.

    Note:
        The collection answers a two-item list and the item route answers the union
        blend. Tests that need the join blend, a 201, or a 204 re-route the path
        themselves — the last response passed to ``route`` repeats, so overriding one
        route leaves the other intact.
    """
    api_server.route(BLENDS_COLLECTION, ScriptedResponse(json_body=BLEND_LIST_BODY))
    api_server.route(BLENDS_ITEM, ScriptedResponse(json_body=BLEND_SINGLE_BODY))
    return api_server


@pytest.fixture
def teams_server(api_server: MockAPIServer) -> MockAPIServer:
    """A server with both team routes wired to successful responses.

    The paths carry the ``/v1`` prefix because teams are served from the core API host,
    where the version lives in the path. Getting this wrong surfaces as a
    ``SupermetricsNotFoundError`` from the server's default 404 route rather than as an
    obvious fixture mistake.

    Note:
        The item route answers a single team and the users route answers a two-member
        list. Tests that need an empty team, or a specific failure status, re-route the
        path themselves — the last response passed to ``route`` repeats, so overriding one
        route leaves the other intact.
    """
    api_server.route(TEAM_ITEM, ScriptedResponse(json_body=TEAM_GET_BODY))
    api_server.route(TEAM_USERS, ScriptedResponse(json_body=TEAM_USERS_BODY))
    return api_server
