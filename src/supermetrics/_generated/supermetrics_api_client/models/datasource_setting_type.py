from typing import Literal, cast

DatasourceSettingType = Literal["checkbox", "combobox", "none", "radio", "select", "text", "textarea"]

DATASOURCE_SETTING_TYPE_VALUES: set[DatasourceSettingType] = {
    "checkbox",
    "combobox",
    "none",
    "radio",
    "select",
    "text",
    "textarea",
}


def check_datasource_setting_type(value: str) -> DatasourceSettingType:
    if value in DATASOURCE_SETTING_TYPE_VALUES:
        return cast(DatasourceSettingType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASOURCE_SETTING_TYPE_VALUES!r}")
