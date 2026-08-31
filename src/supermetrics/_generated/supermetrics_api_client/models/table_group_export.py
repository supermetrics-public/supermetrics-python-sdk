from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TableGroupExport")


@_attrs_define
class TableGroupExport:
    """
    Attributes:
        group_id (str | Unset): Supermetrics table group ID
        group_name (str | Unset): Table group name
        ds_id (str | Unset): Data source ID
        table_prefix (str | Unset): Prefix to table names. Enforced into upper snake case.
    """

    group_id: str | Unset = UNSET
    group_name: str | Unset = UNSET
    ds_id: str | Unset = UNSET
    table_prefix: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_id = self.group_id

        group_name = self.group_name

        ds_id = self.ds_id

        table_prefix = self.table_prefix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if ds_id is not UNSET:
            field_dict["ds_id"] = ds_id
        if table_prefix is not UNSET:
            field_dict["table_prefix"] = table_prefix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_id = d.pop("group_id", UNSET)

        group_name = d.pop("group_name", UNSET)

        ds_id = d.pop("ds_id", UNSET)

        table_prefix = d.pop("table_prefix", UNSET)

        table_group_export = cls(
            group_id=group_id,
            group_name=group_name,
            ds_id=ds_id,
            table_prefix=table_prefix,
        )

        table_group_export.additional_properties = d
        return table_group_export

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
