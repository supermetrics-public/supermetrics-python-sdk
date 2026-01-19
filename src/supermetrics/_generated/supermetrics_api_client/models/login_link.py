from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.login_link_status_code import LoginLinkStatusCode
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="LoginLink")



@_attrs_define
class LoginLink:
    """ 
        Attributes:
            link_id (str | Unset): Supermetrics login link ID
            status_code (LoginLinkStatusCode | Unset): Current link status
            description (str | Unset): Internal link description. Not shown during authentication attempt.
            ds_id (str | Unset): Data source ID
            ds_name (str | Unset): Data source name
            require_username (str | Unset): Data source username that must be used in authentication attempt
            redirect_url (str | Unset): Custom URL to redirect to after successful authentication, if any
            redirect_verifier (str | Unset): Internal verifier string that is passed to redirect_url
            user_id (str | Unset): Supermetrics user ID of the user who will be marked as the primary owner of the login
                credentials
            user_email (str | Unset): Supermetrics user email
            login_url (str | Unset): Full URL to initiate an authentication attempt. Can be accessed multiple times while
                link is open.
            created_time (datetime.datetime | Unset): ISO 8601 datetime for when login link was created
            expiry_time (datetime.datetime | Unset): ISO 8601 datetime for when login link will expire
            login_id (None | str | Unset): Supermetrics login ID for a successful authentication
            login_time (datetime.datetime | None | Unset): ISO 8601 datetime for when authentication occurred
            login_username (None | str | Unset): Username used to authenticate to data source
     """

    link_id: str | Unset = UNSET
    status_code: LoginLinkStatusCode | Unset = UNSET
    description: str | Unset = UNSET
    ds_id: str | Unset = UNSET
    ds_name: str | Unset = UNSET
    require_username: str | Unset = UNSET
    redirect_url: str | Unset = UNSET
    redirect_verifier: str | Unset = UNSET
    user_id: str | Unset = UNSET
    user_email: str | Unset = UNSET
    login_url: str | Unset = UNSET
    created_time: datetime.datetime | Unset = UNSET
    expiry_time: datetime.datetime | Unset = UNSET
    login_id: None | str | Unset = UNSET
    login_time: datetime.datetime | None | Unset = UNSET
    login_username: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        link_id = self.link_id

        status_code: str | Unset = UNSET
        if not isinstance(self.status_code, Unset):
            status_code = self.status_code.value


        description = self.description

        ds_id = self.ds_id

        ds_name = self.ds_name

        require_username = self.require_username

        redirect_url = self.redirect_url

        redirect_verifier = self.redirect_verifier

        user_id = self.user_id

        user_email = self.user_email

        login_url = self.login_url

        created_time: str | Unset = UNSET
        if not isinstance(self.created_time, Unset):
            created_time = self.created_time.isoformat()

        expiry_time: str | Unset = UNSET
        if not isinstance(self.expiry_time, Unset):
            expiry_time = self.expiry_time.isoformat()

        login_id: None | str | Unset
        if isinstance(self.login_id, Unset):
            login_id = UNSET
        else:
            login_id = self.login_id

        login_time: None | str | Unset
        if isinstance(self.login_time, Unset):
            login_time = UNSET
        elif isinstance(self.login_time, datetime.datetime):
            login_time = self.login_time.isoformat()
        else:
            login_time = self.login_time

        login_username: None | str | Unset
        if isinstance(self.login_username, Unset):
            login_username = UNSET
        else:
            login_username = self.login_username


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if link_id is not UNSET:
            field_dict["link_id"] = link_id
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if description is not UNSET:
            field_dict["description"] = description
        if ds_id is not UNSET:
            field_dict["ds_id"] = ds_id
        if ds_name is not UNSET:
            field_dict["ds_name"] = ds_name
        if require_username is not UNSET:
            field_dict["require_username"] = require_username
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url
        if redirect_verifier is not UNSET:
            field_dict["redirect_verifier"] = redirect_verifier
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
        if login_url is not UNSET:
            field_dict["login_url"] = login_url
        if created_time is not UNSET:
            field_dict["created_time"] = created_time
        if expiry_time is not UNSET:
            field_dict["expiry_time"] = expiry_time
        if login_id is not UNSET:
            field_dict["login_id"] = login_id
        if login_time is not UNSET:
            field_dict["login_time"] = login_time
        if login_username is not UNSET:
            field_dict["login_username"] = login_username

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        link_id = d.pop("link_id", UNSET)

        _status_code = d.pop("status_code", UNSET)
        status_code: LoginLinkStatusCode | Unset
        if isinstance(_status_code,  Unset):
            status_code = UNSET
        else:
            status_code = LoginLinkStatusCode(_status_code)




        description = d.pop("description", UNSET)

        ds_id = d.pop("ds_id", UNSET)

        ds_name = d.pop("ds_name", UNSET)

        require_username = d.pop("require_username", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        redirect_verifier = d.pop("redirect_verifier", UNSET)

        user_id = d.pop("user_id", UNSET)

        user_email = d.pop("user_email", UNSET)

        login_url = d.pop("login_url", UNSET)

        _created_time = d.pop("created_time", UNSET)
        created_time: datetime.datetime | Unset
        if isinstance(_created_time,  Unset):
            created_time = UNSET
        else:
            created_time = isoparse(_created_time)




        _expiry_time = d.pop("expiry_time", UNSET)
        expiry_time: datetime.datetime | Unset
        if isinstance(_expiry_time,  Unset):
            expiry_time = UNSET
        else:
            expiry_time = isoparse(_expiry_time)




        def _parse_login_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        login_id = _parse_login_id(d.pop("login_id", UNSET))


        def _parse_login_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                login_time_type_0 = isoparse(data)



                return login_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        login_time = _parse_login_time(d.pop("login_time", UNSET))


        def _parse_login_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        login_username = _parse_login_username(d.pop("login_username", UNSET))


        login_link = cls(
            link_id=link_id,
            status_code=status_code,
            description=description,
            ds_id=ds_id,
            ds_name=ds_name,
            require_username=require_username,
            redirect_url=redirect_url,
            redirect_verifier=redirect_verifier,
            user_id=user_id,
            user_email=user_email,
            login_url=login_url,
            created_time=created_time,
            expiry_time=expiry_time,
            login_id=login_id,
            login_time=login_time,
            login_username=login_username,
        )


        login_link.additional_properties = d
        return login_link

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
