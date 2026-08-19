from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.pagination import Pagination


T = TypeVar("T", bound="MetaWithPagination")


@_attrs_define
class MetaWithPagination:
    """Response metadata including pagination details.

    Attributes:
        request_id (str): Unique identifier for the request, for tracking and debugging. Example:
            BXaEFVtjc7TXaJxgZhmFgSUD9edqq_CN.
        pagination (Pagination): Offset-based pagination metadata for list responses.
    """

    request_id: str
    pagination: Pagination
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_id = self.request_id

        pagination = self.pagination.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request_id": request_id,
                "pagination": pagination,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pagination import Pagination

        d = dict(src_dict)
        request_id = d.pop("request_id")

        pagination = Pagination.from_dict(d.pop("pagination"))

        meta_with_pagination = cls(
            request_id=request_id,
            pagination=pagination,
        )

        meta_with_pagination.additional_properties = d
        return meta_with_pagination

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
