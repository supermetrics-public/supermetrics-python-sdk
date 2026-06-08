from typing import Literal, cast

CreateLoginLinkResponse403Error = Literal["LINK_LIMIT_EXCEEDED"]

CREATE_LOGIN_LINK_RESPONSE_403_ERROR_VALUES: set[CreateLoginLinkResponse403Error] = {
    "LINK_LIMIT_EXCEEDED",
}


def check_create_login_link_response_403_error(value: str) -> CreateLoginLinkResponse403Error:
    if value in CREATE_LOGIN_LINK_RESPONSE_403_ERROR_VALUES:
        return cast(CreateLoginLinkResponse403Error, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_LOGIN_LINK_RESPONSE_403_ERROR_VALUES!r}")
