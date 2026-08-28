from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CloneTransferBodySegmentsItem")


@_attrs_define
class CloneTransferBodySegmentsItem:
    """
    Attributes:
        data_source_username (str):
        segment_id (str):
        segment_name (str | Unset):
    """

    data_source_username: str
    segment_id: str
    segment_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_username = self.data_source_username

        segment_id = self.segment_id

        segment_name = self.segment_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_source_username": data_source_username,
                "segment_id": segment_id,
            }
        )
        if segment_name is not UNSET:
            field_dict["segment_name"] = segment_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_source_username = d.pop("data_source_username")

        segment_id = d.pop("segment_id")

        segment_name = d.pop("segment_name", UNSET)

        clone_transfer_body_segments_item = cls(
            data_source_username=data_source_username,
            segment_id=segment_id,
            segment_name=segment_name,
        )

        clone_transfer_body_segments_item.additional_properties = d
        return clone_transfer_body_segments_item

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
