from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Secret")


@_attrs_define
class Secret:
    """A connector secret (value is never returned).

    Attributes:
        secret_placeholder (str): Unique identifier for the secret Example: sec_a23f23d26.
        secret_name (str): Human-readable name of the secret Example: client_id.
    """

    secret_placeholder: str
    secret_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        secret_placeholder = self.secret_placeholder

        secret_name = self.secret_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secret_placeholder": secret_placeholder,
                "secret_name": secret_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        secret_placeholder = d.pop("secret_placeholder")

        secret_name = d.pop("secret_name")

        secret = cls(
            secret_placeholder=secret_placeholder,
            secret_name=secret_name,
        )

        secret.additional_properties = d
        return secret

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
