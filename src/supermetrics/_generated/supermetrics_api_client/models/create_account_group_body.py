from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.create_account_group_body_data_sources_item import CreateAccountGroupBodyDataSourcesItem


T = TypeVar("T", bound="CreateAccountGroupBody")


@_attrs_define
class CreateAccountGroupBody:
    """
    Attributes:
        display_name (str): Display name for the new account tag
        color (str): Color for the new account tag
        data_sources (list[CreateAccountGroupBodyDataSourcesItem]): Array of data sources and connections
    """

    display_name: str
    color: str
    data_sources: list[CreateAccountGroupBodyDataSourcesItem]

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        color = self.color

        data_sources = []
        for data_sources_item_data in self.data_sources:
            data_sources_item = data_sources_item_data.to_dict()
            data_sources.append(data_sources_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "display_name": display_name,
                "color": color,
                "data_sources": data_sources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_account_group_body_data_sources_item import CreateAccountGroupBodyDataSourcesItem

        d = dict(src_dict)
        display_name = d.pop("display_name")

        color = d.pop("color")

        data_sources = []
        _data_sources = d.pop("data_sources")
        for data_sources_item_data in _data_sources:
            data_sources_item = CreateAccountGroupBodyDataSourcesItem.from_dict(data_sources_item_data)

            data_sources.append(data_sources_item)

        create_account_group_body = cls(
            display_name=display_name,
            color=color,
            data_sources=data_sources,
        )

        return create_account_group_body
