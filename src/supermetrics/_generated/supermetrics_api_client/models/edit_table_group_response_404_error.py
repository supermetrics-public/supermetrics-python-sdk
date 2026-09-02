from typing import Literal

EditTableGroupResponse404Error = Literal["TABLE_GROUP_NOT_FOUND"]

EDIT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES: set[EditTableGroupResponse404Error] = {
    "TABLE_GROUP_NOT_FOUND",
}


def check_edit_table_group_response_404_error(value: str) -> EditTableGroupResponse404Error:
    if value in EDIT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EDIT_TABLE_GROUP_RESPONSE_404_ERROR_VALUES!r}")
