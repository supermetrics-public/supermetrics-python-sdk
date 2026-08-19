from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlendListDataSourceOutput")


@_attrs_define
class BlendListDataSourceOutput:
    """Simplified data source info returned in blend list responses.

    Attributes:
        blend_data_source_id (int | Unset): Internal ID of the blended data source. Example: 1.
        data_source_id (str | Unset): Data source identifier. Example: GA4.
        display_name (str | Unset): Display name of the data source. Example: Google Analytics 4.
        logo_url (str | Unset): Data source logo URL. Example: https://cdn.supermetrics.com/images/datasource-
            logos/GA4.png.
    """

    blend_data_source_id: int | Unset = UNSET
    data_source_id: str | Unset = UNSET
    display_name: str | Unset = UNSET
    logo_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_data_source_id = self.blend_data_source_id

        data_source_id = self.data_source_id

        display_name = self.display_name

        logo_url = self.logo_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blend_data_source_id is not UNSET:
            field_dict["blend_data_source_id"] = blend_data_source_id
        if data_source_id is not UNSET:
            field_dict["data_source_id"] = data_source_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        blend_data_source_id = d.pop("blend_data_source_id", UNSET)

        data_source_id = d.pop("data_source_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        logo_url = d.pop("logo_url", UNSET)

        blend_list_data_source_output = cls(
            blend_data_source_id=blend_data_source_id,
            data_source_id=data_source_id,
            display_name=display_name,
            logo_url=logo_url,
        )

        blend_list_data_source_output.additional_properties = d
        return blend_list_data_source_output

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
