from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.condition_case_condition import ConditionCaseCondition
    from ..models.definition_value import DefinitionValue


T = TypeVar("T", bound="ConditionCase")


@_attrs_define
class ConditionCase:
    """A single case within a condition step: when `condition` evaluates true, the `return` value is produced.

    Example:
        {'return': {'type': 'output_from_previous'}, 'condition': {'type': 'rule', 'rule': 'equals', 'source': {'type':
            'output_from_previous'}, 'target': {'type': 'static', 'value': '1'}}}

    Attributes:
        return_ (DefinitionValue): A value reference used in transformation steps. Depending on `type` the value is read
            from a data-source field, taken from the previous step's output, or supplied as a static literal. Example:
            {'type': 'data_source_field', 'value': 'platform'}.
        condition (ConditionCaseCondition): The rule-based condition evaluated for this case.
    """

    return_: DefinitionValue
    condition: ConditionCaseCondition
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return_ = self.return_.to_dict()

        condition = self.condition.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "return": return_,
                "condition": condition,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.condition_case_condition import ConditionCaseCondition
        from ..models.definition_value import DefinitionValue

        d = dict(src_dict)
        return_ = DefinitionValue.from_dict(d.pop("return"))

        condition = ConditionCaseCondition.from_dict(d.pop("condition"))

        condition_case = cls(
            return_=return_,
            condition=condition,
        )

        condition_case.additional_properties = d
        return condition_case

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
