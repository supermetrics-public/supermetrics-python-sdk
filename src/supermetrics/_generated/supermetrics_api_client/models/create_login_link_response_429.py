from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.error import Error
  from ..models.response_meta import ResponseMeta





T = TypeVar("T", bound="CreateLoginLinkResponse429")



@_attrs_define
class CreateLoginLinkResponse429:
    """ 
        Attributes:
            meta (ResponseMeta | Unset):
            error (Error | Unset):
     """

    meta: ResponseMeta | Unset = UNSET
    error: Error | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.error import Error
        from ..models.response_meta import ResponseMeta
        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if meta is not UNSET:
            field_dict["meta"] = meta
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error import Error
        from ..models.response_meta import ResponseMeta
        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: ResponseMeta | Unset
        if isinstance(_meta,  Unset):
            meta = UNSET
        else:
            meta = ResponseMeta.from_dict(_meta)




        _error = d.pop("error", UNSET)
        error: Error | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = Error.from_dict(_error)




        create_login_link_response_429 = cls(
            meta=meta,
            error=error,
        )


        create_login_link_response_429.additional_properties = d
        return create_login_link_response_429

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
