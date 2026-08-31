from typing import Literal

ImportTableGroupResponse500Error = Literal["TABLE_GROUP_CREATE_FAILED"]

IMPORT_TABLE_GROUP_RESPONSE_500_ERROR_VALUES: set[ImportTableGroupResponse500Error] = {
    "TABLE_GROUP_CREATE_FAILED",
}


def check_import_table_group_response_500_error(value: str) -> ImportTableGroupResponse500Error:
    if value in IMPORT_TABLE_GROUP_RESPONSE_500_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {IMPORT_TABLE_GROUP_RESPONSE_500_ERROR_VALUES!r}")
