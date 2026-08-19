from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_source_connection import DataSourceConnection
    from ..models.meta import Meta


T = TypeVar("T", bound="CreateDataSourceConnectionResponse")


@_attrs_define
class CreateDataSourceConnectionResponse:
    """Response envelope containing a created data source connection.

    Attributes:
        meta (Meta): Metadata included in every API response.
        data (DataSourceConnection): A created data source connection.
    """

    meta: Meta
    data: DataSourceConnection
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_source_connection import DataSourceConnection
        from ..models.meta import Meta

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = DataSourceConnection.from_dict(d.pop("data"))

        create_data_source_connection_response = cls(
            meta=meta,
            data=data,
        )

        create_data_source_connection_response.additional_properties = d
        return create_data_source_connection_response

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
