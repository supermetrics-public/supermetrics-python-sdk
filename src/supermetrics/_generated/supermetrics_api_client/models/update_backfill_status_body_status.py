from typing import Literal, cast

UpdateBackfillStatusBodyStatus = Literal["CANCELLED"]

UPDATE_BACKFILL_STATUS_BODY_STATUS_VALUES: set[UpdateBackfillStatusBodyStatus] = {
    "CANCELLED",
}


def check_update_backfill_status_body_status(value: str) -> UpdateBackfillStatusBodyStatus:
    if value in UPDATE_BACKFILL_STATUS_BODY_STATUS_VALUES:
        return cast(UpdateBackfillStatusBodyStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_BACKFILL_STATUS_BODY_STATUS_VALUES!r}")
