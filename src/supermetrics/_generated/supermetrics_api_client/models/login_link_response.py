from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.login_link import LoginLink
  from ..models.response_meta import ResponseMeta





T = TypeVar("T", bound="LoginLinkResponse")



@_attrs_define
class LoginLinkResponse:
    """ 
        Attributes:
            meta (ResponseMeta | Unset):
            data (LoginLink | Unset):
     """

    meta: ResponseMeta | Unset = UNSET
    data: LoginLink | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.login_link import LoginLink
        from ..models.response_meta import ResponseMeta
        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if meta is not UNSET:
            field_dict["meta"] = meta
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.login_link import LoginLink
        from ..models.response_meta import ResponseMeta
        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: ResponseMeta | Unset
        if isinstance(_meta,  Unset):
            meta = UNSET
        else:
            meta = ResponseMeta.from_dict(_meta)




        _data = d.pop("data", UNSET)
        data: LoginLink | Unset
        if isinstance(_data,  Unset):
            data = UNSET
        else:
            data = LoginLink.from_dict(_data)




        login_link_response = cls(
            meta=meta,
            data=data,
        )


        login_link_response.additional_properties = d
        return login_link_response

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
