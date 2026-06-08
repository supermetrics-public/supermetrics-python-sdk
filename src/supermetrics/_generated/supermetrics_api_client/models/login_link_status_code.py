from typing import Literal, cast

LoginLinkStatusCode = Literal["CLOSED", "EXPIRED", "OPEN"]

LOGIN_LINK_STATUS_CODE_VALUES: set[LoginLinkStatusCode] = {
    "CLOSED",
    "EXPIRED",
    "OPEN",
}


def check_login_link_status_code(value: str) -> LoginLinkStatusCode:
    if value in LOGIN_LINK_STATUS_CODE_VALUES:
        return cast(LoginLinkStatusCode, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOGIN_LINK_STATUS_CODE_VALUES!r}")
