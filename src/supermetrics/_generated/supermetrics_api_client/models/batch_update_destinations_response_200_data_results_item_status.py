from typing import Literal

BatchUpdateDestinationsResponse200DataResultsItemStatus = Literal["error", "success"]

BATCH_UPDATE_DESTINATIONS_RESPONSE_200_DATA_RESULTS_ITEM_STATUS_VALUES: set[
    BatchUpdateDestinationsResponse200DataResultsItemStatus
] = {
    "error",
    "success",
}


def check_batch_update_destinations_response_200_data_results_item_status(
    value: str,
) -> BatchUpdateDestinationsResponse200DataResultsItemStatus:
    if value in BATCH_UPDATE_DESTINATIONS_RESPONSE_200_DATA_RESULTS_ITEM_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BATCH_UPDATE_DESTINATIONS_RESPONSE_200_DATA_RESULTS_ITEM_STATUS_VALUES!r}"
    )
