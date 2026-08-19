from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthMethod")


@_attrs_define
class AuthMethod:
    """
    Attributes:
        id (str): Authentication method identifier Example: AUTH_METHOD_KEY_PAIR.
        label (str): Display label for the authentication method Example: Key Pair Authentication.
        is_default (bool | Unset): Whether this is the default authentication method Default: False.
    """

    id: str
    label: str
    is_default: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        label = self.label

        is_default = self.is_default

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "label": label,
            }
        )
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        label = d.pop("label")

        is_default = d.pop("is_default", UNSET)

        auth_method = cls(
            id=id,
            label=label,
            is_default=is_default,
        )

        return auth_method
