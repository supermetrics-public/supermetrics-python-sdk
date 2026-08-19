from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.change_transfer_state_request_transfer_state import (
    ChangeTransferStateRequestTransferState,
    check_change_transfer_state_request_transfer_state,
)

T = TypeVar("T", bound="ChangeTransferStateRequest")


@_attrs_define
class ChangeTransferStateRequest:
    """
    Attributes:
        transfer_state (ChangeTransferStateRequestTransferState): Action to perform on the transfer state Example:
            pause.
    """

    transfer_state: ChangeTransferStateRequestTransferState

    def to_dict(self) -> dict[str, Any]:
        transfer_state: str = self.transfer_state

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "transfer_state": transfer_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transfer_state = check_change_transfer_state_request_transfer_state(d.pop("transfer_state"))

        change_transfer_state_request = cls(
            transfer_state=transfer_state,
        )

        return change_transfer_state_request
