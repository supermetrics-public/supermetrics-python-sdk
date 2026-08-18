from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.destination_type_settings_auth_methods_item import DestinationTypeSettingsAuthMethodsItem
    from ..models.destination_type_settings_settings_item import DestinationTypeSettingsSettingsItem


T = TypeVar("T", bound="DestinationTypeSettings")


@_attrs_define
class DestinationTypeSettings:
    """Configuration settings for a destination type

    Attributes:
        title (str | Unset): Human-readable title Example: BigQuery.
        type_ (str | Unset): Destination type identifier Example: SQL_BQ.
        connection_check_url (str | Unset): URL endpoint to validate connection
        create_url (str | Unset): URL to create new destination instance
        update_url_template (str | Unset): URL template to update existing destination
        icon_url (str | Unset): URL to destination icon
        app_id (str | Unset): OAuth application ID
        is_internal (bool | Unset): Whether this destination type is for internal use only
        settings (list[DestinationTypeSettingsSettingsItem] | Unset): Setup configuration fields
        auth_methods (list[DestinationTypeSettingsAuthMethodsItem] | Unset): Available authentication methods
    """

    title: str | Unset = UNSET
    type_: str | Unset = UNSET
    connection_check_url: str | Unset = UNSET
    create_url: str | Unset = UNSET
    update_url_template: str | Unset = UNSET
    icon_url: str | Unset = UNSET
    app_id: str | Unset = UNSET
    is_internal: bool | Unset = UNSET
    settings: list[DestinationTypeSettingsSettingsItem] | Unset = UNSET
    auth_methods: list[DestinationTypeSettingsAuthMethodsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        type_ = self.type_

        connection_check_url = self.connection_check_url

        create_url = self.create_url

        update_url_template = self.update_url_template

        icon_url = self.icon_url

        app_id = self.app_id

        is_internal = self.is_internal

        settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)

        auth_methods: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.auth_methods, Unset):
            auth_methods = []
            for auth_methods_item_data in self.auth_methods:
                auth_methods_item = auth_methods_item_data.to_dict()
                auth_methods.append(auth_methods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if type_ is not UNSET:
            field_dict["type"] = type_
        if connection_check_url is not UNSET:
            field_dict["connection_check_url"] = connection_check_url
        if create_url is not UNSET:
            field_dict["create_url"] = create_url
        if update_url_template is not UNSET:
            field_dict["update_url_template"] = update_url_template
        if icon_url is not UNSET:
            field_dict["icon_url"] = icon_url
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if is_internal is not UNSET:
            field_dict["is_internal"] = is_internal
        if settings is not UNSET:
            field_dict["settings"] = settings
        if auth_methods is not UNSET:
            field_dict["auth_methods"] = auth_methods

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_type_settings_auth_methods_item import DestinationTypeSettingsAuthMethodsItem
        from ..models.destination_type_settings_settings_item import DestinationTypeSettingsSettingsItem

        d = dict(src_dict)
        title = d.pop("title", UNSET)

        type_ = d.pop("type", UNSET)

        connection_check_url = d.pop("connection_check_url", UNSET)

        create_url = d.pop("create_url", UNSET)

        update_url_template = d.pop("update_url_template", UNSET)

        icon_url = d.pop("icon_url", UNSET)

        app_id = d.pop("app_id", UNSET)

        is_internal = d.pop("is_internal", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: list[DestinationTypeSettingsSettingsItem] | Unset = UNSET
        if _settings is not UNSET:
            settings = []
            for settings_item_data in _settings:
                settings_item = DestinationTypeSettingsSettingsItem.from_dict(settings_item_data)

                settings.append(settings_item)

        _auth_methods = d.pop("auth_methods", UNSET)
        auth_methods: list[DestinationTypeSettingsAuthMethodsItem] | Unset = UNSET
        if _auth_methods is not UNSET:
            auth_methods = []
            for auth_methods_item_data in _auth_methods:
                auth_methods_item = DestinationTypeSettingsAuthMethodsItem.from_dict(auth_methods_item_data)

                auth_methods.append(auth_methods_item)

        destination_type_settings = cls(
            title=title,
            type_=type_,
            connection_check_url=connection_check_url,
            create_url=create_url,
            update_url_template=update_url_template,
            icon_url=icon_url,
            app_id=app_id,
            is_internal=is_internal,
            settings=settings,
            auth_methods=auth_methods,
        )

        destination_type_settings.additional_properties = d
        return destination_type_settings

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
