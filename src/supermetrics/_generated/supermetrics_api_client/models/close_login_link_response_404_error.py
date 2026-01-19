from enum import Enum

class CloseLoginLinkResponse404Error(str, Enum):
    LINK_NOT_FOUND = "LINK_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
