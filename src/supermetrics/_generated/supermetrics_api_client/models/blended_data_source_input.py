from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blended_data_source_input_accounts_item import BlendedDataSourceInputAccountsItem
    from ..models.blended_data_source_input_data_source_settings_item import (
        BlendedDataSourceInputDataSourceSettingsItem,
    )
    from ..models.blended_data_source_input_report_type_settings_item import (
        BlendedDataSourceInputReportTypeSettingsItem,
    )
    from ..models.blended_data_source_input_segments_item import BlendedDataSourceInputSegmentsItem


T = TypeVar("T", bound="BlendedDataSourceInput")


@_attrs_define
class BlendedDataSourceInput:
    """Data source to include in the blend. At least one of `blend_data_source_id` or `blend_data_source_key` must be non-
    null: use `blend_data_source_key` when creating a new data source, `blend_data_source_id` for an existing one.

        Attributes:
            data_source_id (str): Data source identifier (e.g. the connector ID). Example: GA4.
            blend_data_source_id (int | None): Internal ID of the blended data source. Use when updating an existing data
                source in the blend; null when creating a new one. Example: 146715.
            blend_data_source_key (None | str): Temporary key linking a new data source to field/join references within the
                same request. Required when creating a blend. Must be exactly 8 lowercase alphanumeric characters. Example:
                abcd1234.
            report_type (None | str): Report type ID, if the data source supports report types. Example: organic_search.
            report_type_settings (list[BlendedDataSourceInputReportTypeSettingsItem]): Settings specific to the selected
                report type.
            display_name (str | Unset): Display name of the data source. Defaults to the data source name if omitted.
                Example: Google Analytics 4.
            data_source_settings (list[BlendedDataSourceInputDataSourceSettingsItem] | Unset): Settings to apply when
                querying this data source.
            accounts (list[BlendedDataSourceInputAccountsItem] | Unset): Accounts to query from this data source.
            segments (list[BlendedDataSourceInputSegmentsItem] | Unset): Segments to apply when querying this data source.
    """

    data_source_id: str
    blend_data_source_id: int | None
    blend_data_source_key: None | str
    report_type: None | str
    report_type_settings: list[BlendedDataSourceInputReportTypeSettingsItem]
    display_name: str | Unset = UNSET
    data_source_settings: list[BlendedDataSourceInputDataSourceSettingsItem] | Unset = UNSET
    accounts: list[BlendedDataSourceInputAccountsItem] | Unset = UNSET
    segments: list[BlendedDataSourceInputSegmentsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source_id = self.data_source_id

        blend_data_source_id: int | None
        blend_data_source_id = self.blend_data_source_id

        blend_data_source_key: None | str
        blend_data_source_key = self.blend_data_source_key

        report_type: None | str
        report_type = self.report_type

        report_type_settings = []
        for report_type_settings_item_data in self.report_type_settings:
            report_type_settings_item = report_type_settings_item_data.to_dict()
            report_type_settings.append(report_type_settings_item)

        display_name = self.display_name

        data_source_settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_source_settings, Unset):
            data_source_settings = []
            for data_source_settings_item_data in self.data_source_settings:
                data_source_settings_item = data_source_settings_item_data.to_dict()
                data_source_settings.append(data_source_settings_item)

        accounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)

        segments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.segments, Unset):
            segments = []
            for segments_item_data in self.segments:
                segments_item = segments_item_data.to_dict()
                segments.append(segments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_source_id": data_source_id,
                "blend_data_source_id": blend_data_source_id,
                "blend_data_source_key": blend_data_source_key,
                "report_type": report_type,
                "report_type_settings": report_type_settings,
            }
        )
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if data_source_settings is not UNSET:
            field_dict["data_source_settings"] = data_source_settings
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if segments is not UNSET:
            field_dict["segments"] = segments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blended_data_source_input_accounts_item import BlendedDataSourceInputAccountsItem
        from ..models.blended_data_source_input_data_source_settings_item import (
            BlendedDataSourceInputDataSourceSettingsItem,
        )
        from ..models.blended_data_source_input_report_type_settings_item import (
            BlendedDataSourceInputReportTypeSettingsItem,
        )
        from ..models.blended_data_source_input_segments_item import BlendedDataSourceInputSegmentsItem

        d = dict(src_dict)
        data_source_id = d.pop("data_source_id")

        def _parse_blend_data_source_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        blend_data_source_id = _parse_blend_data_source_id(d.pop("blend_data_source_id"))

        def _parse_blend_data_source_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        blend_data_source_key = _parse_blend_data_source_key(d.pop("blend_data_source_key"))

        def _parse_report_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        report_type = _parse_report_type(d.pop("report_type"))

        report_type_settings = []
        _report_type_settings = d.pop("report_type_settings")
        for report_type_settings_item_data in _report_type_settings:
            report_type_settings_item = BlendedDataSourceInputReportTypeSettingsItem.from_dict(
                report_type_settings_item_data
            )

            report_type_settings.append(report_type_settings_item)

        display_name = d.pop("display_name", UNSET)

        _data_source_settings = d.pop("data_source_settings", UNSET)
        data_source_settings: list[BlendedDataSourceInputDataSourceSettingsItem] | Unset = UNSET
        if _data_source_settings is not UNSET:
            data_source_settings = []
            for data_source_settings_item_data in _data_source_settings:
                data_source_settings_item = BlendedDataSourceInputDataSourceSettingsItem.from_dict(
                    data_source_settings_item_data
                )

                data_source_settings.append(data_source_settings_item)

        _accounts = d.pop("accounts", UNSET)
        accounts: list[BlendedDataSourceInputAccountsItem] | Unset = UNSET
        if _accounts is not UNSET:
            accounts = []
            for accounts_item_data in _accounts:
                accounts_item = BlendedDataSourceInputAccountsItem.from_dict(accounts_item_data)

                accounts.append(accounts_item)

        _segments = d.pop("segments", UNSET)
        segments: list[BlendedDataSourceInputSegmentsItem] | Unset = UNSET
        if _segments is not UNSET:
            segments = []
            for segments_item_data in _segments:
                segments_item = BlendedDataSourceInputSegmentsItem.from_dict(segments_item_data)

                segments.append(segments_item)

        blended_data_source_input = cls(
            data_source_id=data_source_id,
            blend_data_source_id=blend_data_source_id,
            blend_data_source_key=blend_data_source_key,
            report_type=report_type,
            report_type_settings=report_type_settings,
            display_name=display_name,
            data_source_settings=data_source_settings,
            accounts=accounts,
            segments=segments,
        )

        blended_data_source_input.additional_properties = d
        return blended_data_source_input

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
