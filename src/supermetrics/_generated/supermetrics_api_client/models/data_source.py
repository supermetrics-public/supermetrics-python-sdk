from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.data_source_type import DataSourceType
from ..types import UNSET, Unset






T = TypeVar("T", bound="DataSource")



@_attrs_define
class DataSource:
    """ 
        Attributes:
            type_ (DataSourceType | Unset):
            ds_id (str | Unset): Data source ID
            name (str | Unset): Data source name
     """

    type_: DataSourceType | Unset = UNSET
    ds_id: str | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        ds_id = self.ds_id

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if ds_id is not UNSET:
            field_dict["ds_id"] = ds_id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: DataSourceType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = DataSourceType(_type_)




        ds_id = d.pop("ds_id", UNSET)

        name = d.pop("name", UNSET)

        data_source = cls(
            type_=type_,
            ds_id=ds_id,
            name=name,
        )


        data_source.additional_properties = d
        return data_source

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
