from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.team_settings_response_data_type import (
    TeamSettingsResponseDataType,
    check_team_settings_response_data_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamSettingsResponseData")


@_attrs_define
class TeamSettingsResponseData:
    """
    Attributes:
        api_json_unescaped_slashes (bool | Unset): Whether to unescape forward slashes for all authenticated JSON
            responses. Defaults to false. You might need to turn this when integrating into some systems, such as BigQuery.
        api_json_unescaped_unicode (bool | Unset): Whether to unescape unicode characters for all authenticated JSON
            responses. Defaults to false. You might need to turn this on when integrating into some systems, such as
            BigQuery.
        query_default_timezone (None | str | Unset): Default timezone to add to all queries that are missing one. Value
            is either a valid database timezone name or null for system timezone.
        tableau_default_no_headers (bool | Unset): Whether Tableau output format should hide header row by default or
            not. Defaults to true for teams enrolled after June 2nd 2022.
        type_ (TeamSettingsResponseDataType | Unset):
    """

    api_json_unescaped_slashes: bool | Unset = UNSET
    api_json_unescaped_unicode: bool | Unset = UNSET
    query_default_timezone: None | str | Unset = UNSET
    tableau_default_no_headers: bool | Unset = UNSET
    type_: TeamSettingsResponseDataType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_json_unescaped_slashes = self.api_json_unescaped_slashes

        api_json_unescaped_unicode = self.api_json_unescaped_unicode

        query_default_timezone: None | str | Unset
        if isinstance(self.query_default_timezone, Unset):
            query_default_timezone = UNSET
        else:
            query_default_timezone = self.query_default_timezone

        tableau_default_no_headers = self.tableau_default_no_headers

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api_json_unescaped_slashes is not UNSET:
            field_dict["api_json_unescaped_slashes"] = api_json_unescaped_slashes
        if api_json_unescaped_unicode is not UNSET:
            field_dict["api_json_unescaped_unicode"] = api_json_unescaped_unicode
        if query_default_timezone is not UNSET:
            field_dict["query_default_timezone"] = query_default_timezone
        if tableau_default_no_headers is not UNSET:
            field_dict["tableau_default_no_headers"] = tableau_default_no_headers
        if type_ is not UNSET:
            field_dict["@type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_json_unescaped_slashes = d.pop("api_json_unescaped_slashes", UNSET)

        api_json_unescaped_unicode = d.pop("api_json_unescaped_unicode", UNSET)

        def _parse_query_default_timezone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        query_default_timezone = _parse_query_default_timezone(d.pop("query_default_timezone", UNSET))

        tableau_default_no_headers = d.pop("tableau_default_no_headers", UNSET)

        _type_ = d.pop("@type", UNSET)
        type_: TeamSettingsResponseDataType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_team_settings_response_data_type(_type_)

        team_settings_response_data = cls(
            api_json_unescaped_slashes=api_json_unescaped_slashes,
            api_json_unescaped_unicode=api_json_unescaped_unicode,
            query_default_timezone=query_default_timezone,
            tableau_default_no_headers=tableau_default_no_headers,
            type_=type_,
        )

        team_settings_response_data.additional_properties = d
        return team_settings_response_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
