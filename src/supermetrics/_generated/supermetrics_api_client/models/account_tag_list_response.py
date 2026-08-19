from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_tag_overview import AccountTagOverview


T = TypeVar("T", bound="AccountTagListResponse")


@_attrs_define
class AccountTagListResponse:
    """
    Attributes:
        data (list[AccountTagOverview] | Unset): The list of account tags Example: [{'name': 'a1b2c3d', 'display_name':
            'EMEA paid media', 'color': '#112233', 'data_source_count': 3, 'account_count': 42}].
    """

    data: list[AccountTagOverview] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_tag_overview import AccountTagOverview

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[AccountTagOverview] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = AccountTagOverview.from_dict(data_item_data)

                data.append(data_item)

        account_tag_list_response = cls(
            data=data,
        )

        return account_tag_list_response
