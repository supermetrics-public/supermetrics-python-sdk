from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.account_tag_list_response_data import AccountTagListResponseData
    from ..models.meta import Meta


T = TypeVar("T", bound="AccountTagListResponse")


@_attrs_define
class AccountTagListResponse:
    """
    Attributes:
        meta (Meta): Metadata included in every API response.
        data (AccountTagListResponseData): Wrapper object holding the team's account tags Example: {'items': [{'name':
            'a1b2c3d', 'display_name': 'EMEA paid media', 'color': '#112233', 'data_source_count': 3, 'account_count':
            42}]}.
    """

    meta: Meta
    data: AccountTagListResponseData

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "meta": meta,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_tag_list_response_data import AccountTagListResponseData
        from ..models.meta import Meta

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = AccountTagListResponseData.from_dict(d.pop("data"))

        account_tag_list_response = cls(
            meta=meta,
            data=data,
        )

        return account_tag_list_response
