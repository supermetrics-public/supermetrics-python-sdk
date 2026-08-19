from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error import Error
    from ..models.update_destination_response_401_meta import UpdateDestinationResponse401Meta


T = TypeVar("T", bound="UpdateDestinationResponse401")


@_attrs_define
class UpdateDestinationResponse401:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (UpdateDestinationResponse401Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: UpdateDestinationResponse401Meta
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
        from ..models.update_destination_response_401_meta import UpdateDestinationResponse401Meta

        d = dict(src_dict)
        meta = UpdateDestinationResponse401Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        update_destination_response_401 = cls(
            meta=meta,
            error=error,
        )

        return update_destination_response_401
