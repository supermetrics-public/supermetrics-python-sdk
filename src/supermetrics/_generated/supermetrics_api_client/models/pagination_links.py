from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_url import ResourceUrl


T = TypeVar("T", bound="PaginationLinks")


@_attrs_define
class PaginationLinks:
    """Navigation links for paginated collections.

    Attributes:
        next_ (ResourceUrl | Unset): A hyperlink to a related resource.
        previous (ResourceUrl | Unset): A hyperlink to a related resource.
    """

    next_: ResourceUrl | Unset = UNSET
    previous: ResourceUrl | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        previous: dict[str, Any] | Unset = UNSET
        if not isinstance(self.previous, Unset):
            previous = self.previous.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_url import ResourceUrl

        d = dict(src_dict)
        _next_ = d.pop("next", UNSET)
        next_: ResourceUrl | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = ResourceUrl.from_dict(_next_)

        _previous = d.pop("previous", UNSET)
        previous: ResourceUrl | Unset
        if isinstance(_previous, Unset):
            previous = UNSET
        else:
            previous = ResourceUrl.from_dict(_previous)

        pagination_links = cls(
            next_=next_,
            previous=previous,
        )

        return pagination_links
