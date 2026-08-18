from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_destination_details_item import TransferDestinationDetailsItem


T = TypeVar("T", bound="TransferDestination")


@_attrs_define
class TransferDestination:
    """Transfer destination instance

    Attributes:
        destination_id (int | None | Unset): The destination ID Example: 8.
        destination_name (str | Unset): Display name of the destination Example: My BigQuery.
        destination_type (str | Unset): Destination type identifier Example: SQL_BQ.
        destination_label (str | Unset): Human-readable destination type label Example: BigQuery.
        destination_icon_url (str | Unset): URL to destination icon
        is_internal (bool | Unset): Whether this destination is for internal use only
        details (list[TransferDestinationDetailsItem] | Unset): Destination-specific detail fields
    """

    destination_id: int | None | Unset = UNSET
    destination_name: str | Unset = UNSET
    destination_type: str | Unset = UNSET
    destination_label: str | Unset = UNSET
    destination_icon_url: str | Unset = UNSET
    is_internal: bool | Unset = UNSET
    details: list[TransferDestinationDetailsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_id: int | None | Unset
        if isinstance(self.destination_id, Unset):
            destination_id = UNSET
        else:
            destination_id = self.destination_id

        destination_name = self.destination_name

        destination_type = self.destination_type

        destination_label = self.destination_label

        destination_icon_url = self.destination_icon_url

        is_internal = self.is_internal

        details: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = []
            for details_item_data in self.details:
                details_item = details_item_data.to_dict()
                details.append(details_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if destination_id is not UNSET:
            field_dict["destination_id"] = destination_id
        if destination_name is not UNSET:
            field_dict["destination_name"] = destination_name
        if destination_type is not UNSET:
            field_dict["destination_type"] = destination_type
        if destination_label is not UNSET:
            field_dict["destination_label"] = destination_label
        if destination_icon_url is not UNSET:
            field_dict["destination_icon_url"] = destination_icon_url
        if is_internal is not UNSET:
            field_dict["is_internal"] = is_internal
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_destination_details_item import TransferDestinationDetailsItem

        d = dict(src_dict)

        def _parse_destination_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        destination_id = _parse_destination_id(d.pop("destination_id", UNSET))

        destination_name = d.pop("destination_name", UNSET)

        destination_type = d.pop("destination_type", UNSET)

        destination_label = d.pop("destination_label", UNSET)

        destination_icon_url = d.pop("destination_icon_url", UNSET)

        is_internal = d.pop("is_internal", UNSET)

        _details = d.pop("details", UNSET)
        details: list[TransferDestinationDetailsItem] | Unset = UNSET
        if _details is not UNSET:
            details = []
            for details_item_data in _details:
                details_item = TransferDestinationDetailsItem.from_dict(details_item_data)

                details.append(details_item)

        transfer_destination = cls(
            destination_id=destination_id,
            destination_name=destination_name,
            destination_type=destination_type,
            destination_label=destination_label,
            destination_icon_url=destination_icon_url,
            is_internal=is_internal,
            details=details,
        )

        transfer_destination.additional_properties = d
        return transfer_destination

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
