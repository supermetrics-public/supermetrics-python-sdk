from typing import Literal

TeamTransformationOutputFieldType = Literal["dim", "met"]

TEAM_TRANSFORMATION_OUTPUT_FIELD_TYPE_VALUES: set[TeamTransformationOutputFieldType] = {
    "dim",
    "met",
}


def check_team_transformation_output_field_type(value: str) -> TeamTransformationOutputFieldType:
    if value in TEAM_TRANSFORMATION_OUTPUT_FIELD_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TEAM_TRANSFORMATION_OUTPUT_FIELD_TYPE_VALUES!r}")
