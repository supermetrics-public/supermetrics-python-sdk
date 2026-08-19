from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DataSourceInfo")


@_attrs_define
class DataSourceInfo:
    """Data source information

    Attributes:
        data_source_id (str | Unset): Unique data source identifier Example: AW.
        service_name (None | str | Unset): Human-readable service name Example: Google Ads.
        service_provider (None | str | Unset): Service provider name Example: Google.
        logo_url (None | str | Unset): URL to the data source logo
        has_custom_fields (bool | Unset): Whether the data source supports custom account fields
        is_custom_connector (bool | Unset): Whether this is a custom connector
        is_public_beta (bool | Unset): Whether the data source is in public beta
        is_released (bool | Unset): Whether the data source is fully released
        is_internal (bool | None | Unset): Whether the data source is for internal use only
        applicable_destinations (list[str] | Unset): Product codes this data source supports
    """

    data_source_id: str | Unset = UNSET
    service_name: None | str | Unset = UNSET
    service_provider: None | str | Unset = UNSET
    logo_url: None | str | Unset = UNSET
    has_custom_fields: bool | Unset = UNSET
    is_custom_connector: bool | Unset = UNSET
    is_public_beta: bool | Unset = UNSET
    is_released: bool | Unset = UNSET
    is_internal: bool | None | Unset = UNSET
    applicable_destinations: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_id = self.data_source_id

        service_name: None | str | Unset
        if isinstance(self.service_name, Unset):
            service_name = UNSET
        else:
            service_name = self.service_name

        service_provider: None | str | Unset
        if isinstance(self.service_provider, Unset):
            service_provider = UNSET
        else:
            service_provider = self.service_provider

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        has_custom_fields = self.has_custom_fields

        is_custom_connector = self.is_custom_connector

        is_public_beta = self.is_public_beta

        is_released = self.is_released

        is_internal: bool | None | Unset
        if isinstance(self.is_internal, Unset):
            is_internal = UNSET
        else:
            is_internal = self.is_internal

        applicable_destinations: list[str] | Unset = UNSET
        if not isinstance(self.applicable_destinations, Unset):
            applicable_destinations = self.applicable_destinations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_source_id is not UNSET:
            field_dict["data_source_id"] = data_source_id
        if service_name is not UNSET:
            field_dict["service_name"] = service_name
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if has_custom_fields is not UNSET:
            field_dict["has_custom_fields"] = has_custom_fields
        if is_custom_connector is not UNSET:
            field_dict["is_custom_connector"] = is_custom_connector
        if is_public_beta is not UNSET:
            field_dict["is_public_beta"] = is_public_beta
        if is_released is not UNSET:
            field_dict["is_released"] = is_released
        if is_internal is not UNSET:
            field_dict["is_internal"] = is_internal
        if applicable_destinations is not UNSET:
            field_dict["applicable_destinations"] = applicable_destinations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_source_id = d.pop("data_source_id", UNSET)

        def _parse_service_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service_name = _parse_service_name(d.pop("service_name", UNSET))

        def _parse_service_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service_provider = _parse_service_provider(d.pop("service_provider", UNSET))

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logo_url", UNSET))

        has_custom_fields = d.pop("has_custom_fields", UNSET)

        is_custom_connector = d.pop("is_custom_connector", UNSET)

        is_public_beta = d.pop("is_public_beta", UNSET)

        is_released = d.pop("is_released", UNSET)

        def _parse_is_internal(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_internal = _parse_is_internal(d.pop("is_internal", UNSET))

        applicable_destinations = cast(list[str], d.pop("applicable_destinations", UNSET))

        data_source_info = cls(
            data_source_id=data_source_id,
            service_name=service_name,
            service_provider=service_provider,
            logo_url=logo_url,
            has_custom_fields=has_custom_fields,
            is_custom_connector=is_custom_connector,
            is_public_beta=is_public_beta,
            is_released=is_released,
            is_internal=is_internal,
            applicable_destinations=applicable_destinations,
        )

        data_source_info.additional_properties = d
        return data_source_info

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
