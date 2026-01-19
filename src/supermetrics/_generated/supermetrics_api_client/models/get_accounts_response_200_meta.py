from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.get_accounts_response_200_meta_query import GetAccountsResponse200MetaQuery





T = TypeVar("T", bound="GetAccountsResponse200Meta")



@_attrs_define
class GetAccountsResponse200Meta:
    """ 
        Attributes:
            request_id (str | Unset): API request ID
            query (GetAccountsResponse200MetaQuery | Unset):
     """

    request_id: str | Unset = UNSET
    query: GetAccountsResponse200MetaQuery | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_accounts_response_200_meta_query import GetAccountsResponse200MetaQuery
        request_id = self.request_id

        query: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_accounts_response_200_meta_query import GetAccountsResponse200MetaQuery
        d = dict(src_dict)
        request_id = d.pop("request_id", UNSET)

        _query = d.pop("query", UNSET)
        query: GetAccountsResponse200MetaQuery | Unset
        if isinstance(_query,  Unset):
            query = UNSET
        else:
            query = GetAccountsResponse200MetaQuery.from_dict(_query)




        get_accounts_response_200_meta = cls(
            request_id=request_id,
            query=query,
        )


        get_accounts_response_200_meta.additional_properties = d
        return get_accounts_response_200_meta

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
