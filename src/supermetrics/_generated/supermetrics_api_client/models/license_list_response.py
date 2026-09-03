from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.license_data import LicenseData
    from ..models.license_list_response_meta import LicenseListResponseMeta


T = TypeVar("T", bound="LicenseListResponse")


@_attrs_define
class LicenseListResponse:
    """Response envelope containing a list of licenses

    Attributes:
        meta (LicenseListResponseMeta | Unset): Response metadata
        data (list[LicenseData] | Unset): List of licenses
    """

    meta: LicenseListResponseMeta | Unset = UNSET
    data: list[LicenseData] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if meta is not UNSET:
            field_dict["meta"] = meta
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.license_data import LicenseData
        from ..models.license_list_response_meta import LicenseListResponseMeta

        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: LicenseListResponseMeta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = LicenseListResponseMeta.from_dict(_meta)

        _data = d.pop("data", UNSET)
        data: list[LicenseData] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = LicenseData.from_dict(data_item_data)

                data.append(data_item)

        license_list_response = cls(
            meta=meta,
            data=data,
        )

        license_list_response.additional_properties = d
        return license_list_response

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
