from enum import Enum


class DatasourceSettingType(str, Enum):
    CHECKBOX = "checkbox"
    COMBOBOX = "combobox"
    NONE = "none"
    RADIO = "radio"
    SELECT = "select"
    TEXT = "text"
    TEXTAREA = "textarea"

    def __str__(self) -> str:
        return str(self.value)
