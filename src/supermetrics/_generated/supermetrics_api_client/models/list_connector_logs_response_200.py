from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.log_entry import LogEntry


T = TypeVar("T", bound="ListConnectorLogsResponse200")


@_attrs_define
class ListConnectorLogsResponse200:
    """
    Attributes:
        logs (list[LogEntry]):
    """

    logs: list[LogEntry]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logs = []
        for logs_item_data in self.logs:
            logs_item = logs_item_data.to_dict()
            logs.append(logs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logs": logs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_entry import LogEntry

        d = dict(src_dict)
        logs = []
        _logs = d.pop("logs")
        for logs_item_data in _logs:
            logs_item = LogEntry.from_dict(logs_item_data)

            logs.append(logs_item)

        list_connector_logs_response_200 = cls(
            logs=logs,
        )

        list_connector_logs_response_200.additional_properties = d
        return list_connector_logs_response_200

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
