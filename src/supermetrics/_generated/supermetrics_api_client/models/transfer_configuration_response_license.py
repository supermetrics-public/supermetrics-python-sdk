from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_configuration_response_license_features import TransferConfigurationResponseLicenseFeatures


T = TypeVar("T", bound="TransferConfigurationResponseLicense")


@_attrs_define
class TransferConfigurationResponseLicense:
    """License information

    Attributes:
        id (int | Unset): License ID
        product_title (str | Unset): Product title
        license_title (str | Unset): License title
        is_expired (bool | Unset): Whether license is expired
        is_trial (bool | Unset): Whether license is trial
        end_date (datetime.datetime | Unset): License end date
        features (TransferConfigurationResponseLicenseFeatures | Unset): License features
    """

    id: int | Unset = UNSET
    product_title: str | Unset = UNSET
    license_title: str | Unset = UNSET
    is_expired: bool | Unset = UNSET
    is_trial: bool | Unset = UNSET
    end_date: datetime.datetime | Unset = UNSET
    features: TransferConfigurationResponseLicenseFeatures | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        product_title = self.product_title

        license_title = self.license_title

        is_expired = self.is_expired

        is_trial = self.is_trial

        end_date: str | Unset = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        features: dict[str, Any] | Unset = UNSET
        if not isinstance(self.features, Unset):
            features = self.features.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if product_title is not UNSET:
            field_dict["product_title"] = product_title
        if license_title is not UNSET:
            field_dict["license_title"] = license_title
        if is_expired is not UNSET:
            field_dict["is_expired"] = is_expired
        if is_trial is not UNSET:
            field_dict["is_trial"] = is_trial
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if features is not UNSET:
            field_dict["features"] = features

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_configuration_response_license_features import (
            TransferConfigurationResponseLicenseFeatures,
        )

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        product_title = d.pop("product_title", UNSET)

        license_title = d.pop("license_title", UNSET)

        is_expired = d.pop("is_expired", UNSET)

        is_trial = d.pop("is_trial", UNSET)

        _end_date = d.pop("end_date", UNSET)
        end_date: datetime.datetime | Unset
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = datetime.datetime.fromisoformat(_end_date)

        _features = d.pop("features", UNSET)
        features: TransferConfigurationResponseLicenseFeatures | Unset
        if isinstance(_features, Unset):
            features = UNSET
        else:
            features = TransferConfigurationResponseLicenseFeatures.from_dict(_features)

        transfer_configuration_response_license = cls(
            id=id,
            product_title=product_title,
            license_title=license_title,
            is_expired=is_expired,
            is_trial=is_trial,
            end_date=end_date,
            features=features,
        )

        transfer_configuration_response_license.additional_properties = d
        return transfer_configuration_response_license

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
