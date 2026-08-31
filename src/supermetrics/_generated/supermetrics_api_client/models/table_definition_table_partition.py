from typing import Literal

TableDefinitionTablePartition = Literal["date", "none"]

TABLE_DEFINITION_TABLE_PARTITION_VALUES: set[TableDefinitionTablePartition] = {
    "date",
    "none",
}


def check_table_definition_table_partition(value: str) -> TableDefinitionTablePartition:
    if value in TABLE_DEFINITION_TABLE_PARTITION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TABLE_DEFINITION_TABLE_PARTITION_VALUES!r}")
