from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaginationLinks")


@_attrs_define
class PaginationLinks:
    """Navigation links for paginated collections.

    Attributes:
        first (None | str | Unset): URL of the first page, or null when not applicable. Example:
            https://api.supermetrics.com/v1/teams/team_abc/custom-fields?offset=0&limit=20.
        prev (None | str | Unset): URL of the previous page, or null on the first page.
        next_ (None | str | Unset): URL of the next page, or null on the last page. Example:
            https://api.supermetrics.com/v1/teams/team_abc/custom-fields?offset=20&limit=20.
        last (None | str | Unset): URL of the last page, or null when not applicable.
    """

    first: None | str | Unset = UNSET
    prev: None | str | Unset = UNSET
    next_: None | str | Unset = UNSET
    last: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        first: None | str | Unset
        if isinstance(self.first, Unset):
            first = UNSET
        else:
            first = self.first

        prev: None | str | Unset
        if isinstance(self.prev, Unset):
            prev = UNSET
        else:
            prev = self.prev

        next_: None | str | Unset
        if isinstance(self.next_, Unset):
            next_ = UNSET
        else:
            next_ = self.next_

        last: None | str | Unset
        if isinstance(self.last, Unset):
            last = UNSET
        else:
            last = self.last

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if first is not UNSET:
            field_dict["first"] = first
        if prev is not UNSET:
            field_dict["prev"] = prev
        if next_ is not UNSET:
            field_dict["next"] = next_
        if last is not UNSET:
            field_dict["last"] = last

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_first(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first = _parse_first(d.pop("first", UNSET))

        def _parse_prev(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prev = _parse_prev(d.pop("prev", UNSET))

        def _parse_next_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_ = _parse_next_(d.pop("next", UNSET))

        def _parse_last(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last = _parse_last(d.pop("last", UNSET))

        pagination_links = cls(
            first=first,
            prev=prev,
            next_=next_,
            last=last,
        )

        return pagination_links
