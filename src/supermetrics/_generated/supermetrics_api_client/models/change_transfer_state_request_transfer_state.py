from typing import Literal

ChangeTransferStateRequestTransferState = Literal["pause", "unpause"]

CHANGE_TRANSFER_STATE_REQUEST_TRANSFER_STATE_VALUES: set[ChangeTransferStateRequestTransferState] = {
    "pause",
    "unpause",
}


def check_change_transfer_state_request_transfer_state(value: str) -> ChangeTransferStateRequestTransferState:
    if value in CHANGE_TRANSFER_STATE_REQUEST_TRANSFER_STATE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CHANGE_TRANSFER_STATE_REQUEST_TRANSFER_STATE_VALUES!r}"
    )
