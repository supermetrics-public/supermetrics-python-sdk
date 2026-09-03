from typing import Literal

TeamSettingsResponseDataType = Literal["team_settings"]

TEAM_SETTINGS_RESPONSE_DATA_TYPE_VALUES: set[TeamSettingsResponseDataType] = {
    "team_settings",
}


def check_team_settings_response_data_type(value: str) -> TeamSettingsResponseDataType:
    if value in TEAM_SETTINGS_RESPONSE_DATA_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TEAM_SETTINGS_RESPONSE_DATA_TYPE_VALUES!r}")
