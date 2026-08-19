from typing import Literal

ListTransferRunsSortDirection = Literal["ASC", "DESC"]

LIST_TRANSFER_RUNS_SORT_DIRECTION_VALUES: set[ListTransferRunsSortDirection] = {
    "ASC",
    "DESC",
}


def check_list_transfer_runs_sort_direction(value: str) -> ListTransferRunsSortDirection:
    if value in LIST_TRANSFER_RUNS_SORT_DIRECTION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_TRANSFER_RUNS_SORT_DIRECTION_VALUES!r}")
