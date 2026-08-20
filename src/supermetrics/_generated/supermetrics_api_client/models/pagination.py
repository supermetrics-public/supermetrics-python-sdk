from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pagination_links import PaginationLinks


T = TypeVar("T", bound="Pagination")


@_attrs_define
class Pagination:
    """Offset-based pagination metadata for list responses.

    Attributes:
        total_count (int | Unset): Total number of items available across all pages. Example: 137.
        limit (int | Unset): Maximum number of items returned in this page. Example: 20.
        offset (int | Unset): Number of items skipped before this page.
        links (PaginationLinks | Unset): Navigation links for paginated collections.
    """

    total_count: int | Unset = UNSET
    limit: int | Unset = UNSET
    offset: int | Unset = UNSET
    links: PaginationLinks | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        total_count = self.total_count

        limit = self.limit

        offset = self.offset

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if total_count is not UNSET:
            field_dict["total_count"] = total_count
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pagination_links import PaginationLinks

        d = dict(src_dict)
        total_count = d.pop("total_count", UNSET)

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        _links = d.pop("links", UNSET)
        links: PaginationLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = PaginationLinks.from_dict(_links)

        pagination = cls(
            total_count=total_count,
            limit=limit,
            offset=offset,
            links=links,
        )

        return pagination
