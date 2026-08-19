from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_config import BlendConfig
    from ..models.blended_data_source_input import BlendedDataSourceInput


T = TypeVar("T", bound="BlendBaseRequest")


@_attrs_define
class BlendBaseRequest:
    """Fields shared by the blend create and update requests. Concrete request schemas compose this via `allOf` and add
    their own required-field constraints (and, for create, the `type` discriminator).

        Attributes:
            display_name (str | Unset): Display name of the blend. Example: My Blend.
            description (None | str | Unset): Optional free-text description of the blend. Example: Description of the
                blend.
            blended_data_sources (list[BlendedDataSourceInput] | Unset): Data sources to include in the blend.
            config (BlendConfig | Unset): Field mappings and join configuration for the blend (request). Union blends
                contain only `fields`; join blends also include `query_table` and `joins`.
    """

    display_name: str | Unset = UNSET
    description: None | str | Unset = UNSET
    blended_data_sources: list[BlendedDataSourceInput] | Unset = UNSET
    config: BlendConfig | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        blended_data_sources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.blended_data_sources, Unset):
            blended_data_sources = []
            for blended_data_sources_item_data in self.blended_data_sources:
                blended_data_sources_item = blended_data_sources_item_data.to_dict()
                blended_data_sources.append(blended_data_sources_item)

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if blended_data_sources is not UNSET:
            field_dict["blended_data_sources"] = blended_data_sources
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_config import BlendConfig
        from ..models.blended_data_source_input import BlendedDataSourceInput

        d = dict(src_dict)
        display_name = d.pop("display_name", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _blended_data_sources = d.pop("blended_data_sources", UNSET)
        blended_data_sources: list[BlendedDataSourceInput] | Unset = UNSET
        if _blended_data_sources is not UNSET:
            blended_data_sources = []
            for blended_data_sources_item_data in _blended_data_sources:
                blended_data_sources_item = BlendedDataSourceInput.from_dict(blended_data_sources_item_data)

                blended_data_sources.append(blended_data_sources_item)

        _config = d.pop("config", UNSET)
        config: BlendConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = BlendConfig.from_dict(_config)

        blend_base_request = cls(
            display_name=display_name,
            description=description,
            blended_data_sources=blended_data_sources,
            config=config,
        )

        blend_base_request.additional_properties = d
        return blend_base_request

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
