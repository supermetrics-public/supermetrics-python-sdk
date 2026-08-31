from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.table_group_type import TableGroupType, check_table_group_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.table_group_links import TableGroupLinks


T = TypeVar("T", bound="TableGroup")


@_attrs_define
class TableGroup:
    """
    Attributes:
        type_ (TableGroupType | Unset):
        group_id (str | Unset): Supermetrics table group ID
        schema_id (int | Unset): Numeric schema identifier (dwh_schema_id) of this table group. Use this value as the
            `schema_id` parameter when creating a transfer.
        name (str | Unset): Table group name
        links (TableGroupLinks | Unset):
    """

    type_: TableGroupType | Unset = UNSET
    group_id: str | Unset = UNSET
    schema_id: int | Unset = UNSET
    name: str | Unset = UNSET
    links: TableGroupLinks | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        group_id = self.group_id

        schema_id = self.schema_id

        name = self.name

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
        if schema_id is not UNSET:
            field_dict["schema_id"] = schema_id
        if name is not UNSET:
            field_dict["name"] = name
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.table_group_links import TableGroupLinks

        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: TableGroupType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_table_group_type(_type_)

        group_id = d.pop("group_id", UNSET)

        schema_id = d.pop("schema_id", UNSET)

        name = d.pop("name", UNSET)

        _links = d.pop("links", UNSET)
        links: TableGroupLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = TableGroupLinks.from_dict(_links)

        table_group = cls(
            type_=type_,
            group_id=group_id,
            schema_id=schema_id,
            name=name,
            links=links,
        )

        table_group.additional_properties = d
        return table_group

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
