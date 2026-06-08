from typing import Literal, cast

DataSourceLoginType = Literal["ds_login"]

DATA_SOURCE_LOGIN_TYPE_VALUES: set[DataSourceLoginType] = {
    "ds_login",
}


def check_data_source_login_type(value: str) -> DataSourceLoginType:
    if value in DATA_SOURCE_LOGIN_TYPE_VALUES:
        return cast(DataSourceLoginType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_SOURCE_LOGIN_TYPE_VALUES!r}")
