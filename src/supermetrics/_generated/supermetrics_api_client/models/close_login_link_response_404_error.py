from typing import Literal, cast

CloseLoginLinkResponse404Error = Literal["LINK_NOT_FOUND"]

CLOSE_LOGIN_LINK_RESPONSE_404_ERROR_VALUES: set[CloseLoginLinkResponse404Error] = {
    "LINK_NOT_FOUND",
}


def check_close_login_link_response_404_error(value: str) -> CloseLoginLinkResponse404Error:
    if value in CLOSE_LOGIN_LINK_RESPONSE_404_ERROR_VALUES:
        return cast(CloseLoginLinkResponse404Error, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CLOSE_LOGIN_LINK_RESPONSE_404_ERROR_VALUES!r}")
