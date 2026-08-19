from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_config_query_table import BlendConfigQueryTable
    from ..models.blend_field import BlendField
    from ..models.blend_join import BlendJoin


T = TypeVar("T", bound="BlendConfig")


@_attrs_define
class BlendConfig:
    """Field mappings and join configuration for the blend (request). Union blends contain only `fields`; join blends also
    include `query_table` and `joins`.

        Attributes:
            query_table (BlendConfigQueryTable | Unset): Primary (left-hand) data source — present for join blends only.
                Provide `blend_data_source_key` when creating, `blend_data_source_id` when updating with an existing data
                source.
            joins (list[BlendJoin] | Unset): Join definitions — present for join blends only.
            fields (list[BlendField] | Unset): Field definitions for the blend.
    """

    query_table: BlendConfigQueryTable | Unset = UNSET
    joins: list[BlendJoin] | Unset = UNSET
    fields: list[BlendField] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_table: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query_table, Unset):
            query_table = self.query_table.to_dict()

        joins: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.joins, Unset):
            joins = []
            for joins_item_data in self.joins:
                joins_item = joins_item_data.to_dict()
                joins.append(joins_item)

        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_table is not UNSET:
            field_dict["query_table"] = query_table
        if joins is not UNSET:
            field_dict["joins"] = joins
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_config_query_table import BlendConfigQueryTable
        from ..models.blend_field import BlendField
        from ..models.blend_join import BlendJoin

        d = dict(src_dict)
        _query_table = d.pop("query_table", UNSET)
        query_table: BlendConfigQueryTable | Unset
        if isinstance(_query_table, Unset):
            query_table = UNSET
        else:
            query_table = BlendConfigQueryTable.from_dict(_query_table)

        _joins = d.pop("joins", UNSET)
        joins: list[BlendJoin] | Unset = UNSET
        if _joins is not UNSET:
            joins = []
            for joins_item_data in _joins:
                joins_item = BlendJoin.from_dict(joins_item_data)

                joins.append(joins_item)

        _fields = d.pop("fields", UNSET)
        fields: list[BlendField] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = BlendField.from_dict(fields_item_data)

                fields.append(fields_item)

        blend_config = cls(
            query_table=query_table,
            joins=joins,
            fields=fields,
        )

        blend_config.additional_properties = d
        return blend_config

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
