from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.function_step_type import FunctionStepType, check_function_step_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_argument import FunctionArgument


T = TypeVar("T", bound="FunctionStep")


@_attrs_define
class FunctionStep:
    """A transformation step that applies a named function to its arguments.

    Example:
        {'type': 'function', 'name': 'upper_case', 'arguments': [{'name': 'value', 'value': {'type':
            'data_source_field', 'value': 'platform'}}], 'description': None}

    Attributes:
        type_ (FunctionStepType): Discriminator value identifying this step as a function step. Example: function.
        name (str): Name of the function to apply. Example: upper_case.
        arguments (list[FunctionArgument]): Arguments passed to this function.
        description (None | str | Unset): Optional free-text description of the transformation step.
    """

    type_: FunctionStepType
    name: str
    arguments: list[FunctionArgument]
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        name = self.name

        arguments = []
        for arguments_item_data in self.arguments:
            arguments_item = arguments_item_data.to_dict()
            arguments.append(arguments_item)

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
                "name": name,
                "arguments": arguments,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_argument import FunctionArgument

        d = dict(src_dict)
        type_ = check_function_step_type(d.pop("type"))

        name = d.pop("name")

        arguments = []
        _arguments = d.pop("arguments")
        for arguments_item_data in _arguments:
            arguments_item = FunctionArgument.from_dict(arguments_item_data)

            arguments.append(arguments_item)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        function_step = cls(
            type_=type_,
            name=name,
            arguments=arguments,
            description=description,
        )

        function_step.additional_properties = d
        return function_step

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
