from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.workspace_invite_request_invites_item import WorkspaceInviteRequestInvitesItem


T = TypeVar("T", bound="WorkspaceInviteRequest")


@_attrs_define
class WorkspaceInviteRequest:
    """Users to invite to a workspace.

    Attributes:
        invites (list[WorkspaceInviteRequestInvitesItem]): List of user invitations with email and role Example:
            [{'email': 'user@example.com', 'role': 'EDITOR'}].
    """

    invites: list[WorkspaceInviteRequestInvitesItem]

    def to_dict(self) -> dict[str, Any]:
        invites = []
        for invites_item_data in self.invites:
            invites_item = invites_item_data.to_dict()
            invites.append(invites_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invites": invites,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_invite_request_invites_item import WorkspaceInviteRequestInvitesItem

        d = dict(src_dict)
        invites = []
        _invites = d.pop("invites")
        for invites_item_data in _invites:
            invites_item = WorkspaceInviteRequestInvitesItem.from_dict(invites_item_data)

            invites.append(invites_item)

        workspace_invite_request = cls(
            invites=invites,
        )

        return workspace_invite_request
