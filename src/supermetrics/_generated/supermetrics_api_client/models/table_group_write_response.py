from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.table_group_write_response_type import TableGroupWriteResponseType, check_table_group_write_response_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.table_group_write_response_links import TableGroupWriteResponseLinks


T = TypeVar("T", bound="TableGroupWriteResponse")


@_attrs_define
class TableGroupWriteResponse:
    """Flat response returned by import and edit endpoints.

    Attributes:
        type_ (TableGroupWriteResponseType | Unset):
        group_id (str | Unset): Supermetrics table group ID (prefixed, e.g. tg_123)
        group_name (str | Unset): Table group name
        links (TableGroupWriteResponseLinks | Unset):
    """

    type_: TableGroupWriteResponseType | Unset = UNSET
    group_id: str | Unset = UNSET
    group_name: str | Unset = UNSET
    links: TableGroupWriteResponseLinks | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        group_id = self.group_id

        group_name = self.group_name

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.table_group_write_response_links import TableGroupWriteResponseLinks

        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: TableGroupWriteResponseType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_table_group_write_response_type(_type_)

        group_id = d.pop("group_id", UNSET)

        group_name = d.pop("group_name", UNSET)

        _links = d.pop("links", UNSET)
        links: TableGroupWriteResponseLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = TableGroupWriteResponseLinks.from_dict(_links)

        table_group_write_response = cls(
            type_=type_,
            group_id=group_id,
            group_name=group_name,
            links=links,
        )

        table_group_write_response.additional_properties = d
        return table_group_write_response

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
