from typing import Literal

QueryType = Literal["query"]

QUERY_TYPE_VALUES: set[QueryType] = {
    "query",
}


def check_query_type(value: str) -> QueryType:
    if value in QUERY_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUERY_TYPE_VALUES!r}")
