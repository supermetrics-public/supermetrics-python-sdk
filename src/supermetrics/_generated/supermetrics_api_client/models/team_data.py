from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamData")


@_attrs_define
class TeamData:
    """Team resource

    Attributes:
        team_id (int | Unset): Unique identifier of the team Example: 123.
        name (str | Unset): Name of the team Example: My Team.
        display_id (str | Unset): Human-readable display identifier of the team Example: SM_ABC123.
        status (int | Unset): Status code of the team Example: 1.
        created_at (datetime.datetime | Unset): Timestamp when the team was created in ISO 8601 format Example:
            2026-01-01T00:00:00+00:00.
    """

    team_id: int | Unset = UNSET
    name: str | Unset = UNSET
    display_id: str | Unset = UNSET
    status: int | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        team_id = self.team_id

        name = self.name

        display_id = self.display_id

        status = self.status

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if name is not UNSET:
            field_dict["name"] = name
        if display_id is not UNSET:
            field_dict["display_id"] = display_id
        if status is not UNSET:
            field_dict["status"] = status
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        team_id = d.pop("team_id", UNSET)

        name = d.pop("name", UNSET)

        display_id = d.pop("display_id", UNSET)

        status = d.pop("status", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)

        team_data = cls(
            team_id=team_id,
            name=name,
            display_id=display_id,
            status=status,
            created_at=created_at,
        )

        team_data.additional_properties = d
        return team_data

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
