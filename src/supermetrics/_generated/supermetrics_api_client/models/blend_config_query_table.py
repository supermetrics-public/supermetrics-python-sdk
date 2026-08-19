from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlendConfigQueryTable")


@_attrs_define
class BlendConfigQueryTable:
    """Primary (left-hand) data source — present for join blends only. Provide `blend_data_source_key` when creating,
    `blend_data_source_id` when updating with an existing data source.

        Attributes:
            blend_data_source_id (int | None | Unset): Internal ID of the primary data source. Example: 146715.
            blend_data_source_key (None | str | Unset): Key of the primary data source (for new data sources). Example:
                abcd1234.
    """

    blend_data_source_id: int | None | Unset = UNSET
    blend_data_source_key: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_data_source_id: int | None | Unset
        if isinstance(self.blend_data_source_id, Unset):
            blend_data_source_id = UNSET
        else:
            blend_data_source_id = self.blend_data_source_id

        blend_data_source_key: None | str | Unset
        if isinstance(self.blend_data_source_key, Unset):
            blend_data_source_key = UNSET
        else:
            blend_data_source_key = self.blend_data_source_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blend_data_source_id is not UNSET:
            field_dict["blend_data_source_id"] = blend_data_source_id
        if blend_data_source_key is not UNSET:
            field_dict["blend_data_source_key"] = blend_data_source_key

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

        def _parse_blend_data_source_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        blend_data_source_key = _parse_blend_data_source_key(d.pop("blend_data_source_key", UNSET))

        blend_config_query_table = cls(
            blend_data_source_id=blend_data_source_id,
            blend_data_source_key=blend_data_source_key,
        )

        blend_config_query_table.additional_properties = d
        return blend_config_query_table

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
