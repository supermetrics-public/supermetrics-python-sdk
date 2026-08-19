from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlendedDataSourceInputAccountsItem")


@_attrs_define
class BlendedDataSourceInputAccountsItem:
    """An account selected for this data source.

    Attributes:
        account_id (str | Unset): Account identifier. Example: 1234567890.
        account_name (str | Unset): Account display name. Example: Acme Corp.
        group_name (None | str | Unset): Group the account belongs to, if any. Example: EMEA.
        data_source_username (str | Unset): Username used to authenticate with the data source. Example:
            user@supermetrics.com.
        data_source_display_username (str | Unset): Display name of the data source username. Example:
            user@supermetrics.com.
    """

    account_id: str | Unset = UNSET
    account_name: str | Unset = UNSET
    group_name: None | str | Unset = UNSET
    data_source_username: str | Unset = UNSET
    data_source_display_username: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = self.account_id

        account_name = self.account_name

        group_name: None | str | Unset
        if isinstance(self.group_name, Unset):
            group_name = UNSET
        else:
            group_name = self.group_name

        data_source_username = self.data_source_username

        data_source_display_username = self.data_source_display_username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if account_name is not UNSET:
            field_dict["account_name"] = account_name
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if data_source_username is not UNSET:
            field_dict["data_source_username"] = data_source_username
        if data_source_display_username is not UNSET:
            field_dict["data_source_display_username"] = data_source_display_username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_id = d.pop("account_id", UNSET)

        account_name = d.pop("account_name", UNSET)

        def _parse_group_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_name = _parse_group_name(d.pop("group_name", UNSET))

        data_source_username = d.pop("data_source_username", UNSET)

        data_source_display_username = d.pop("data_source_display_username", UNSET)

        blended_data_source_input_accounts_item = cls(
            account_id=account_id,
            account_name=account_name,
            group_name=group_name,
            data_source_username=data_source_username,
            data_source_display_username=data_source_display_username,
        )

        blended_data_source_input_accounts_item.additional_properties = d
        return blended_data_source_input_accounts_item

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
