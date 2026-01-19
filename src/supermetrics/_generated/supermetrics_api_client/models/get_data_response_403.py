from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="GetDataResponse403")



@_attrs_define
class GetDataResponse403:
    """ RFC 9457 Problem Details for HTTP APIs

        Attributes:
            type_ (str): A URI reference that identifies the problem type Example:
                https://supermetrics.com/problems/unauthorized.
            title (str): A short, human-readable summary of the problem type Example: Unauthorized.
            status (int): The HTTP status code Example: 401.
            detail (str | Unset): A human-readable explanation specific to this occurrence Example: Authentication required.
            instance (str | Unset): A URI reference that identifies the specific occurrence Example:
                https://api.supermetrics.com/v2/api-keys.
     """

    type_: str
    title: str
    status: int
    detail: str | Unset = UNSET
    instance: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        status = self.status

        detail = self.detail

        instance = self.instance


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "title": title,
            "status": status,
        })
        if detail is not UNSET:
            field_dict["detail"] = detail
        if instance is not UNSET:
            field_dict["instance"] = instance

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        status = d.pop("status")

        detail = d.pop("detail", UNSET)

        instance = d.pop("instance", UNSET)

        get_data_response_403 = cls(
            type_=type_,
            title=title,
            status=status,
            detail=detail,
            instance=instance,
        )

        return get_data_response_403

