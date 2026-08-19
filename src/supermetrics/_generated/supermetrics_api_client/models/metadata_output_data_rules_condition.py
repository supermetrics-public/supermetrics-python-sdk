from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rule_output import RuleOutput


T = TypeVar("T", bound="MetadataOutputDataRulesCondition")


@_attrs_define
class MetadataOutputDataRulesCondition:
    """Rules available for condition steps.

    Attributes:
        items (list[RuleOutput] | Unset): Available condition rules.
    """

    items: list[RuleOutput] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rule_output import RuleOutput

        d = dict(src_dict)
        _items = d.pop("items", UNSET)
        items: list[RuleOutput] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:
                items_item = RuleOutput.from_dict(items_item_data)

                items.append(items_item)

        metadata_output_data_rules_condition = cls(
            items=items,
        )

        metadata_output_data_rules_condition.additional_properties = d
        return metadata_output_data_rules_condition

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
