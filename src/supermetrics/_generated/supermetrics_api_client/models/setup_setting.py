from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.setup_setting_options_item import SetupSettingOptionsItem
    from ..models.setup_setting_show_for_item import SetupSettingShowForItem


T = TypeVar("T", bound="SetupSetting")


@_attrs_define
class SetupSetting:
    """
    Attributes:
        id (str): Unique identifier for the setting Example: hostname.
        input_type (str): Type of input control Example: text.
        is_required (bool): Whether this setting is required Example: True.
        label (None | str | Unset): Display label for the setting Example: Hostname.
        value (bool | int | None | str | Unset): Current value of the setting (type varies based on input_type) Example:
            myaccount.snowflakecomputing.com.
        options (list[SetupSettingOptionsItem] | Unset): Available options for select/radio inputs
        help_text (None | str | Unset): Help text for the setting
        help_url (None | str | Unset): URL to additional help documentation
        note (None | str | Unset): Additional notes about the setting
        group (str | Unset): Group identifier for organizing settings
        group_label (str | Unset): Display label for the group
        show_for (list[SetupSettingShowForItem] | Unset): Conditional display rules
    """

    id: str
    input_type: str
    is_required: bool
    label: None | str | Unset = UNSET
    value: bool | int | None | str | Unset = UNSET
    options: list[SetupSettingOptionsItem] | Unset = UNSET
    help_text: None | str | Unset = UNSET
    help_url: None | str | Unset = UNSET
    note: None | str | Unset = UNSET
    group: str | Unset = UNSET
    group_label: str | Unset = UNSET
    show_for: list[SetupSettingShowForItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        input_type = self.input_type

        is_required = self.is_required

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        value: bool | int | None | str | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        help_text: None | str | Unset
        if isinstance(self.help_text, Unset):
            help_text = UNSET
        else:
            help_text = self.help_text

        help_url: None | str | Unset
        if isinstance(self.help_url, Unset):
            help_url = UNSET
        else:
            help_url = self.help_url

        note: None | str | Unset
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        group = self.group

        group_label = self.group_label

        show_for: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.show_for, Unset):
            show_for = []
            for show_for_item_data in self.show_for:
                show_for_item = show_for_item_data.to_dict()
                show_for.append(show_for_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "input_type": input_type,
                "is_required": is_required,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if value is not UNSET:
            field_dict["value"] = value
        if options is not UNSET:
            field_dict["options"] = options
        if help_text is not UNSET:
            field_dict["help_text"] = help_text
        if help_url is not UNSET:
            field_dict["help_url"] = help_url
        if note is not UNSET:
            field_dict["note"] = note
        if group is not UNSET:
            field_dict["group"] = group
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if show_for is not UNSET:
            field_dict["show_for"] = show_for

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_setting_options_item import SetupSettingOptionsItem
        from ..models.setup_setting_show_for_item import SetupSettingShowForItem

        d = dict(src_dict)
        id = d.pop("id")

        input_type = d.pop("input_type")

        is_required = d.pop("is_required")

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_value(data: object) -> bool | int | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | int | None | str | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        _options = d.pop("options", UNSET)
        options: list[SetupSettingOptionsItem] | Unset = UNSET
        if _options is not UNSET:
            options = []
            for options_item_data in _options:
                options_item = SetupSettingOptionsItem.from_dict(options_item_data)

                options.append(options_item)

        def _parse_help_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        help_text = _parse_help_text(d.pop("help_text", UNSET))

        def _parse_help_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        help_url = _parse_help_url(d.pop("help_url", UNSET))

        def _parse_note(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        note = _parse_note(d.pop("note", UNSET))

        group = d.pop("group", UNSET)

        group_label = d.pop("group_label", UNSET)

        _show_for = d.pop("show_for", UNSET)
        show_for: list[SetupSettingShowForItem] | Unset = UNSET
        if _show_for is not UNSET:
            show_for = []
            for show_for_item_data in _show_for:
                show_for_item = SetupSettingShowForItem.from_dict(show_for_item_data)

                show_for.append(show_for_item)

        setup_setting = cls(
            id=id,
            input_type=input_type,
            is_required=is_required,
            label=label,
            value=value,
            options=options,
            help_text=help_text,
            help_url=help_url,
            note=note,
            group=group,
            group_label=group_label,
            show_for=show_for,
        )

        return setup_setting
