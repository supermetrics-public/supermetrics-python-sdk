from typing import Literal, cast

GetDataSourceLoginResponse500Error = Literal["LOGIN_SEARCH_FAILED"]

GET_DATA_SOURCE_LOGIN_RESPONSE_500_ERROR_VALUES: set[GetDataSourceLoginResponse500Error] = {
    "LOGIN_SEARCH_FAILED",
}


def check_get_data_source_login_response_500_error(value: str) -> GetDataSourceLoginResponse500Error:
    if value in GET_DATA_SOURCE_LOGIN_RESPONSE_500_ERROR_VALUES:
        return cast(GetDataSourceLoginResponse500Error, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_DATA_SOURCE_LOGIN_RESPONSE_500_ERROR_VALUES!r}")
