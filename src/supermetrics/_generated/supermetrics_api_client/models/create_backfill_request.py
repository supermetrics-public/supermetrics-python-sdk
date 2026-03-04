from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CreateBackfillRequest")


@_attrs_define
class CreateBackfillRequest:
    """
    Attributes:
        range_start (datetime.date): Start date of the backfill range (inclusive) Example: 2024-01-01.
        range_end (datetime.date): End date of the backfill range (inclusive) Example: 2024-01-31.
    """

    range_start: datetime.date
    range_end: datetime.date
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        range_start = self.range_start.isoformat()

        range_end = self.range_end.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "range_start": range_start,
                "range_end": range_end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        range_start = isoparse(d.pop("range_start")).date()

        range_end = isoparse(d.pop("range_end")).date()

        create_backfill_request = cls(
            range_start=range_start,
            range_end=range_end,
        )

        create_backfill_request.additional_properties = d
        return create_backfill_request

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
