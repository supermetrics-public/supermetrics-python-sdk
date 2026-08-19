from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryDetails")


@_attrs_define
class QueryDetails:
    """Per-query execution details within a transfer run.

    Attributes:
        status (str): Status of this query execution Example: COMPLETED.
        rows (int): Number of rows returned by this query Example: 3000.
        duration (float | None | Unset): Duration of this query in seconds Example: 12.5.
        error_description (None | str | Unset): Error description if the query failed
    """

    status: str
    rows: int
    duration: float | None | Unset = UNSET
    error_description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        rows = self.rows

        duration: float | None | Unset
        if isinstance(self.duration, Unset):
            duration = UNSET
        else:
            duration = self.duration

        error_description: None | str | Unset
        if isinstance(self.error_description, Unset):
            error_description = UNSET
        else:
            error_description = self.error_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "rows": rows,
            }
        )
        if duration is not UNSET:
            field_dict["duration"] = duration
        if error_description is not UNSET:
            field_dict["error_description"] = error_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        rows = d.pop("rows")

        def _parse_duration(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration = _parse_duration(d.pop("duration", UNSET))

        def _parse_error_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_description = _parse_error_description(d.pop("error_description", UNSET))

        query_details = cls(
            status=status,
            rows=rows,
            duration=duration,
            error_description=error_description,
        )

        query_details.additional_properties = d
        return query_details

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
