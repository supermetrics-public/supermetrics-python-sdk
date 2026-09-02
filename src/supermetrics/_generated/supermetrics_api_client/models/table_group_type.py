from typing import Literal

TableGroupType = Literal["table_group"]

TABLE_GROUP_TYPE_VALUES: set[TableGroupType] = {
    "table_group",
}


def check_table_group_type(value: str) -> TableGroupType:
    if value in TABLE_GROUP_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TABLE_GROUP_TYPE_VALUES!r}")
