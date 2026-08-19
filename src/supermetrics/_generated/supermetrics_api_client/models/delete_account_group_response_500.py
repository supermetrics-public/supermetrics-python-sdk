from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.delete_account_group_response_500_meta import DeleteAccountGroupResponse500Meta
    from ..models.error import Error


T = TypeVar("T", bound="DeleteAccountGroupResponse500")


@_attrs_define
class DeleteAccountGroupResponse500:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (DeleteAccountGroupResponse500Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: DeleteAccountGroupResponse500Meta
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
        from ..models.delete_account_group_response_500_meta import DeleteAccountGroupResponse500Meta
        from ..models.error import Error

        d = dict(src_dict)
        meta = DeleteAccountGroupResponse500Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        delete_account_group_response_500 = cls(
            meta=meta,
            error=error,
        )

        return delete_account_group_response_500
