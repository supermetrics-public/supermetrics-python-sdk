from typing import Literal

TransferRunItemType = Literal["Backfill", "Recurring"]

TRANSFER_RUN_ITEM_TYPE_VALUES: set[TransferRunItemType] = {
    "Backfill",
    "Recurring",
}


def check_transfer_run_item_type(value: str) -> TransferRunItemType:
    if value in TRANSFER_RUN_ITEM_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TRANSFER_RUN_ITEM_TYPE_VALUES!r}")
