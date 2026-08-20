from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.account_tag_overview import AccountTagOverview


T = TypeVar("T", bound="AccountTagListResponseData")


@_attrs_define
class AccountTagListResponseData:
    """Wrapper object holding the team's account tags

    Example:
        {'items': [{'name': 'a1b2c3d', 'display_name': 'EMEA paid media', 'color': '#112233', 'data_source_count': 3,
            'account_count': 42}]}

    Attributes:
        items (list[AccountTagOverview]): The list of account tags
    """

    items: list[AccountTagOverview]

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_tag_overview import AccountTagOverview

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = AccountTagOverview.from_dict(items_item_data)

            items.append(items_item)

        account_tag_list_response_data = cls(
            items=items,
        )

        return account_tag_list_response_data
