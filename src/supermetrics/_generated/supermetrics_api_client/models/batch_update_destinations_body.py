from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.batch_update_destinations_body_updates_item import BatchUpdateDestinationsBodyUpdatesItem


T = TypeVar("T", bound="BatchUpdateDestinationsBody")


@_attrs_define
class BatchUpdateDestinationsBody:
    """
    Attributes:
        type_ (str): Destination type shared by all items in the batch Example: DWH_SNOWFLAKE.
        updates (list[BatchUpdateDestinationsBodyUpdatesItem]):
    """

    type_: str
    updates: list[BatchUpdateDestinationsBodyUpdatesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        updates = []
        for updates_item_data in self.updates:
            updates_item = updates_item_data.to_dict()
            updates.append(updates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "updates": updates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_update_destinations_body_updates_item import BatchUpdateDestinationsBodyUpdatesItem

        d = dict(src_dict)
        type_ = d.pop("type")

        updates = []
        _updates = d.pop("updates")
        for updates_item_data in _updates:
            updates_item = BatchUpdateDestinationsBodyUpdatesItem.from_dict(updates_item_data)

            updates.append(updates_item)

        batch_update_destinations_body = cls(
            type_=type_,
            updates=updates,
        )

        batch_update_destinations_body.additional_properties = d
        return batch_update_destinations_body

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
