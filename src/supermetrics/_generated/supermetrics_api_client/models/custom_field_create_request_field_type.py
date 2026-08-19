from typing import Literal

CustomFieldCreateRequestFieldType = Literal["dim", "met"]

CUSTOM_FIELD_CREATE_REQUEST_FIELD_TYPE_VALUES: set[CustomFieldCreateRequestFieldType] = {
    "dim",
    "met",
}


def check_custom_field_create_request_field_type(value: str) -> CustomFieldCreateRequestFieldType:
    if value in CUSTOM_FIELD_CREATE_REQUEST_FIELD_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CUSTOM_FIELD_CREATE_REQUEST_FIELD_TYPE_VALUES!r}")
