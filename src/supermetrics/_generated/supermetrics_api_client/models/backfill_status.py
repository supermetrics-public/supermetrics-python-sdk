from enum import Enum


class BackfillStatus(str, Enum):
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"

    def __str__(self) -> str:
        return str(self.value)
