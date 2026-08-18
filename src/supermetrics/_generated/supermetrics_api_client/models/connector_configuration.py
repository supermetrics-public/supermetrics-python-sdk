from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connector_configuration_configuration_json import ConnectorConfigurationConfigurationJson


T = TypeVar("T", bound="ConnectorConfiguration")


@_attrs_define
class ConnectorConfiguration:
    """Configuration data for a connector.

    Attributes:
        version (str | Unset): Version of the configuration Example: 1.0.0.
        configuration_json (ConnectorConfigurationConfigurationJson | Unset): JSON configuration data
        created_at (datetime.datetime | Unset): Configuration creation timestamp in ISO 8601 format Example:
            2025-01-01T00:00:00+00:00.
        updated_at (datetime.datetime | Unset): Configuration last update timestamp in ISO 8601 format Example:
            2025-01-01T00:00:00+00:00.
    """

    version: str | Unset = UNSET
    configuration_json: ConnectorConfigurationConfigurationJson | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        configuration_json: dict[str, Any] | Unset = UNSET
        if not isinstance(self.configuration_json, Unset):
            configuration_json = self.configuration_json.to_dict()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if configuration_json is not UNSET:
            field_dict["configuration_json"] = configuration_json
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connector_configuration_configuration_json import ConnectorConfigurationConfigurationJson

        d = dict(src_dict)
        version = d.pop("version", UNSET)

        _configuration_json = d.pop("configuration_json", UNSET)
        configuration_json: ConnectorConfigurationConfigurationJson | Unset
        if isinstance(_configuration_json, Unset):
            configuration_json = UNSET
        else:
            configuration_json = ConnectorConfigurationConfigurationJson.from_dict(_configuration_json)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        connector_configuration = cls(
            version=version,
            configuration_json=configuration_json,
            created_at=created_at,
            updated_at=updated_at,
        )

        connector_configuration.additional_properties = d
        return connector_configuration

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
