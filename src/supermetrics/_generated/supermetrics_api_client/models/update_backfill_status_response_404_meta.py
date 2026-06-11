from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateBackfillStatusResponse404Meta")


@_attrs_define
class UpdateBackfillStatusResponse404Meta:
    """Metadata included in every API response.

    Attributes:
        request_id (str): Unique identifier for the request, for tracking and debugging. Example:
            BXaEFVtjc7TXaJxgZhmFgSUD9edqq_CN.
    """

    request_id: str

    def to_dict(self) -> dict[str, Any]:
        request_id = self.request_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "request_id": request_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        request_id = d.pop("request_id")

        update_backfill_status_response_404_meta = cls(
            request_id=request_id,
        )

        return update_backfill_status_response_404_meta
