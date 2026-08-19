from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_join_condition_output_operator import (
    BlendJoinConditionOutputOperator,
    check_blend_join_condition_output_operator,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_datasource_field_ref_output import BlendDatasourceFieldRefOutput


T = TypeVar("T", bound="BlendJoinConditionOutput")


@_attrs_define
class BlendJoinConditionOutput:
    """A condition comparing one field from each data source (response).

    Attributes:
        operator (BlendJoinConditionOutputOperator | Unset): Comparison operator. Example: =.
        left (BlendDatasourceFieldRefOutput | Unset): A field reference within a data source (response).
        right (BlendDatasourceFieldRefOutput | Unset): A field reference within a data source (response).
    """

    operator: BlendJoinConditionOutputOperator | Unset = UNSET
    left: BlendDatasourceFieldRefOutput | Unset = UNSET
    right: BlendDatasourceFieldRefOutput | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator: str | Unset = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator

        left: dict[str, Any] | Unset = UNSET
        if not isinstance(self.left, Unset):
            left = self.left.to_dict()

        right: dict[str, Any] | Unset = UNSET
        if not isinstance(self.right, Unset):
            right = self.right.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operator is not UNSET:
            field_dict["operator"] = operator
        if left is not UNSET:
            field_dict["left"] = left
        if right is not UNSET:
            field_dict["right"] = right

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_datasource_field_ref_output import BlendDatasourceFieldRefOutput

        d = dict(src_dict)
        _operator = d.pop("operator", UNSET)
        operator: BlendJoinConditionOutputOperator | Unset
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = check_blend_join_condition_output_operator(_operator)

        _left = d.pop("left", UNSET)
        left: BlendDatasourceFieldRefOutput | Unset
        if isinstance(_left, Unset):
            left = UNSET
        else:
            left = BlendDatasourceFieldRefOutput.from_dict(_left)

        _right = d.pop("right", UNSET)
        right: BlendDatasourceFieldRefOutput | Unset
        if isinstance(_right, Unset):
            right = UNSET
        else:
            right = BlendDatasourceFieldRefOutput.from_dict(_right)

        blend_join_condition_output = cls(
            operator=operator,
            left=left,
            right=right,
        )

        blend_join_condition_output.additional_properties = d
        return blend_join_condition_output

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
