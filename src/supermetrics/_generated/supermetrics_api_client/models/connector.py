from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Connector")


@_attrs_define
class Connector:
    """A custom connector with its metadata.

    Attributes:
        connector_identifier (str | Unset): Unique identifier of the connector Example: T3S70.
        name (str | Unset): Name of the connector Example: Test Connector.
        description (None | str | Unset): Description of the connector Example: A custom connector for fetching
            marketing data.
        logo_url (None | str | Unset): URL of the connector logo Example:
            https://assets.supermetrics.com/images/dsLogos/Custom_Connector_Default.png.
        created_at (datetime.datetime | Unset): Creation timestamp in ISO 8601 format Example:
            2025-01-01T00:00:00+00:00.
        updated_at (datetime.datetime | Unset): Last update timestamp in ISO 8601 format Example:
            2025-01-01T00:00:00+00:00.
    """

    connector_identifier: str | Unset = UNSET
    name: str | Unset = UNSET
    description: None | str | Unset = UNSET
    logo_url: None | str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connector_identifier = self.connector_identifier

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connector_identifier is not UNSET:
            field_dict["connector_identifier"] = connector_identifier
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connector_identifier = d.pop("connector_identifier", UNSET)

        name = d.pop("name", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logo_url", UNSET))

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

        connector = cls(
            connector_identifier=connector_identifier,
            name=name,
            description=description,
            logo_url=logo_url,
            created_at=created_at,
            updated_at=updated_at,
        )

        connector.additional_properties = d
        return connector

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
