from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_join_output_type import BlendJoinOutputType, check_blend_join_output_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_join_output_conditions import BlendJoinOutputConditions
    from ..models.blend_join_output_join_table import BlendJoinOutputJoinTable


T = TypeVar("T", bound="BlendJoinOutput")


@_attrs_define
class BlendJoinOutput:
    """Join definition between two data sources (response).

    Attributes:
        join_table (BlendJoinOutputJoinTable | Unset): Data source joined with the primary table.
        type_ (BlendJoinOutputType | Unset): Join type. Example: left.
        conditions (BlendJoinOutputConditions | Unset): Conditions that define how the two data sources are joined.
    """

    join_table: BlendJoinOutputJoinTable | Unset = UNSET
    type_: BlendJoinOutputType | Unset = UNSET
    conditions: BlendJoinOutputConditions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        join_table: dict[str, Any] | Unset = UNSET
        if not isinstance(self.join_table, Unset):
            join_table = self.join_table.to_dict()

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        conditions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = self.conditions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if join_table is not UNSET:
            field_dict["join_table"] = join_table
        if type_ is not UNSET:
            field_dict["type"] = type_
        if conditions is not UNSET:
            field_dict["conditions"] = conditions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_join_output_conditions import BlendJoinOutputConditions
        from ..models.blend_join_output_join_table import BlendJoinOutputJoinTable

        d = dict(src_dict)
        _join_table = d.pop("join_table", UNSET)
        join_table: BlendJoinOutputJoinTable | Unset
        if isinstance(_join_table, Unset):
            join_table = UNSET
        else:
            join_table = BlendJoinOutputJoinTable.from_dict(_join_table)

        _type_ = d.pop("type", UNSET)
        type_: BlendJoinOutputType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_blend_join_output_type(_type_)

        _conditions = d.pop("conditions", UNSET)
        conditions: BlendJoinOutputConditions | Unset
        if isinstance(_conditions, Unset):
            conditions = UNSET
        else:
            conditions = BlendJoinOutputConditions.from_dict(_conditions)

        blend_join_output = cls(
            join_table=join_table,
            type_=type_,
            conditions=conditions,
        )

        blend_join_output.additional_properties = d
        return blend_join_output

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
