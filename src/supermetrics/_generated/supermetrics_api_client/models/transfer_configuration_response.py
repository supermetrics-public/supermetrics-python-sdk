from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_account import TransferAccount
    from ..models.transfer_configuration_response_data_source import TransferConfigurationResponseDataSource
    from ..models.transfer_configuration_response_license import TransferConfigurationResponseLicense
    from ..models.transfer_configuration_response_notification_recipients_type_0_item import (
        TransferConfigurationResponseNotificationRecipientsType0Item,
    )
    from ..models.transfer_schedule import TransferSchedule
    from ..models.transfer_segment import TransferSegment


T = TypeVar("T", bound="TransferConfigurationResponse")


@_attrs_define
class TransferConfigurationResponse:
    """Full transfer configuration

    Attributes:
        transfer_id (int | Unset): The transfer ID Example: 36091.
        display_name (str | Unset): Display name of the transfer Example: AW enhanced 2022-11-17.
        schema_id (int | Unset): Numeric schema identifier (the data warehouse `dwh_schema_id`) of the table group this
            transfer writes into. Matches the `schema_id` field returned by the List table groups endpoint (`GET
            /table/groups`). Example: 2.
        destination_id (int | None | Unset): Destination identifier Example: 8.
        accounts (list[TransferAccount] | Unset): Data source accounts included in transfer
        segments (list[TransferSegment] | Unset): Data segments included in transfer
        license_ (TransferConfigurationResponseLicense | Unset): License information
        schedule (list[TransferSchedule] | Unset): Transfer schedule configuration
        data_source (TransferConfigurationResponseDataSource | Unset): Data source information and settings
        notification_recipients (list[TransferConfigurationResponseNotificationRecipientsType0Item] | None | Unset):
            Email recipients for transfer notifications
        external_url (None | str | Unset): External URL for DTS BigQuery transfers
    """

    transfer_id: int | Unset = UNSET
    display_name: str | Unset = UNSET
    schema_id: int | Unset = UNSET
    destination_id: int | None | Unset = UNSET
    accounts: list[TransferAccount] | Unset = UNSET
    segments: list[TransferSegment] | Unset = UNSET
    license_: TransferConfigurationResponseLicense | Unset = UNSET
    schedule: list[TransferSchedule] | Unset = UNSET
    data_source: TransferConfigurationResponseDataSource | Unset = UNSET
    notification_recipients: list[TransferConfigurationResponseNotificationRecipientsType0Item] | None | Unset = UNSET
    external_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transfer_id = self.transfer_id

        display_name = self.display_name

        schema_id = self.schema_id

        destination_id: int | None | Unset
        if isinstance(self.destination_id, Unset):
            destination_id = UNSET
        else:
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

        license_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.license_, Unset):
            license_ = self.license_.to_dict()

        schedule: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = []
            for schedule_item_data in self.schedule:
                schedule_item = schedule_item_data.to_dict()
                schedule.append(schedule_item)

        data_source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data_source, Unset):
            data_source = self.data_source.to_dict()

        notification_recipients: list[dict[str, Any]] | None | Unset
        if isinstance(self.notification_recipients, Unset):
            notification_recipients = UNSET
        elif isinstance(self.notification_recipients, list):
            notification_recipients = []
            for notification_recipients_type_0_item_data in self.notification_recipients:
                notification_recipients_type_0_item = notification_recipients_type_0_item_data.to_dict()
                notification_recipients.append(notification_recipients_type_0_item)

        else:
            notification_recipients = self.notification_recipients

        external_url: None | str | Unset
        if isinstance(self.external_url, Unset):
            external_url = UNSET
        else:
            external_url = self.external_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transfer_id is not UNSET:
            field_dict["transfer_id"] = transfer_id
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
        if license_ is not UNSET:
            field_dict["license"] = license_
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if notification_recipients is not UNSET:
            field_dict["notification_recipients"] = notification_recipients
        if external_url is not UNSET:
            field_dict["external_url"] = external_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_account import TransferAccount
        from ..models.transfer_configuration_response_data_source import TransferConfigurationResponseDataSource
        from ..models.transfer_configuration_response_license import TransferConfigurationResponseLicense
        from ..models.transfer_configuration_response_notification_recipients_type_0_item import (
            TransferConfigurationResponseNotificationRecipientsType0Item,
        )
        from ..models.transfer_schedule import TransferSchedule
        from ..models.transfer_segment import TransferSegment

        d = dict(src_dict)
        transfer_id = d.pop("transfer_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        schema_id = d.pop("schema_id", UNSET)

        def _parse_destination_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        destination_id = _parse_destination_id(d.pop("destination_id", UNSET))

        _accounts = d.pop("accounts", UNSET)
        accounts: list[TransferAccount] | Unset = UNSET
        if _accounts is not UNSET:
            accounts = []
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

        _license_ = d.pop("license", UNSET)
        license_: TransferConfigurationResponseLicense | Unset
        if isinstance(_license_, Unset):
            license_ = UNSET
        else:
            license_ = TransferConfigurationResponseLicense.from_dict(_license_)

        _schedule = d.pop("schedule", UNSET)
        schedule: list[TransferSchedule] | Unset = UNSET
        if _schedule is not UNSET:
            schedule = []
            for schedule_item_data in _schedule:
                schedule_item = TransferSchedule.from_dict(schedule_item_data)

                schedule.append(schedule_item)

        _data_source = d.pop("data_source", UNSET)
        data_source: TransferConfigurationResponseDataSource | Unset
        if isinstance(_data_source, Unset):
            data_source = UNSET
        else:
            data_source = TransferConfigurationResponseDataSource.from_dict(_data_source)

        def _parse_notification_recipients(
            data: object,
        ) -> list[TransferConfigurationResponseNotificationRecipientsType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                notification_recipients_type_0 = []
                _notification_recipients_type_0 = data
                for notification_recipients_type_0_item_data in _notification_recipients_type_0:
                    notification_recipients_type_0_item = (
                        TransferConfigurationResponseNotificationRecipientsType0Item.from_dict(
                            notification_recipients_type_0_item_data
                        )
                    )

                    notification_recipients_type_0.append(notification_recipients_type_0_item)

                return notification_recipients_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[TransferConfigurationResponseNotificationRecipientsType0Item] | None | Unset, data)

        notification_recipients = _parse_notification_recipients(d.pop("notification_recipients", UNSET))

        def _parse_external_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_url = _parse_external_url(d.pop("external_url", UNSET))

        transfer_configuration_response = cls(
            transfer_id=transfer_id,
            display_name=display_name,
            schema_id=schema_id,
            destination_id=destination_id,
            accounts=accounts,
            segments=segments,
            license_=license_,
            schedule=schedule,
            data_source=data_source,
            notification_recipients=notification_recipients,
            external_url=external_url,
        )

        transfer_configuration_response.additional_properties = d
        return transfer_configuration_response

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
