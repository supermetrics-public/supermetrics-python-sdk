from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.datasource_details_categories_item import DatasourceDetailsCategoriesItem
from ..models.datasource_details_status import DatasourceDetailsStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datasource_details_account_labels_type_0 import DatasourceDetailsAccountLabelsType0
    from ..models.datasource_report_type import DatasourceReportType
    from ..models.datasource_setting import DatasourceSetting


T = TypeVar("T", bound="DatasourceDetails")


@_attrs_define
class DatasourceDetails:
    """
    Attributes:
        id (str | Unset): Unique identifier of the datasource (e.g., "GAWA", "AW", "SA360") Example: GAWA.
        name (str | Unset): Human-readable name of the datasource Example: Google Analytics 4.
        description (str | Unset): Detailed description of the datasource and its capabilities Example: A web analytics
            service for tracking website traffic and user behavior, with a focus on AI and machine learning..
        marketing_name (None | str | Unset): Connector marketing name Example: Google Analytics.
        logo_url (str | Unset): Connector logo URL Example: https://assets.supermetrics.com/images/dsLogos/GAWA.png.
        categories (list[DatasourceDetailsCategoriesItem] | Unset): Categories that this datasource belongs to Example:
            ['ANALYTICS'].
        products (list[str] | Unset): List of products where this datasource is available Example: ['API', 'DS',
            'SHEETS', 'EXCEL', 'DWH'].
        status (DatasourceDetailsStatus | Unset): Connector release status Example: Released.
        is_premium (bool | Unset): Is connector premium
        tags (list[str] | Unset): Tags associated with this datasource (e.g., "popular") Example: ['popular'].
        is_authentication_required (bool | Unset): Whether this datasource requires authentication to use Example: True.
        has_account_list (bool | Unset): Whether this datasource has account-level resources that can be selected
            Example: True.
        has_fields (bool | Unset): Whether this datasource has field selection capabilities Example: True.
        has_segments (bool | Unset): Indicates if the data source supports segments
        has_report_type_selection (bool | Unset): Whether the report type selection UI should be shown to users
        is_date_range_required (bool | Unset): Whether date range selection is applicable at the datasource level (can
            be overridden by report types) Example: True.
        is_custom_data_import (bool | Unset): Indicates if the data source supports custom data import
        min_metrics (int | None | Unset): Minimum number of metrics required for the data source query Example: 1.
        max_metrics (int | None | Unset): Maximum number of metrics allowed for the data source query Example: 10.
        min_dimensions (int | None | Unset): Minimum number of dimensions required for the data source query
        max_dimensions (int | None | Unset): Maximum number of dimensions allowed for the data source query Example: 9.
        report_type_header_label (str | Unset): Dynamic label used for UI to show what the report type header should be
            called Example: Report Type.
        account_labels (DatasourceDetailsAccountLabelsType0 | None | Unset): Labels for the accounts
        report_types (list[DatasourceReportType] | Unset): Available report types for this datasource
        common_settings (list[DatasourceSetting] | Unset): General settings not tied to a specific report type
    """

    id: str | Unset = UNSET
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    marketing_name: None | str | Unset = UNSET
    logo_url: str | Unset = UNSET
    categories: list[DatasourceDetailsCategoriesItem] | Unset = UNSET
    products: list[str] | Unset = UNSET
    status: DatasourceDetailsStatus | Unset = UNSET
    is_premium: bool | Unset = UNSET
    tags: list[str] | Unset = UNSET
    is_authentication_required: bool | Unset = UNSET
    has_account_list: bool | Unset = UNSET
    has_fields: bool | Unset = UNSET
    has_segments: bool | Unset = UNSET
    has_report_type_selection: bool | Unset = UNSET
    is_date_range_required: bool | Unset = UNSET
    is_custom_data_import: bool | Unset = UNSET
    min_metrics: int | None | Unset = UNSET
    max_metrics: int | None | Unset = UNSET
    min_dimensions: int | None | Unset = UNSET
    max_dimensions: int | None | Unset = UNSET
    report_type_header_label: str | Unset = UNSET
    account_labels: DatasourceDetailsAccountLabelsType0 | None | Unset = UNSET
    report_types: list[DatasourceReportType] | Unset = UNSET
    common_settings: list[DatasourceSetting] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.datasource_details_account_labels_type_0 import DatasourceDetailsAccountLabelsType0

        id = self.id

        name = self.name

        description = self.description

        marketing_name: None | str | Unset
        if isinstance(self.marketing_name, Unset):
            marketing_name = UNSET
        else:
            marketing_name = self.marketing_name

        logo_url = self.logo_url

        categories: list[str] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.value
                categories.append(categories_item)

        products: list[str] | Unset = UNSET
        if not isinstance(self.products, Unset):
            products = self.products

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        is_premium = self.is_premium

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        is_authentication_required = self.is_authentication_required

        has_account_list = self.has_account_list

        has_fields = self.has_fields

        has_segments = self.has_segments

        has_report_type_selection = self.has_report_type_selection

        is_date_range_required = self.is_date_range_required

        is_custom_data_import = self.is_custom_data_import

        min_metrics: int | None | Unset
        if isinstance(self.min_metrics, Unset):
            min_metrics = UNSET
        else:
            min_metrics = self.min_metrics

        max_metrics: int | None | Unset
        if isinstance(self.max_metrics, Unset):
            max_metrics = UNSET
        else:
            max_metrics = self.max_metrics

        min_dimensions: int | None | Unset
        if isinstance(self.min_dimensions, Unset):
            min_dimensions = UNSET
        else:
            min_dimensions = self.min_dimensions

        max_dimensions: int | None | Unset
        if isinstance(self.max_dimensions, Unset):
            max_dimensions = UNSET
        else:
            max_dimensions = self.max_dimensions

        report_type_header_label = self.report_type_header_label

        account_labels: dict[str, Any] | None | Unset
        if isinstance(self.account_labels, Unset):
            account_labels = UNSET
        elif isinstance(self.account_labels, DatasourceDetailsAccountLabelsType0):
            account_labels = self.account_labels.to_dict()
        else:
            account_labels = self.account_labels

        report_types: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.report_types, Unset):
            report_types = []
            for report_types_item_data in self.report_types:
                report_types_item = report_types_item_data.to_dict()
                report_types.append(report_types_item)

        common_settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.common_settings, Unset):
            common_settings = []
            for common_settings_item_data in self.common_settings:
                common_settings_item = common_settings_item_data.to_dict()
                common_settings.append(common_settings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if marketing_name is not UNSET:
            field_dict["marketing_name"] = marketing_name
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if categories is not UNSET:
            field_dict["categories"] = categories
        if products is not UNSET:
            field_dict["products"] = products
        if status is not UNSET:
            field_dict["status"] = status
        if is_premium is not UNSET:
            field_dict["is_premium"] = is_premium
        if tags is not UNSET:
            field_dict["tags"] = tags
        if is_authentication_required is not UNSET:
            field_dict["is_authentication_required"] = is_authentication_required
        if has_account_list is not UNSET:
            field_dict["has_account_list"] = has_account_list
        if has_fields is not UNSET:
            field_dict["has_fields"] = has_fields
        if has_segments is not UNSET:
            field_dict["has_segments"] = has_segments
        if has_report_type_selection is not UNSET:
            field_dict["has_report_type_selection"] = has_report_type_selection
        if is_date_range_required is not UNSET:
            field_dict["is_date_range_required"] = is_date_range_required
        if is_custom_data_import is not UNSET:
            field_dict["is_custom_data_import"] = is_custom_data_import
        if min_metrics is not UNSET:
            field_dict["min_metrics"] = min_metrics
        if max_metrics is not UNSET:
            field_dict["max_metrics"] = max_metrics
        if min_dimensions is not UNSET:
            field_dict["min_dimensions"] = min_dimensions
        if max_dimensions is not UNSET:
            field_dict["max_dimensions"] = max_dimensions
        if report_type_header_label is not UNSET:
            field_dict["report_type_header_label"] = report_type_header_label
        if account_labels is not UNSET:
            field_dict["account_labels"] = account_labels
        if report_types is not UNSET:
            field_dict["report_types"] = report_types
        if common_settings is not UNSET:
            field_dict["common_settings"] = common_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datasource_details_account_labels_type_0 import DatasourceDetailsAccountLabelsType0
        from ..models.datasource_report_type import DatasourceReportType
        from ..models.datasource_setting import DatasourceSetting

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        def _parse_marketing_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        marketing_name = _parse_marketing_name(d.pop("marketing_name", UNSET))

        logo_url = d.pop("logo_url", UNSET)

        _categories = d.pop("categories", UNSET)
        categories: list[DatasourceDetailsCategoriesItem] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = DatasourceDetailsCategoriesItem(categories_item_data)

                categories.append(categories_item)

        products = cast(list[str], d.pop("products", UNSET))

        _status = d.pop("status", UNSET)
        status: DatasourceDetailsStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DatasourceDetailsStatus(_status)

        is_premium = d.pop("is_premium", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        is_authentication_required = d.pop("is_authentication_required", UNSET)

        has_account_list = d.pop("has_account_list", UNSET)

        has_fields = d.pop("has_fields", UNSET)

        has_segments = d.pop("has_segments", UNSET)

        has_report_type_selection = d.pop("has_report_type_selection", UNSET)

        is_date_range_required = d.pop("is_date_range_required", UNSET)

        is_custom_data_import = d.pop("is_custom_data_import", UNSET)

        def _parse_min_metrics(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        min_metrics = _parse_min_metrics(d.pop("min_metrics", UNSET))

        def _parse_max_metrics(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_metrics = _parse_max_metrics(d.pop("max_metrics", UNSET))

        def _parse_min_dimensions(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        min_dimensions = _parse_min_dimensions(d.pop("min_dimensions", UNSET))

        def _parse_max_dimensions(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_dimensions = _parse_max_dimensions(d.pop("max_dimensions", UNSET))

        report_type_header_label = d.pop("report_type_header_label", UNSET)

        def _parse_account_labels(data: object) -> DatasourceDetailsAccountLabelsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                account_labels_type_0 = DatasourceDetailsAccountLabelsType0.from_dict(data)

                return account_labels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DatasourceDetailsAccountLabelsType0 | None | Unset, data)

        account_labels = _parse_account_labels(d.pop("account_labels", UNSET))

        _report_types = d.pop("report_types", UNSET)
        report_types: list[DatasourceReportType] | Unset = UNSET
        if _report_types is not UNSET:
            report_types = []
            for report_types_item_data in _report_types:
                report_types_item = DatasourceReportType.from_dict(report_types_item_data)

                report_types.append(report_types_item)

        _common_settings = d.pop("common_settings", UNSET)
        common_settings: list[DatasourceSetting] | Unset = UNSET
        if _common_settings is not UNSET:
            common_settings = []
            for common_settings_item_data in _common_settings:
                common_settings_item = DatasourceSetting.from_dict(common_settings_item_data)

                common_settings.append(common_settings_item)

        datasource_details = cls(
            id=id,
            name=name,
            description=description,
            marketing_name=marketing_name,
            logo_url=logo_url,
            categories=categories,
            products=products,
            status=status,
            is_premium=is_premium,
            tags=tags,
            is_authentication_required=is_authentication_required,
            has_account_list=has_account_list,
            has_fields=has_fields,
            has_segments=has_segments,
            has_report_type_selection=has_report_type_selection,
            is_date_range_required=is_date_range_required,
            is_custom_data_import=is_custom_data_import,
            min_metrics=min_metrics,
            max_metrics=max_metrics,
            min_dimensions=min_dimensions,
            max_dimensions=max_dimensions,
            report_type_header_label=report_type_header_label,
            account_labels=account_labels,
            report_types=report_types,
            common_settings=common_settings,
        )

        datasource_details.additional_properties = d
        return datasource_details

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
