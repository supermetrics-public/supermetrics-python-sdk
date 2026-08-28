from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.clone_transfer_body_schedule_item_run_interval import (
    CloneTransferBodyScheduleItemRunInterval,
    check_clone_transfer_body_schedule_item_run_interval,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CloneTransferBodyScheduleItem")


@_attrs_define
class CloneTransferBodyScheduleItem:
    """
    Attributes:
        run_interval (CloneTransferBodyScheduleItemRunInterval):
        refresh_window (int):
        run_hour (int | Unset): Hour of day to run (UTC). Required for daily, weekly, and monthly intervals.
        run_weekday (int | Unset): Day of week (1=Monday, 7=Sunday). Required for weekly interval.
        run_day (int | Unset): Day of month. Required for monthly interval.
    """

    run_interval: CloneTransferBodyScheduleItemRunInterval
    refresh_window: int
    run_hour: int | Unset = UNSET
    run_weekday: int | Unset = UNSET
    run_day: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_interval: str = self.run_interval

        refresh_window = self.refresh_window

        run_hour = self.run_hour

        run_weekday = self.run_weekday

        run_day = self.run_day

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "run_interval": run_interval,
                "refresh_window": refresh_window,
            }
        )
        if run_hour is not UNSET:
            field_dict["run_hour"] = run_hour
        if run_weekday is not UNSET:
            field_dict["run_weekday"] = run_weekday
        if run_day is not UNSET:
            field_dict["run_day"] = run_day

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_interval = check_clone_transfer_body_schedule_item_run_interval(d.pop("run_interval"))

        refresh_window = d.pop("refresh_window")

        run_hour = d.pop("run_hour", UNSET)

        run_weekday = d.pop("run_weekday", UNSET)

        run_day = d.pop("run_day", UNSET)

        clone_transfer_body_schedule_item = cls(
            run_interval=run_interval,
            refresh_window=refresh_window,
            run_hour=run_hour,
            run_weekday=run_weekday,
            run_day=run_day,
        )

        clone_transfer_body_schedule_item.additional_properties = d
        return clone_transfer_body_schedule_item

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
