from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clone_transfer_body_accounts_item import CloneTransferBodyAccountsItem
    from ..models.clone_transfer_body_data_source_settings_item import CloneTransferBodyDataSourceSettingsItem
    from ..models.clone_transfer_body_schedule_item import CloneTransferBodyScheduleItem
    from ..models.clone_transfer_body_segments_item import CloneTransferBodySegmentsItem


T = TypeVar("T", bound="CloneTransferBody")


@_attrs_define
class CloneTransferBody:
    """
    Attributes:
        display_name (str | Unset): Name for the clone. Defaults to "Copy of <source name>" Example: My Cloned Transfer.
        schema_id (int | Unset): Schema identifier Example: 2.
        destination_id (int | Unset): Destination identifier (must belong to the same team and be the same destination
            type as the source) Example: 8.
        accounts (list[CloneTransferBodyAccountsItem] | Unset): Data source accounts (replaces source accounts entirely)
        segments (list[CloneTransferBodySegmentsItem] | Unset): Data segments (replaces source segments entirely)
        schedule (list[CloneTransferBodyScheduleItem] | Unset): Transfer execution schedule (replaces source schedule
            entirely)
        data_source_settings (list[CloneTransferBodyDataSourceSettingsItem] | Unset): Source-specific configuration
            settings
        notification_recipients (list[str] | Unset): Email addresses for notifications (source recipients are not copied
            by default)
    """

    display_name: str | Unset = UNSET
    schema_id: int | Unset = UNSET
    destination_id: int | Unset = UNSET
    accounts: list[CloneTransferBodyAccountsItem] | Unset = UNSET
    segments: list[CloneTransferBodySegmentsItem] | Unset = UNSET
    schedule: list[CloneTransferBodyScheduleItem] | Unset = UNSET
    data_source_settings: list[CloneTransferBodyDataSourceSettingsItem] | Unset = UNSET
    notification_recipients: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        schema_id = self.schema_id

        destination_id = self.destination_id

        accounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)

        segments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.segments, Unset):
            segments = []
            for segments_item_data in self.segments:
                segments_item = segments_item_data.to_dict()
                segments.append(segments_item)

        schedule: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = []
            for schedule_item_data in self.schedule:
                schedule_item = schedule_item_data.to_dict()
                schedule.append(schedule_item)

        data_source_settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_source_settings, Unset):
            data_source_settings = []
            for data_source_settings_item_data in self.data_source_settings:
                data_source_settings_item = data_source_settings_item_data.to_dict()
                data_source_settings.append(data_source_settings_item)

        notification_recipients: list[str] | Unset = UNSET
        if not isinstance(self.notification_recipients, Unset):
            notification_recipients = self.notification_recipients

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if schema_id is not UNSET:
            field_dict["schema_id"] = schema_id
        if destination_id is not UNSET:
            field_dict["destination_id"] = destination_id
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if segments is not UNSET:
            field_dict["segments"] = segments
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if data_source_settings is not UNSET:
            field_dict["data_source_settings"] = data_source_settings
        if notification_recipients is not UNSET:
            field_dict["notification_recipients"] = notification_recipients

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.clone_transfer_body_accounts_item import CloneTransferBodyAccountsItem
        from ..models.clone_transfer_body_data_source_settings_item import CloneTransferBodyDataSourceSettingsItem
        from ..models.clone_transfer_body_schedule_item import CloneTransferBodyScheduleItem
        from ..models.clone_transfer_body_segments_item import CloneTransferBodySegmentsItem

        d = dict(src_dict)
        display_name = d.pop("display_name", UNSET)

        schema_id = d.pop("schema_id", UNSET)

        destination_id = d.pop("destination_id", UNSET)

        _accounts = d.pop("accounts", UNSET)
        accounts: list[CloneTransferBodyAccountsItem] | Unset = UNSET
        if _accounts is not UNSET:
            accounts = []
            for accounts_item_data in _accounts:
                accounts_item = CloneTransferBodyAccountsItem.from_dict(accounts_item_data)

                accounts.append(accounts_item)

        _segments = d.pop("segments", UNSET)
        segments: list[CloneTransferBodySegmentsItem] | Unset = UNSET
        if _segments is not UNSET:
            segments = []
            for segments_item_data in _segments:
                segments_item = CloneTransferBodySegmentsItem.from_dict(segments_item_data)

                segments.append(segments_item)

        _schedule = d.pop("schedule", UNSET)
        schedule: list[CloneTransferBodyScheduleItem] | Unset = UNSET
        if _schedule is not UNSET:
            schedule = []
            for schedule_item_data in _schedule:
                schedule_item = CloneTransferBodyScheduleItem.from_dict(schedule_item_data)

                schedule.append(schedule_item)

        _data_source_settings = d.pop("data_source_settings", UNSET)
        data_source_settings: list[CloneTransferBodyDataSourceSettingsItem] | Unset = UNSET
        if _data_source_settings is not UNSET:
            data_source_settings = []
            for data_source_settings_item_data in _data_source_settings:
                data_source_settings_item = CloneTransferBodyDataSourceSettingsItem.from_dict(
                    data_source_settings_item_data
                )

                data_source_settings.append(data_source_settings_item)

        notification_recipients = cast(list[str], d.pop("notification_recipients", UNSET))

        clone_transfer_body = cls(
            display_name=display_name,
            schema_id=schema_id,
            destination_id=destination_id,
            accounts=accounts,
            segments=segments,
            schedule=schedule,
            data_source_settings=data_source_settings,
            notification_recipients=notification_recipients,
        )

        clone_transfer_body.additional_properties = d
        return clone_transfer_body

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
