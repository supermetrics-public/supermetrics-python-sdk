from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_definition import FieldDefinition
    from ..models.table_definition import TableDefinition
    from ..models.table_group_import import TableGroupImport


T = TypeVar("T", bound="ImportTableGroupBody")


@_attrs_define
class ImportTableGroupBody:
    """
    Attributes:
        version (int): Data model version for the received data
        group (TableGroupImport):
        tables (list[TableDefinition]): List of table objects
        fields (list[FieldDefinition] | Unset): List of field objects
    """

    version: int
    group: TableGroupImport
    tables: list[TableDefinition]
    fields: list[FieldDefinition] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        group = self.group.to_dict()

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
        field_dict.update(
            {
                "version": version,
                "group": group,
                "tables": tables,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.field_definition import FieldDefinition
        from ..models.table_definition import TableDefinition
        from ..models.table_group_import import TableGroupImport

        d = dict(src_dict)
        version = d.pop("version")

        group = TableGroupImport.from_dict(d.pop("group"))

        tables = []
        _tables = d.pop("tables")
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

        import_table_group_body = cls(
            version=version,
            group=group,
            tables=tables,
            fields=fields,
        )

        import_table_group_body.additional_properties = d
        return import_table_group_body

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
