from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delete_account_group_response_200_data import DeleteAccountGroupResponse200Data


T = TypeVar("T", bound="DeleteAccountGroupResponse200")


@_attrs_define
class DeleteAccountGroupResponse200:
    """
    Attributes:
        data (DeleteAccountGroupResponse200Data | Unset):
    """

    data: DeleteAccountGroupResponse200Data | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delete_account_group_response_200_data import DeleteAccountGroupResponse200Data

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: DeleteAccountGroupResponse200Data | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = DeleteAccountGroupResponse200Data.from_dict(_data)

        delete_account_group_response_200 = cls(
            data=data,
        )

        return delete_account_group_response_200
