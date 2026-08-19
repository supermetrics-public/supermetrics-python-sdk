from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.meta import Meta
    from ..models.team_transformation_output import TeamTransformationOutput


T = TypeVar("T", bound="SingleTransformationOutput")


@_attrs_define
class SingleTransformationOutput:
    """Success envelope wrapping a single custom field transformation.

    Example:
        {'meta': {'request_id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'}, 'data': {'id': 42, 'name':
            'spec_example_field', 'data_source_id': 'GAWA', 'display_name': 'Spec Example Field', 'description': 'Temporary
            transformation for spec examples', 'field_type': 'dim', 'data_type': 'string.text.value', 'modified_time_utc':
            '2026-04-06T10:59:04+0000', 'modified_user': {'email': 'user@supermetrics.com', 'first_name': 'John',
            'last_name': 'Doe'}, 'definition': {'items': [{'type': 'function', 'name': 'upper_case', 'arguments': [{'name':
            'value', 'value': {'type': 'data_source_field', 'value': 'platform'}}], 'description': None}]}, 'report_types':
            ['Default']}}

    Attributes:
        meta (Meta): Metadata included in every API response.
        data (TeamTransformationOutput): A persisted custom field (field transformation) as returned by read operations.
            Example: {'id': 42, 'name': 'spec_example_field', 'data_source_id': 'GAWA', 'display_name': 'Spec Example Field
            Updated', 'description': 'Updated temporary transformation for spec examples', 'field_type': 'dim', 'data_type':
            'string.text.value', 'modified_time_utc': '2026-04-06T10:59:04+0000', 'modified_user': {'email':
            'user@supermetrics.com', 'first_name': 'John', 'last_name': 'Doe'}, 'definition': {'items': [{'type':
            'function', 'name': 'upper_case', 'arguments': [{'name': 'value', 'value': {'type': 'data_source_field',
            'value': 'platform'}}], 'description': None}]}, 'report_types': ['Default']}.
    """

    meta: Meta
    data: TeamTransformationOutput
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
        from ..models.team_transformation_output import TeamTransformationOutput

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = TeamTransformationOutput.from_dict(d.pop("data"))

        single_transformation_output = cls(
            meta=meta,
            data=data,
        )

        single_transformation_output.additional_properties = d
        return single_transformation_output

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
