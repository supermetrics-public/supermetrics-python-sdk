from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.condition_step_type import ConditionStepType, check_condition_step_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.condition_case import ConditionCase
    from ..models.definition_value import DefinitionValue
    from ..models.function_step import FunctionStep


T = TypeVar("T", bound="ConditionStep")


@_attrs_define
class ConditionStep:
    """A transformation step that evaluates an ordered list of cases and returns the result of the first matching case,
    falling back to `default` when none match.

        Attributes:
            type_ (ConditionStepType): Discriminator value identifying this step as a condition step. Example: condition.
            default (DefinitionValue | FunctionStep): Value returned when no case matches. May be a plain DefinitionValue or
                a nested FunctionStep.
            cases (list[ConditionCase]): Condition cases evaluated in order; the first match wins.
            description (None | str | Unset): Optional free-text description of the transformation step.
    """

    type_: ConditionStepType
    default: DefinitionValue | FunctionStep
    cases: list[ConditionCase]
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.definition_value import DefinitionValue

        type_: str = self.type_

        default: dict[str, Any]
        if isinstance(self.default, DefinitionValue):
            default = self.default.to_dict()
        else:
            default = self.default.to_dict()

        cases = []
        for cases_item_data in self.cases:
            cases_item = cases_item_data.to_dict()
            cases.append(cases_item)

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "default": default,
                "cases": cases,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.condition_case import ConditionCase
        from ..models.definition_value import DefinitionValue
        from ..models.function_step import FunctionStep

        d = dict(src_dict)
        type_ = check_condition_step_type(d.pop("type"))

        def _parse_default(data: object) -> DefinitionValue | FunctionStep:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_type_0 = DefinitionValue.from_dict(data)

                return default_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            default_type_1 = FunctionStep.from_dict(data)

            return default_type_1

        default = _parse_default(d.pop("default"))

        cases = []
        _cases = d.pop("cases")
        for cases_item_data in _cases:
            cases_item = ConditionCase.from_dict(cases_item_data)

            cases.append(cases_item)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        condition_step = cls(
            type_=type_,
            default=default,
            cases=cases,
            description=description,
        )

        condition_step.additional_properties = d
        return condition_step

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
