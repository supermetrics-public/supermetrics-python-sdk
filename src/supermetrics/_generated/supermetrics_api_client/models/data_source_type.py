from typing import Literal, cast

DataSourceType = Literal["ds"]

DATA_SOURCE_TYPE_VALUES: set[DataSourceType] = {
    "ds",
}


def check_data_source_type(value: str) -> DataSourceType:
    if value in DATA_SOURCE_TYPE_VALUES:
        return cast(DataSourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_SOURCE_TYPE_VALUES!r}")
