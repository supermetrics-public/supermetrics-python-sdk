from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_connector_request_configuration import UpdateConnectorRequestConfiguration
    from ..models.update_connector_request_connector import UpdateConnectorRequestConnector


T = TypeVar("T", bound="UpdateConnectorRequest")


@_attrs_define
class UpdateConnectorRequest:
    """Connector metadata and configuration to update.

    Attributes:
        connector (UpdateConnectorRequestConnector | Unset): Connector metadata to update
        configuration (UpdateConnectorRequestConfiguration | Unset): Connector configuration to update
    """

    connector: UpdateConnectorRequestConnector | Unset = UNSET
    configuration: UpdateConnectorRequestConfiguration | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connector: dict[str, Any] | Unset = UNSET
        if not isinstance(self.connector, Unset):
            connector = self.connector.to_dict()

        configuration: dict[str, Any] | Unset = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connector is not UNSET:
            field_dict["connector"] = connector
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_connector_request_configuration import UpdateConnectorRequestConfiguration
        from ..models.update_connector_request_connector import UpdateConnectorRequestConnector

        d = dict(src_dict)
        _connector = d.pop("connector", UNSET)
        connector: UpdateConnectorRequestConnector | Unset
        if isinstance(_connector, Unset):
            connector = UNSET
        else:
            connector = UpdateConnectorRequestConnector.from_dict(_connector)

        _configuration = d.pop("configuration", UNSET)
        configuration: UpdateConnectorRequestConfiguration | Unset
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = UpdateConnectorRequestConfiguration.from_dict(_configuration)

        update_connector_request = cls(
            connector=connector,
            configuration=configuration,
        )

        update_connector_request.additional_properties = d
        return update_connector_request

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
