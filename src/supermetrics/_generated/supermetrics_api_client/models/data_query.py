from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.data_query_ds_accounts_type_2 import DataQueryDsAccountsType2
  from ..models.data_query_fields_type_2_item import DataQueryFieldsType2Item
  from ..models.data_query_settings import DataQuerySettings





T = TypeVar("T", bound="DataQuery")



@_attrs_define
class DataQuery:
    """ 
        Attributes:
            ds_id (str): Target data source ID Example: GA.
            api_key (str | Unset): API key when not using an authorization header Example: abc123def456.
            schedule_id (str | Unset): Schedule ID for this query request. If not provided, one will be generated from other
                query parameters Example: my_query_123.
            ds_accounts (DataQueryDsAccountsType2 | list[str] | str | Unset): List of data source accounts the query should
                target, or a filter for them Example: ['account123', 'account456'].
            ds_segments (list[str] | str | Unset): List of data source segment IDs the query should target Example:
                ['segment1', 'segment2'].
            ds_user (str | Unset): Shorthand parameter to provide one value for ds_users Example: user@example.com.
            ds_users (list[str] | str | Unset): List of data source login usernames to limit when searching for suitable
                authentication
            date_range_type (str | Unset): Type of date range the query should use
            start_date (str | Unset): Fixed or relative start date for your query Example: yesterday.
            end_date (str | Unset): Fixed or relative end date for your query Example: yesterday.
            compare_type (str | Unset): Date range comparison type. Defaults to none
            compare_show (str | Unset): When compare_type is custom, display type for comparison values
            compare_start_date (str | Unset): When compare_type is custom, fixed or relative start date for comparison
            compare_end_date (str | Unset): When compare_type is custom, fixed or relative end date for comparison
            fields (list[DataQueryFieldsType2Item] | list[str] | str | Unset): Target data source fields the query should
                return
            settings (DataQuerySettings | Unset): Settings that should be applied when performing the query
            filter_ (str | Unset): Filter string that should be applied to the results
            order_columns (str | Unset): Order instruction for fields that are split by column
            order_rows (list[str] | str | Unset): List of order fields and sort directions for result rows
            max_columns (int | Unset): Maximum number of columns the query results should contain
            max_rows (int | Unset): Maximum number of rows the query results should contain
            offset_start (int | Unset): Starting row index for paginated response
            offset_end (int | Unset): Ending row index for paginated response
            cache_minutes (int | Unset): Maximum allowed age of query results cache in minutes
            sync_timeout (int | Unset): Number of seconds the API should wait for query to finish
     """

    ds_id: str
    api_key: str | Unset = UNSET
    schedule_id: str | Unset = UNSET
    ds_accounts: DataQueryDsAccountsType2 | list[str] | str | Unset = UNSET
    ds_segments: list[str] | str | Unset = UNSET
    ds_user: str | Unset = UNSET
    ds_users: list[str] | str | Unset = UNSET
    date_range_type: str | Unset = UNSET
    start_date: str | Unset = UNSET
    end_date: str | Unset = UNSET
    compare_type: str | Unset = UNSET
    compare_show: str | Unset = UNSET
    compare_start_date: str | Unset = UNSET
    compare_end_date: str | Unset = UNSET
    fields: list[DataQueryFieldsType2Item] | list[str] | str | Unset = UNSET
    settings: DataQuerySettings | Unset = UNSET
    filter_: str | Unset = UNSET
    order_columns: str | Unset = UNSET
    order_rows: list[str] | str | Unset = UNSET
    max_columns: int | Unset = UNSET
    max_rows: int | Unset = UNSET
    offset_start: int | Unset = UNSET
    offset_end: int | Unset = UNSET
    cache_minutes: int | Unset = UNSET
    sync_timeout: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.data_query_ds_accounts_type_2 import DataQueryDsAccountsType2
        from ..models.data_query_fields_type_2_item import DataQueryFieldsType2Item
        from ..models.data_query_settings import DataQuerySettings
        ds_id = self.ds_id

        api_key = self.api_key

        schedule_id = self.schedule_id

        ds_accounts: dict[str, Any] | list[str] | str | Unset
        if isinstance(self.ds_accounts, Unset):
            ds_accounts = UNSET
        elif isinstance(self.ds_accounts, list):
            ds_accounts = self.ds_accounts


        elif isinstance(self.ds_accounts, DataQueryDsAccountsType2):
            ds_accounts = self.ds_accounts.to_dict()
        else:
            ds_accounts = self.ds_accounts

        ds_segments: list[str] | str | Unset
        if isinstance(self.ds_segments, Unset):
            ds_segments = UNSET
        elif isinstance(self.ds_segments, list):
            ds_segments = self.ds_segments


        else:
            ds_segments = self.ds_segments

        ds_user = self.ds_user

        ds_users: list[str] | str | Unset
        if isinstance(self.ds_users, Unset):
            ds_users = UNSET
        elif isinstance(self.ds_users, list):
            ds_users = self.ds_users


        else:
            ds_users = self.ds_users

        date_range_type = self.date_range_type

        start_date = self.start_date

        end_date = self.end_date

        compare_type = self.compare_type

        compare_show = self.compare_show

        compare_start_date = self.compare_start_date

        compare_end_date = self.compare_end_date

        fields: list[dict[str, Any]] | list[str] | str | Unset
        if isinstance(self.fields, Unset):
            fields = UNSET
        elif isinstance(self.fields, list):
            fields = self.fields


        elif isinstance(self.fields, list):
            fields = []
            for fields_type_2_item_data in self.fields:
                fields_type_2_item = fields_type_2_item_data.to_dict()
                fields.append(fields_type_2_item)


        else:
            fields = self.fields

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        filter_ = self.filter_

        order_columns = self.order_columns

        order_rows: list[str] | str | Unset
        if isinstance(self.order_rows, Unset):
            order_rows = UNSET
        elif isinstance(self.order_rows, list):
            order_rows = self.order_rows


        else:
            order_rows = self.order_rows

        max_columns = self.max_columns

        max_rows = self.max_rows

        offset_start = self.offset_start

        offset_end = self.offset_end

        cache_minutes = self.cache_minutes

        sync_timeout = self.sync_timeout


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ds_id": ds_id,
        })
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if schedule_id is not UNSET:
            field_dict["schedule_id"] = schedule_id
        if ds_accounts is not UNSET:
            field_dict["ds_accounts"] = ds_accounts
        if ds_segments is not UNSET:
            field_dict["ds_segments"] = ds_segments
        if ds_user is not UNSET:
            field_dict["ds_user"] = ds_user
        if ds_users is not UNSET:
            field_dict["ds_users"] = ds_users
        if date_range_type is not UNSET:
            field_dict["date_range_type"] = date_range_type
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if compare_type is not UNSET:
            field_dict["compare_type"] = compare_type
        if compare_show is not UNSET:
            field_dict["compare_show"] = compare_show
        if compare_start_date is not UNSET:
            field_dict["compare_start_date"] = compare_start_date
        if compare_end_date is not UNSET:
            field_dict["compare_end_date"] = compare_end_date
        if fields is not UNSET:
            field_dict["fields"] = fields
        if settings is not UNSET:
            field_dict["settings"] = settings
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if order_columns is not UNSET:
            field_dict["order_columns"] = order_columns
        if order_rows is not UNSET:
            field_dict["order_rows"] = order_rows
        if max_columns is not UNSET:
            field_dict["max_columns"] = max_columns
        if max_rows is not UNSET:
            field_dict["max_rows"] = max_rows
        if offset_start is not UNSET:
            field_dict["offset_start"] = offset_start
        if offset_end is not UNSET:
            field_dict["offset_end"] = offset_end
        if cache_minutes is not UNSET:
            field_dict["cache_minutes"] = cache_minutes
        if sync_timeout is not UNSET:
            field_dict["sync_timeout"] = sync_timeout

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_query_ds_accounts_type_2 import DataQueryDsAccountsType2
        from ..models.data_query_fields_type_2_item import DataQueryFieldsType2Item
        from ..models.data_query_settings import DataQuerySettings
        d = dict(src_dict)
        ds_id = d.pop("ds_id")

        api_key = d.pop("api_key", UNSET)

        schedule_id = d.pop("schedule_id", UNSET)

        def _parse_ds_accounts(data: object) -> DataQueryDsAccountsType2 | list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ds_accounts_type_1 = cast(list[str], data)

                return ds_accounts_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ds_accounts_type_2 = DataQueryDsAccountsType2.from_dict(data)



                return ds_accounts_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DataQueryDsAccountsType2 | list[str] | str | Unset, data)

        ds_accounts = _parse_ds_accounts(d.pop("ds_accounts", UNSET))


        def _parse_ds_segments(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ds_segments_type_1 = cast(list[str], data)

                return ds_segments_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        ds_segments = _parse_ds_segments(d.pop("ds_segments", UNSET))


        ds_user = d.pop("ds_user", UNSET)

        def _parse_ds_users(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ds_users_type_1 = cast(list[str], data)

                return ds_users_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        ds_users = _parse_ds_users(d.pop("ds_users", UNSET))


        date_range_type = d.pop("date_range_type", UNSET)

        start_date = d.pop("start_date", UNSET)

        end_date = d.pop("end_date", UNSET)

        compare_type = d.pop("compare_type", UNSET)

        compare_show = d.pop("compare_show", UNSET)

        compare_start_date = d.pop("compare_start_date", UNSET)

        compare_end_date = d.pop("compare_end_date", UNSET)

        def _parse_fields(data: object) -> list[DataQueryFieldsType2Item] | list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                fields_type_1 = cast(list[str], data)

                return fields_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                fields_type_2 = []
                _fields_type_2 = data
                for fields_type_2_item_data in (_fields_type_2):
                    fields_type_2_item = DataQueryFieldsType2Item.from_dict(fields_type_2_item_data)



                    fields_type_2.append(fields_type_2_item)

                return fields_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DataQueryFieldsType2Item] | list[str] | str | Unset, data)

        fields = _parse_fields(d.pop("fields", UNSET))


        _settings = d.pop("settings", UNSET)
        settings: DataQuerySettings | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = DataQuerySettings.from_dict(_settings)




        filter_ = d.pop("filter", UNSET)

        order_columns = d.pop("order_columns", UNSET)

        def _parse_order_rows(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                order_rows_type_1 = cast(list[str], data)

                return order_rows_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        order_rows = _parse_order_rows(d.pop("order_rows", UNSET))


        max_columns = d.pop("max_columns", UNSET)

        max_rows = d.pop("max_rows", UNSET)

        offset_start = d.pop("offset_start", UNSET)

        offset_end = d.pop("offset_end", UNSET)

        cache_minutes = d.pop("cache_minutes", UNSET)

        sync_timeout = d.pop("sync_timeout", UNSET)

        data_query = cls(
            ds_id=ds_id,
            api_key=api_key,
            schedule_id=schedule_id,
            ds_accounts=ds_accounts,
            ds_segments=ds_segments,
            ds_user=ds_user,
            ds_users=ds_users,
            date_range_type=date_range_type,
            start_date=start_date,
            end_date=end_date,
            compare_type=compare_type,
            compare_show=compare_show,
            compare_start_date=compare_start_date,
            compare_end_date=compare_end_date,
            fields=fields,
            settings=settings,
            filter_=filter_,
            order_columns=order_columns,
            order_rows=order_rows,
            max_columns=max_columns,
            max_rows=max_rows,
            offset_start=offset_start,
            offset_end=offset_end,
            cache_minutes=cache_minutes,
            sync_timeout=sync_timeout,
        )


        data_query.additional_properties = d
        return data_query

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
