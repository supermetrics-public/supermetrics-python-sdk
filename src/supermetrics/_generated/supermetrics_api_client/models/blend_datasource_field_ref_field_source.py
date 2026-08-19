from typing import Literal

BlendDatasourceFieldRefFieldSource = Literal["data_source_account_custom", "standard", "transformation"]

BLEND_DATASOURCE_FIELD_REF_FIELD_SOURCE_VALUES: set[BlendDatasourceFieldRefFieldSource] = {
    "data_source_account_custom",
    "standard",
    "transformation",
}


def check_blend_datasource_field_ref_field_source(value: str) -> BlendDatasourceFieldRefFieldSource:
    if value in BLEND_DATASOURCE_FIELD_REF_FIELD_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_DATASOURCE_FIELD_REF_FIELD_SOURCE_VALUES!r}")
