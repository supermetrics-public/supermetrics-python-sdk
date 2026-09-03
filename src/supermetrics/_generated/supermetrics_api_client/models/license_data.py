from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseData")


@_attrs_define
class LicenseData:
    """License resource

    Attributes:
        license_id (int | Unset): Unique identifier of the license Example: 1.
        team_id (int | Unset): ID of the team the license belongs to Example: 123.
        license_model (str | Unset): The licensing model type Example: team.
        status (str | Unset): Current status of the license Example: active.
        is_trial (bool | Unset): Whether this is a trial license
        available_data_sources (list[str] | Unset): List of data source identifiers available under this license
            Example: ['GA', 'FA'].
    """

    license_id: int | Unset = UNSET
    team_id: int | Unset = UNSET
    license_model: str | Unset = UNSET
    status: str | Unset = UNSET
    is_trial: bool | Unset = UNSET
    available_data_sources: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        license_id = self.license_id

        team_id = self.team_id

        license_model = self.license_model

        status = self.status

        is_trial = self.is_trial

        available_data_sources: list[str] | Unset = UNSET
        if not isinstance(self.available_data_sources, Unset):
            available_data_sources = self.available_data_sources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if license_id is not UNSET:
            field_dict["license_id"] = license_id
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if license_model is not UNSET:
            field_dict["license_model"] = license_model
        if status is not UNSET:
            field_dict["status"] = status
        if is_trial is not UNSET:
            field_dict["is_trial"] = is_trial
        if available_data_sources is not UNSET:
            field_dict["available_data_sources"] = available_data_sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        license_id = d.pop("license_id", UNSET)

        team_id = d.pop("team_id", UNSET)

        license_model = d.pop("license_model", UNSET)

        status = d.pop("status", UNSET)

        is_trial = d.pop("is_trial", UNSET)

        available_data_sources = cast(list[str], d.pop("available_data_sources", UNSET))

        license_data = cls(
            license_id=license_id,
            team_id=team_id,
            license_model=license_model,
            status=status,
            is_trial=is_trial,
            available_data_sources=available_data_sources,
        )

        license_data.additional_properties = d
        return license_data

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
