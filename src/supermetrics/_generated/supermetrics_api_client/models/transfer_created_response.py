from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransferCreatedResponse")


@_attrs_define
class TransferCreatedResponse:
    """Response from creating a transfer

    Attributes:
        transfer_id (int | Unset): The ID of the created transfer Example: 36091.
        transfer_name (str | Unset): The display name of the created transfer Example: AW enhanced 2022-11-17.
    """

    transfer_id: int | Unset = UNSET
    transfer_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transfer_id = self.transfer_id

        transfer_name = self.transfer_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transfer_id is not UNSET:
            field_dict["transfer_id"] = transfer_id
        if transfer_name is not UNSET:
            field_dict["transfer_name"] = transfer_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transfer_id = d.pop("transfer_id", UNSET)

        transfer_name = d.pop("transfer_name", UNSET)

        transfer_created_response = cls(
            transfer_id=transfer_id,
            transfer_name=transfer_name,
        )

        transfer_created_response.additional_properties = d
        return transfer_created_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
