from typing import Literal

BlendOutputType = Literal["join", "union"]

BLEND_OUTPUT_TYPE_VALUES: set[BlendOutputType] = {
    "join",
    "union",
}


def check_blend_output_type(value: str) -> BlendOutputType:
    if value in BLEND_OUTPUT_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_OUTPUT_TYPE_VALUES!r}")
