from typing import Literal

DefinitionValueType = Literal["data_source_field", "output_from_previous", "static"]

DEFINITION_VALUE_TYPE_VALUES: set[DefinitionValueType] = {
    "data_source_field",
    "output_from_previous",
    "static",
}


def check_definition_value_type(value: str) -> DefinitionValueType:
    if value in DEFINITION_VALUE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEFINITION_VALUE_TYPE_VALUES!r}")
