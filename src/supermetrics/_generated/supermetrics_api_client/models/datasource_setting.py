from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.datasource_setting_context import DatasourceSettingContext, check_datasource_setting_context
from ..models.datasource_setting_type import DatasourceSettingType, check_datasource_setting_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datasource_option import DatasourceOption


T = TypeVar("T", bound="DatasourceSetting")


@_attrs_define
class DatasourceSetting:
    """
    Attributes:
        setting_id (str | Unset):
        context (DatasourceSettingContext | Unset):
        type_ (DatasourceSettingType | Unset):
        label (str | Unset):
        help_text (None | str | Unset):
        default_value (None | str | Unset):
        options (list[DatasourceOption] | Unset):
        is_value_required (bool | Unset):
    """

    setting_id: str | Unset = UNSET
    context: DatasourceSettingContext | Unset = UNSET
    type_: DatasourceSettingType | Unset = UNSET
    label: str | Unset = UNSET
    help_text: None | str | Unset = UNSET
    default_value: None | str | Unset = UNSET
    options: list[DatasourceOption] | Unset = UNSET
    is_value_required: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        setting_id = self.setting_id

        context: str | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        label = self.label

        help_text: None | str | Unset
        if isinstance(self.help_text, Unset):
            help_text = UNSET
        else:
            help_text = self.help_text

        default_value: None | str | Unset
        if isinstance(self.default_value, Unset):
            default_value = UNSET
        else:
            default_value = self.default_value

        options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        is_value_required = self.is_value_required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if setting_id is not UNSET:
            field_dict["setting_id"] = setting_id
        if context is not UNSET:
            field_dict["context"] = context
        if type_ is not UNSET:
            field_dict["type"] = type_
        if label is not UNSET:
            field_dict["label"] = label
        if help_text is not UNSET:
            field_dict["help_text"] = help_text
        if default_value is not UNSET:
            field_dict["default_value"] = default_value
        if options is not UNSET:
            field_dict["options"] = options
        if is_value_required is not UNSET:
            field_dict["is_value_required"] = is_value_required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datasource_option import DatasourceOption

        d = dict(src_dict)
        setting_id = d.pop("setting_id", UNSET)

        _context = d.pop("context", UNSET)
        context: DatasourceSettingContext | Unset
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = check_datasource_setting_context(_context)

        _type_ = d.pop("type", UNSET)
        type_: DatasourceSettingType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_datasource_setting_type(_type_)

        label = d.pop("label", UNSET)

        def _parse_help_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        help_text = _parse_help_text(d.pop("help_text", UNSET))

        def _parse_default_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_value = _parse_default_value(d.pop("default_value", UNSET))

        _options = d.pop("options", UNSET)
        options: list[DatasourceOption] | Unset = UNSET
        if _options is not UNSET:
            options = []
            for options_item_data in _options:
                options_item = DatasourceOption.from_dict(options_item_data)

                options.append(options_item)

        is_value_required = d.pop("is_value_required", UNSET)

        datasource_setting = cls(
            setting_id=setting_id,
            context=context,
            type_=type_,
            label=label,
            help_text=help_text,
            default_value=default_value,
            options=options,
            is_value_required=is_value_required,
        )

        datasource_setting.additional_properties = d
        return datasource_setting

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
