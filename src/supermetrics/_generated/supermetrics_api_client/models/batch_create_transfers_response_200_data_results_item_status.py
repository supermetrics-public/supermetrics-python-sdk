from typing import Literal

BatchCreateTransfersResponse200DataResultsItemStatus = Literal["error", "success"]

BATCH_CREATE_TRANSFERS_RESPONSE_200_DATA_RESULTS_ITEM_STATUS_VALUES: set[
    BatchCreateTransfersResponse200DataResultsItemStatus
] = {
    "error",
    "success",
}


def check_batch_create_transfers_response_200_data_results_item_status(
    value: str,
) -> BatchCreateTransfersResponse200DataResultsItemStatus:
    if value in BATCH_CREATE_TRANSFERS_RESPONSE_200_DATA_RESULTS_ITEM_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BATCH_CREATE_TRANSFERS_RESPONSE_200_DATA_RESULTS_ITEM_STATUS_VALUES!r}"
    )
