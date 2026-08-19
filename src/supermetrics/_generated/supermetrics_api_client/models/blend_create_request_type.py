from typing import Literal

BlendCreateRequestType = Literal["join", "union"]

BLEND_CREATE_REQUEST_TYPE_VALUES: set[BlendCreateRequestType] = {
    "join",
    "union",
}


def check_blend_create_request_type(value: str) -> BlendCreateRequestType:
    if value in BLEND_CREATE_REQUEST_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_CREATE_REQUEST_TYPE_VALUES!r}")
