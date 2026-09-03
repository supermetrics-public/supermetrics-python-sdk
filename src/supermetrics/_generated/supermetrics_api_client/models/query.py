from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.query_type import QueryType, check_query_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_source import DataSource
    from ..models.query_group import QueryGroup
    from ..models.query_query_params import QueryQueryParams


T = TypeVar("T", bound="Query")


@_attrs_define
class Query:
    """
    Attributes:
        type_ (QueryType | Unset):
        query_id (str | Unset): Supermetrics query ID
        slug (str | Unset): Unique query slug string, used in query's short URL
        name (str | Unset): Custom query name
        modified_time (datetime.datetime | None | Unset): ISO 8601 datetime for when the saved query was last modified
        ds_info (DataSource | Unset):
        group_info (QueryGroup | Unset):
        query_params (QueryQueryParams | Unset): Query parameters in key-value pairs, as expected by the get data
            endpoint
    """

    type_: QueryType | Unset = UNSET
    query_id: str | Unset = UNSET
    slug: str | Unset = UNSET
    name: str | Unset = UNSET
    modified_time: datetime.datetime | None | Unset = UNSET
    ds_info: DataSource | Unset = UNSET
    group_info: QueryGroup | Unset = UNSET
    query_params: QueryQueryParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        query_id = self.query_id

        slug = self.slug

        name = self.name

        modified_time: None | str | Unset
        if isinstance(self.modified_time, Unset):
            modified_time = UNSET
        elif isinstance(self.modified_time, datetime.datetime):
            modified_time = self.modified_time.isoformat()
        else:
            modified_time = self.modified_time

        ds_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ds_info, Unset):
            ds_info = self.ds_info.to_dict()

        group_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.group_info, Unset):
            group_info = self.group_info.to_dict()

        query_params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query_params, Unset):
            query_params = self.query_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if query_id is not UNSET:
            field_dict["query_id"] = query_id
        if slug is not UNSET:
            field_dict["slug"] = slug
        if name is not UNSET:
            field_dict["name"] = name
        if modified_time is not UNSET:
            field_dict["modified_time"] = modified_time
        if ds_info is not UNSET:
            field_dict["ds_info"] = ds_info
        if group_info is not UNSET:
            field_dict["group_info"] = group_info
        if query_params is not UNSET:
            field_dict["query_params"] = query_params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_source import DataSource
        from ..models.query_group import QueryGroup
        from ..models.query_query_params import QueryQueryParams

        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: QueryType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_query_type(_type_)

        query_id = d.pop("query_id", UNSET)

        slug = d.pop("slug", UNSET)

        name = d.pop("name", UNSET)

        def _parse_modified_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                modified_time_type_0 = datetime.datetime.fromisoformat(data)

                return modified_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        modified_time = _parse_modified_time(d.pop("modified_time", UNSET))

        _ds_info = d.pop("ds_info", UNSET)
        ds_info: DataSource | Unset
        if isinstance(_ds_info, Unset):
            ds_info = UNSET
        else:
            ds_info = DataSource.from_dict(_ds_info)

        _group_info = d.pop("group_info", UNSET)
        group_info: QueryGroup | Unset
        if isinstance(_group_info, Unset):
            group_info = UNSET
        else:
            group_info = QueryGroup.from_dict(_group_info)

        _query_params = d.pop("query_params", UNSET)
        query_params: QueryQueryParams | Unset
        if isinstance(_query_params, Unset):
            query_params = UNSET
        else:
            query_params = QueryQueryParams.from_dict(_query_params)

        query = cls(
            type_=type_,
            query_id=query_id,
            slug=slug,
            name=name,
            modified_time=modified_time,
            ds_info=ds_info,
            group_info=group_info,
            query_params=query_params,
        )

        query.additional_properties = d
        return query

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
