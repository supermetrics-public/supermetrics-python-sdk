from typing import Literal

WorkspaceUserRoleUpdateRequestRole = Literal["ADMIN", "EDITOR", "FINANCE", "OWNER", "VIEWER"]

WORKSPACE_USER_ROLE_UPDATE_REQUEST_ROLE_VALUES: set[WorkspaceUserRoleUpdateRequestRole] = {
    "ADMIN",
    "EDITOR",
    "FINANCE",
    "OWNER",
    "VIEWER",
}


def check_workspace_user_role_update_request_role(value: str) -> WorkspaceUserRoleUpdateRequestRole:
    if value in WORKSPACE_USER_ROLE_UPDATE_REQUEST_ROLE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {WORKSPACE_USER_ROLE_UPDATE_REQUEST_ROLE_VALUES!r}")
