from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

T = TypeVar("T", bound="WorkspaceCreateRequest")


@_attrs_define
class WorkspaceCreateRequest:
    """Payload for creating a new sub-workspace.

    Attributes:
        name (str): Name of the new workspace Example: Marketing.
        parent_workspace_id (UUID): UUID of the parent workspace Example: 71bc0582-31b5-11f1-a55c-4201ac182030.
    """

    name: str
    parent_workspace_id: UUID

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        parent_workspace_id = str(self.parent_workspace_id)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "parent_workspace_id": parent_workspace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        parent_workspace_id = UUID(d.pop("parent_workspace_id"))

        workspace_create_request = cls(
            name=name,
            parent_workspace_id=parent_workspace_id,
        )

        return workspace_create_request
