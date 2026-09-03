from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_update_destinations_response_200_data import BatchUpdateDestinationsResponse200Data
    from ..models.meta import Meta


T = TypeVar("T", bound="BatchUpdateDestinationsResponse200")


@_attrs_define
class BatchUpdateDestinationsResponse200:
    """
    Attributes:
        meta (Meta | Unset): Metadata included in every API response.
        data (BatchUpdateDestinationsResponse200Data | Unset):
    """

    meta: Meta | Unset = UNSET
    data: BatchUpdateDestinationsResponse200Data | Unset = UNSET
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
        from ..models.batch_update_destinations_response_200_data import BatchUpdateDestinationsResponse200Data
        from ..models.meta import Meta

        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: Meta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = Meta.from_dict(_meta)

        _data = d.pop("data", UNSET)
        data: BatchUpdateDestinationsResponse200Data | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = BatchUpdateDestinationsResponse200Data.from_dict(_data)

        batch_update_destinations_response_200 = cls(
            meta=meta,
            data=data,
        )

        batch_update_destinations_response_200.additional_properties = d
        return batch_update_destinations_response_200

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
