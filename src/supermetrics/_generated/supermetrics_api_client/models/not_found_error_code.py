from typing import Literal

NotFoundErrorCode = Literal["NOT_FOUND"]

NOT_FOUND_ERROR_CODE_VALUES: set[NotFoundErrorCode] = {
    "NOT_FOUND",
}


def check_not_found_error_code(value: str) -> NotFoundErrorCode:
    if value in NOT_FOUND_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NOT_FOUND_ERROR_CODE_VALUES!r}")
