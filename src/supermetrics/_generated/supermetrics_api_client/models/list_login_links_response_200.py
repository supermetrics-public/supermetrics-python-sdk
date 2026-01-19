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





T = TypeVar("T", bound="ListLoginLinksResponse200")



@_attrs_define
class ListLoginLinksResponse200:
    """ 
        Attributes:
            meta (ResponseMeta | Unset):
            data (list[LoginLink] | Unset):
     """

    meta: ResponseMeta | Unset = UNSET
    data: list[LoginLink] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.login_link import LoginLink
        from ..models.response_meta import ResponseMeta
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
        data: list[LoginLink] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = LoginLink.from_dict(data_item_data)



                data.append(data_item)


        list_login_links_response_200 = cls(
            meta=meta,
            data=data,
        )


        list_login_links_response_200.additional_properties = d
        return list_login_links_response_200

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
