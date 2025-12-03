from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DataResponseMetaResult")


@_attrs_define
class DataResponseMetaResult:
    """
    Attributes:
        total_columns (int | Unset): Total amount of columns
        total_rows (int | Unset): Total amount of rows in data
        run_seconds (float | Unset): Number of seconds it took for the query to run
        data_sampled (bool | Unset): If data source has provided sampled data
        cache_used (bool | Unset): If cached data was used
        cache_time (datetime.datetime | Unset): ISO 8601 datetime for the most recent cached data
    """

    total_columns: int | Unset = UNSET
    total_rows: int | Unset = UNSET
    run_seconds: float | Unset = UNSET
    data_sampled: bool | Unset = UNSET
    cache_used: bool | Unset = UNSET
    cache_time: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_columns = self.total_columns

        total_rows = self.total_rows

        run_seconds = self.run_seconds

        data_sampled = self.data_sampled

        cache_used = self.cache_used

        cache_time: str | Unset = UNSET
        if not isinstance(self.cache_time, Unset):
            cache_time = self.cache_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_columns is not UNSET:
            field_dict["total_columns"] = total_columns
        if total_rows is not UNSET:
            field_dict["total_rows"] = total_rows
        if run_seconds is not UNSET:
            field_dict["run_seconds"] = run_seconds
        if data_sampled is not UNSET:
            field_dict["data_sampled"] = data_sampled
        if cache_used is not UNSET:
            field_dict["cache_used"] = cache_used
        if cache_time is not UNSET:
            field_dict["cache_time"] = cache_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_columns = d.pop("total_columns", UNSET)

        total_rows = d.pop("total_rows", UNSET)

        run_seconds = d.pop("run_seconds", UNSET)

        data_sampled = d.pop("data_sampled", UNSET)

        cache_used = d.pop("cache_used", UNSET)

        _cache_time = d.pop("cache_time", UNSET)
        cache_time: datetime.datetime | Unset
        if isinstance(_cache_time, Unset):
            cache_time = UNSET
        else:
            cache_time = isoparse(_cache_time)

        data_response_meta_result = cls(
            total_columns=total_columns,
            total_rows=total_rows,
            run_seconds=run_seconds,
            data_sampled=data_sampled,
            cache_used=cache_used,
            cache_time=cache_time,
        )

        data_response_meta_result.additional_properties = d
        return data_response_meta_result

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
