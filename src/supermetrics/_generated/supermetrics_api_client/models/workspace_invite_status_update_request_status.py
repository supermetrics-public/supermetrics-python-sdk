from typing import Literal

WorkspaceInviteStatusUpdateRequestStatus = Literal["cancelled"]

WORKSPACE_INVITE_STATUS_UPDATE_REQUEST_STATUS_VALUES: set[WorkspaceInviteStatusUpdateRequestStatus] = {
    "cancelled",
}


def check_workspace_invite_status_update_request_status(value: str) -> WorkspaceInviteStatusUpdateRequestStatus:
    if value in WORKSPACE_INVITE_STATUS_UPDATE_REQUEST_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {WORKSPACE_INVITE_STATUS_UPDATE_REQUEST_STATUS_VALUES!r}"
    )
