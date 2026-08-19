from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_destination_request_fields import CreateDestinationRequestFields


T = TypeVar("T", bound="CreateDestinationRequest")


@_attrs_define
class CreateDestinationRequest:
    """
    Attributes:
        type_ (str): Destination type (e.g., DWH_SNOWFLAKE, DWH_BIGQUERY) Example: DWH_SNOWFLAKE.
        display_name (str): Human-readable name for the destination Example: My Snowflake Destination.
        fields (CreateDestinationRequestFields): Destination-specific configuration fields (varies by destination type)
            Example: {'hostname': 'any-domain.my-region.snowflakecomputing.com', 'warehouse': 'DEMO_WH', 'database_name':
            'TEST_DB', 'schema': 'PUBLIC', 'role': 'ACCOUNTADMIN', 'username': 'USER', 'private_key': '-----BEGIN ENCRYPTED
            PRIVATE KEY-----...', 'passphrase': '***'}.
        auth_method (str | Unset): Authentication method for the destination Example: AUTH_METHOD_KEY_PAIR.
    """

    type_: str
    display_name: str
    fields: CreateDestinationRequestFields
    auth_method: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        display_name = self.display_name

        fields = self.fields.to_dict()

        auth_method = self.auth_method

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_destination_request_fields import CreateDestinationRequestFields

        d = dict(src_dict)
        type_ = d.pop("type")

        display_name = d.pop("display_name")

        fields = CreateDestinationRequestFields.from_dict(d.pop("fields"))

        auth_method = d.pop("auth_method", UNSET)

        create_destination_request = cls(
            type_=type_,
            display_name=display_name,
            fields=fields,
            auth_method=auth_method,
        )

        return create_destination_request
