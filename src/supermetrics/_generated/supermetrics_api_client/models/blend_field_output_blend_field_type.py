from typing import Literal

BlendFieldOutputBlendFieldType = Literal["dim", "met"]

BLEND_FIELD_OUTPUT_BLEND_FIELD_TYPE_VALUES: set[BlendFieldOutputBlendFieldType] = {
    "dim",
    "met",
}


def check_blend_field_output_blend_field_type(value: str) -> BlendFieldOutputBlendFieldType:
    if value in BLEND_FIELD_OUTPUT_BLEND_FIELD_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_FIELD_OUTPUT_BLEND_FIELD_TYPE_VALUES!r}")
