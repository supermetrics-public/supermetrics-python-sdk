from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.login_revoke_response_data import LoginRevokeResponseData
    from ..models.meta import Meta


T = TypeVar("T", bound="LoginRevokeResponse")


@_attrs_define
class LoginRevokeResponse:
    """Response envelope for a data source login revoke operation

    Attributes:
        meta (Meta | Unset): Metadata included in every API response.
        data (LoginRevokeResponseData | Unset): Result payload for the revoke operation
    """

    meta: Meta | Unset = UNSET
    data: LoginRevokeResponseData | Unset = UNSET
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
        from ..models.login_revoke_response_data import LoginRevokeResponseData
        from ..models.meta import Meta

        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: Meta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = Meta.from_dict(_meta)

        _data = d.pop("data", UNSET)
        data: LoginRevokeResponseData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = LoginRevokeResponseData.from_dict(_data)

        login_revoke_response = cls(
            meta=meta,
            data=data,
        )

        login_revoke_response.additional_properties = d
        return login_revoke_response

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
