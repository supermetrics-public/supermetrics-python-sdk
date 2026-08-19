from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_join_condition_operator import BlendJoinConditionOperator, check_blend_join_condition_operator

if TYPE_CHECKING:
    from ..models.blend_datasource_field_ref import BlendDatasourceFieldRef


T = TypeVar("T", bound="BlendJoinCondition")


@_attrs_define
class BlendJoinCondition:
    """A condition comparing one field from each data source (request).

    Attributes:
        operator (BlendJoinConditionOperator): Comparison operator. Example: =.
        left (BlendDatasourceFieldRef): A field reference within a data source (request). At least one of
            `blend_data_source_id` or `blend_data_source_key` must be non-null. When creating a blend (POST), use
            `blend_data_source_key`. When updating (PUT), use `blend_data_source_id` for existing data sources or
            `blend_data_source_key` for newly added ones.
        right (BlendDatasourceFieldRef): A field reference within a data source (request). At least one of
            `blend_data_source_id` or `blend_data_source_key` must be non-null. When creating a blend (POST), use
            `blend_data_source_key`. When updating (PUT), use `blend_data_source_id` for existing data sources or
            `blend_data_source_key` for newly added ones.
    """

    operator: BlendJoinConditionOperator
    left: BlendDatasourceFieldRef
    right: BlendDatasourceFieldRef
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator: str = self.operator

        left = self.left.to_dict()

        right = self.right.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
                "left": left,
                "right": right,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_datasource_field_ref import BlendDatasourceFieldRef

        d = dict(src_dict)
        operator = check_blend_join_condition_operator(d.pop("operator"))

        left = BlendDatasourceFieldRef.from_dict(d.pop("left"))

        right = BlendDatasourceFieldRef.from_dict(d.pop("right"))

        blend_join_condition = cls(
            operator=operator,
            left=left,
            right=right,
        )

        blend_join_condition.additional_properties = d
        return blend_join_condition

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
