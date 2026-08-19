from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blend_list_item_output_type import BlendListItemOutputType, check_blend_list_item_output_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blend_list_item_output_blended_data_sources import BlendListItemOutputBlendedDataSources


T = TypeVar("T", bound="BlendListItemOutput")


@_attrs_define
class BlendListItemOutput:
    """A blend summary returned in list responses (without the full config).

    Attributes:
        blend_id (int | Unset): Blend ID. Example: 569.
        blend_uuid (UUID | Unset): Blend UUID. Example: 71bc0582-31b5-11f1-a55c-4201ac182030.
        type_ (BlendListItemOutputType | Unset): Blend type. Example: union.
        display_name (str | Unset): Display name of the blend. Example: My Blend.
        description (None | str | Unset): Description of the blend. Example: Description of the blend.
        modified_time_utc (datetime.datetime | Unset): Timestamp of the last modification, in UTC. Serialized with a
            numeric offset (e.g. "+0000") rather than a trailing "Z". Example: 2026-04-07T10:00:00+0000.
        last_modify_user_email (str | Unset): Email of the user who last modified the blend. Example:
            user@supermetrics.com.
        blended_data_sources (BlendListItemOutputBlendedDataSources | Unset): Simplified data source list for this
            blend.
    """

    blend_id: int | Unset = UNSET
    blend_uuid: UUID | Unset = UNSET
    type_: BlendListItemOutputType | Unset = UNSET
    display_name: str | Unset = UNSET
    description: None | str | Unset = UNSET
    modified_time_utc: datetime.datetime | Unset = UNSET
    last_modify_user_email: str | Unset = UNSET
    blended_data_sources: BlendListItemOutputBlendedDataSources | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blend_id = self.blend_id

        blend_uuid: str | Unset = UNSET
        if not isinstance(self.blend_uuid, Unset):
            blend_uuid = str(self.blend_uuid)

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        display_name = self.display_name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        modified_time_utc: str | Unset = UNSET
        if not isinstance(self.modified_time_utc, Unset):
            modified_time_utc = self.modified_time_utc.isoformat()

        last_modify_user_email = self.last_modify_user_email

        blended_data_sources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.blended_data_sources, Unset):
            blended_data_sources = self.blended_data_sources.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blend_id is not UNSET:
            field_dict["blend_id"] = blend_id
        if blend_uuid is not UNSET:
            field_dict["blend_uuid"] = blend_uuid
        if type_ is not UNSET:
            field_dict["type"] = type_
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if modified_time_utc is not UNSET:
            field_dict["modified_time_utc"] = modified_time_utc
        if last_modify_user_email is not UNSET:
            field_dict["last_modify_user_email"] = last_modify_user_email
        if blended_data_sources is not UNSET:
            field_dict["blended_data_sources"] = blended_data_sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blend_list_item_output_blended_data_sources import BlendListItemOutputBlendedDataSources

        d = dict(src_dict)
        blend_id = d.pop("blend_id", UNSET)

        _blend_uuid = d.pop("blend_uuid", UNSET)
        blend_uuid: UUID | Unset
        if isinstance(_blend_uuid, Unset):
            blend_uuid = UNSET
        else:
            blend_uuid = UUID(_blend_uuid)

        _type_ = d.pop("type", UNSET)
        type_: BlendListItemOutputType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_blend_list_item_output_type(_type_)

        display_name = d.pop("display_name", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _modified_time_utc = d.pop("modified_time_utc", UNSET)
        modified_time_utc: datetime.datetime | Unset
        if isinstance(_modified_time_utc, Unset):
            modified_time_utc = UNSET
        else:
            modified_time_utc = datetime.datetime.fromisoformat(_modified_time_utc)

        last_modify_user_email = d.pop("last_modify_user_email", UNSET)

        _blended_data_sources = d.pop("blended_data_sources", UNSET)
        blended_data_sources: BlendListItemOutputBlendedDataSources | Unset
        if isinstance(_blended_data_sources, Unset):
            blended_data_sources = UNSET
        else:
            blended_data_sources = BlendListItemOutputBlendedDataSources.from_dict(_blended_data_sources)

        blend_list_item_output = cls(
            blend_id=blend_id,
            blend_uuid=blend_uuid,
            type_=type_,
            display_name=display_name,
            description=description,
            modified_time_utc=modified_time_utc,
            last_modify_user_email=last_modify_user_email,
            blended_data_sources=blended_data_sources,
        )

        blend_list_item_output.additional_properties = d
        return blend_list_item_output

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
