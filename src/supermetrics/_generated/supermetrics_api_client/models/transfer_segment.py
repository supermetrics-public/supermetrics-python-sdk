from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransferSegment")


@_attrs_define
class TransferSegment:
    """
    Example:
        {'data_source_username': 'user.name@supermetrics.com', 'login_id': 2830506, 'segment_id': '-1', 'segment_name':
            'All users'}

    Attributes:
        data_source_username (str | Unset): Username for data source authentication
        login_id (int | Unset): Login identifier
        segment_id (str | Unset): Segment identifier
        segment_name (str | Unset): Human-readable segment name
    """

    data_source_username: str | Unset = UNSET
    login_id: int | Unset = UNSET
    segment_id: str | Unset = UNSET
    segment_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_username = self.data_source_username

        login_id = self.login_id

        segment_id = self.segment_id

        segment_name = self.segment_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_source_username is not UNSET:
            field_dict["data_source_username"] = data_source_username
        if login_id is not UNSET:
            field_dict["login_id"] = login_id
        if segment_id is not UNSET:
            field_dict["segment_id"] = segment_id
        if segment_name is not UNSET:
            field_dict["segment_name"] = segment_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_source_username = d.pop("data_source_username", UNSET)

        login_id = d.pop("login_id", UNSET)

        segment_id = d.pop("segment_id", UNSET)

        segment_name = d.pop("segment_name", UNSET)

        transfer_segment = cls(
            data_source_username=data_source_username,
            login_id=login_id,
            segment_id=segment_id,
            segment_name=segment_name,
        )

        transfer_segment.additional_properties = d
        return transfer_segment

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
