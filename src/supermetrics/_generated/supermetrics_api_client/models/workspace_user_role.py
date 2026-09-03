from typing import Literal

WorkspaceUserRole = Literal["ADMIN", "EDITOR", "FINANCE", "OWNER", "VIEWER"]

WORKSPACE_USER_ROLE_VALUES: set[WorkspaceUserRole] = {
    "ADMIN",
    "EDITOR",
    "FINANCE",
    "OWNER",
    "VIEWER",
}


def check_workspace_user_role(value: str) -> WorkspaceUserRole:
    if value in WORKSPACE_USER_ROLE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {WORKSPACE_USER_ROLE_VALUES!r}")
