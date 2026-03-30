from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datasource_setting import DatasourceSetting


T = TypeVar("T", bound="DatasourceReportType")


@_attrs_define
class DatasourceReportType:
    """
    Attributes:
        label (str | Unset): Human-readable report type name Example: Cohort Daily.
        id (str | Unset): Unique identifier for the report type Example: CohortDaily.
        is_date_range_required (bool | Unset): Whether date range selection is required for this specific report type
        is_free_text_account_required (bool | Unset): Whether this report type requires free-text account input (e.g.,
            page aliases, URLs) Example: True.
        settings (list[DatasourceSetting] | Unset): List of settings applicable to this report type
    """

    label: str | Unset = UNSET
    id: str | Unset = UNSET
    is_date_range_required: bool | Unset = UNSET
    is_free_text_account_required: bool | Unset = UNSET
    settings: list[DatasourceSetting] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        id = self.id

        is_date_range_required = self.is_date_range_required

        is_free_text_account_required = self.is_free_text_account_required

        settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if id is not UNSET:
            field_dict["id"] = id
        if is_date_range_required is not UNSET:
            field_dict["is_date_range_required"] = is_date_range_required
        if is_free_text_account_required is not UNSET:
            field_dict["is_free_text_account_required"] = is_free_text_account_required
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datasource_setting import DatasourceSetting

        d = dict(src_dict)
        label = d.pop("label", UNSET)

        id = d.pop("id", UNSET)

        is_date_range_required = d.pop("is_date_range_required", UNSET)

        is_free_text_account_required = d.pop("is_free_text_account_required", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: list[DatasourceSetting] | Unset = UNSET
        if _settings is not UNSET:
            settings = []
            for settings_item_data in _settings:
                settings_item = DatasourceSetting.from_dict(settings_item_data)

                settings.append(settings_item)

        datasource_report_type = cls(
            label=label,
            id=id,
            is_date_range_required=is_date_range_required,
            is_free_text_account_required=is_free_text_account_required,
            settings=settings,
        )

        datasource_report_type.additional_properties = d
        return datasource_report_type

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
