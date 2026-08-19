from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_options_response_accounts_item import TransferOptionsResponseAccountsItem
    from ..models.transfer_options_response_data_source import TransferOptionsResponseDataSource
    from ..models.transfer_options_response_license import TransferOptionsResponseLicense
    from ..models.transfer_options_response_logins_item import TransferOptionsResponseLoginsItem
    from ..models.transfer_options_response_schedule_options_item import TransferOptionsResponseScheduleOptionsItem
    from ..models.transfer_options_response_schemas_item import TransferOptionsResponseSchemasItem
    from ..models.transfer_options_response_segments_item import TransferOptionsResponseSegmentsItem


T = TypeVar("T", bound="TransferOptionsResponse")


@_attrs_define
class TransferOptionsResponse:
    """Transfer configuration options for a given source/destination combination

    Attributes:
        data_source (TransferOptionsResponseDataSource | Unset): Data source information and settings
        schedule_options (list[TransferOptionsResponseScheduleOptionsItem] | Unset): Available schedule options
        schemas (list[TransferOptionsResponseSchemasItem] | Unset): Available schemas for the transfer
        logins (list[TransferOptionsResponseLoginsItem] | Unset): Available logins for the data source
        accounts (list[TransferOptionsResponseAccountsItem] | Unset): Available accounts for the data source
        segments (list[TransferOptionsResponseSegmentsItem] | Unset): Available segments for the data source
        license_ (TransferOptionsResponseLicense | Unset): License information for the team
    """

    data_source: TransferOptionsResponseDataSource | Unset = UNSET
    schedule_options: list[TransferOptionsResponseScheduleOptionsItem] | Unset = UNSET
    schemas: list[TransferOptionsResponseSchemasItem] | Unset = UNSET
    logins: list[TransferOptionsResponseLoginsItem] | Unset = UNSET
    accounts: list[TransferOptionsResponseAccountsItem] | Unset = UNSET
    segments: list[TransferOptionsResponseSegmentsItem] | Unset = UNSET
    license_: TransferOptionsResponseLicense | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data_source, Unset):
            data_source = self.data_source.to_dict()

        schedule_options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schedule_options, Unset):
            schedule_options = []
            for schedule_options_item_data in self.schedule_options:
                schedule_options_item = schedule_options_item_data.to_dict()
                schedule_options.append(schedule_options_item)

        schemas: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schemas, Unset):
            schemas = []
            for schemas_item_data in self.schemas:
                schemas_item = schemas_item_data.to_dict()
                schemas.append(schemas_item)

        logins: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.logins, Unset):
            logins = []
            for logins_item_data in self.logins:
                logins_item = logins_item_data.to_dict()
                logins.append(logins_item)

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if schedule_options is not UNSET:
            field_dict["schedule_options"] = schedule_options
        if schemas is not UNSET:
            field_dict["schemas"] = schemas
        if logins is not UNSET:
            field_dict["logins"] = logins
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if segments is not UNSET:
            field_dict["segments"] = segments
        if license_ is not UNSET:
            field_dict["license"] = license_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_options_response_accounts_item import TransferOptionsResponseAccountsItem
        from ..models.transfer_options_response_data_source import TransferOptionsResponseDataSource
        from ..models.transfer_options_response_license import TransferOptionsResponseLicense
        from ..models.transfer_options_response_logins_item import TransferOptionsResponseLoginsItem
        from ..models.transfer_options_response_schedule_options_item import TransferOptionsResponseScheduleOptionsItem
        from ..models.transfer_options_response_schemas_item import TransferOptionsResponseSchemasItem
        from ..models.transfer_options_response_segments_item import TransferOptionsResponseSegmentsItem

        d = dict(src_dict)
        _data_source = d.pop("data_source", UNSET)
        data_source: TransferOptionsResponseDataSource | Unset
        if isinstance(_data_source, Unset):
            data_source = UNSET
        else:
            data_source = TransferOptionsResponseDataSource.from_dict(_data_source)

        _schedule_options = d.pop("schedule_options", UNSET)
        schedule_options: list[TransferOptionsResponseScheduleOptionsItem] | Unset = UNSET
        if _schedule_options is not UNSET:
            schedule_options = []
            for schedule_options_item_data in _schedule_options:
                schedule_options_item = TransferOptionsResponseScheduleOptionsItem.from_dict(schedule_options_item_data)

                schedule_options.append(schedule_options_item)

        _schemas = d.pop("schemas", UNSET)
        schemas: list[TransferOptionsResponseSchemasItem] | Unset = UNSET
        if _schemas is not UNSET:
            schemas = []
            for schemas_item_data in _schemas:
                schemas_item = TransferOptionsResponseSchemasItem.from_dict(schemas_item_data)

                schemas.append(schemas_item)

        _logins = d.pop("logins", UNSET)
        logins: list[TransferOptionsResponseLoginsItem] | Unset = UNSET
        if _logins is not UNSET:
            logins = []
            for logins_item_data in _logins:
                logins_item = TransferOptionsResponseLoginsItem.from_dict(logins_item_data)

                logins.append(logins_item)

        _accounts = d.pop("accounts", UNSET)
        accounts: list[TransferOptionsResponseAccountsItem] | Unset = UNSET
        if _accounts is not UNSET:
            accounts = []
            for accounts_item_data in _accounts:
                accounts_item = TransferOptionsResponseAccountsItem.from_dict(accounts_item_data)

                accounts.append(accounts_item)

        _segments = d.pop("segments", UNSET)
        segments: list[TransferOptionsResponseSegmentsItem] | Unset = UNSET
        if _segments is not UNSET:
            segments = []
            for segments_item_data in _segments:
                segments_item = TransferOptionsResponseSegmentsItem.from_dict(segments_item_data)

                segments.append(segments_item)

        _license_ = d.pop("license", UNSET)
        license_: TransferOptionsResponseLicense | Unset
        if isinstance(_license_, Unset):
            license_ = UNSET
        else:
            license_ = TransferOptionsResponseLicense.from_dict(_license_)

        transfer_options_response = cls(
            data_source=data_source,
            schedule_options=schedule_options,
            schemas=schemas,
            logins=logins,
            accounts=accounts,
            segments=segments,
            license_=license_,
        )

        transfer_options_response.additional_properties = d
        return transfer_options_response

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
