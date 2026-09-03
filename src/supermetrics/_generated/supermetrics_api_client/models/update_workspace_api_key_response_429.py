from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error import Error
    from ..models.update_workspace_api_key_response_429_meta import UpdateWorkspaceApiKeyResponse429Meta


T = TypeVar("T", bound="UpdateWorkspaceApiKeyResponse429")


@_attrs_define
class UpdateWorkspaceApiKeyResponse429:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (UpdateWorkspaceApiKeyResponse429Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: UpdateWorkspaceApiKeyResponse429Meta
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
        from ..models.update_workspace_api_key_response_429_meta import UpdateWorkspaceApiKeyResponse429Meta

        d = dict(src_dict)
        meta = UpdateWorkspaceApiKeyResponse429Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        update_workspace_api_key_response_429 = cls(
            meta=meta,
            error=error,
        )

        return update_workspace_api_key_response_429
