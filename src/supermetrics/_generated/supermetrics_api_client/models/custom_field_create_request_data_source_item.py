from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldCreateRequestDataSourceItem")


@_attrs_define
class CustomFieldCreateRequestDataSourceItem:
    """A data source (and optional report type) the custom field applies to.

    Attributes:
        data_source_id (str | Unset): ID of the data source. Example: GAWA.
        report_type (None | str | Unset): Report type associated with the data source, if any. Example: something.
    """

    data_source_id: str | Unset = UNSET
    report_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_id = self.data_source_id

        report_type: None | str | Unset
        if isinstance(self.report_type, Unset):
            report_type = UNSET
        else:
            report_type = self.report_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_source_id is not UNSET:
            field_dict["data_source_id"] = data_source_id
        if report_type is not UNSET:
            field_dict["report_type"] = report_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_source_id = d.pop("data_source_id", UNSET)

        def _parse_report_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        report_type = _parse_report_type(d.pop("report_type", UNSET))

        custom_field_create_request_data_source_item = cls(
            data_source_id=data_source_id,
            report_type=report_type,
        )

        custom_field_create_request_data_source_item.additional_properties = d
        return custom_field_create_request_data_source_item

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
