from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDataSourceConnectionRequest")


@_attrs_define
class CreateDataSourceConnectionRequest:
    """Connection configuration specifying the data source and destination for a Hub transfer.

    Attributes:
        data_source_id (str): Data source identifier (e.g., "GA" for Google Analytics, "ADM" for Adobe Analytics
            Metrics) Example: ADM.
        destination_type (str): Destination type identifier (e.g., "SQL_BQ" for BigQuery, "DWH_SNOWFLAKE" for Snowflake)
            Example: DWH_SNOWFLAKE.
        api_key (str | Unset): API Key for authentication (optional if provided in Authorization header).
            This is a reserved framework parameter and will be automatically handled.
             Example: sk_your_api_key_here.
    """

    data_source_id: str
    destination_type: str
    api_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_id = self.data_source_id

        destination_type = self.destination_type

        api_key = self.api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_source_id": data_source_id,
                "destination_type": destination_type,
            }
        )
        if api_key is not UNSET:
            field_dict["api_key"] = api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_source_id = d.pop("data_source_id")

        destination_type = d.pop("destination_type")

        api_key = d.pop("api_key", UNSET)

        create_data_source_connection_request = cls(
            data_source_id=data_source_id,
            destination_type=destination_type,
            api_key=api_key,
        )

        create_data_source_connection_request.additional_properties = d
        return create_data_source_connection_request

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
