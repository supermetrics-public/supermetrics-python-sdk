from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountTagOverview")


@_attrs_define
class AccountTagOverview:
    """
    Attributes:
        name (str | Unset): The unique name of the account tag Example: a1b2c3d.
        display_name (str | Unset): Human-readable name of the account tag Example: EMEA paid media.
        color (str | Unset): Display color of the account tag Example: #112233.
        data_source_count (int | Unset): Number of data sources represented in the tag Example: 3.
        account_count (int | Unset): Number of accounts in the tag Example: 42.
    """

    name: str | Unset = UNSET
    display_name: str | Unset = UNSET
    color: str | Unset = UNSET
    data_source_count: int | Unset = UNSET
    account_count: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        display_name = self.display_name

        color = self.color

        data_source_count = self.data_source_count

        account_count = self.account_count

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if color is not UNSET:
            field_dict["color"] = color
        if data_source_count is not UNSET:
            field_dict["data_source_count"] = data_source_count
        if account_count is not UNSET:
            field_dict["account_count"] = account_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        display_name = d.pop("display_name", UNSET)

        color = d.pop("color", UNSET)

        data_source_count = d.pop("data_source_count", UNSET)

        account_count = d.pop("account_count", UNSET)

        account_tag_overview = cls(
            name=name,
            display_name=display_name,
            color=color,
            data_source_count=data_source_count,
            account_count=account_count,
        )

        return account_tag_overview
