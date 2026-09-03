from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.workspace_user_role_update_request_role import (
    WorkspaceUserRoleUpdateRequestRole,
    check_workspace_user_role_update_request_role,
)

T = TypeVar("T", bound="WorkspaceUserRoleUpdateRequest")


@_attrs_define
class WorkspaceUserRoleUpdateRequest:
    """New role to assign to a workspace user.

    Attributes:
        role (WorkspaceUserRoleUpdateRequestRole): New role for the workspace user Example: EDITOR.
    """

    role: WorkspaceUserRoleUpdateRequestRole

    def to_dict(self) -> dict[str, Any]:
        role: str = self.role

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = check_workspace_user_role_update_request_role(d.pop("role"))

        workspace_user_role_update_request = cls(
            role=role,
        )

        return workspace_user_role_update_request
