from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auth_method import AuthMethod
    from ..models.setup_setting import SetupSetting


T = TypeVar("T", bound="DestinationType")


@_attrs_define
class DestinationType:
    """
    Attributes:
        type_ (str): Destination type identifier Example: DWH_SNOWFLAKE.
        title (str): Display name for the destination type Example: Snowflake.
        icon_url (str): URL to the destination type icon Example: https://supermetrics.com/icons/snowflake.svg.
        connection_check_url (str | Unset): URL for connection testing
        create_url (str | Unset): URL for creating a destination
        update_url_template (str | Unset): URL template for updating a destination
        app_id (str | Unset): Application identifier
        is_internal (bool | Unset): Whether this is an internal destination type Default: False.
        settings (list[SetupSetting] | Unset): Available settings for this destination type
        auth_methods (list[AuthMethod] | Unset): Available authentication methods
    """

    type_: str
    title: str
    icon_url: str
    connection_check_url: str | Unset = UNSET
    create_url: str | Unset = UNSET
    update_url_template: str | Unset = UNSET
    app_id: str | Unset = UNSET
    is_internal: bool | Unset = False
    settings: list[SetupSetting] | Unset = UNSET
    auth_methods: list[AuthMethod] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        icon_url = self.icon_url

        connection_check_url = self.connection_check_url

        create_url = self.create_url

        update_url_template = self.update_url_template

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

        field_dict.update(
            {
                "type": type_,
                "title": title,
                "icon_url": icon_url,
            }
        )
        if connection_check_url is not UNSET:
            field_dict["connection_check_url"] = connection_check_url
        if create_url is not UNSET:
            field_dict["create_url"] = create_url
        if update_url_template is not UNSET:
            field_dict["update_url_template"] = update_url_template
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
        from ..models.auth_method import AuthMethod
        from ..models.setup_setting import SetupSetting

        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        icon_url = d.pop("icon_url")

        connection_check_url = d.pop("connection_check_url", UNSET)

        create_url = d.pop("create_url", UNSET)

        update_url_template = d.pop("update_url_template", UNSET)

        app_id = d.pop("app_id", UNSET)

        is_internal = d.pop("is_internal", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: list[SetupSetting] | Unset = UNSET
        if _settings is not UNSET:
            settings = []
            for settings_item_data in _settings:
                settings_item = SetupSetting.from_dict(settings_item_data)

                settings.append(settings_item)

        _auth_methods = d.pop("auth_methods", UNSET)
        auth_methods: list[AuthMethod] | Unset = UNSET
        if _auth_methods is not UNSET:
            auth_methods = []
            for auth_methods_item_data in _auth_methods:
                auth_methods_item = AuthMethod.from_dict(auth_methods_item_data)

                auth_methods.append(auth_methods_item)

        destination_type = cls(
            type_=type_,
            title=title,
            icon_url=icon_url,
            connection_check_url=connection_check_url,
            create_url=create_url,
            update_url_template=update_url_template,
            app_id=app_id,
            is_internal=is_internal,
            settings=settings,
            auth_methods=auth_methods,
        )

        return destination_type
