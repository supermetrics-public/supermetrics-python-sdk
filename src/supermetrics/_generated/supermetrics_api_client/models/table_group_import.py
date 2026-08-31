from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TableGroupImport")


@_attrs_define
class TableGroupImport:
    """
    Attributes:
        group_name (str): Table group name
        ds_id (str): Data source ID
        table_prefix (str | Unset): Prefix to table names. Enforced into upper snake case. Maximum length is 15
            characters. Appended with an underscore.
    """

    group_name: str
    ds_id: str
    table_prefix: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_name = self.group_name

        ds_id = self.ds_id

        table_prefix = self.table_prefix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_name": group_name,
                "ds_id": ds_id,
            }
        )
        if table_prefix is not UNSET:
            field_dict["table_prefix"] = table_prefix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_name = d.pop("group_name")

        ds_id = d.pop("ds_id")

        table_prefix = d.pop("table_prefix", UNSET)

        table_group_import = cls(
            group_name=group_name,
            ds_id=ds_id,
            table_prefix=table_prefix,
        )

        table_group_import.additional_properties = d
        return table_group_import

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
