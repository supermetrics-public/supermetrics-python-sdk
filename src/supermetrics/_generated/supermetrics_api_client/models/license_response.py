from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assign_result_data import AssignResultData
    from ..models.license_response_meta import LicenseResponseMeta


T = TypeVar("T", bound="LicenseResponse")


@_attrs_define
class LicenseResponse:
    """Response envelope containing assignment result

    Attributes:
        meta (LicenseResponseMeta | Unset): Response metadata
        data (AssignResultData | Unset): Result of a user assignment operation
    """

    meta: LicenseResponseMeta | Unset = UNSET
    data: AssignResultData | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

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
        from ..models.assign_result_data import AssignResultData
        from ..models.license_response_meta import LicenseResponseMeta

        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: LicenseResponseMeta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = LicenseResponseMeta.from_dict(_meta)

        _data = d.pop("data", UNSET)
        data: AssignResultData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = AssignResultData.from_dict(_data)

        license_response = cls(
            meta=meta,
            data=data,
        )

        license_response.additional_properties = d
        return license_response

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
