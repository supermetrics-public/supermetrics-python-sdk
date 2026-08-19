from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlendConfigOutputQueryTable")


@_attrs_define
class BlendConfigOutputQueryTable:
    """Primary (left-hand) data source — present for join blends only.

    Attributes:
        blend_data_source_id (int | None | Unset): Internal ID of the primary data source. Example: 146715.
    """

    blend_data_source_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_data_source_id: int | None | Unset
        if isinstance(self.blend_data_source_id, Unset):
            blend_data_source_id = UNSET
        else:
            blend_data_source_id = self.blend_data_source_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blend_data_source_id is not UNSET:
            field_dict["blend_data_source_id"] = blend_data_source_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_blend_data_source_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        blend_data_source_id = _parse_blend_data_source_id(d.pop("blend_data_source_id", UNSET))

        blend_config_output_query_table = cls(
            blend_data_source_id=blend_data_source_id,
        )

        blend_config_output_query_table.additional_properties = d
        return blend_config_output_query_table

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
