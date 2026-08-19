from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_list_item_output import BlendListItemOutput


T = TypeVar("T", bound="BlendListResponseData")


@_attrs_define
class BlendListResponseData:
    """Container holding the list of blend summaries.

    Attributes:
        items (list[BlendListItemOutput] | Unset): Blend summary items.
    """

    items: list[BlendListItemOutput] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_list_item_output import BlendListItemOutput

        d = dict(src_dict)
        _items = d.pop("items", UNSET)
        items: list[BlendListItemOutput] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:
                items_item = BlendListItemOutput.from_dict(items_item_data)

                items.append(items_item)

        blend_list_response_data = cls(
            items=items,
        )

        blend_list_response_data.additional_properties = d
        return blend_list_response_data

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
