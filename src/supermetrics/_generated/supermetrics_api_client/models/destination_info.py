from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.destination_type import DestinationType
    from ..models.setup_setting import SetupSetting


T = TypeVar("T", bound="DestinationInfo")


@_attrs_define
class DestinationInfo:
    """
    Attributes:
        display_name (str): Human-readable name for the destination Example: My Snowflake Destination.
        destination_type (DestinationType):
        edit_settings (list[SetupSetting]): Configuration settings for the destination
        id (int | None | Unset): Unique identifier for the destination Example: 123.
    """

    display_name: str
    destination_type: DestinationType
    edit_settings: list[SetupSetting]
    id: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        destination_type = self.destination_type.to_dict()

        edit_settings = []
        for edit_settings_item_data in self.edit_settings:
            edit_settings_item = edit_settings_item_data.to_dict()
            edit_settings.append(edit_settings_item)

        id: int | None | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "display_name": display_name,
                "destination_type": destination_type,
                "edit_settings": edit_settings,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_type import DestinationType
        from ..models.setup_setting import SetupSetting

        d = dict(src_dict)
        display_name = d.pop("display_name")

        destination_type = DestinationType.from_dict(d.pop("destination_type"))

        edit_settings = []
        _edit_settings = d.pop("edit_settings")
        for edit_settings_item_data in _edit_settings:
            edit_settings_item = SetupSetting.from_dict(edit_settings_item_data)

            edit_settings.append(edit_settings_item)

        def _parse_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        destination_info = cls(
            display_name=display_name,
            destination_type=destination_type,
            edit_settings=edit_settings,
            id=id,
        )

        return destination_info
