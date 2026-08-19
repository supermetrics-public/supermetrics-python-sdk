from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_join_type import BlendJoinType, check_blend_join_type

if TYPE_CHECKING:
    from ..models.blend_join_condition import BlendJoinCondition
    from ..models.blend_join_join_table import BlendJoinJoinTable


T = TypeVar("T", bound="BlendJoin")


@_attrs_define
class BlendJoin:
    """Join definition between the primary table and one other data source (request).

    Attributes:
        join_table (BlendJoinJoinTable): Data source to join with the primary table. Provide `blend_data_source_key`
            when creating, `blend_data_source_id` when updating with an existing data source.
        type_ (BlendJoinType): Join type. Example: left.
        conditions (list[BlendJoinCondition]): Conditions that define how the two data sources are joined.
    """

    join_table: BlendJoinJoinTable
    type_: BlendJoinType
    conditions: list[BlendJoinCondition]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        join_table = self.join_table.to_dict()

        type_: str = self.type_

        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()
            conditions.append(conditions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "join_table": join_table,
                "type": type_,
                "conditions": conditions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_join_condition import BlendJoinCondition
        from ..models.blend_join_join_table import BlendJoinJoinTable

        d = dict(src_dict)
        join_table = BlendJoinJoinTable.from_dict(d.pop("join_table"))

        type_ = check_blend_join_type(d.pop("type"))

        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = BlendJoinCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        blend_join = cls(
            join_table=join_table,
            type_=type_,
            conditions=conditions,
        )

        blend_join.additional_properties = d
        return blend_join

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
