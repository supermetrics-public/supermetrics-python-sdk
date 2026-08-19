from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_details import QueryDetails


T = TypeVar("T", bound="TransferRunDetail")


@_attrs_define
class TransferRunDetail:
    """Detail view of a single transfer run.

    Attributes:
        id (int): Unique identifier of the transfer run Example: 12345.
        status (str): Current status of the transfer run Example: COMPLETED.
        query_details (list[QueryDetails]): Per-query execution details for the transfer run
        external_id (str): External identifier of the transfer run Example: ext-12345.
        message (str): Status message or error description for the transfer run
        started_time (datetime.datetime | None | Unset): Timestamp when the transfer run started processing (ISO 8601
            format) Example: 2024-01-15T10:00:00Z.
        ended_time (datetime.datetime | None | Unset): Timestamp when the transfer run finished processing (ISO 8601
            format) Example: 2024-01-15T10:05:30Z.
        created_time (datetime.datetime | None | Unset): Timestamp when the transfer run was created (ISO 8601 format)
            Example: 2024-01-15T09:55:00Z.
        queued_time (datetime.datetime | None | Unset): Timestamp when the transfer run was queued for processing (ISO
            8601 format) Example: 2024-01-15T09:58:00Z.
        failed_query_amount (int | None | Unset): Number of queries that failed during the transfer run
        total_duration (float | None | Unset): Sum of all query durations in seconds Example: 330.5.
        total_rows (int | None | Unset): Total number of rows processed during the transfer run Example: 15000.
        query_amount (int | None | Unset): Total number of queries executed during the transfer run Example: 5.
        data_date (datetime.date | None | Unset): The data date this transfer run covers Example: 2024-01-15.
    """

    id: int
    status: str
    query_details: list[QueryDetails]
    external_id: str
    message: str
    started_time: datetime.datetime | None | Unset = UNSET
    ended_time: datetime.datetime | None | Unset = UNSET
    created_time: datetime.datetime | None | Unset = UNSET
    queued_time: datetime.datetime | None | Unset = UNSET
    failed_query_amount: int | None | Unset = UNSET
    total_duration: float | None | Unset = UNSET
    total_rows: int | None | Unset = UNSET
    query_amount: int | None | Unset = UNSET
    data_date: datetime.date | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status

        query_details = []
        for query_details_item_data in self.query_details:
            query_details_item = query_details_item_data.to_dict()
            query_details.append(query_details_item)

        external_id = self.external_id

        message = self.message

        started_time: None | str | Unset
        if isinstance(self.started_time, Unset):
            started_time = UNSET
        elif isinstance(self.started_time, datetime.datetime):
            started_time = self.started_time.isoformat()
        else:
            started_time = self.started_time

        ended_time: None | str | Unset
        if isinstance(self.ended_time, Unset):
            ended_time = UNSET
        elif isinstance(self.ended_time, datetime.datetime):
            ended_time = self.ended_time.isoformat()
        else:
            ended_time = self.ended_time

        created_time: None | str | Unset
        if isinstance(self.created_time, Unset):
            created_time = UNSET
        elif isinstance(self.created_time, datetime.datetime):
            created_time = self.created_time.isoformat()
        else:
            created_time = self.created_time

        queued_time: None | str | Unset
        if isinstance(self.queued_time, Unset):
            queued_time = UNSET
        elif isinstance(self.queued_time, datetime.datetime):
            queued_time = self.queued_time.isoformat()
        else:
            queued_time = self.queued_time

        failed_query_amount: int | None | Unset
        if isinstance(self.failed_query_amount, Unset):
            failed_query_amount = UNSET
        else:
            failed_query_amount = self.failed_query_amount

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

        query_amount: int | None | Unset
        if isinstance(self.query_amount, Unset):
            query_amount = UNSET
        else:
            query_amount = self.query_amount

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
                "query_details": query_details,
                "external_id": external_id,
                "message": message,
            }
        )
        if started_time is not UNSET:
            field_dict["started_time"] = started_time
        if ended_time is not UNSET:
            field_dict["ended_time"] = ended_time
        if created_time is not UNSET:
            field_dict["created_time"] = created_time
        if queued_time is not UNSET:
            field_dict["queued_time"] = queued_time
        if failed_query_amount is not UNSET:
            field_dict["failed_query_amount"] = failed_query_amount
        if total_duration is not UNSET:
            field_dict["total_duration"] = total_duration
        if total_rows is not UNSET:
            field_dict["total_rows"] = total_rows
        if query_amount is not UNSET:
            field_dict["query_amount"] = query_amount
        if data_date is not UNSET:
            field_dict["data_date"] = data_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_details import QueryDetails

        d = dict(src_dict)
        id = d.pop("id")

        status = d.pop("status")

        query_details = []
        _query_details = d.pop("query_details")
        for query_details_item_data in _query_details:
            query_details_item = QueryDetails.from_dict(query_details_item_data)

            query_details.append(query_details_item)

        external_id = d.pop("external_id")

        message = d.pop("message")

        def _parse_started_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_time_type_0 = datetime.datetime.fromisoformat(data)

                return started_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        started_time = _parse_started_time(d.pop("started_time", UNSET))

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

        def _parse_queued_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                queued_time_type_0 = datetime.datetime.fromisoformat(data)

                return queued_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        queued_time = _parse_queued_time(d.pop("queued_time", UNSET))

        def _parse_failed_query_amount(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        failed_query_amount = _parse_failed_query_amount(d.pop("failed_query_amount", UNSET))

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

        def _parse_query_amount(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        query_amount = _parse_query_amount(d.pop("query_amount", UNSET))

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

        transfer_run_detail = cls(
            id=id,
            status=status,
            query_details=query_details,
            external_id=external_id,
            message=message,
            started_time=started_time,
            ended_time=ended_time,
            created_time=created_time,
            queued_time=queued_time,
            failed_query_amount=failed_query_amount,
            total_duration=total_duration,
            total_rows=total_rows,
            query_amount=query_amount,
            data_date=data_date,
        )

        transfer_run_detail.additional_properties = d
        return transfer_run_detail

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
