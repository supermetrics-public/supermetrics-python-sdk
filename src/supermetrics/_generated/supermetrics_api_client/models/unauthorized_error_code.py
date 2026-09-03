from typing import Literal

UnauthorizedErrorCode = Literal["UNAUTHORIZED"]

UNAUTHORIZED_ERROR_CODE_VALUES: set[UnauthorizedErrorCode] = {
    "UNAUTHORIZED",
}


def check_unauthorized_error_code(value: str) -> UnauthorizedErrorCode:
    if value in UNAUTHORIZED_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UNAUTHORIZED_ERROR_CODE_VALUES!r}")
