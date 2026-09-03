from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_key_type import ApiKeyType, check_api_key_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user import User


T = TypeVar("T", bound="ApiKey")


@_attrs_define
class ApiKey:
    """
    Attributes:
        type_ (ApiKeyType | Unset):
        api_key_id (str | Unset): Supermetrics API key ID
        created_time (datetime.datetime | Unset): ISO 8601 datetime for when API key was created
        description (str | Unset): Internal API key description
        key_type (str | Unset): Type of API key
        key_start (str | Unset): First 10 characters from the API key value
        key_value (None | str | Unset): API key value as plain text, when requested. Defaults to null.
        scope_names (list[str] | Unset): List of permission scopes for the API key
        allow_ips (list[str] | Unset): List of fixed or CIDR formatted IP addresses allowed to use API key
        is_enabled (bool | Unset): Whether API key is enabled and can be used in requests
        behalf_of_user_info (User | Unset):
    """

    type_: ApiKeyType | Unset = UNSET
    api_key_id: str | Unset = UNSET
    created_time: datetime.datetime | Unset = UNSET
    description: str | Unset = UNSET
    key_type: str | Unset = UNSET
    key_start: str | Unset = UNSET
    key_value: None | str | Unset = UNSET
    scope_names: list[str] | Unset = UNSET
    allow_ips: list[str] | Unset = UNSET
    is_enabled: bool | Unset = UNSET
    behalf_of_user_info: User | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        api_key_id = self.api_key_id

        created_time: str | Unset = UNSET
        if not isinstance(self.created_time, Unset):
            created_time = self.created_time.isoformat()

        description = self.description

        key_type = self.key_type

        key_start = self.key_start

        key_value: None | str | Unset
        if isinstance(self.key_value, Unset):
            key_value = UNSET
        else:
            key_value = self.key_value

        scope_names: list[str] | Unset = UNSET
        if not isinstance(self.scope_names, Unset):
            scope_names = self.scope_names

        allow_ips: list[str] | Unset = UNSET
        if not isinstance(self.allow_ips, Unset):
            allow_ips = self.allow_ips

        is_enabled = self.is_enabled

        behalf_of_user_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.behalf_of_user_info, Unset):
            behalf_of_user_info = self.behalf_of_user_info.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if api_key_id is not UNSET:
            field_dict["api_key_id"] = api_key_id
        if created_time is not UNSET:
            field_dict["created_time"] = created_time
        if description is not UNSET:
            field_dict["description"] = description
        if key_type is not UNSET:
            field_dict["key_type"] = key_type
        if key_start is not UNSET:
            field_dict["key_start"] = key_start
        if key_value is not UNSET:
            field_dict["key_value"] = key_value
        if scope_names is not UNSET:
            field_dict["scope_names"] = scope_names
        if allow_ips is not UNSET:
            field_dict["allow_ips"] = allow_ips
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled
        if behalf_of_user_info is not UNSET:
            field_dict["behalf_of_user_info"] = behalf_of_user_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user import User

        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: ApiKeyType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_api_key_type(_type_)

        api_key_id = d.pop("api_key_id", UNSET)

        _created_time = d.pop("created_time", UNSET)
        created_time: datetime.datetime | Unset
        if isinstance(_created_time, Unset):
            created_time = UNSET
        else:
            created_time = datetime.datetime.fromisoformat(_created_time)

        description = d.pop("description", UNSET)

        key_type = d.pop("key_type", UNSET)

        key_start = d.pop("key_start", UNSET)

        def _parse_key_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key_value = _parse_key_value(d.pop("key_value", UNSET))

        scope_names = cast(list[str], d.pop("scope_names", UNSET))

        allow_ips = cast(list[str], d.pop("allow_ips", UNSET))

        is_enabled = d.pop("is_enabled", UNSET)

        _behalf_of_user_info = d.pop("behalf_of_user_info", UNSET)
        behalf_of_user_info: User | Unset
        if isinstance(_behalf_of_user_info, Unset):
            behalf_of_user_info = UNSET
        else:
            behalf_of_user_info = User.from_dict(_behalf_of_user_info)

        api_key = cls(
            type_=type_,
            api_key_id=api_key_id,
            created_time=created_time,
            description=description,
            key_type=key_type,
            key_start=key_start,
            key_value=key_value,
            scope_names=scope_names,
            allow_ips=allow_ips,
            is_enabled=is_enabled,
            behalf_of_user_info=behalf_of_user_info,
        )

        api_key.additional_properties = d
        return api_key

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
