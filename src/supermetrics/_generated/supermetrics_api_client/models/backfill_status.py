from typing import Literal, cast

BackfillStatus = Literal["CANCELLED", "COMPLETED", "CREATED", "FAILED", "RUNNING", "SCHEDULED"]

BACKFILL_STATUS_VALUES: set[BackfillStatus] = {
    "CANCELLED",
    "COMPLETED",
    "CREATED",
    "FAILED",
    "RUNNING",
    "SCHEDULED",
}


def check_backfill_status(value: str) -> BackfillStatus:
    if value in BACKFILL_STATUS_VALUES:
        return cast(BackfillStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BACKFILL_STATUS_VALUES!r}")
