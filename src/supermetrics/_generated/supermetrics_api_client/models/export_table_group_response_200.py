from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_definition import FieldDefinition
    from ..models.table_definition import TableDefinition
    from ..models.table_group_export import TableGroupExport


T = TypeVar("T", bound="ExportTableGroupResponse200")


@_attrs_define
class ExportTableGroupResponse200:
    """
    Attributes:
        version (int | Unset): Data model version
        group (TableGroupExport | Unset):
        tables (list[TableDefinition] | Unset): List of table objects
        fields (list[FieldDefinition] | Unset): List of field objects
    """

    version: int | Unset = UNSET
    group: TableGroupExport | Unset = UNSET
    tables: list[TableDefinition] | Unset = UNSET
    fields: list[FieldDefinition] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        group: dict[str, Any] | Unset = UNSET
        if not isinstance(self.group, Unset):
            group = self.group.to_dict()

        tables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tables, Unset):
            tables = []
            for tables_item_data in self.tables:
                tables_item = tables_item_data.to_dict()
                tables.append(tables_item)

        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if group is not UNSET:
            field_dict["group"] = group
        if tables is not UNSET:
            field_dict["tables"] = tables
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.field_definition import FieldDefinition
        from ..models.table_definition import TableDefinition
        from ..models.table_group_export import TableGroupExport

        d = dict(src_dict)
        version = d.pop("version", UNSET)

        _group = d.pop("group", UNSET)
        group: TableGroupExport | Unset
        if isinstance(_group, Unset):
            group = UNSET
        else:
            group = TableGroupExport.from_dict(_group)

        _tables = d.pop("tables", UNSET)
        tables: list[TableDefinition] | Unset = UNSET
        if _tables is not UNSET:
            tables = []
            for tables_item_data in _tables:
                tables_item = TableDefinition.from_dict(tables_item_data)

                tables.append(tables_item)

        _fields = d.pop("fields", UNSET)
        fields: list[FieldDefinition] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = FieldDefinition.from_dict(fields_item_data)

                fields.append(fields_item)

        export_table_group_response_200 = cls(
            version=version,
            group=group,
            tables=tables,
            fields=fields,
        )

        export_table_group_response_200.additional_properties = d
        return export_table_group_response_200

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
