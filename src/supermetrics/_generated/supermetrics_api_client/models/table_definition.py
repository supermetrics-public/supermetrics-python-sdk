from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.table_definition_table_partition import (
    TableDefinitionTablePartition,
    check_table_definition_table_partition,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TableDefinition")


@_attrs_define
class TableDefinition:
    """
    Attributes:
        table_name (str): Table name. Enforced into upper snake case.
        fields (list[str]): List of field IDs for the table
        table_partition (TableDefinitionTablePartition | Unset): Table partition. Either date or none. Default: 'date'.
        report_type (None | str | Unset): Data source report type. Required for some data sources.
    """

    table_name: str
    fields: list[str]
    table_partition: TableDefinitionTablePartition | Unset = "date"
    report_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_name = self.table_name

        fields = self.fields

        table_partition: str | Unset = UNSET
        if not isinstance(self.table_partition, Unset):
            table_partition = self.table_partition

        report_type: None | str | Unset
        if isinstance(self.report_type, Unset):
            report_type = UNSET
        else:
            report_type = self.report_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_name": table_name,
                "fields": fields,
            }
        )
        if table_partition is not UNSET:
            field_dict["table_partition"] = table_partition
        if report_type is not UNSET:
            field_dict["report_type"] = report_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        table_name = d.pop("table_name")

        fields = cast(list[str], d.pop("fields"))

        _table_partition = d.pop("table_partition", UNSET)
        table_partition: TableDefinitionTablePartition | Unset
        if isinstance(_table_partition, Unset):
            table_partition = UNSET
        else:
            table_partition = check_table_definition_table_partition(_table_partition)

        def _parse_report_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        report_type = _parse_report_type(d.pop("report_type", UNSET))

        table_definition = cls(
            table_name=table_name,
            fields=fields,
            table_partition=table_partition,
            report_type=report_type,
        )

        table_definition.additional_properties = d
        return table_definition

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
