from typing import Literal

QueryGroupType = Literal["query_group"]

QUERY_GROUP_TYPE_VALUES: set[QueryGroupType] = {
    "query_group",
}


def check_query_group_type(value: str) -> QueryGroupType:
    if value in QUERY_GROUP_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUERY_GROUP_TYPE_VALUES!r}")
