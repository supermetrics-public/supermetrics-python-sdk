from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_datasource_field_ref_datasource_field_type import (
    BlendDatasourceFieldRefDatasourceFieldType,
    check_blend_datasource_field_ref_datasource_field_type,
)
from ..models.blend_datasource_field_ref_field_source import (
    BlendDatasourceFieldRefFieldSource,
    check_blend_datasource_field_ref_field_source,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_datasource_field_ref_meta_type_0 import BlendDatasourceFieldRefMetaType0


T = TypeVar("T", bound="BlendDatasourceFieldRef")


@_attrs_define
class BlendDatasourceFieldRef:
    """A field reference within a data source (request). At least one of `blend_data_source_id` or `blend_data_source_key`
    must be non-null. When creating a blend (POST), use `blend_data_source_key`. When updating (PUT), use
    `blend_data_source_id` for existing data sources or `blend_data_source_key` for newly added ones.

        Attributes:
            datasource_field_name (str): Field name as defined by the data source. Example: Date.
            field_source (BlendDatasourceFieldRefFieldSource): Origin of the field: `standard` = from the data source,
                `transformation` = computed field, `data_source_account_custom` = account-level custom field. Example: standard.
            blend_data_source_id (int | None | Unset): Internal ID of the blended data source. Use for existing data sources
                when updating a blend; null when referencing a new data source by key. Example: 146715.
            blend_data_source_key (None | str | Unset): Temporary key linking a new data source to field/join references
                within the same request. Required when creating a blend; used for new data sources when updating. Must be
                exactly 8 lowercase alphanumeric characters. Example: abcd1234.
            datasource_field_display_name (str | Unset): Display name of the field. Example: Date.
            datasource_field_type (BlendDatasourceFieldRefDatasourceFieldType | Unset): Field type: `dim` (dimension) or
                `met` (metric). Example: dim.
            datasource_field_data_type (str | Unset): Data type of the field (e.g. string.time.date, int.number.value).
                Example: string.text.value.
            meta (BlendDatasourceFieldRefMetaType0 | None | Unset): Optional metadata, e.g. account-level overrides.
    """

    datasource_field_name: str
    field_source: BlendDatasourceFieldRefFieldSource
    blend_data_source_id: int | None | Unset = UNSET
    blend_data_source_key: None | str | Unset = UNSET
    datasource_field_display_name: str | Unset = UNSET
    datasource_field_type: BlendDatasourceFieldRefDatasourceFieldType | Unset = UNSET
    datasource_field_data_type: str | Unset = UNSET
    meta: BlendDatasourceFieldRefMetaType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.blend_datasource_field_ref_meta_type_0 import BlendDatasourceFieldRefMetaType0

        datasource_field_name = self.datasource_field_name

        field_source: str = self.field_source

        blend_data_source_id: int | None | Unset
        if isinstance(self.blend_data_source_id, Unset):
            blend_data_source_id = UNSET
        else:
            blend_data_source_id = self.blend_data_source_id

        blend_data_source_key: None | str | Unset
        if isinstance(self.blend_data_source_key, Unset):
            blend_data_source_key = UNSET
        else:
            blend_data_source_key = self.blend_data_source_key

        datasource_field_display_name = self.datasource_field_display_name

        datasource_field_type: str | Unset = UNSET
        if not isinstance(self.datasource_field_type, Unset):
            datasource_field_type = self.datasource_field_type

        datasource_field_data_type = self.datasource_field_data_type

        meta: dict[str, Any] | None | Unset
        if isinstance(self.meta, Unset):
            meta = UNSET
        elif isinstance(self.meta, BlendDatasourceFieldRefMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datasource_field_name": datasource_field_name,
                "field_source": field_source,
            }
        )
        if blend_data_source_id is not UNSET:
            field_dict["blend_data_source_id"] = blend_data_source_id
        if blend_data_source_key is not UNSET:
            field_dict["blend_data_source_key"] = blend_data_source_key
        if datasource_field_display_name is not UNSET:
            field_dict["datasource_field_display_name"] = datasource_field_display_name
        if datasource_field_type is not UNSET:
            field_dict["datasource_field_type"] = datasource_field_type
        if datasource_field_data_type is not UNSET:
            field_dict["datasource_field_data_type"] = datasource_field_data_type
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_datasource_field_ref_meta_type_0 import BlendDatasourceFieldRefMetaType0

        d = dict(src_dict)
        datasource_field_name = d.pop("datasource_field_name")

        field_source = check_blend_datasource_field_ref_field_source(d.pop("field_source"))

        def _parse_blend_data_source_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        blend_data_source_id = _parse_blend_data_source_id(d.pop("blend_data_source_id", UNSET))

        def _parse_blend_data_source_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        blend_data_source_key = _parse_blend_data_source_key(d.pop("blend_data_source_key", UNSET))

        datasource_field_display_name = d.pop("datasource_field_display_name", UNSET)

        _datasource_field_type = d.pop("datasource_field_type", UNSET)
        datasource_field_type: BlendDatasourceFieldRefDatasourceFieldType | Unset
        if isinstance(_datasource_field_type, Unset):
            datasource_field_type = UNSET
        else:
            datasource_field_type = check_blend_datasource_field_ref_datasource_field_type(_datasource_field_type)

        datasource_field_data_type = d.pop("datasource_field_data_type", UNSET)

        def _parse_meta(data: object) -> BlendDatasourceFieldRefMetaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = BlendDatasourceFieldRefMetaType0.from_dict(data)

                return meta_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BlendDatasourceFieldRefMetaType0 | None | Unset, data)

        meta = _parse_meta(d.pop("meta", UNSET))

        blend_datasource_field_ref = cls(
            datasource_field_name=datasource_field_name,
            field_source=field_source,
            blend_data_source_id=blend_data_source_id,
            blend_data_source_key=blend_data_source_key,
            datasource_field_display_name=datasource_field_display_name,
            datasource_field_type=datasource_field_type,
            datasource_field_data_type=datasource_field_data_type,
            meta=meta,
        )

        blend_datasource_field_ref.additional_properties = d
        return blend_datasource_field_ref

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
