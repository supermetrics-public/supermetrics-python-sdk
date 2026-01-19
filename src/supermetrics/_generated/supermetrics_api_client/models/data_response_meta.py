from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.data_response_meta_query import DataResponseMetaQuery
  from ..models.data_response_meta_result import DataResponseMetaResult
  from ..models.data_response_meta_paginate import DataResponseMetaPaginate





T = TypeVar("T", bound="DataResponseMeta")



@_attrs_define
class DataResponseMeta:
    """ 
        Attributes:
            request_id (str | Unset): API request ID
            schedule_id (str | Unset): Custom or generated schedule ID for the query
            status_code (str | Unset): Status code for the query
            query (DataResponseMetaQuery | Unset):
            result (DataResponseMetaResult | Unset):
            paginate (DataResponseMetaPaginate | Unset):
     """

    request_id: str | Unset = UNSET
    schedule_id: str | Unset = UNSET
    status_code: str | Unset = UNSET
    query: DataResponseMetaQuery | Unset = UNSET
    result: DataResponseMetaResult | Unset = UNSET
    paginate: DataResponseMetaPaginate | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.data_response_meta_query import DataResponseMetaQuery
        from ..models.data_response_meta_result import DataResponseMetaResult
        from ..models.data_response_meta_paginate import DataResponseMetaPaginate
        request_id = self.request_id

        schedule_id = self.schedule_id

        status_code = self.status_code

        query: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()

        result: dict[str, Any] | Unset = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        paginate: dict[str, Any] | Unset = UNSET
        if not isinstance(self.paginate, Unset):
            paginate = self.paginate.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if schedule_id is not UNSET:
            field_dict["schedule_id"] = schedule_id
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if query is not UNSET:
            field_dict["query"] = query
        if result is not UNSET:
            field_dict["result"] = result
        if paginate is not UNSET:
            field_dict["paginate"] = paginate

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_response_meta_query import DataResponseMetaQuery
        from ..models.data_response_meta_result import DataResponseMetaResult
        from ..models.data_response_meta_paginate import DataResponseMetaPaginate
        d = dict(src_dict)
        request_id = d.pop("request_id", UNSET)

        schedule_id = d.pop("schedule_id", UNSET)

        status_code = d.pop("status_code", UNSET)

        _query = d.pop("query", UNSET)
        query: DataResponseMetaQuery | Unset
        if isinstance(_query,  Unset):
            query = UNSET
        else:
            query = DataResponseMetaQuery.from_dict(_query)




        _result = d.pop("result", UNSET)
        result: DataResponseMetaResult | Unset
        if isinstance(_result,  Unset):
            result = UNSET
        else:
            result = DataResponseMetaResult.from_dict(_result)




        _paginate = d.pop("paginate", UNSET)
        paginate: DataResponseMetaPaginate | Unset
        if isinstance(_paginate,  Unset):
            paginate = UNSET
        else:
            paginate = DataResponseMetaPaginate.from_dict(_paginate)




        data_response_meta = cls(
            request_id=request_id,
            schedule_id=schedule_id,
            status_code=status_code,
            query=query,
            result=result,
            paginate=paginate,
        )


        data_response_meta.additional_properties = d
        return data_response_meta

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
