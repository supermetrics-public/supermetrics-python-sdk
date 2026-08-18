from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.meta import Meta
    from ..models.transfer_created_response import TransferCreatedResponse


T = TypeVar("T", bound="TransferCreatedEnvelope")


@_attrs_define
class TransferCreatedEnvelope:
    """Response envelope containing a created transfer.

    Attributes:
        meta (Meta): Metadata included in every API response.
        data (TransferCreatedResponse): Response from creating a transfer
    """

    meta: Meta
    data: TransferCreatedResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.meta import Meta
        from ..models.transfer_created_response import TransferCreatedResponse

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = TransferCreatedResponse.from_dict(d.pop("data"))

        transfer_created_envelope = cls(
            meta=meta,
            data=data,
        )

        transfer_created_envelope.additional_properties = d
        return transfer_created_envelope

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
