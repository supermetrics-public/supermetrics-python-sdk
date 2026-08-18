from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransferDataSourceSetting")


@_attrs_define
class TransferDataSourceSetting:
    """
    Example:
        {'field_id': 'BRAND_KEYWORDS', 'value': '', 'group': 'Default'}

    Attributes:
        field_id (str | Unset): Setting field identifier
        value (bool | int | None | str | Unset): Setting value (type varies by field)
        group (str | Unset): Setting group identifier
    """

    field_id: str | Unset = UNSET
    value: bool | int | None | str | Unset = UNSET
    group: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        value: bool | int | None | str | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        group = self.group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_id is not UNSET:
            field_dict["field_id"] = field_id
        if value is not UNSET:
            field_dict["value"] = value
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field_id = d.pop("field_id", UNSET)

        def _parse_value(data: object) -> bool | int | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | int | None | str | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        group = d.pop("group", UNSET)

        transfer_data_source_setting = cls(
            field_id=field_id,
            value=value,
            group=group,
        )

        transfer_data_source_setting.additional_properties = d
        return transfer_data_source_setting

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
