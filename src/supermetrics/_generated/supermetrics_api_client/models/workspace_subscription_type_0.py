from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceSubscriptionType0")


@_attrs_define
class WorkspaceSubscriptionType0:
    """Subscription details of the workspace, or null when none is active

    Attributes:
        end_date (datetime.date | Unset): End date of the subscription Example: 2026-12-31.
        assigned_seats (int | Unset): Number of assigned seats Example: 5.
        total_seats (int | Unset): Total number of seats Example: 10.
        destinations (list[str] | Unset): Destinations enabled by the subscription
    """

    end_date: datetime.date | Unset = UNSET
    assigned_seats: int | Unset = UNSET
    total_seats: int | Unset = UNSET
    destinations: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end_date: str | Unset = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        assigned_seats = self.assigned_seats

        total_seats = self.total_seats

        destinations: list[str] | Unset = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = self.destinations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if assigned_seats is not UNSET:
            field_dict["assigned_seats"] = assigned_seats
        if total_seats is not UNSET:
            field_dict["total_seats"] = total_seats
        if destinations is not UNSET:
            field_dict["destinations"] = destinations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _end_date = d.pop("end_date", UNSET)
        end_date: datetime.date | Unset
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = datetime.date.fromisoformat(_end_date)

        assigned_seats = d.pop("assigned_seats", UNSET)

        total_seats = d.pop("total_seats", UNSET)

        destinations = cast(list[str], d.pop("destinations", UNSET))

        workspace_subscription_type_0 = cls(
            end_date=end_date,
            assigned_seats=assigned_seats,
            total_seats=total_seats,
            destinations=destinations,
        )

        workspace_subscription_type_0.additional_properties = d
        return workspace_subscription_type_0

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
