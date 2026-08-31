from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CloneTransferBodyAccountsItem")


@_attrs_define
class CloneTransferBodyAccountsItem:
    """
    Attributes:
        data_source_username (str):
        login_id (int):
        account_id (str):
    """

    data_source_username: str
    login_id: int
    account_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_username = self.data_source_username

        login_id = self.login_id

        account_id = self.account_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_source_username": data_source_username,
                "login_id": login_id,
                "account_id": account_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_source_username = d.pop("data_source_username")

        login_id = d.pop("login_id")

        account_id = d.pop("account_id")

        clone_transfer_body_accounts_item = cls(
            data_source_username=data_source_username,
            login_id=login_id,
            account_id=account_id,
        )

        clone_transfer_body_accounts_item.additional_properties = d
        return clone_transfer_body_accounts_item

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
