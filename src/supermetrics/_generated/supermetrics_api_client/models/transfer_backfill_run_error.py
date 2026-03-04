from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="TransferBackfillRunError")


@_attrs_define
class TransferBackfillRunError:
    """
    Attributes:
        transfer_run_date (datetime.date): The date of the transfer run that failed Example: 2024-01-15.
        error (str): Error message describing what went wrong Example: Connection timeout to data source.
    """

    transfer_run_date: datetime.date
    error: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transfer_run_date = self.transfer_run_date.isoformat()

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transfer_run_date": transfer_run_date,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transfer_run_date = isoparse(d.pop("transfer_run_date")).date()

        error = d.pop("error")

        transfer_backfill_run_error = cls(
            transfer_run_date=transfer_run_date,
            error=error,
        )

        transfer_backfill_run_error.additional_properties = d
        return transfer_backfill_run_error

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
