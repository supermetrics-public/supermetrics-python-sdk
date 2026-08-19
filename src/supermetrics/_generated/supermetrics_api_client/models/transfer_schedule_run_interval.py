from typing import Literal

TransferScheduleRunInterval = Literal["daily", "hourly", "monthly", "weekly"]

TRANSFER_SCHEDULE_RUN_INTERVAL_VALUES: set[TransferScheduleRunInterval] = {
    "daily",
    "hourly",
    "monthly",
    "weekly",
}


def check_transfer_schedule_run_interval(value: str) -> TransferScheduleRunInterval:
    if value in TRANSFER_SCHEDULE_RUN_INTERVAL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TRANSFER_SCHEDULE_RUN_INTERVAL_VALUES!r}")
