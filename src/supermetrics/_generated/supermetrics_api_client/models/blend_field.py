from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_datasource_field_ref import BlendDatasourceFieldRef


T = TypeVar("T", bound="BlendField")


@_attrs_define
class BlendField:
    """A blend field and its mapping to fields in each data source (request).

    Attributes:
        blend_field_name (str): Unique name of the blend field — cannot be changed once created. Example: impressions.
        blend_datasource_fields (list[BlendDatasourceFieldRef]): Per-data-source field mappings for this blend field.
        blend_field_display_name (str | Unset): Display name of the blend field. Example: Impressions.
    """

    blend_field_name: str
    blend_datasource_fields: list[BlendDatasourceFieldRef]
    blend_field_display_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_field_name = self.blend_field_name

        blend_datasource_fields = []
        for blend_datasource_fields_item_data in self.blend_datasource_fields:
            blend_datasource_fields_item = blend_datasource_fields_item_data.to_dict()
            blend_datasource_fields.append(blend_datasource_fields_item)

        blend_field_display_name = self.blend_field_display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blend_field_name": blend_field_name,
                "blend_datasource_fields": blend_datasource_fields,
            }
        )
        if blend_field_display_name is not UNSET:
            field_dict["blend_field_display_name"] = blend_field_display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_datasource_field_ref import BlendDatasourceFieldRef

        d = dict(src_dict)
        blend_field_name = d.pop("blend_field_name")

        blend_datasource_fields = []
        _blend_datasource_fields = d.pop("blend_datasource_fields")
        for blend_datasource_fields_item_data in _blend_datasource_fields:
            blend_datasource_fields_item = BlendDatasourceFieldRef.from_dict(blend_datasource_fields_item_data)

            blend_datasource_fields.append(blend_datasource_fields_item)

        blend_field_display_name = d.pop("blend_field_display_name", UNSET)

        blend_field = cls(
            blend_field_name=blend_field_name,
            blend_datasource_fields=blend_datasource_fields,
            blend_field_display_name=blend_field_display_name,
        )

        blend_field.additional_properties = d
        return blend_field

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
