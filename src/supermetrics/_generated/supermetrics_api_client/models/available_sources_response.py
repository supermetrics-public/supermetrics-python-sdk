from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_source_info import DataSourceInfo
    from ..models.destination_type_settings import DestinationTypeSettings
    from ..models.transfer_destination import TransferDestination


T = TypeVar("T", bound="AvailableSourcesResponse")


@_attrs_define
class AvailableSourcesResponse:
    """Available data sources and destinations for Hub transfers

    Attributes:
        data_sources (list[DataSourceInfo] | Unset): Available data sources sorted alphabetically by service name
        destinations (list[TransferDestination] | Unset): Available transfer destinations
        destination_types (list[DestinationTypeSettings] | Unset): Destination type configurations with setup settings
            and auth methods
    """

    data_sources: list[DataSourceInfo] | Unset = UNSET
    destinations: list[TransferDestination] | Unset = UNSET
    destination_types: list[DestinationTypeSettings] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_sources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_sources, Unset):
            data_sources = []
            for data_sources_item_data in self.data_sources:
                data_sources_item = data_sources_item_data.to_dict()
                data_sources.append(data_sources_item)

        destinations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = []
            for destinations_item_data in self.destinations:
                destinations_item = destinations_item_data.to_dict()
                destinations.append(destinations_item)

        destination_types: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.destination_types, Unset):
            destination_types = []
            for destination_types_item_data in self.destination_types:
                destination_types_item = destination_types_item_data.to_dict()
                destination_types.append(destination_types_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_sources is not UNSET:
            field_dict["data_sources"] = data_sources
        if destinations is not UNSET:
            field_dict["destinations"] = destinations
        if destination_types is not UNSET:
            field_dict["destination_types"] = destination_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_source_info import DataSourceInfo
        from ..models.destination_type_settings import DestinationTypeSettings
        from ..models.transfer_destination import TransferDestination

        d = dict(src_dict)
        _data_sources = d.pop("data_sources", UNSET)
        data_sources: list[DataSourceInfo] | Unset = UNSET
        if _data_sources is not UNSET:
            data_sources = []
            for data_sources_item_data in _data_sources:
                data_sources_item = DataSourceInfo.from_dict(data_sources_item_data)

                data_sources.append(data_sources_item)

        _destinations = d.pop("destinations", UNSET)
        destinations: list[TransferDestination] | Unset = UNSET
        if _destinations is not UNSET:
            destinations = []
            for destinations_item_data in _destinations:
                destinations_item = TransferDestination.from_dict(destinations_item_data)

                destinations.append(destinations_item)

        _destination_types = d.pop("destination_types", UNSET)
        destination_types: list[DestinationTypeSettings] | Unset = UNSET
        if _destination_types is not UNSET:
            destination_types = []
            for destination_types_item_data in _destination_types:
                destination_types_item = DestinationTypeSettings.from_dict(destination_types_item_data)

                destination_types.append(destination_types_item)

        available_sources_response = cls(
            data_sources=data_sources,
            destinations=destinations,
            destination_types=destination_types,
        )

        available_sources_response.additional_properties = d
        return available_sources_response

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
