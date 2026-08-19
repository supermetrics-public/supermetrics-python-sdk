from typing import Literal

BlendDatasourceFieldRefOutputFieldSource = Literal["data_source_account_custom", "standard", "transformation"]

BLEND_DATASOURCE_FIELD_REF_OUTPUT_FIELD_SOURCE_VALUES: set[BlendDatasourceFieldRefOutputFieldSource] = {
    "data_source_account_custom",
    "standard",
    "transformation",
}


def check_blend_datasource_field_ref_output_field_source(value: str) -> BlendDatasourceFieldRefOutputFieldSource:
    if value in BLEND_DATASOURCE_FIELD_REF_OUTPUT_FIELD_SOURCE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BLEND_DATASOURCE_FIELD_REF_OUTPUT_FIELD_SOURCE_VALUES!r}"
    )
