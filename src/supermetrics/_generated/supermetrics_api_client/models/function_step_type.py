from typing import Literal

FunctionStepType = Literal["function"]

FUNCTION_STEP_TYPE_VALUES: set[FunctionStepType] = {
    "function",
}


def check_function_step_type(value: str) -> FunctionStepType:
    if value in FUNCTION_STEP_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_STEP_TYPE_VALUES!r}")
