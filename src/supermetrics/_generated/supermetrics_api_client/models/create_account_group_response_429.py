from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.create_account_group_response_429_meta import CreateAccountGroupResponse429Meta
    from ..models.error import Error


T = TypeVar("T", bound="CreateAccountGroupResponse429")


@_attrs_define
class CreateAccountGroupResponse429:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (CreateAccountGroupResponse429Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: CreateAccountGroupResponse429Meta
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
        from ..models.create_account_group_response_429_meta import CreateAccountGroupResponse429Meta
        from ..models.error import Error

        d = dict(src_dict)
        meta = CreateAccountGroupResponse429Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        create_account_group_response_429 = cls(
            meta=meta,
            error=error,
        )

        return create_account_group_response_429
