from typing import Literal

ExportTableGroupResponse404Error = Literal["TABLE_GROUP_NOT_FOUND"]

EXPORT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES: set[ExportTableGroupResponse404Error] = {
    "TABLE_GROUP_NOT_FOUND",
}


def check_export_table_group_response_404_error(value: str) -> ExportTableGroupResponse404Error:
    if value in EXPORT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EXPORT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES!r}")
