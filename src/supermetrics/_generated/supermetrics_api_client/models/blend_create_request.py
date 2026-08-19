from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_create_request_type import BlendCreateRequestType, check_blend_create_request_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_config import BlendConfig
    from ..models.blended_data_source_input import BlendedDataSourceInput


T = TypeVar("T", bound="BlendCreateRequest")


@_attrs_define
class BlendCreateRequest:
    """Payload for creating a new blend. Extends BlendBaseRequest and additionally requires the blend `type`. When
    creating, new data sources are referenced by `blend_data_source_key` rather than `blend_data_source_id`.

        Attributes:
            display_name (str): Display name of the blend. Example: My Blend.
            blended_data_sources (list[BlendedDataSourceInput]): Data sources to include in the blend.
            config (BlendConfig): Field mappings and join configuration for the blend (request). Union blends contain only
                `fields`; join blends also include `query_table` and `joins`.
            type_ (BlendCreateRequestType): Blend type: `union` stacks rows, `join` joins data sources on shared fields.
                Example: union.
            description (None | str | Unset): Optional free-text description of the blend. Example: Description of the
                blend.
    """

    display_name: str
    blended_data_sources: list[BlendedDataSourceInput]
    config: BlendConfig
    type_: BlendCreateRequestType
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        blended_data_sources = []
        for blended_data_sources_item_data in self.blended_data_sources:
            blended_data_sources_item = blended_data_sources_item_data.to_dict()
            blended_data_sources.append(blended_data_sources_item)

        config = self.config.to_dict()

        type_: str = self.type_

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "blended_data_sources": blended_data_sources,
                "config": config,
                "type": type_,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_config import BlendConfig
        from ..models.blended_data_source_input import BlendedDataSourceInput

        d = dict(src_dict)
        display_name = d.pop("display_name")

        blended_data_sources = []
        _blended_data_sources = d.pop("blended_data_sources")
        for blended_data_sources_item_data in _blended_data_sources:
            blended_data_sources_item = BlendedDataSourceInput.from_dict(blended_data_sources_item_data)

            blended_data_sources.append(blended_data_sources_item)

        config = BlendConfig.from_dict(d.pop("config"))

        type_ = check_blend_create_request_type(d.pop("type"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        blend_create_request = cls(
            display_name=display_name,
            blended_data_sources=blended_data_sources,
            config=config,
            type_=type_,
            description=description,
        )

        blend_create_request.additional_properties = d
        return blend_create_request

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
