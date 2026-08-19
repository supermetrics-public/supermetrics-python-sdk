from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DestinationListItem")


@_attrs_define
class DestinationListItem:
    """
    Attributes:
        id (int): Unique identifier for the destination Example: 123.
        display_name (str): Human-readable name for the destination Example: My Snowflake Destination.
        type_ (str): Destination type identifier Example: DWH_SNOWFLAKE.
    """

    id: int
    display_name: str
    type_: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        display_name = self.display_name

        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "display_name": display_name,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        display_name = d.pop("display_name")

        type_ = d.pop("type")

        destination_list_item = cls(
            id=id,
            display_name=display_name,
            type_=type_,
        )

        return destination_list_item
