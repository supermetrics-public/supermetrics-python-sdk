from typing import Literal

ConditionCaseConditionType = Literal["rule"]

CONDITION_CASE_CONDITION_TYPE_VALUES: set[ConditionCaseConditionType] = {
    "rule",
}


def check_condition_case_condition_type(value: str) -> ConditionCaseConditionType:
    if value in CONDITION_CASE_CONDITION_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONDITION_CASE_CONDITION_TYPE_VALUES!r}")
