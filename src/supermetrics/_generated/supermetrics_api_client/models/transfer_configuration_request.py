from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_account import TransferAccount
    from ..models.transfer_data_source_setting import TransferDataSourceSetting
    from ..models.transfer_schedule import TransferSchedule
    from ..models.transfer_segment import TransferSegment


T = TypeVar("T", bound="TransferConfigurationRequest")


@_attrs_define
class TransferConfigurationRequest:
    """
    Attributes:
        data_source_id (str): Data source identifier Example: AW.
        schema_id (int): Numeric schema identifier (the data warehouse `dwh_schema_id`) of the table group this transfer
            writes into. Obtain it from the `schema_id` field of the List table groups endpoint (`GET /table/groups`). The
            table group's prefixed `group_id` (for example `tg_99999`) is NOT accepted here. Example: 2.
        destination_id (int): Destination identifier Example: 8.
        display_name (str): Human-readable name for the transfer Example: AW enhanced 2022-11-17.
        schedule (list[TransferSchedule]): Transfer execution schedule configuration
        accounts (list[TransferAccount]): Data source accounts to include in transfer
        segments (list[TransferSegment] | Unset): Data segments to include in transfer
        data_source_settings (list[TransferDataSourceSetting] | Unset): Source-specific configuration settings
        notification_recipients (list[str] | Unset): Email addresses to notify on transfer events Example:
            ['user1@supermetrics.com', 'user2@supermetrics.com'].
        transfer_type (int | Unset): Transfer type identifier Example: 1.
    """

    data_source_id: str
    schema_id: int
    destination_id: int
    display_name: str
    schedule: list[TransferSchedule]
    accounts: list[TransferAccount]
    segments: list[TransferSegment] | Unset = UNSET
    data_source_settings: list[TransferDataSourceSetting] | Unset = UNSET
    notification_recipients: list[str] | Unset = UNSET
    transfer_type: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data_source_id = self.data_source_id

        schema_id = self.schema_id

        destination_id = self.destination_id

        display_name = self.display_name

        schedule = []
        for schedule_item_data in self.schedule:
            schedule_item = schedule_item_data.to_dict()
            schedule.append(schedule_item)

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

        data_source_settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_source_settings, Unset):
            data_source_settings = []
            for data_source_settings_item_data in self.data_source_settings:
                data_source_settings_item = data_source_settings_item_data.to_dict()
                data_source_settings.append(data_source_settings_item)

        notification_recipients: list[str] | Unset = UNSET
        if not isinstance(self.notification_recipients, Unset):
            notification_recipients = self.notification_recipients

        transfer_type = self.transfer_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data_source_id": data_source_id,
                "schema_id": schema_id,
                "destination_id": destination_id,
                "display_name": display_name,
                "schedule": schedule,
                "accounts": accounts,
            }
        )
        if segments is not UNSET:
            field_dict["segments"] = segments
        if data_source_settings is not UNSET:
            field_dict["data_source_settings"] = data_source_settings
        if notification_recipients is not UNSET:
            field_dict["notification_recipients"] = notification_recipients
        if transfer_type is not UNSET:
            field_dict["transfer_type"] = transfer_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_account import TransferAccount
        from ..models.transfer_data_source_setting import TransferDataSourceSetting
        from ..models.transfer_schedule import TransferSchedule
        from ..models.transfer_segment import TransferSegment

        d = dict(src_dict)
        data_source_id = d.pop("data_source_id")

        schema_id = d.pop("schema_id")

        destination_id = d.pop("destination_id")

        display_name = d.pop("display_name")

        schedule = []
        _schedule = d.pop("schedule")
        for schedule_item_data in _schedule:
            schedule_item = TransferSchedule.from_dict(schedule_item_data)

            schedule.append(schedule_item)

        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = TransferAccount.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        _segments = d.pop("segments", UNSET)
        segments: list[TransferSegment] | Unset = UNSET
        if _segments is not UNSET:
            segments = []
            for segments_item_data in _segments:
                segments_item = TransferSegment.from_dict(segments_item_data)

                segments.append(segments_item)

        _data_source_settings = d.pop("data_source_settings", UNSET)
        data_source_settings: list[TransferDataSourceSetting] | Unset = UNSET
        if _data_source_settings is not UNSET:
            data_source_settings = []
            for data_source_settings_item_data in _data_source_settings:
                data_source_settings_item = TransferDataSourceSetting.from_dict(data_source_settings_item_data)

                data_source_settings.append(data_source_settings_item)

        notification_recipients = cast(list[str], d.pop("notification_recipients", UNSET))

        transfer_type = d.pop("transfer_type", UNSET)

        transfer_configuration_request = cls(
            data_source_id=data_source_id,
            schema_id=schema_id,
            destination_id=destination_id,
            display_name=display_name,
            schedule=schedule,
            accounts=accounts,
            segments=segments,
            data_source_settings=data_source_settings,
            notification_recipients=notification_recipients,
            transfer_type=transfer_type,
        )

        return transfer_configuration_request
