from enum import Enum

class DataSourceType(str, Enum):
    DS = "ds"

    def __str__(self) -> str:
        return str(self.value)
