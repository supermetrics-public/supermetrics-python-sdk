from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batch_create_transfers_response_200_data_results_item_status import (
    BatchCreateTransfersResponse200DataResultsItemStatus,
    check_batch_create_transfers_response_200_data_results_item_status,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_create_transfers_response_200_data_results_item_validation_errors_item import (
        BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem,
    )


T = TypeVar("T", bound="BatchCreateTransfersResponse200DataResultsItem")


@_attrs_define
class BatchCreateTransfersResponse200DataResultsItem:
    """
    Attributes:
        index (int): Zero-based position in the input array
        status (BatchCreateTransfersResponse200DataResultsItemStatus):
        transfer_id (int | Unset): ID of the created transfer (present on success)
        transfer_name (str | Unset): Display name of the created transfer (present on success)
        error_code (str | Unset): Machine-readable error identifier (present on error).
            Possible values: INVALID_ITEM_DATA, DWH_INVALID_TRANSFER_SETUP_DATA,
            DWH_TRANSFER_CREATE_FAILED, DWH_BATCH_CREATE_DUPLICATE_CONFIGURATION
        message (str | Unset): Human-readable error description (present on error)
        validation_errors (list[BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem] | Unset): Field-
            level validation details (present when error_code is DWH_INVALID_TRANSFER_SETUP_DATA)
    """

    index: int
    status: BatchCreateTransfersResponse200DataResultsItemStatus
    transfer_id: int | Unset = UNSET
    transfer_name: str | Unset = UNSET
    error_code: str | Unset = UNSET
    message: str | Unset = UNSET
    validation_errors: list[BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        status: str = self.status

        transfer_id = self.transfer_id

        transfer_name = self.transfer_name

        error_code = self.error_code

        message = self.message

        validation_errors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.validation_errors, Unset):
            validation_errors = []
            for validation_errors_item_data in self.validation_errors:
                validation_errors_item = validation_errors_item_data.to_dict()
                validation_errors.append(validation_errors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
                "status": status,
            }
        )
        if transfer_id is not UNSET:
            field_dict["transfer_id"] = transfer_id
        if transfer_name is not UNSET:
            field_dict["transfer_name"] = transfer_name
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if message is not UNSET:
            field_dict["message"] = message
        if validation_errors is not UNSET:
            field_dict["validation_errors"] = validation_errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_create_transfers_response_200_data_results_item_validation_errors_item import (
            BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem,
        )

        d = dict(src_dict)
        index = d.pop("index")

        status = check_batch_create_transfers_response_200_data_results_item_status(d.pop("status"))

        transfer_id = d.pop("transfer_id", UNSET)

        transfer_name = d.pop("transfer_name", UNSET)

        error_code = d.pop("error_code", UNSET)

        message = d.pop("message", UNSET)

        _validation_errors = d.pop("validation_errors", UNSET)
        validation_errors: list[BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem] | Unset = UNSET
        if _validation_errors is not UNSET:
            validation_errors = []
            for validation_errors_item_data in _validation_errors:
                validation_errors_item = BatchCreateTransfersResponse200DataResultsItemValidationErrorsItem.from_dict(
                    validation_errors_item_data
                )

                validation_errors.append(validation_errors_item)

        batch_create_transfers_response_200_data_results_item = cls(
            index=index,
            status=status,
            transfer_id=transfer_id,
            transfer_name=transfer_name,
            error_code=error_code,
            message=message,
            validation_errors=validation_errors,
        )

        batch_create_transfers_response_200_data_results_item.additional_properties = d
        return batch_create_transfers_response_200_data_results_item

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
