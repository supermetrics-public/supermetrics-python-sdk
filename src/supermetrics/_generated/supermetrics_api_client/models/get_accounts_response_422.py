from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error import Error
    from ..models.get_accounts_response_422_meta import GetAccountsResponse422Meta


T = TypeVar("T", bound="GetAccountsResponse422")


@_attrs_define
class GetAccountsResponse422:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (GetAccountsResponse422Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: GetAccountsResponse422Meta
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
        from ..models.get_accounts_response_422_meta import GetAccountsResponse422Meta

        d = dict(src_dict)
        meta = GetAccountsResponse422Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        get_accounts_response_422 = cls(
            meta=meta,
            error=error,
        )

        return get_accounts_response_422
