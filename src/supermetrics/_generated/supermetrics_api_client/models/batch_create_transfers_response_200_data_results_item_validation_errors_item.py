from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem")


@_attrs_define
class BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem:
    """
    Attributes:
        field_id (str): The field that failed validation
        error_code (str): Validation error code (values originate from the validation framework, not an enum-stable set)
        message (str): Human-readable validation error message
    """

    field_id: str
    error_code: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        error_code = self.error_code

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field_id": field_id,
                "error_code": error_code,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field_id = d.pop("field_id")

        error_code = d.pop("error_code")

        message = d.pop("message")

        batch_create_transfers_response_200_data_results_item_validation_errors_item = cls(
            field_id=field_id,
            error_code=error_code,
            message=message,
        )

        batch_create_transfers_response_200_data_results_item_validation_errors_item.additional_properties = d
        return batch_create_transfers_response_200_data_results_item_validation_errors_item

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
