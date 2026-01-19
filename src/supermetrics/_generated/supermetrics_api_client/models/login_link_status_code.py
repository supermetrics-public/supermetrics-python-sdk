from enum import Enum

class LoginLinkStatusCode(str, Enum):
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"
    OPEN = "OPEN"

    def __str__(self) -> str:
        return str(self.value)
