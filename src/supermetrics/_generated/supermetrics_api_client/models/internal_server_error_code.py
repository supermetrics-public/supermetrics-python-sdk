from typing import Literal

InternalServerErrorCode = Literal["INTERNAL_SERVER_ERROR"]

INTERNAL_SERVER_ERROR_CODE_VALUES: set[InternalServerErrorCode] = {
    "INTERNAL_SERVER_ERROR",
}


def check_internal_server_error_code(value: str) -> InternalServerErrorCode:
    if value in INTERNAL_SERVER_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INTERNAL_SERVER_ERROR_CODE_VALUES!r}")
