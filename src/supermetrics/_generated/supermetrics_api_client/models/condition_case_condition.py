from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.condition_case_condition_type import ConditionCaseConditionType, check_condition_case_condition_type

if TYPE_CHECKING:
    from ..models.definition_value import DefinitionValue


T = TypeVar("T", bound="ConditionCaseCondition")


@_attrs_define
class ConditionCaseCondition:
    """The rule-based condition evaluated for this case.

    Attributes:
        type_ (ConditionCaseConditionType): Discriminator value identifying the condition kind (always `rule`). Example:
            rule.
        rule (str): The comparison operator applied between `source` and `target`. Example: equals.
        source (DefinitionValue): A value reference used in transformation steps. Depending on `type` the value is read
            from a data-source field, taken from the previous step's output, or supplied as a static literal. Example:
            {'type': 'data_source_field', 'value': 'platform'}.
        target (DefinitionValue): A value reference used in transformation steps. Depending on `type` the value is read
            from a data-source field, taken from the previous step's output, or supplied as a static literal. Example:
            {'type': 'data_source_field', 'value': 'platform'}.
    """

    type_: ConditionCaseConditionType
    rule: str
    source: DefinitionValue
    target: DefinitionValue
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        rule = self.rule

        source = self.source.to_dict()

        target = self.target.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "rule": rule,
                "source": source,
                "target": target,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.definition_value import DefinitionValue

        d = dict(src_dict)
        type_ = check_condition_case_condition_type(d.pop("type"))

        rule = d.pop("rule")

        source = DefinitionValue.from_dict(d.pop("source"))

        target = DefinitionValue.from_dict(d.pop("target"))

        condition_case_condition = cls(
            type_=type_,
            rule=rule,
            source=source,
            target=target,
        )

        condition_case_condition.additional_properties = d
        return condition_case_condition

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
