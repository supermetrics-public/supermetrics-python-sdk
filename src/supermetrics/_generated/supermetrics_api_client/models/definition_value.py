from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.definition_value_type import DefinitionValueType, check_definition_value_type
from ..types import UNSET, Unset

T = TypeVar("T", bound="DefinitionValue")


@_attrs_define
class DefinitionValue:
    """A value reference used in transformation steps. Depending on `type` the value is read from a data-source field,
    taken from the previous step's output, or supplied as a static literal.

        Example:
            {'type': 'data_source_field', 'value': 'platform'}

        Attributes:
            type_ (DefinitionValueType): Where the value comes from: `data_source_field` (a named field on the data source),
                `output_from_previous` (the result of the preceding step), or `static` (a literal value). Example:
                data_source_field.
            value (str | Unset): The value itself: the field name when `type` is `data_source_field`, a literal when `type`
                is `static`, and omitted when `type` is `output_from_previous`. Example: platform.
    """

    type_: DefinitionValueType
    value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_definition_value_type(d.pop("type"))

        value = d.pop("value", UNSET)

        definition_value = cls(
            type_=type_,
            value=value,
        )

        definition_value.additional_properties = d
        return definition_value

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
