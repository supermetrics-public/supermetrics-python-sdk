from typing import Literal

WorkspaceInviteRequestInvitesItemRole = Literal["ADMIN", "EDITOR", "FINANCE", "OWNER", "VIEWER"]

WORKSPACE_INVITE_REQUEST_INVITES_ITEM_ROLE_VALUES: set[WorkspaceInviteRequestInvitesItemRole] = {
    "ADMIN",
    "EDITOR",
    "FINANCE",
    "OWNER",
    "VIEWER",
}


def check_workspace_invite_request_invites_item_role(value: str) -> WorkspaceInviteRequestInvitesItemRole:
    if value in WORKSPACE_INVITE_REQUEST_INVITES_ITEM_ROLE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {WORKSPACE_INVITE_REQUEST_INVITES_ITEM_ROLE_VALUES!r}"
    )
