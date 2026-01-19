from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GetAccountsResponse200MetaQuery")



@_attrs_define
class GetAccountsResponse200MetaQuery:
    """ 
        Attributes:
            cache_minutes (int | None | Unset): Requested maximum age of cache in minutes
     """

    cache_minutes: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cache_minutes: int | None | Unset
        if isinstance(self.cache_minutes, Unset):
            cache_minutes = UNSET
        else:
            cache_minutes = self.cache_minutes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if cache_minutes is not UNSET:
            field_dict["cache_minutes"] = cache_minutes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_cache_minutes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cache_minutes = _parse_cache_minutes(d.pop("cache_minutes", UNSET))


        get_accounts_response_200_meta_query = cls(
            cache_minutes=cache_minutes,
        )


        get_accounts_response_200_meta_query.additional_properties = d
        return get_accounts_response_200_meta_query

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
