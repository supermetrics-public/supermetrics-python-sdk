from enum import Enum

class GetDataSourceLoginResponse500Error(str, Enum):
    LOGIN_SEARCH_FAILED = "LOGIN_SEARCH_FAILED"

    def __str__(self) -> str:
        return str(self.value)
