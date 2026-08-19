from typing import Literal

BlendJoinType = Literal["full outer", "inner", "left", "right"]

BLEND_JOIN_TYPE_VALUES: set[BlendJoinType] = {
    "full outer",
    "inner",
    "left",
    "right",
}


def check_blend_join_type(value: str) -> BlendJoinType:
    if value in BLEND_JOIN_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_JOIN_TYPE_VALUES!r}")
