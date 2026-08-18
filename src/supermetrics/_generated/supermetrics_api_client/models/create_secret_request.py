from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateSecretRequest")


@_attrs_define
class CreateSecretRequest:
    """Secret name and value to encrypt and store.

    Attributes:
        secret_name (str): Human-readable name for the secret Example: client_id.
        secret_value (str): Plaintext value to be encrypted and stored Example: my-super-secret-value.
    """

    secret_name: str
    secret_value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        secret_name = self.secret_name

        secret_value = self.secret_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secret_name": secret_name,
                "secret_value": secret_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        secret_name = d.pop("secret_name")

        secret_value = d.pop("secret_value")

        create_secret_request = cls(
            secret_name=secret_name,
            secret_value=secret_value,
        )

        create_secret_request.additional_properties = d
        return create_secret_request

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
