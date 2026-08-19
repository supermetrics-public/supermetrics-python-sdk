from typing import Literal

BlendDatasourceFieldRefOutputDatasourceFieldType = Literal["dim", "met"]

BLEND_DATASOURCE_FIELD_REF_OUTPUT_DATASOURCE_FIELD_TYPE_VALUES: set[
    BlendDatasourceFieldRefOutputDatasourceFieldType
] = {
    "dim",
    "met",
}


def check_blend_datasource_field_ref_output_datasource_field_type(
    value: str,
) -> BlendDatasourceFieldRefOutputDatasourceFieldType:
    if value in BLEND_DATASOURCE_FIELD_REF_OUTPUT_DATASOURCE_FIELD_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BLEND_DATASOURCE_FIELD_REF_OUTPUT_DATASOURCE_FIELD_TYPE_VALUES!r}"
    )
