from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error import Error
    from ..models.list_connectors_response_401_meta import ListConnectorsResponse401Meta


T = TypeVar("T", bound="ListConnectorsResponse401")


@_attrs_define
class ListConnectorsResponse401:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (ListConnectorsResponse401Meta): Metadata included in every API response.
        error (Error):
    """

    meta: ListConnectorsResponse401Meta
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
        from ..models.list_connectors_response_401_meta import ListConnectorsResponse401Meta

        d = dict(src_dict)
        meta = ListConnectorsResponse401Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        list_connectors_response_401 = cls(
            meta=meta,
            error=error,
        )

        return list_connectors_response_401
