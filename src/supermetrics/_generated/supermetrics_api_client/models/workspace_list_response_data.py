from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_list_item import WorkspaceListItem


T = TypeVar("T", bound="WorkspaceListResponseData")


@_attrs_define
class WorkspaceListResponseData:
    """Workspace list payload

    Attributes:
        workspaces (list[WorkspaceListItem] | Unset): List of workspaces
        unique_users_in_workspaces_count (int | Unset): Count of unique users across all workspaces Example: 12.
    """

    workspaces: list[WorkspaceListItem] | Unset = UNSET
    unique_users_in_workspaces_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workspaces: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.workspaces, Unset):
            workspaces = []
            for workspaces_item_data in self.workspaces:
                workspaces_item = workspaces_item_data.to_dict()
                workspaces.append(workspaces_item)

        unique_users_in_workspaces_count = self.unique_users_in_workspaces_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces
        if unique_users_in_workspaces_count is not UNSET:
            field_dict["unique_users_in_workspaces_count"] = unique_users_in_workspaces_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_list_item import WorkspaceListItem

        d = dict(src_dict)
        _workspaces = d.pop("workspaces", UNSET)
        workspaces: list[WorkspaceListItem] | Unset = UNSET
        if _workspaces is not UNSET:
            workspaces = []
            for workspaces_item_data in _workspaces:
                workspaces_item = WorkspaceListItem.from_dict(workspaces_item_data)

                workspaces.append(workspaces_item)

        unique_users_in_workspaces_count = d.pop("unique_users_in_workspaces_count", UNSET)

        workspace_list_response_data = cls(
            workspaces=workspaces,
            unique_users_in_workspaces_count=unique_users_in_workspaces_count,
        )

        workspace_list_response_data.additional_properties = d
        return workspace_list_response_data

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
