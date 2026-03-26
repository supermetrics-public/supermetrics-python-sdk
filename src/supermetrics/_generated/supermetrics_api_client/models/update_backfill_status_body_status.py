from enum import Enum


class UpdateBackfillStatusBodyStatus(str, Enum):
    CANCELLED = "CANCELLED"

    def __str__(self) -> str:
        return str(self.value)
