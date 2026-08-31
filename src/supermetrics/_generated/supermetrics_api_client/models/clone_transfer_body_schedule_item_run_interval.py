from typing import Literal

CloneTransferBodyScheduleItemRunInterval = Literal["daily", "monthly", "weekly"]

CLONE_TRANSFER_BODY_SCHEDULE_ITEM_RUN_INTERVAL_VALUES: set[CloneTransferBodyScheduleItemRunInterval] = {
    "daily",
    "monthly",
    "weekly",
}


def check_clone_transfer_body_schedule_item_run_interval(value: str) -> CloneTransferBodyScheduleItemRunInterval:
    if value in CLONE_TRANSFER_BODY_SCHEDULE_ITEM_RUN_INTERVAL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLONE_TRANSFER_BODY_SCHEDULE_ITEM_RUN_INTERVAL_VALUES!r}"
    )
