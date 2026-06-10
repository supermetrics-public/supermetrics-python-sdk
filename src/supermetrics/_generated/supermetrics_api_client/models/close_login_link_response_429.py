from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.close_login_link_response_429_meta import CloseLoginLinkResponse429Meta
    from ..models.error import Error


T = TypeVar("T", bound="CloseLoginLinkResponse429")


@_attrs_define
class CloseLoginLinkResponse429:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (CloseLoginLinkResponse429Meta): Metadata included in every API response.
        error (Error):
    """

    meta: CloseLoginLinkResponse429Meta
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
        from ..models.close_login_link_response_429_meta import CloseLoginLinkResponse429Meta
        from ..models.error import Error

        d = dict(src_dict)
        meta = CloseLoginLinkResponse429Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        close_login_link_response_429 = cls(
            meta=meta,
            error=error,
        )

        return close_login_link_response_429
