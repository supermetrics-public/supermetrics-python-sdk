from typing import Literal, cast

ListDataSourceLoginsResponse500Error = Literal["LOGIN_SEARCH_FAILED"]

LIST_DATA_SOURCE_LOGINS_RESPONSE_500_ERROR_VALUES: set[ListDataSourceLoginsResponse500Error] = {
    "LOGIN_SEARCH_FAILED",
}


def check_list_data_source_logins_response_500_error(value: str) -> ListDataSourceLoginsResponse500Error:
    if value in LIST_DATA_SOURCE_LOGINS_RESPONSE_500_ERROR_VALUES:
        return cast(ListDataSourceLoginsResponse500Error, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_DATA_SOURCE_LOGINS_RESPONSE_500_ERROR_VALUES!r}"
    )
