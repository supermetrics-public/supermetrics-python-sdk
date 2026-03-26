from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.error_response_error import ErrorResponseError
    from ..models.meta import Meta


T = TypeVar("T", bound="CreateBackfillResponse401")


@_attrs_define
class CreateBackfillResponse401:
    """
    Attributes:
        meta (Meta):
        error (ErrorResponseError):
    """

    meta: Meta
    error: ErrorResponseError
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_response_error import ErrorResponseError
        from ..models.meta import Meta

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        error = ErrorResponseError.from_dict(d.pop("error"))

        create_backfill_response_401 = cls(
            meta=meta,
            error=error,
        )

        create_backfill_response_401.additional_properties = d
        return create_backfill_response_401

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
