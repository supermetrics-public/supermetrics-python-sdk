from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_connection_request_fields import TestConnectionRequestFields


T = TypeVar("T", bound="TestConnectionRequest")


@_attrs_define
class TestConnectionRequest:
    """
    Attributes:
        type_ (str): Destination type to test Example: DWH_SNOWFLAKE.
        display_name (str): Display name for the connection being tested Example: Test Connection.
        fields (TestConnectionRequestFields): Connection credentials and settings to test
        auth_method (str | Unset): Authentication method to test Example: AUTH_METHOD_KEY_PAIR.
        destination_id (int | Unset): Optional - ID of existing destination to test with new credentials Example: 8.
        new_password (str | Unset): New secret value for credential testing. Field name varies by auth method (e.g.,
            new_private_key for key-pair auth)
    """

    type_: str
    display_name: str
    fields: TestConnectionRequestFields
    auth_method: str | Unset = UNSET
    destination_id: int | Unset = UNSET
    new_password: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        display_name = self.display_name

        fields = self.fields.to_dict()

        auth_method = self.auth_method

        destination_id = self.destination_id

        new_password = self.new_password

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "display_name": display_name,
                "fields": fields,
            }
        )
        if auth_method is not UNSET:
            field_dict["auth_method"] = auth_method
        if destination_id is not UNSET:
            field_dict["destination_id"] = destination_id
        if new_password is not UNSET:
            field_dict["new_password"] = new_password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_connection_request_fields import TestConnectionRequestFields

        d = dict(src_dict)
        type_ = d.pop("type")

        display_name = d.pop("display_name")

        fields = TestConnectionRequestFields.from_dict(d.pop("fields"))

        auth_method = d.pop("auth_method", UNSET)

        destination_id = d.pop("destination_id", UNSET)

        new_password = d.pop("new_password", UNSET)

        test_connection_request = cls(
            type_=type_,
            display_name=display_name,
            fields=fields,
            auth_method=auth_method,
            destination_id=destination_id,
            new_password=new_password,
        )

        return test_connection_request
