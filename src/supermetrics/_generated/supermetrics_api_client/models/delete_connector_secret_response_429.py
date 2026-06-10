from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.delete_connector_secret_response_429_meta import DeleteConnectorSecretResponse429Meta
    from ..models.error import Error


T = TypeVar("T", bound="DeleteConnectorSecretResponse429")


@_attrs_define
class DeleteConnectorSecretResponse429:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (DeleteConnectorSecretResponse429Meta): Metadata included in every API response.
        error (Error):
    """

    meta: DeleteConnectorSecretResponse429Meta
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
        from ..models.delete_connector_secret_response_429_meta import DeleteConnectorSecretResponse429Meta
        from ..models.error import Error

        d = dict(src_dict)
        meta = DeleteConnectorSecretResponse429Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        delete_connector_secret_response_429 = cls(
            meta=meta,
            error=error,
        )

        return delete_connector_secret_response_429
