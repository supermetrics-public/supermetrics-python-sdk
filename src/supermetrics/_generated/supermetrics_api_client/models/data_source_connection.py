from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DataSourceConnection")


@_attrs_define
class DataSourceConnection:
    """A created data source connection.

    Attributes:
        connection_id (UUID): Unique identifier for the created connection Example:
            019461A0-0000-7000-8000-000000000000.
        login_url (None | str | Unset): URL for OAuth login flow (used when data source requires user authentication).
            In the current V1 implementation, this is always null.
        connect_url (None | str | Unset): URL for connection flow (used when additional authentication steps are
            required).
            In the current V1 implementation, this is always null.
    """

    connection_id: UUID
    login_url: None | str | Unset = UNSET
    connect_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connection_id = str(self.connection_id)

        login_url: None | str | Unset
        if isinstance(self.login_url, Unset):
            login_url = UNSET
        else:
            login_url = self.login_url

        connect_url: None | str | Unset
        if isinstance(self.connect_url, Unset):
            connect_url = UNSET
        else:
            connect_url = self.connect_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connection_id": connection_id,
            }
        )
        if login_url is not UNSET:
            field_dict["login_url"] = login_url
        if connect_url is not UNSET:
            field_dict["connect_url"] = connect_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = UUID(d.pop("connection_id"))

        def _parse_login_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        login_url = _parse_login_url(d.pop("login_url", UNSET))

        def _parse_connect_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        connect_url = _parse_connect_url(d.pop("connect_url", UNSET))

        data_source_connection = cls(
            connection_id=connection_id,
            login_url=login_url,
            connect_url=connect_url,
        )

        data_source_connection.additional_properties = d
        return data_source_connection

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
