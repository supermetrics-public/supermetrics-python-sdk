from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ActionResult")


@_attrs_define
class ActionResult:
    """Result of a workspace action

    Attributes:
        result (bool): Whether the action completed successfully Example: True.
    """

    result: bool

    def to_dict(self) -> dict[str, Any]:
        result = self.result

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        result = d.pop("result")

        action_result = cls(
            result=result,
        )

        return action_result
