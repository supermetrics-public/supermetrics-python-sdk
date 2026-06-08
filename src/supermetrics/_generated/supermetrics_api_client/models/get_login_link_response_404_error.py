from typing import Literal, cast

GetLoginLinkResponse404Error = Literal["LINK_NOT_FOUND"]

GET_LOGIN_LINK_RESPONSE_404_ERROR_VALUES: set[GetLoginLinkResponse404Error] = {
    "LINK_NOT_FOUND",
}


def check_get_login_link_response_404_error(value: str) -> GetLoginLinkResponse404Error:
    if value in GET_LOGIN_LINK_RESPONSE_404_ERROR_VALUES:
        return cast(GetLoginLinkResponse404Error, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_LOGIN_LINK_RESPONSE_404_ERROR_VALUES!r}")
