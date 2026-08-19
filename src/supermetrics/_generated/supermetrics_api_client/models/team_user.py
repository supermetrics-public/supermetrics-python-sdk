from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamUser")


@_attrs_define
class TeamUser:
    """A user belonging to a team.

    Attributes:
        user_id (int | Unset): Unique identifier of the user Example: 1.
        email (str | Unset): Email address of the user Example: user@example.com.
        first_name (str | Unset): First name of the user Example: John.
        last_name (str | Unset): Last name of the user Example: Doe.
        role (str | Unset): Role of the user within the team Example: ADMIN.
        created_at (datetime.datetime | Unset): Timestamp when the user was added to the team in ISO 8601 format
            Example: 2026-01-01T00:00:00+00:00.
    """

    user_id: int | Unset = UNSET
    email: str | Unset = UNSET
    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    role: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        role = self.role

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if role is not UNSET:
            field_dict["role"] = role
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("user_id", UNSET)

        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        role = d.pop("role", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)

        team_user = cls(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            created_at=created_at,
        )

        return team_user
