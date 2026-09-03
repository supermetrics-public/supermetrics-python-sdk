from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batch_update_destinations_response_200_data_results_item_status import (
    BatchUpdateDestinationsResponse200DataResultsItemStatus,
    check_batch_update_destinations_response_200_data_results_item_status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchUpdateDestinationsResponse200DataResultsItem")


@_attrs_define
class BatchUpdateDestinationsResponse200DataResultsItem:
    """
    Attributes:
        destination_id (int):
        status (BatchUpdateDestinationsResponse200DataResultsItemStatus):
        error_code (str | Unset): Error code identifying the failure reason. Only present when status is error.
        message (str | Unset): Human-readable error description. Only present when status is error.
    """

    destination_id: int
    status: BatchUpdateDestinationsResponse200DataResultsItemStatus
    error_code: str | Unset = UNSET
    message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_id = self.destination_id

        status: str = self.status

        error_code = self.error_code

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destination_id": destination_id,
                "status": status,
            }
        )
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destination_id = d.pop("destination_id")

        status = check_batch_update_destinations_response_200_data_results_item_status(d.pop("status"))

        error_code = d.pop("error_code", UNSET)

        message = d.pop("message", UNSET)

        batch_update_destinations_response_200_data_results_item = cls(
            destination_id=destination_id,
            status=status,
            error_code=error_code,
            message=message,
        )

        batch_update_destinations_response_200_data_results_item.additional_properties = d
        return batch_update_destinations_response_200_data_results_item

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
