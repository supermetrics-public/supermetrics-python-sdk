from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_backfill_status_body_status import UpdateBackfillStatusBodyStatus

T = TypeVar("T", bound="UpdateBackfillStatusBody")


@_attrs_define
class UpdateBackfillStatusBody:
    """
    Attributes:
        status (UpdateBackfillStatusBodyStatus): New status for the backfill. Currently only "CANCELLED" is supported.
            Example: CANCELLED.
    """

    status: UpdateBackfillStatusBodyStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = UpdateBackfillStatusBodyStatus(d.pop("status"))

        update_backfill_status_body = cls(
            status=status,
        )

        update_backfill_status_body.additional_properties = d
        return update_backfill_status_body

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
