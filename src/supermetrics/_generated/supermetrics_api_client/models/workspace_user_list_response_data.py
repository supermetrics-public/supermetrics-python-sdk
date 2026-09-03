from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_user import WorkspaceUser


T = TypeVar("T", bound="WorkspaceUserListResponseData")


@_attrs_define
class WorkspaceUserListResponseData:
    """Workspace users payload

    Attributes:
        public_uuid (UUID | Unset): UUID of the workspace Example: 71bc0582-31b5-11f1-a55c-4201ac182030.
        users (list[WorkspaceUser] | Unset): List of workspace users
    """

    public_uuid: UUID | Unset = UNSET
    users: list[WorkspaceUser] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        public_uuid: str | Unset = UNSET
        if not isinstance(self.public_uuid, Unset):
            public_uuid = str(self.public_uuid)

        users: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if public_uuid is not UNSET:
            field_dict["public_uuid"] = public_uuid
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_user import WorkspaceUser

        d = dict(src_dict)
        _public_uuid = d.pop("public_uuid", UNSET)
        public_uuid: UUID | Unset
        if isinstance(_public_uuid, Unset):
            public_uuid = UNSET
        else:
            public_uuid = UUID(_public_uuid)

        _users = d.pop("users", UNSET)
        users: list[WorkspaceUser] | Unset = UNSET
        if _users is not UNSET:
            users = []
            for users_item_data in _users:
                users_item = WorkspaceUser.from_dict(users_item_data)

                users.append(users_item)

        workspace_user_list_response_data = cls(
            public_uuid=public_uuid,
            users=users,
        )

        workspace_user_list_response_data.additional_properties = d
        return workspace_user_list_response_data

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
