from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ResourceUrl")


@_attrs_define
class ResourceUrl:
    """A hyperlink to a related resource.

    Attributes:
        href (str): Absolute URL of the resource. Example: https://api.supermetrics.com/v1/teams/team_abc/custom-
            fields?offset=20&limit=20.
    """

    href: str

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "href": href,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        href = d.pop("href")

        resource_url = cls(
            href=href,
        )

        return resource_url
