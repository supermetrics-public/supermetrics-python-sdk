from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.setup_setting import SetupSetting


T = TypeVar("T", bound="AuthMethod")


@_attrs_define
class AuthMethod:
    """
    Attributes:
        id (str): Authentication method identifier Example: AUTH_METHOD_KEY_PAIR.
        title (str): Display title for the authentication method Example: Key Pair Authentication.
        fields (list[SetupSetting] | Unset): Settings the user must fill in to use this authentication method.
        new_secret_field (SetupSetting | Unset):
        is_default (bool | Unset): Whether this is the default authentication method Default: False.
    """

    id: str
    title: str
    fields: list[SetupSetting] | Unset = UNSET
    new_secret_field: SetupSetting | Unset = UNSET
    is_default: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)

        new_secret_field: dict[str, Any] | Unset = UNSET
        if not isinstance(self.new_secret_field, Unset):
            new_secret_field = self.new_secret_field.to_dict()

        is_default = self.is_default

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields
        if new_secret_field is not UNSET:
            field_dict["new_secret_field"] = new_secret_field
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_setting import SetupSetting

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        _fields = d.pop("fields", UNSET)
        fields: list[SetupSetting] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = SetupSetting.from_dict(fields_item_data)

                fields.append(fields_item)

        _new_secret_field = d.pop("new_secret_field", UNSET)
        new_secret_field: SetupSetting | Unset
        if isinstance(_new_secret_field, Unset):
            new_secret_field = UNSET
        else:
            new_secret_field = SetupSetting.from_dict(_new_secret_field)

        is_default = d.pop("is_default", UNSET)

        auth_method = cls(
            id=id,
            title=title,
            fields=fields,
            new_secret_field=new_secret_field,
            is_default=is_default,
        )

        return auth_method
