from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="GetAccountsResponse200DataItemAccountsItem")



@_attrs_define
class GetAccountsResponse200DataItemAccountsItem:
    """ 
        Attributes:
            account_id (str | Unset): Account ID
            account_name (str | Unset): Account name
            group_name (str | Unset): Account group name (empty string when not available)
     """

    account_id: str | Unset = UNSET
    account_name: str | Unset = UNSET
    group_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        account_id = self.account_id

        account_name = self.account_name

        group_name = self.group_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if account_name is not UNSET:
            field_dict["account_name"] = account_name
        if group_name is not UNSET:
            field_dict["group_name"] = group_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_id = d.pop("account_id", UNSET)

        account_name = d.pop("account_name", UNSET)

        group_name = d.pop("group_name", UNSET)

        get_accounts_response_200_data_item_accounts_item = cls(
            account_id=account_id,
            account_name=account_name,
            group_name=group_name,
        )


        get_accounts_response_200_data_item_accounts_item.additional_properties = d
        return get_accounts_response_200_data_item_accounts_item

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
