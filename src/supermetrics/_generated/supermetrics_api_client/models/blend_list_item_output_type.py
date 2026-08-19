from typing import Literal

BlendListItemOutputType = Literal["join", "union"]

BLEND_LIST_ITEM_OUTPUT_TYPE_VALUES: set[BlendListItemOutputType] = {
    "join",
    "union",
}


def check_blend_list_item_output_type(value: str) -> BlendListItemOutputType:
    if value in BLEND_LIST_ITEM_OUTPUT_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BLEND_LIST_ITEM_OUTPUT_TYPE_VALUES!r}")
