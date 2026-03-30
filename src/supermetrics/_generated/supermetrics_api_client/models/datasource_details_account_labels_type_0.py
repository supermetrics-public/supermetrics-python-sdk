from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasourceDetailsAccountLabelsType0")


@_attrs_define
class DatasourceDetailsAccountLabelsType0:
    """Labels for the accounts

    Attributes:
        plural (str | Unset): Plural form of the account label Example: Accounts.
        singular (str | Unset): Singular form of the account label Example: Account.
    """

    plural: str | Unset = UNSET
    singular: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plural = self.plural

        singular = self.singular

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plural is not UNSET:
            field_dict["plural"] = plural
        if singular is not UNSET:
            field_dict["singular"] = singular

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plural = d.pop("plural", UNSET)

        singular = d.pop("singular", UNSET)

        datasource_details_account_labels_type_0 = cls(
            plural=plural,
            singular=singular,
        )

        datasource_details_account_labels_type_0.additional_properties = d
        return datasource_details_account_labels_type_0

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
