from enum import Enum

class CreateLoginLinkResponse403Error(str, Enum):
    LINK_LIMIT_EXCEEDED = "LINK_LIMIT_EXCEEDED"

    def __str__(self) -> str:
        return str(self.value)
