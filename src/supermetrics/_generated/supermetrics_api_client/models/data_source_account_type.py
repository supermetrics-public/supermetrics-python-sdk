from typing import Literal

DataSourceAccountType = Literal["ds_account"]

DATA_SOURCE_ACCOUNT_TYPE_VALUES: set[DataSourceAccountType] = {
    "ds_account",
}


def check_data_source_account_type(value: str) -> DataSourceAccountType:
    if value in DATA_SOURCE_ACCOUNT_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_SOURCE_ACCOUNT_TYPE_VALUES!r}")
