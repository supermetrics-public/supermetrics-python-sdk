from enum import Enum

class CloseLoginLinkResponse500Error(str, Enum):
    LINK_UPDATE_FAILED = "LINK_UPDATE_FAILED"

    def __str__(self) -> str:
        return str(self.value)
