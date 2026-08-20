"""Regression tests for response shapes the *real* API sends but the generated
models reject.

Every case here was found by running the SDK against production (see
docs.local/scratchpads/live_discovery.py). The pre-existing e2e fixtures for these
resources happened to include fields production omits, so they stayed green while the
same call crashed on real data. Each test below feeds the *production* shape through
the whole stack over a loopback socket and asserts the call succeeds.

All four defects are now fixed at the source — the OpenAPI spec was patched and the
generated models regenerated (see docs/openapi-spec-fixes.md). These tests lock the
fixes in: each reproduces the exact production shape that used to crash, so a future
regeneration that reintroduced the mismatch would fail here.

Root causes (all OpenAPI-spec vs production mismatches), now resolved:
  - custom_fields.list #1: Pagination required total_count/limit/offset; production
    meta.pagination omits them -> was KeyError: 'total_count'. Made optional.
  - custom_fields.list #4: PaginationLinks modelled next/previous as ResourceUrl
    objects; production sends first/prev/next/last as nullable URL strings ->
    was TypeError on the null ``next``. Redefined to nullable string URLs.
  - destinations.get: AuthMethod required ``label``; production auth methods send
    ``title`` (plus ``fields`` / ``new_secret_field``) -> was KeyError: 'label'.
    Redefined to the real shape.
  - account_tags.list: AccountTagListResponse expected ``data`` to be a bare list;
    production double-wraps it as ``data.items`` -> was ValueError from dict().
    Redefined to data.items and the adapter reads it.
"""

from __future__ import annotations

import pytest

from supermetrics import SupermetricsClient

from .conftest import META, MockAPIServer, ScriptedResponse

pytestmark = pytest.mark.e2e


# --- Bug #1: custom_fields.list pagination ------------------------------------

#: A custom field as the collection returns it (minimal, valid).
_CUSTOM_FIELD = {
    "id": 42,
    "name": "spec_example_field",
    "data_source_id": "GAWA",
    "display_name": "Spec Example Field",
    "field_type": "dim",
    "data_type": "string.text.value",
    "modified_time_utc": "2026-04-06T10:59:04+0000",
    "definition": {"items": []},
    "report_types": ["Default"],
}

#: The production shape: meta.pagination has ONLY ``links`` — no total_count/limit/offset.
CUSTOM_FIELDS_LIST_PROD_BODY = {
    "meta": {
        "request_id": META["request_id"],
        "pagination": {
            "links": {"first": "https://api/x?offset=0", "prev": None, "next": None, "last": "https://api/x?offset=0"}
        },
    },
    "data": {"items": [_CUSTOM_FIELD]},
}


def test_custom_fields_list_tolerates_pagination_without_totals(api_server: MockAPIServer) -> None:
    """A page whose pagination carries only ``links`` must still list its fields."""
    api_server.route("/v1/teams/42/custom-fields", ScriptedResponse(json_body=CUSTOM_FIELDS_LIST_PROD_BODY))

    with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
        fields = client.custom_fields.list(team_id=42)

    assert len(fields) == 1
    assert fields[0].id == 42


# --- Bug #3: account_tags.list double-wrapped data ----------------------------

#: The production shape: ``data`` is ``{"items": [...]}``, not a bare list.
ACCOUNT_TAGS_LIST_PROD_BODY = {
    "meta": {"request_id": META["request_id"]},
    "data": {
        "items": [
            {
                "name": "a1b2c3d",
                "display_name": "EMEA paid media",
                "color": "#112233",
                "data_source_count": 3,
                "account_count": 42,
            }
        ]
    },
}


def test_account_tags_list_tolerates_data_items_wrapper(api_server: MockAPIServer) -> None:
    """A double-wrapped ``data.items`` list must still surface the tags."""
    api_server.route("/v1/teams/42/account_tags", ScriptedResponse(json_body=ACCOUNT_TAGS_LIST_PROD_BODY))

    with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
        tags = client.account_tags.list(team_id=42)

    assert len(tags) == 1
    assert tags[0].display_name == "EMEA paid media"


# --- Bug #2: destinations.get auth_method shape -------------------------------


def _setting(id_: str) -> dict:
    """One destination setting field, in the production shape."""
    return {
        "input_type": "text",
        "options": [],
        "label": "Some label",
        "help_text": None,
        "help_url": None,
        "note": None,
        "is_required": True,
        "id": id_,
        "group": "g",
        "group_label": "Group",
        "value": "v",
        "show_for": [],
    }


#: The production shape of a destination detail. The auth method under
#: destination_type.auth_methods carries ``id``/``title``/``fields``/``new_secret_field``
#: and NO ``label`` — which is the field the generated AuthMethod model requires.
DESTINATION_GET_PROD_BODY = {
    "meta": {"request_id": META["request_id"]},
    "data": {
        "id": 11007,
        "display_name": "Analytics warehouse",
        "destination_type": {
            "title": "BigQuery",
            "type": "SQL_BQ",
            "connection_check_url": "https://x/check",
            "create_url": "https://x/create",
            "update_url_template": "https://x/update/{id}",
            "icon_url": "https://x/icon.png",
            "app_id": "bq",
            "is_internal": False,
            "settings": [_setting("project_id")],
            "auth_methods": [
                {
                    "id": "service_account",
                    "title": "Service account",
                    "fields": [_setting("key_json")],
                    "new_secret_field": _setting("key_json"),
                }
            ],
        },
        "edit_settings": [_setting("project_id")],
    },
}


def test_destinations_get_tolerates_auth_method_without_label(api_server: MockAPIServer) -> None:
    """A destination whose auth methods use ``title`` (not ``label``) must still parse."""
    api_server.route("/teams/42/destinations/11007", ScriptedResponse(json_body=DESTINATION_GET_PROD_BODY))

    with SupermetricsClient(api_key="api_k", base_url=api_server.base_url) as client:
        destination = client.destinations.get(team_id=42, destination_id=11007)

    assert destination.id == 11007
