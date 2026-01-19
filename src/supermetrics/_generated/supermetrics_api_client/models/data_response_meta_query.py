from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.data_response_meta_query_settings import DataResponseMetaQuerySettings
  from ..models.data_response_meta_query_fields_item import DataResponseMetaQueryFieldsItem





T = TypeVar("T", bound="DataResponseMetaQuery")



@_attrs_define
class DataResponseMetaQuery:
    """ 
        Attributes:
            start_date (str | Unset): Query start date in YYYY-MM-DD format
            end_date (str | Unset): Query end date in YYYY-MM-DD format
            ds_accounts (list[str] | Unset): Data source account IDs used in the query
            ds_segments (list[str] | Unset): Data source segment IDs used in the query
            fields (list[DataResponseMetaQueryFieldsItem] | Unset):
            compare_type (str | Unset): Date range comparison type used
            compare_show (str | Unset): Display type for comparison values
            compare_start_date (str | Unset): Start date for comparison date range
            compare_end_date (str | Unset): End date for comparison date range
            settings (DataResponseMetaQuerySettings | Unset): Settings used in query
            cache_minutes (int | Unset): Requested maximum age of cache in minutes
     """

    start_date: str | Unset = UNSET
    end_date: str | Unset = UNSET
    ds_accounts: list[str] | Unset = UNSET
    ds_segments: list[str] | Unset = UNSET
    fields: list[DataResponseMetaQueryFieldsItem] | Unset = UNSET
    compare_type: str | Unset = UNSET
    compare_show: str | Unset = UNSET
    compare_start_date: str | Unset = UNSET
    compare_end_date: str | Unset = UNSET
    settings: DataResponseMetaQuerySettings | Unset = UNSET
    cache_minutes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.data_response_meta_query_settings import DataResponseMetaQuerySettings
        from ..models.data_response_meta_query_fields_item import DataResponseMetaQueryFieldsItem
        start_date = self.start_date

        end_date = self.end_date

        ds_accounts: list[str] | Unset = UNSET
        if not isinstance(self.ds_accounts, Unset):
            ds_accounts = self.ds_accounts



        ds_segments: list[str] | Unset = UNSET
        if not isinstance(self.ds_segments, Unset):
            ds_segments = self.ds_segments



        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)



        compare_type = self.compare_type

        compare_show = self.compare_show

        compare_start_date = self.compare_start_date

        compare_end_date = self.compare_end_date

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        cache_minutes = self.cache_minutes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if ds_accounts is not UNSET:
            field_dict["ds_accounts"] = ds_accounts
        if ds_segments is not UNSET:
            field_dict["ds_segments"] = ds_segments
        if fields is not UNSET:
            field_dict["fields"] = fields
        if compare_type is not UNSET:
            field_dict["compare_type"] = compare_type
        if compare_show is not UNSET:
            field_dict["compare_show"] = compare_show
        if compare_start_date is not UNSET:
            field_dict["compare_start_date"] = compare_start_date
        if compare_end_date is not UNSET:
            field_dict["compare_end_date"] = compare_end_date
        if settings is not UNSET:
            field_dict["settings"] = settings
        if cache_minutes is not UNSET:
            field_dict["cache_minutes"] = cache_minutes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_response_meta_query_settings import DataResponseMetaQuerySettings
        from ..models.data_response_meta_query_fields_item import DataResponseMetaQueryFieldsItem
        d = dict(src_dict)
        start_date = d.pop("start_date", UNSET)

        end_date = d.pop("end_date", UNSET)

        ds_accounts = cast(list[str], d.pop("ds_accounts", UNSET))


        ds_segments = cast(list[str], d.pop("ds_segments", UNSET))


        _fields = d.pop("fields", UNSET)
        fields: list[DataResponseMetaQueryFieldsItem] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = DataResponseMetaQueryFieldsItem.from_dict(fields_item_data)



                fields.append(fields_item)


        compare_type = d.pop("compare_type", UNSET)

        compare_show = d.pop("compare_show", UNSET)

        compare_start_date = d.pop("compare_start_date", UNSET)

        compare_end_date = d.pop("compare_end_date", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: DataResponseMetaQuerySettings | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = DataResponseMetaQuerySettings.from_dict(_settings)




        cache_minutes = d.pop("cache_minutes", UNSET)

        data_response_meta_query = cls(
            start_date=start_date,
            end_date=end_date,
            ds_accounts=ds_accounts,
            ds_segments=ds_segments,
            fields=fields,
            compare_type=compare_type,
            compare_show=compare_show,
            compare_start_date=compare_start_date,
            compare_end_date=compare_end_date,
            settings=settings,
            cache_minutes=cache_minutes,
        )


        data_response_meta_query.additional_properties = d
        return data_response_meta_query

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
