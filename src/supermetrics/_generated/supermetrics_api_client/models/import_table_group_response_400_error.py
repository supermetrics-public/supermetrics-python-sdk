from typing import Literal

ImportTableGroupResponse400Error = Literal["TABLE_GROUP_IMPORT_ERROR"]

IMPORT_TABLE_GROUP_RESPONSE_400_ERROR_VALUES: set[ImportTableGroupResponse400Error] = {
    "TABLE_GROUP_IMPORT_ERROR",
}


def check_import_table_group_response_400_error(value: str) -> ImportTableGroupResponse400Error:
    if value in IMPORT_TABLE_GROUP_RESPONSE_400_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {IMPORT_TABLE_GROUP_RESPONSE_400_ERROR_VALUES!r}")
