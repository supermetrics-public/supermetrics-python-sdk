from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.datasource_setting_context import DatasourceSettingContext
from ..models.datasource_setting_type import DatasourceSettingType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datasource_option import DatasourceOption


T = TypeVar("T", bound="DatasourceSetting")


@_attrs_define
class DatasourceSetting:
    """
    Attributes:
        setting_id (str | Unset): Unique identifier for the setting, using the v2 API key format Example:
            blanks_to_zero.
        context (DatasourceSettingContext | Unset): The context in which the setting is applied. Example: options.
        type_ (DatasourceSettingType | Unset): UI component type Example: checkbox.
        label (str | Unset): Human-readable label for the setting Example: Replace blank metric values with zeros.
        help_text (None | str | Unset): Optional helper text shown to users Example: When you're splitting the data by a
            time dimension, using this setting ensures all time values (dates / weeks / months / years) will be returned,
            even if there's no data for some of them..
        default_value (Any | Unset): Optional default value; type depends on the setting type
        options (list[DatasourceOption] | Unset): Zero or more selectable options, applicable when type is
            select/multiselect
        is_value_required (bool | Unset): Whether a value is mandatory for this setting
    """

    setting_id: str | Unset = UNSET
    context: DatasourceSettingContext | Unset = UNSET
    type_: DatasourceSettingType | Unset = UNSET
    label: str | Unset = UNSET
    help_text: None | str | Unset = UNSET
    default_value: Any | Unset = UNSET
    options: list[DatasourceOption] | Unset = UNSET
    is_value_required: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        setting_id = self.setting_id

        context: str | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.value

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        label = self.label

        help_text: None | str | Unset
        if isinstance(self.help_text, Unset):
            help_text = UNSET
        else:
            help_text = self.help_text

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
            context = DatasourceSettingContext(_context)

        _type_ = d.pop("type", UNSET)
        type_: DatasourceSettingType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = DatasourceSettingType(_type_)

        label = d.pop("label", UNSET)

        def _parse_help_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        help_text = _parse_help_text(d.pop("help_text", UNSET))

        default_value = d.pop("default_value", UNSET)

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
