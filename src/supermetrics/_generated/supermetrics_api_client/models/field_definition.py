from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldDefinition")


@_attrs_define
class FieldDefinition:
    """
    Attributes:
        field_id (str): Field ID that appears in one of the table objects
        field_name (str | Unset): Data source field name
        display_name (str | Unset): Field display name
        target_name (str | Unset): Field name in target table. Defaults to field ID in lower snake case.
        data_type (str | Unset): Field data type
    """

    field_id: str
    field_name: str | Unset = UNSET
    display_name: str | Unset = UNSET
    target_name: str | Unset = UNSET
    data_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        field_name = self.field_name

        display_name = self.display_name

        target_name = self.target_name

        data_type = self.data_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field_id": field_id,
            }
        )
        if field_name is not UNSET:
            field_dict["field_name"] = field_name
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if target_name is not UNSET:
            field_dict["target_name"] = target_name
        if data_type is not UNSET:
            field_dict["data_type"] = data_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field_id = d.pop("field_id")

        field_name = d.pop("field_name", UNSET)

        display_name = d.pop("display_name", UNSET)

        target_name = d.pop("target_name", UNSET)

        data_type = d.pop("data_type", UNSET)

        field_definition = cls(
            field_id=field_id,
            field_name=field_name,
            display_name=display_name,
            target_name=target_name,
            data_type=data_type,
        )

        field_definition.additional_properties = d
        return field_definition

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
