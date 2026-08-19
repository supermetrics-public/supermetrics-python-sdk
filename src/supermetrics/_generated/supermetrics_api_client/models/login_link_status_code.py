from typing import Literal

LoginLinkStatusCode = Literal["CLOSED", "EXPIRED", "OPEN"]

LOGIN_LINK_STATUS_CODE_VALUES: set[LoginLinkStatusCode] = {
    "CLOSED",
    "EXPIRED",
    "OPEN",
}


def check_login_link_status_code(value: str) -> LoginLinkStatusCode:
    if value in LOGIN_LINK_STATUS_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOGIN_LINK_STATUS_CODE_VALUES!r}")
