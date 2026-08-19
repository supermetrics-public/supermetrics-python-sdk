from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.blend_output import BlendOutput
    from ..models.meta import Meta


T = TypeVar("T", bound="BlendResponse")


@_attrs_define
class BlendResponse:
    """Success envelope wrapping a single blend.

    Attributes:
        meta (Meta): Metadata included in every API response.
        data (BlendOutput): A blend with its fields and data sources, as returned for a single-blend read. Example:
            {'blend_id': 569, 'blend_uuid': '71bc0582-31b5-11f1-a55c-4201ac182030', 'type': 'union', 'display_name': 'My
            Blend', 'description': 'Description of the blend', 'modified_time_utc': '2026-04-07T10:00:00+0000',
            'last_modify_user_email': 'user@supermetrics.com'}.
    """

    meta: Meta
    data: BlendOutput
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
        from ..models.blend_output import BlendOutput
        from ..models.meta import Meta

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = BlendOutput.from_dict(d.pop("data"))

        blend_response = cls(
            meta=meta,
            data=data,
        )

        blend_response.additional_properties = d
        return blend_response

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
