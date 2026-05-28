from typing import Literal, cast

DatasourceSettingContext = Literal["options", "reportConfiguration"]

DATASOURCE_SETTING_CONTEXT_VALUES: set[DatasourceSettingContext] = {
    "options",
    "reportConfiguration",
}


def check_datasource_setting_context(value: str) -> DatasourceSettingContext:
    if value in DATASOURCE_SETTING_CONTEXT_VALUES:
        return cast(DatasourceSettingContext, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASOURCE_SETTING_CONTEXT_VALUES!r}")
