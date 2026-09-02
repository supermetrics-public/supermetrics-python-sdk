from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_url import ResourceURL


T = TypeVar("T", bound="TableGroupWriteResponseLinks")


@_attrs_define
class TableGroupWriteResponseLinks:
    """
    Attributes:
        enclosure (ResourceURL | Unset):
    """

    enclosure: ResourceURL | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enclosure: dict[str, Any] | Unset = UNSET
        if not isinstance(self.enclosure, Unset):
            enclosure = self.enclosure.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enclosure is not UNSET:
            field_dict["enclosure"] = enclosure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_url import ResourceURL

        d = dict(src_dict)
        _enclosure = d.pop("enclosure", UNSET)
        enclosure: ResourceURL | Unset
        if isinstance(_enclosure, Unset):
            enclosure = UNSET
        else:
            enclosure = ResourceURL.from_dict(_enclosure)

        table_group_write_response_links = cls(
            enclosure=enclosure,
        )

        table_group_write_response_links.additional_properties = d
        return table_group_write_response_links

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
