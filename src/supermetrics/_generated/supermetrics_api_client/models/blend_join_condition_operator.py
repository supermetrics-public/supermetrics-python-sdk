from typing import Literal

BlendJoinConditionOperator = Literal["="]

BLEND_JOIN_CONDITION_OPERATOR_VALUES: set[BlendJoinConditionOperator] = {
    "=",
}


def check_blend_join_condition_operator(value: str) -> BlendJoinConditionOperator:
    if value in BLEND_JOIN_CONDITION_OPERATOR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_JOIN_CONDITION_OPERATOR_VALUES!r}")
