from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_connector_request_configuration_configuration_json import (
        UpdateConnectorRequestConfigurationConfigurationJson,
    )


T = TypeVar("T", bound="UpdateConnectorRequestConfiguration")


@_attrs_define
class UpdateConnectorRequestConfiguration:
    """Connector configuration to update

    Attributes:
        configuration_json (UpdateConnectorRequestConfigurationConfigurationJson): JSON configuration data
    """

    configuration_json: UpdateConnectorRequestConfigurationConfigurationJson
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configuration_json = self.configuration_json.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "configuration_json": configuration_json,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_connector_request_configuration_configuration_json import (
            UpdateConnectorRequestConfigurationConfigurationJson,
        )

        d = dict(src_dict)
        configuration_json = UpdateConnectorRequestConfigurationConfigurationJson.from_dict(d.pop("configuration_json"))

        update_connector_request_configuration = cls(
            configuration_json=configuration_json,
        )

        update_connector_request_configuration.additional_properties = d
        return update_connector_request_configuration

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
