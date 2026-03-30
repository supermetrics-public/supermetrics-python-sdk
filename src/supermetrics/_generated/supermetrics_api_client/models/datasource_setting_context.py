from enum import Enum


class DatasourceSettingContext(str, Enum):
    OPTIONS = "options"
    REPORTCONFIGURATION = "reportConfiguration"

    def __str__(self) -> str:
        return str(self.value)
