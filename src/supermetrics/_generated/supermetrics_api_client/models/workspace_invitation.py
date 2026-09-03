from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_invitation_role import WorkspaceInvitationRole, check_workspace_invitation_role
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceInvitation")


@_attrs_define
class WorkspaceInvitation:
    """Workspace invitation data

    Attributes:
        role (WorkspaceInvitationRole | Unset): Role assigned to the invited user Example: EDITOR.
        email (str | Unset): Email address of the invited user Example: user@example.com.
        date_sent (datetime.date | Unset): Date the invitation was sent Example: 2026-06-15.
    """

    role: WorkspaceInvitationRole | Unset = UNSET
    email: str | Unset = UNSET
    date_sent: datetime.date | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role

        email = self.email

        date_sent: str | Unset = UNSET
        if not isinstance(self.date_sent, Unset):
            date_sent = self.date_sent.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["role"] = role
        if email is not UNSET:
            field_dict["email"] = email
        if date_sent is not UNSET:
            field_dict["date_sent"] = date_sent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _role = d.pop("role", UNSET)
        role: WorkspaceInvitationRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = check_workspace_invitation_role(_role)

        email = d.pop("email", UNSET)

        _date_sent = d.pop("date_sent", UNSET)
        date_sent: datetime.date | Unset
        if isinstance(_date_sent, Unset):
            date_sent = UNSET
        else:
            date_sent = datetime.date.fromisoformat(_date_sent)

        workspace_invitation = cls(
            role=role,
            email=email,
            date_sent=date_sent,
        )

        workspace_invitation.additional_properties = d
        return workspace_invitation

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
