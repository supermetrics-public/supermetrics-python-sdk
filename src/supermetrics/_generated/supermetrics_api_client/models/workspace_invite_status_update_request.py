from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.workspace_invite_status_update_request_status import (
    WorkspaceInviteStatusUpdateRequestStatus,
    check_workspace_invite_status_update_request_status,
)

T = TypeVar("T", bound="WorkspaceInviteStatusUpdateRequest")


@_attrs_define
class WorkspaceInviteStatusUpdateRequest:
    """Invitation status update.

    Attributes:
        email (str): Email of the user whose invitation to update Example: user@example.com.
        status (WorkspaceInviteStatusUpdateRequestStatus): New invitation status Example: cancelled.
    """

    email: str
    status: WorkspaceInviteStatusUpdateRequestStatus

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        status: str = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        status = check_workspace_invite_status_update_request_status(d.pop("status"))

        workspace_invite_status_update_request = cls(
            email=email,
            status=status,
        )

        return workspace_invite_status_update_request
