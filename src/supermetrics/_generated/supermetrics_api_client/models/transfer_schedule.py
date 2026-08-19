from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transfer_schedule_run_interval import TransferScheduleRunInterval, check_transfer_schedule_run_interval
from ..types import UNSET, Unset

T = TypeVar("T", bound="TransferSchedule")


@_attrs_define
class TransferSchedule:
    """
    Example:
        {'run_interval': 'daily', 'run_hour': 22, 'refresh_window': 1}

    Attributes:
        run_interval (TransferScheduleRunInterval | Unset): Frequency of transfer execution
        run_hour (int | Unset): Hour of day to run (UTC)
        refresh_window (int | Unset): Number of days to refresh
        run_weekday (int | Unset): Day of week to run (1=Monday, 7=Sunday). Required for weekly interval.
        run_day (int | Unset): Day of month to run. Required for monthly interval.
    """

    run_interval: TransferScheduleRunInterval | Unset = UNSET
    run_hour: int | Unset = UNSET
    refresh_window: int | Unset = UNSET
    run_weekday: int | Unset = UNSET
    run_day: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_interval: str | Unset = UNSET
        if not isinstance(self.run_interval, Unset):
            run_interval = self.run_interval

        run_hour = self.run_hour

        refresh_window = self.refresh_window

        run_weekday = self.run_weekday

        run_day = self.run_day

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if run_interval is not UNSET:
            field_dict["run_interval"] = run_interval
        if run_hour is not UNSET:
            field_dict["run_hour"] = run_hour
        if refresh_window is not UNSET:
            field_dict["refresh_window"] = refresh_window
        if run_weekday is not UNSET:
            field_dict["run_weekday"] = run_weekday
        if run_day is not UNSET:
            field_dict["run_day"] = run_day

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _run_interval = d.pop("run_interval", UNSET)
        run_interval: TransferScheduleRunInterval | Unset
        if isinstance(_run_interval, Unset):
            run_interval = UNSET
        else:
            run_interval = check_transfer_schedule_run_interval(_run_interval)

        run_hour = d.pop("run_hour", UNSET)

        refresh_window = d.pop("refresh_window", UNSET)

        run_weekday = d.pop("run_weekday", UNSET)

        run_day = d.pop("run_day", UNSET)

        transfer_schedule = cls(
            run_interval=run_interval,
            run_hour=run_hour,
            refresh_window=refresh_window,
            run_weekday=run_weekday,
            run_day=run_day,
        )

        transfer_schedule.additional_properties = d
        return transfer_schedule

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
