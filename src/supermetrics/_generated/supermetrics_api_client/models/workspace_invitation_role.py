from typing import Literal

WorkspaceInvitationRole = Literal["ADMIN", "EDITOR", "FINANCE", "OWNER", "VIEWER"]

WORKSPACE_INVITATION_ROLE_VALUES: set[WorkspaceInvitationRole] = {
    "ADMIN",
    "EDITOR",
    "FINANCE",
    "OWNER",
    "VIEWER",
}


def check_workspace_invitation_role(value: str) -> WorkspaceInvitationRole:
    if value in WORKSPACE_INVITATION_ROLE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {WORKSPACE_INVITATION_ROLE_VALUES!r}")
