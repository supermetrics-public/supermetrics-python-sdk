from typing import Literal

ConditionStepType = Literal["condition"]

CONDITION_STEP_TYPE_VALUES: set[ConditionStepType] = {
    "condition",
}


def check_condition_step_type(value: str) -> ConditionStepType:
    if value in CONDITION_STEP_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONDITION_STEP_TYPE_VALUES!r}")
