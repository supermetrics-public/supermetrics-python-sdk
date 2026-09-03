from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkspaceApiKeyBody")


@_attrs_define
class CreateWorkspaceApiKeyBody:
    """
    Attributes:
        scope_names (list[str]): List of permission scopes for the API key.
        behalf_of_user_id (None | str): Supermetrics user ID the API key identifies as
        description (str | Unset): Internal API key description
        allow_ips (list[str] | Unset): List of fixed or CIDR formatted IP addresses allowed to use API key. Only IPv4 is
            supported.
        is_enabled (bool | Unset): Whether API key is enabled and can be used in requests Default: True.
    """

    scope_names: list[str]
    behalf_of_user_id: None | str
    description: str | Unset = UNSET
    allow_ips: list[str] | Unset = UNSET
    is_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope_names = self.scope_names

        behalf_of_user_id: None | str
        behalf_of_user_id = self.behalf_of_user_id

        description = self.description

        allow_ips: list[str] | Unset = UNSET
        if not isinstance(self.allow_ips, Unset):
            allow_ips = self.allow_ips

        is_enabled = self.is_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope_names": scope_names,
                "behalf_of_user_id": behalf_of_user_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if allow_ips is not UNSET:
            field_dict["allow_ips"] = allow_ips
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope_names = cast(list[str], d.pop("scope_names"))

        def _parse_behalf_of_user_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        behalf_of_user_id = _parse_behalf_of_user_id(d.pop("behalf_of_user_id"))

        description = d.pop("description", UNSET)

        allow_ips = cast(list[str], d.pop("allow_ips", UNSET))

        is_enabled = d.pop("is_enabled", UNSET)

        create_workspace_api_key_body = cls(
            scope_names=scope_names,
            behalf_of_user_id=behalf_of_user_id,
            description=description,
            allow_ips=allow_ips,
            is_enabled=is_enabled,
        )

        create_workspace_api_key_body.additional_properties = d
        return create_workspace_api_key_body

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
