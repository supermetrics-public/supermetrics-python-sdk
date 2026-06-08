from typing import Literal, cast

CloseLoginLinkResponse500Error = Literal["LINK_UPDATE_FAILED"]

CLOSE_LOGIN_LINK_RESPONSE_500_ERROR_VALUES: set[CloseLoginLinkResponse500Error] = {
    "LINK_UPDATE_FAILED",
}


def check_close_login_link_response_500_error(value: str) -> CloseLoginLinkResponse500Error:
    if value in CLOSE_LOGIN_LINK_RESPONSE_500_ERROR_VALUES:
        return cast(CloseLoginLinkResponse500Error, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CLOSE_LOGIN_LINK_RESPONSE_500_ERROR_VALUES!r}")
