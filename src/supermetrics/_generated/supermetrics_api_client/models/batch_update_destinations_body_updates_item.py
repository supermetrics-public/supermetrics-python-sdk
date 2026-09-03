from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BatchUpdateDestinationsBodyUpdatesItem")


@_attrs_define
class BatchUpdateDestinationsBodyUpdatesItem:
    """
    Attributes:
        destination_id (int): ID of the destination to rotate the secret for
        new_secret (str): New secret value for credential rotation
    """

    destination_id: int
    new_secret: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_id = self.destination_id

        new_secret = self.new_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destination_id": destination_id,
                "new_secret": new_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destination_id = d.pop("destination_id")

        new_secret = d.pop("new_secret")

        batch_update_destinations_body_updates_item = cls(
            destination_id=destination_id,
            new_secret=new_secret,
        )

        batch_update_destinations_body_updates_item.additional_properties = d
        return batch_update_destinations_body_updates_item

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
