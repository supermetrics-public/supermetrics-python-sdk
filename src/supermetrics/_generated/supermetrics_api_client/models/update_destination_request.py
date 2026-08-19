from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_destination_request_fields import UpdateDestinationRequestFields


T = TypeVar("T", bound="UpdateDestinationRequest")


@_attrs_define
class UpdateDestinationRequest:
    """
    Attributes:
        type_ (str): Destination type (e.g., DWH_SNOWFLAKE, DWH_BIGQUERY) Example: DWH_SNOWFLAKE.
        display_name (str): Human-readable name for the destination Example: My Snowflake Destination.
        fields (UpdateDestinationRequestFields): Destination-specific configuration fields (varies by destination type)
        auth_method (str | Unset): Authentication method for the destination Example: AUTH_METHOD_KEY_PAIR.
        new_password (str | Unset): New secret value for credential rotation. Field name varies by auth method (e.g.,
            new_private_key for key-pair auth)
    """

    type_: str
    display_name: str
    fields: UpdateDestinationRequestFields
    auth_method: str | Unset = UNSET
    new_password: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        display_name = self.display_name

        fields = self.fields.to_dict()

        auth_method = self.auth_method

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
        if new_password is not UNSET:
            field_dict["new_password"] = new_password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_destination_request_fields import UpdateDestinationRequestFields

        d = dict(src_dict)
        type_ = d.pop("type")

        display_name = d.pop("display_name")

        fields = UpdateDestinationRequestFields.from_dict(d.pop("fields"))

        auth_method = d.pop("auth_method", UNSET)

        new_password = d.pop("new_password", UNSET)

        update_destination_request = cls(
            type_=type_,
            display_name=display_name,
            fields=fields,
            auth_method=auth_method,
            new_password=new_password,
        )

        return update_destination_request
