from typing import Literal

BadRequestErrorCode = Literal["BAD_REQUEST"]

BAD_REQUEST_ERROR_CODE_VALUES: set[BadRequestErrorCode] = {
    "BAD_REQUEST",
}


def check_bad_request_error_code(value: str) -> BadRequestErrorCode:
    if value in BAD_REQUEST_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BAD_REQUEST_ERROR_CODE_VALUES!r}")
