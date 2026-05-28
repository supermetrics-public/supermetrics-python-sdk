from typing import Literal, cast

DatasourceDetailsStatus = Literal["Early access", "Released"]

DATASOURCE_DETAILS_STATUS_VALUES: set[DatasourceDetailsStatus] = {
    "Early access",
    "Released",
}


def check_datasource_details_status(value: str) -> DatasourceDetailsStatus:
    if value in DATASOURCE_DETAILS_STATUS_VALUES:
        return cast(DatasourceDetailsStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASOURCE_DETAILS_STATUS_VALUES!r}")
