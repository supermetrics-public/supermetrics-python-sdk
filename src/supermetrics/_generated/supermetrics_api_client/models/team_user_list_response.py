from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.meta import Meta
    from ..models.team_user import TeamUser


T = TypeVar("T", bound="TeamUserListResponse")


@_attrs_define
class TeamUserListResponse:
    """Response envelope containing a list of team users.

    Attributes:
        meta (Meta): Metadata included in every API response.
        data (list[TeamUser]): List of team users Example: [{'user_id': 1, 'email': 'user@example.com', 'first_name':
            'John', 'last_name': 'Doe', 'role': 'member', 'created_at': '2026-01-01T00:00:00+00:00'}].
    """

    meta: Meta
    data: list[TeamUser]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta = self.meta.to_dict()

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.meta import Meta
        from ..models.team_user import TeamUser

        d = dict(src_dict)
        meta = Meta.from_dict(d.pop("meta"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = TeamUser.from_dict(data_item_data)

            data.append(data_item)

        team_user_list_response = cls(
            meta=meta,
            data=data,
        )

        team_user_list_response.additional_properties = d
        return team_user_list_response

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
