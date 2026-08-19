from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.definition_value import DefinitionValue


T = TypeVar("T", bound="FunctionArgument")


@_attrs_define
class FunctionArgument:
    """A named argument supplied to a function step.

    Example:
        {'name': 'value', 'value': {'type': 'data_source_field', 'value': 'platform'}}

    Attributes:
        name (str): Argument name as expected by the function. Example: value.
        value (DefinitionValue): A value reference used in transformation steps. Depending on `type` the value is read
            from a data-source field, taken from the previous step's output, or supplied as a static literal. Example:
            {'type': 'data_source_field', 'value': 'platform'}.
    """

    name: str
    value: DefinitionValue
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.definition_value import DefinitionValue

        d = dict(src_dict)
        name = d.pop("name")

        value = DefinitionValue.from_dict(d.pop("value"))

        function_argument = cls(
            name=name,
            value=value,
        )

        function_argument.additional_properties = d
        return function_argument

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
