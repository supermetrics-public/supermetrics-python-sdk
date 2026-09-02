from typing import Literal

ExportTableGroupResponse500Error = Literal["TABLE_GROUP_SEARCH_FAILED"]

EXPORT_TABLE_GROUP_RESPONSE_500_ERROR_VALUES: set[ExportTableGroupResponse500Error] = {
    "TABLE_GROUP_SEARCH_FAILED",
}


def check_export_table_group_response_500_error(value: str) -> ExportTableGroupResponse500Error:
    if value in EXPORT_TABLE_GROUP_RESPONSE_500_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EXPORT_TABLE_GROUP_RESPONSE_500_ERROR_VALUES!r}")
