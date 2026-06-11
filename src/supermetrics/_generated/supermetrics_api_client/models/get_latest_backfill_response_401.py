from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error import Error
    from ..models.get_latest_backfill_response_401_meta import GetLatestBackfillResponse401Meta


T = TypeVar("T", bound="GetLatestBackfillResponse401")


@_attrs_define
class GetLatestBackfillResponse401:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (GetLatestBackfillResponse401Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: GetLatestBackfillResponse401Meta
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
        from ..models.get_latest_backfill_response_401_meta import GetLatestBackfillResponse401Meta

        d = dict(src_dict)
        meta = GetLatestBackfillResponse401Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        get_latest_backfill_response_401 = cls(
            meta=meta,
            error=error,
        )

        return get_latest_backfill_response_401
