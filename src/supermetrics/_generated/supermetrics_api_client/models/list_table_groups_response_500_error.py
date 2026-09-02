from typing import Literal

ListTableGroupsResponse500Error = Literal["TABLE_GROUP_SEARCH_FAILED"]

LIST_TABLE_GROUPS_RESPONSE_500_ERROR_VALUES: set[ListTableGroupsResponse500Error] = {
    "TABLE_GROUP_SEARCH_FAILED",
}


def check_list_table_groups_response_500_error(value: str) -> ListTableGroupsResponse500Error:
    if value in LIST_TABLE_GROUPS_RESPONSE_500_ERROR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_TABLE_GROUPS_RESPONSE_500_ERROR_VALUES!r}")
