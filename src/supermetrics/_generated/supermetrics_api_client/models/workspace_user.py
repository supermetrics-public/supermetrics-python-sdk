from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_user_role import WorkspaceUserRole, check_workspace_user_role
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceUser")


@_attrs_define
class WorkspaceUser:
    """Workspace user data

    Attributes:
        user_id (int | Unset): ID of the user Example: 12345.
        email (str | Unset): Email address of the user Example: user@example.com.
        first_name (str | Unset): First name of the user Example: Ada.
        last_name (str | Unset): Last name of the user Example: Lovelace.
        role (WorkspaceUserRole | Unset): Role of the user in the workspace Example: EDITOR.
    """

    user_id: int | Unset = UNSET
    email: str | Unset = UNSET
    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    role: WorkspaceUserRole | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("user_id", UNSET)

        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        _role = d.pop("role", UNSET)
        role: WorkspaceUserRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = check_workspace_user_role(_role)

        workspace_user = cls(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

        workspace_user.additional_properties = d
        return workspace_user

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
