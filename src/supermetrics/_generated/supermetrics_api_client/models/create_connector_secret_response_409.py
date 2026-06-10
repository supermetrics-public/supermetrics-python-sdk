from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.create_connector_secret_response_409_meta import CreateConnectorSecretResponse409Meta
    from ..models.error import Error


T = TypeVar("T", bound="CreateConnectorSecretResponse409")


@_attrs_define
class CreateConnectorSecretResponse409:
    """Standard envelope returned by all error (4xx/5xx) responses.

    Attributes:
        meta (CreateConnectorSecretResponse409Meta): Metadata included in every API response.
        error (Error): Machine- and human-readable detail for a failed request.
    """

    meta: CreateConnectorSecretResponse409Meta
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
        from ..models.create_connector_secret_response_409_meta import CreateConnectorSecretResponse409Meta
        from ..models.error import Error

        d = dict(src_dict)
        meta = CreateConnectorSecretResponse409Meta.from_dict(d.pop("meta"))

        error = Error.from_dict(d.pop("error"))

        create_connector_secret_response_409 = cls(
            meta=meta,
            error=error,
        )

        return create_connector_secret_response_409
