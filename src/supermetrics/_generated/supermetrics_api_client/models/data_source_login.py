from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.data_source_login_type import DataSourceLoginType
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.data_source import DataSource
  from ..models.user import User





T = TypeVar("T", bound="DataSourceLogin")



@_attrs_define
class DataSourceLogin:
    """ 
        Attributes:
            type_ (DataSourceLoginType | Unset):
            login_id (str | Unset): Supermetrics login ID
            login_type (str | Unset): Authentication type. Note that some data sources support multiple types, and user can
                choose between them.
            username (str | Unset): Authenticated username, used in queries as ds_user
            display_name (str | Unset): Visible name for this authentication in product UIs
            ds_info (DataSource | Unset):
            default_scopes (list[str] | Unset): List of default source API scopes used in authentication
            additional_scopes (list[str] | Unset): List of additional source API scopes user has granted to access more data
            auth_time (datetime.datetime | Unset): ISO 8601 datetime for when last user authentication occurred
            auth_user_info (User | Unset):
            expiry_time (datetime.datetime | None | Unset): ISO 8601 datetime for when authentication expires, if any
            revoked_time (datetime.datetime | None | Unset): ISO 8601 datetime for when authentication was revoked, if any
            is_refreshable (bool | Unset): Whether authentication can be automatically refreshed after expiry time, without
                user involvement
            is_shared (bool | Unset): Whether login is shared with all team users
     """

    type_: DataSourceLoginType | Unset = UNSET
    login_id: str | Unset = UNSET
    login_type: str | Unset = UNSET
    username: str | Unset = UNSET
    display_name: str | Unset = UNSET
    ds_info: DataSource | Unset = UNSET
    default_scopes: list[str] | Unset = UNSET
    additional_scopes: list[str] | Unset = UNSET
    auth_time: datetime.datetime | Unset = UNSET
    auth_user_info: User | Unset = UNSET
    expiry_time: datetime.datetime | None | Unset = UNSET
    revoked_time: datetime.datetime | None | Unset = UNSET
    is_refreshable: bool | Unset = UNSET
    is_shared: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.data_source import DataSource
        from ..models.user import User
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        login_id = self.login_id

        login_type = self.login_type

        username = self.username

        display_name = self.display_name

        ds_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ds_info, Unset):
            ds_info = self.ds_info.to_dict()

        default_scopes: list[str] | Unset = UNSET
        if not isinstance(self.default_scopes, Unset):
            default_scopes = self.default_scopes



        additional_scopes: list[str] | Unset = UNSET
        if not isinstance(self.additional_scopes, Unset):
            additional_scopes = self.additional_scopes



        auth_time: str | Unset = UNSET
        if not isinstance(self.auth_time, Unset):
            auth_time = self.auth_time.isoformat()

        auth_user_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auth_user_info, Unset):
            auth_user_info = self.auth_user_info.to_dict()

        expiry_time: None | str | Unset
        if isinstance(self.expiry_time, Unset):
            expiry_time = UNSET
        elif isinstance(self.expiry_time, datetime.datetime):
            expiry_time = self.expiry_time.isoformat()
        else:
            expiry_time = self.expiry_time

        revoked_time: None | str | Unset
        if isinstance(self.revoked_time, Unset):
            revoked_time = UNSET
        elif isinstance(self.revoked_time, datetime.datetime):
            revoked_time = self.revoked_time.isoformat()
        else:
            revoked_time = self.revoked_time

        is_refreshable = self.is_refreshable

        is_shared = self.is_shared


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["@type"] = type_
        if login_id is not UNSET:
            field_dict["login_id"] = login_id
        if login_type is not UNSET:
            field_dict["login_type"] = login_type
        if username is not UNSET:
            field_dict["username"] = username
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if ds_info is not UNSET:
            field_dict["ds_info"] = ds_info
        if default_scopes is not UNSET:
            field_dict["default_scopes"] = default_scopes
        if additional_scopes is not UNSET:
            field_dict["additional_scopes"] = additional_scopes
        if auth_time is not UNSET:
            field_dict["auth_time"] = auth_time
        if auth_user_info is not UNSET:
            field_dict["auth_user_info"] = auth_user_info
        if expiry_time is not UNSET:
            field_dict["expiry_time"] = expiry_time
        if revoked_time is not UNSET:
            field_dict["revoked_time"] = revoked_time
        if is_refreshable is not UNSET:
            field_dict["is_refreshable"] = is_refreshable
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_source import DataSource
        from ..models.user import User
        d = dict(src_dict)
        _type_ = d.pop("@type", UNSET)
        type_: DataSourceLoginType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = DataSourceLoginType(_type_)




        login_id = d.pop("login_id", UNSET)

        login_type = d.pop("login_type", UNSET)

        username = d.pop("username", UNSET)

        display_name = d.pop("display_name", UNSET)

        _ds_info = d.pop("ds_info", UNSET)
        ds_info: DataSource | Unset
        if isinstance(_ds_info,  Unset):
            ds_info = UNSET
        else:
            ds_info = DataSource.from_dict(_ds_info)




        default_scopes = cast(list[str], d.pop("default_scopes", UNSET))


        additional_scopes = cast(list[str], d.pop("additional_scopes", UNSET))


        _auth_time = d.pop("auth_time", UNSET)
        auth_time: datetime.datetime | Unset
        if isinstance(_auth_time,  Unset):
            auth_time = UNSET
        else:
            auth_time = isoparse(_auth_time)




        _auth_user_info = d.pop("auth_user_info", UNSET)
        auth_user_info: User | Unset
        if isinstance(_auth_user_info,  Unset):
            auth_user_info = UNSET
        else:
            auth_user_info = User.from_dict(_auth_user_info)




        def _parse_expiry_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiry_time_type_0 = isoparse(data)



                return expiry_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expiry_time = _parse_expiry_time(d.pop("expiry_time", UNSET))


        def _parse_revoked_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_time_type_0 = isoparse(data)



                return revoked_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        revoked_time = _parse_revoked_time(d.pop("revoked_time", UNSET))


        is_refreshable = d.pop("is_refreshable", UNSET)

        is_shared = d.pop("is_shared", UNSET)

        data_source_login = cls(
            type_=type_,
            login_id=login_id,
            login_type=login_type,
            username=username,
            display_name=display_name,
            ds_info=ds_info,
            default_scopes=default_scopes,
            additional_scopes=additional_scopes,
            auth_time=auth_time,
            auth_user_info=auth_user_info,
            expiry_time=expiry_time,
            revoked_time=revoked_time,
            is_refreshable=is_refreshable,
            is_shared=is_shared,
        )


        data_source_login.additional_properties = d
        return data_source_login

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
