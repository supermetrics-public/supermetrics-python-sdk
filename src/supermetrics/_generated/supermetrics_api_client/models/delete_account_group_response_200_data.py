from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteAccountGroupResponse200Data")


@_attrs_define
class DeleteAccountGroupResponse200Data:
    """
    Attributes:
        result (bool | Unset): True when the account tag was deleted; false when no tag with that name existed Example:
            True.
    """

    result: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        result = self.result

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        result = d.pop("result", UNSET)

        delete_account_group_response_200_data = cls(
            result=result,
        )

        return delete_account_group_response_200_data
