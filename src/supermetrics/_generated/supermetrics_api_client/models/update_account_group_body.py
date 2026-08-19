from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateAccountGroupBody")


@_attrs_define
class UpdateAccountGroupBody:
    """
    Attributes:
        display_name (str): Display name for the account tag
        color (str): Color for the account tag
    """

    display_name: str
    color: str

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        color = self.color

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "display_name": display_name,
                "color": color,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("display_name")

        color = d.pop("color")

        update_account_group_body = cls(
            display_name=display_name,
            color=color,
        )

        return update_account_group_body
