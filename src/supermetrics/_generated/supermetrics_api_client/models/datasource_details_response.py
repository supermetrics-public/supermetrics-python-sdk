from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datasource_details import DatasourceDetails
    from ..models.response_meta import ResponseMeta


T = TypeVar("T", bound="DatasourceDetailsResponse")


@_attrs_define
class DatasourceDetailsResponse:
    """
    Attributes:
        meta (ResponseMeta | Unset):
        data (DatasourceDetails | Unset):
    """

    meta: ResponseMeta | Unset = UNSET
    data: DatasourceDetails | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if meta is not UNSET:
            field_dict["meta"] = meta
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datasource_details import DatasourceDetails
        from ..models.response_meta import ResponseMeta

        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: ResponseMeta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = ResponseMeta.from_dict(_meta)

        _data = d.pop("data", UNSET)
        data: DatasourceDetails | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = DatasourceDetails.from_dict(_data)

        datasource_details_response = cls(
            meta=meta,
            data=data,
        )

        datasource_details_response.additional_properties = d
        return datasource_details_response

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
