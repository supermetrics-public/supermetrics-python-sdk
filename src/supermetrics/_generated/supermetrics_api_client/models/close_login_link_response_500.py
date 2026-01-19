from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.close_login_link_response_500_error import CloseLoginLinkResponse500Error
from ..types import UNSET, Unset






T = TypeVar("T", bound="CloseLoginLinkResponse500")



@_attrs_define
class CloseLoginLinkResponse500:
    """ 
        Attributes:
            error (CloseLoginLinkResponse500Error | Unset):
            message (str | Unset):
     """

    error: CloseLoginLinkResponse500Error | Unset = UNSET
    message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        error: str | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.value


        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if error is not UNSET:
            field_dict["error"] = error
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _error = d.pop("error", UNSET)
        error: CloseLoginLinkResponse500Error | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = CloseLoginLinkResponse500Error(_error)




        message = d.pop("message", UNSET)

        close_login_link_response_500 = cls(
            error=error,
            message=message,
        )


        close_login_link_response_500.additional_properties = d
        return close_login_link_response_500

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
