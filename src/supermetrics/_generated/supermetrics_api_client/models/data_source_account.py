from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_source_account_type import DataSourceAccountType, check_data_source_account_type
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataSourceAccount")


@_attrs_define
class DataSourceAccount:
    """
    Attributes:
        type_ (DataSourceAccountType | Unset):
        account_id (str | Unset): Data source account ID, as used in ds_accounts parameter
        name (str | Unset): Data source account name
        group (str | Unset): Group name for account in Supermetrics products
    """

    type_: DataSourceAccountType | Unset = UNSET
    account_id: str | Unset = UNSET
    name: str | Unset = UNSET
    group: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        account_id = self.account_id

        name = self.name

        group = self.group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if name is not UNSET:
            field_dict["name"] = name
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: DataSourceAccountType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_data_source_account_type(_type_)

        account_id = d.pop("account_id", UNSET)

        name = d.pop("name", UNSET)

        group = d.pop("group", UNSET)

        data_source_account = cls(
            type_=type_,
            account_id=account_id,
            name=name,
            group=group,
        )

        data_source_account.additional_properties = d
        return data_source_account

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
