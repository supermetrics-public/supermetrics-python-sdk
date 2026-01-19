from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="CreateLoginLinkBody")



@_attrs_define
class CreateLoginLinkBody:
    """ 
        Attributes:
            ds_id (str): Data source ID
            expiry_time (datetime.datetime): Link expiry time as date, datetime or relative time string. Value is saved as
                ISO 8601, defaulting to midnight as time of day.
            description (str | Unset): Internal description for the link. Not shown during the authentication attempt.
            require_username (str | Unset): Data source username that needs to be used in authentication attempt. Normally
                used when renewing existing credentials.
            redirect_url (str | Unset): Custom URL to redirect to after successful authentication.
     """

    ds_id: str
    expiry_time: datetime.datetime
    description: str | Unset = UNSET
    require_username: str | Unset = UNSET
    redirect_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ds_id = self.ds_id

        expiry_time = self.expiry_time.isoformat()

        description = self.description

        require_username = self.require_username

        redirect_url = self.redirect_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ds_id": ds_id,
            "expiry_time": expiry_time,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if require_username is not UNSET:
            field_dict["require_username"] = require_username
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ds_id = d.pop("ds_id")

        expiry_time = isoparse(d.pop("expiry_time"))




        description = d.pop("description", UNSET)

        require_username = d.pop("require_username", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        create_login_link_body = cls(
            ds_id=ds_id,
            expiry_time=expiry_time,
            description=description,
            require_username=require_username,
            redirect_url=redirect_url,
        )


        create_login_link_body.additional_properties = d
        return create_login_link_body

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
