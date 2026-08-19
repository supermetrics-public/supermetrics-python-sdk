from typing import Literal

LookupStepType = Literal["lookup"]

LOOKUP_STEP_TYPE_VALUES: set[LookupStepType] = {
    "lookup",
}


def check_lookup_step_type(value: str) -> LookupStepType:
    if value in LOOKUP_STEP_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOOKUP_STEP_TYPE_VALUES!r}")
