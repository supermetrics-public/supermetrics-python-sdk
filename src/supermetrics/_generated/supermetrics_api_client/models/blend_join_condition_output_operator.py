from typing import Literal

BlendJoinConditionOutputOperator = Literal["="]

BLEND_JOIN_CONDITION_OUTPUT_OPERATOR_VALUES: set[BlendJoinConditionOutputOperator] = {
    "=",
}


def check_blend_join_condition_output_operator(value: str) -> BlendJoinConditionOutputOperator:
    if value in BLEND_JOIN_CONDITION_OUTPUT_OPERATOR_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_JOIN_CONDITION_OUTPUT_OPERATOR_VALUES!r}")
