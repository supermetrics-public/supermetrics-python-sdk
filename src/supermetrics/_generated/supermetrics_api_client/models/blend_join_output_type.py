from typing import Literal

BlendJoinOutputType = Literal["full outer", "inner", "left", "right"]

BLEND_JOIN_OUTPUT_TYPE_VALUES: set[BlendJoinOutputType] = {
    "full outer",
    "inner",
    "left",
    "right",
}


def check_blend_join_output_type(value: str) -> BlendJoinOutputType:
    if value in BLEND_JOIN_OUTPUT_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_JOIN_OUTPUT_TYPE_VALUES!r}")
