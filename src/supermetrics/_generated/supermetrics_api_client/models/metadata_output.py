from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.meta import Meta
    from ..models.metadata_output_data import MetadataOutputData


T = TypeVar("T", bound="MetadataOutput")


@_attrs_define
class MetadataOutput:
    """Success envelope describing the metadata available for building custom fields: the functions, condition/lookup
    rules, field data types, output data types, and the team's transformation-step limit.

        Example:
            {'meta': {'request_id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'}, 'data': {'rules': {'condition': {'items':
                [{'name': 'equals', 'display_name': 'EQUALS'}]}, 'lookup': {'items': [{'name': 'equals', 'display_name':
                'EQUALS'}]}}, 'functions': {'items': [{'name': 'upper_case', 'display_name': 'Upper Case', 'description':
                'Converts text to upper case', 'group_name': 'String', 'arguments': [{'name': 'value'}], 'return_types':
                ['string.text.value']}]}, 'field_data_types': ['string.text.value'], 'output_data_types': {'items':
                [{'output_type': 'string.text.value', 'label': 'STRING'}]}, 'data_transformation_steps_limit': 10}}

        Attributes:
            meta (Meta): Metadata included in every API response.
            data (MetadataOutputData): Metadata for custom field transformations.
    """

    meta: Meta
    data: MetadataOutputData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.meta import Meta
        from ..models.metadata_output_data import MetadataOutputData

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = MetadataOutputData.from_dict(d.pop("data"))

        metadata_output = cls(
            meta=meta,
            data=data,
        )

        metadata_output.additional_properties = d
        return metadata_output

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
