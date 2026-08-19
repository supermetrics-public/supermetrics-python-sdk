from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_tag_data_sources_item import AccountTagDataSourcesItem


T = TypeVar("T", bound="AccountTag")


@_attrs_define
class AccountTag:
    """
    Example:
        {'name': 'a1b2c3d', 'display_name': 'EMEA paid media', 'color': '#112233', 'data_sources': [{'data_source_id':
            'AW', 'accounts': [{'account_id': '123-456-7890'}]}]}

    Attributes:
        name (str | Unset): The unique name of the account tag Example: a1b2c3d.
        display_name (str | Unset): Human-readable name of the account tag Example: EMEA paid media.
        color (str | Unset): Display color of the account tag Example: #112233.
        data_sources (list[AccountTagDataSourcesItem] | Unset): Data sources and their accounts belonging to the tag
            Example: [{'data_source_id': 'AW', 'accounts': [{'account_id': '123-456-7890'}]}].
    """

    name: str | Unset = UNSET
    display_name: str | Unset = UNSET
    color: str | Unset = UNSET
    data_sources: list[AccountTagDataSourcesItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        display_name = self.display_name

        color = self.color

        data_sources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_sources, Unset):
            data_sources = []
            for data_sources_item_data in self.data_sources:
                data_sources_item = data_sources_item_data.to_dict()
                data_sources.append(data_sources_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if color is not UNSET:
            field_dict["color"] = color
        if data_sources is not UNSET:
            field_dict["data_sources"] = data_sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_tag_data_sources_item import AccountTagDataSourcesItem

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        display_name = d.pop("display_name", UNSET)

        color = d.pop("color", UNSET)

        _data_sources = d.pop("data_sources", UNSET)
        data_sources: list[AccountTagDataSourcesItem] | Unset = UNSET
        if _data_sources is not UNSET:
            data_sources = []
            for data_sources_item_data in _data_sources:
                data_sources_item = AccountTagDataSourcesItem.from_dict(data_sources_item_data)

                data_sources.append(data_sources_item)

        account_tag = cls(
            name=name,
            display_name=display_name,
            color=color,
            data_sources=data_sources,
        )

        return account_tag
