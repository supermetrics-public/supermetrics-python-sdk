from typing import Literal

PermissionErrorCode = Literal["PERMISSION_ERROR"]

PERMISSION_ERROR_CODE_VALUES: set[PermissionErrorCode] = {
    "PERMISSION_ERROR",
}


def check_permission_error_code(value: str) -> PermissionErrorCode:
    if value in PERMISSION_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PERMISSION_ERROR_CODE_VALUES!r}")
