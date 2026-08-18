from typing import Literal

ListTransferRunsSortField = Literal["created_time", "data_date", "ended_time"]

LIST_TRANSFER_RUNS_SORT_FIELD_VALUES: set[ListTransferRunsSortField] = {
    "created_time",
    "data_date",
    "ended_time",
}


def check_list_transfer_runs_sort_field(value: str) -> ListTransferRunsSortField:
    if value in LIST_TRANSFER_RUNS_SORT_FIELD_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_TRANSFER_RUNS_SORT_FIELD_VALUES!r}")
