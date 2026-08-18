from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateConnectorBody")


@_attrs_define
class CreateConnectorBody:
    """
    Attributes:
        title (str): Name of the connector
        description (str | Unset): Description of the connector
        connector_identifier (str | Unset): Identifier of an existing connector to duplicate. If omitted, creates with
            default configuration.
    """

    title: str
    description: str | Unset = UNSET
    connector_identifier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        connector_identifier = self.connector_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if connector_identifier is not UNSET:
            field_dict["connector_identifier"] = connector_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        description = d.pop("description", UNSET)

        connector_identifier = d.pop("connector_identifier", UNSET)

        create_connector_body = cls(
            title=title,
            description=description,
            connector_identifier=connector_identifier,
        )

        create_connector_body.additional_properties = d
        return create_connector_body

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
