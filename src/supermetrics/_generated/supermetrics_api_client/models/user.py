from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.user_type import UserType
from ..types import UNSET, Unset






T = TypeVar("T", bound="User")



@_attrs_define
class User:
    """ 
        Attributes:
            type_ (UserType | Unset):
            user_id (str | Unset): Supermetrics user ID
            email (str | Unset): Supermetrics user email
     """

    type_: UserType | Unset = UNSET
    user_id: str | Unset = UNSET
    email: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        user_id = self.user_id

        email = self.email


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: UserType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = UserType(_type_)




        user_id = d.pop("user_id", UNSET)

        email = d.pop("email", UNSET)

        user = cls(
            type_=type_,
            user_id=user_id,
            email=email,
        )


        user.additional_properties = d
        return user

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
