from enum import Enum


class DatasourceDetailsStatus(str, Enum):
    EARLY_ACCESS = "Early access"
    RELEASED = "Released"

    def __str__(self) -> str:
        return str(self.value)
