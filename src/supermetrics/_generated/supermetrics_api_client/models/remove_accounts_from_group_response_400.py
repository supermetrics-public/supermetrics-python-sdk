from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error import Error
    from ..models.remove_accounts_from_group_response_400_meta import RemoveAccountsFromGroupResponse400Meta


T = TypeVar("T", bound="RemoveAccountsFromGroupResponse400")


@_attrs_define
class RemoveAccountsFromGroupResponse400:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (RemoveAccountsFromGroupResponse400Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: RemoveAccountsFromGroupResponse400Meta
    error: Error

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "meta": meta,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error import Error
        from ..models.remove_accounts_from_group_response_400_meta import RemoveAccountsFromGroupResponse400Meta

        d = dict(src_dict)
        meta = RemoveAccountsFromGroupResponse400Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        remove_accounts_from_group_response_400 = cls(
            meta=meta,
            error=error,
        )

        return remove_accounts_from_group_response_400
