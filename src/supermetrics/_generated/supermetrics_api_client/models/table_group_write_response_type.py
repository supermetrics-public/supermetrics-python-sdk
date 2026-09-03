from typing import Literal

TableGroupWriteResponseType = Literal["table_group"]

TABLE_GROUP_WRITE_RESPONSE_TYPE_VALUES: set[TableGroupWriteResponseType] = {
    "table_group",
}


def check_table_group_write_response_type(value: str) -> TableGroupWriteResponseType:
    if value in TABLE_GROUP_WRITE_RESPONSE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TABLE_GROUP_WRITE_RESPONSE_TYPE_VALUES!r}")
