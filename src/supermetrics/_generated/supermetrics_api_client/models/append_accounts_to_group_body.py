from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.append_accounts_to_group_body_data_sources_item import AppendAccountsToGroupBodyDataSourcesItem


T = TypeVar("T", bound="AppendAccountsToGroupBody")


@_attrs_define
class AppendAccountsToGroupBody:
    """
    Attributes:
        data_sources (list[AppendAccountsToGroupBodyDataSourcesItem]): Array of data sources and connections
    """

    data_sources: list[AppendAccountsToGroupBodyDataSourcesItem]

    def to_dict(self) -> dict[str, Any]:
        data_sources = []
        for data_sources_item_data in self.data_sources:
            data_sources_item = data_sources_item_data.to_dict()
            data_sources.append(data_sources_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data_sources": data_sources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.append_accounts_to_group_body_data_sources_item import AppendAccountsToGroupBodyDataSourcesItem

        d = dict(src_dict)
        data_sources = []
        _data_sources = d.pop("data_sources")
        for data_sources_item_data in _data_sources:
            data_sources_item = AppendAccountsToGroupBodyDataSourcesItem.from_dict(data_sources_item_data)

            data_sources.append(data_sources_item)

        append_accounts_to_group_body = cls(
            data_sources=data_sources,
        )

        return append_accounts_to_group_body
