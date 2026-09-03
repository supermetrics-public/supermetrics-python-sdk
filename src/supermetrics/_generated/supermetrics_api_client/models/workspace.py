from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_subscription_type_0 import WorkspaceSubscriptionType0


T = TypeVar("T", bound="Workspace")


@_attrs_define
class Workspace:
    """Workspace data

    Attributes:
        id (UUID | Unset): UUID of the workspace Example: 71bc0582-31b5-11f1-a55c-4201ac182030.
        parent_id (None | Unset | UUID): UUID of the parent workspace, or null for a zero-level workspace Example:
            5d514fda-f2ec-4c6a-afb0-00ffe8066024.
        team_id (int | None | Unset): ID of the team the workspace is linked to Example: 936506.
        date_created (datetime.date | Unset): Date the workspace was created Example: 2026-06-15.
        status (str | Unset): Status of the workspace Example: active.
        team_name (None | str | Unset): Name of the workspace's team Example: Marketing.
        team_display_id (None | str | Unset): Display ID of the workspace's team Example: Display Id 936506.
        parent_team_name (None | str | Unset): Name of the parent workspace's team Example: Acme.
        parent_team_display_id (None | str | Unset): Display ID of the parent workspace's team Example: Display Id
            936505.
        subscription (None | Unset | WorkspaceSubscriptionType0): Subscription details of the workspace, or null when
            none is active
    """

    id: UUID | Unset = UNSET
    parent_id: None | Unset | UUID = UNSET
    team_id: int | None | Unset = UNSET
    date_created: datetime.date | Unset = UNSET
    status: str | Unset = UNSET
    team_name: None | str | Unset = UNSET
    team_display_id: None | str | Unset = UNSET
    parent_team_name: None | str | Unset = UNSET
    parent_team_display_id: None | str | Unset = UNSET
    subscription: None | Unset | WorkspaceSubscriptionType0 = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_subscription_type_0 import WorkspaceSubscriptionType0

        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        parent_id: None | str | Unset
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        elif isinstance(self.parent_id, UUID):
            parent_id = str(self.parent_id)
        else:
            parent_id = self.parent_id

        team_id: int | None | Unset
        if isinstance(self.team_id, Unset):
            team_id = UNSET
        else:
            team_id = self.team_id

        date_created: str | Unset = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        status = self.status

        team_name: None | str | Unset
        if isinstance(self.team_name, Unset):
            team_name = UNSET
        else:
            team_name = self.team_name

        team_display_id: None | str | Unset
        if isinstance(self.team_display_id, Unset):
            team_display_id = UNSET
        else:
            team_display_id = self.team_display_id

        parent_team_name: None | str | Unset
        if isinstance(self.parent_team_name, Unset):
            parent_team_name = UNSET
        else:
            parent_team_name = self.parent_team_name

        parent_team_display_id: None | str | Unset
        if isinstance(self.parent_team_display_id, Unset):
            parent_team_display_id = UNSET
        else:
            parent_team_display_id = self.parent_team_display_id

        subscription: dict[str, Any] | None | Unset
        if isinstance(self.subscription, Unset):
            subscription = UNSET
        elif isinstance(self.subscription, WorkspaceSubscriptionType0):
            subscription = self.subscription.to_dict()
        else:
            subscription = self.subscription

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if status is not UNSET:
            field_dict["status"] = status
        if team_name is not UNSET:
            field_dict["team_name"] = team_name
        if team_display_id is not UNSET:
            field_dict["team_display_id"] = team_display_id
        if parent_team_name is not UNSET:
            field_dict["parent_team_name"] = parent_team_name
        if parent_team_display_id is not UNSET:
            field_dict["parent_team_display_id"] = parent_team_display_id
        if subscription is not UNSET:
            field_dict["subscription"] = subscription

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_subscription_type_0 import WorkspaceSubscriptionType0

        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        def _parse_parent_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_id_type_0 = UUID(data)

                return parent_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        def _parse_team_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        team_id = _parse_team_id(d.pop("team_id", UNSET))

        _date_created = d.pop("date_created", UNSET)
        date_created: datetime.date | Unset
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = datetime.date.fromisoformat(_date_created)

        status = d.pop("status", UNSET)

        def _parse_team_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        team_name = _parse_team_name(d.pop("team_name", UNSET))

        def _parse_team_display_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        team_display_id = _parse_team_display_id(d.pop("team_display_id", UNSET))

        def _parse_parent_team_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_team_name = _parse_parent_team_name(d.pop("parent_team_name", UNSET))

        def _parse_parent_team_display_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_team_display_id = _parse_parent_team_display_id(d.pop("parent_team_display_id", UNSET))

        def _parse_subscription(data: object) -> None | Unset | WorkspaceSubscriptionType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_workspace_subscription_type_0 = WorkspaceSubscriptionType0.from_dict(data)

                return componentsschemas_workspace_subscription_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WorkspaceSubscriptionType0, data)

        subscription = _parse_subscription(d.pop("subscription", UNSET))

        workspace = cls(
            id=id,
            parent_id=parent_id,
            team_id=team_id,
            date_created=date_created,
            status=status,
            team_name=team_name,
            team_display_id=team_display_id,
            parent_team_name=parent_team_name,
            parent_team_display_id=parent_team_display_id,
            subscription=subscription,
        )

        workspace.additional_properties = d
        return workspace

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
