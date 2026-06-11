from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.secret import Secret


T = TypeVar("T", bound="CreateConnectorSecretResponse201")


@_attrs_define
class CreateConnectorSecretResponse201:
    """
    Attributes:
        count (int): Number of secrets
        secrets (list[Secret]):
    """

    count: int
    secrets: list[Secret]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        secrets = []
        for secrets_item_data in self.secrets:
            secrets_item = secrets_item_data.to_dict()
            secrets.append(secrets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "secrets": secrets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.secret import Secret

        d = dict(src_dict)
        count = d.pop("count")

        secrets = []
        _secrets = d.pop("secrets")
        for secrets_item_data in _secrets:
            secrets_item = Secret.from_dict(secrets_item_data)

            secrets.append(secrets_item)

        create_connector_secret_response_201 = cls(
            count=count,
            secrets=secrets,
        )

        create_connector_secret_response_201.additional_properties = d
        return create_connector_secret_response_201

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
