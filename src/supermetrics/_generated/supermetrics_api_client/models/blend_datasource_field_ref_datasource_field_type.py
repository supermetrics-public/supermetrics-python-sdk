from typing import Literal

BlendDatasourceFieldRefDatasourceFieldType = Literal["dim", "met"]

BLEND_DATASOURCE_FIELD_REF_DATASOURCE_FIELD_TYPE_VALUES: set[BlendDatasourceFieldRefDatasourceFieldType] = {
    "dim",
    "met",
}


def check_blend_datasource_field_ref_datasource_field_type(value: str) -> BlendDatasourceFieldRefDatasourceFieldType:
    if value in BLEND_DATASOURCE_FIELD_REF_DATASOURCE_FIELD_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BLEND_DATASOURCE_FIELD_REF_DATASOURCE_FIELD_TYPE_VALUES!r}"
    )
