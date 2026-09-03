from typing import Literal

TooManyRequestsErrorCode = Literal["TOO_MANY_REQUESTS"]

TOO_MANY_REQUESTS_ERROR_CODE_VALUES: set[TooManyRequestsErrorCode] = {
    "TOO_MANY_REQUESTS",
}


def check_too_many_requests_error_code(value: str) -> TooManyRequestsErrorCode:
    if value in TOO_MANY_REQUESTS_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TOO_MANY_REQUESTS_ERROR_CODE_VALUES!r}")
