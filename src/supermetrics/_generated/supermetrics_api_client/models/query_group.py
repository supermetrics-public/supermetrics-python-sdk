from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.query_group_type import QueryGroupType, check_query_group_type
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryGroup")


@_attrs_define
class QueryGroup:
    """
    Attributes:
        type_ (QueryGroupType | Unset):
        group_id (str | Unset): Supermetrics query group ID
        name (str | Unset): Query group name
    """

    type_: QueryGroupType | Unset = UNSET
    group_id: str | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        group_id = self.group_id

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: QueryGroupType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_query_group_type(_type_)

        group_id = d.pop("group_id", UNSET)

        name = d.pop("name", UNSET)

        query_group = cls(
            type_=type_,
            group_id=group_id,
            name=name,
        )

        query_group.additional_properties = d
        return query_group

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
