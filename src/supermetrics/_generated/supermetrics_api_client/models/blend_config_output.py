from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_config_output_fields import BlendConfigOutputFields
    from ..models.blend_config_output_joins import BlendConfigOutputJoins
    from ..models.blend_config_output_query_table import BlendConfigOutputQueryTable


T = TypeVar("T", bound="BlendConfigOutput")


@_attrs_define
class BlendConfigOutput:
    """Field mappings and join configuration for the blend (response). Union blends contain only `fields`; join blends also
    include `query_table` and `joins`.

        Attributes:
            query_table (BlendConfigOutputQueryTable | Unset): Primary (left-hand) data source — present for join blends
                only.
            joins (BlendConfigOutputJoins | Unset): Join definitions — present for join blends only.
            fields (BlendConfigOutputFields | Unset): Field definitions for the blend.
    """

    query_table: BlendConfigOutputQueryTable | Unset = UNSET
    joins: BlendConfigOutputJoins | Unset = UNSET
    fields: BlendConfigOutputFields | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_table: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query_table, Unset):
            query_table = self.query_table.to_dict()

        joins: dict[str, Any] | Unset = UNSET
        if not isinstance(self.joins, Unset):
            joins = self.joins.to_dict()

        fields: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

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
        from ..models.blend_config_output_fields import BlendConfigOutputFields
        from ..models.blend_config_output_joins import BlendConfigOutputJoins
        from ..models.blend_config_output_query_table import BlendConfigOutputQueryTable

        d = dict(src_dict)
        _query_table = d.pop("query_table", UNSET)
        query_table: BlendConfigOutputQueryTable | Unset
        if isinstance(_query_table, Unset):
            query_table = UNSET
        else:
            query_table = BlendConfigOutputQueryTable.from_dict(_query_table)

        _joins = d.pop("joins", UNSET)
        joins: BlendConfigOutputJoins | Unset
        if isinstance(_joins, Unset):
            joins = UNSET
        else:
            joins = BlendConfigOutputJoins.from_dict(_joins)

        _fields = d.pop("fields", UNSET)
        fields: BlendConfigOutputFields | Unset
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = BlendConfigOutputFields.from_dict(_fields)

        blend_config_output = cls(
            query_table=query_table,
            joins=joins,
            fields=fields,
        )

        blend_config_output.additional_properties = d
        return blend_config_output

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
