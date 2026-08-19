from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.meta_with_pagination import MetaWithPagination
    from ..models.paginated_transformations_output_data import PaginatedTransformationsOutputData


T = TypeVar("T", bound="PaginatedTransformationsOutput")


@_attrs_define
class PaginatedTransformationsOutput:
    """Paginated collection of custom field transformations. The `meta` envelope carries pagination details and
    `data.items` holds the page of transformations.

        Example:
            {'data': {'items': [{'id': 42, 'name': 'spec_example_field', 'data_source_id': 'GAWA', 'display_name': 'Spec
                Example Field', 'description': 'Temporary transformation for spec examples', 'field_type': 'dim', 'data_type':
                'string.text.value', 'modified_time_utc': '2026-04-06T10:59:04+0000', 'modified_user': {'email':
                'user@supermetrics.com', 'first_name': 'John', 'last_name': 'Doe'}, 'definition': {'items': [{'type':
                'function', 'name': 'upper_case', 'arguments': [{'name': 'value', 'value': {'type': 'data_source_field',
                'value': 'platform'}}], 'description': None}]}, 'report_types': ['Default']}]}}

        Attributes:
            meta (MetaWithPagination | Unset): Response metadata including pagination details.
            data (PaginatedTransformationsOutputData | Unset): Wrapper holding the page of transformation objects.
    """

    meta: MetaWithPagination | Unset = UNSET
    data: PaginatedTransformationsOutputData | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if meta is not UNSET:
            field_dict["meta"] = meta
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.meta_with_pagination import MetaWithPagination
        from ..models.paginated_transformations_output_data import PaginatedTransformationsOutputData

        d = dict(src_dict)
        _meta = d.pop("meta", UNSET)
        meta: MetaWithPagination | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = MetaWithPagination.from_dict(_meta)

        _data = d.pop("data", UNSET)
        data: PaginatedTransformationsOutputData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = PaginatedTransformationsOutputData.from_dict(_data)

        paginated_transformations_output = cls(
            meta=meta,
            data=data,
        )

        paginated_transformations_output.additional_properties = d
        return paginated_transformations_output

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
