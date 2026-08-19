from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_specification_output_arguments_item import FunctionSpecificationOutputArgumentsItem


T = TypeVar("T", bound="FunctionSpecificationOutput")


@_attrs_define
class FunctionSpecificationOutput:
    """Specification of a function available for building function steps.

    Example:
        {'name': 'upper_case', 'display_name': 'Upper Case', 'description': 'Converts text to upper case', 'group_name':
            'String', 'arguments': [{'name': 'value'}], 'return_types': ['string.text.value']}

    Attributes:
        name (str | Unset): Internal name of the function. Example: upper_case.
        display_name (str | Unset): Human-readable name of the function. Example: Upper Case.
        description (str | Unset): Detailed description of what the function does. Example: Converts text to upper case.
        group_name (str | Unset): Group the function belongs to. Example: String.
        arguments (list[FunctionSpecificationOutputArgumentsItem] | Unset): Input arguments expected by the function.
            Example: [{'name': 'value'}].
        return_types (list[str] | Unset): Data types the function can return. Example: ['string.text.value'].
    """

    name: str | Unset = UNSET
    display_name: str | Unset = UNSET
    description: str | Unset = UNSET
    group_name: str | Unset = UNSET
    arguments: list[FunctionSpecificationOutputArgumentsItem] | Unset = UNSET
    return_types: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        display_name = self.display_name

        description = self.description

        group_name = self.group_name

        arguments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = []
            for arguments_item_data in self.arguments:
                arguments_item = arguments_item_data.to_dict()
                arguments.append(arguments_item)

        return_types: list[str] | Unset = UNSET
        if not isinstance(self.return_types, Unset):
            return_types = self.return_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if arguments is not UNSET:
            field_dict["arguments"] = arguments
        if return_types is not UNSET:
            field_dict["return_types"] = return_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_specification_output_arguments_item import FunctionSpecificationOutputArgumentsItem

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        display_name = d.pop("display_name", UNSET)

        description = d.pop("description", UNSET)

        group_name = d.pop("group_name", UNSET)

        _arguments = d.pop("arguments", UNSET)
        arguments: list[FunctionSpecificationOutputArgumentsItem] | Unset = UNSET
        if _arguments is not UNSET:
            arguments = []
            for arguments_item_data in _arguments:
                arguments_item = FunctionSpecificationOutputArgumentsItem.from_dict(arguments_item_data)

                arguments.append(arguments_item)

        return_types = cast(list[str], d.pop("return_types", UNSET))

        function_specification_output = cls(
            name=name,
            display_name=display_name,
            description=description,
            group_name=group_name,
            arguments=arguments,
            return_types=return_types,
        )

        function_specification_output.additional_properties = d
        return function_specification_output

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
