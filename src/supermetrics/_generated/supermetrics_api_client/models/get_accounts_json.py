from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GetAccountsJson")



@_attrs_define
class GetAccountsJson:
    """ 
        Attributes:
            ds_id (str): Data source ID
            api_key (str | Unset): API key when not using an authorization header
            ds_users (list[str] | str | Unset): List of data source login usernames to target (case-insensitive)
            cache_minutes (int | Unset): Maximum allowed age of cache in minutes
     """

    ds_id: str
    api_key: str | Unset = UNSET
    ds_users: list[str] | str | Unset = UNSET
    cache_minutes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ds_id = self.ds_id

        api_key = self.api_key

        ds_users: list[str] | str | Unset
        if isinstance(self.ds_users, Unset):
            ds_users = UNSET
        elif isinstance(self.ds_users, list):
            ds_users = self.ds_users


        else:
            ds_users = self.ds_users

        cache_minutes = self.cache_minutes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ds_id": ds_id,
        })
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if ds_users is not UNSET:
            field_dict["ds_users"] = ds_users
        if cache_minutes is not UNSET:
            field_dict["cache_minutes"] = cache_minutes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ds_id = d.pop("ds_id")

        api_key = d.pop("api_key", UNSET)

        def _parse_ds_users(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ds_users_type_1 = cast(list[str], data)

                return ds_users_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        ds_users = _parse_ds_users(d.pop("ds_users", UNSET))


        cache_minutes = d.pop("cache_minutes", UNSET)

        get_accounts_json = cls(
            ds_id=ds_id,
            api_key=api_key,
            ds_users=ds_users,
            cache_minutes=cache_minutes,
        )


        get_accounts_json.additional_properties = d
        return get_accounts_json

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
