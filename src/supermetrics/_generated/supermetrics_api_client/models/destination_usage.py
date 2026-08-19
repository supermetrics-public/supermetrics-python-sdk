from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.destination_usage_transfers_item import DestinationUsageTransfersItem


T = TypeVar("T", bound="DestinationUsage")


@_attrs_define
class DestinationUsage:
    """
    Attributes:
        is_used (bool): Whether the destination is currently being used by any transfers Example: True.
        transfers (list[DestinationUsageTransfersItem]): List of transfers using this destination
    """

    is_used: bool
    transfers: list[DestinationUsageTransfersItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_used = self.is_used

        transfers = []
        for transfers_item_data in self.transfers:
            transfers_item = transfers_item_data.to_dict()
            transfers.append(transfers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_used": is_used,
                "transfers": transfers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_usage_transfers_item import DestinationUsageTransfersItem

        d = dict(src_dict)
        is_used = d.pop("is_used")

        transfers = []
        _transfers = d.pop("transfers")
        for transfers_item_data in _transfers:
            transfers_item = DestinationUsageTransfersItem.from_dict(transfers_item_data)

            transfers.append(transfers_item)

        destination_usage = cls(
            is_used=is_used,
            transfers=transfers,
        )

        destination_usage.additional_properties = d
        return destination_usage

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
