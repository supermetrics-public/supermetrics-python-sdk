from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.team_transformation_output_field_type import (
    TeamTransformationOutputFieldType,
    check_team_transformation_output_field_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.team_transformation_output_definition import TeamTransformationOutputDefinition
    from ..models.transformation_user_output import TransformationUserOutput


T = TypeVar("T", bound="TeamTransformationOutput")


@_attrs_define
class TeamTransformationOutput:
    """A persisted custom field (field transformation) as returned by read operations.

    Example:
        {'id': 42, 'name': 'spec_example_field', 'data_source_id': 'GAWA', 'display_name': 'Spec Example Field Updated',
            'description': 'Updated temporary transformation for spec examples', 'field_type': 'dim', 'data_type':
            'string.text.value', 'modified_time_utc': '2026-04-06T10:59:04+0000', 'modified_user': {'email':
            'user@supermetrics.com', 'first_name': 'John', 'last_name': 'Doe'}, 'definition': {'items': [{'type':
            'function', 'name': 'upper_case', 'arguments': [{'name': 'value', 'value': {'type': 'data_source_field',
            'value': 'platform'}}], 'description': None}]}, 'report_types': ['Default']}

    Attributes:
        id (int | Unset): Unique identifier of the custom field. Example: 42.
        name (str | Unset): Unique machine name of the field transformation. Example: spec_example_field.
        data_source_id (str | Unset): ID of the data source the transformation belongs to. Example: GAWA.
        display_name (str | Unset): User-facing name of the transformation shown in the UI. Example: Spec Example Field
            Updated.
        description (str | Unset): Free-text description of the transformation. Example: Updated temporary
            transformation for spec examples.
        field_type (TeamTransformationOutputFieldType | Unset): Field kind: `dim` (dimension) or `met` (metric).
            Example: dim.
        data_type (str | Unset): Data type of the transformed field. Example: string.text.value.
        modified_time_utc (datetime.datetime | Unset): Timestamp of the last modification, in UTC. Serialized with a
            numeric offset (e.g. "+0000") rather than a trailing "Z". Example: 2026-04-06T10:59:04+0000.
        modified_user (TransformationUserOutput | Unset): The user who last modified a custom field transformation.
            Example: {'email': 'user@supermetrics.com', 'first_name': 'John', 'last_name': 'Doe'}.
        definition (TeamTransformationOutputDefinition | Unset): Wrapper holding the ordered transformation steps.
        report_types (list[str] | Unset): Report types associated with the transformation. Example: ['Default'].
    """

    id: int | Unset = UNSET
    name: str | Unset = UNSET
    data_source_id: str | Unset = UNSET
    display_name: str | Unset = UNSET
    description: str | Unset = UNSET
    field_type: TeamTransformationOutputFieldType | Unset = UNSET
    data_type: str | Unset = UNSET
    modified_time_utc: datetime.datetime | Unset = UNSET
    modified_user: TransformationUserOutput | Unset = UNSET
    definition: TeamTransformationOutputDefinition | Unset = UNSET
    report_types: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        data_source_id = self.data_source_id

        display_name = self.display_name

        description = self.description

        field_type: str | Unset = UNSET
        if not isinstance(self.field_type, Unset):
            field_type = self.field_type

        data_type = self.data_type

        modified_time_utc: str | Unset = UNSET
        if not isinstance(self.modified_time_utc, Unset):
            modified_time_utc = self.modified_time_utc.isoformat()

        modified_user: dict[str, Any] | Unset = UNSET
        if not isinstance(self.modified_user, Unset):
            modified_user = self.modified_user.to_dict()

        definition: dict[str, Any] | Unset = UNSET
        if not isinstance(self.definition, Unset):
            definition = self.definition.to_dict()

        report_types: list[str] | Unset = UNSET
        if not isinstance(self.report_types, Unset):
            report_types = self.report_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if data_source_id is not UNSET:
            field_dict["data_source_id"] = data_source_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if field_type is not UNSET:
            field_dict["field_type"] = field_type
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if modified_time_utc is not UNSET:
            field_dict["modified_time_utc"] = modified_time_utc
        if modified_user is not UNSET:
            field_dict["modified_user"] = modified_user
        if definition is not UNSET:
            field_dict["definition"] = definition
        if report_types is not UNSET:
            field_dict["report_types"] = report_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.team_transformation_output_definition import TeamTransformationOutputDefinition
        from ..models.transformation_user_output import TransformationUserOutput

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        data_source_id = d.pop("data_source_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        description = d.pop("description", UNSET)

        _field_type = d.pop("field_type", UNSET)
        field_type: TeamTransformationOutputFieldType | Unset
        if isinstance(_field_type, Unset):
            field_type = UNSET
        else:
            field_type = check_team_transformation_output_field_type(_field_type)

        data_type = d.pop("data_type", UNSET)

        _modified_time_utc = d.pop("modified_time_utc", UNSET)
        modified_time_utc: datetime.datetime | Unset
        if isinstance(_modified_time_utc, Unset):
            modified_time_utc = UNSET
        else:
            modified_time_utc = datetime.datetime.fromisoformat(_modified_time_utc)

        _modified_user = d.pop("modified_user", UNSET)
        modified_user: TransformationUserOutput | Unset
        if isinstance(_modified_user, Unset):
            modified_user = UNSET
        else:
            modified_user = TransformationUserOutput.from_dict(_modified_user)

        _definition = d.pop("definition", UNSET)
        definition: TeamTransformationOutputDefinition | Unset
        if isinstance(_definition, Unset):
            definition = UNSET
        else:
            definition = TeamTransformationOutputDefinition.from_dict(_definition)

        report_types = cast(list[str], d.pop("report_types", UNSET))

        team_transformation_output = cls(
            id=id,
            name=name,
            data_source_id=data_source_id,
            display_name=display_name,
            description=description,
            field_type=field_type,
            data_type=data_type,
            modified_time_utc=modified_time_utc,
            modified_user=modified_user,
            definition=definition,
            report_types=report_types,
        )

        team_transformation_output.additional_properties = d
        return team_transformation_output

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
