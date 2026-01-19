from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DataResponseMetaQueryFieldsItem")



@_attrs_define
class DataResponseMetaQueryFieldsItem:
    """ 
        Attributes:
            id (str | Unset): Field ID from the request
            field_id (str | Unset): Field ID the API uses
            field_name (str | Unset): Field name
            field_type (str | Unset): Field type
            field_split (str | Unset): Field split by type
            data_type (str | Unset): Field data type
            data_column (int | Unset): Field value position in each data row
            visible (bool | Unset): Whether data for this field is visible
     """

    id: str | Unset = UNSET
    field_id: str | Unset = UNSET
    field_name: str | Unset = UNSET
    field_type: str | Unset = UNSET
    field_split: str | Unset = UNSET
    data_type: str | Unset = UNSET
    data_column: int | Unset = UNSET
    visible: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        field_id = self.field_id

        field_name = self.field_name

        field_type = self.field_type

        field_split = self.field_split

        data_type = self.data_type

        data_column = self.data_column

        visible = self.visible


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if field_id is not UNSET:
            field_dict["field_id"] = field_id
        if field_name is not UNSET:
            field_dict["field_name"] = field_name
        if field_type is not UNSET:
            field_dict["field_type"] = field_type
        if field_split is not UNSET:
            field_dict["field_split"] = field_split
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if data_column is not UNSET:
            field_dict["data_column"] = data_column
        if visible is not UNSET:
            field_dict["visible"] = visible

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        field_id = d.pop("field_id", UNSET)

        field_name = d.pop("field_name", UNSET)

        field_type = d.pop("field_type", UNSET)

        field_split = d.pop("field_split", UNSET)

        data_type = d.pop("data_type", UNSET)

        data_column = d.pop("data_column", UNSET)

        visible = d.pop("visible", UNSET)

        data_response_meta_query_fields_item = cls(
            id=id,
            field_id=field_id,
            field_name=field_name,
            field_type=field_type,
            field_split=field_split,
            data_type=data_type,
            data_column=data_column,
            visible=visible,
        )


        data_response_meta_query_fields_item.additional_properties = d
        return data_response_meta_query_fields_item

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
