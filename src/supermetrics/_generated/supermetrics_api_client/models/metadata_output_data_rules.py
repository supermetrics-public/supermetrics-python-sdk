from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_output_data_rules_condition import MetadataOutputDataRulesCondition
    from ..models.metadata_output_data_rules_lookup import MetadataOutputDataRulesLookup


T = TypeVar("T", bound="MetadataOutputDataRules")


@_attrs_define
class MetadataOutputDataRules:
    """Matching rules available for condition and lookup steps.

    Attributes:
        condition (MetadataOutputDataRulesCondition | Unset): Rules available for condition steps.
        lookup (MetadataOutputDataRulesLookup | Unset): Rules available for lookup steps.
    """

    condition: MetadataOutputDataRulesCondition | Unset = UNSET
    lookup: MetadataOutputDataRulesLookup | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        condition: dict[str, Any] | Unset = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        lookup: dict[str, Any] | Unset = UNSET
        if not isinstance(self.lookup, Unset):
            lookup = self.lookup.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if condition is not UNSET:
            field_dict["condition"] = condition
        if lookup is not UNSET:
            field_dict["lookup"] = lookup

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_output_data_rules_condition import MetadataOutputDataRulesCondition
        from ..models.metadata_output_data_rules_lookup import MetadataOutputDataRulesLookup

        d = dict(src_dict)
        _condition = d.pop("condition", UNSET)
        condition: MetadataOutputDataRulesCondition | Unset
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = MetadataOutputDataRulesCondition.from_dict(_condition)

        _lookup = d.pop("lookup", UNSET)
        lookup: MetadataOutputDataRulesLookup | Unset
        if isinstance(_lookup, Unset):
            lookup = UNSET
        else:
            lookup = MetadataOutputDataRulesLookup.from_dict(_lookup)

        metadata_output_data_rules = cls(
            condition=condition,
            lookup=lookup,
        )

        metadata_output_data_rules.additional_properties = d
        return metadata_output_data_rules

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
