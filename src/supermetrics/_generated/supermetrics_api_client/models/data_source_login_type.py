from enum import Enum

class DataSourceLoginType(str, Enum):
    DS_LOGIN = "ds_login"

    def __str__(self) -> str:
        return str(self.value)
