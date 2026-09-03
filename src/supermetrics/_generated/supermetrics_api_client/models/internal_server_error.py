from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.internal_server_error_code import InternalServerErrorCode, check_internal_server_error_code
from ..types import UNSET, Unset

T = TypeVar("T", bound="InternalServerError")


@_attrs_define
class InternalServerError:
    """
    Attributes:
        message (str | Unset): Internal server error
        code (InternalServerErrorCode | Unset): INTERNAL_SERVER_ERROR
    """

    message: str | Unset = UNSET
    code: InternalServerErrorCode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        code: str | Unset = UNSET
        if not isinstance(self.code, Unset):
            code = self.code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message", UNSET)

        _code = d.pop("code", UNSET)
        code: InternalServerErrorCode | Unset
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = check_internal_server_error_code(_code)

        internal_server_error = cls(
            message=message,
            code=code,
        )

        internal_server_error.additional_properties = d
        return internal_server_error

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
