from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transfer_run_item_type import TransferRunItemType, check_transfer_run_item_type
from ..types import UNSET, Unset

T = TypeVar("T", bound="TransferRunItem")


@_attrs_define
class TransferRunItem:
    """List item view of a transfer run.

    Attributes:
        id (int): Unique identifier of the transfer run Example: 12345.
        status (str): Current status of the transfer run Example: COMPLETED.
        type_ (TransferRunItemType): Type of the transfer run Example: Recurring.
        message (str): Status message or error description for the transfer run
        created_time (datetime.datetime | None | Unset): Timestamp when the transfer run was created (ISO 8601 format)
            Example: 2024-01-15T09:55:00Z.
        ended_time (datetime.datetime | None | Unset): Timestamp when the transfer run finished processing (ISO 8601
            format) Example: 2024-01-15T10:05:30Z.
        total_duration (float | None | Unset): Sum of all query durations in seconds Example: 330.5.
        total_rows (int | None | Unset): Total number of rows processed during the transfer run Example: 15000.
        data_date (datetime.date | None | Unset): The data date this transfer run covers Example: 2024-01-15.
    """

    id: int
    status: str
    type_: TransferRunItemType
    message: str
    created_time: datetime.datetime | None | Unset = UNSET
    ended_time: datetime.datetime | None | Unset = UNSET
    total_duration: float | None | Unset = UNSET
    total_rows: int | None | Unset = UNSET
    data_date: datetime.date | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status

        type_: str = self.type_

        message = self.message

        created_time: None | str | Unset
        if isinstance(self.created_time, Unset):
            created_time = UNSET
        elif isinstance(self.created_time, datetime.datetime):
            created_time = self.created_time.isoformat()
        else:
            created_time = self.created_time

        ended_time: None | str | Unset
        if isinstance(self.ended_time, Unset):
            ended_time = UNSET
        elif isinstance(self.ended_time, datetime.datetime):
            ended_time = self.ended_time.isoformat()
        else:
            ended_time = self.ended_time

        total_duration: float | None | Unset
        if isinstance(self.total_duration, Unset):
            total_duration = UNSET
        else:
            total_duration = self.total_duration

        total_rows: int | None | Unset
        if isinstance(self.total_rows, Unset):
            total_rows = UNSET
        else:
            total_rows = self.total_rows

        data_date: None | str | Unset
        if isinstance(self.data_date, Unset):
            data_date = UNSET
        elif isinstance(self.data_date, datetime.date):
            data_date = self.data_date.isoformat()
        else:
            data_date = self.data_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "type": type_,
                "message": message,
            }
        )
        if created_time is not UNSET:
            field_dict["created_time"] = created_time
        if ended_time is not UNSET:
            field_dict["ended_time"] = ended_time
        if total_duration is not UNSET:
            field_dict["total_duration"] = total_duration
        if total_rows is not UNSET:
            field_dict["total_rows"] = total_rows
        if data_date is not UNSET:
            field_dict["data_date"] = data_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = d.pop("status")

        type_ = check_transfer_run_item_type(d.pop("type"))

        message = d.pop("message")

        def _parse_created_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_time_type_0 = datetime.datetime.fromisoformat(data)

                return created_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_time = _parse_created_time(d.pop("created_time", UNSET))

        def _parse_ended_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_time_type_0 = datetime.datetime.fromisoformat(data)

                return ended_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        ended_time = _parse_ended_time(d.pop("ended_time", UNSET))

        def _parse_total_duration(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        total_duration = _parse_total_duration(d.pop("total_duration", UNSET))

        def _parse_total_rows(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_rows = _parse_total_rows(d.pop("total_rows", UNSET))

        def _parse_data_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_date_type_0 = datetime.date.fromisoformat(data)

                return data_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        data_date = _parse_data_date(d.pop("data_date", UNSET))

        transfer_run_item = cls(
            id=id,
            status=status,
            type_=type_,
            message=message,
            created_time=created_time,
            ended_time=ended_time,
            total_duration=total_duration,
            total_rows=total_rows,
            data_date=data_date,
        )

        transfer_run_item.additional_properties = d
        return transfer_run_item

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
