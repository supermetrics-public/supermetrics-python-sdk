from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_tag import AccountTag


T = TypeVar("T", bound="AccountTagResponse")


@_attrs_define
class AccountTagResponse:
    """
    Attributes:
        data (AccountTag | Unset):  Example: {'name': 'a1b2c3d', 'display_name': 'EMEA paid media', 'color': '#112233',
            'data_sources': [{'data_source_id': 'AW', 'accounts': [{'account_id': '123-456-7890'}]}]}.
    """

    data: AccountTag | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_tag import AccountTag

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: AccountTag | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = AccountTag.from_dict(_data)

        account_tag_response = cls(
            data=data,
        )

        return account_tag_response
