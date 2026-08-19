from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_data_source_setting import TransferDataSourceSetting


T = TypeVar("T", bound="TransferConfigurationResponseDataSource")


@_attrs_define
class TransferConfigurationResponseDataSource:
    """Data source information and settings

    Attributes:
        data_source_id (str | Unset): Data source identifier
        service_name (str | Unset): Service name
        service_provider (str | Unset): Service provider
        settings (list[TransferDataSourceSetting] | Unset): Data source settings
    """

    data_source_id: str | Unset = UNSET
    service_name: str | Unset = UNSET
    service_provider: str | Unset = UNSET
    settings: list[TransferDataSourceSetting] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_id = self.data_source_id

        service_name = self.service_name

        service_provider = self.service_provider

        settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_source_id is not UNSET:
            field_dict["data_source_id"] = data_source_id
        if service_name is not UNSET:
            field_dict["service_name"] = service_name
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_data_source_setting import TransferDataSourceSetting

        d = dict(src_dict)
        data_source_id = d.pop("data_source_id", UNSET)

        service_name = d.pop("service_name", UNSET)

        service_provider = d.pop("service_provider", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: list[TransferDataSourceSetting] | Unset = UNSET
        if _settings is not UNSET:
            settings = []
            for settings_item_data in _settings:
                settings_item = TransferDataSourceSetting.from_dict(settings_item_data)

                settings.append(settings_item)

        transfer_configuration_response_data_source = cls(
            data_source_id=data_source_id,
            service_name=service_name,
            service_provider=service_provider,
            settings=settings,
        )

        transfer_configuration_response_data_source.additional_properties = d
        return transfer_configuration_response_data_source

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
