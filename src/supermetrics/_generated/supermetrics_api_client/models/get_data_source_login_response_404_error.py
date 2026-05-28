from typing import Literal, cast

GetDataSourceLoginResponse404Error = Literal["LOGIN_NOT_FOUND"]

GET_DATA_SOURCE_LOGIN_RESPONSE_404_ERROR_VALUES: set[GetDataSourceLoginResponse404Error] = {
    "LOGIN_NOT_FOUND",
}


def check_get_data_source_login_response_404_error(value: str) -> GetDataSourceLoginResponse404Error:
    if value in GET_DATA_SOURCE_LOGIN_RESPONSE_404_ERROR_VALUES:
        return cast(GetDataSourceLoginResponse404Error, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_DATA_SOURCE_LOGIN_RESPONSE_404_ERROR_VALUES!r}")
