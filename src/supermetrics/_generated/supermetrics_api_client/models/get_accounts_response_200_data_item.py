from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.get_accounts_response_200_data_item_accounts_item import GetAccountsResponse200DataItemAccountsItem





T = TypeVar("T", bound="GetAccountsResponse200DataItem")



@_attrs_define
class GetAccountsResponse200DataItem:
    """ 
        Attributes:
            ds_user (str | Unset): Data source login username
            display_name (str | Unset): Display name for login
            cache_time (datetime.datetime | None | Unset): ISO 8601 datetime for the last time the login data was fetched
                and cached
            accounts (list[GetAccountsResponse200DataItemAccountsItem] | Unset):
     """

    ds_user: str | Unset = UNSET
    display_name: str | Unset = UNSET
    cache_time: datetime.datetime | None | Unset = UNSET
    accounts: list[GetAccountsResponse200DataItemAccountsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_accounts_response_200_data_item_accounts_item import GetAccountsResponse200DataItemAccountsItem
        ds_user = self.ds_user

        display_name = self.display_name

        cache_time: None | str | Unset
        if isinstance(self.cache_time, Unset):
            cache_time = UNSET
        elif isinstance(self.cache_time, datetime.datetime):
            cache_time = self.cache_time.isoformat()
        else:
            cache_time = self.cache_time

        accounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if ds_user is not UNSET:
            field_dict["ds_user"] = ds_user
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if cache_time is not UNSET:
            field_dict["cache_time"] = cache_time
        if accounts is not UNSET:
            field_dict["accounts"] = accounts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_accounts_response_200_data_item_accounts_item import GetAccountsResponse200DataItemAccountsItem
        d = dict(src_dict)
        ds_user = d.pop("ds_user", UNSET)

        display_name = d.pop("display_name", UNSET)

        def _parse_cache_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cache_time_type_0 = isoparse(data)



                return cache_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        cache_time = _parse_cache_time(d.pop("cache_time", UNSET))


        _accounts = d.pop("accounts", UNSET)
        accounts: list[GetAccountsResponse200DataItemAccountsItem] | Unset = UNSET
        if _accounts is not UNSET:
            accounts = []
            for accounts_item_data in _accounts:
                accounts_item = GetAccountsResponse200DataItemAccountsItem.from_dict(accounts_item_data)



                accounts.append(accounts_item)


        get_accounts_response_200_data_item = cls(
            ds_user=ds_user,
            display_name=display_name,
            cache_time=cache_time,
            accounts=accounts,
        )


        get_accounts_response_200_data_item.additional_properties = d
        return get_accounts_response_200_data_item

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
