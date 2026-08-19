from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_field_output_blend_field_type import (
    BlendFieldOutputBlendFieldType,
    check_blend_field_output_blend_field_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_field_output_blend_datasource_fields import BlendFieldOutputBlendDatasourceFields


T = TypeVar("T", bound="BlendFieldOutput")


@_attrs_define
class BlendFieldOutput:
    """A blend field and its mapping to fields in each data source (response).

    Attributes:
        blend_field_name (str | Unset): Unique name of the blend field — cannot be changed once created. Example:
            impressions.
        blend_field_display_name (str | Unset): Display name of the blend field. Example: Impressions.
        blend_field_type (BlendFieldOutputBlendFieldType | Unset): Field type: `dim` (dimension) or `met` (metric).
            Example: met.
        blend_field_data_type (str | Unset): Data type of the field (e.g. string.time.date, int.number.value). Example:
            int.number.value.
        blend_datasource_fields (BlendFieldOutputBlendDatasourceFields | Unset): Per-data-source field mappings for this
            blend field.
    """

    blend_field_name: str | Unset = UNSET
    blend_field_display_name: str | Unset = UNSET
    blend_field_type: BlendFieldOutputBlendFieldType | Unset = UNSET
    blend_field_data_type: str | Unset = UNSET
    blend_datasource_fields: BlendFieldOutputBlendDatasourceFields | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_field_name = self.blend_field_name

        blend_field_display_name = self.blend_field_display_name

        blend_field_type: str | Unset = UNSET
        if not isinstance(self.blend_field_type, Unset):
            blend_field_type = self.blend_field_type

        blend_field_data_type = self.blend_field_data_type

        blend_datasource_fields: dict[str, Any] | Unset = UNSET
        if not isinstance(self.blend_datasource_fields, Unset):
            blend_datasource_fields = self.blend_datasource_fields.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blend_field_name is not UNSET:
            field_dict["blend_field_name"] = blend_field_name
        if blend_field_display_name is not UNSET:
            field_dict["blend_field_display_name"] = blend_field_display_name
        if blend_field_type is not UNSET:
            field_dict["blend_field_type"] = blend_field_type
        if blend_field_data_type is not UNSET:
            field_dict["blend_field_data_type"] = blend_field_data_type
        if blend_datasource_fields is not UNSET:
            field_dict["blend_datasource_fields"] = blend_datasource_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_field_output_blend_datasource_fields import BlendFieldOutputBlendDatasourceFields

        d = dict(src_dict)
        blend_field_name = d.pop("blend_field_name", UNSET)

        blend_field_display_name = d.pop("blend_field_display_name", UNSET)

        _blend_field_type = d.pop("blend_field_type", UNSET)
        blend_field_type: BlendFieldOutputBlendFieldType | Unset
        if isinstance(_blend_field_type, Unset):
            blend_field_type = UNSET
        else:
            blend_field_type = check_blend_field_output_blend_field_type(_blend_field_type)

        blend_field_data_type = d.pop("blend_field_data_type", UNSET)

        _blend_datasource_fields = d.pop("blend_datasource_fields", UNSET)
        blend_datasource_fields: BlendFieldOutputBlendDatasourceFields | Unset
        if isinstance(_blend_datasource_fields, Unset):
            blend_datasource_fields = UNSET
        else:
            blend_datasource_fields = BlendFieldOutputBlendDatasourceFields.from_dict(_blend_datasource_fields)

        blend_field_output = cls(
            blend_field_name=blend_field_name,
            blend_field_display_name=blend_field_display_name,
            blend_field_type=blend_field_type,
            blend_field_data_type=blend_field_data_type,
            blend_datasource_fields=blend_datasource_fields,
        )

        blend_field_output.additional_properties = d
        return blend_field_output

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
