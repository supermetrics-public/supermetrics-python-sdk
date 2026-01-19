from enum import Enum

class GetDataSourceLoginResponse404Error(str, Enum):
    LOGIN_NOT_FOUND = "LOGIN_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
