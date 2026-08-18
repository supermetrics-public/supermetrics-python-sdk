from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogEntry")


@_attrs_define
class LogEntry:
    """A connector execution log entry.

    Attributes:
        id (str | Unset): Log entry identifier Example: 123-foo.
        log_time (datetime.datetime | Unset): Timestamp of the log entry Example: 2025-01-01T00:00:00Z.
        status (int | None | Unset): HTTP status code Example: 200.
        event (None | str | Unset): Event type Example: auth.token.refresh.
        request (None | str | Unset): Request method and path Example: POST /api/oauth/token_refresh.
        duration_ms (int | None | Unset): Request duration in milliseconds Example: 253.
        request_id (None | Unset | UUID): Request tracking identifier
    """

    id: str | Unset = UNSET
    log_time: datetime.datetime | Unset = UNSET
    status: int | None | Unset = UNSET
    event: None | str | Unset = UNSET
    request: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    request_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        log_time: str | Unset = UNSET
        if not isinstance(self.log_time, Unset):
            log_time = self.log_time.isoformat()

        status: int | None | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        event: None | str | Unset
        if isinstance(self.event, Unset):
            event = UNSET
        else:
            event = self.event

        request: None | str | Unset
        if isinstance(self.request, Unset):
            request = UNSET
        else:
            request = self.request

        duration_ms: int | None | Unset
        if isinstance(self.duration_ms, Unset):
            duration_ms = UNSET
        else:
            duration_ms = self.duration_ms

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        elif isinstance(self.request_id, UUID):
            request_id = str(self.request_id)
        else:
            request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if log_time is not UNSET:
            field_dict["log_time"] = log_time
        if status is not UNSET:
            field_dict["status"] = status
        if event is not UNSET:
            field_dict["event"] = event
        if request is not UNSET:
            field_dict["request"] = request
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if request_id is not UNSET:
            field_dict["request_id"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        _log_time = d.pop("log_time", UNSET)
        log_time: datetime.datetime | Unset
        if isinstance(_log_time, Unset):
            log_time = UNSET
        else:
            log_time = isoparse(_log_time)

        def _parse_status(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_event(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        event = _parse_event(d.pop("event", UNSET))

        def _parse_request(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request = _parse_request(d.pop("request", UNSET))

        def _parse_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        duration_ms = _parse_duration_ms(d.pop("duration_ms", UNSET))

        def _parse_request_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                request_id_type_0 = UUID(data)

                return request_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        log_entry = cls(
            id=id,
            log_time=log_time,
            status=status,
            event=event,
            request=request,
            duration_ms=duration_ms,
            request_id=request_id,
        )

        log_entry.additional_properties = d
        return log_entry

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
