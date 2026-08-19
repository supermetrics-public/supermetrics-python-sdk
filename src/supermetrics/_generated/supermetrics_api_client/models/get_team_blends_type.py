from typing import Literal

GetTeamBlendsType = Literal["join", "union"]

GET_TEAM_BLENDS_TYPE_VALUES: set[GetTeamBlendsType] = {
    "join",
    "union",
}


def check_get_team_blends_type(value: str) -> GetTeamBlendsType:
    if value in GET_TEAM_BLENDS_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_TEAM_BLENDS_TYPE_VALUES!r}")
