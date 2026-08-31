from typing import Literal

ImportTableGroupResponse409Error = Literal["TABLE_GROUP_NAME_CONFLICT"]

IMPORT_TABLE_GROUP_RESPONSE_409_ERROR_VALUES: set[ImportTableGroupResponse409Error] = {
    "TABLE_GROUP_NAME_CONFLICT",
}


def check_import_table_group_response_409_error(value: str) -> ImportTableGroupResponse409Error:
    if value in IMPORT_TABLE_GROUP_RESPONSE_409_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {IMPORT_TABLE_GROUP_RESPONSE_409_ERROR_VALUES!r}")
