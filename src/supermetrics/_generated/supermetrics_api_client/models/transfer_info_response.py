from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_info_response_backfill_type_0 import TransferInfoResponseBackfillType0
    from ..models.transfer_info_response_data_source_type_0 import TransferInfoResponseDataSourceType0
    from ..models.transfer_info_response_destination_type_0 import TransferInfoResponseDestinationType0


T = TypeVar("T", bound="TransferInfoResponse")


@_attrs_define
class TransferInfoResponse:
    """Transfer information for list endpoint

    Attributes:
        dwh_transfer_id (int | Unset): The transfer ID Example: 36091.
        display_name (str | Unset): Display name of the transfer Example: AW enhanced 2022-11-17.
        external_transfer_id (str | Unset): External identifier for the transfer Example: ext-36091.
        status (str | Unset): Transfer status Example: active.
        state (str | Unset): Transfer state (active or paused) Example: active.
        schedule (str | Unset): Schedule description Example: daily.
        run_date (str | Unset): Last run date Example: 2026-01-01.
        data_source (None | TransferInfoResponseDataSourceType0 | Unset): Data source information
        destination (None | TransferInfoResponseDestinationType0 | Unset): Destination information
        accounts (list[str] | Unset): Account identifiers
        backfill (None | TransferInfoResponseBackfillType0 | Unset): Backfill statistics
    """

    dwh_transfer_id: int | Unset = UNSET
    display_name: str | Unset = UNSET
    external_transfer_id: str | Unset = UNSET
    status: str | Unset = UNSET
    state: str | Unset = UNSET
    schedule: str | Unset = UNSET
    run_date: str | Unset = UNSET
    data_source: None | TransferInfoResponseDataSourceType0 | Unset = UNSET
    destination: None | TransferInfoResponseDestinationType0 | Unset = UNSET
    accounts: list[str] | Unset = UNSET
    backfill: None | TransferInfoResponseBackfillType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.transfer_info_response_backfill_type_0 import TransferInfoResponseBackfillType0
        from ..models.transfer_info_response_data_source_type_0 import TransferInfoResponseDataSourceType0
        from ..models.transfer_info_response_destination_type_0 import TransferInfoResponseDestinationType0

        dwh_transfer_id = self.dwh_transfer_id

        display_name = self.display_name

        external_transfer_id = self.external_transfer_id

        status = self.status

        state = self.state

        schedule = self.schedule

        run_date = self.run_date

        data_source: dict[str, Any] | None | Unset
        if isinstance(self.data_source, Unset):
            data_source = UNSET
        elif isinstance(self.data_source, TransferInfoResponseDataSourceType0):
            data_source = self.data_source.to_dict()
        else:
            data_source = self.data_source

        destination: dict[str, Any] | None | Unset
        if isinstance(self.destination, Unset):
            destination = UNSET
        elif isinstance(self.destination, TransferInfoResponseDestinationType0):
            destination = self.destination.to_dict()
        else:
            destination = self.destination

        accounts: list[str] | Unset = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts

        backfill: dict[str, Any] | None | Unset
        if isinstance(self.backfill, Unset):
            backfill = UNSET
        elif isinstance(self.backfill, TransferInfoResponseBackfillType0):
            backfill = self.backfill.to_dict()
        else:
            backfill = self.backfill

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dwh_transfer_id is not UNSET:
            field_dict["dwh_transfer_id"] = dwh_transfer_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if external_transfer_id is not UNSET:
            field_dict["external_transfer_id"] = external_transfer_id
        if status is not UNSET:
            field_dict["status"] = status
        if state is not UNSET:
            field_dict["state"] = state
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if run_date is not UNSET:
            field_dict["run_date"] = run_date
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if destination is not UNSET:
            field_dict["destination"] = destination
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if backfill is not UNSET:
            field_dict["backfill"] = backfill

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_info_response_backfill_type_0 import TransferInfoResponseBackfillType0
        from ..models.transfer_info_response_data_source_type_0 import TransferInfoResponseDataSourceType0
        from ..models.transfer_info_response_destination_type_0 import TransferInfoResponseDestinationType0

        d = dict(src_dict)
        dwh_transfer_id = d.pop("dwh_transfer_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        external_transfer_id = d.pop("external_transfer_id", UNSET)

        status = d.pop("status", UNSET)

        state = d.pop("state", UNSET)

        schedule = d.pop("schedule", UNSET)

        run_date = d.pop("run_date", UNSET)

        def _parse_data_source(data: object) -> None | TransferInfoResponseDataSourceType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_source_type_0 = TransferInfoResponseDataSourceType0.from_dict(data)

                return data_source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TransferInfoResponseDataSourceType0 | Unset, data)

        data_source = _parse_data_source(d.pop("data_source", UNSET))

        def _parse_destination(data: object) -> None | TransferInfoResponseDestinationType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                destination_type_0 = TransferInfoResponseDestinationType0.from_dict(data)

                return destination_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TransferInfoResponseDestinationType0 | Unset, data)

        destination = _parse_destination(d.pop("destination", UNSET))

        accounts = cast(list[str], d.pop("accounts", UNSET))

        def _parse_backfill(data: object) -> None | TransferInfoResponseBackfillType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                backfill_type_0 = TransferInfoResponseBackfillType0.from_dict(data)

                return backfill_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TransferInfoResponseBackfillType0 | Unset, data)

        backfill = _parse_backfill(d.pop("backfill", UNSET))

        transfer_info_response = cls(
            dwh_transfer_id=dwh_transfer_id,
            display_name=display_name,
            external_transfer_id=external_transfer_id,
            status=status,
            state=state,
            schedule=schedule,
            run_date=run_date,
            data_source=data_source,
            destination=destination,
            accounts=accounts,
            backfill=backfill,
        )

        transfer_info_response.additional_properties = d
        return transfer_info_response

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
