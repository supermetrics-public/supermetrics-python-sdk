from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.backfill_status import BackfillStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_backfill_run_error import TransferBackfillRunError


T = TypeVar("T", bound="Backfill")


@_attrs_define
class Backfill:
    """
    Attributes:
        transfer_backfill_id (int): Unique identifier of the backfill Example: 12345.
        transfer_id (int): ID of the transfer this backfill belongs to Example: 456789.
        range_start_date (datetime.date): Start date of the backfill range Example: 2024-01-01.
        range_end_date (datetime.date): End date of the backfill range Example: 2024-01-31.
        created_time (datetime.datetime): Timestamp when the backfill was created (ISO 8601 format) Example:
            2024-02-01T09:00:00Z.
        created_user_id (int): ID of the user who created the backfill Example: 789.
        status (BackfillStatus): Current status of the backfill Example: RUNNING.
        transfer_runs_total (int): Total number of transfer runs created for this backfill Example: 31.
        transfer_runs_created (int): Number of transfer runs that have been created Example: 31.
        transfer_runs_completed (int): Number of transfer runs that have completed successfully Example: 25.
        transfer_runs_failed (int): Number of transfer runs that have failed Example: 2.
        removed_time (datetime.datetime | None | Unset): Timestamp when the backfill was cancelled/removed (ISO 8601
            format) Example: 2024-02-01T15:00:00Z.
        removed_user_id (int | None | Unset): ID of the user who cancelled/removed the backfill Example: 790.
        start_time (datetime.datetime | None | Unset): Timestamp when the backfill processing started (ISO 8601 format)
            Example: 2024-02-01T10:00:00Z.
        end_time (datetime.datetime | None | Unset): Timestamp when the backfill processing completed (ISO 8601 format)
            Example: 2024-02-01T12:30:00Z.
        error_report (list[TransferBackfillRunError] | Unset): List of errors that occurred during backfill processing
            (empty array if no errors)
    """

    transfer_backfill_id: int
    transfer_id: int
    range_start_date: datetime.date
    range_end_date: datetime.date
    created_time: datetime.datetime
    created_user_id: int
    status: BackfillStatus
    transfer_runs_total: int
    transfer_runs_created: int
    transfer_runs_completed: int
    transfer_runs_failed: int
    removed_time: datetime.datetime | None | Unset = UNSET
    removed_user_id: int | None | Unset = UNSET
    start_time: datetime.datetime | None | Unset = UNSET
    end_time: datetime.datetime | None | Unset = UNSET
    error_report: list[TransferBackfillRunError] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transfer_backfill_id = self.transfer_backfill_id

        transfer_id = self.transfer_id

        range_start_date = self.range_start_date.isoformat()

        range_end_date = self.range_end_date.isoformat()

        created_time = self.created_time.isoformat()

        created_user_id = self.created_user_id

        status = self.status.value

        transfer_runs_total = self.transfer_runs_total

        transfer_runs_created = self.transfer_runs_created

        transfer_runs_completed = self.transfer_runs_completed

        transfer_runs_failed = self.transfer_runs_failed

        removed_time: None | str | Unset
        if isinstance(self.removed_time, Unset):
            removed_time = UNSET
        elif isinstance(self.removed_time, datetime.datetime):
            removed_time = self.removed_time.isoformat()
        else:
            removed_time = self.removed_time

        removed_user_id: int | None | Unset
        if isinstance(self.removed_user_id, Unset):
            removed_user_id = UNSET
        else:
            removed_user_id = self.removed_user_id

        start_time: None | str | Unset
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        end_time: None | str | Unset
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        error_report: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.error_report, Unset):
            error_report = []
            for error_report_item_data in self.error_report:
                error_report_item = error_report_item_data.to_dict()
                error_report.append(error_report_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transfer_backfill_id": transfer_backfill_id,
                "transfer_id": transfer_id,
                "range_start_date": range_start_date,
                "range_end_date": range_end_date,
                "created_time": created_time,
                "created_user_id": created_user_id,
                "status": status,
                "transfer_runs_total": transfer_runs_total,
                "transfer_runs_created": transfer_runs_created,
                "transfer_runs_completed": transfer_runs_completed,
                "transfer_runs_failed": transfer_runs_failed,
            }
        )
        if removed_time is not UNSET:
            field_dict["removed_time"] = removed_time
        if removed_user_id is not UNSET:
            field_dict["removed_user_id"] = removed_user_id
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if error_report is not UNSET:
            field_dict["error_report"] = error_report

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_backfill_run_error import TransferBackfillRunError

        d = dict(src_dict)
        transfer_backfill_id = d.pop("transfer_backfill_id")

        transfer_id = d.pop("transfer_id")

        range_start_date = isoparse(d.pop("range_start_date")).date()

        range_end_date = isoparse(d.pop("range_end_date")).date()

        created_time = isoparse(d.pop("created_time"))

        created_user_id = d.pop("created_user_id")

        status = BackfillStatus(d.pop("status"))

        transfer_runs_total = d.pop("transfer_runs_total")

        transfer_runs_created = d.pop("transfer_runs_created")

        transfer_runs_completed = d.pop("transfer_runs_completed")

        transfer_runs_failed = d.pop("transfer_runs_failed")

        def _parse_removed_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                removed_time_type_0 = isoparse(data)

                return removed_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        removed_time = _parse_removed_time(d.pop("removed_time", UNSET))

        def _parse_removed_user_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        removed_user_id = _parse_removed_user_id(d.pop("removed_user_id", UNSET))

        def _parse_start_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        _error_report = d.pop("error_report", UNSET)
        error_report: list[TransferBackfillRunError] | Unset = UNSET
        if _error_report is not UNSET:
            error_report = []
            for error_report_item_data in _error_report:
                error_report_item = TransferBackfillRunError.from_dict(error_report_item_data)

                error_report.append(error_report_item)

        backfill = cls(
            transfer_backfill_id=transfer_backfill_id,
            transfer_id=transfer_id,
            range_start_date=range_start_date,
            range_end_date=range_end_date,
            created_time=created_time,
            created_user_id=created_user_id,
            status=status,
            transfer_runs_total=transfer_runs_total,
            transfer_runs_created=transfer_runs_created,
            transfer_runs_completed=transfer_runs_completed,
            transfer_runs_failed=transfer_runs_failed,
            removed_time=removed_time,
            removed_user_id=removed_user_id,
            start_time=start_time,
            end_time=end_time,
            error_report=error_report,
        )

        backfill.additional_properties = d
        return backfill

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
