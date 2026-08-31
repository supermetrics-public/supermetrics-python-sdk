from typing import Literal

ImportTableGroupResponse404Error = Literal["TABLE_GROUP_NOT_FOUND"]

IMPORT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES: set[ImportTableGroupResponse404Error] = {
    "TABLE_GROUP_NOT_FOUND",
}


def check_import_table_group_response_404_error(value: str) -> ImportTableGroupResponse404Error:
    if value in IMPORT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {IMPORT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES!r}")
