from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blended_data_source_output_accounts import BlendedDataSourceOutputAccounts
    from ..models.blended_data_source_output_data_source_settings import BlendedDataSourceOutputDataSourceSettings
    from ..models.blended_data_source_output_report_type_settings import BlendedDataSourceOutputReportTypeSettings
    from ..models.blended_data_source_output_segments import BlendedDataSourceOutputSegments


T = TypeVar("T", bound="BlendedDataSourceOutput")


@_attrs_define
class BlendedDataSourceOutput:
    """A data source included in the blend response, with field mappings and account details.

    Attributes:
        blend_data_source_id (int | Unset): Internal ID of the blended data source. Example: 1.
        blend_id (int | Unset): ID of the blend this data source belongs to. Example: 569.
        data_source_id (str | Unset): Data source identifier. Example: GA4.
        display_name (str | Unset): Display name of the data source. Example: Google Analytics 4.
        data_source_settings (BlendedDataSourceOutputDataSourceSettings | Unset): Settings applied when querying this
            data source.
        accounts (BlendedDataSourceOutputAccounts | Unset): Accounts queried from this data source.
        segments (BlendedDataSourceOutputSegments | Unset): Segments applied when querying this data source.
        report_type (None | str | Unset): Report type ID. Example: organic_search.
        report_type_settings (BlendedDataSourceOutputReportTypeSettings | Unset): Settings for the selected report type.
        logo_url (str | Unset): Data source logo URL. Example: https://cdn.supermetrics.com/images/datasource-
            logos/GA4.png.
    """

    blend_data_source_id: int | Unset = UNSET
    blend_id: int | Unset = UNSET
    data_source_id: str | Unset = UNSET
    display_name: str | Unset = UNSET
    data_source_settings: BlendedDataSourceOutputDataSourceSettings | Unset = UNSET
    accounts: BlendedDataSourceOutputAccounts | Unset = UNSET
    segments: BlendedDataSourceOutputSegments | Unset = UNSET
    report_type: None | str | Unset = UNSET
    report_type_settings: BlendedDataSourceOutputReportTypeSettings | Unset = UNSET
    logo_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_data_source_id = self.blend_data_source_id

        blend_id = self.blend_id

        data_source_id = self.data_source_id

        display_name = self.display_name

        data_source_settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data_source_settings, Unset):
            data_source_settings = self.data_source_settings.to_dict()

        accounts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts.to_dict()

        segments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.segments, Unset):
            segments = self.segments.to_dict()

        report_type: None | str | Unset
        if isinstance(self.report_type, Unset):
            report_type = UNSET
        else:
            report_type = self.report_type

        report_type_settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.report_type_settings, Unset):
            report_type_settings = self.report_type_settings.to_dict()

        logo_url = self.logo_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blend_data_source_id is not UNSET:
            field_dict["blend_data_source_id"] = blend_data_source_id
        if blend_id is not UNSET:
            field_dict["blend_id"] = blend_id
        if data_source_id is not UNSET:
            field_dict["data_source_id"] = data_source_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if data_source_settings is not UNSET:
            field_dict["data_source_settings"] = data_source_settings
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if segments is not UNSET:
            field_dict["segments"] = segments
        if report_type is not UNSET:
            field_dict["report_type"] = report_type
        if report_type_settings is not UNSET:
            field_dict["report_type_settings"] = report_type_settings
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blended_data_source_output_accounts import BlendedDataSourceOutputAccounts
        from ..models.blended_data_source_output_data_source_settings import BlendedDataSourceOutputDataSourceSettings
        from ..models.blended_data_source_output_report_type_settings import BlendedDataSourceOutputReportTypeSettings
        from ..models.blended_data_source_output_segments import BlendedDataSourceOutputSegments

        d = dict(src_dict)
        blend_data_source_id = d.pop("blend_data_source_id", UNSET)

        blend_id = d.pop("blend_id", UNSET)

        data_source_id = d.pop("data_source_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        _data_source_settings = d.pop("data_source_settings", UNSET)
        data_source_settings: BlendedDataSourceOutputDataSourceSettings | Unset
        if isinstance(_data_source_settings, Unset):
            data_source_settings = UNSET
        else:
            data_source_settings = BlendedDataSourceOutputDataSourceSettings.from_dict(_data_source_settings)

        _accounts = d.pop("accounts", UNSET)
        accounts: BlendedDataSourceOutputAccounts | Unset
        if isinstance(_accounts, Unset):
            accounts = UNSET
        else:
            accounts = BlendedDataSourceOutputAccounts.from_dict(_accounts)

        _segments = d.pop("segments", UNSET)
        segments: BlendedDataSourceOutputSegments | Unset
        if isinstance(_segments, Unset):
            segments = UNSET
        else:
            segments = BlendedDataSourceOutputSegments.from_dict(_segments)

        def _parse_report_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        report_type = _parse_report_type(d.pop("report_type", UNSET))

        _report_type_settings = d.pop("report_type_settings", UNSET)
        report_type_settings: BlendedDataSourceOutputReportTypeSettings | Unset
        if isinstance(_report_type_settings, Unset):
            report_type_settings = UNSET
        else:
            report_type_settings = BlendedDataSourceOutputReportTypeSettings.from_dict(_report_type_settings)

        logo_url = d.pop("logo_url", UNSET)

        blended_data_source_output = cls(
            blend_data_source_id=blend_data_source_id,
            blend_id=blend_id,
            data_source_id=data_source_id,
            display_name=display_name,
            data_source_settings=data_source_settings,
            accounts=accounts,
            segments=segments,
            report_type=report_type,
            report_type_settings=report_type_settings,
            logo_url=logo_url,
        )

        blended_data_source_output.additional_properties = d
        return blended_data_source_output

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
